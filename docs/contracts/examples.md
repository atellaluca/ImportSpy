# Contract Examples

This page provides complete examples of import contracts (`.yml` files) supported by ImportSpy.

Each example demonstrates how to declare structural expectations and runtime constraints for a Python module using the SpyModel format.

---

## Basic Module Contract

This example defines a simple module called `plugin.py` with one variable, one class, and one method.

```yaml
filename: plugin.py
variables:
  - name: mode
    value: production
    annotation: str
classes:
  - name: Plugin
    methods:
      - name: run
        arguments:
          - name: self
        return_annotation: None
deployments:
  - arch: x86_64
    systems:
      - os: linux
        pythons:
          - version: 3.11
            interpreter: CPython
```

---

## Function With Typed Arguments

This contract describes a module where the `analyze` function requires two arguments with specific types.

```yaml
filename: analyzer.py
functions:
  - name: analyze
    arguments:
      - name: self
      - name: data
        annotation: list[str]
      - name: verbose
        annotation: bool
    return_annotation: dict
deployments:
  - arch: x86_64
    systems:
      - os: linux
        pythons:
          - version: 3.12
            interpreter: CPython
```

---

## Class With Attributes and Methods

This contract defines a module that exposes a `TaskManager` class with attributes and a method.

```yaml
filename: manager.py
classes:
  - name: TaskManager
    attributes:
      - name: tasks
        annotation: list[str]
      - name: state
        annotation: str
    methods:
      - name: reset
        arguments:
          - name: self
        return_annotation: None
deployments:
  - arch: arm64
    systems:
      - os: darwin
        environment:
          variables:
            - name: MODE
              value: development
              annotation: str
        pythons:
          - version: 3.11
            interpreter: CPython
```

---

## Runtime-Only Validation

This contract enforces only environmental and interpreter constraints — no structural validation.

```yaml
deployments:
  - arch: x86_64
    systems:
      - os: linux
        pythons:
          - version: 3.10
            interpreter: CPython
```

---

## Multiple Deployments

If your module supports multiple platforms, you can define multiple `deployments`.

```yaml
filename: plugin.py
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
          - version: 3.11
            interpreter: CPython
  - arch: arm64
    systems:
      - os: darwin
        pythons:
          - version: 3.12
            interpreter: CPython
```

---

## Using Environment Variables

This example enforces that an environment variable is set and has a given type.

```yaml
filename: checker.py
deployments:
  - arch: x86_64
    systems:
      - os: linux
        environment:
          variables:
            - name: DEBUG
              value: "true"
              annotation: str
        pythons:
          - version: 3.10
            interpreter: CPython
```

---

## Related Topics

- [Contract Syntax](syntax.md)
- [Violation System](../advanced/violations.md)
- [SpyModel Architecture](../advanced/spymodel.md)
