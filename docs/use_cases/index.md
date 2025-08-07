# Use Cases

ImportSpy brings contract-based validation to dynamic Python environments, enabling control, predictability, and safety.

Below are common scenarios where ImportSpy proves useful.

---

## Embedded Mode in Plugin Architectures

In plugin-based systems, a core module often exposes an interface or expected structure that plugins must follow.

With ImportSpy embedded in the core, plugins are validated **at import time** to ensure they define the required classes, methods, variables, and environment conditions.

This prevents silent failures or misconfigurations by enforcing structural and runtime constraints early.

!!! example "Example: Plugin Enforced at Import"
    ```python
    --8<-- "examples/plugin_based_architecture/package.py"
    ```

See also [Embedded Mode](../modes/embedded.md) and [Contract Syntax](../contracts/syntax.md) for YAML details.

---

## CLI Validation in CI/CD Pipelines

In DevOps workflows or during pre-release validation, ImportSpy can be executed from the command line to ensure a Python module conforms to its declared import contract.

Typical use cases:
- Automated deployment verification  
- Open-source plugin contributions  
- Validating extension points in modular codebases  

!!! example "Example: Validate via CLI"
    ```bash
    importspy extensions.py -s spymodel.yml -l INFO
    ```

See [CLI Mode](../modes/cli.md) for full usage.

---

## Restricting Import Access by Runtime Context

A module can refuse to be imported unless specific runtime conditions are met — such as CPU architecture, OS, Python version, or interpreter.

This enables:
- Targeted deployments (e.g., Linux-only, CPython-only)
- Restriction to known-safe execution environments
- Fail-fast behavior in unsupported contexts

Contracts can define system constraints like:

```yaml
deployments:
  - arch: x86_64
    systems:
      - os: linux
        pythons:
          - version: 3.12
            interpreter: CPython
```

If the runtime doesn't match, import fails with a clear error message.

---

## Contract-as-Code: Executable Documentation

ImportSpy contracts double as living specifications for module structure and environment assumptions.

Rather than maintaining separate interface docs, a `.yml` contract acts as:

- ✅ Interface specification  
- ✅ Compatibility schema  
- ✅ Runtime validator  

This approach improves communication in:
- Plugin-based systems  
- Collaborative teams sharing Python APIs  
- Educational or onboarding contexts  

!!! example "Example Contract Snippet"
    ```yaml
    classes:
      - name: Plugin
        methods:
          - name: run
            arguments:
              - name: self
    ```

Any contributor can run `importspy` or trigger the embedded validation to ensure conformance.

---

## Supporting Multiple Deployment Targets

Modules may need to support more than one runtime environment (e.g., Linux and Windows, or Python 3.10+).

ImportSpy contracts support listing **multiple valid deployments**, each with its own OS, interpreter, and version constraints.

```yaml
deployments:
  - arch: x86_64
    systems:
      - os: linux
        pythons:
          - version: 3.10
      - os: windows
        pythons:
          - version: 3.11
```

This enables the same module to be validated across CI matrices or downstream consumers with differing setups.

---

Together, these use cases show how ImportSpy bridges **runtime context and modular structure** through declarative contracts — empowering safer, more predictable Python architectures.
