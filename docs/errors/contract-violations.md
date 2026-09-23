# Understanding admission violations

`check` returns an ADMIT or DENY decision without executing the target. It can
report multiple policy violations together. Use stable codes from JSON or SARIF
for automation rather than parsing human message text.

```bash
importspy check plugin.py --contract policy.yml --format json
```

## Core codes

| Code | Meaning | Next step |
| --- | --- | --- |
| `ISPY-S001` | Unreadable or invalid Python source | Check the path, encoding, syntax, and scope rules. |
| `ISPY-S101` | Missing structural declaration | Add the required declaration or correct the contract. |
| `ISPY-S102` | Structural value, annotation, filename, or version mismatch | Compare the reported facts with the requirement. |
| `ISPY-S103` | Required structure remains unknown statically | Use inspectable declarations or explicitly redesign the runtime check. |
| `ISPY-D101` | Dependency denied by policy | Remove the dependency or review the policy. |
| `ISPY-D102` | Unresolved import | Check installations, import paths, and project-root configuration. |
| `ISPY-D103` | Required dependency not observed | Import the required dependency or revise the requirement. |
| `ISPY-D104` | Dependency version requirement failed | Install an allowed version and recheck. |
| `ISPY-D105` | Declaration requirement failed or unknown | Correct supported project metadata and the selected project root. |
| `ISPY-D106` | Origin requirement failed or unknown | Inspect PEP 610 metadata and the policy's origin fields. |
| `ISPY-D107` | Editable-install requirement failed or unknown | Use an installation whose metadata establishes the required state. |
| `ISPY-D108` | External distribution missing a policy entry | Review and add an explicit distribution rule. |
| `ISPY-R101` | Host OS, architecture, or implementation denied | Use an allowed host or update the requirement. |
| `ISPY-R102` | Host Python version denied | Use a permitted interpreter version. |
| `ISPY-R103` | Environment or secret requirement failed | Supply the required host configuration; values stay redacted. |
| `ISPY-R104` | No matching legacy deployment | Review the legacy architecture/system/Python alternatives. |
| `ISPY-R201` | Target failed during explicit execution | Inspect the application failure; target effects may already have occurred. |
| `ISPY-P101` | Required evidence unavailable or insufficient | Select a trusted provider and inspect verification/availability status. |
| `ISPY-C101` | Invalid contract or configuration | Correct the configuration; the CLI exits with code 2. |
| `ISPY-C199` | Admission tool failure | Report a minimal, redacted reproduction; the CLI exits with code 3. |

Unknown facts are not successful checks. In particular, `ISPY-S103` does not
cause ImportSpy to execute source to discover the answer. Unavailable evidence
causes denial when a policy requires that evidence.

## Reading a report

A violation contains its code, category, severity, phase, subject, message, and
optional location, expected/observed data, and remediation. Missing source
locations are left absent. A decision also records dependency inventory,
evidence status, hashes, host identity, and whether target execution occurred.

Warnings and notes do not cause denial by themselves. CLI exit codes are 0 for
ADMIT, 1 for DENY, 2 for invalid configuration, and 3 for tool failure. A directory
check reports all explicitly configured subjects; use the exit code as the
aggregate outcome and inspect individual decisions for details.

Compare the source hash, policy hash, host, project root, and installed versions
when local and CI outcomes differ. Separate checks can observe different
environments even though evaluation of the same facts is deterministic.

The deprecated `Spy` validators still raise `ValueError` with legacy formatting.
See [structured reporting](../advanced/violations.md),
[CLI usage](../modes/cli.md), and [migration](../migration-0.5.md).
