# Where ImportSpy fits

ImportSpy is a **policy-as-code admission layer for Python modules and dependencies**.

It does not create a compatible environment, replace a package manager, validate API payloads, or sandbox Python code.

Its job is different:

> Given this Python source, this host, the available dependency metadata and selected evidence, does this component satisfy the policy required to be admitted for execution?

That distinction matters because several existing Python tools solve related problems at different boundaries.

---

## The short version

A useful way to think about the ecosystem is:

```text
Build / reproduce the environment
        |
        |  uv, pip, mise, Nix, containers
        v
Resolve packages and runtime
        |
        v
-----------------------------------------
        IMPORTSPY ADMISSION BOUNDARY
-----------------------------------------
        |
        |  source + dependencies
        |  + host facts + evidence
        |  + policy
        v
     ADMIT / DENY
        |
        v
Explicit execution
        |
        v
Runtime behaviour and data
        |
        |  Pydantic, Typeguard, beartype,
        |  application-specific validation
        v
Application
```

ImportSpy operates at the boundary immediately before execution.

A dependency being installable does not necessarily mean it is allowed.

A module being importable does not necessarily mean it satisfies the host's policy.

A reproducible environment does not necessarily mean every component available inside that environment should be admitted.

---

# Importable is not the same as admissible

Consider this module:

```python
import packaging
import typer

print("THIS MUST NOT RUN")
```

Both dependencies may be correctly installed.

The Python version may be supported.

The environment may be perfectly reproducible.

The source may be syntactically valid.

And yet the host may have a policy saying:

```yaml
schema_version: 1

dependencies:
  packaging:
    allowed: true
  typer:
    allowed: false
```

ImportSpy can inspect the source and dependency metadata and return:

```text
DENY
```

without executing the target.

The question is not:

> Can Python execute this?

It is:

> Does policy allow this source to enter this runtime?

---

# Environment management and admission are different problems

Tools such as **uv**, **pip**, **mise**, **Nix**, virtual environments and containers are extremely useful for constructing and reproducing execution environments.

They answer questions such as:

```text
Which packages should be installed?

Which package versions can coexist?

Which Python version should be used?

Which operating-system dependencies are required?

Can this environment be reproduced elsewhere?
```

ImportSpy does not replace any of those tools.

It assumes an environment exists and asks another question:

```text
Given the environment that exists now,
is this particular Python component allowed to execute here?
```

For example:

```text
Dependency resolution                    ✓
Python version                           ✓
Operating system                         ✓
Environment reproducible                 ✓
Module importable                        ✓

Host policy:

dependency typer allowed                 ✗

                                      → DENY
```

A package manager can successfully resolve a package that an application policy deliberately rejects.

Those are not contradictory results.

They belong to different layers.

---

# Interfaces and admission are different problems

Python already provides excellent tools for describing interfaces.

An ABC can define an explicit inheritance contract:

```python
from abc import ABC, abstractmethod


class Processor(ABC):

    @abstractmethod
    def process(self, payload: bytes) -> bytes:
        ...
```

A Protocol can express structural compatibility:

```python
from typing import Protocol


class Processor(Protocol):

    def process(self, payload: bytes) -> bytes:
        ...
```

Static type checkers can reason about those interfaces before execution.

ImportSpy does not replace these mechanisms either.

An admission policy can include structural requirements, but it can also combine them with requirements from other layers:

```text
required callable structure
        +
dependency policy
        +
Python / OS / architecture constraints
        +
environment conditions
        +
selected external evidence
        =
admission decision
```

The important difference is that the decision belongs to the **host/component boundary**.

---

# Data validation and component admission are different problems

Tools such as **Pydantic** are commonly used at data boundaries:

```text
HTTP request
     |
     v
Pydantic validation
     |
     v
Application code
```

Runtime type-checking tools such as Typeguard or beartype can enforce type-related assumptions while Python code is executing.

Those are useful boundaries.

ImportSpy operates earlier:

```text
Python component
      |
      v
ImportSpy admission
      |
   ADMIT?
    /   \
  no     yes
  |       |
 stop     v
       execute
          |
          v
    application data
          |
          v
   runtime validation
```

ImportSpy is not primarily checking the values moving through a component.

It is deciding whether the component itself satisfies the policy required to enter the system.

This also means that checks which can be established statically do not need to be repeatedly enforced on an application's hot path.

---

# Static admission and runtime validation are separate

ImportSpy 0.5 deliberately separates these two phases.

The main pipeline is:

```text
Source
  |
  v
static preflight
  |
  v
dependency resolution
  |
  v
evidence collection
  |
  v
policy evaluation
  |
  v
ADMIT / DENY
  |
  | ADMIT
  v
explicit load
  |
  v
execution
  |
  v
optional runtime validation
```

`AdmissionEngine.check()` does not execute or import the inspected target.

Source inspection works from the source and its AST, while dependency admission uses packaging metadata rather than importing the observed dependencies.

If required facts cannot be established statically, ImportSpy can fail closed instead of executing the target merely to discover them.

See:

- [Static preflight](static-preflight.md)
- [Dependency admission](dependencies.md)
- [Security model](security-model.md)

---

# Why runtime validators still exist

Not every property can be established from source.

Some checks genuinely require Python runtime objects.

For those cases ImportSpy exposes `RuntimeValidator`.

Runtime validators execute only after explicit module execution.

This boundary is intentional.

Once Python execution starts, side effects may already have occurred:

```text
ADMIT
  |
  v
execute module
  |
  +--> filesystem
  +--> network
  +--> subprocess
  +--> global state
  |
  v
RuntimeValidator
```

A runtime denial cannot undo those effects.

For that reason, requirements that can be established before execution should normally remain on the admission side of the boundary.

See [Building an extension](extensions.md).

---

# Supply-chain tools and ImportSpy

Tools such as vulnerability scanners, provenance systems and attestation frameworks produce information about software artifacts.

Examples include:

- pip-audit
- OSV
- Sigstore
- SLSA-based systems

ImportSpy does not attempt to become all of those tools.

Instead, its extension model allows selected evidence providers to contribute observations to an admission decision.

Conceptually:

```text
vulnerability scanner ─┐
                       |
provenance verifier ───+──> evidence ──> ImportSpy policy ──> ADMIT / DENY
                       |
internal platform ─────┘
```

This keeps two responsibilities separate:

```text
Produce or verify a fact
          !=
Decide what application policy should do with that fact
```

Core ImportSpy does not manufacture cryptographic provenance from package metadata and does not contain a vulnerability scanner.

See [Supply-chain evidence](supply-chain.md) and [Building an extension](extensions.md).

---

# A comparison by responsibility

| Tool / concept | Primary responsibility |
| --- | --- |
| `pip`, `uv` | Package installation and dependency resolution |
| `mise` | Tool/runtime version management |
| Nix / containers | Reproducible or isolated execution environments |
| ABC / Protocol | Python interface contracts |
| mypy / pyright | Static type analysis |
| Pydantic | Runtime data validation |
| Typeguard / beartype | Runtime type enforcement |
| pip-audit / OSV | Known-vulnerability information |
| Sigstore / SLSA ecosystem | Artifact identity, attestations and provenance mechanisms |
| **ImportSpy** | **Policy-based admission of Python source before execution** |

These categories overlap in useful ways.

The point is not to replace the other layers.

The point is to make the admission boundary explicit.

---

# A practical example

Suppose an application discovers a third-party plugin.

The environment is already provisioned successfully:

```text
Python 3.12                       ✓
Linux                             ✓
requests 2.32 installed           ✓
internal SDK installed            ✓
```

The plugin is also syntactically valid:

```python
from internal_sdk import Client
import requests


def process(amount: int) -> str:
    ...
```

But the host contract requires:

```yaml
schema_version: 1

functions:
  - name: process
    arguments:
      - name: amount
        annotation: int
    return_annotation: str

runtime:
  python: ">=3.10"
  environment:
    PAYMENT_MODE: production

dependencies:
  requests:
    version: ">=2.32,<3"
    declared: true

  internal-sdk:
    editable: false

dependency_options:
  unresolved: deny
  undeclared: deny
  unlisted: deny
```

The environment may be valid while the component is still denied because, for example:

```text
PAYMENT_MODE is not satisfied             ✗

or

internal-sdk is an editable install       ✗

or

requests is not declared                  ✗

or

an additional unlisted dependency exists  ✗
```

That is the problem ImportSpy is designed to model.

---

# Why this matters for plugin systems

Plugin systems create a natural admission boundary.

A naive lifecycle is:

```text
discover
   |
   v
import
   |
   v
activate
```

A policy-aware lifecycle can instead become:

```text
discover
   |
   v
inspect
   |
   v
resolve dependencies
   |
   v
collect evidence
   |
   v
evaluate policy
   |
   +------ DENY
   |
   v
ADMIT
   |
   v
explicit load
   |
   v
activate
```

The host now has an explicit place where it can decide whether a component belongs in the system.

ImportSpy does not require every plugin to contain ImportSpy-specific code in order for the host to inspect it.

The policy belongs to the admission boundary.

---

# Why this may matter for AI tool runtimes

Modern AI tool systems often recreate a familiar plugin architecture:

```text
Agent
  |
  v
Tool registry
  |
  v
Python tool implementation
```

A tool schema can describe how a model should invoke a capability:

```json
{
  "name": "weather",
  "parameters": {
    "city": "string"
  }
}
```

But an AI-facing callable schema and an execution policy are not necessarily the same thing.

The underlying Python tool may still have assumptions about:

- dependencies
- runtime versions
- environment variables
- host capabilities
- source structure
- deployment policy
- externally verified evidence

That suggests a possible architecture:

```text
tool discovered
      |
      v
admission policy
      |
   +--+--+
   |     |
 DENY   ADMIT
         |
         v
 register tool
         |
         v
 expose to agent
```

ImportSpy can already provide the admission primitives needed to explore this architecture.

A complete AI-tool integration should still be treated as a separate integration case study and tested against a concrete agent/tool runtime.

---

# What ImportSpy is not

An `ADMIT` decision does **not** mean:

```text
this code is safe
```

It means:

```text
the inspected facts and selected evidence satisfy this policy
```

ImportSpy is not:

- a Python sandbox
- a package manager
- a vulnerability scanner
- an operating-system isolation boundary
- a proof that admitted code is non-malicious
- a cryptographic verifier by itself

Once execution begins, ordinary Python code can produce arbitrary side effects permitted by the surrounding process.

Use process, container, operating-system or other appropriate isolation when untrusted execution requires a real security boundary.

See the [security model](security-model.md).

---

# When ImportSpy is a good fit

ImportSpy becomes interesting when an application has an explicit component boundary and needs policy beyond simple dependency installation.

Typical examples include:

- plugin systems
- extensible Python applications
- controlled internal modules
- embedded Python components
- CI admission gates
- customer- or team-supplied extensions
- platform components developed independently
- tool registries where code should be reviewed before activation

The common question is:

> What must be true before this Python component is allowed to execute here?

---

# When another tool is probably the better answer

If the main problem is:

> How do I install compatible dependencies?

use a package/dependency manager.

If it is:

> How do I reproduce this entire environment?

use environment or system reproducibility tooling.

If it is:

> Does this object satisfy my static interface?

use Python's typing ecosystem.

If it is:

> Is this incoming JSON valid?

use a data-validation library.

If it is:

> Can I safely execute hostile Python code?

use a real isolation boundary.

ImportSpy is useful when the problem that remains is **admission policy**.

---

# The boundary in one sentence

> **ImportSpy does not create a compatible Python environment. It decides whether Python source satisfies the policies required to enter one.**