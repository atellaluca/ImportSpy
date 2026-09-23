"""Metadata-only dependency resolution and deterministic dependency policy."""

import json
import re
import sys
from pathlib import Path
from typing import Literal
from urllib.parse import urlsplit, urlunsplit

from packaging.requirements import InvalidRequirement, Requirement
from packaging.specifiers import SpecifierSet
from packaging.utils import canonicalize_name
from packaging.version import InvalidVersion, Version
from pydantic import JsonValue, field_validator

from importspy.domain import (
    Dependency, Distribution, Evidence, ImportReference, Location, Origin, Record,
    Violation,
)

if sys.version_info >= (3, 11):
    from importlib import metadata

    import tomllib
else:
    # Python 3.10's stdlib mapping ignores wheels without top_level.txt.
    # The maintained backport also infers import names from RECORD metadata.
    import importlib_metadata as metadata
    import tomli as tomllib


def normalize_url(value: str, *, repository: bool = False) -> str | None:
    """Normalize an origin URL while removing userinfo, query and fragment."""
    if not value or any(ord(char) < 33 for char in value):
        return None
    try:
        parts = urlsplit(value)
        if parts.scheme.lower() not in {"https", "http", "ssh", "git", "file", "ftp"}:
            return None
        host = (parts.hostname or "").lower()
        if parts.scheme != "file" and not host:
            return None
        if ":" in host:
            host = f"[{host}]"
        port = parts.port
        if port is not None and (parts.scheme, port) not in {("https", 443), ("http", 80)}:
            host += f":{port}"
        path = parts.path.rstrip("/")
        if repository and path.endswith(".git"):
            path = path[:-4]
        return urlunsplit((parts.scheme.lower(), host, path, "", ""))
    except ValueError:
        return None


class OriginRule(Record):
    type: Literal["unknown", "index", "vcs", "local", "archive"] | None = None
    repository: str | None = None
    url: str | None = None
    commit: str | None = None

    @field_validator("repository", "url")
    @classmethod
    def valid_url(cls, value: str | None) -> str | None:
        if value is not None and normalize_url(value) is None:
            raise ValueError("origin URLs must be absolute supported URLs")
        return value


class ProvenanceRule(Record):
    required: bool = False


class DependencyRule(Record):
    allowed: bool = True
    required: bool = False
    version: str | None = None
    declared: bool | None = None
    origin: OriginRule | None = None
    editable: bool | None = None
    provenance: bool | ProvenanceRule = False

    @field_validator("version")
    @classmethod
    def valid_specifier(cls, value: str | None) -> str | None:
        if value is not None:
            SpecifierSet(value)
        return value


class DependencyOptions(Record):
    unresolved: Literal["allow", "deny"] = "deny"
    undeclared: Literal["allow", "deny"] = "allow"
    unlisted: Literal["allow", "deny"] = "allow"


def read_origin(raw: str | None) -> Origin:
    """Read untrusted PEP 610 metadata; missing or malformed data stays unknown."""
    if raw is None:
        return Origin()
    try:
        data = json.loads(raw)
        if not isinstance(data, dict) or not isinstance(data.get("url"), str):
            return Origin()
        url = normalize_url(data["url"])
        kinds = [key for key in ("vcs_info", "dir_info", "archive_info") if key in data]
        if url is None or len(kinds) != 1:
            return Origin()
        info = data[kinds[0]]
        if not isinstance(info, dict):
            return Origin()
        if kinds[0] == "vcs_info":
            if not all(isinstance(info.get(key), str) and info[key] for key in ("vcs", "commit_id")):
                return Origin()
            return Origin(
                type="vcs", url=url, repository=normalize_url(url, repository=True),
                commit=info["commit_id"], editable=False,
            )
        if kinds[0] == "dir_info":
            editable = info.get("editable", False)
            if not isinstance(editable, bool) or not url.startswith("file:"):
                return Origin()
            return Origin(type="local", url=url, editable=editable)
        hashes = info.get("hashes", {})
        if not isinstance(hashes, dict):
            return Origin()
        legacy_hash = info.get("hash")
        if isinstance(legacy_hash, str) and "=" in legacy_hash:
            algorithm, digest = legacy_hash.split("=", 1)
            hashes = {algorithm: digest, **hashes}
        if not all(
            isinstance(key, str) and re.fullmatch(r"[A-Za-z0-9_+-]+", key)
            and isinstance(value, str) and re.fullmatch(r"[a-fA-F0-9]+", value)
            for key, value in hashes.items()
        ):
            return Origin()
        return Origin(type="archive", url=url, editable=False, hashes=hashes)
    except (ValueError, TypeError, RecursionError):
        return Origin()


def _project_declarations(root: Path) -> set[str] | None:
    """Names mentioned by runtime or optional project dependencies, not activation."""
    try:
        data = tomllib.loads((root / "pyproject.toml").read_text(encoding="utf-8"))
        if "project" in data:
            project = data["project"]
            if not isinstance(project, dict):
                return None
            dynamic = project.get("dynamic", [])
            if not isinstance(dynamic, list) or {"dependencies", "optional-dependencies"}.intersection(dynamic):
                return None
            requirements = project.get("dependencies", [])
            optional = project.get("optional-dependencies", {})
            if not isinstance(requirements, list) or not isinstance(optional, dict):
                return None
            requirements = list(requirements)
            for group in optional.values():
                if not isinstance(group, list):
                    return None
                requirements.extend(group)
            return {str(canonicalize_name(Requirement(item).name)) for item in requirements}
        poetry = data.get("tool", {}).get("poetry", {})
        requirements = poetry.get("dependencies")
        if isinstance(requirements, dict):
            if any(not isinstance(value, (str, dict, list)) for value in requirements.values()):
                return None
            return {str(canonicalize_name(name, validate=True)) for name in requirements if name != "python"}
    except (OSError, ValueError, TypeError, AttributeError, InvalidRequirement):
        pass
    return None


class DependencyResolver:
    """Resolve using source paths and installed metadata, never target imports.

    Each instance is a metadata snapshot: reuse for a batch, recreate after installs.
    Custom metadata finders already installed in the host are part of its trust boundary.
    """

    def __init__(self, project_root: Path):
        self.project_root = project_root.resolve()
        self._mapping: dict[str, list[str]] | None = None
        self._distributions: dict[str, Distribution | None] = {}
        self._declarations = _project_declarations(self.project_root)

    def _distribution(self, name: str) -> Distribution | None:
        name = str(canonicalize_name(name))
        if name not in self._distributions:
            try:
                dist = metadata.distribution(name)
                actual_name = dist.metadata["Name"]
                if not isinstance(actual_name, str) or canonicalize_name(actual_name) != name:
                    self._distributions[name] = None
                else:
                    self._distributions[name] = Distribution(
                        name=name, version=dist.version or None,
                        origin=read_origin(dist.read_text("direct_url.json")),
                        declared=name in self._declarations if self._declarations is not None else None,
                    )
            except (OSError, ValueError, TypeError, KeyError, metadata.PackageNotFoundError):
                self._distributions[name] = None
        return self._distributions[name]

    def _local_kind(
        self, reference: ImportReference, subject: Path,
    ) -> Literal["internal", "namespace", "unresolved"] | None:
        parts = reference.name.split(".") if reference.name else []
        if any(not part.isidentifier() for part in parts):
            return None
        roots: tuple[Path, ...]
        if reference.level:
            base = subject.resolve().parent
            for _ in range(reference.level - 1):
                base = base.parent
            roots = (base,)
        else:
            roots = (self.project_root / "src", self.project_root, subject.resolve().parent)
        namespace = False
        for root in roots:
            path = root.joinpath(*parts)
            top = root / parts[0] if parts else root
            candidates = [path.with_suffix(".py"), path]
            # A regular top-level module/package shadows installed submodules too.
            if not reference.level:
                candidates = [top.with_suffix(".py"), top / "__init__.py", *candidates]
            for candidate in candidates:
                try:
                    if not (candidate.is_file() or candidate.is_dir()):
                        continue
                    candidate.resolve().relative_to(self.project_root)
                    if reference.level or top.with_suffix(".py").is_file() or (top / "__init__.py").is_file():
                        return "internal"
                    namespace = True
                except (ValueError, OSError, RuntimeError):
                    return "unresolved"
        return "namespace" if namespace else None

    def resolve(self, references: list[ImportReference], subject: Path) -> list[Dependency]:
        result: list[Dependency] = []
        for reference in references:
            top = reference.name.partition(".")[0]
            if not reference.level and top in sys.builtin_module_names:
                result.append(Dependency(reference=reference, kind="stdlib"))
                continue
            local_kind = self._local_kind(reference, subject)
            if local_kind in {"internal", "unresolved"}:
                result.append(Dependency(
                    reference=reference, kind=local_kind,
                    detail="A local import path escapes the project root." if local_kind == "unresolved" else None,
                ))
                continue
            if not reference.level and top in sys.stdlib_module_names:
                result.append(Dependency(reference=reference, kind="stdlib"))
                continue
            if self._mapping is None:
                try:
                    self._mapping = dict(metadata.packages_distributions())
                except (OSError, ValueError, TypeError, KeyError):
                    self._mapping = {}
            candidates = [] if reference.level else self._mapping.get(top, [])
            mapping_complete = isinstance(candidates, (list, tuple))
            if not isinstance(candidates, (list, tuple)):
                candidates = []
            names = []
            for candidate in candidates:
                try:
                    if not isinstance(candidate, str):
                        raise ValueError("invalid distribution name")
                    names.append(str(canonicalize_name(candidate, validate=True)))
                except ValueError:
                    mapping_complete = False
            names = sorted(set(names))
            distributions = [dist for name in names if (dist := self._distribution(name)) is not None]
            if not names and mapping_complete and local_kind == "namespace":
                result.append(Dependency(reference=reference, kind="internal"))
                continue
            if not mapping_complete or not distributions or len(distributions) != len(names):
                result.append(Dependency(
                    reference=reference, kind="unresolved", distributions=distributions,
                    detail="No complete installed distribution mapping or local source was found.",
                ))
                continue
            kind: Literal["namespace", "direct", "external"] = "external"
            if len(distributions) > 1 or local_kind == "namespace":
                kind = "namespace"
            elif distributions[0].origin.type in {"vcs", "local", "archive"}:
                kind = "direct"
            declared = None if self._declarations is None else all(dist.declared for dist in distributions)
            result.append(Dependency(
                reference=reference, kind=kind, distributions=distributions, declared=declared,
                detail="Local namespace source and installed contributors were both found." if local_kind == "namespace" else None,
            ))
        return result


def collect_dependency_evidence(dependencies: list[Dependency]) -> list[Evidence]:
    evidence: list[Evidence] = []
    seen: set[str] = set()
    for dependency in dependencies:
        evidence.append(Evidence(
            kind="dependency.classification", subject=dependency.reference.name,
            observed=dependency.kind,
            status="unknown" if dependency.kind == "unresolved" else "observed",
            detail=dependency.detail,
        ))
        for dist in dependency.distributions:
            if dist.name in seen:
                continue
            seen.add(dist.name)
            for kind, observed in (
                ("version", dist.version), ("declared", dist.declared),
                ("origin", dist.origin.model_dump(mode="json")), ("editable", dist.origin.editable),
            ):
                evidence.append(Evidence(
                    kind=f"dependency.{kind}", subject=dist.name, observed=observed,
                    provider="importspy.metadata",
                    status="unknown" if observed is None or (kind == "origin" and dist.origin.type == "unknown") else "observed",
                ))
    return evidence


def _rule_violations(
    dependency: Dependency, distribution: Distribution | None,
    key: str, rule: DependencyRule, subject: str,
) -> list[Violation]:
    violations: list[Violation] = []
    location = Location(path=subject, line=dependency.reference.line, column=dependency.reference.column)

    def add(code: str, message: str, expected: JsonValue, observed: JsonValue) -> None:
        violations.append(Violation(
            code=code, category="dependency", subject=key, message=message,
            expected=expected, observed=observed, location=location,
            remediation="Update the dependency installation or the admission contract.",
        ))

    if not rule.allowed:
        add("ISPY-D101", f"Dependency `{key}` is not permitted by policy.", "absent", "observed")
    if rule.version is not None:
        version = distribution.version if distribution else None
        try:
            valid = version is not None and SpecifierSet(rule.version).contains(Version(version))
        except InvalidVersion:
            valid = False
        if not valid:
            add("ISPY-D104", f"Dependency `{key}` does not satisfy version {rule.version}.", rule.version, version)
    declared = distribution.declared if distribution else dependency.declared
    if rule.declared is not None and declared is not rule.declared:
        add("ISPY-D105", f"Declaration requirement for `{key}` was not established.", rule.declared, declared)
    origin = distribution.origin if distribution else Origin()
    if rule.editable is not None and origin.editable is not rule.editable:
        add("ISPY-D107", f"Editable installation requirement for `{key}` was not established.", rule.editable, origin.editable)
    if rule.origin is not None:
        for field, expected in rule.origin.model_dump(exclude_none=True).items():
            observed = getattr(origin, field)
            if field in {"repository", "url"}:
                expected = normalize_url(expected, repository=field == "repository")
                observed = normalize_url(observed, repository=field == "repository") if observed else None
            if expected != observed:
                add("ISPY-D106", f"Dependency `{key}` has an unexpected or unknown origin {field}.", expected, observed)
    return violations


def evaluate_dependencies(
    deps: list[Dependency], rules: dict[str, DependencyRule],
    options: DependencyOptions, subject: str,
) -> list[Violation]:
    """Evaluate collected facts without IO. Provenance uses the evidence policy layer."""
    normalized = [
        (key if key.startswith("import:") else str(canonicalize_name(key)), rule)
        for key, rule in sorted(rules.items())
    ]
    observed: set[str] = set()
    violations: list[Violation] = []
    for dep in deps:
        import_key = f"import:{dep.reference.name.partition('.')[0]}"
        observed.add(import_key)
        location = Location(path=subject, line=dep.reference.line, column=dep.reference.column)
        if dep.kind == "unresolved" and options.unresolved == "deny":
            violations.append(Violation(
                code="ISPY-D102", category="dependency", subject=dep.reference.name,
                message=f"Import `{dep.reference.name}` could not be resolved.", location=location,
                expected="resolved", observed="unresolved",
                remediation="Install the dependency or explicitly allow unresolved imports.",
            ))
        for key, rule in normalized:
            if key == import_key:
                if dep.distributions:
                    for dist in dep.distributions:
                        violations.extend(_rule_violations(dep, dist, key, rule, subject))
                else:
                    violations.extend(_rule_violations(dep, None, key, rule, subject))
        for dist in dep.distributions:
            name = str(canonicalize_name(dist.name))
            observed.add(name)
            matched = [(key, rule) for key, rule in normalized if key == name]
            if not matched and options.unlisted == "deny":
                violations.append(Violation(
                    code="ISPY-D108", category="dependency", subject=name,
                    message=f"Dependency `{name}` has no distribution policy entry.", location=location,
                    expected="listed", observed="unlisted",
                ))
            if options.undeclared == "deny" and dist.declared is not True:
                violations.append(Violation(
                    code="ISPY-D105", category="dependency", subject=name,
                    message=f"Dependency `{name}` is undeclared or its declaration context is unknown.",
                    location=location, expected=True, observed=dist.declared,
                ))
            for key, rule in matched:
                violations.extend(_rule_violations(dep, dist, key, rule, subject))
    for key, rule in normalized:
        if rule.required and key not in observed:
            violations.append(Violation(
                code="ISPY-D103", category="dependency", subject=key,
                message=f"Required dependency `{key}` was not observed in source.",
                expected="observed", observed="absent",
                remediation="Declare and import the required dependency or revise the contract.",
            ))
    return violations
