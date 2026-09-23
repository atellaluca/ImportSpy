"""Serializable admission facts and decisions shared by the engine and extensions."""

from datetime import datetime, timezone
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, JsonValue


class Record(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Location(Record):
    path: str
    line: int | None = None
    column: int | None = None


class Evidence(Record):
    kind: str
    subject: str
    observed: JsonValue = None
    expected: JsonValue = None
    provider: str = "importspy"
    phase: Literal["static", "runtime", "external"] = "static"
    status: Literal["verified", "observed", "unknown", "unavailable"] = "observed"
    detail: str | None = None


class Violation(Record):
    code: str
    category: str
    message: str
    subject: str
    severity: Literal["error", "warning", "note"] = "error"
    phase: Literal["static", "runtime", "external", "configuration"] = "static"
    location: Location | None = None
    expected: JsonValue = None
    observed: JsonValue = None
    remediation: str | None = None


class ImportReference(Record):
    name: str
    line: int = 1
    column: int = 1
    level: int = 0
    optional: bool = False


class Origin(Record):
    type: Literal["unknown", "index", "vcs", "local", "archive"] = "unknown"
    url: str | None = None
    repository: str | None = None
    commit: str | None = None
    editable: bool | None = None
    hashes: dict[str, str] = Field(default_factory=dict)


class Distribution(Record):
    name: str
    version: str | None = None
    declared: bool | None = None
    origin: Origin = Field(default_factory=Origin)


class Dependency(Record):
    reference: ImportReference
    kind: Literal["stdlib", "internal", "external", "namespace", "direct", "unresolved"]
    distributions: list[Distribution] = Field(default_factory=list)
    declared: bool | None = None
    detail: str | None = None


class AdmissionContext(Record):
    subject: Path
    project_root: Path
    environment: dict[str, str] = Field(default_factory=dict)
    network_allowed: bool = False


class AdmissionRequest(Record):
    subject: Path
    contract: Path | None = None
    project_root: Path | None = None


class AdmissionDecision(Record):
    schema_version: Literal[1] = 1
    subject: str
    source_hash: str | None = None
    contract_identity: str | None = None
    contract_hash: str | None = None
    engine_version: str
    environment: dict[str, str] = Field(default_factory=dict)
    dependencies: list[Dependency] = Field(default_factory=list)
    evidence: list[Evidence] = Field(default_factory=list)
    violations: list[Violation] = Field(default_factory=list)
    decision: Literal["ADMIT", "DENY"] = "DENY"
    phases: list[str] = Field(default_factory=list)
    runtime_required: bool = False
    target_executed: bool = False
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @property
    def admitted(self) -> bool:
        return self.decision == "ADMIT"
