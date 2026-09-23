# ImportSpy

**Policy-as-code admission for Python modules and dependencies.**

ImportSpy inspects Python source, resolves its external dependencies, collects
evidence, and evaluates policy before you choose to execute the module.

```bash
pip install importspy
importspy init plugin.py
# Review the generated plugin.importspy.yml.
importspy check plugin.py
```

A check never imports the target, including when the decision is ADMIT.
The [quickstart](intro/quickstart.md) demonstrates a dependency denial that
prevents a top-level print statement from running.

## What admission evaluates

| Layer | What it checks |
| --- | --- |
| Static preflight | Syntax, declarations, signatures, annotations, imports, and known literal values. |
| Dependencies | Distribution identity, versions, declarations, origins, and editable installations. |
| Host runtime | Python, OS, architecture, interpreter implementation, and environment requirements. |
| Evidence | Facts from core and explicitly selected trusted providers. |
| Policy | Consistent violations and an ADMIT or DENY decision. |

Human, JSON, and SARIF output derive from the same decision. Required facts that
cannot be established statically fail closed. Execution is a separate explicit
library operation; runtime validators run after that execution.

## Read next

- [Quickstart](intro/quickstart.md) and [installation](intro/install.md).
- [Contract syntax](contracts/syntax.md), [examples](contracts/examples.md), and [CLI](modes/cli.md).
- [Dependency policy](dependencies.md), [static preflight](static-preflight.md), and [library usage](modes/embedded.md).
- [Architecture](architecture.md), [extensions](extensions.md), and [API reference](api-reference.md).
- [CI](ci.md), [security model](security-model.md), and [migration from 0.4](migration-0.5.md).

Core admission works offline without an account or telemetry. ImportSpy is not a
sandbox or a vulnerability scanner: it enforces policy using available evidence.
