# Building an extension

ImportSpy exposes small Python protocols in `importspy.extensions`. Implement the
documented methods; inheritance from a framework base class is not required.

| Extension | Method | Responsibility |
| --- | --- | --- |
| `EvidenceProvider` | `collect(context, dependencies) -> Iterable[Evidence]` | Collect facts; declare `name` and `requires_network`. |
| `PolicyValidator` | `evaluate(policy, evidence, dependencies, context) -> Iterable[Violation]` | Evaluate collected facts without IO. |
| `RuntimeValidator` | `validate(module, decision) -> Iterable[Violation]` | Inspect objects after explicit execution. |
| `Reporter` | `render(decision) -> str` | Format a decision without rerunning checks. |

These objects are trusted application/plugin code. Loading a provider entry point
executes that package's Python code. They must never import the inspected target
during admission. Network declaration is an engine scheduling contract, not a
sandbox that prevents a dishonest provider from opening sockets.

## Complete offline provider

This provider describes the resolver's installed inventory. It deliberately emits
an observation, not cryptographic provenance:

```python
from collections.abc import Iterable
from importspy.domain import AdmissionContext, Dependency, Evidence

class InventoryProvider:
    name = "example-inventory"
    requires_network = False

    def collect(
        self, context: AdmissionContext, dependencies: list[Dependency]
    ) -> Iterable[Evidence]:
        names = sorted({
            dist.name
            for dependency in dependencies
            for dist in dependency.distributions
        })
        yield Evidence(
            kind="example.inventory",
            subject="dependencies",
            observed={"distributions": [name for name in names]},
            provider=self.name,
            status="observed",
            detail="Names copied from installed metadata; not provenance verification.",
        )
```

Require it in a contract:

```yaml
schema_version: 1
evidence_requirements:
  - kind: example.inventory
    subject: dependencies
    provider: example-inventory
    status: observed
```

Select the provider explicitly:

```python
from pathlib import Path
from importspy.domain import AdmissionRequest
from importspy.engine import AdmissionEngine

engine = AdmissionEngine(providers=(InventoryProvider(),))
decision = engine.check(AdmissionRequest(
    subject=Path("plugin.py"),
    contract=Path("plugin.importspy.yml"),
))
print(decision.decision)
```

The [tested checkout example](https://github.com/atellaluca/ImportSpy/tree/main/examples/admission)
contains this provider, a pure distribution allowlist validator, and runnable
contracts. From the checkout:

```bash
python -m examples.admission.extension_demo
poetry run pytest tests/test_examples.py
```

It admits an observed `packaging` inventory, denies an application allowlist
mismatch, and denies missing provider evidence. No credentials, network, or
provenance claims are involved.

## Add pure policy

The example's `DistributionAllowlist` reads the selected provider's inventory,
validates its shape, and compares names against an application-supplied allowlist.
It yields `EXAMPLE-P001` for unusable inventory and `EXAMPLE-P002` for a name outside
the allowlist. It performs no filesystem or network access.

```python
from examples.admission.extensions import DistributionAllowlist, InventoryProvider
from importspy.engine import AdmissionEngine

engine = AdmissionEngine(
    providers=(InventoryProvider(),),
    validators=(DistributionAllowlist(frozenset({"packaging"})),),
)
```

`examples` is checkout code, not an installed ImportSpy module; put your own
implementation in your extension package. Custom validators run alongside core
policy and cannot erase existing violations. Use a unique machine-readable code
prefix and return source locations only when known.

## Package a provider entry point

In your extension package's `pyproject.toml`:

```toml
[project.entry-points."importspy.evidence_providers"]
company-inventory = "company_inventory:InventoryProvider"
```

The value points to a zero-argument factory or class implementing the provider
protocol. After installing the extension in the checking environment:

```bash
importspy check plugin.py --provider company-inventory
```

Only explicitly named providers are loaded. Unknown or duplicate entry-point names
are configuration errors. The entry-point name used on the command line can differ
from the provider's `name`; evidence pins use the provider's declared name.

Provider names must be unique, nonempty strings and must not start with
`importspy`, which is reserved for authoritative core evidence. The engine stamps
returned records with the selected provider's identity.

Policy validators, runtime validators, and reporters are passed as Python objects.
Core does not auto-discover or register every installed extension, and the CLI
does not currently offer arbitrary custom validator or reporter entry points.

## Network, unavailable evidence, and caching

A network provider sets `requires_network = True`. Core skips its collection
unless `AdmissionEngine(allow_network=True)` or CLI `--allow-network` is selected.
A skipped or failed collector produces unavailable evidence. Required facts then
deny admission; optional missing facts alone do not.

Providers should use bounded requests, explicit endpoints, careful redirect and
credential handling, and documented caches. Cache keys must include the identity
of the artifact or fact, verification configuration, and freshness constraints.
Core does not supply a provider cache or infer that cached verification is current.

Each collector's complete iterable is validated before its evidence is appended.
If collection raises or yields invalid objects, its partial results are discarded.
Do not encode a failed verification as a truthy object accepted by a generic
evidence requirement; emit false, unknown, or unavailable as appropriate.

## Runtime validators and reporters

`AdmissionEngine(runtime_validators=(validator,)).load(request)` freshly checks
admission, executes the inspected target bytes, then calls the runtime validator.
The callback cannot prevent or roll back top-level effects. A runtime denial has
`target_executed: true`. An unknown static requirement must first be redesigned or
moved into an explicit runtime policy; `load` does not bypass a static denial.

To add output, implement `Reporter.render(decision)` and call it from your
application. Built-ins are `HumanReporter`, `JSONReporter`, and `SARIFReporter`.
Never repeat collection or load the target merely to format a decision.

See [evidence semantics](evidence.md), [supply-chain integration](supply-chain.md),
and the [community roadmap](community-roadmap.md) for contribution scopes.
