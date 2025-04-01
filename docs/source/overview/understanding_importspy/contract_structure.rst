Contract Structure
==================

Introduction
------------

Import contracts are YAML-based files used by **ImportSpy** to describe the **expected structure, dependencies, and runtime requirements** of a Python module.  
They act as **execution-level contracts**, enabling the system to validate whether a module is being used in a compliant environment — across operating systems, Python interpreters, or deployment platforms.

These contracts are evaluated at runtime (in embedded mode) or via CLI (in external mode), and are automatically parsed into Python `SpyModel` objects during validation.

This page explains the **structure, hierarchy, and semantics** of import contracts and provides a **complete real-world example**.

Contract Format Overview
------------------------

The import contract is structured as a YAML document with the following **top-level directives**:

- `filename`: The main module name.
- `variables`: Global variables expected in the module.
- `functions`: Top-level functions.
- `classes`: Class definitions and their structure.
- `deployments`: Valid runtime environments that are permitted to execute the module.

Each directive maps directly to a validation layer in ImportSpy's architecture.  
The contract can be **partial** (you can specify only what you want to validate), but the **hierarchy must always be respected**.

Contract Schema
---------------

Below is the full structural hierarchy with explanation:

- `filename` *(str)*: The name of the module file to validate (e.g., `extension.py`).
- `version` *(optional)*: Expected version of the module.
- `variables` *(dict)*: Key-value pairs of expected global variables.
- `functions` *(list)*:
  - `name`: Name of the function.
  - `arguments`: Parameters of the function.
  - `return_annotation`: Expected return type.

- `classes` *(list)*:
  - `name`: Name of the class.
  - `attributes`:
    - `type`: `"class"` or `"instance"`
    - `name`: Attribute name.
    - `value`: Expected default value.
    - `annotation` *(optional)*: Expected type.
  - `methods`: Same structure as `functions`.
  - `superclasses`: Base classes the class should inherit from.

- `deployments` *(list)*:
  - `arch`: CPU architecture (`x86_64`, `ARM64`, etc.).
  - `systems` *(list)*:
    - `os`: Operating system (`windows`, `linux`, `macos`).
    - `envs` *(dict, optional)*: Expected environment variables.
    - `pythons` *(list)*:
      - `version`: Python version.
      - `interpreter`: Python interpreter (e.g., `CPython`, `PyPy`, `IronPython`).
      - `modules` *(list)*: Repeats the module definition (`filename`, `variables`, `functions`, `classes`).

Full Example
------------

Below is a real-world contract describing an IoT plugin module:

.. code-block:: yaml

   filename: extension.py
   variables:
     engine: docker
     plugin_name: plugin name
     plugin_description: plugin description
   classes:
     - name: Extension
       attributes:
         - type: instance
           name: extension_instance_name
           value: extension_instance_value
         - type: class
           name: extension_name
           value: extension_value
       methods:
         - name: __init__
           arguments:
             - name: self
         - name: add_extension
           arguments:
             - name: self
             - name: msg
               annotation: str
           return_annotation: str
         - name: remove_extension
           arguments:
             - name: self
         - name: http_get_request
           arguments:
             - name: self
       superclasses:
         - Plugin
     - name: Foo
       methods:
         - name: get_bar
           arguments:
             - name: self
   deployments:
     - arch: x86_64
       systems:
         - os: windows
           pythons:
             - version: 3.12.8
               interpreter: CPython
               modules:
                 - filename: extension.py
                   variables:
                     author: Luca Atella
             - version: 3.12.4
               modules:
                 - filename: addons.py
             - interpreter: IronPython
               modules:
                 - filename: addons.py
         - os: linux
           pythons:
             - version: 3.12.8
               interpreter: CPython
               modules:
                 - filename: extension.py
                   variables:
                     author: Luca Atella

Semantics of Deployment Blocks
------------------------------

The `deployments` section allows you to describe **different valid environments** for the module.  
Each combination of `arch` → `os` → `python` defines an **allowed execution context**.

If the top-level module definition exists **outside of `deployments`**, it means:
- **The module must exist in all environments**.
- It acts as a **global constraint**, enforced regardless of the architecture.

Usage Notes
-----------

- All fields are **optional**, but **hierarchy is mandatory**.
- Missing fields are not validated.
- The YAML is parsed into a `SpyModel`, which is then validated via ImportSpy’s internal logic.
- Contracts can be reused across different modes:
  - Embedded mode (`from importspy import Spy`)
  - CLI mode (`importspy -s spymodel.yml extension.py`)

Related Topics
--------------

- :doc:`embedded_mode`
- :doc:`external_mode`
- :doc:`defining_import_contracts`
