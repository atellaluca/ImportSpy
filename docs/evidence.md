# Evidence and admission decisions

Evidence is a serializable fact used to explain an admission decision. Collection
and policy evaluation are separate: providers collect observations, while policy
validators evaluate them without performing network requests.

`AdmissionDecision` contains source and contract identities/hashes, engine version,
host information, dependencies, evidence, violations, phases, a timestamp, and the
ADMIT/DENY result. `target_executed` records whether the explicit execution boundary
was crossed. A plain `check` leaves it false.

## Evidence fields

| Field | Meaning |
| --- | --- |
| `kind` | A stable fact name, such as `dependency.version`. |
| `subject` | The entity described: distribution name, source path, or declaration name. |
| `observed` | A JSON-compatible value, or null when unavailable. |
| `expected` | Optional expected value when the collector knows it. |
| `provider` | The producer's identity. |
| `phase` | `static`, `runtime`, or `external`. |
| `status` | `verified`, `observed`, `unknown`, or `unavailable`. |
| `detail` | Optional explanation without credentials or private payloads. |

`verified` means that the producer established the stated fact using its documented
verification procedure. Its meaning is scoped to that fact: verified source syntax
does not prove arbitrary code is safe, and a verified declaration does not prove
every future runtime binding. Providers are trusted code; the engine does not
cryptographically authenticate a status string.

`observed` records available data without stronger verification. Installed package
version/origin metadata is observed. `unknown` represents a fact the current
method cannot establish; `unavailable` represents a failed or disabled collection
source.

## Core evidence

| Kind | Typical subject and observation |
| --- | --- |
| `source.syntax` | Source path and `valid` after parsing/compilation without execution. |
| `module.function.present`, `module.class.present` | Declaration name and presence. |
| `module.variable.present` | Declared variable name and presence. |
| `module.import` | Import name and static reference, location, and optional flag. |
| `dependency.classification` | Import name and resolver category. |
| `dependency.version` | Canonical distribution name and installed version. |
| `dependency.origin` | Canonical name and normalized origin record. |
| `dependency.declared` | Canonical name and true/false/null declaration state. |
| `dependency.editable` | Canonical name and true/false/null editable state. |
| `runtime.python`, `runtime.os`, `runtime.architecture`, `runtime.implementation` | Source path and observed host information. |
| `runtime.environment` | Environment variable name and requirement-match boolean. |
| `provider.availability` | Provider name and collection-unavailable status. |

Host evidence can use phase `runtime` during a static admission check because it
describes the host runtime, not an executed target. Inspect `target_executed` and
the decision's phases to distinguish host inspection from target execution.

## Evidence requirements

```yaml
schema_version: 1
evidence_requirements:
  - kind: example.inventory
    subject: dependencies
    provider: example-inventory
    status: observed
```

A requirement matches kind and subject exactly, optionally pins a provider, requires
the stated status, and requires a truthy observed value. The default required
status is `verified`; a verified fact also satisfies an `observed` requirement.
Unknown/unavailable facts, null values, false booleans, and empty values do not
satisfy requirements. Missing evidence produces `ISPY-P101`.

This small built-in rule checks evidence presence and status, not arbitrary
expressions, numeric thresholds, schema contents, or publisher identity. Use a
pure [PolicyValidator](extensions.md) for richer comparisons. Do not place a
nonempty error object in `observed` when the intended fact is false: the built-in
requirement evaluates truthiness.

A dependency `provenance: true` rule requires
`distribution.provenance` evidence for each observed matching distribution, with
a canonical distribution subject, verified status, and a truthy result. An
explicit evidence requirement can additionally pin the trusted provider.
See [supply-chain policy](supply-chain.md) for artifact-binding requirements.

## Failures, privacy, and reproducibility

Provider output is collected and validated as a batch. A provider that raises or
yields invalid objects contributes an unavailable marker, not its partial results.
Required evidence then fails closed. An optional unavailable provider alone does
not deny admission when no policy requires its facts.

The engine assigns returned evidence to the selected provider's name. Names must
be nonempty, unique within an engine, and outside the reserved `importspy` prefix.
Providers receive copies of core inputs, and cannot update the original dependency
inventory by mutating their arguments.

Core environment requirements report match booleans, not environment values.
Origin URLs remove userinfo, query strings, and fragments. Third-party providers
must redact their own evidence; the engine cannot identify arbitrary secrets
inside a custom payload.

Policy evaluation is deterministic for fixed policy and facts. Collection can
change when source, installed metadata, host state, or external evidence changes.
Decision timestamps are intentionally variable. No provider-response cache or
freshness guarantee is supplied by core; providers must document those semantics.

Human, JSON, and SARIF reporters consume the same decision. SARIF primarily carries
violations and known locations; JSON retains the full inventory and evidence.
