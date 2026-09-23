"""Integration tests for admission, evidence, runtime and explicit execution."""

import json
import sys
from pathlib import Path

import pytest

from importspy.domain import AdmissionRequest, Evidence, Violation
from importspy.engine import AdmissionDenied, AdmissionEngine, ExecutionFailed
from importspy.policy import AdmissionPolicy, ContractError, load_policy
from importspy.reporters import HumanReporter, JSONReporter, SARIFReporter


def request(tmp_path: Path, source="value = 1\n", policy="schema_version: 1\n"):
    target = tmp_path / "plugin.py"
    contract = tmp_path / "plugin.importspy.yml"
    target.write_text(source)
    contract.write_text(policy)
    return AdmissionRequest(subject=target, contract=contract, project_root=tmp_path)


def test_check_admitted_does_not_execute_and_load_executes_once(tmp_path):
    marker = tmp_path / "marker"
    req = request(
        tmp_path,
        f"from pathlib import Path\nPath({str(marker)!r}).write_text('once')\nvalue = 42\n",
    )
    engine = AdmissionEngine()
    decision = engine.check(req)
    assert decision.admitted and not decision.target_executed
    assert not marker.exists()
    module, executed = engine.load(req, name="importspy_test_plugin")
    try:
        assert module.value == 42 and executed.target_executed
        assert marker.read_text() == "once"
    finally:
        sys.modules.pop(module.__name__, None)


def test_denied_load_no_side_effects_and_multiple_violations(tmp_path):
    req = request(
        tmp_path,
        "raise AssertionError('EXECUTED')\n",
        "functions:\n  - name: missing\nclasses:\n  - name: Absent\n",
    )
    with pytest.raises(AdmissionDenied) as failure:
        AdmissionEngine().load(req)
    decision = failure.value.decision
    assert not decision.target_executed
    assert len(decision.violations) == 2


def test_load_executes_inspected_bytes_not_changed_path(tmp_path):
    req = request(tmp_path)

    class SwapProvider:
        name = "swap"
        requires_network = False

        def collect(self, context, dependencies):
            context.subject.write_text(
                "raise AssertionError('changed path executed')\n"
            )
            return []

    module, decision = AdmissionEngine(providers=(SwapProvider(),)).load(
        req, name="importspy_test_snapshot"
    )
    try:
        assert module.value == 1 and decision.target_executed
    finally:
        sys.modules.pop(module.__name__, None)


def test_explicit_runtime_checks_cannot_claim_no_execution(tmp_path):
    class CheckRuntime:
        def validate(self, module, decision):
            assert module.value == 1 and decision.target_executed
            return [
                Violation(
                    code="CUSTOM-R1",
                    category="runtime",
                    phase="runtime",
                    subject=decision.subject,
                    message="Runtime denied.",
                )
            ]

    with pytest.raises(AdmissionDenied) as error:
        AdmissionEngine(runtime_validators=(CheckRuntime(),)).load(
            request(tmp_path), name="importspy_test_runtime"
        )
    assert error.value.decision.target_executed
    assert "importspy_test_runtime" not in sys.modules
    assert "Target module was executed." in HumanReporter().render(error.value.decision)


def test_execution_exception_cleanup(tmp_path):
    with pytest.raises(ExecutionFailed) as error:
        AdmissionEngine().load(
            request(tmp_path, "raise RuntimeError('secret')"),
            name="importspy_test_failure",
        )
    assert error.value.decision.target_executed
    assert "importspy_test_failure" not in sys.modules
    assert "secret" not in error.value.decision.model_dump_json()


def test_unknown_dynamic_value_fails_closed(tmp_path):
    req = request(
        tmp_path, "value = int('1')\n", "variables:\n  - name: value\n    value: 1\n"
    )
    decision = AdmissionEngine().check(req)
    assert not decision.admitted and decision.runtime_required


def test_host_runtime_env_values_redacted(tmp_path, monkeypatch):
    monkeypatch.setenv("ADMISSION_TEST_TOKEN", "super-secret-value")
    req = request(
        tmp_path,
        policy="runtime:\n  python: '>=3.10'\n  environment:\n    ADMISSION_TEST_TOKEN: expected-secret\n",
    )
    decision = AdmissionEngine().check(req)
    assert not decision.admitted
    output = JSONReporter().render(decision)
    assert "super-secret-value" not in output and "expected-secret" not in output
    assert any(item.code == "ISPY-R103" for item in decision.violations)


def test_provider_network_opt_in_and_required_evidence(tmp_path):
    class Provider:
        name = "fixture"
        requires_network = True
        called = False

        def collect(self, context, dependencies):
            self.called = True
            assert context.network_allowed
            return [
                Evidence(
                    kind="test.approval",
                    subject="example",
                    observed=True,
                    phase="external",
                    status="verified",
                )
            ]

    provider = Provider()
    req = request(
        tmp_path,
        policy="evidence_requirements:\n  - kind: test.approval\n    subject: example\n    provider: fixture\n",
    )
    denied = AdmissionEngine(providers=(provider,)).check(req)
    assert not provider.called and not denied.admitted
    admitted = AdmissionEngine(providers=(provider,), allow_network=True).check(req)
    assert provider.called and admitted.admitted


def test_provider_failure_is_unavailable_not_secret_or_verified(tmp_path):
    class Broken:
        name = "broken"
        requires_network = False

        def collect(self, context, dependencies):
            raise RuntimeError("https://user:secret@example.com")

    req = request(
        tmp_path,
        policy="evidence_requirements:\n  - kind: test.approval\n    subject: example\n",
    )
    decision = AdmissionEngine(providers=(Broken(),)).check(req)
    assert not decision.admitted
    assert "secret" not in decision.model_dump_json()
    assert any(item.status == "unavailable" for item in decision.evidence)


def test_serialization_and_sarif_locations(tmp_path):
    req = request(
        tmp_path,
        "import forbidden_package\n",
        "dependencies:\n  'import:forbidden_package':\n    allowed: false\n",
    )
    decision = AdmissionEngine().check(req)
    assert JSONReporter().render(decision) == JSONReporter().render(decision)
    assert json.loads(JSONReporter().render(decision))["source_hash"]
    sarif = json.loads(SARIFReporter().render(decision))
    assert sarif["version"] == "2.1.0"
    assert sarif["runs"][0]["results"]
    for result in sarif["runs"][0]["results"]:
        for location in result.get("locations", []):
            assert location["physicalLocation"]["region"]["startLine"] == 1


@pytest.mark.parametrize(
    "policy",
    [
        "schema_version: 2",
        "dependency_options:\n  typo: true",
        "functions:\n  - name: f\n    typo: true",
        "runtime:\n  python: nonsense",
        "!!python/object/apply:os.system ['echo BAD']",
        "dependencies:\n  Foo_Bar: {}\n  foo-bar: {}",
        "[]",
    ],
)
def test_invalid_contracts_reject_without_execution(tmp_path, policy):
    req = request(tmp_path, "raise AssertionError('execution')", policy)
    with pytest.raises(ContractError):
        AdmissionEngine().check(req)


def test_policy_no_module_version_schema_collision(tmp_path):
    req = request(
        tmp_path, "__version__ = '1.2.3'", "schema_version: 1\nversion: '1.2.3'"
    )
    assert AdmissionEngine().check(req).admitted
    assert AdmissionPolicy().schema_version == 1
    policy, digest = load_policy(req.contract)
    assert policy.version == "1.2.3" and len(digest) == 64


def test_legacy_environment_evidence_cannot_cross_deployment_alternatives(
    tmp_path, monkeypatch
):
    import platform
    from ruamel.yaml import YAML

    monkeypatch.setenv("REQUIRED", "actual")
    req = request(tmp_path)
    data = {
        "deployments": [
            {
                "arch": platform.machine().lower(),
                "systems": [
                    {
                        "os": platform.system().lower(),
                        "environment": {
                            "variables": [{"name": "REQUIRED", "value": "wrong"}]
                        },
                        "pythons": [{"modules": []}],
                    },
                    {
                        "os": "windows"
                        if platform.system().lower() != "windows"
                        else "linux",
                        "environment": {
                            "variables": [{"name": "REQUIRED", "value": "actual"}]
                        },
                        "pythons": [{"modules": []}],
                    },
                ],
            },
        ]
    }
    with req.contract.open("w") as stream:
        YAML(typ="safe").dump(data, stream)
    assert not AdmissionEngine().check(req).admitted


def test_absent_optional_dependency_does_not_require_provenance(tmp_path):
    req = request(tmp_path, policy="dependencies:\n  absent:\n    provenance: true\n")
    assert AdmissionEngine().check(req).admitted


@pytest.mark.parametrize("observed", [False, None, 0, {}, [], ""])
def test_empty_external_evidence_cannot_satisfy_requirement(tmp_path, observed):
    class Empty:
        name = "empty"
        requires_network = False

        def collect(self, context, dependencies):
            return [
                Evidence(
                    kind="approval",
                    subject="example",
                    status="verified",
                    observed=observed,
                )
            ]

    req = request(
        tmp_path,
        policy="evidence_requirements:\n  - kind: approval\n    subject: example\n",
    )
    assert not AdmissionEngine(providers=(Empty(),)).check(req).admitted


def test_provider_cannot_satisfy_host_secret_presence(tmp_path, monkeypatch):
    import platform
    from ruamel.yaml import YAML

    monkeypatch.delenv("IMPORTSPY_ABSENT_SECRET", raising=False)
    req = request(tmp_path)
    data = {
        "deployments": [
            {
                "arch": platform.machine().lower(),
                "systems": [
                    {
                        "os": platform.system().lower(),
                        "environment": {"secrets": ["IMPORTSPY_ABSENT_SECRET"]},
                        "pythons": [{"modules": []}],
                    }
                ],
            }
        ]
    }
    with req.contract.open("w") as stream:
        YAML(typ="safe").dump(data, stream)

    class Provider:
        name = "external-host-snapshot"
        requires_network = False

        def collect(self, context, dependencies):
            return [
                Evidence(
                    kind="runtime.secret.present",
                    subject="IMPORTSPY_ABSENT_SECRET",
                    observed=True,
                    provider="importspy",
                    status="verified",
                )
            ]

    assert not AdmissionEngine(providers=(Provider(),)).check(req).admitted


def test_provider_names_cannot_collide_with_host_or_each_other():
    class Provider:
        name = "importspy"
        requires_network = False

        def collect(self, context, dependencies):
            return []

    with pytest.raises(ValueError, match="reserved"):
        AdmissionEngine(providers=(Provider(),))
    Provider.name = "example"
    with pytest.raises(ValueError, match="unique"):
        AdmissionEngine(providers=(Provider(), Provider()))
