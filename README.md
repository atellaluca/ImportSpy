# ImportSpy

![License](https://img.shields.io/github/license/atellaluca/importspy)
[![PyPI Version](https://img.shields.io/pypi/v/importspy)](https://pypi.org/project/importspy/)
[![Docs](https://img.shields.io/badge/docs-online-blue)](https://atellaluca.github.io/ImportSpy/)
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

In Python:

- a module is considered valid as long as it *imports*
- assumptions about shape, dependencies, and side effects remain informal
- failures emerge late, often in production
- there is no clear boundary between **API**, **runtime behavior**, and **execution context**

This makes the evolution of systems fragile, especially when they are:

- plugin-based  
- multi-tenant  
- long-running  
- dynamically loaded  

---

## Approach

ImportSpy introduces a **declarative contract** associated with a module, expressed through a YAML-based DSL and compiled into a `SpyModel`.

The contract is verified **at import time** or during controlled initialization, and can cover:

- module structure  
- required public symbols  
- allowed or forbidden dependencies  
- runtime invariants  
- contextual constraints (e.g., environment, flags, configuration)  

Contract failures are **deterministic, immediate, and diagnosable**.

---

## Key Concepts

### SpyModel

A `SpyModel` describes what a module **must be** at a structural and contextual level, not just what it exposes as an API.

It models the **minimum acceptable contract** of a module in terms of:

- required attributes and callables  
- expected types and signatures  
- custom validation rules  
- restrictions on secondary imports  
- execution conditions and invariants  

---

### Runtime Contract

The contract:

- is verified at runtime  
- is versionable  
- is separated from the implementation  
- acts as an **architectural boundary**  

It allows explicit governance over which modules are allowed to enter the runtime.

---

### Controlled Import

ImportSpy does not replace Python’s `import`, it **governs** it:

- intercepts  
- validates  
- fails explicitly  

Modules that do not satisfy their declared contract are prevented from loading.

---

## Example (Embedded Mode, YAML-first)

ImportSpy contracts are authored as a declarative YAML file (typically `spymodel.yml`) and parsed into a `SpyModel` internally.

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

### 2) Protected module (`plugin.py`)

```python
from importspy import Spy

caller = Spy().importspy(filepath="spymodel.yml")

# Example: call something from the importer
caller.Plugin().run()
```

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

ImportSpy uses a **subset compatibility strategy**:

- the declared contract defines a minimum acceptable execution context  
- the runtime context must contain **at least** what the contract specifies  
- extra capabilities are allowed  
- missing or incompatible capabilities are rejected  

This makes contracts **future-proof** and evolution-friendly by design.

---

## Typical Use Cases

ImportSpy is suitable when you:

- load third-party plugins  
- execute partially trusted code  
- maintain long-term compatibility  
- govern runtime extensions  
- want to make system invariants explicit  

Typical domains include:

- plugin engines  
- industrial or embedded systems  
- integration orchestrators  
- long-lived modular backends  

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

- Used in real-world modular systems  
- Stable and conservative public API  
- Focused on correctness and readability  
- No framework lock-in  

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

![ImportSpy logo](https://raw.githubusercontent.com/atellaluca/ImportSpy/refs/heads/main/docs/assets/importspy-logo_100px.png)
