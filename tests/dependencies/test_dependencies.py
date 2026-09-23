import json
import sys
import pytest
from pydantic import ValidationError

from importspy.dependencies import (
    DependencyOptions, DependencyResolver, DependencyRule, OriginRule,
    collect_dependency_evidence, evaluate_dependencies, metadata, normalize_url, read_origin,
)
from importspy.domain import Dependency, Distribution, ImportReference, Origin


@pytest.fixture
def installed(tmp_path, monkeypatch):
    """Real dist-info records, separate from the inspected project, with no imports."""
    site = tmp_path / "site-packages"
    site.mkdir()
    project = tmp_path / "project"
    project.mkdir()
    monkeypatch.setattr(sys, "path", [str(site), *sys.path])

    def install(name, import_name, version="1.2.0", origin=None):
        dist_info = site / f"{name.replace('-', '_')}-{version}.dist-info"
        dist_info.mkdir()
        (dist_info / "METADATA").write_text(
            f"Metadata-Version: 2.1\nName: {name}\nVersion: {version}\n", encoding="utf-8"
        )
        (dist_info / "top_level.txt").write_text(import_name + "\n", encoding="utf-8")
        (dist_info / "RECORD").write_text(f"{import_name}/__init__.py,,\n", encoding="utf-8")
        package = site / import_name
        package.mkdir(exist_ok=True)
        (package / "__init__.py").write_text("raise RuntimeError('TARGET EXECUTED')\n", encoding="utf-8")
        if origin is not None:
            (dist_info / "direct_url.json").write_text(json.dumps(origin), encoding="utf-8")
        return dist_info

    return project, install


def resolve(project, *names):
    return DependencyResolver(project).resolve(
        [ImportReference(name=name) for name in names], project / "plugin.py"
    )


def test_metadata_name_mismatch_many_to_many_and_no_import(installed):
    project, install = installed
    install("ISP-Yaml", "ispy_yaml")
    install("ISP-Namespace-One", "ispy_namespace")
    install("ISP-Namespace-Two", "ispy_namespace")
    deps = resolve(project, "ispy_yaml", "ispy_namespace.child", "ispy_missing_xyz")
    assert [dep.kind for dep in deps] == ["external", "namespace", "unresolved"]
    assert deps[0].distributions[0].name == "isp-yaml"
    assert [dist.name for dist in deps[1].distributions] == ["isp-namespace-one", "isp-namespace-two"]
    assert "ispy_yaml" not in sys.modules
    assert "ispy_namespace" not in sys.modules


def test_record_only_wheels_resolve_namespaces_without_importing(installed):
    project, install = installed
    for name, import_name in [
        ("ISP-Record", "ispy_record"),
        ("ISP-Record-One", "ispy_record_namespace"),
        ("ISP-Record-Two", "ispy_record_namespace"),
    ]:
        dist_info = install(name, import_name)
        (dist_info / "top_level.txt").unlink()

    deps = resolve(project, "ispy_record", "ispy_record_namespace.child")
    assert [dep.kind for dep in deps] == ["external", "namespace"]
    assert deps[0].distributions[0].name == "isp-record"
    assert [dist.name for dist in deps[1].distributions] == ["isp-record-one", "isp-record-two"]
    assert "ispy_record" not in sys.modules
    assert "ispy_record_namespace" not in sys.modules


def test_source_and_stdlib_paths_never_find_spec(tmp_path, monkeypatch):
    import importlib.util

    def forbidden(*args, **kwargs):
        raise AssertionError("find_spec must not run")

    monkeypatch.setattr(importlib.util, "find_spec", forbidden)
    (tmp_path / "local.py").write_text("raise RuntimeError()")
    (tmp_path / "json.py").write_text("raise RuntimeError()")
    (tmp_path / "src" / "mypkg").mkdir(parents=True)
    (tmp_path / "src" / "mypkg" / "__init__.py").write_text("raise RuntimeError()")
    (tmp_path / "src" / "mypkg" / "child.py").write_text("raise RuntimeError()")
    deps = resolve(tmp_path, "sys", "pathlib", "local", "json", "json.tool", "mypkg.child")
    assert [dep.kind for dep in deps] == ["stdlib", "stdlib", "internal", "internal", "internal", "internal"]
    relative = DependencyResolver(tmp_path).resolve(
        [ImportReference(name="child", level=1), ImportReference(name="absent", level=1)],
        tmp_path / "src" / "mypkg" / "plugin.py",
    )
    assert [dep.kind for dep in relative] == ["internal", "unresolved"]


def test_metadata_cached_per_resolver(installed, monkeypatch):
    project, install = installed
    install("ISP-Cached", "ispy_cached")
    actual_mapping = metadata.packages_distributions
    actual_distribution = metadata.distribution
    calls = {"mapping": 0, "distribution": 0}

    def mapping():
        calls["mapping"] += 1
        return actual_mapping()

    def distribution(name):
        calls["distribution"] += 1
        return actual_distribution(name)

    monkeypatch.setattr(metadata, "packages_distributions", mapping)
    monkeypatch.setattr(metadata, "distribution", distribution)
    resolver = DependencyResolver(project)
    for _ in range(2):
        resolver.resolve([ImportReference(name="ispy_cached"), ImportReference(name="ispy_cached.sub")], project / "plugin.py")
    assert calls == {"mapping": 1, "distribution": 1}


@pytest.mark.parametrize("raw", [None, "not json", "null", "[]", '{"url": []}', '{"url":"https://x", "vcs_info": []}', '{"url":"https://x", "dir_info": {}}'])
def test_malformed_metadata_stays_unknown(raw):
    assert read_origin(raw).type == "unknown"


def test_vcs_url_redaction_normalization_and_origin_policy(installed):
    project, install = installed
    install("ISP-Vcs", "ispy_vcs", origin={
        "url": "https://user:SECRET@EXAMPLE.com:443/acme/sdk.git?token=SECRET#SECRET",
        "vcs_info": {"vcs": "git", "commit_id": "abc123", "requested_revision": "main"},
    })
    dep = resolve(project, "ispy_vcs")[0]
    origin = dep.distributions[0].origin
    assert dep.kind == "direct"
    assert origin.repository == "https://example.com/acme/sdk"
    assert origin.commit == "abc123"
    assert "SECRET" not in dep.model_dump_json()
    rule = DependencyRule(origin=OriginRule(type="vcs", repository="https://EXAMPLE.com/acme/sdk.git/"), editable=False)
    assert evaluate_dependencies([dep], {"ISP_VCS": rule}, DependencyOptions(), str(project / "plugin.py")) == []
    rule.origin.repository = "https://example.com/other"
    assert evaluate_dependencies([dep], {"isp-vcs": rule}, DependencyOptions(), "plugin.py")[0].code == "ISPY-D106"


@pytest.mark.parametrize("editable", [True, False])
def test_local_editable_metadata(installed, editable):
    project, install = installed
    install("ISP-Local", "ispy_local", origin={"url": "file:///opt/project", "dir_info": {"editable": editable}})
    dep = resolve(project, "ispy_local")[0]
    assert dep.kind == "direct"
    assert dep.distributions[0].origin.editable is editable
    violations = evaluate_dependencies([dep], {"isp-local": DependencyRule(editable=not editable)}, DependencyOptions(), "plugin.py")
    assert violations[0].code == "ISPY-D107"


def test_archive_hashes_and_no_pypi_inference():
    origin = read_origin(json.dumps({
        "url": "https://example.com/sdk.whl?secret=hidden", "archive_info": {"hashes": {"sha256": "abcd"}}
    }))
    assert origin.type == "archive"
    assert origin.hashes == {"sha256": "abcd"}
    assert origin.url == "https://example.com/sdk.whl"
    assert read_origin(None) == Origin()
    assert read_origin(json.dumps({"url": "https://example.com/x", "archive_info": {"hashes": []}})).type == "unknown"
    assert normalize_url("https://host:broken/path") is None
    assert normalize_url("https://host/\nsecret") is None


def test_pep621_optional_marker_and_namespace_declarations(installed):
    project, install = installed
    install("ISP-Declared", "ispy_shared")
    install("ISP-Transitive", "ispy_shared")
    install("ISP-Optional", "ispy_optional")
    (project / "pyproject.toml").write_text('''
[project]
name = "example"
dependencies = ["ISP-Declared[feature]>=1; python_version < '1'"]
[project.optional-dependencies]
test = ["ISP-Optional>=1"]
''')
    shared, optional = resolve(project, "ispy_shared", "ispy_optional")
    assert shared.declared is False
    assert [dist.declared for dist in shared.distributions] == [True, False]
    assert optional.declared is True
    violations = evaluate_dependencies([shared], {"isp-declared": DependencyRule(declared=True)}, DependencyOptions(), "plugin.py")
    assert violations == []
    violations = evaluate_dependencies([shared], {}, DependencyOptions(undeclared="deny"), "plugin.py")
    assert [violation.subject for violation in violations] == ["isp-transitive"]


@pytest.mark.parametrize("content", ["", "malformed [", '[project]\ndynamic=["dependencies"]', '[project]\ndependencies=["not a requirement ^"]'])
def test_unknown_declarations_fail_closed_if_required(installed, content):
    project, install = installed
    install("ISP-Unknown", "ispy_unknown")
    (project / "pyproject.toml").write_text(content)
    dep = resolve(project, "ispy_unknown")[0]
    assert dep.declared is None
    violations = evaluate_dependencies([dep], {}, DependencyOptions(undeclared="deny"), "plugin.py")
    assert violations[0].code == "ISPY-D105"


def test_poetry_runtime_declarations_exclude_development_groups(installed):
    project, install = installed
    install("ISP-Runtime", "ispy_runtime")
    install("ISP-Dev", "ispy_dev")
    (project / "pyproject.toml").write_text('''
[tool.poetry.dependencies]
python = "^3.10"
ISP-Runtime = {version="^1.0", optional=true}
[tool.poetry.group.dev.dependencies]
ISP-Dev = "^1.0"
''')
    deps = resolve(project, "ispy_runtime", "ispy_dev")
    assert [dep.declared for dep in deps] == [True, False]


def external(version="2.5", declared=True):
    return Dependency(
        reference=ImportReference(name="yaml", line=4, column=2), kind="external", declared=declared,
        distributions=[Distribution(name="pyyaml", version=version, declared=declared)],
    )


def test_allow_deny_required_version_and_locations():
    deps = [external()]
    rules = {"PyYAML": DependencyRule(version=">=2,<3", required=True)}
    assert evaluate_dependencies(deps, rules, DependencyOptions(), "plugin.py") == []
    rules = {"PyYAML": DependencyRule(allowed=False, version=">=3"), "missing": DependencyRule(required=True)}
    violations = evaluate_dependencies(deps, rules, DependencyOptions(), "plugin.py")
    assert {violation.code for violation in violations} == {"ISPY-D101", "ISPY-D103", "ISPY-D104"}
    assert violations[0].location.path == "plugin.py"
    assert violations[0].location.line == 4
    assert violations[-1].location is None


@pytest.mark.parametrize("version", [None, "not-a-version", "3.0", "2.0rc1"])
def test_version_unknown_invalid_and_prerelease(version):
    violations = evaluate_dependencies([external(version)], {"pyyaml": DependencyRule(version=">=2,<3")}, DependencyOptions(), "plugin.py")
    assert violations[0].code == "ISPY-D104"


def test_invalid_version_policy_is_configuration_error():
    with pytest.raises(ValidationError):
        DependencyRule(version="^1.0")


def test_import_rules_and_unresolved_optional_policy():
    dep = Dependency(reference=ImportReference(name="missing.sub", optional=True), kind="unresolved")
    rule = DependencyRule(allowed=False, required=True)
    violations = evaluate_dependencies([dep], {"import:missing": rule}, DependencyOptions(), "plugin.py")
    assert {violation.code for violation in violations} == {"ISPY-D101", "ISPY-D102"}
    assert evaluate_dependencies([dep], {}, DependencyOptions(unresolved="allow"), "plugin.py") == []


def test_unlisted_applies_to_distributions_and_namespace_members():
    dep = external()
    dep.distributions.append(Distribution(name="other", version="1"))
    violations = evaluate_dependencies([dep], {"pyyaml": DependencyRule()}, DependencyOptions(unlisted="deny"), "plugin.py")
    assert [violation.subject for violation in violations] == ["other"]


def test_evidence_unknown_origin_is_not_verified():
    dep = external(declared=None)
    evidence = collect_dependency_evidence([dep, dep])
    by_kind = {item.kind: item for item in evidence}
    assert by_kind["dependency.origin"].status == "unknown"
    assert by_kind["dependency.declared"].status == "unknown"
    assert by_kind["dependency.version"].observed == "2.5"
    assert len([item for item in evidence if item.kind == "dependency.version"]) == 1


def test_missing_distribution_metadata_is_unresolved(tmp_path, monkeypatch):
    monkeypatch.setattr(metadata, "packages_distributions", lambda: {"missing": ["ispy-does-not-exist"]})
    assert resolve(tmp_path, "missing")[0].kind == "unresolved"


def test_symlink_outside_project_is_not_internal(tmp_path, monkeypatch):
    project = tmp_path / "project"
    project.mkdir()
    (tmp_path / "external.py").write_text("raise RuntimeError()")
    (project / "linked.py").symlink_to(tmp_path / "external.py")
    monkeypatch.setattr(metadata, "packages_distributions", lambda: {})
    assert resolve(project, "linked")[0].kind == "unresolved"


def test_local_regular_module_shadows_installed_distribution(installed):
    project, install = installed
    install("ISP-Shadow", "ispy_shadow")
    (project / "ispy_shadow.py").write_text("raise RuntimeError('TARGET EXECUTED')")
    deps = resolve(project, "ispy_shadow", "ispy_shadow.nested")
    assert all(dep.kind == "internal" and not dep.distributions for dep in deps)


def test_local_namespace_keeps_installed_contributors(installed):
    project, install = installed
    install("ISP-Shared", "ispy_shared")
    (project / "ispy_shared").mkdir()
    (project / "ispy_shared" / "local.py").write_text("raise RuntimeError('TARGET EXECUTED')")
    dep = resolve(project, "ispy_shared.local")[0]
    assert dep.kind == "namespace"
    assert [dist.name for dist in dep.distributions] == ["isp-shared"]


def test_external_mapping_does_not_claim_nested_submodule_exists(installed):
    project, install = installed
    install("ISP-Top", "ispy_top")
    dep = resolve(project, "ispy_top.nested.does_not_exist")[0]
    assert dep.kind == "external"
    assert dep.distributions[0].name == "isp-top"
    assert "ispy_top" not in sys.modules


def test_symlink_shadow_of_stdlib_is_unresolved(tmp_path):
    project = tmp_path / "project"
    project.mkdir()
    (tmp_path / "outside.py").write_text("raise RuntimeError('TARGET EXECUTED')")
    (project / "json.py").symlink_to(tmp_path / "outside.py")
    assert resolve(project, "json.tool")[0].kind == "unresolved"


@pytest.mark.parametrize("candidates", [None, "bad", [None], ["illegal/name"]])
def test_malformed_import_mapping_is_unresolved(tmp_path, monkeypatch, candidates):
    monkeypatch.setattr(metadata, "packages_distributions", lambda: {"bad": candidates})
    assert resolve(tmp_path, "bad")[0].kind == "unresolved"


def test_partial_namespace_mapping_retains_known_facts_and_denies(installed, monkeypatch):
    project, install = installed
    install("ISP-Present", "ispy_partial")
    monkeypatch.setattr(metadata, "packages_distributions", lambda: {"ispy_partial": ["ISP-Present", None]})
    dep = resolve(project, "ispy_partial")[0]
    assert dep.kind == "unresolved"
    assert dep.distributions[0].name == "isp-present"
    assert evaluate_dependencies([dep], {}, DependencyOptions(), "plugin.py")[0].code == "ISPY-D102"


def test_policy_evaluation_never_reads_metadata(monkeypatch):
    def forbidden(*args, **kwargs):
        raise AssertionError("pure policy must not collect metadata")

    monkeypatch.setattr(metadata, "packages_distributions", forbidden)
    monkeypatch.setattr(metadata, "distribution", forbidden)
    deps = [external()]
    assert collect_dependency_evidence(deps)
    assert evaluate_dependencies(deps, {"pyyaml": DependencyRule(version=">=2")}, DependencyOptions(), "plugin.py") == []


def test_explicit_zero_port_is_distinct_from_default_origin(installed):
    project, install = installed
    install("ISP-Port", "ispy_port", origin={
        "url": "https://example.com:0/sdk.whl", "archive_info": {},
    })
    dep = resolve(project, "ispy_port")[0]
    assert dep.distributions[0].origin.url == "https://example.com:0/sdk.whl"
    rule = DependencyRule(origin=OriginRule(url="https://example.com/sdk.whl"))
    violations = evaluate_dependencies([dep], {"isp-port": rule}, DependencyOptions(), "plugin.py")
    assert [item.code for item in violations] == ["ISPY-D106"]
