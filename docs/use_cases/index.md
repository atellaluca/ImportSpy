# Use cases

ImportSpy fits an admission boundary where an application or CI job has Python
source, a policy, and an environment to inspect.

## Plugin loading

Check candidate plugin declarations and dependency policy before the application's
loader executes them. Require a `Plugin` class and `run` method, reject prohibited
distributions, then use explicit `AdmissionEngine.load` when admission succeeds.
The check validates source facts; it does not prove the plugin's behavior is safe.
See [library admission](../modes/embedded.md).

## CI admission

Commit contracts beside selected modules and run:

```bash
importspy check plugin.py --contract plugin.importspy.yml
```

Use a configured `importspy check .` to evaluate an explicit project subject list.
JSON supports custom automation; SARIF supports code-scanning integrations.
Install the project's dependencies in the checking environment so metadata
matches the environment being evaluated. See [CI integration](../ci.md).

## Dependency and origin policy

Reject a disallowed dependency, require supported versions, or prevent accidental
reliance on transitive dependencies through declaration requirements. For internal
packages, constrain observed VCS repository/revision or editable-install metadata.
Unresolved and ambiguous mappings remain visible rather than being guessed from
import names. See [dependency policy](../dependencies.md).

## Host compatibility

Express supported Python versions, operating systems, architectures, interpreter
implementations, and environment presence/value requirements. These checks
inspect the host without importing the target:

```yaml
runtime:
  python: ">=3.10,<4"
  os: [linux, windows]
  implementation: [CPython]
```

The report records host facts and redacted environment outcomes. A contract
accepting an environment does not certify that every package supports it.

## Existing supply-chain evidence

Require evidence from a trusted provider that consumes a scanner result or
verifies an artifact's provenance. Collection happens separately from policy
evaluation, with explicit network opt-in where needed. ImportSpy does not replace
the scanner, cryptographic verifier, or artifact identity checks.
See [evidence](../evidence.md) and [extensions](../extensions.md).

## Shared module contracts

Use `init` to generate a starter contract, review it, and maintain it with source
changes. Contributors can check a shared interface locally using the same policy
as CI. Computed values and dynamic interfaces may remain unknown; describe any
later runtime validation separately instead of promising a static guarantee.
See [contract examples](../contracts/examples.md).
