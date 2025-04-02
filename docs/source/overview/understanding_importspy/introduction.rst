Introduction to ImportSpy
==========================

Welcome to the core introduction to **ImportSpy** —  
a validation and compliance framework that transforms Python's dynamic import system into a structured, predictable process.

ImportSpy enables developers to define **executable contracts** that external modules must follow.  
These contracts describe not only a module's expected structure, but also its **execution environment**, including:

- Python version  
- Interpreter type (e.g., CPython, PyPy, IronPython)  
- Operating system  
- Required classes, functions, variables  
- Environment variables and metadata

If the contract is not respected — the module doesn’t load.  
It’s as simple and powerful as that.

What Problem Does ImportSpy Solve? 🚧
-------------------------------------

Python is known for flexibility — but that comes at a cost:

- Modules can silently drift from expected interfaces  
- Plugin systems can misbehave if assumptions aren’t validated  
- Deployment environments may differ in subtle, breaking ways  
- Runtime errors often appear too late, and debugging them is slow and painful

ImportSpy introduces **import-time validation**, enforcing that:

✅ A module’s structure is as expected  
✅ Its runtime context matches predefined constraints  
✅ Violations are caught **before execution** begins

The result? Safer systems, clearer boundaries, and predictable integrations.

What Are Import Contracts? 📜
------------------------------

Import contracts are YAML-based documents that define the rules a module must follow to be considered valid.

They declare:

- Required classes, methods, and attributes  
- Module-level variables and metadata  
- Expected Python interpreter, version, OS, and CPU architecture  
- Environmental assumptions (e.g., required env vars)  

At runtime, ImportSpy parses these contracts and validates them **against the actual module and environment**.  
These contracts serve as:

- 🔍 Executable specifications  
- 📖 Documentation for expected interfaces  
- 🛡️ Runtime validation logic  

The result is a **formal, testable boundary** between modules — especially in dynamic systems like plugin frameworks.

Validation Modes Supported 🔁
------------------------------

ImportSpy supports two complementary modes of validation:

.. list-table::
   :widths: 25 75
   :header-rows: 1

   * - Mode
     - Description
   * - Embedded Mode
     - The core module validates the structure of the **importer**.  
       Useful in plugin architectures where the base module ensures it is being imported in a safe, compliant context.
   * - CLI Mode
     - Validation is performed externally via the command line.  
       Ideal for pipelines, static checks, and CI/CD integration.

This flexibility allows ImportSpy to adapt to **runtime and pre-deployment validation scenarios** with equal precision.

What You’ll Learn in This Documentation 📘
------------------------------------------

This documentation will guide you through:

- 🚀 How ImportSpy works and why it matters  
- 🛠️ How to define and apply import contracts  
- 🔄 How validation is triggered in both modes  
- 🧪 Real-world examples with plugins and pipelines  
- ⚙️ Best practices for integration in production systems  
- 🔐 Security benefits and enforcement patterns  
- 💼 How to use ImportSpy in automated CI/CD workflows

Installing ImportSpy
----------------------

To get started, install ImportSpy using pip:

.. code-block:: bash

   pip install importspy

Then visit:

- :doc:`../../get_started/installation` to set up your environment  
- :doc:`../../get_started/example_overview` to run your first validated example

Let’s Get Started 🚀
---------------------

ImportSpy turns Python’s imports into a **secure contract** — not just a hope for compatibility.

By shifting validation **before execution**, it empowers developers to build modular, extensible, and production-safe Python systems.

Ready to unlock the next level of confidence in your code?  
Start by defining your first import contract and let ImportSpy take care of the rest.
