Welcome to ImportSpy's Documentation
=====================================

ImportSpy is a Python validation framework designed to ensure that external modules  
comply with strict structural, contextual, and runtime requirements before execution.

It supports two distinct validation modes:

- **Embedded validation** – where a module (e.g. a plugin) is validated by the code it imports.
- **CLI / Pipeline validation** – where validation is executed externally, such as in CI/CD workflows,  
  using declarative contracts written in human-readable YAML.

This flexibility allows ImportSpy to adapt to both **plugin-based architectures** and **automated pipelines**.

What Problem Does ImportSpy Solve? ⚠️
--------------------------------------

Python’s modularity and dynamic nature offer tremendous flexibility.  
But with that comes fragility: third-party modules can evolve, break expectations, or misbehave silently.

Common risks include:

- APIs that change without warning
- Modules that behave differently across environments
- Missing functions or misaligned class structures
- Runtime crashes caused by unvalidated imports

ImportSpy proactively mitigates these issues by **enforcing contracts** before a module is ever used.

What Are Import Contracts? 📄
------------------------------

Import contracts are **external YAML files** that define what a module is expected to look like:  
its classes, functions, attributes, variables, and even runtime constraints such as OS or Python version.

Rather than writing Python code to validate Python code, contracts give you a **declarative, testable interface**  
that can be embedded in projects or reused across pipelines.

Validation Modes 🔍
--------------------

ImportSpy offers two complementary ways to enforce these contracts:

.. list-table::
   :widths: 25 75
   :header-rows: 1

   * - Validation Mode
     - Description
   * - Embedded Validation
     - The module under validation **imports a core package**, which runs ImportSpy to inspect and validate the caller.  
       This approach is ideal for plugin-based systems or modular architectures where each extension must prove it’s valid before interacting.
   * - CLI / Pipeline Validation
     - The module is validated **externally via CLI**, typically as part of a **CI/CD pipeline**, a manual review process,  
       or a pre-deployment hook. This method is fully decoupled and perfect for static inspection and continuous integration.

What This Documentation Offers 📚
----------------------------------

- 🚀 **Quickstart guides** to get you up and running
- 📖 **Conceptual breakdowns** of how ImportSpy works internally
- 🧱 **Examples and real-world use cases**
- ⚙️ **Integration tips** for pipelines and distributed systems
- ✅ **Security insights** for managing third-party code safely
- 🧪 **Explore examples** using both validation approaches

Get Started 🛠️
---------------

To start validating your modules with ImportSpy:

.. code-block:: bash

   pip install importspy

Then explore the :doc:`get_started/installation` guide  
or jump straight into :doc:`examples/examples_overview` to see it in action.

Conclusion 🔚
-------------

ImportSpy brings structure, safety, and clarity to Python's modular world.  
Whether you're validating plugins at runtime or checking code during CI,  
it empowers developers to **ship confidently, validate automatically, and control external complexity**.

Let ImportSpy be your safeguard against the chaos of unchecked imports.
