# CLI Mode

ImportSpy can also be used **outside of runtime** to validate a Python module against a contract from the command line.

This is useful in **CI/CD pipelines**, **pre-commit hooks**, or manual validations — whenever you want to enforce import contracts without modifying the target module.

---

## How it works

In CLI Mode, you invoke the `importspy` command and provide:

- The path to the **module** to validate
- The path to the **YAML contract**
- (Optional) a log level for output verbosity

ImportSpy loads the module dynamically, builds its SpyModel, and compares it against the `.yml` contract.

If the module is non-compliant, the command will:

- Exit with a non-zero status
- Print a structured error explaining the violation

---

## Basic usage

```bash
importspy extensions.py -s spymodel.yml -l WARNING
```

### CLI options

+-----------------------------------------------------------------------------+
| Flag               | Description                                            |
|--------------------|--------------------------------------------------------|
| `-s, --spymodel`   | Path to the import contract `.yml` file                |
| `-l, --log-level`  | Logging verbosity: `DEBUG`, `INFO`, `WARNING`, `ERROR` |
| `-v, --version`    | Show ImportSpy version                                 |
| `--help`           | Show help message and exit                             |
+-----------------------------------------------------------------------------+
---

## Example project

Let’s look at a full CLI-mode validation example.

### Project structure

```
pipeline_validation/
├── extensions.py
└── spymodel.yml
```

### 📄 Source files

=== "extensions.py"

```python
--8<-- "examples/plugin_based_architecture/pipeline_validation/extensions.py"
```

=== "spymodel.yml"

```yaml
--8<-- "examples/plugin_based_architecture/pipeline_validation/spymodel.yml"
```

### 🔍 Run validation

```bash
cd examples/plugin_based_architecture/pipeline_validation
importspy extensions.py -s spymodel.yml -l WARNING
```

If the module matches the contract, the command exits silently with `0`.  
If it doesn't, you’ll see a structured error like:

```
[Structure Violation] Missing required method 'get_bar' in class 'Foo'.
```

---

## When to use CLI Mode

!!! tip "Use CLI Mode for automation"
    CLI Mode is ideal when you want to:
    
    - Validate modules **without changing their code**
    - Integrate checks in **CI/CD pipelines**
    - Enforce contracts in **external packages**
    - Run **batch validations** over multiple files

---

# Import Contract Syntax

An ImportSpy contract is a YAML file that describes:

- The **structure** expected in the calling module (classes, methods, variables…)
- The **runtime and system environment** where the module is allowed to run
- The required **environment variables** and optional secrets

This contract is parsed into a `SpyModel`, which is then compared against the actual runtime and importing module.

---

## ✅ Overview

Here’s a minimal but complete contract:

```yaml
filename: extension.py
variables:
  - name: engine
    value: docker
classes:
  - name: Plugin
    methods:
      - name: run
        arguments:
          - name: self
deployments:
  - arch: x86_64
    systems:
      - os: linux
        pythons:
          - version: 3.12
            interpreter: CPython
```

---

## 📄 filename

```yaml
filename: extension.py
```

- Optional.
- Declares the filename of the module being validated.
- Used for reference and filtering in multi-module declarations.

---

## 🔣 variables

```yaml
variables:
  - name: engine
    value: docker
```

- Declares top-level variables that must be present in the importing module.
- Supports optional `annotation` (type hint).

```yaml
  - name: debug
    annotation: bool
    value: true
```

---

## 🧠 functions

```yaml
functions:
  - name: run
    arguments:
      - name: self
      - name: config
        annotation: dict
    return_annotation: bool
```

- Declares standalone functions expected in the importing module.
- Use `arguments` and `return_annotation` for stricter typing.

---

## 🧱 classes

```yaml
classes:
  - name: Plugin
    attributes:
      - type: class
        name: plugin_name
        value: my_plugin
    methods:
      - name: run
        arguments:
          - name: self
    superclasses:
      - name: BasePlugin
```

Each class can declare:

- `attributes`: divided by `type` (`class` or `instance`)
- `methods`: each with `arguments` and optional `return_annotation`
- `superclasses`: flat list of required superclass names

---

## 🧭 deployments

This section defines where the module is allowed to run.

```yaml
deployments:
  - arch: x86_64
    systems:
      - os: linux
        pythons:
          - version: 3.12.9
            interpreter: CPython
            modules:
              - filename: extension.py
                version: 1.0.0
                variables:
                  - name: author
                    value: Luca Atella
```

### ✳️ Fields

| Field        | Type     | Description                                |
|--------------|----------|--------------------------------------------|
| `arch`       | Enum     | e.g. `x86_64`, `arm64`                     |
| `os`         | Enum     | `linux`, `windows`, `darwin`               |
| `version`    | str      | Python version string (`3.12.4`)           |
| `interpreter`| Enum     | `CPython`, `PyPy`, `IronPython`, etc.      |
| `modules`    | list     | Repeats the structure declaration per module |

This structure allows fine-grained targeting of supported environments.

---

## 🌱 environment

Environment variables and secrets expected on the system.

```yaml
environment:
  variables:
    - name: LOG_LEVEL
      value: INFO
    - name: DEBUG
      annotation: bool
      value: true
  secrets:
    - MY_SECRET_KEY
    - DATABASE_PASSWORD
```

- `variables`: can define name, value, and annotation
- `secrets`: only their presence is verified — values are never exposed

---

## Notes

- All fields are optional — contracts can be partial
- Field order does not matter
- Unknown fields are ignored with a warning (not an error)

---

## Learn more

- [Contract syntax](../contracts/syntax.md)
- [Contract violations](../errors/contract-violations.md)
