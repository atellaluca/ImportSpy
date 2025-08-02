# Violation System

The Violation System in **ImportSpy** is responsible for surfacing clear, contextual, and actionable errors when a Python module fails to comply with its declared **import contract**.

Rather than raising generic Python exceptions, this subsystem transforms validation failures into precise, domain-specific diagnostics that are structured, explainable, and safe to expose in both development and production contexts.

---

## Purpose

In modular and plugin-based systems, structural mismatches and runtime incompatibilities can lead to subtle bugs, hard crashes, or silent failures.

The Violation System serves as a **contract enforcement layer** that:

- Captures detailed context about the failure (module, scope, variable, system)
- Distinguishes between **missing**, **mismatched**, and **invalid** values
- Produces **human-readable** error messages tailored to developers and CI pipelines
- Structures error reporting consistently across validation layers (module, runtime, environment, etc.)

---

## Core Concepts

### 1. `ContractViolation` Interface

An abstract base that defines the required interface for all contract violations. It ensures consistency across the different scopes (variables, functions, systems, etc.).

```python
class ContractViolation(ABC):
    @property
    @abstractmethod
    def context(self) -> str

    @abstractmethod
    def label(self, spec: str) -> str

    @abstractmethod
    def missing_error_handler(self, spec: str) -> str

    @abstractmethod
    def mismatch_error_handler(self, spec: str) -> str

    @abstractmethod
    def invalid_error_handler(self, spec: str) -> str
```

### 2. `BaseContractViolation`

A reusable abstract class that implements common logic for generating violation messages (e.g. missing values, mismatches, invalid values) across all scopes.  
It uses templates from `Errors` to construct consistent, high-fidelity diagnostics.

```text
Example output:
[Module Validation Error]: Variable 'API_KEY' is missing. - Declare it in the expected module.
```

---

## Specific Violation Classes

Each domain (Variable, Function, Runtime, etc.) has its own implementation:

| Class                     | Purpose                                                  |
|--------------------------|----------------------------------------------------------|
| `VariableContractViolation` | Handles variable mismatches or missing values           |
| `FunctionContractViolation` | Detects function mismatches and signature issues        |
| `ModuleContractViolation`   | Validates filename and version consistency              |
| `RuntimeContractViolation`  | Validates system architectures (`x86_64`, `arm64`, etc.)|
| `SystemContractViolation`   | Checks operating system and environment variable match  |
| `PythonContractViolation`   | Validates interpreter and Python version compatibility  |

Each one specializes the `.label()` method to return error-specific context (e.g., "Environment variable `MY_SECRET` is missing in production runtime").

---

## Dynamic Payload Injection via `Bundle`

Each violation operates with a shared mutable dictionary-like object called a **`Bundle`**:

```python
@dataclass
class Bundle(MutableMapping):
    state: Optional[dict[str, Any]] = field(default_factory=dict)
```

It serves two purposes:

- Collect **contextual information** at validation time (e.g., variable name, expected type)
- Dynamically populate **templated error messages** using the `Errors` constant map

This design allows error messages to adapt to the specific failure, with no hardcoding.

---

## Error Categorization

ImportSpy distinguishes between three primary error types:

| Category     | Description                                                              |
|--------------|--------------------------------------------------------------------------|
| `MISSING`     | A required entity (class, method, variable) was not found               |
| `MISMATCH`    | An entity exists but its value, annotation, or structure differs        |
| `INVALID`     | A value exists but does not belong to the allowed set (e.g., OS types)  |

The `Errors` constant defines templates for all categories, per context:

```yaml
"MISSING":
  "module":
    "template": "Expected module '{label}' is missing"
    "solution": "Add the module to your import path"
```

---

## Engineering Highlights

- **Encapsulation**: All formatting, message construction, and error typing is abstracted out of validators.
- **Separation of Concerns**: Validators focus only on logic, while violations handle messaging.
- **Templated Errors**: All violations draw from `Errors`, ensuring uniformity and easier localization or branding.
- **Composable Context**: The `Bundle` allows rich diagnostics without tight coupling between layers.

---

## Example Usage

```python
from importspy.violation_systems import VariableContractViolation

bundle = Bundle()
bundle["expected_variable"] = "API_KEY"

raise ValueError(
    VariableContractViolation(
        scope="module",
        context="MODULE_CONTEXT",
        bundle=bundle
    ).missing_error_handler("entity")
)
```

Produces:

```text
[Module Validation]: Variable 'API_KEY' is missing - Declare it in the target module.
```

---

## Future Extensions

The Violation System is designed to be:

- Extensible with new scopes (`Decorators`, `ReturnTypes`, `Dependencies`)
- Pluggable with i18n/l10n systems
- Renderable in **structured JSON** for machine processing in DevOps pipelines

---

## Summary

The Violation System is not just error handling — it is ImportSpy’s **engine of clarity**.  
It converts abstract contract mismatches into structured, interpretable diagnostics that empower developers to catch errors before runtime.

By modeling validation feedback as first-class entities, ImportSpy enables precise governance across modular codebases.
