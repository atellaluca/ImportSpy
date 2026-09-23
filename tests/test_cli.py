"""Exercise the public CLI and its no-execution contract."""

import json
import sys
from pathlib import Path

import pytest
from ruamel.yaml import YAML
from typer.testing import CliRunner

from importspy import cli
from importspy.domain import Evidence
from importspy.version import __version__


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def source(tmp_path):
    path = tmp_path / "plugin.py"
    path.write_text("def run():\n    return 1\n")
    return path


def test_help_and_version(runner):
    help_result = runner.invoke(cli.app, ["--help"])
    assert help_result.exit_code == 0
    assert "check" in help_result.stdout and "init" in help_result.stdout
    version = runner.invoke(cli.app, ["--version"])
    assert version.exit_code == 0
    assert version.stdout.strip() == f"ImportSpy {__version__}"


@pytest.mark.parametrize("output", ["human", "json", "sarif"])
def test_check_formats_admit_without_execution(runner, source, tmp_path, output):
    marker = tmp_path / "must-not-exist"
    source.write_text(
        f"open({str(marker)!r}, 'w').write('executed')\nprint('EXECUTED-TARGET')\n"
    )
    result = runner.invoke(cli.app, ["check", str(source), "--format", output])
    assert result.exit_code == 0, result.output
    assert not marker.exists()
    assert "EXECUTED-TARGET" not in result.stdout
    if output == "json":
        decision = json.loads(result.stdout)
        assert decision["decision"] == "ADMIT"
        assert decision["target_executed"] is False
        assert decision["source_hash"]
    elif output == "sarif":
        report = json.loads(result.stdout)
        assert report["version"] == "2.1.0"
        assert report["runs"][0]["results"] == []
    else:
        assert "Decision: ADMIT" in result.stdout
        assert "Target module was not executed." in result.stdout


def test_check_denies_dependency_before_printing_or_writing(runner, source, tmp_path):
    marker = tmp_path / "marker"
    source.write_text(
        f"import os\nprint('EXECUTED-TARGET')\nopen({str(marker)!r}, 'w').close()\n"
    )
    contract = source.with_suffix(".importspy.yml")
    contract.write_text("dependencies:\n  import:os:\n    allowed: false\n")
    result = runner.invoke(cli.app, ["check", str(source), "--format", "json"])
    assert result.exit_code == 1, result.output
    decision = json.loads(result.stdout)
    assert decision["decision"] == "DENY"
    assert decision["target_executed"] is False
    assert decision["contract_identity"] == str(contract)
    assert "EXECUTED-TARGET" not in result.stdout
    assert not marker.exists()


@pytest.mark.parametrize(
    "content",
    [
        "schema_version: 99\n",
        "unexpected: true\n",
        "- not-a-mapping\n",
        "!!python/object:module.Class {}\n",
    ],
)
def test_invalid_contract_has_exit_two_and_machine_readable_error(
    runner, source, content
):
    contract = source.with_suffix(".yml")
    contract.write_text(content)
    result = runner.invoke(
        cli.app, ["check", str(source), "-s", str(contract), "-f", "json"]
    )
    assert result.exit_code == 2, result.output
    decision = json.loads(result.stdout)
    assert decision["violations"][0]["code"] == "ISPY-C101"
    assert decision["target_executed"] is False


def test_unexpected_tool_error_is_redacted_and_exit_three(runner, source, monkeypatch):
    def fail(*args, **kwargs):
        raise RuntimeError("private-access-token")

    monkeypatch.setattr(cli.AdmissionEngine, "check", fail)
    result = runner.invoke(cli.app, ["check", str(source), "-f", "json"])
    assert result.exit_code == 3
    assert "private-access-token" not in result.output
    assert json.loads(result.stdout)["violations"][0]["code"] == "ISPY-C199"


def test_init_creates_editable_sidecar_without_execution_or_overwrite(
    runner, source, tmp_path
):
    marker = tmp_path / "marker"
    source.write_text(
        f"open({str(marker)!r}, 'w').close()\nprint('EXECUTED-TARGET')\ndef run(): pass\n"
    )
    first = runner.invoke(cli.app, ["init", str(source)])
    assert first.exit_code == 0, first.output
    contract = source.with_suffix(".importspy.yml")
    generated = contract.read_bytes()
    data = YAML(typ="safe").load(generated)
    assert data["schema_version"] == 1
    assert data["filename"] == "plugin.py"
    assert data["functions"] == [{"name": "run"}]
    assert not marker.exists()
    assert "EXECUTED-TARGET" not in first.stdout
    second = runner.invoke(cli.app, ["init", str(source)])
    assert second.exit_code == 2
    assert contract.read_bytes() == generated
    assert not marker.exists()


def test_init_unknown_imports_generate_denials(runner, source):
    source.write_text("import nonexistent_importspy_cli_fixture\n")
    result = runner.invoke(cli.app, ["init", str(source)])
    assert result.exit_code == 0, result.output
    data = YAML(typ="safe").load(source.with_suffix(".importspy.yml"))
    assert (
        data["dependencies"]["import:nonexistent_importspy_cli_fixture"]["allowed"]
        is False
    )
    assert runner.invoke(cli.app, ["check", str(source)]).exit_code == 1


def test_init_decorated_declarations_remain_unknown(runner, source):
    source.write_text("@changes_signature\ndef run(): pass\n")
    assert runner.invoke(cli.app, ["init", str(source)]).exit_code == 0
    result = runner.invoke(cli.app, ["check", str(source), "-f", "json"])
    assert result.exit_code == 1
    decision = json.loads(result.stdout)
    assert decision["runtime_required"] is True
    assert any(item["code"] == "ISPY-S103" for item in decision["violations"])


def test_init_custom_destination_and_invalid_source(runner, source, tmp_path):
    destination = tmp_path / "custom.yml"
    assert (
        runner.invoke(cli.app, ["init", str(source), "-o", str(destination)]).exit_code
        == 0
    )
    assert destination.exists()
    source.write_text("return 1\n")
    invalid = runner.invoke(cli.app, ["init", str(source)])
    assert invalid.exit_code == 2
    assert not source.with_suffix(".importspy.yml").exists()


def test_init_tool_failure_is_redacted_and_exit_three(runner, source, monkeypatch):
    from importspy.dependencies import DependencyResolver

    def fail(*args, **kwargs):
        raise RuntimeError("private-metadata-token")

    monkeypatch.setattr(DependencyResolver, "resolve", fail)
    result = runner.invoke(cli.app, ["init", str(source)])
    assert result.exit_code == 3
    assert "private-metadata-token" not in result.output
    assert not source.with_suffix(".importspy.yml").exists()


def _project(root: Path, entries: str) -> None:
    (root / "pyproject.toml").write_text(f"[tool.importspy]\nsubjects = {entries}\n")
    (root / "policy.yml").write_text("{}\n")


def test_project_checks_only_explicit_subjects_and_returns_json_array(
    runner, source, tmp_path
):
    (tmp_path / "unlisted.py").write_text("invalid python :::\n")
    _project(tmp_path, '[{path = "plugin.py", contract = "policy.yml"}]')
    result = runner.invoke(cli.app, ["check", str(tmp_path), "-f", "json"])
    assert result.exit_code == 0, result.output
    decisions = json.loads(result.stdout)
    assert isinstance(decisions, list) and len(decisions) == 1
    assert decisions[0]["subject"] == str(source)


@pytest.mark.parametrize(
    "entries",
    [
        '[{path = "../outside.py", contract = "policy.yml"}]',
        '[{path = "plugin.py", contract = "../outside.yml"}]',
        '[{path = "plugin.py"}]',
        "[]",
    ],
)
def test_project_configuration_rejects_traversal_and_ambiguous_entries(
    runner, source, tmp_path, entries
):
    _project(tmp_path, entries)
    result = runner.invoke(cli.app, ["check", str(tmp_path), "-f", "json"])
    assert result.exit_code == 2
    assert json.loads(result.stdout)[0]["violations"][0]["code"] == "ISPY-C101"


def test_project_rejects_symlink_escape(runner, source, tmp_path):
    source.unlink()
    source.symlink_to(tmp_path.parent / "external.py")
    _project(tmp_path, '[{path = "plugin.py", contract = "policy.yml"}]')
    assert runner.invoke(cli.app, ["check", str(tmp_path)]).exit_code == 2


def test_project_requires_configuration_and_rejects_contract_override(
    runner, source, tmp_path
):
    assert runner.invoke(cli.app, ["check", str(tmp_path)]).exit_code == 2
    _project(tmp_path, '[{path = "plugin.py", contract = "policy.yml"}]')
    assert (
        runner.invoke(
            cli.app, ["check", str(tmp_path), "-s", str(tmp_path / "policy.yml")]
        ).exit_code
        == 2
    )


def test_no_provider_is_loaded_implicitly(runner, source, monkeypatch):
    def unexpected(name):
        pytest.fail(f"Unexpected plugin load: {name}")

    monkeypatch.setattr(cli, "load_provider", unexpected)
    assert runner.invoke(cli.app, ["check", str(source)]).exit_code == 0


def test_missing_selected_provider_is_configuration_failure(
    runner, source, monkeypatch
):
    def missing(name):
        raise ValueError("provider-secret")

    monkeypatch.setattr(cli, "load_provider", missing)
    result = runner.invoke(
        cli.app, ["check", str(source), "--provider", "missing", "-f", "json"]
    )
    assert result.exit_code == 2
    assert "provider-secret" not in result.output


@pytest.mark.parametrize("allow_network", [False, True])
def test_selected_provider_and_network_option_reach_engine(
    runner, source, monkeypatch, allow_network
):
    loaded = []
    collected = []

    class NetworkProvider:
        name = "network-fixture"
        requires_network = True

        def collect(self, context, dependencies):
            collected.append(context.network_allowed)
            return [Evidence(kind="test.signal", subject="fixture", observed=True)]

    monkeypatch.setattr(
        cli, "load_provider", lambda name: loaded.append(name) or NetworkProvider()
    )
    args = ["check", str(source), "--provider", "network-fixture", "-f", "json"]
    if allow_network:
        args.append("--allow-network")
    result = runner.invoke(cli.app, args)
    assert result.exit_code == 0
    assert loaded == ["network-fixture"]
    assert collected == ([True] if allow_network else [])
    evidence = json.loads(result.stdout)["evidence"]
    assert any(
        item["kind"] == ("test.signal" if allow_network else "provider.availability")
        for item in evidence
    )


def test_legacy_main_invocation_is_static_and_warns(source, monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["importspy", str(source), "-f", "json"])
    with pytest.raises(SystemExit) as exited:
        cli.main()
    assert exited.value.code == 0
    captured = capsys.readouterr()
    assert "Deprecated invocation" in captured.err
    assert json.loads(captured.out)["target_executed"] is False


def test_reserved_provider_name_is_configuration_failure(runner, source, monkeypatch):
    class ReservedProvider:
        name = "importspy.fake"
        requires_network = False

        def collect(self, context, dependencies):
            return []

    monkeypatch.setattr(cli, "load_provider", lambda name: ReservedProvider())
    result = runner.invoke(
        cli.app, ["check", str(source), "--provider", "reserved", "-f", "json"]
    )
    assert result.exit_code == 2
    assert json.loads(result.stdout)["violations"][0]["code"] == "ISPY-C101"
