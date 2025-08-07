# ImportSpy

**Context‑aware import validation for Python modules**

ImportSpy is an open‑source Python library that brings structural and environmental awareness to Python’s import system.  
It introduces a new concept: the **import contract** — a versioned, declarative `.yml` file that describes exactly how and where a module is allowed to be imported.

This enables predictable, secure, and modular Python codebases, especially in complex or regulated environments.

---

## What is an Import Contract?

An import contract defines what a module expects from:

- The importing environment: operating system, CPU architecture, Python version, interpreter type
- Its internal structure: functions, classes, methods, arguments, annotations, variables
- Optional runtime conditions: environment variables, base classes, or structural patterns

If the context does not meet the declared conditions, ImportSpy blocks the import and raises a structured, human-readable error — before any runtime logic is executed.

---

## Key Features

- Declarative, YAML-based import contracts  
- Embedded and CLI validation modes  
- Structural enforcement: functions, classes, variables, method signatures  
- Runtime checks: OS, architecture, Python version, interpreter  
- Contract-driven plugin validation and safe extensibility  
- CI/CD‑friendly error reporting  
- Seamless integration with DevSecOps pipelines

---

## Use Cases

ImportSpy is designed for:

- Plugin frameworks with strict interface enforcement  
- Runtime protection against unsupported environments  
- Early validation in CI/CD and regulated deployments  
- Defensive boundaries between internal components  
- Automated structural checks during deployment

---

## Example: Embedded Mode

```python
from importspy import Spy

caller = Spy().importspy(filepath="contracts/spymodel.yml")
caller.MyPlugin().run()
```

---

## Example: CLI Mode

```bash
importspy src/mymodule.py -s contracts/spymodel.yml --log-level DEBUG
```

---

## Project Structure

ImportSpy is built around:

- `SpyModel`: defines expected structure and runtime environment  
- `Spy`: the engine that validates real vs declared conditions  
- Violation system: structured, human‑readable error reporting

---

## Documentation Overview

### Get Started
- [Quickstart](intro/quickstart.md)  
- [Installation](intro/install.md)  
- [Overview](intro/overview.md)

### Modes of Operation
- [Embedded Mode](modes/embedded.md)  
- [CLI Mode](modes/cli.md)

### Import Contracts
- [Contract Syntax](contracts/syntax.md)  
- [SpyModel Specification](advanced/spymodel.md)

### Validation Engine
- [Violation System](advanced/violations.md)  
- [Contract Violations](errors/contract-violations.md)

### Use Cases
- [Plugin-based Architectures](use_cases/index.md)

### API Reference
- [API Docs](api-reference.md)

---

## Architecture Diagram

![SpyModel UML](assets/importspy-spy-model-architecture.png)

---

## Why ImportSpy?

Python’s import mechanism is flexible, but not context-aware.  
ImportSpy adds a layer of governance and runtime validation, making your code more robust and secure.

It’s ideal for:

- Securing plugin boundaries  
- Enforcing internal interfaces  
- Preventing unsupported imports  
- CI/CD enforcement of import assumptions  
- Runtime compatibility in multi-environment systems

---

## Support and Community

If ImportSpy is useful in your infrastructure, consider:

- [Starring the project on GitHub](https://github.com/atellaluca/ImportSpy)  
- [Becoming a GitHub Sponsor](https://github.com/sponsors/atellaluca)

---

> ImportSpy is more than a validator — it’s a contract of trust between Python modules.
