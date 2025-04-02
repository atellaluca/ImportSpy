Utilities & Mixins: Internal Tools for Reflection and Runtime Enforcement
=========================================================================

ImportSpy’s validation engine is powered by a suite of **utility classes** and **mixins**  
that enable deep introspection of modules, environments, and Python runtimes.  
These components provide the **mechanical backbone** for runtime analysis, structural extraction,  
and platform compatibility checks across both **embedded** and **external** validation modes.

This layer is not typically exposed to end-users—but is invaluable for contributors,  
integrators, and advanced developers extending ImportSpy’s logic or building custom tooling.

Utility Modules ⚙️
------------------

Each utility module encapsulates a specific aspect of **runtime introspection**, enabling:

- 🔍 Extraction of class/function signatures, annotations, and globals  
- 🧠 Detection of system identity (OS, architecture, interpreter, etc.)  
- 🔐 Compliance checks for cross-platform and interpreter-specific constraints  
- ⚙️ Lightweight, cached evaluation of runtime conditions

These utilities are **orchestrated automatically** by the validation pipeline but can also  
be used independently to write tools or perform standalone validations.

ModuleUtil – Structural Reflection 🧱
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This utility performs deep reflection on a Python module, extracting:

- Public/private classes  
- Methods and their argument signatures  
- Attribute values and types  
- Class hierarchies and superclasses  
- Function return annotations

.. autoclass:: importspy.utilities.module_util.ModuleUtil
   :members:
   :undoc-members:
   :show-inheritance:

SystemUtil – OS & Environment Detection 🌐
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Gathers platform metadata such as:

- OS name (`linux`, `windows`, etc.)  
- Hostname, architecture  
- Environment variable inspection and resolution

.. autoclass:: importspy.utilities.system_util.SystemUtil
   :members:
   :undoc-members:
   :show-inheritance:

PythonUtil – Interpreter Validation 🐍
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Identifies the active interpreter and Python version with semantic normalization.  
Also verifies whether the environment satisfies version-based or interpreter-based constraints  
declared in the import contract.

.. autoclass:: importspy.utilities.python_util.PythonUtil
   :members:
   :undoc-members:
   :show-inheritance:

RuntimeUtil – Hardware & Architecture Awareness 🧬
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Provides a detailed overview of:

- CPU architecture (`x86_64`, `arm64`, etc.)  
- Runtime compatibility with deployment targets  
- Cross-architecture filtering logic for contract enforcement

.. autoclass:: importspy.utilities.runtime_util.RuntimeUtil
   :members:
   :undoc-members:
   :show-inheritance:

Mixin Components 🔁
-------------------

ImportSpy also uses **mixins** to modularize logic that applies across validators and inspectors  
without duplicating functionality or creating deep class hierarchies.

These reusable components inject specialized logic into validation classes where needed.

AnnotationValidatorMixin 🏷️
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Ensures that function signatures and variable annotations match the declared expectations.  
It supports:

- Basic type matching (`str`, `int`, etc.)  
- Optional and generic annotations  
- Graceful fallback for missing or untyped values

.. autoclass:: importspy.mixins.annotations_validator_mixin.AnnotationValidatorMixin
   :members:
   :undoc-members:
   :show-inheritance:

📌 Tip:
-------

While these components are internal, they can be extended or overridden when customizing  
ImportSpy’s validation strategy for highly specific use cases (e.g., custom deployment platforms,  
corporate runtime wrappers, or secure import enforcement).

For more on customizing validation behavior, see:

- :doc:`../architecture/architecture_design_decisions`
- :doc:`api_validators`
