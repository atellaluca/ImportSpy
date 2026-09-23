"""Static admission and starter-contract generation for local and CI use."""

import json
import sys
from enum import Enum
from io import StringIO
from pathlib import Path
from typing import Optional

import typer
from ruamel.yaml import YAML

from .domain import AdmissionDecision, AdmissionRequest, Violation
from .engine import AdmissionEngine, project_root_for
from .extensions import load_provider
from .inspection import SourceInspector, starter_contract
from .policy import AdmissionPolicy, ContractError
from .reporters import HumanReporter, JSONReporter, SARIFReporter
from .version import __version__

app = typer.Typer(
    no_args_is_help=True,
    help="Policy-as-code admission for Python modules and dependencies.",
)


class OutputFormat(str, Enum):
    human = "human"
    json = "json"
    sarif = "sarif"


def _version(value: bool) -> None:
    if value:
        typer.echo(f"ImportSpy {__version__}")
        raise typer.Exit()


@app.callback()
def entry(
    version: bool = typer.Option(
        False, "--version", "-v", callback=_version, is_eager=True
    ),
) -> None:
    """Inspect, resolve, collect evidence, evaluate policy, admit or deny."""


def _sidecar(subject: Path) -> Path:
    return subject.with_suffix(".importspy.yml")


def _requests(
    subject: Path, contract: Path | None, project_root: Path | None
) -> list[AdmissionRequest]:
    if not subject.is_dir():
        selected = contract or (
            _sidecar(subject) if _sidecar(subject).is_file() else None
        )
        return [
            AdmissionRequest(
                subject=subject, contract=selected, project_root=project_root
            )
        ]
    if contract is not None:
        raise ContractError(
            "Directory checks use [tool.importspy].subjects; do not pass --contract."
        )
    try:
        if sys.version_info >= (3, 11):
            import tomllib
        else:
            import tomli as tomllib
        data = tomllib.loads((subject / "pyproject.toml").read_text(encoding="utf-8"))
        entries = data["tool"]["importspy"]["subjects"]
        if not isinstance(entries, list) or not entries:
            raise ValueError
        requests = []
        root = subject.resolve()
        for item in entries:
            if not isinstance(item, dict) or set(item) != {"path", "contract"}:
                raise ValueError
            source = (root / item["path"]).resolve()
            policy = (root / item["contract"]).resolve()
            if not source.is_relative_to(root) or not policy.is_relative_to(root):
                raise ValueError
            requests.append(
                AdmissionRequest(
                    subject=source, contract=policy, project_root=project_root or root
                )
            )
        return requests
    except (OSError, ValueError, TypeError, KeyError):
        raise ContractError(
            "Directory checks require explicit path/contract entries in [tool.importspy].subjects inside this project."
        ) from None


def _render(
    decisions: list[AdmissionDecision], output: OutputFormat, *, project: bool = False
) -> str:
    if output == OutputFormat.sarif:
        return SARIFReporter().render_many(decisions)
    if output == OutputFormat.json:
        if len(decisions) == 1 and not project:
            return JSONReporter().render(decisions[0])
        return json.dumps(
            [item.model_dump(mode="json") for item in decisions], indent=2
        )
    return "\n\n".join(HumanReporter().render(item) for item in decisions)


@app.command()
def check(
    subject: Path = typer.Argument(
        ..., help="Python source or a configured project directory."
    ),
    contract: Optional[Path] = typer.Option(None, "--contract", "--spymodel", "-s"),
    output: OutputFormat = typer.Option(OutputFormat.human, "--format", "-f"),
    project_root: Optional[Path] = typer.Option(None, "--project-root"),
    provider: Optional[list[str]] = typer.Option(
        None, "--provider", help="Explicit trusted evidence provider entry point."
    ),
    allow_network: bool = typer.Option(False, "--allow-network"),
) -> None:
    """Decide admission without executing target code. Exit 0/1/2/3: admit/deny/config/tool."""
    decisions = []
    exit_code = 0
    try:
        requests = _requests(subject, contract, project_root)
        try:
            providers = tuple(load_provider(name) for name in provider or [])
            engine = AdmissionEngine(providers=providers, allow_network=allow_network)
        except (ValueError, AttributeError, ImportError):
            raise ContractError("Cannot load a selected evidence provider.") from None
        for request in requests:
            try:
                decision = engine.check(request)
                exit_code = max(exit_code, 0 if decision.admitted else 1)
            except ContractError as exc:
                decision = _error(
                    request.subject, "ISPY-C101", str(exc), "configuration"
                )
                exit_code = max(exit_code, 2)
            decisions.append(decision)
    except ContractError as exc:
        decisions.append(_error(subject, "ISPY-C101", str(exc), "configuration"))
        exit_code = 2
    except Exception:
        decisions.append(
            _error(
                subject,
                "ISPY-C199",
                "Admission tool failed (details withheld).",
                "tool",
            )
        )
        exit_code = 3
    typer.echo(_render(decisions, output, project=subject.is_dir()))
    raise typer.Exit(exit_code)


def _error(subject: Path, code: str, message: str, category: str) -> AdmissionDecision:
    return AdmissionDecision(
        subject=str(subject),
        engine_version=__version__,
        violations=[
            Violation(
                code=code,
                category=category,
                phase="configuration",
                subject=str(subject),
                message=message,
            )
        ],
    )


@app.command()
def init(
    subject: Path = typer.Argument(..., help="Source to inspect without execution."),
    output: Optional[Path] = typer.Option(None, "--output", "-o"),
) -> None:
    """Write an editable starter contract beside the source; never overwrite a file."""
    from .dependencies import DependencyResolver

    try:
        inspection = SourceInspector().inspect(subject)
        if inspection.violations:
            raise ContractError(
                "Cannot generate a contract: source is unreadable or invalid."
            )
        data = starter_contract(inspection)
        data["schema_version"] = 1
        dependencies = DependencyResolver(project_root_for(subject)).resolve(
            inspection.imports, subject
        )
        rules: dict[str, dict[str, bool]] = {}
        for item in dependencies:
            if item.kind == "unresolved":
                rules[f"import:{item.reference.name.split('.')[0]}"] = {
                    "allowed": False
                }
            for distribution in item.distributions:
                rules[distribution.name] = {"allowed": True}
        if rules:
            data["dependencies"] = rules
        AdmissionPolicy.model_validate(data)
        # Serialize before creating the destination, so generation failures do
        # not leave a misleading partial policy behind.
        serialized = StringIO()
        YAML(typ="safe").dump(data, serialized)
    except ContractError as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(2) from None
    except Exception:
        typer.echo("Contract generation failed (details withheld).", err=True)
        raise typer.Exit(3) from None
    destination = output or _sidecar(subject)
    try:
        with destination.open("x", encoding="utf-8") as stream:
            stream.write(
                "# Generated from source declarations, not proof of runtime behavior.\n"
                "# Review dependency approvals and add version/origin/evidence requirements.\n"
                "# Unresolved imports are denied until explicitly reviewed.\n"
            )
            stream.write(serialized.getvalue())
    except OSError:
        typer.echo(
            "Cannot create contract: destination exists or is not writable.", err=True
        )
        raise typer.Exit(2) from None
    typer.echo(
        f"Created {destination}. Review the policy, then run importspy check {subject}."
    )


def main() -> None:
    # Compatibility with 0.4's positional command; all validation is now static.
    args = sys.argv[1:]
    if args and args[0] not in {"check", "init"} and not args[0].startswith("-"):
        typer.echo(
            "Deprecated invocation: use 'importspy check SOURCE --contract POLICY'.",
            err=True,
        )
        args.insert(0, "check")
    app(args=args)


if __name__ == "__main__":
    main()
