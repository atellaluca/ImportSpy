"""Human, JSON and SARIF views of the same admission decision."""

import json
from pathlib import Path

from .domain import AdmissionDecision


def _text(value: str) -> str:
    return "".join(character if character.isprintable() else " " for character in value)


class HumanReporter:
    def render(self, decision: AdmissionDecision) -> str:
        if decision.target_executed:
            preflight = "Execution: target code ran"
        elif any(
            item.kind == "source.syntax"
            and item.status == "verified"
            and item.observed == "valid"
            for item in decision.evidence
        ):
            preflight = "Preflight: parsed without target execution"
        elif "static" in decision.phases:
            preflight = "Preflight: failed"
        else:
            preflight = "Preflight: not completed"
        lines = [
            "ImportSpy Admission Report",
            f"Source: {_text(decision.subject)}",
            preflight,
            f"Contract: {_text(decision.contract_identity or 'default policy')}",
            f"Dependencies: {len(decision.dependencies)} import references",
        ]
        for dependency in decision.dependencies:
            distributions = ", ".join(
                f"{item.name} {item.version or '?'}"
                for item in dependency.distributions
            )
            lines.append(
                f"  {_text(dependency.reference.name)}: {dependency.kind}"
                + (f" ({_text(distributions)})" if distributions else "")
            )
        lines.append(
            "Host runtime: "
            + (
                ", ".join(
                    f"{_text(key)}={_text(value)}"
                    for key, value in sorted(decision.environment.items())
                )
                or "not collected"
            )
        )
        lines.append(f"Evidence: {len(decision.evidence)} observations")
        for item in decision.evidence:
            if item.status in {"unknown", "unavailable"}:
                lines.append(
                    f"  {_text(item.kind)} [{_text(item.provider)}]: {item.status}"
                )
        for violation in decision.violations:
            lines.append(
                f"{_text(violation.code)} [{violation.severity}] {_text(violation.message)}"
            )
        if decision.runtime_required:
            lines.append(
                "Some required facts are unknown until runtime; static policy failed closed."
            )
        lines.extend(
            [
                f"Decision: {decision.decision}",
                "Target module was executed."
                if decision.target_executed
                else "Target module was not executed.",
            ]
        )
        return "\n".join(lines)


class JSONReporter:
    def render(self, decision: AdmissionDecision) -> str:
        return decision.model_dump_json(indent=2)


class SARIFReporter:
    def render(self, decision: AdmissionDecision) -> str:
        return self.render_many([decision])

    def render_many(self, decisions: list[AdmissionDecision]) -> str:
        codes = sorted(
            {item.code for decision in decisions for item in decision.violations}
        )
        results = []
        for decision in decisions:
            for item in decision.violations:
                result: dict[str, object] = {
                    "ruleId": item.code,
                    "ruleIndex": codes.index(item.code),
                    "level": {"error": "error", "warning": "warning", "note": "note"}[
                        item.severity
                    ],
                    "message": {"text": item.message},
                    "properties": {"subject": item.subject, "phase": item.phase},
                }
                if item.location and item.location.path:
                    physical: dict[str, object] = {
                        "artifactLocation": {
                            "uri": Path(item.location.path).absolute().as_uri()
                        }
                    }
                    if item.location.line is not None and item.location.line > 0:
                        region = {"startLine": item.location.line}
                        if (
                            item.location.column is not None
                            and item.location.column > 0
                        ):
                            region["startColumn"] = item.location.column
                        physical["region"] = region
                    result["locations"] = [{"physicalLocation": physical}]
                results.append(result)
        version = decisions[0].engine_version if decisions else "unknown"
        return json.dumps(
            {
                "$schema": "https://json.schemastore.org/sarif-2.1.0.json",
                "version": "2.1.0",
                "runs": [
                    {
                        "tool": {
                            "driver": {
                                "name": "ImportSpy",
                                "version": version,
                                "informationUri": "https://github.com/atellaluca/ImportSpy",
                                "rules": [{"id": code} for code in codes],
                            }
                        },
                        "results": results,
                        "properties": {
                            "decisions": [decision.decision for decision in decisions]
                        },
                    }
                ],
            },
            indent=2,
        )
