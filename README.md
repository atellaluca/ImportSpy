# ImportSpy

![License](https://img.shields.io/github/license/atellaluca/importspy)
[![PyPI Version](https://img.shields.io/pypi/v/importspy)](https://pypi.org/project/importspy/)
[![Docs](https://img.shields.io/badge/docs-online-blue)](https://importspy.atellaluca.com)
![Python Versions](https://img.shields.io/pypi/pyversions/importspy)
[![Build Status](https://img.shields.io/github/actions/workflow/status/atellaluca/ImportSpy/ci.yml?branch=main)](https://github.com/atellaluca/ImportSpy/actions/workflows/ci.yml)

![ImportSpy banner](https://raw.githubusercontent.com/atellaluca/ImportSpy/refs/heads/main/docs/assets/importspy-banner_500px.png)

---

**ImportSpy** is a runtime contract enforcement engine for Python modules.

It allows developers to declare and verify **structural, contextual, and execution constraints** on imported modules, making explicit the architectural assumptions that in Python are normally implicit or unverified.

It is designed for modular systems, plugin architectures, embedded environments, and integration-heavy platforms.

ImportSpy formalizes architectural assumptions as executable contracts, making long-lived Python systems evolvable and governable over time.

---

## Problem

In Python, a module is considered valid as long as it successfully imports.  
There is no built-in mechanism to express or enforce assumptions about:

- required structure  
- allowed dependencies  
- execution environment  
- runtime invariants  
- contextual compatibility  

As a result:

- integration errors surface late, often in production  
- failures occur deep in execution flows  
- architectural assumptions remain informal  
- modular systems become fragile as they evolve  

This becomes especially problematic in systems that are plugin-based, dynamically extensible, multi-tenant, long-running, or integration-heavy.

---

## Approach

ImportSpy introduces a **declarative runtime contract** associated with each module.

The contract is authored in a YAML-based DSL and compiled into an internal `SpyModel`.  
It is validated **at import time** or during controlled initialization.

Contracts can express:

- required module structure  
- mandatory classes and functions  
- method signatures and types  
- runtime invariants  
- environmental constraints (OS, Python version, env vars)  
- dependency restrictions  

If a module violates its declared contract, the import fails deterministically with structured diagnostics.

This makes architectural assumptions:

- explicit  
- executable  
- versionable  
- enforceable at runtime  

---

## Core Concepts

### SpyModel

A `SpyModel` represents the **minimum acceptable contract** of a module.

It does not describe what a module *does*, but what it *must be* in order to be admitted into the runtime.

It can model:

- required attributes and callables  
- expected signatures and annotations  
- custom validation rules  
- restrictions on secondary imports  
- execution conditions and invariants  
- deployment compatibility constraints  

---

### Runtime Contract

A runtime contract:

- is verified dynamically  
- is versioned independently of code  
- is separated from implementation  
- acts as an **architectural boundary**  

It allows explicit governance over which modules are allowed to participate in a system.

---

### Controlled Import

ImportSpy does not replace Python's `import`.  
It **governs** it.

The import process is intercepted, validated, and either accepted or rejected based on the declared contract.

Modules that do not satisfy their contract are prevented from loading before any side effects occur.

---

## Example (YAML-first, Embedded Mode)

ImportSpy contracts are authored as declarative YAML files (typically `spymodel.yml`) and parsed into a `SpyModel` internally.

### 1) Contract (`spymodel.yml`)

```yaml
filename: plugin.py
version: "1.2.3"

variables:
  - name: MODE
    value: production
    annotation: str

functions:
  - name: initialize
    arguments:
      - name: self
      - name: config
        annotation: dict
    return_annotation: None

classes:
  - name: Plugin
    attributes:
      - name: settings
        value: default
        annotation: dict
        type: instance
    methods:
      - name: run
        arguments:
          - name: self
        return_annotation: None
    superclasses:
      - BasePlugin

deployments:
  - arch: x86_64
    systems:
      - os: linux
        environment:
          variables:
            - name: IMPORTSPY_ENABLED
              value: true
              annotation: bool
        pythons:
          - version: "3.11"
            interpreter: CPython
            modules:
              - filename: plugin.py
                version: "1.2.3"
```

---

### 2) Protected module (`plugin.py`)

```python
from importspy import Spy

caller = Spy().importspy(filepath="spymodel.yml")

caller.Plugin().run()
```

---

### 3) Importer (`main.py`)

```python
class Plugin:
    def run(self):
        print("Plugin running")

import plugin
```

If the module does not satisfy the contract, the import fails with structured diagnostics.

---

## Validation Model

ImportSpy uses a **subset compatibility strategy**.

The declared contract defines the minimum acceptable execution context.  
The runtime context must contain **at least** what the contract specifies.

Extra capabilities are allowed.  
Missing or incompatible capabilities are rejected.

This makes contracts evolution-friendly and future-proof by design.

---

## Typical Use Cases

ImportSpy is suitable when you:

- load third-party plugins  
- execute partially trusted code  
- maintain long-term compatibility  
- govern runtime extensions  
- enforce architectural invariants  
- want deterministic failure modes  

Typical domains include:

- plugin engines  
- modular backends  
- embedded or industrial platforms  
- integration orchestrators  
- long-lived service architectures  

---

## Design Principles

- Contract-first, not feature-first  
- Deterministic validation  
- No hidden side effects  
- Explicit and early failures  
- Low runtime overhead  
- No invasive dependencies  

---

## Project Status

ImportSpy is used in real-world modular systems and follows a conservative evolution strategy.

The public API is intentionally minimal and focused on correctness, readability, and long-term maintainability.

The project avoids framework lock-in and is designed to remain usable across different architectural styles.

---

## Documentation

The official and authoritative documentation for ImportSpy is available at:

https://importspy.atellaluca.com

It includes:

- the complete contract format specification  
- advanced validation semantics  
- runtime contract patterns  
- architectural rationale  
- embedded and CLI usage modes  
- structured error models  
- real-world examples  

The online documentation is the primary reference for all features and should be considered the source of truth for the current API and contract DSL.

---

## Talks & Community

The architectural concepts behind ImportSpy have been shared publicly within technical communities as part of a broader effort to promote runtime governance patterns for modular and extensible Python systems.

### ImportSpy: When Python modules know how to say no.  
**GDG Basilicata · Flash Talks Arena**

A community talk focused on *import-time contracts* and how modular systems can enforce architectural assumptions (Python version, OS, environment variables, and other runtime constraints) before executing non-conforming modules.

This talk introduces ImportSpy not as a utility library, but as an architectural governance layer for plugin-based and long-running backend systems.

**Resources**
- Slides (PDF, Italian): [ImportSpy GDG Basilicata talk](https://profile.atellaluca.com/assets/talks/importspy-gdg-basilicata-it.pdf)  
- Slides (PDF, English technical translation): [Runtime Contract Validation in Modular Python Systems](https://profile.atellaluca.com/assets/talks/importspy-runtime-contract-validation-en.pdf)  
- Official GDG Basilicata event page: https://gdg.community.dev/events/details/google-gdg-basilicata-presents-flash-talks-arena/  
- Community listing: https://www.pignolalug.it/iniziative/flash-talks-arena/

For a deeper architectural overview, see the full case study:  
https://profile.atellaluca.com/case-studies/importspy/

---

## Installation

```bash
pip install importspy
```

---

## Intentional Limitations

ImportSpy does **not**:

- sandbox Python code  
- replace OS-level security systems  
- isolate processes  
- promise protection against malicious code  

It is a tool for **architectural governance**, not for hard security.

---

## License

MIT License

---

## Author

Luca Atella  
Backend Engineer · Platform Architect · Systems Designer  

![ImportSpy logo](https://raw.githubusercontent.com/atellaluca/ImportSpy/refs/heads/main/docs/assets/importspy-logo_100px.png)
