# Embedded Mode

In Embedded Mode, ImportSpy is embedded directly into the module you want to protect.  
When that module is imported, it inspects the runtime environment and the importing module.  
If the context doesn't match the declared contract, the import fails with a structured error.

---

## How it works

By using `Spy().importspy(...)`, a protected module can validate:

- The **runtime** (OS, Python version, architecture…)
- The **caller module’s structure** (classes, methods, variables, annotations…)

If validation passes, the module returns a reference to the caller.  
If not, the import is blocked and an exception is raised (e.g. `ValueError` or custom error class).

---

## Real-world example: plugin-based architecture

Let’s walk through a complete example.  
This simulates a plugin framework that wants to validate the structure of external plugins at import time.

### Project structure

```
external_module_compliance/
├── extensions.py          # The plugin (caller)
├── package.py             # The protected framework
├── plugin_interface.py    # Base interface for plugins
└── spymodel.yml           # The import contract
```

---

### 🧩 Source files

=== "package.py"

```python
--8<-- "examples/plugin_based_architecture/external_module_compliance/package.py"
```

=== "extensions.py"

```python
--8<-- "examples/plugin_based_architecture/external_module_compliance/extensions.py"
```

=== "spymodel.yml"

```yaml
--8<-- "examples/plugin_based_architecture/external_module_compliance/spymodel.yml"
```

---

## When to use Embedded Mode

Use this mode when:

- You want to **protect a module** from being imported incorrectly
- You’re building a **plugin system** and expect structural consistency from plugins
- You want to **fail fast** in invalid environments
- You need to enforce custom logic during `import` without modifying the caller

---

## Learn more

- [→ CLI Mode](cli.md)
- [→ Contract syntax](../contracts/syntax.md)
- [→ Error types](../errors/index.md)
