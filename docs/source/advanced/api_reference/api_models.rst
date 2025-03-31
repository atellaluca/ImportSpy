Models & Contracts
==================

ImportSpy structures its validation and compliance process through a unified concept called the **Import Contract**.

An **Import Contract** is a declarative specification (typically written in YAML) that describes the **expected structure, behavior, and runtime constraints** of a Python module.  
This contract is loaded and interpreted by the internal model class: `SpyModel`.

Supported Validation Modes 🧭
-----------------------------

Import Contracts are used consistently across **both validation modes** offered by ImportSpy:

- 🔌 **Embedded Validation** – ImportSpy is embedded inside the imported module.  
  The contract is enforced *by the module being imported*, inspecting its caller at runtime.
  
- 🛠️ **CLI/Pipeline Validation** – ImportSpy is run as an **external CLI tool** or as part of a **CI/CD pipeline**,  
  validating a module against a contract before it is deployed or integrated.

Regardless of the mode, the validation process is powered by the same internal logic and model structures.

SpyModel 🏗️
------------

The `SpyModel` class is the **core abstraction** that defines the **expected structure and execution constraints**  
for modules being validated.

It transforms a YAML Import Contract into a structured, queryable Python object and enables runtime comparison  
between **what is declared** and **what is actually present** in the target module.

Key Responsibilities:
^^^^^^^^^^^^^^^^^^^^^^

- Captures **module structure**:
  - Classes, functions, attributes, annotations
- Defines **runtime and environmental constraints**:
  - Supported OS, architecture, Python version, interpreter
- Enables **cross-environment consistency checks**
- Validates **import-time metadata** (e.g., variables, file names, version)

.. autoclass:: importspy.models.SpyModel
   :members:
   :undoc-members:
   :show-inheritance:

Validators ✅
------------

ImportSpy includes a **modular validation system** that enforces compliance  
between a module and its declared `SpyModel`.

Each validator focuses on a specific layer:

- **Runtime validation** → OS, Python version, hardware
- **Structural validation** → Classes, methods, variables, annotations
- **System & environment validation** → Dependencies, variables, environment setup

For a complete breakdown of validators, see:

.. toctree::
   :maxdepth: 1

   api_validators
