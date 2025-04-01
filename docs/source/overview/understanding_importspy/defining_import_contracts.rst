Defining Import Contracts
=========================

Understanding Import Contracts
------------------------------

In ImportSpy, **import contracts** are YAML-based configuration files that define the **structural and environmental constraints**  
under which a Python module is allowed to execute. These contracts are the external representations of what is internally parsed  
into a `SpyModel` — the core object used by ImportSpy during runtime validation.

An import contract allows developers to declare **explicit rules** about the environment, dependencies, structure, and runtime  
context a module expects when it is imported. This introduces a layer of **predictability, portability, and enforcement**  
typically missing from Python's dynamic import system.

Import contracts are fully declarative, extensible, and compatible with both **embedded validation** (inside the module)  
and **external validation** (via CLI or CI pipelines).

Use Cases
---------

Import contracts are ideal when:

- A module **must not run in arbitrary environments**
- You want to prevent execution in **incompatible operating systems**
- Specific **Python versions or interpreters** must be enforced
- The module depends on a **well-defined structure of classes, functions, or environment variables**
- You need to define **multi-environment deployment policies**

From Contract to Validation
---------------------------

ImportSpy parses `.yml` contracts into internal `SpyModel` objects. These are then validated against the **actual runtime environment**  
and importing context. If any mismatch is detected, **execution is blocked** before the module becomes accessible.

.. note::
   The contract file lives outside your module and is version-controllable. It is parsed only once per session and can be reused
   across environments.

Contract Principles
-------------------

- An import contract **does not describe how a module behaves**, but **how and where it is allowed to run**
- It enforces **environmental, runtime, and structural constraints**
- It is **dynamic and context-aware**, validating the environment before import
- It can declare **multiple deployments**, allowing flexible but controlled execution

Key Sections in a Contract
--------------------------

Import contracts support a rich schema divided into these key layers:

1. **Module-Level Definition**
   - `filename`: Name of the main module to protect
   - `variables`: Expected global variables (e.g., metadata like `plugin_name`, `engine`, `description`)
   - `functions`: Top-level functions with optional arguments and return annotations
   - `classes`: Class declarations with attributes, methods, and superclasses

2. **Deployments**
   A list of allowed runtime environments where the module can run.

   Each `deployment` includes:
   - `arch`: CPU architecture (e.g., `x86_64`, `ARM64`)
   - `systems`: List of OS-level system definitions

3. **Systems**
   Each `system` may define:
   - `os`: Target operating system (e.g., `linux`, `windows`)
   - `envs`: Required environment variables (`ENV_VAR`: `expected_value`)
   - `pythons`: Python runtimes allowed in this system

4. **Python Runtimes**
   Each Python runtime includes:
   - `version`: Python version (e.g., `3.12.8`)
   - `interpreter`: Optional interpreter type (`CPython`, `PyPy`, etc.)
   - `modules`: List of modules that must exist in this environment

5. **Modules (Nested)**
   - `filename`: Module name
   - `version`: Optional version to match
   - `variables`: Required module-level variables
   - `functions`, `classes`: Structural expectations at function/class level

.. note::
   You may define a `module` at the root level to indicate that **the entire environment must support this module regardless of deployment**.
   This acts as a **baseline structural constraint**.

Design Considerations
---------------------

- **Fields are optional**, but their hierarchical structure must be respected.
- Lists like `classes`, `methods`, and `attributes` are **order-independent**.
- Empty definitions are allowed — but if defined, **they must match** at runtime.
- The contract is parsed with strict validation: missing fields or structure mismatches cause immediate failures.

Minimal Example
---------------

.. code-block:: yaml

    filename: extension.py
    variables:
      plugin_name: core
    classes:
      - name: Extension
        attributes:
          - type: class
            name: extension_name
            value: core
        methods:
          - name: __init__
            arguments:
              - name: self
          - name: run
            arguments:
              - name: self
              - name: data
                annotation: str
            return_annotation: str
    deployments:
      - arch: x86_64
        systems:
          - os: linux
            envs:
              ENV: production
            pythons:
              - version: 3.12.8
                interpreter: CPython
                modules:
                  - filename: extension.py
                    variables:
                      author: Luca Atella

Final Notes
-----------

Import contracts are **the foundation of ImportSpy’s enforcement model**.  
By describing execution constraints externally, they create a **strict but flexible validation layer**  
that brings **determinism** to module imports in Python.

Their declarative nature makes them ideal for:
- embedding in distributed plugins
- validating deployment readiness in CI/CD pipelines
- enforcing policy compliance in sensitive environments

To understand how contracts are evaluated at runtime, refer to :doc:`spy_execution_flow`.
