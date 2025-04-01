Welcome to ImportSpy's Documentation
=====================================

ImportSpy is a Python validation framework designed to ensure that external modules  
comply with strict structural, contextual, and runtime requirements before execution.

It supports two complementary validation modes:

- **Embedded Validation** – where a module (typically a plugin) validates the environment that imports it.
- **External (CLI) Validation** – where validation occurs externally via CLI, often as part of CI/CD workflows,  
  using declarative contracts written in YAML.

This flexibility allows ImportSpy to adapt to both **runtime validation** and **static validation** during development or deployment.

What Problem Does ImportSpy Solve?
----------------------------------

Python’s flexibility comes at the cost of predictability. Without structural enforcement, modules can:

- Change APIs unexpectedly.
- Misbehave in different Python runtimes or platforms.
- Lack required functions, attributes, or environment variables.
- Fail silently or crash due to misaligned expectations.

ImportSpy addresses this by introducing **import-time validation** using structured contracts, ensuring:

- **Consistency across environments**
- **Prevention of unintended changes**
- **Safe extension of plugin-based systems**
- **Validation of runtime assumptions before execution**

What Are Import Contracts?
--------------------------

Import contracts are **YAML-based declarations** that describe the expected structure and execution environment of a Python module.

They define:

- Expected **functions**, **classes**, and **attributes**
- Required **environment variables** and **runtime interpreters**
- Compatible **operating systems** and **CPU architectures**
- Module-level metadata (like `version` or `variables`)

Import contracts are parsed into `SpyModel` objects at runtime, enabling validation of:

- A module’s structure
- The importing environment’s compatibility
- Cross-platform and interpreter-level constraints

These contracts act as **executable specifications** for module behavior, and serve as documentation, tests, and enforcement logic simultaneously.

Validation Modes
----------------

.. list-table::
   :widths: 25 75
   :header-rows: 1

   * - Mode
     - Description
   * - Embedded Validation
     - The module imports `importspy` and triggers a validation of **the importing environment**.  
       This is ideal for **plugins and extensions**, ensuring they are only loaded in secure and validated contexts.
   * - External (CLI) Validation
     - Run via the CLI using `importspy -s contract.yml module.py`, typically within CI/CD.  
       This decouples validation from runtime execution, ensuring correctness **before deployment**.

This dual-mode approach supports **defensive plugin design** and **pre-deployment contract enforcement**.

What You'll Find in the Documentation
-------------------------------------

- ✅ **Quickstart examples** and setup instructions
- ⚙️ **Details on contract structure** and schema hierarchy
- 📦 **Concepts and glossary** to master ImportSpy’s model
- 🔐 **Security insights** for safe dependency handling
- 🔍 **Comparison of embedded vs. external validation**
- 🔁 **CI/CD integrations** for full pipeline coverage

Installation
------------

Install via pip:

.. code-block:: bash

   pip install importspy

Then follow the guides in:

- :doc:`../../get_started/installation`
- :doc:`../../get_started/example_overview`

Conclusion
----------

ImportSpy brings **discipline to Python imports** — no more runtime surprises, no more fragile dependencies.

By defining import contracts and validating structure and context, ImportSpy empowers developers to:

- **Ship modular code with confidence**
- **Catch violations before runtime**
- **Secure their applications against misuse or regression**

Let ImportSpy be your guardrail in dynamic Python environments.
