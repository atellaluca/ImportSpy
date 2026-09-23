# Security policy

ImportSpy enforces policy using source declarations, installed package metadata,
and explicitly selected evidence providers. An admitted module is not proven
safe. Static inspection is not a Python sandbox, and dependency metadata alone
does not establish artifact integrity or cryptographic provenance.

## Report a vulnerability privately

Contact maintainer Luca Atella at **info@atellaluca.com**, the maintainer address
listed in the package metadata. Use the subject `ImportSpy security report`.
Do not open a public issue with an exploit, credentials, or sensitive evidence.
This repository does not assume that GitHub private vulnerability reporting is
enabled.

Include the affected version, Python/OS details, a minimal reproduction, the
policy and invocation used, expected versus observed behavior, and the practical
impact. Share a harmless local reproduction where possible. Redact real tokens,
private repository URLs, and personal data. If the report requires a sensitive
attachment, first ask the maintainer for an appropriate transfer method.

The maintainer will coordinate investigation, fixes, and disclosure with the
reporter. This volunteer project cannot promise a response deadline. Please
allow time to investigate and coordinate disclosure before publishing exploit
details.

## Supported versions

Security fixes target the current 0.5 release line. Upgrade older installations;
backports to 0.4 and earlier are not guaranteed. The migration guide explains the
runtime-only behavior retained by compatibility APIs.

## Boundaries relevant to reports

- `AdmissionEngine.check` and CLI `check` / `init` must not import or execute the
  target. Bypasses of that boundary, unsafe contract parsing, and policy
  requirements silently ignored are security-relevant reports.
- `AdmissionEngine.load` explicitly executes admitted code. Target imports and
  runtime validators can have side effects, and a later runtime failure cannot
  undo them. `Spy.importspy` validates code that has already executed.
- Source analysis covers the inspected subject, not arbitrary behavior of every
  transitive import. Passing structural policy does not prove behavioral safety.
- Evidence providers, custom validators, reporters, and their installed entry
  points are trusted code. Network opt-in is a provider contract, not isolation.
  A provider must correctly bind verified claims to the artifact being checked.
- Admission reports should not expose environment values or credentials.
  The legacy `SpyModel.from_module` snapshot retains environment values in memory
  for comparison; applications must not publish that full snapshot.

Report routine usability bugs through the public issue templates. Preserve the
license and avoid claims that policy enforcement replaces independent scanner,
attestation verification, or application isolation controls.
