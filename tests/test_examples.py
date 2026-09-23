"""Exercise the public launch demo, example contracts, and offline extensions."""

import json
import re
import sys
from pathlib import Path

import pytest
from typer.testing import CliRunner

from examples.admission.extension_demo import main as extension_main
from examples.admission.extensions import DistributionAllowlist, InventoryProvider
from importspy.cli import app
from importspy.domain import AdmissionRequest
from importspy.engine import AdmissionDenied, AdmissionEngine


ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "examples" / "admission"


def request(source, contract):
    return AdmissionRequest(
        subject=EXAMPLES / source,
        contract=EXAMPLES / contract,
        project_root=EXAMPLES,
    )


def test_actual_readme_launch_demo_is_denied_without_execution(tmp_path, capsys):
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    source_block = re.search(r"```python\n(.*?)\n```", readme, re.DOTALL)
    policy_block = re.search(r"```yaml\n(.*?)\n```", readme, re.DOTALL)
    assert source_block is not None and policy_block is not None
    assert 'print("THIS MUST NOT RUN")' in source_block.group(1)
    source = tmp_path / "plugin.py"
    source.write_text(source_block.group(1), encoding="utf-8")
    policy = tmp_path / "plugin.importspy.yml"
    policy.write_text(policy_block.group(1), encoding="utf-8")
    admission = AdmissionRequest(subject=source, contract=policy, project_root=tmp_path)
    engine = AdmissionEngine()
    decision = engine.check(admission)
    assert decision.decision == "DENY"
    assert not decision.target_executed
    assert any(item.code == "ISPY-D101" and item.subject == "typer" for item in decision.violations)
    assert capsys.readouterr().out == ""
    with pytest.raises(AdmissionDenied):
        engine.load(admission)
    assert capsys.readouterr().out == ""

    result = CliRunner().invoke(app, ["check", str(source)])
    assert result.exit_code == 1, result.output
    assert "ISPY-D101" in result.output
    assert "Decision: DENY" in result.output
    assert "Target module was not executed." in result.output
    assert "THIS MUST NOT RUN" not in result.output


def test_checked_in_launch_example_matches_readme_behavior(capsys):
    decision = AdmissionEngine().check(request("plugin.py", "plugin.importspy.yml"))
    assert not decision.admitted
    assert not decision.target_executed
    assert {(item.code, item.subject) for item in decision.violations} == {("ISPY-D101", "typer")}
    assert capsys.readouterr().out == ""


@pytest.mark.parametrize("name", ["structural_plugin", "versioned_plugin"])
def test_structure_and_version_declaration_examples_admit(name, capsys):
    decision = AdmissionEngine().check(request(f"{name}.py", f"{name}.importspy.yml"))
    assert decision.admitted, decision.model_dump_json()
    assert not decision.target_executed
    assert capsys.readouterr().out == ""


def test_runtime_example_passes_and_fails_without_disclosing_value(monkeypatch):
    admission = request("structural_plugin.py", "runtime.yml")
    monkeypatch.setenv("IMPORTSPY_EXAMPLE_MODE", "production")
    assert AdmissionEngine().check(admission).admitted
    monkeypatch.setenv("IMPORTSPY_EXAMPLE_MODE", "PRIVATE_VALUE")
    decision = AdmissionEngine().check(admission)
    assert not decision.admitted
    assert any(item.code == "ISPY-R103" for item in decision.violations)
    assert "PRIVATE_VALUE" not in decision.model_dump_json()
    assert not decision.target_executed


def test_undeclared_example_distinguishes_project_from_importspy_installation():
    decision = AdmissionEngine().check(request("plugin.py", "undeclared.yml"))
    assert not decision.admitted
    assert {(item.code, item.subject) for item in decision.violations} == {("ISPY-D105", "typer")}
    distributions = {dist.name: dist for dep in decision.dependencies for dist in dep.distributions}
    assert distributions["packaging"].declared is True
    assert distributions["typer"].declared is False


def test_version_example_rejects_incompatible_installed_version(tmp_path):
    policy = tmp_path / "too-old.yml"
    policy.write_text('dependencies:\n  packaging:\n    version: "<0"\n')
    admission = request("versioned_plugin.py", "versioned_plugin.importspy.yml")
    admission.contract = policy
    decision = AdmissionEngine().check(admission)
    assert not decision.admitted
    assert any(item.code == "ISPY-D104" for item in decision.violations)


@pytest.fixture
def installed_sdk(tmp_path, monkeypatch):
    """An actual dist-info installation with import-time failure if executed."""
    site = tmp_path / "site-packages"
    dist = site / "company_payment_sdk-1.0.dist-info"
    dist.mkdir(parents=True)
    (dist / "METADATA").write_text("Metadata-Version: 2.1\nName: company-payment-sdk\nVersion: 1.0\n")
    (dist / "top_level.txt").write_text("company_sdk\n")
    (dist / "RECORD").write_text("company_sdk/__init__.py,,\n")
    package = site / "company_sdk"
    package.mkdir()
    (package / "__init__.py").write_text("raise AssertionError('SDK MUST NOT EXECUTE')\n")
    monkeypatch.setattr(sys, "path", [str(site), *sys.path])

    def origin(data):
        (dist / "direct_url.json").write_text(json.dumps(data))

    return origin


def test_vcs_origin_example_uses_metadata_without_importing_sdk(installed_sdk):
    installed_sdk({
        "url": "https://github.com/acme/payment-sdk.git",
        "vcs_info": {"vcs": "git", "commit_id": "abc123"},
    })
    admission = request("origin_plugin.py", "vcs-origin.yml")
    assert AdmissionEngine().check(admission).admitted
    assert "company_sdk" not in sys.modules
    installed_sdk({
        "url": "https://github.com/acme/payment-sdk.git",
        "vcs_info": {"vcs": "git", "commit_id": "different"},
    })
    decision = AdmissionEngine().check(admission)
    assert any(item.code == "ISPY-D106" for item in decision.violations)


@pytest.mark.parametrize("editable", [True, False])
def test_local_origin_example_enforces_editable_policy(installed_sdk, editable):
    installed_sdk({"url": "file:///controlled/company-sdk", "dir_info": {"editable": editable}})
    decision = AdmissionEngine().check(request("origin_plugin.py", "local-origin.yml"))
    assert decision.admitted is (not editable)
    if editable:
        assert any(item.code == "ISPY-D107" for item in decision.violations)
    assert not decision.target_executed


def test_provenance_example_does_not_treat_metadata_as_verification():
    decision = AdmissionEngine().check(request("versioned_plugin.py", "provenance.yml"))
    assert not decision.admitted
    assert any(item.code == "ISPY-P101" and item.subject == "packaging" for item in decision.violations)


def test_offline_provider_and_pure_validator_admit_and_deny():
    admission = request("versioned_plugin.py", "custom-evidence.yml")
    admitted = AdmissionEngine(
        providers=(InventoryProvider(),), validators=(DistributionAllowlist(),)
    ).check(admission)
    assert admitted.admitted, admitted.model_dump_json()
    inventory = next(item for item in admitted.evidence if item.kind == "example.inventory")
    assert inventory.status == "observed"
    assert inventory.provider == "example-inventory"
    assert inventory.observed == {"distributions": ["packaging"]}
    denied = AdmissionEngine(
        providers=(InventoryProvider(),), validators=(DistributionAllowlist(frozenset()),)
    ).check(admission)
    assert any(item.code == "EXAMPLE-P002" for item in denied.violations)
    unavailable = AdmissionEngine(validators=(DistributionAllowlist(),)).check(admission)
    assert {item.code for item in unavailable.violations} == {"ISPY-P101", "EXAMPLE-P001"}


def test_extension_demo_runs_without_executing_target(capsys):
    assert extension_main() == 0
    output = capsys.readouterr().out
    assert "Decision: ADMIT" in output
    assert "Target module was not executed." in output


def test_explicit_load_of_structural_example():
    name = "importspy_example_structural_loaded"
    try:
        module, decision = AdmissionEngine().load(
            request("structural_plugin.py", "structural_plugin.importspy.yml"), name=name
        )
        assert decision.admitted and decision.target_executed
        assert module.process(3) == "3"
        assert module.Plugin().run("request") == "request"
    finally:
        sys.modules.pop(name, None)
