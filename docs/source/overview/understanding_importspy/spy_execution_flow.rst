Spy Execution Flow
==================

ImportSpy operates as an **execution validation layer**, ensuring that the environment in which a Python module is imported  
complies with the structural and runtime constraints defined in its associated **import contract**.  

Rather than inspecting the imported module directly, ImportSpy validates whether **the importing environment**  
satisfies the expected execution conditions, as specified by the module author.

.. note::

   ImportSpy supports two execution modes:
   
   - :doc:`Embedded Mode <embedded_mode>`: validation is embedded inside the protected module.
   - :doc:`External Mode <external_mode>`: validation is invoked externally (e.g., via CLI or CI pipeline).

This architecture enables strict enforcement of execution guarantees in both local and distributed systems.

Execution Phases
----------------

The import validation process follows a structured sequence of dynamic runtime operations:

1. **Identifying the Importing Module**

   ImportSpy uses stack introspection to detect which module is attempting to import a protected module.  
   This allows it to establish a *validation boundary* and enforce constraints **at the exact point of interaction**.

2. **Extracting Execution Context**

   Once the importing module is identified, ImportSpy dynamically reconstructs a runtime snapshot, including:

   - Operating system and CPU architecture  
   - Python version and interpreter  
   - Available environment variables  
   - Installed modules and dependencies  

   This snapshot is converted into a `SpyModel` object that represents the current state of the importing environment.

3. **Parsing the Import Contract**

   The protected module defines a set of expected conditions in an external YAML file, known as an **import contract**.  
   ImportSpy parses this contract to produce a target `SpyModel`, defining the **required runtime configuration**.

4. **Validation Checkpoint**

   The dynamically generated `SpyModel` (actual environment) is compared with the parsed import contract (expected environment).  
   The validation includes:

   - Matching architecture, OS, interpreter, and Python version  
   - Checking declared environment variables  
   - Ensuring structural alignment of attributes, functions, and classes  
   - Verifying declared modules and submodules  
   - Matching custom variable names and values

5. **Enforcement**

   If discrepancies are found, ImportSpy:

   - Blocks execution immediately  
   - Raises a `ValueError` with detailed diagnostics  
   - Prevents unsafe or non-compliant usage

   If validation passes, execution proceeds securely and predictably.

6. **Runtime Optimization**

   For performance, ImportSpy uses **runtime caching** of validated environments, avoiding redundant checks in long-running processes.

Security Guarantees
-------------------

ImportSpy follows a **Zero-Trust approach**:

- No execution is allowed unless the import contract is fully respected.
- The contract acts as a **pre-execution firewall**, blocking misconfigured or malicious import attempts.
- This protects against accidental misuse, API drift, and environment inconsistencies.

Contract Enforcement Is Not Optional
------------------------------------

ImportSpy does not offer a fallback or "best-effort" mode.  
Any violation of the import contract results in **enforced termination** of the importing process.

By enforcing constraints before code execution begins, ImportSpy guarantees:

- High-integrity imports  
- Traceable and explainable runtime behavior  
- Fail-fast debugging with actionable logs

.. important::

   Use :doc:`Embedded Mode <embedded_mode>` for internal validation logic  
   or :doc:`External Mode <external_mode>` for decoupled validation pipelines.
