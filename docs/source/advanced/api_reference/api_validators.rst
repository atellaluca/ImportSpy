The Validation Engine
=====================

ImportSpy’s validation system is a modular, extensible framework designed to enforce the integrity  
and runtime compatibility of any Python module protected by an **Import Contract**.  
Whether used in **embedded validation** (inside the module) or in **external CLI mode**,  
this engine guarantees that no module is loaded in an unauthorized or structurally inconsistent environment.

Core Validator Pipeline ⚙️
--------------------------

At the center of the engine is the `SpyModelValidator`, a coordinator that orchestrates multiple specialized validators.  
Each validator is responsible for comparing part of the actual runtime context or module structure against its declared expectations.

This pipeline enforces:

- ✅ Structural integrity  
- ✅ Environment compatibility  
- ✅ Runtime reproducibility  
- ✅ Compliance with declared variables and system settings

.. note::
   All validators are executed **at runtime**, just before the module is made accessible to the importing code.

Validation Modes Supported
---------------------------

The validation engine operates seamlessly across both execution modes:

- **🧬 Embedded Mode** — The module validates its own importer at the moment it is loaded.
- **🛠️ External Mode (CLI)** — The module is validated *before* execution begins, often in CI/CD or static validation workflows.

SpyModelValidator 🧠
---------------------

This is the **entry point** to the validation pipeline. It receives both:

- The expected structure (parsed from a `.yml` contract or inline SpyModel), and  
- The actual runtime data (extracted via introspection)

It dispatches these to domain-specific validators, collects results, and raises structured errors on failure.

.. autoclass:: importspy.validators.spymodel_validator.SpyModelValidator
   :members:
   :undoc-members:
   :show-inheritance:

Structural Validators 🔎
------------------------

These validators inspect the internal structure of the target module:

AttributeValidator 🔤
^^^^^^^^^^^^^^^^^^^^^

- Ensures global/module/class attributes exist  
- Validates `type`, `value`, and `scope` (class vs instance)  
- Supports default values and optional annotations

.. autoclass:: importspy.validators.attribute_validator.AttributeValidator
   :members:
   :undoc-members:
   :show-inheritance:

FunctionValidator 🛠️
^^^^^^^^^^^^^^^^^^^^^

- Verifies function/method presence  
- Checks signatures and return annotations  
- Detects function mismatches across versions or overrides

.. autoclass:: importspy.validators.function_validator.FunctionValidator
   :members:
   :undoc-members:
   :show-inheritance:

ArgumentValidator 🎛️
^^^^^^^^^^^^^^^^^^^^^^

- Validates function arguments against contract declarations  
- Supports type annotations and default value checks  
- Ensures complete function interface compliance

.. autoclass:: importspy.validators.argument_validator.ArgumentValidator
   :members:
   :undoc-members:
   :show-inheritance:

Environment & Runtime Validators 🌍
-----------------------------------

These components validate that the system attempting to import the module is authorized:

ModuleValidator 📦
^^^^^^^^^^^^^^^^^^

- Validates module metadata (`filename`, `version`, global `variables`)  
- Applies naming constraints defined in contracts

.. autoclass:: importspy.validators.module_validator.ModuleValidator
   :members:
   :undoc-members:
   :show-inheritance:

SystemValidator 🖥️
^^^^^^^^^^^^^^^^^^^

- Verifies OS name and version compatibility  
- Enforces required `env` variables (e.g., `API_KEY`, `DEPLOY_REGION`)  
- Useful for containerized and multi-host setups

.. autoclass:: importspy.validators.system_validator.SystemValidator
   :members:
   :undoc-members:
   :show-inheritance:

PythonValidator 🐍
^^^^^^^^^^^^^^^^^^

- Checks that the interpreter matches contract constraints  
- Supports semantic Python version matching  
- Verifies implementation type (`CPython`, `PyPy`, `IronPython`)

.. autoclass:: importspy.validators.python_validator.PythonValidator
   :members:
   :undoc-members:
   :show-inheritance:

RuntimeValidator 🚀
^^^^^^^^^^^^^^^^^^^^

- Validates CPU architecture (`x86_64`, `ARM64`, etc.)  
- Filters deployments that must only run on specific hardware targets  
- Useful for embedded devices, edge computing, and platform-specific plugins

.. autoclass:: importspy.validators.runtime_validator.RuntimeValidator
   :members:
   :undoc-members:
   :show-inheritance:

Extending the Engine 🧩
-----------------------

Want to add your own validator?

- Subclass any validator listed here  
- Implement the `.validate()` interface  
- Register it manually via `SpyModelValidator` or contract-driven hooks

This makes ImportSpy ideal for **internal compliance layers**, **custom rule sets**, or **secure enterprise environments**.

See also:

- :doc:`api_models` for understanding SpyModel structure  
