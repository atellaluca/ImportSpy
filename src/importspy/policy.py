"""Validated contract schema and pure evidence policy evaluation."""

from hashlib import sha256
from pathlib import Path
from typing import Literal

from packaging.specifiers import InvalidSpecifier, SpecifierSet
from packaging.utils import canonicalize_name
from pydantic import Field, ValidationError, field_validator
from ruamel.yaml import YAML
from ruamel.yaml.error import YAMLError

from .dependencies import DependencyOptions, DependencyRule, evaluate_dependencies
from .domain import AdmissionContext, Dependency, Evidence, Record, Violation
from .inspection import SourceInspection, evaluate_structure
from .models import SpyModel


class ContractError(ValueError):
    """The policy cannot be interpreted; callers should use exit code 2."""


class RuntimePolicy(Record):
    python: str | None = None
    os: list[str] = Field(default_factory=list)
    architecture: list[str] = Field(default_factory=list)
    implementation: list[str] = Field(default_factory=list)
    environment: dict[str, str | None] = Field(default_factory=dict)

    @field_validator("python")
    @classmethod
    def valid_python(cls, value: str | None) -> str | None:
        if value is not None:
            try:
                SpecifierSet(value)
            except InvalidSpecifier as exc:
                raise ValueError("python must be a PEP 440 version range") from exc
        return value


class EvidenceRequirement(Record):
    kind: str
    subject: str
    provider: str | None = None
    status: Literal["verified", "observed"] = "verified"


class AdmissionPolicy(SpyModel):
    """0.5 extends SpyModel's structural fields; version remains module version."""

    schema_version: Literal[1] = 1
    policy_id: str | None = None
    runtime: RuntimePolicy = Field(default_factory=RuntimePolicy)
    dependencies: dict[str, DependencyRule] = Field(default_factory=dict)
    dependency_options: DependencyOptions = Field(default_factory=DependencyOptions)
    evidence_requirements: list[EvidenceRequirement] = Field(default_factory=list)

    @field_validator("dependencies")
    @classmethod
    def distinct_names(
        cls, rules: dict[str, DependencyRule]
    ) -> dict[str, DependencyRule]:
        names = []
        for key in rules:
            if key.startswith("import:"):
                if not key.removeprefix("import:").isidentifier():
                    raise ValueError(
                        "import policy keys must name one top-level identifier"
                    )
                names.append(key)
            else:
                names.append(canonicalize_name(key, validate=True))
        if len(set(names)) != len(names):
            raise ValueError("duplicate normalized dependency names")
        return rules


def load_policy(path: Path) -> tuple[AdmissionPolicy, str]:
    try:
        raw = path.read_bytes()
        data = YAML(typ="safe").load(raw)
        if not isinstance(data, dict):
            raise ContractError("Contract must be a YAML mapping.")
        policy = AdmissionPolicy.model_validate(data)
    except ValidationError as exc:
        # Pydantic's default error includes input values, potentially secrets.
        details = "; ".join(
            f"{'.'.join(map(str, item['loc']))}: {item['type']}"
            for item in exc.errors(include_input=False, include_url=False)
        )
        raise ContractError(f"Invalid contract fields: {details}") from None
    except (OSError, YAMLError, UnicodeError, ValueError) as exc:
        if isinstance(exc, ContractError):
            raise
        raise ContractError(f"Cannot read contract ({type(exc).__name__}).") from None
    return policy, sha256(raw).hexdigest()


def collect_runtime_evidence(
    policy: AdmissionPolicy, context: AdmissionContext
) -> list[Evidence]:
    """Inspect host facts only; environment values are never serialized."""
    import os

    items = [
        Evidence(
            kind=f"runtime.{key}",
            subject=str(context.subject),
            observed=value,
            phase="runtime",
            status="verified",
        )
        for key, value in context.environment.items()
    ]
    for name, expected in policy.runtime.environment.items():
        observed = os.environ.get(name)
        items.append(
            Evidence(
                kind="runtime.environment",
                subject=name,
                observed=observed is not None
                and (expected is None or observed == expected),
                expected=True,
                phase="runtime",
                status="verified",
            )
        )
    for deployment_index, deployment in enumerate(policy.deployments or []):
        for system_index, system in enumerate(deployment.systems):
            if system.environment:
                for variable in system.environment.variables or []:
                    value = os.environ.get(variable.name)
                    items.append(
                        Evidence(
                            kind="runtime.legacy_environment",
                            subject=variable.name,
                            observed=value is not None
                            and (
                                variable.value is None or value == str(variable.value)
                            ),
                            expected=True,
                            phase="runtime",
                            status="verified",
                            detail=f"deployment:{deployment_index}/system:{system_index}",
                        )
                    )
                for name in system.environment.secrets or []:
                    items.append(
                        Evidence(
                            kind="runtime.secret.present",
                            subject=name,
                            observed=name in os.environ,
                            expected=True,
                            phase="runtime",
                            status="verified",
                        )
                    )
    return items


def _runtime_violations(
    policy: AdmissionPolicy,
    context: AdmissionContext,
    evidence: list[Evidence],
    inspection: SourceInspection,
) -> list[Violation]:
    runtime = policy.runtime
    host = context.environment
    violations = []
    for name, allowed in (
        ("os", runtime.os),
        ("architecture", runtime.architecture),
        ("implementation", runtime.implementation),
    ):
        if allowed and host.get(name) not in allowed:
            violations.append(
                Violation(
                    code="ISPY-R101",
                    category="runtime",
                    phase="runtime",
                    subject=str(context.subject),
                    message=f"Host {name} is not permitted.",
                    expected=list(allowed),
                    observed=host.get(name),
                )
            )
    if runtime.python and not SpecifierSet(runtime.python).contains(
        host["python"], prereleases=True
    ):
        violations.append(
            Violation(
                code="ISPY-R102",
                category="runtime",
                phase="runtime",
                subject=str(context.subject),
                message="Host Python version is not permitted.",
                expected=runtime.python,
                observed=host["python"],
            )
        )
    for item in evidence:
        if (
            item.kind == "runtime.environment"
            and item.provider == "importspy"
            and item.observed is not True
        ):
            violations.append(
                Violation(
                    code="ISPY-R103",
                    category="runtime",
                    phase="runtime",
                    subject=item.subject,
                    message="Required environment variable is missing or differs (value redacted).",
                )
            )
    if policy.deployments:
        alternatives: list[list[Violation]] = []
        for deployment_index, deployment in enumerate(policy.deployments):
            if deployment.arch.value != host["architecture"]:
                continue
            for system_index, system in enumerate(deployment.systems):
                if system.os.value != host["os"]:
                    continue
                for python in system.pythons:
                    if python.version and python.version != host["python"]:
                        continue
                    if (
                        python.interpreter
                        and python.interpreter.value != host["implementation"]
                    ):
                        continue
                    failures: list[Violation] = []
                    # Legacy nested modules constrain this target; they are not imports to execute.
                    for module in python.modules:
                        failures.extend(evaluate_structure(module, inspection))
                    if system.environment:
                        for variable in system.environment.variables or []:
                            matches = [
                                item
                                for item in evidence
                                if item.kind == "runtime.legacy_environment"
                                and item.subject == variable.name
                                and item.provider == "importspy"
                                and item.detail
                                == f"deployment:{deployment_index}/system:{system_index}"
                            ]
                            if not matches or not any(
                                item.observed is True for item in matches
                            ):
                                failures.append(
                                    Violation(
                                        code="ISPY-R103",
                                        category="runtime",
                                        phase="runtime",
                                        subject=variable.name,
                                        message="Legacy environment requirement failed (value redacted).",
                                    )
                                )
                        for name in system.environment.secrets or []:
                            if not any(
                                item.kind == "runtime.secret.present"
                                and item.provider == "importspy"
                                and item.subject == name
                                and item.status == "verified"
                                and item.observed is True
                                for item in evidence
                            ):
                                failures.append(
                                    Violation(
                                        code="ISPY-R103",
                                        category="runtime",
                                        phase="runtime",
                                        subject=name,
                                        message="Required secret is absent (value redacted).",
                                    )
                                )
                    alternatives.append(failures)
        if not alternatives:
            violations.append(
                Violation(
                    code="ISPY-R104",
                    category="runtime",
                    phase="runtime",
                    subject=str(context.subject),
                    message="No legacy deployment matches this host.",
                )
            )
        elif not any(not failures for failures in alternatives):
            best = alternatives[0]
            for alternative in alternatives[1:]:
                if len(alternative) < len(best):
                    best = alternative
            violations.extend(best)
    return violations


class PolicyEngine:
    """Evaluate already collected facts. No filesystem, imports or network operations."""

    def evaluate(
        self,
        policy: AdmissionPolicy,
        inspection: SourceInspection,
        dependencies: list[Dependency],
        evidence: list[Evidence],
        context: AdmissionContext,
    ) -> list[Violation]:
        violations = evaluate_structure(policy, inspection)
        violations.extend(
            evaluate_dependencies(
                dependencies,
                policy.dependencies,
                policy.dependency_options,
                str(context.subject),
            )
        )
        violations.extend(_runtime_violations(policy, context, evidence, inspection))
        requirements = list(policy.evidence_requirements)
        for name, rule in policy.dependencies.items():
            provenance = rule.provenance
            required = (
                provenance if isinstance(provenance, bool) else provenance.required
            )
            if not required:
                continue
            if name.startswith("import:"):
                matches = [
                    dep
                    for dep in dependencies
                    if f"import:{dep.reference.name.partition('.')[0]}" == name
                ]
                subjects = {dist.name for dep in matches for dist in dep.distributions}
                if matches and not subjects:
                    subjects = {
                        name
                    }  # No distribution identity can establish provenance.
            else:
                normalized = canonicalize_name(name)
                subjects = {
                    dist.name
                    for dep in dependencies
                    for dist in dep.distributions
                    if dist.name == normalized
                }
            for subject in sorted(subjects):
                requirements.append(
                    EvidenceRequirement(kind="distribution.provenance", subject=subject)
                )
        for requirement in requirements:
            if not any(
                item.kind == requirement.kind
                and item.subject == requirement.subject
                and (
                    item.status == requirement.status
                    or (requirement.status == "observed" and item.status == "verified")
                )
                and bool(item.observed)
                and (
                    requirement.provider is None
                    or item.provider == requirement.provider
                )
                for item in evidence
            ):
                violations.append(
                    Violation(
                        code="ISPY-P101",
                        category="evidence",
                        phase="external",
                        subject=requirement.subject,
                        message=f"Required {requirement.kind} evidence is unavailable or insufficient.",
                        expected=requirement.status,
                        remediation="Select a trusted evidence provider explicitly, or revise the policy.",
                    )
                )
        return violations
