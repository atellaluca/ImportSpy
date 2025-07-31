# What is ImportSpy?

**ImportSpy** is a Python library that brings context awareness to the most fragile point in the lifecycle of a module: its import.

It lets developers declare explicit import contracts — versionable `.yml` files that describe under which conditions a module can be imported. These contracts are validated at runtime, ensuring that the importing environment (and optionally the importing module) matches the declared requirements.

If the conditions are not satisfied, the import fails immediately, with a detailed and structured error message.

---

## Why use ImportSpy?

Python offers no built-in mechanism to control how and where a module can be imported. In modular systems, plugin frameworks, and regulated environments, this leads to:

- Unexpected runtime errors
- Hard-to-diagnose misconfigurations
- Fragile CI/CD workflows

ImportSpy solves this by introducing **import-time validation** based on:

- Runtime environment (OS, CPU, Python version, interpreter)
- Required environment variables and secret presence
- Structural expectations of the importing module (classes, methods, types…)

This results in safer, more predictable imports — whether you're building a plugin system, enforcing architectural rules, or protecting critical components.

---

## How does it work?

ImportSpy uses a **declarative import contract** — a `.yml` file written by the developer — to define expected conditions.

At runtime, this contract is parsed into a structured Python object called a **SpyModel**, which is used internally for validation.

Depending on the operation mode (Embedded or CLI), ImportSpy:

- Validates the runtime and system environment
- Optionally inspects the module that is importing the protected one
- Enforces declared constraints on structure, type annotations, variable values, and more

If all constraints are respected, the import succeeds.  
If not, a descriptive error is raised (e.g. `ValueError`, `ImportSpyViolation`).

---

## Key features

- ✅ Declarative, versionable `.yml` import contracts
- 🧠 Runtime validation of OS, CPU architecture, Python version/interpreter
- 🔍 Structural checks on the importing module (classes, methods, attributes, types)
- 🔐 Validation of required environment variables and secrets (presence only)
- 🚀 Dual operation modes: Embedded Mode and CLI Mode
- 🧪 Full integration with CI/CD pipelines
- 📋 Structured, human-readable error reports with actionable messages

---

## Who is it for?

ImportSpy is designed for:

- Plugin frameworks that enforce structural compliance
- Systems with strict version, runtime or security constraints
- Teams building modular Python applications
- Projects that need to validate import-time compatibility
- Open-source maintainers looking to define and enforce import boundaries

---

## What’s next?

- [→ Install ImportSpy](install.md)
- [→ Try a minimal working example](quickstart.md)
- [→ Learn about the operation modes](../modes/embedded.md)
