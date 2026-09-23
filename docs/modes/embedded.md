# Library admission and execution

Place admission in the application's loader, before it imports a candidate.
`AdmissionEngine.check` inspects source and returns a decision without executing
the target. The application chooses whether to proceed.

```python
from pathlib import Path
from importspy.domain import AdmissionRequest
from importspy.engine import AdmissionEngine
from importspy.reporters import HumanReporter

request = AdmissionRequest(
    subject=Path("plugin.py"),
    contract=Path("plugin.importspy.yml"),
)
engine = AdmissionEngine()
decision = engine.check(request)
print(HumanReporter().render(decision))
```

Unlike CLI sidecar discovery, the Python request uses the contract path supplied
by the caller. Omitting `contract` uses the default policy. Set `project_root`
when project declaration metadata or local source resolution needs an explicit
root.

## Execute after fresh admission

```python
from importspy.engine import AdmissionDenied, ExecutionFailed

try:
    module, executed_decision = engine.load(request, name="admitted_plugin")
except AdmissionDenied as error:
    print(error.decision.decision, error.decision.target_executed)
except ExecutionFailed as error:
    print(error.decision.violations)
else:
    print(executed_decision.target_executed)
```

`load` repeats admission with refreshed dependency metadata and executes the
exact source bytes it inspected. It does not accept an old decision as authority
to execute changed source. It rejects a name already present in `sys.modules`.
The loader does not modify `sys.path`; configure the application's normal import
environment first. Package-relative imports require an appropriate qualified
module name and an existing package context.

Execution runs arbitrary Python, including normal dependency imports. The
loader does not recursively admit dependency source or freeze the host
environment. Runtime validators supplied through `runtime_validators=(...)`
run **after top-level execution**. A later failure removes the loader's module
registration but cannot undo filesystem, network, or other effects.

The [extension guide](../extensions.md) documents evidence providers, pure
policy validators, and runtime validators. Network providers require explicit
selection and opt-in; loading those providers itself runs trusted Python code.

## Deprecated embedded validation

`Spy.importspy` remains a runtime-only compatibility API in 0.5 and is scheduled
for removal in 1.0. It emits `DeprecationWarning`, inspects an already loaded
module, and returns the same object without reloading it.

Embedding `Spy` inside a module does not prevent its earlier top-level code from
running. It cannot provide a pre-execution guarantee. New applications should
use source admission in their loader; existing applications should follow
[migration from 0.4](../migration-0.5.md).

See [static preflight](../static-preflight.md), [contract syntax](../contracts/syntax.md),
and the [security model](../security-model.md) for the limits of admission.
