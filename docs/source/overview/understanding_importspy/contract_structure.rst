Import Contract Structure
==========================

Import contracts are the foundation of how ImportSpy performs validation.

They are **YAML-based configuration files** that describe both the **structure** of a Python module and the **execution environments** in which it is valid.

This page provides a deep dive into the schema, semantics, and flexibility of import contracts — and how they serve as **executable specifications** for modular systems.

Overview
--------

Each contract is made up of two primary blocks:

- **Module definition**: describes what the module must contain (e.g., classes, functions, metadata)  
- **Deployments**: lists the environments (OS, Python, interpreter) in which the module is allowed to run

Contracts can define either:

- **Global constraints**: structural requirements that apply to all deployments  
- **Deployment-specific overrides**: context-sensitive rules based on platform or interpreter

Top-Level Schema
----------------

Here is a reference of the main fields in a contract:

Top-Level Fields
~~~~~~~~~~~~~~~~

- ``filename`` *(str)*: The name of the module to validate  
- ``version`` *(str, optional)*: Expected module version (e.g., `__version__`)  
- ``variables`` *(dict)*: Top-level variables and their expected values  
- ``functions`` *(list)*: List of required functions  
- ``classes`` *(list)*: List of required classes and their details  
- ``deployments`` *(list)*: Permitted environments in which the module can be loaded  

Function Schema
~~~~~~~~~~~~~~~

Each function can define:

- ``name``: Function name  
- ``arguments``: List of parameter names and optional annotations  
- ``return_annotation``: Optional return type annotation

Class Schema
~~~~~~~~~~~~

Each class may include:

- ``name``: Class name  
- ``attributes``:  
  - ``type``: `"instance"` or `"class"`  
  - ``name``: Attribute name  
  - ``value``: Expected value  
  - ``annotation``: Optional type annotation  
- ``methods``: Follows the same format as functions  
- ``superclasses``: List of required base classes

Deployments Block
------------------

The ``deployments`` section defines runtime compatibility requirements:

- ``arch``: CPU architecture (e.g., `x86_64`, `arm64`)  
- ``systems``: list of operating systems and environment constraints  
  - ``os``: `linux`, `windows`, or `macos`  
  - ``envs``: Required environment variables (`KEY: value`)  
  - ``pythons``: Supported Python versions and interpreters  
    - ``version``: Python version (e.g., `3.12.8`)  
    - ``interpreter``: `CPython`, `PyPy`, etc.  
    - ``modules``: Nested module definitions required in that context

Global Module Definition (Baseline)
-----------------------------------

If you define a module structure **outside the `deployments:` section**,  
it acts as a **global baseline** — a structural requirement that applies to **all environments**.

This section can include:

- ``filename``, ``variables``, ``functions``, ``classes``  
- Shared interface contracts across platforms  
- The minimum valid structure for the module to ever be imported

.. note::
   This is semantically treated as a **lower bound**:  
   each deployment must satisfy the global structure plus any deployment-specific overrides.

Full Example
------------

Here is a complete import contract:

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

Validation Behavior
--------------------

- All fields are **optional**, but the **hierarchy must be respected**  
- Missing fields are simply skipped during validation  
- Order of items in lists (methods, attributes) is **not enforced**  
- Contracts are parsed into `SpyModel` objects during validation  
- Validation is consistent across both embedded and CLI modes

Related Topics
--------------

- :doc:`defining_import_contracts`  
- :doc:`spy_execution_flow`  
- :doc:`embedded_mode`  
- :doc:`external_mode`  
