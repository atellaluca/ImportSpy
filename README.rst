.. image:: https://img.shields.io/pypi/v/importspy
   :target: https://pypi.org/project/importspy/
.. image:: https://img.shields.io/pypi/dm/importspy
.. image:: https://img.shields.io/pypi/pyversions/importspy
.. image:: https://img.shields.io/github/actions/workflow/status/atellaluca/ImportSpy/python-package.yml?style=flat-square
   :target: https://github.com/atellaluca/ImportSpy/actions/workflows/python-package.yml
.. image:: https://img.shields.io/readthedocs/importspy?style=flat-square
   :target: https://importspy.readthedocs.io/
   :alt: Documentation Status
.. image:: https://img.shields.io/github/license/atellaluca/importspy

ImportSpy
=========

Validate and enforce structural compliance in Python modules through YAML-defined import contracts.

ImportSpy is a developer-first tool to **monitor, validate, and control Python module structure** at runtime or during CI/CD using declarative YAML contracts.

It enables robust module validation through two powerful modes:

- **Embedded Mode** – for package-level introspective validation at runtime.
- **External Mode** – for standalone CLI-based validation in CI/CD workflows.

.. image:: https://raw.githubusercontent.com/atellaluca/ImportSpy/refs/heads/main/assets/importspy-works.png
   :width: 830
   :alt: How ImportSpy Works

🚀 Why ImportSpy?
-----------------

Modern software development thrives on **modularity**, enabling seamless integration of external components. However, this flexibility introduces **critical compliance, security, and consistency risks**.

ImportSpy addresses this challenge by enforcing a **declarative contract-driven structure** to Python modules:

- ✅ Prevents unexpected failures caused by incorrect dependencies.
- ✅ Ensures security by blocking unauthorized imports.
- ✅ Eliminates debugging headaches by validating environments dynamically.
- ✅ Gives you full control over how and where your code is used.

.. note::

   "ImportSpy is not just a tool; it's a movement toward secure, auditable Python codebases."

🔴 Without vs 🟢 With ImportSpy
-------------------------------

.. list-table:: Comparison of Using and Not Using ImportSpy
   :header-rows: 1
   :widths: 20 40 40

   * - Aspect
     - 🔴 Without ImportSpy
     - 🟢 With ImportSpy
   * - Compatibility
     - Modules may break in wrong Python versions or OS setups
     - Blocks execution in non-compliant environments
   * - Debugging
     - Failures can be silent and hard to trace
     - Errors are caught early with clear validation messages
   * - Security
     - No protection against unauthorized or unsafe imports
     - Enforces structural integrity and import ownership
   * - Consistency
     - Behavior varies between environments
     - Predictable behavior through enforced import contracts

🧪 Example: A Contract in Action
--------------------------------

.. code-block:: yaml

    filename: extension.py
    variables:
      engine: docker
      plugin_name: plugin name
      plugin_description: plugin description
    classes:
      - name: Extension
        attributes:
          - type: instance
            name: extension_instance_name
            value: extension_instance_value
          - type: class
            name: extension_name
            value: extension_value
        methods:
          - name: __init__
            arguments:
              - name: self
          - name: add_extension
            arguments:
              - name: self
              - name: msg
                annotation: str
            return_annotation: str
          - name: remove_extension
            arguments:
              - name: self
          - name: http_get_request
            arguments:
              - name: self
        superclasses:
          - Plugin

🧠 Embedded Mode (Runtime)
--------------------------

.. code-block:: python

    from importspy import Spy
    import logging

    caller_module = Spy().importspy(
        filepath="./contracts.yml",
        log_level=logging.DEBUG
    )

    caller_module.Foo().get_bar()

- If validation passes: the importer module is returned.
- If validation fails: a detailed exception is raised.

🔧 External Mode (CLI for CI/CD)
--------------------------------

.. code-block:: bash

    importspy -s contracts.yml -l DEBUG my_module.py

**CLI Options**::

    Usage: importspy [OPTIONS] [MODULEPATH]

    Options:
      -s, --spymodel TEXT   Path to the import contract file (.yml).
      -l, --log-level TEXT  Log level (DEBUG, INFO, WARNING, ERROR).
      -v, --version         Show version and exit.
      --help                Show help and exit.

👤 Who Should Use ImportSpy?
----------------------------

- 🔹 **Enterprise teams** that need strict environment control
- 🔹 **Plugin-based architectures** and modular systems
- 🔹 **Security-focused projects** that want to restrict runtime execution contexts
- 🔹 **Python package maintainers** who need to validate runtime constraints for users

.. tip::

   If your project relies on external modules, ImportSpy is your safeguard against execution chaos. 🔥

📦 Installation
---------------

.. code-block:: bash

    pip install importspy

Or, if using Poetry:

.. code-block:: bash

    poetry add importspy

📚 Key Concepts
---------------

- **Import Contracts**: YAML files describing structural expectations
- **Validation Engine**: core component that compares module against contract
- **Spy Execution Flow**: logic that determines how and when validation occurs
- **Error Handling**: developer-friendly error messages
- **Modes**: Embedded (runtime) and External (CLI)

⚙ Requirements
--------------

- Python 3.10+
- Uses: Pydantic, Typer, ruamel.yaml
- Dev tools: Poetry, Sphinx, Pytest

📦 Architecture Highlights
--------------------------

- **Runtime validation engine**
- **YAML contract parser**
- **Python reflection for deep inspection**
- **CI/CD-friendly CLI**

🔐 Use Cases
------------

- ✅ Validation at scale across plugin ecosystems
- 🔒 Security through strict import contexts
- 📑 Enforce regulatory or organizational compliance
- 🧠 IoT and modular embedded systems

🤝 Contributing & Sponsorship
-----------------------------

ImportSpy is built to improve the **resilience, auditability, and safety** of Python codebases.

- 🛠 Developers: Build validators or tooling
- 🏢 Companies: Enforce contracts at scale
- 💡 CI engineers: Automate structural compliance

💖 Support the Project
----------------------

Your sponsorship helps us:

- Expand validation features
- Improve docs and tutorials
- Develop IDE extensions

👉 https://github.com/sponsors/atellaluca

📚 Learn More
-------------

- `Installation <https://importspy.readthedocs.io/en/latest/get_started/installation.html>`__
- `Contract Design <https://importspy.readthedocs.io/en/latest/overview/understanding_importspy/defining_import_contracts.html>`__
- `Architecture <https://importspy.readthedocs.io/en/latest/advanced/architecture_index.html>`__

📦 Project Status
-----------------

Launched in **October 2024**, ImportSpy is actively maintained and ready for production use.

🔥 Take control of your imports. Start using ImportSpy today! 🚀
