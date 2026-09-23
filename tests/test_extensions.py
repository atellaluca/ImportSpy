"""Explicit plugin selection and evidence collection failure boundaries."""

import json
from types import SimpleNamespace

import pytest

from importspy import extensions
from importspy.domain import AdmissionRequest, Evidence
from importspy.engine import AdmissionEngine


class Provider:
    name = "test-provider"
    requires_network = False

    def collect(self, context, dependencies):
        return [
            Evidence(
                kind="test.verified",
                subject="plugin",
                observed=True,
                status="verified",
                phase="external",
            )
        ]


def test_entrypoint_loads_only_explicit_selection(monkeypatch):
    loaded = []

    def discover(**kwargs):
        assert kwargs == {"group": "importspy.evidence_providers", "name": "selected"}
        return [SimpleNamespace(load=lambda: loaded.append("selected") or Provider)]

    monkeypatch.setattr(extensions, "entry_points", discover)
    assert extensions.load_provider("selected").name == "test-provider"
    assert loaded == ["selected"]


@pytest.mark.parametrize("count", [0, 2])
def test_missing_or_ambiguous_entrypoint_never_loads(monkeypatch, count):
    def unexpected():
        pytest.fail("Ambiguous entry points must not be loaded")

    monkeypatch.setattr(
        extensions,
        "entry_points",
        lambda **kwargs: [SimpleNamespace(load=unexpected)] * count,
    )
    with pytest.raises(ValueError, match="exactly one"):
        extensions.load_provider("unknown")


@pytest.mark.parametrize(
    "provider",
    [
        SimpleNamespace(name="bad", requires_network="yes", collect=lambda: []),
        SimpleNamespace(name=3, requires_network=False, collect=lambda: []),
    ],
)
def test_invalid_provider_protocol_is_rejected(monkeypatch, provider):
    monkeypatch.setattr(
        extensions,
        "entry_points",
        lambda **kwargs: [SimpleNamespace(load=lambda: lambda: provider)],
    )
    with pytest.raises(ValueError, match="protocol"):
        extensions.load_provider("invalid")


@pytest.fixture
def request_with_evidence(tmp_path):
    source = tmp_path / "plugin.py"
    source.write_text("print('TARGET NEVER EXECUTED')\n")
    contract = tmp_path / "policy.yml"
    contract.write_text(
        "evidence_requirements:\n  - kind: test.verified\n    subject: plugin\n    provider: test-provider\n"
    )
    return AdmissionRequest(subject=source, contract=contract)


def test_network_provider_is_not_called_without_opt_in(request_with_evidence):
    class NetworkProvider(Provider):
        requires_network = True

        def collect(self, context, dependencies):
            pytest.fail("Network provider must remain disabled")

    decision = AdmissionEngine(providers=(NetworkProvider(),)).check(
        request_with_evidence
    )
    assert not decision.admitted
    assert any(
        item.status == "unavailable" and "Network" in item.detail
        for item in decision.evidence
    )
    assert any(item.code == "ISPY-P101" for item in decision.violations)


def test_network_opt_in_and_provider_identity(request_with_evidence, capsys):
    class NetworkProvider(Provider):
        requires_network = True

        def collect(self, context, dependencies):
            assert context.network_allowed is True
            yield Evidence(
                kind="test.verified",
                subject="plugin",
                observed=True,
                status="verified",
                provider="spoofed",
                phase="external",
            )

    decision = AdmissionEngine(
        providers=(NetworkProvider(),), allow_network=True
    ).check(request_with_evidence)
    assert decision.admitted
    assert any(
        item.kind == "test.verified" and item.provider == "test-provider"
        for item in decision.evidence
    )
    assert decision.target_executed is False
    assert capsys.readouterr().out == ""


def test_provider_exception_is_redacted_and_required_evidence_denied(
    request_with_evidence,
):
    class BrokenProvider(Provider):
        def collect(self, context, dependencies):
            raise RuntimeError("private-api-token")

    decision = AdmissionEngine(providers=(BrokenProvider(),)).check(
        request_with_evidence
    )
    assert not decision.admitted
    assert "private-api-token" not in decision.model_dump_json()
    assert any(item.status == "unavailable" for item in decision.evidence)


def test_invalid_provider_batch_does_not_partially_satisfy_policy(
    request_with_evidence,
):
    class InvalidProvider(Provider):
        def collect(self, context, dependencies):
            return [*super().collect(context, dependencies), {"invalid": "record"}]

    decision = AdmissionEngine(providers=(InvalidProvider(),)).check(
        request_with_evidence
    )
    assert not decision.admitted
    assert not any(item.kind == "test.verified" for item in decision.evidence)


def test_provider_receives_copies_of_context_and_dependencies(request_with_evidence):
    class MutatingProvider(Provider):
        def collect(self, context, dependencies):
            context.environment["python"] = "fake-version"
            context.environment["secret"] = "private-token"
            dependencies.clear()
            return super().collect(context, dependencies)

    request_with_evidence.subject.write_text("import os\n")
    decision = AdmissionEngine(providers=(MutatingProvider(),)).check(
        request_with_evidence
    )
    assert decision.admitted
    assert decision.environment["python"] != "fake-version"
    assert len(decision.dependencies) == 1
    assert "private-token" not in json.dumps(decision.model_dump(mode="json"))
