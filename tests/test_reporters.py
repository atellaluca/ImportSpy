"""Reporters preserve one decision and never invent verification or locations."""

import json
from datetime import datetime, timezone

import pytest

from importspy.domain import AdmissionDecision, Evidence, Location, Violation
from importspy.reporters import HumanReporter, JSONReporter, SARIFReporter


def decision(**kwargs):
    return AdmissionDecision(
        subject="plugin.py",
        engine_version="0.5.0",
        timestamp=datetime(2026, 1, 1, tzinfo=timezone.utc),
        **kwargs,
    )


def violation(**kwargs):
    return Violation(
        code="ISPY-S101",
        category="structure",
        subject="run",
        message="Required function is missing.",
        **kwargs,
    )


def test_json_is_stable_and_round_trips_the_same_decision():
    item = decision(
        violations=[violation()],
        evidence=[
            Evidence(
                kind="source.syntax",
                subject="plugin.py",
                observed="valid",
                status="verified",
            )
        ],
    )
    report = JSONReporter()
    assert report.render(item) == report.render(item)
    assert AdmissionDecision.model_validate_json(report.render(item)) == item
    assert json.loads(report.render(item)) == item.model_dump(mode="json")


def test_sarif_has_schema_driver_rules_results_and_real_location(tmp_path):
    path = tmp_path / "plugin with spaces.py"
    item = decision(
        violations=[violation(location=Location(path=str(path), line=7, column=3))]
    )
    report = json.loads(SARIFReporter().render(item))
    assert report["version"] == "2.1.0"
    assert report["$schema"].endswith("sarif-2.1.0.json")
    run = report["runs"][0]
    assert run["tool"]["driver"]["name"] == "ImportSpy"
    assert run["tool"]["driver"]["rules"] == [{"id": "ISPY-S101"}]
    result = run["results"][0]
    assert result["ruleId"] == "ISPY-S101" and result["ruleIndex"] == 0
    assert result["level"] == "error"
    assert result["message"]["text"] == item.violations[0].message
    assert result["locations"][0]["physicalLocation"] == {
        "artifactLocation": {"uri": path.as_uri()},
        "region": {"startLine": 7, "startColumn": 3},
    }


def test_sarif_omits_unknown_locations_and_regions():
    item = decision(
        violations=[violation(), violation(location=Location(path="plugin.py"))]
    )
    results = json.loads(SARIFReporter().render(item))["runs"][0]["results"]
    assert "locations" not in results[0]
    assert "region" not in results[1]["locations"][0]["physicalLocation"]


def test_sarif_empty_path_does_not_invent_current_directory_location():
    item = decision(violations=[violation(location=Location(path="", line=7))])
    result = json.loads(SARIFReporter().render(item))["runs"][0]["results"][0]
    assert "locations" not in result


@pytest.mark.parametrize("line,column", [(0, 1), (-1, 2), (None, 5)])
def test_sarif_never_emits_nonpositive_or_unanchored_positions(line, column):
    item = decision(
        violations=[
            violation(location=Location(path="plugin.py", line=line, column=column))
        ]
    )
    physical = json.loads(SARIFReporter().render(item))["runs"][0]["results"][0][
        "locations"
    ][0]["physicalLocation"]
    assert "region" not in physical


def test_sarif_nonpositive_column_is_omitted():
    item = decision(
        violations=[violation(location=Location(path="plugin.py", line=2, column=0))]
    )
    region = json.loads(SARIFReporter().render(item))["runs"][0]["results"][0][
        "locations"
    ][0]["physicalLocation"]["region"]
    assert region == {"startLine": 2}


def test_sarif_project_uses_shared_rule_indexes_and_maps_severities():
    items = [
        decision(violations=[violation(severity="warning")]),
        decision(
            violations=[
                Violation(
                    code="ISPY-D101",
                    category="dependency",
                    subject="dep",
                    message="Denied.",
                    severity="note",
                )
            ]
        ),
    ]
    run = json.loads(SARIFReporter().render_many(items))["runs"][0]
    assert run["tool"]["driver"]["rules"] == [{"id": "ISPY-D101"}, {"id": "ISPY-S101"}]
    assert [(result["ruleIndex"], result["level"]) for result in run["results"]] == [
        (1, "warning"),
        (0, "note"),
    ]
    assert run["properties"]["decisions"] == ["DENY", "DENY"]


def test_human_report_does_not_claim_preflight_for_configuration_failure():
    text = HumanReporter().render(
        decision(
            violations=[
                Violation(
                    code="ISPY-C101",
                    category="configuration",
                    phase="configuration",
                    subject="plugin.py",
                    message="Invalid contract.",
                )
            ]
        )
    )
    assert "Preflight: not completed" in text
    assert "inspected without target execution" not in text
    assert "Target module was not executed." in text


def test_human_report_distinguishes_valid_source_from_failed_parse():
    parsed = decision(
        phases=["static"],
        evidence=[
            Evidence(
                kind="source.syntax",
                subject="plugin.py",
                observed="valid",
                status="verified",
            )
        ],
    )
    invalid = decision(
        phases=["static"],
        violations=[
            Violation(
                code="ISPY-S001",
                category="source",
                subject="plugin.py",
                message="Syntax error",
            )
        ],
    )
    assert "Preflight: parsed without target execution" in HumanReporter().render(
        parsed
    )
    assert "Preflight: failed" in HumanReporter().render(invalid)


def test_human_report_marks_runtime_execution_and_unknowns():
    item = decision(
        target_executed=True,
        runtime_required=True,
        evidence=[Evidence(kind="dynamic.fact", subject="plugin.py", status="unknown")],
    )
    text = HumanReporter().render(item)
    assert "Target module was executed." in text
    assert "dynamic.fact [importspy]: unknown" in text
    assert "unknown until runtime" in text


def test_human_report_sanitizes_all_untrusted_inline_fields():
    item = decision(
        environment={"os": "\x1b[31mmalicious\nvalue"},
        violations=[
            Violation(
                code="ISPY-X\x1b[2J",
                category="external",
                subject="subject",
                message="Line\n\x1b[31mvalue",
            )
        ],
    )
    text = HumanReporter().render(item)
    assert "\x1b" not in text
    assert "malicious\nvalue" not in text
