Defining Import Contracts
==========================

Import contracts are at the core of how ImportSpy enforces structural and runtime compliance.

They are **YAML-based declarations** that describe exactly how a Python module is expected to behave — not in terms of logic, but in terms of **structure, compatibility, and execution context**.

This page explains how to define contracts, what they contain, and how ImportSpy uses them to validate modules at import time.

What Are Import Contracts?
--------------------------

An import contract tells ImportSpy:

- 🔧 What a module **must contain** (functions, classes, attributes, variables)  
- 🧠 Where it **is allowed to run** (Python version, OS, architecture, interpreter)  
- 🔐 What **runtime conditions** must be met (environment variables, deployment setups)  

ImportSpy uses this contract to decide:  
> “Should I allow this module to be used — or block it immediately?”

Contracts are used in both validation modes:

- **Embedded mode**: the validated module validates the importer at runtime  
- **CLI mode**: a module is validated externally via `importspy -s contract.yml module.py`

When to Use Them
----------------

Use import contracts when:

- You need to **block incompatible modules** from being loaded  
- You want to define **clear structure and interface expectations**  
- Your code must **run only on certain platforms or interpreters**  
- You’re building a system with **extensible plugins or dynamic modules**  
- You need **environment-aware validation** during CI/CD or deployment

Import Contract Anatomy
------------------------

Import contracts follow a hierarchical schema, with two main areas:

Structure Requirements
~~~~~~~~~~~~~~~~~~~~~~

This defines what the module must expose:

- `filename`: expected module file name  
- `variables`: global-level constants or metadata  
- `functions`: expected functions (with arguments and annotations)  
- `classes`: expected classes, with methods, attributes, and superclasses  

Deployment Constraints
~~~~~~~~~~~~~~~~~~~~~~

This defines **where and under what conditions** the module is valid:

- `arch`: expected CPU architecture (e.g., `x86_64`, `arm64`)  
- `systems`: list of supported OS/platform combinations  
  - `os`: operating system (e.g., `linux`, `windows`)  
  - `envs`: required environment variables  
  - `pythons`: Python runtime environments  
    - `version`, `interpreter` (e.g., `CPython`, `PyPy`)  
    - `modules`: nested modules required in that Python env  

Contracts can declare **multiple deployments**, supporting flexibility while enforcing strict constraints.

Baseline Constraints (Global Scope)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you define module-level fields **outside the `deployments:` section**,  
they act as **baseline constraints** that apply to **all runtime environments**.

This is useful when:

- You want to enforce a shared structure across multiple deployments  
- The module must always expose certain classes, functions, or variables  
- You need a "lowest common denominator" for all environments

.. note::
   These top-level rules define a **lower bound** for compliance —  
   each `deployment` can extend or specialize these expectations,  
   but never violate or ignore the top-level contract.

Minimal Example
----------------

Here’s a basic contract example:

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

This contract:

- Requires a class `Extension` with specific methods and attributes  
- Enforces Linux OS, CPython 3.12.8, and a production environment  
- Declares `extension.py` as the expected module file  
- Requires a top-level variable `plugin_name`

Design Principles
------------------

- Contracts are **declarative**: no logic, only structure and expectations  
- All fields are optional — but if declared, they **must be met**  
- Lists like `classes`, `methods`, and `attributes` are **order-independent**  
- Contracts are parsed once per session for performance  
- Contracts can express **baseline rules** (outside deployments) or per-environment logic

Best Practices
--------------

- Start minimal: validate structure first, then layer on environment constraints  
- Version your contracts alongside your code — they are **enforceable documentation**  
- Use deployments to support different runtime contexts while keeping control  
- Always define `filename` — it's the root entry point for validation

What’s Next?
-------------

Now that you understand how to define contracts:

- See how ImportSpy executes validation in :doc:`spy_execution_flow`  
- Explore common validation patterns in the :doc:`validation_and_compliance` section  
- Learn how contracts behave in :doc:`embedded_mode` and :doc:`external_mode`  
