# What ImportSpy does

ImportSpy is a Python admission engine. It evaluates whether a source module and
its observed dependencies satisfy policy before an application admits it for
execution.

The lifecycle is:

```text
inspect → resolve → collect evidence → evaluate policy → ADMIT / DENY
                                                         │
                                          explicit load after ADMIT
                                                         │
                                        execution → runtime validation
```

A contract can require an interface, constrain external distributions and host
runtime, or require evidence from a trusted provider. Core resolution uses local
source paths and installed metadata. Evaluation remains separate from collection
and performs no network requests.

## Evidence and uncertainty

A decision contains source and contract identities, hashes, engine/environment
information, dependency inventory, evidence, violations, phases, and execution
state. Evidence distinguishes verified facts, observations, unknown facts, and
unavailable providers.

Static declarations are not proof of every runtime behavior. Decorators,
conditional definitions, computed values, and dynamic namespace changes can make
required facts unknown. ImportSpy denies those requirements without executing the
module. A later runtime validator is an explicit application choice.

## Boundaries

ImportSpy is not a sandbox, vulnerability database, SBOM generator, or package
manager. It does not replace OSV, pip-audit, Sigstore, or SLSA. Providers can turn
their outputs into evidence for admission policy.

Admission inspects the selected source and its import inventory, not every
transitive dependency's source. Execution can have side effects and the surrounding
environment can change. See the [security model](../security-model.md).

The open-source engine works offline without an account, telemetry, or a cloud
service. A separate control plane can consume structured decisions without
replacing local enforcement.

See [architecture](../architecture.md), [extensions](../extensions.md), and the
[migration guide](../migration-0.5.md) for the transition from runtime validation.
