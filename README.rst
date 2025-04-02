.. image:: https://img.shields.io/pypi/v/importspy
   :target: https://pypi.org/project/importspy/
.. image:: https://img.shields.io/pypi/dm/importspy
.. image:: https://img.shields.io/pypi/pyversions/importspy
.. image:: https://img.shields.io/github/actions/workflow/status/atellaluca/ImportSpy/python-package.yml?style=flat-square
   :target: https://github.com/atellaluca/ImportSpy/actions/workflows/python-package.yml
.. image:: https://img.shields.io/readthedocs/importspy?style=flat-square
   :target: https://importspy.readthedocs.io/
.. image:: https://img.shields.io/github/license/atellaluca/importspy

ImportSpy
=========

Contract-based import validation for Python modules.

ImportSpy is a runtime enforcement engine that protects Python modules from being imported or executed in unauthorized, unverified, or structurally incompatible environments — using declarative **import contracts** defined in YAML.

🧠 **ImportSpy** ensures:  

   ✅ Your code is only imported in **verified contexts**  

   ✅ Module structure matches declared expectations  

   ✅ Runtime conditions (OS, Python version, architecture) are enforced  

   ✅ Environments behave predictably across CI, staging, and production  


.. image:: https://raw.githubusercontent.com/atellaluca/ImportSpy/refs/heads/main/assets/importspy-works.png
   :width: 830
   :alt: How ImportSpy Works

💡 Why ImportSpy?
-----------------

Python's flexibility is powerful — but risky.

Without guardrails, imports can break due to:

- 🚫 Missing or malformed classes/functions
- 🚫 Undeclared changes in shared dependencies
- 🚫 Execution in unsupported OS/Python environments
- 🚫 Unauthorized use of internal packages

ImportSpy gives you **import boundaries** and **runtime control** using **YAML-defined contracts**.

Two powerful usage modes:

- 🔒 **Embedded Mode** – Self-protective modules that validate their own importers.
- 🧪 **External CLI Mode** – Contract validation via `importspy` during builds or CI/CD pipelines.

Comparison Table
----------------

.. list-table::
   :widths: 20 40 40
   :header-rows: 1

   * - Aspect
     - Without ImportSpy
     - With ImportSpy
   * - Compatibility
     - Modules can run in unsupported runtimes
     - Imports blocked in mismatched OS/Python contexts
   * - Debugging
     - Silent runtime errors and broken contracts
     - Clear errors with structured validation output
   * - Security
     - Unverified third-party modules can access internals
     - Controlled import surface and enforced structure
   * - Reproducibility
     - Behavior varies across environments
     - Predictable imports under contract governance

📜 What’s a Contract?
---------------------

A **contract** is a YAML file that defines the expected structure and runtime constraints of your module.

Example:

.. code-block:: yaml

   filename: extension.py
   variables:
     engine: docker
   classes:
     - name: Extension
       attributes:
         - type: class
           name: extension_name
           value: extension_value
       methods:
         - name: add_extension
           arguments:
             - name: self
             - name: msg
               annotation: str
           return_annotation: str
       superclasses:
         - Plugin

This defines a structural + runtime boundary for where your module is allowed to run — and how.

⚙️ Embedded Mode
----------------

Validate importer modules from inside your code.

.. code-block:: python

   from importspy import Spy
   import logging

   importer = Spy().importspy(filepath="spymodel.yml", log_level=logging.DEBUG)
   importer.Foo().run()

🔧 CLI Mode (External)
----------------------

Validate a module against its contract from CI, terminal, or script.

.. code-block:: bash

   importspy -s spymodel.yml -l DEBUG path/to/module.py

📦 Installation
---------------

.. code-block:: bash

   pip install importspy

Supported Python: 3.10+

📚 Features at a Glance
-----------------------

- ✅ YAML-based declarative import contracts  
- ✅ OS + interpreter + architecture validation  
- ✅ Class/function/argument/attribute enforcement  
- ✅ Embedded or CLI-driven validation modes  
- ✅ Full error trace and CI/CD logging support  
- ✅ SpyModel-powered introspection pipeline  

📎 Ideal For:
-------------

- 🔐 Security-driven systems (banking, medical, gov)
- 🧩 Plugin frameworks (CMS, IoT, CLI extensions)
- 🔬 Large codebases needing structural validation
- 🧪 CI/CD workflows enforcing compatibility and compliance
- 📦 Maintainers distributing validated packages

🔍 How It Works
---------------

1. Your module defines a contract (YAML or Python).
2. ImportSpy is triggered at runtime or CLI.
3. The environment and structure of the importer are introspected.
4. Validation checks everything against the contract.
5. If the contract fails: import is blocked.  
   If it passes: import proceeds safely.

🔧 Example CLI Usage

.. code-block:: bash

   importspy -s spymodel.yml -l ERROR plugin.py

🎯 Tech Stack
-------------

- ✅ Pydantic v2 → validation engine  
- ✅ Typer → CLI interface  
- ✅ ruamel.yaml → YAML parsing  
- ✅ inspect + platform + sys → runtime reflection  
- ✅ Poetry → package management  
- ✅ Sphinx + ReadTheDocs → full docs coverage

📚 Docs
-------

- 📘 Full Documentation → https://importspy.readthedocs.io/  
- 🧱 Architecture Overview → https://importspy.readthedocs.io/en/latest/advanced/architecture_index.html  
- 🧪 Examples & Use Cases → https://importspy.readthedocs.io/en/latest/overview/use_cases_index.html

❤️ Contribute, Share, Support
-----------------------------

- ⭐ Star on GitHub → https://github.com/atellaluca/ImportSpy  
- 🛠 Contribute: PRs, Issues, Docs welcome  
- 💖 Sponsor → https://github.com/sponsors/atellaluca  

📜 License
----------

MIT © 2024 — Luca Atella

🔥 Take control of your imports. Validate with ImportSpy.
