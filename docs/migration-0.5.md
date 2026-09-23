# Migrating from 0.4 to 0.5

ImportSpy 0.5 introduces static admission: inspect source, resolve dependencies,
collect evidence, and evaluate policy before choosing whether to execute a
module. Runtime introspection remains available for compatibility.

## Replace the primary workflow

```bash
importspy init plugin.py
importspy check plugin.py
importspy check plugin.py --contract policy.yml --format json
```

`init` creates `plugin.importspy.yml` from source declarations without importing
the target. Review generated dependency approvals and add the constraints you
need. `check` discovers that sidecar automatically or accepts `--contract`.
It evaluates admission without executing the target, including when admission
succeeds. Human, JSON, and SARIF output share the same decision model.

The old positional CLI invocation is deprecated and forwards to `check`.
`--spymodel` remains an alias for `--contract`. A static check cannot reproduce
arbitrary runtime reflection: dynamically created objects, computed values, and
conditional definitions can remain unknown. Consult the static preflight
reference before translating a runtime-only contract.

Exit codes are `0` for admission, `1` for denial, `2` for invalid configuration,
and `3` for a tool failure. Update CI jobs that previously assumed every error
had the same exit code.

## Contract compatibility and stricter validation

Existing structural fields such as `filename`, `variables`, `functions`,
`classes`, and `deployments` remain supported. The admission policy adds
`schema_version: 1`. The existing `version` field continues to mean the target
module's version; do not replace it with the contract schema number.

```yaml
schema_version: 1
filename: plugin.py
functions:
  - name: run
    arguments:
      - name: request
        annotation: Request
    return_annotation: Response
```

Unknown fields now fail validation at every structural nesting level. For
example, `returns: str` is rejected; use `return_annotation: str`. Previously
ignored misspellings can therefore make old files invalid. Correct the field
names instead of dropping the requirement.

Annotations now accept arbitrary strings, including `list[User] | None`, rather
than a fixed enumeration of built-in types. Existing annotation enum values
remain accepted. Annotation text is not evaluated as a Python expression.

Unresolved imports are denied by default. Correct missing installations or
project-root configuration, or explicitly configure the unresolved policy when
that uncertainty is acceptable. Generated contracts mark unresolved imports as
denied until reviewed. An import name is distinct from its distribution name;
use the dependency policy reference when translating existing dependency rules.

## Runtime compatibility API

`Spy.importspy(...)` is deprecated in 0.5, remains available throughout the 0.5
series, and is scheduled for removal in 1.0. It emits `DeprecationWarning` and
validates a module that has already executed. Use `AdmissionEngine.check` or
`importspy check` for static admission.

```python
from importspy import Spy
import trusted_plugin

# Runtime validation: trusted_plugin has already executed above.
validated = Spy().importspy(
    filepath="trusted-plugin-runtime.yml",
    info_module=trusted_plugin,
)
assert validated is trusted_plugin
```

The method now returns the exact provided module. It does not reload it, remove
it from `sys.modules`, or discard runtime mutations. Contracts without
`deployments` validate their top-level structural constraints successfully.
Code relying on the former repeated execution must move that initialization
into an explicit application operation.

`SpyModel.from_module(module)` also inspects the supplied, already loaded object
without reloading or unregistering it. The returned model exposes the module
structure directly and retains the legacy deployment representation. Runtime
inspection can invoke dynamic Python attributes, so it belongs after admission
and is appropriate only for trusted code. Embedding a `Spy` call inside a module
cannot prevent that module's earlier top-level effects.

## Environment and YAML handling

Environment validation diagnostics redact values; debug logs report counts
instead of dumping expected and observed variables. Secret requirements test
names, and environment string representations list names only. The legacy
runtime model still contains observed environment values in memory for value
comparison: do not serialize or publish a full runtime model containing secrets.
Admission reports follow their separate evidence-redaction rules.

Contract files use safe YAML construction. Python object tags, unknown tags,
duplicate keys, and a non-mapping document root are rejected. YAML reading no
longer preserves arbitrary custom tags or round-trip formatting. Ordinary YAML
mappings remain supported.
