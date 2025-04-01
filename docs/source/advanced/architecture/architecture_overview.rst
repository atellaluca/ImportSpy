ImportSpy Architecture
======================

ImportSpy is a **runtime validation framework** that enforces **execution constraints** on the environment where a module is imported.  
Unlike traditional validation systems, ImportSpy allows a **module to define an import contract** that explicitly declares the  
conditions required by any importing environment—blocking non-compliant usage at runtime.

This section provides a **comprehensive introduction** to ImportSpy’s architecture, exploring its **core components**,  
**execution model**, and the mechanisms it uses to guarantee **safe, predictable, and secure imports**.

Architectural Philosophy & Objectives 📌
----------------------------------------

ImportSpy’s design is driven by four fundamental principles:

1. **Environment-Centric Validation**  
   Validation targets the **importing environment**, not the imported module itself.

2. **Dynamic Runtime Enforcement**  
   All checks occur **at runtime**, leveraging Python’s introspection capabilities.

3. **Zero-Trust Security Model**  
   If the environment does not meet contract conditions, execution is **blocked** by default.

4. **Declarative Import Contracts**  
   Modules can define YAML-based import contracts that **codify their expectations**.

This architectural approach allows ImportSpy to protect sensitive modules from being used in unintended contexts  
—ensuring that execution is **predictable, compliant, and reproducible**.

Architectural Layers Overview 📊
--------------------------------

ImportSpy is structured into several layers, each with a distinct responsibility:

- 🏗️ **Context Extraction Layer**  
  Gathers system details: OS, architecture, environment variables, interpreter, Python version, etc.

- ⚡ **Import Interception Layer**  
  Hooks into Python’s import system and determines **who is importing the protected module**.

- 🔍 **Runtime Analysis & SpyModel Construction**  
  Dynamically builds a `SpyModel` from the importing module's context to compare against declared expectations.

- 🛡️ **Validator Pipeline**  
  A modular stack of validators that **checks system, runtime, environment, and structural integrity**.

- ❌ **Enforcement Layer**  
  Raises errors and halts execution if **any constraint fails**—in accordance with the contract.

- ✅ **Pass-through Layer**  
  If validation succeeds, the import is allowed to proceed **transparently**.

Visual Overview
^^^^^^^^^^^^^^^

.. image:: https://raw.githubusercontent.com/atellaluca/ImportSpy/refs/heads/main/assets/importspy-embedded-mode.png
   :align: center
   :alt: ImportSpy Architecture Diagram

How Runtime Enforcement Works 🧠
------------------------------------

ImportSpy performs the following steps when a module protected by an import contract is imported:

1. **Intercept Import Call**  
   ImportSpy inspects the call stack and identifies the **importing module**.

2. **Extract Execution Context**  
   It collects OS, interpreter type, Python version, environment variables, and installed modules.

3. **Build Runtime SpyModel**  
   A `SpyModel` object is generated based on the execution context of the **importing code**.

4. **Compare Against Contract**  
   The runtime model is compared with the declared contract (defined via YAML or Python object).

5. **Enforce Rules**  
   - If compliant → import proceeds normally.  
   - If non-compliant → a `ValueError` is raised, and execution halts immediately.

Strict Validation Flow 🧱
-------------------------

ImportSpy’s runtime architecture is designed to support:

- **Cross-platform compatibility enforcement**  
- **Zero-tolerance validation policies for high-security environments**  
- **Dynamic enforcement across CI/CD, container runtimes, or plugin architectures**

This guarantees **structural consistency and environmental compatibility** without modifying existing application logic.

Why This Architecture Matters 🚀
------------------------------------

ImportSpy’s layered architecture is critical for enforcing:

- ✅ **Predictable execution** across multiple systems and runtime configurations  
- 🔐 **Security boundaries** between sensitive code and unverified third-party dependencies  
- 📦 **Contract-driven integration** for plugins, extensions, and modular frameworks  
- 🔄 **CI/CD compliance enforcement**, ensuring environment correctness at every pipeline stage  

Next Steps 🔬
-------------

Explore ImportSpy's internals in more detail:

- :doc:`architecture_runtime_analysis` → Deep dive into the context extraction layer.  
- :doc:`architecture_design_decisions` → Understand the motivations behind the architectural choices.  
