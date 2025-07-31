# Use Cases

ImportSpy brings contract-based validation to dynamic Python environments, enabling control, predictability, and safety.

Below are common scenarios where ImportSpy proves useful.

---

## Embedded Mode in Plugin Architectures

In plugin-based systems, a core module often exposes an interface or expected structure that plugins must follow.

With ImportSpy embedded in the core, plugins are validated at import time to ensure they define the required classes, methods, variables, and environment conditions.

This prevents silent failures or misconfigurations by enforcing structural and runtime constraints early.

---

## CLI Validation in CI/CD Pipelines

In DevOps pipelines or pre-release validation, ImportSpy can be run via CLI to ensure a Python module conforms to its declared import contract.

This use case is especially valuable in:

- Automated deployments  
- Open-source projects with modular extensions  
- Static validation of third-party contributions

---

## Restricting Import Access by Runtime Context

A module can use ImportSpy to refuse being imported unless specific runtime conditions are met — such as architecture, operating system, interpreter, or Python version.

This enforces strict execution environments and prevents unintended usage in unsupported contexts.

It's particularly helpful in:

- Security-sensitive modules  
- Packages intended for specific embedded systems  
- Conditional feature sets based on runtime capabilities

---

These use cases show how ImportSpy bridges runtime context and modular design through declarative contracts.
