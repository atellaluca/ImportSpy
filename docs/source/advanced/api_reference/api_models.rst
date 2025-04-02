Model Layer: SpyModel & Contract Validation System
==================================================

At the heart of ImportSpy’s compliance framework lies the `SpyModel`:  
a fully structured representation of how a Python module **should behave** across different runtime environments.

ImportSpy does not merely analyze code — it validates whether a module conforms to a **contractual definition**  
that includes its **structure**, **runtime expectations**, and **execution constraints**.

🔍 Whether you’re operating in **embedded mode** or running validations via the **CLI**,  
`SpyModel` is the foundation on which all validation logic is built.

Validation Modes Supported 🧭
-----------------------------

Import contracts defined via `.yml` files (or SpyModel objects in code) are evaluated in:

- **Embedded Mode** 🔌  
  Modules protect themselves by invoking `Spy().importspy()` and enforcing contracts on their importers.

- **External (CLI) Mode** 🛠️  
  Used in pipelines or audits to validate a target module before execution or integration.

Both workflows rely on **SpyModel-based comparison** between expected and actual module states.

SpyModel Class 🏗️
-------------------

The `SpyModel` is a high-level, Pydantic-based model that transforms an import contract into a validated runtime object.

It defines:

- 🧱 Structural rules → Expected classes, attributes, methods, return types  
- 🧪 Runtime rules → Supported OS, CPU architectures, Python interpreters  
- 🔐 Environment rules → Required environment variables and submodule dependencies

.. autoclass:: importspy.models.SpyModel
   :members:
   :undoc-members:
   :show-inheritance:

Model Subcomponents 📦
^^^^^^^^^^^^^^^^^^^^^^^^

`SpyModel` is composed of granular submodels that represent the contract’s declarative schema:

- `Function` → Represents function name, arguments, and return annotations  
- `Attribute` → Captures class or global variables (with value, type, and scope)  
- `Class` → Groups attributes and methods, along with expected inheritance  
- `Module` → Represents nested modules inside deployments  
- `Python`, `System`, `Deployment` → Define runtime matrix for cross-platform validation

.. autoclass:: importspy.models.Function
   :members:
   :undoc-members:

.. autoclass:: importspy.models.Attribute
   :members:
   :undoc-members:

.. autoclass:: importspy.models.Argument
   :members:
   :undoc-members:

.. autoclass:: importspy.models.Class
   :members:
   :undoc-members:

.. autoclass:: importspy.models.Module
   :members:
   :undoc-members:

.. autoclass:: importspy.models.Python
   :members:
   :undoc-members:

.. autoclass:: importspy.models.System
   :members:
   :undoc-members:
  
.. autoclass:: importspy.models.Runtime
   :members:
   :undoc-members:

Validator Interface ✅
----------------------

ImportSpy includes a pluggable validator system that compares:

- The `SpyModel` contract (expected)
- The actual runtime snapshot of the importing environment

Validators are executed as part of a pipeline that checks:

- ✔️ Function and method presence  
- ✔️ Signature alignment and argument types  
- ✔️ Class structure and attribute correctness  
- ✔️ Deployment compatibility and environment config  
- ✔️ Interpreter and version compliance  

To explore how validators are defined and chained:

.. toctree::
   :maxdepth: 1

   api_validators
