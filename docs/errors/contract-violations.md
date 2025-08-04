# Contract Violations

When an import contract is not satisfied, **ImportSpy** blocks the import and raises a detailed error message.  
These violations are central to the library's purpose: enforcing predictable, secure, and valid module usage across Python runtimes.

## How Violations Work

Every time a module is imported using ImportSpy (either in **embedded** or **CLI** mode), the system performs deep introspection and validation checks.

If something does not match the declared contract (`.yml`), ImportSpy will:

1. **Capture the context** (e.g., `MODULE`, `CLASS`, `RUNTIME`, etc.)
2. **Identify the type** of error:
   - `missing`: required element is absent
   - `mismatch`: expected vs actual values differ
   - `invalid`: unexpected or disallowed value found
3. **Generate a structured error message** including:
   - a human-readable message
   - exact label of the failing entity
   - possible solutions or corrective actions

These violations are raised as `ValueError`, but contain detailed introspection metadata under the hood.

---

## Error Categories

ImportSpy organizes violations into **logical layers**, based on what is being validated:

| Layer              | Validator Class         | Violation Raised                        |
|-------------------|--------------------------|------------------------------------------|
| Architecture/OS   | `RuntimeValidator`       | `RuntimeContractViolation`              |
| OS / Environment  | `SystemValidator`        | `SystemContractViolation`               |
| Python Interpreter| `PythonValidator`        | `PythonContractViolation`               |
| Module File       | `ModuleValidator`        | `ModuleContractViolation`               |
| Class Structure   | `ClassValidator`         | `ModuleContractViolation (CLASS_CONTEXT)` |
| Functions         | `FunctionValidator`      | `FunctionContractViolation`             |
| Variables / Args  | `VariableValidator`      | `VariableContractViolation`             |

Each of these violations inherits from `BaseContractViolation`, which provides:
- A consistent interface for labeling (`.label()`)
- Templated messages for each category
- A `Bundle` object used to inject dynamic context into the error

---

## Error Message Anatomy

A full ImportSpy violation message looks like this:

```
[MODULE] Expected variable `timeout: int` not found in `my_module.py`
→ Please add the variable or update your contract.
```

Each message consists of:
- `[CONTEXT]`: tells where the error occurred
- **Label**: dynamically generated from the contract structure
- **Expected/Actual**: shown for mismatch/invalid errors
- **Solution**: human-readable advice from the YAML spec

---

## Debugging Tips

- Use `-l DEBUG` when invoking ImportSpy via CLI to see exact comparison steps.
- Violations are deterministic and reproducible. If one fails in CI, it will fail locally too.
- You can inspect the violation context by capturing the `ValueError` and logging its message.

---

## 📋 Contract Violation Table

Below is a comprehensive list of all possible error messages emitted by ImportSpy:

--8<-- "errors/error_table.md"

---

## Related Topics

- [Contract Syntax](../contracts/syntax.md)
- [Embedded Mode](../modes/embedded.md)
- [CLI Mode](../modes/cli.md)
- [SpyModel Architecture](../advanced/spymodel.md)
