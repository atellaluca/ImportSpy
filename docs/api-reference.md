# Python API reference

The 0.5 API separates source inspection, evidence collection, policy evaluation,
and explicit execution. Start with [library admission](modes/embedded.md) and
[architecture](architecture.md); use [extensions](extensions.md) for third-party
providers, validators, and reporters.

## Admission engine

`AdmissionEngine.check(AdmissionRequest(...))` returns an `AdmissionDecision`
without target execution. `load` performs fresh admission and explicitly executes
captured source bytes. `AdmissionDenied` and `ExecutionFailed` retain their
associated decision.

::: importspy.engine

## Requests, facts, and decisions

The shared domain records serialize to JSON through Pydantic's
`model_dump(mode="json")` and `model_dump_json()` methods. Decision schema version
and contract schema version describe separate record formats.

::: importspy.domain

## Contracts and policy

`AdmissionPolicy` extends the structural model. `load_policy` uses safe YAML and
returns the validated policy with its SHA-256 hash. `PolicyEngine.evaluate`
compares collected facts without performing I/O.

::: importspy.policy

## Static source inspection

`SourceInspector.inspect` reads, hashes, parses, and compiles source without
execution. `evaluate_structure` compares structural requirements with those
facts; `starter_contract` generates editable structural requirements.

::: importspy.inspection

## Dependency resolution

`DependencyResolver` uses source paths and installed metadata without importing
the target dependencies. An instance is a metadata snapshot; recreate it after
changing installations. Origin and declaration facts retain unknown states.

::: importspy.dependencies

## Extension protocols

Provider loading is explicit and executes trusted plugin code. `RuntimeValidator`
here is the post-execution protocol; it is distinct from the legacy class with
the same name in `importspy.validators`.

::: importspy.extensions

## Reporters

Human, JSON, and SARIF reporters render the same decision. A reporter does not
collect evidence or evaluate policy again.

::: importspy.reporters

## Legacy runtime compatibility

These modules support 0.4-style validation of already executed modules.
`Spy.importspy` is deprecated in 0.5, with removal planned for 1.0.
`SpyModel.from_module` is runtime introspection and can invoke dynamic attributes;
it is not static admission. See [migration](migration-0.5.md).

::: importspy.s

::: importspy.models

::: importspy.validators

::: importspy.violation_systems

::: importspy.persistences
