# Admission architecture

ImportSpy is a policy-as-code admission engine for Python modules and their
observed dependencies. The local engine remains useful offline: it does not
require an account, send telemetry, or contact a control plane.

```text
Source bytes → SourceInspector → DependencyResolver → Evidence collection
                                                        ↓
                                      AdmissionPolicy + PolicyEngine
                                                        ↓
                                               AdmissionDecision
                                             ADMIT           DENY
                                               ↓              stop
                                     explicit load(request)
                                               ↓
                                     execute inspected bytes
                                               ↓
                                     optional runtime validators
```

`check` never executes target code, including on admission. `load` performs a
fresh admission and executes the captured bytes once only after admission. The
host's Python, operating system, architecture and requested environment
conditions can be inspected before loading a target. Checks requiring actual
runtime objects necessarily happen **after module initialization**, and cannot
prevent or undo its top-level effects. No part of this is a sandbox.

## Responsibilities

| Component | Responsibility | Executes target code? |
| --- | --- | --- |
| `SourceInspector` | Parse/compile syntax; collect lexical declarations, imports and uncertainty | No |
| `DependencyResolver` | Resolve local paths and installed distribution metadata; collect origins/declarations | No |
| Host evidence collection | Read host identity and requested environment conditions | No |
| `EvidenceProvider` | Collect explicitly selected external/local facts | Trusted plugin code runs |
| `PolicyEngine` | Compare collected facts to structural, runtime, dependency and evidence policy | No |
| `AdmissionEngine.check` | Orchestrate inspection, collection and pure evaluation | No |
| `AdmissionEngine.load` | Admit fresh source, execute captured bytes, run runtime validators | Yes |
| Reporters | Render an existing decision as human text, JSON or SARIF | No |
| `Spy.importspy`, `SpyModel.from_module` | Compatibility inspection of already loaded objects | Runtime introspection may invoke dynamic attributes |

Providers and validators are application-selected trusted code. Entry-point
loading executes Python and is not itself covered by the target no-execution
boundary. The engine never automatically imports all installed extensions.

## Data and policy

`domain.py` defines serializable `AdmissionRequest`, `AdmissionContext`,
`AdmissionDecision`, `Evidence`, `Violation`, dependency and origin records.
The decision includes source/policy identity and SHA-256 hashes, engine version,
host identity, dependencies, observations, violations, phases, timestamp,
`runtime_required`, and `target_executed`.

`Evidence.status` distinguishes `verified`, `observed`, `unknown`, and
`unavailable`; `phase` distinguishes static, host/runtime, and external collection.
Verification is scoped to the provider's stated fact. Observed installation
metadata is not cryptographic provenance. Static facts describe declarations,
not the eventual behavior of arbitrary Python code.

`AdmissionPolicy` extends the existing structural `SpyModel` vocabulary.
`schema_version: 1` is validated; `version` still constrains the target module's
version. Unknown fields are rejected. Contracts are loaded with safe YAML;
annotations are compared as text and never evaluated.

Policy evaluation performs no network or filesystem operations. Collection and
policy remain separate so applications can test deterministic decisions and
replace providers. JSON serialization of the same decision is stable; timestamps
and host/install metadata can differ between separate checks.

## Execution and limitations

The loader rejects an already loaded module name rather than replacing an
existing `sys.modules` entry. Execution or runtime-validation failure removes
its registration; it cannot roll back other effects. It does not alter
`sys.path`, install packages or implement an import hook. Configure the runtime's
normal import environment before loading; package-relative loading needs the
appropriate qualified name and package context.

Dependency resolution inventories imports in the inspected file, including
conditional/function imports. It is not recursive transitive dependency
validation and does not intercept dynamic imports. A project directory checks
only explicit configured subjects. Metadata caching is scoped to an engine
instance; explicit `load` refreshes it. Create a new engine after changing an
installation for independent check-only requests.

A future control plane can consume decisions and evidence without changing the
local enforcement API. Organizational dashboards, policy registries and approval
workflows are outside this repository; no core enforcement feature requires them.
