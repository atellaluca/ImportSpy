Validation Engine
=================

ImportSpy provides a **modular validation engine** that enforces compliance between a target module  
and its associated **Import Contract**.

This validation engine operates transparently in both execution modes:

- **Embedded Validation** 🧬 – Where a module uses ImportSpy to **validate the context of its own importer**.
- **CLI/Pipeline Validation** 🛠️ – Where ImportSpy is run **externally** to validate a target module against a contract.

All validations are orchestrated by the `SpyModelValidator` and delegated to a rich set of internal validators,  
each responsible for checking a specific domain (structure, runtime, environment).

Core Responsibilities 🔎
------------------------

The validation system ensures that modules:

- Are executed in **approved environments** (e.g., OS, architecture, Python version)
- Contain all **required structural elements** (e.g., classes, attributes, methods)
- Match all **contractual expectations** defined in the Import Contract
- Respect **environmental and system constraints** (e.g., variables, superclasses)

SpyModelValidator 🏗️
---------------------

The `SpyModelValidator` is the **entry point** of the validation engine.

It orchestrates the entire process by comparing:

- The **expected model** (parsed from an Import Contract)
- The **actual structure** of the loaded Python module

.. autoclass:: importspy.validators.spymodel_validator.SpyModelValidator
   :members:
   :undoc-members:
   :show-inheritance:

Structural Validators 🧱
------------------------

These validators ensure the **internal structure** of the module matches expectations.

AttributeValidator 🔤
^^^^^^^^^^^^^^^^^^^^^

Validates presence and values of:

- Class-level attributes
- Instance-level attributes
- Global variables

.. autoclass:: importspy.validators.attribute_validator.AttributeValidator
   :members:
   :undoc-members:
   :show-inheritance:

FunctionValidator 🛠️
^^^^^^^^^^^^^^^^^^^^^

Ensures all declared methods and functions exist, with matching:

- Names  
- Signatures  
- Return annotations

.. autoclass:: importspy.validators.function_validator.FunctionValidator
   :members:
   :undoc-members:
   :show-inheritance:

ArgumentValidator 🎛️
^^^^^^^^^^^^^^^^^^^^^^

Validates function and method **arguments** against expectations for:

- Argument names  
- Annotations (type hints)  
- Default values

.. autoclass:: importspy.validators.argument_validator.ArgumentValidator
   :members:
   :undoc-members:
   :show-inheritance:

Runtime & Environment Validators 🌍
-----------------------------------

These validators ensure the execution environment meets all runtime constraints defined in the Import Contract.

ModuleValidator 📦
^^^^^^^^^^^^^^^^^^

Validates **module metadata** such as:

- Filename  
- Version  
- Declared global variables

.. autoclass:: importspy.validators.module_validator.ModuleValidator
   :members:
   :undoc-members:
   :show-inheritance:

SystemValidator 🖥️
^^^^^^^^^^^^^^^^^^^

Validates system-specific constraints:

- Supported OS (Linux, Windows, macOS)  
- Environment variables  

.. autoclass:: importspy.validators.system_validator.SystemValidator
   :members:
   :undoc-members:
   :show-inheritance:

PythonValidator 🐍
^^^^^^^^^^^^^^^^^^

Validates Python interpreter constraints:

- Required version (e.g., 3.10+)  
- Python implementation (e.g., CPython, PyPy)

.. autoclass:: importspy.validators.python_validator.PythonValidator
   :members:
   :undoc-members:
   :show-inheritance:

RuntimeValidator 🚀
^^^^^^^^^^^^^^^^^^^^

Validates hardware-level constraints:

- Supported CPU architectures (e.g., x86_64, ARM64)  
- Interpreter/platform-specific settings

.. autoclass:: importspy.validators.runtime_validator.RuntimeValidator
   :members:
   :undoc-members:
   :show-inheritance:
