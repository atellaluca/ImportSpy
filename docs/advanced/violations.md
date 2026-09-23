# Structured violations and reporting

Admission rules return `Violation` records. `AdmissionEngine.check` gathers
those records into an `AdmissionDecision`; a failed policy normally returns
DENY instead of raising the first generic validation error.

A violation records a stable code, category, severity, phase, subject, message,
and optional location, expected/observed facts, and remediation. Reporters render
that existing decision as human text, JSON, or SARIF without evaluating policy
again. Locations are included only when known.

```python
from importspy.domain import Violation

violation = Violation(
    code="ACME-P101",
    category="organization-policy",
    phase="external",
    subject="example-package",
    message="Required review evidence is unavailable.",
    remediation="Provide a current review from the selected trusted provider.",
)
```

Use a distinct code namespace for a third-party extension. Core code families
and user remediation are listed in [contract violations](../errors/contract-violations.md).
The [extension guide](../extensions.md) explains custom policy validators.

## Decisions and exceptions

Error-severity violations cause DENY. Warnings and notes remain visible without
causing denial by themselves. A required static fact that remains unknown is an
error, not a warning. `runtime_required` indicates this uncertainty; it does not
authorize execution to resolve a failed policy.

An unreadable or invalid contract raises `ContractError` in the Python API and
maps to CLI exit code 2. `AdmissionEngine.load` raises `AdmissionDenied` when
fresh admission fails, and also when post-execution runtime validation denies.
Inspect its `decision.target_executed` to distinguish those cases. Target
execution failure is represented by `ExecutionFailed` with an attached decision.

## Legacy exception formatting

The 0.4 compatibility validators still raise `ValueError` using the
`ContractViolation` hierarchy and a mutable `Bundle` of formatting context.
These are retained for existing callers; they are not the 0.5 admission record
format. Environment diagnostics redact values.

Migrate integrations that parse legacy exception text to structured decision
codes. See [migration](../migration-0.5.md) and the [API reference](../api-reference.md).
