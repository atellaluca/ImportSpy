# Contract Syntax

ImportSpy contracts are written in YAML and describe the **structure and runtime expectations** of a Python module. These contracts can be embedded or validated externally (e.g., in CI/CD), and act as **import-time filters** for enforcing compatibility and intent.

A contract defines:
- What variables, classes, and functions a module must expose
- What runtime conditions are required (OS, architecture, Python version, etc.)
- How strict or flexible the structure must be

This document explains the full syntax supported in `.yml` contract files.

---

## Top-Level Structure

Every `.yml` contract is structured as follows:

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

## Fields Explained

### `filename`
The name of the target Python file or module this contract applies to.

### `version`
Optional string that defines the expected version of the module. Can be used to pin specific builds or releases.

---

## `variables`

Declares **global or module-level variables** the importer must provide.

```yaml
variables:
  - name: DEBUG
    value: true
    annotation: bool
```

Each variable entry supports:
- `name` (**required**): Variable name
- `value` (optional): Expected value
- `annotation` (optional): Expected type annotation as string (e.g., `"str"`, `"dict"`)

---

## `functions`

Specifies required functions in the importing module.

```yaml
functions:
  - name: load_config
    arguments:
      - name: path
        annotation: str
    return_annotation: dict
```

Each function supports:
- `name`: The function's name
- `arguments`: List of required arguments (each with optional `annotation`)
- `return_annotation`: Expected return type (as string)

---

## `classes`

Defines required class structures.

```yaml
classes:
  - name: Plugin
    attributes:
      - name: config
        annotation: dict
        value: {}
        type: instance
    methods:
      - name: execute
        arguments:
          - name: self
    superclasses:
      - BasePlugin
```

A class may include:
- `name`: Class name
- `attributes`: A list of attributes exposed by the class
  - `type`: Can be `"instance"` or `"class"` to indicate attribute level
- `methods`: Required method declarations (same format as top-level `functions`)
- `superclasses`: Optional list of superclass names expected

> Attributes are matched on name, annotation, and (if provided) value.

---

## `deployments`

This section defines **runtime constraints** in which the import is valid. It allows validation based on:

- Architecture
- Operating system
- Environment variables
- Python version and interpreter
- Declared modules

```yaml
deployments:
  - arch: x86_64
    systems:
      - os: linux
        environment:
          variables:
            - name: MODE
              value: prod
              annotation: str
        pythons:
          - version: "3.10"
            interpreter: CPython
            modules:
              - filename: plugin.py
```

### Deployment fields:

| Field        | Description                                 |
|--------------|---------------------------------------------|
| `arch`       | CPU architecture (e.g. `x86_64`, `arm64`)   |
| `systems.os` | Operating system (e.g. `linux`, `windows`)  |
| `environment.variables` | Required runtime env variables   |
| `pythons.version` | Required Python version (string)       |
| `pythons.interpreter` | Interpreter (e.g., `CPython`)      |
| `modules`    | Specific modules to check (with filename/version) |

> Note: all conditions are **AND-combined** within a deployment block.

---

## Matching Rules

ImportSpy uses a strict structural validator. Here are some notes:

- Variables, functions, and methods are matched **by name**.
- Annotations are matched **as plain strings** – no semantic typing or runtime evaluation.
- If an annotation is omitted, it is **not enforced**.
- Superclasses are checked only **by name**, not by inheritance tree resolution.

---

## Best Practices

- Use consistent annotations: `"str"`, `"dict"`, `"list"`, etc.
- Prefer matching exact function signatures for critical plugins
- Define environment constraints only when needed (e.g., `IMPORTSPY_MODE=prod`)
- Use `modules.filename` to enforce versioning in multi-plugin systems

---

## Related Sections

- [Contract Examples](examples.md)
- [SpyModel Architecture](../advanced/spymodel.md)
- [Contract Violations](../errors/contract-violations.md)
