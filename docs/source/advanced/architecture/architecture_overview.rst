Architecture Overview
=====================

ImportSpy is a structural validation engine for Python that operates across two distinct execution models: **embedded mode** and **external (CLI) mode**.  
Its architecture is designed to adapt seamlessly to both, providing a **runtime validation system** that enforces **import contracts**—declarative YAML specifications defining how and where a module is allowed to run.

This section introduces the architectural layers, flows, and principles behind ImportSpy’s execution model.

Architectural Objectives
------------------------

ImportSpy is built upon four core pillars:

1. **Contract-Driven Validation**  
   Modules define import contracts that describe the expected runtime and structural context.

2. **Zero-Trust Execution Model**  
   Code is never executed unless the importing or imported module complies with declared constraints.

3. **Dynamic Runtime Enforcement**  
   System context is reconstructed at runtime using reflection and introspection.

4. **Composable Validation Layers**  
   Validation is performed in discrete phases (structure, environment, runtime, interpreter), making the architecture modular and extensible.

Supported Execution Modes
--------------------------

ImportSpy is dual-mode by design:

🔹 **Embedded Mode** (for modules that protect themselves)

- Validation is triggered **inside** the protected module.
- The module inspects **who is importing it** and verifies the caller’s structure and runtime context.
- Typical use case: plugins that must ensure their importing host complies with an expected contract.

🔹 **External Mode** (for CI/CD or static compliance pipelines)

- Validation is triggered via CLI before execution.
- The target module is validated **from the outside**, ensuring it conforms to its declared contract.
- Typical use case: pipeline validation of Python modules before deployment.

Both modes share the same validation engine and contract semantics but differ in the **direction** of the inspection (who validates whom).

Architectural Layers
--------------------

The architecture of ImportSpy can be decomposed into the following logical layers:

🏗️ **Context Reconstruction Layer**  
   - Gathers system information from the current runtime.
   - Captures OS, Python version, architecture, interpreter, and environment variables.

🔁 **SpyModel Builder**  
   - Builds a structured representation of the runtime or module to validate.
   - Converts contracts and runtime state into Pydantic models.

📦 **Import Contract Loader**  
   - Parses the YAML `.yml` contract into a typed validation model.
   - Supports nested structures, deployment variations, and type annotations.

🔍 **Validation Pipeline**  
   - Compares the reconstructed runtime or module state against the contract.
   - Handles structure (functions, classes), environment (variables), and system (interpreter, OS, arch).

🔐 **Enforcement & Error Handling**  
   - Raises structured exceptions on failure (with detailed error classification).
   - Blocks execution in embedded mode; returns exit codes in CLI mode.

Execution Flow
--------------

📌 Embedded Mode:

1. Module executes `Spy().importspy(...)` at the top of its source.
2. The call stack is inspected to identify the **caller module**.
3. A `SpyModel` of the caller is reconstructed.
4. The module’s own contract is loaded.
5. If the caller matches the contract, execution continues.
6. If not, a `ValidationError` is raised and execution is blocked.

📌 External Mode:

1. CLI is invoked with `importspy -s contract.yml my_module.py`.
2. `my_module.py` is dynamically loaded and introspected.
3. Its structure is extracted: classes, functions, attributes, variables.
4. The YAML contract is parsed into a validation model.
5. Structural and runtime validation is performed.
6. Success → status code 0. Failure → detailed error message and exit code 1.

Illustration:

.. image:: https://raw.githubusercontent.com/atellaluca/ImportSpy/main/assets/importspy-architecture.png
   :align: center
   :alt: ImportSpy Architecture Overview

Why This Architecture Matters
-----------------------------

This architecture provides:

- ✅ Full control over **execution guarantees** of Python modules
- ✅ Runtime enforcement of **environmental and structural policies**
- ✅ Dual-mode support for **plugin protection and CI/CD validation**
- ✅ A uniform validation model across **local, container, and distributed runtimes**

What’s Next?
------------

Continue with:

- :doc:`architecture_runtime_analysis` → How ImportSpy reconstructs runtime environments  
- :doc:`architecture_validation_engine` → The core validation logic and error system  
- :doc:`architecture_design_decisions` → Design trade-offs, limitations, and rationale
