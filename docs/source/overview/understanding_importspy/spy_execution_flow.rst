Spy Execution Flow
===================

At the heart of ImportSpy lies a powerful validation engine that activates the moment an import occurs.

Whether you're using **embedded mode** or **CLI validation**, ImportSpy reconstructs a full picture of the runtime environment, compares it to your declared import contract, and enforces compliance **before execution begins**.

This page explains, step by step, how ImportSpy processes a validation request — from **introspection to enforcement**.

Overview
--------

ImportSpy enforces a simple but strict rule:

> ❌ If the importing environment does not match the contract, the module is blocked.  
> ✅ If the environment is compliant, execution proceeds normally.

This model brings **predictability and control** to Python's otherwise dynamic import system.

Execution Modes Supported
--------------------------

ImportSpy works in two execution modes:

- :doc:`Embedded Mode <embedded_mode>` → The validated module runs `importspy()` internally to inspect its importer  
- :doc:`External Mode <external_mode>` → Validation is triggered via CLI, often in CI/CD or static validation steps

Execution Pipeline
------------------

Here’s how ImportSpy validates imports, broken down into phases:

1. Detect the Importer
~~~~~~~~~~~~~~~~~~~~~~

ImportSpy uses **stack introspection** to determine which module is importing the validated one.  
This lets it establish a **validation boundary**, isolating the exact caller and its context.

2. Capture Runtime Context
~~~~~~~~~~~~~~~~~~~~~~~~~~

Once the importer is found, ImportSpy collects runtime data:

- Current OS and CPU architecture  
- Python version and interpreter type  
- Available environment variables  
- Installed Python modules and paths

This snapshot is encoded into an internal `SpyModel` object, representing the actual runtime conditions.

3. Parse the Contract
~~~~~~~~~~~~~~~~~~~~~

Next, ImportSpy loads and parses the YAML-based import contract (typically `spymodel.yml`).

This creates a second `SpyModel` representing the **expected structure and execution environment**.

4. Compare & Validate
~~~~~~~~~~~~~~~~~~~~~

ImportSpy performs a deep comparison between the **actual SpyModel** and the **expected SpyModel**.

Validation includes:

- Matching CPU architecture and operating system  
- Checking Python version and interpreter type  
- Verifying required environment variables  
- Matching declared functions, classes, methods, and attributes  
- Validating module variables and custom metadata  
- Checking nested modules and deployment-specific rules

5. Enforce or Reject
~~~~~~~~~~~~~~~~~~~~~

- If the validation **fails**:  
  - ImportSpy raises a `ValueError`  
  - Detailed diagnostics are included in the exception  
  - Execution is halted immediately

- If the validation **passes**:  
  - The validated importer is returned (in embedded mode)  
  - Execution proceeds safely

6. Optimize for Runtime
~~~~~~~~~~~~~~~~~~~~~~~~

To avoid repeated validation during long-running processes or multi-import scenarios, ImportSpy uses **caching** to store validated environments.

This provides fast re-entry for already-validated modules without compromising security.

Security Philosophy
-------------------

ImportSpy follows a **fail-fast and zero-trust model**:

- 🚫 No module runs unless it satisfies all declared constraints  
- ✅ All failures are explicit and traceable  
- 🔐 This prevents silent regressions, broken interfaces, and unpredictable imports

There is **no fallback behavior** — if a violation is detected, it is blocked **by design**.

Best Practices
--------------

- Use :doc:`embedded_mode` to validate who is importing your module  
- Use :doc:`external_mode` to validate a module before deployment  
- Always define structural + runtime constraints in your contract for full coverage

Related Topics
--------------

- :doc:`defining_import_contracts`  
- :doc:`contract_structure`  
- :doc:`error_handling`  
- :doc:`validation_and_compliance`
