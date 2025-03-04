.. image:: https://static.pepy.tech/badge/importspy
   :target: https://pepy.tech/project/importspy

.. image:: https://img.shields.io/github/actions/workflow/status/atellaluca/ImportSpy/python-package.yml?style=flat-square
   :target: https://github.com/atellaluca/ImportSpy/actions/workflows/python-package.yml

.. image:: https://img.shields.io/github/license/atellaluca/ImportSpy?style=flat-square
   :target: https://github.com/atellaluca/ImportSpy/blob/main/LICENSE

ImportSpy
=========

.. image:: https://raw.githubusercontent.com/atellaluca/ImportSpy/refs/heads/main/assets/ImportSpy.png
   :width: 830
   :alt: ImportSpy Image

A **powerful runtime validation framework** ensuring that your Python modules  
are imported **only in compliant execution environments**.

🔍 **Prevent unexpected failures**  
🛡️ **Enforce execution policies dynamically**  
⚙️ **Guarantee stability across environments**  

Overview 🌍
===========

ImportSpy is a **runtime validation framework** that **enforces execution constraints**  
on modules by ensuring they are imported **only in predefined, structured environments**.  

Unlike static analysis tools, ImportSpy **actively validates runtime conditions**,  
making it an essential tool for projects requiring:

- **Execution environment validation** → Ensuring modules run in supported OS, Python versions, and system configurations.  
- **Strict compliance enforcement** → Blocking imports in misconfigured environments to prevent unpredictable failures.  
- **Runtime introspection** → Extracting metadata dynamically for debugging and validation.  

For a complete introduction to ImportSpy, visit the documentation:  
`ImportSpy Docs <https://importspy.readthedocs.io>`_

Why Use ImportSpy? 🚀
=====================

ImportSpy is built to **solve real-world challenges** in **modular, microservices, and plugin-based architectures**,  
where external dependencies **must comply with execution constraints**.

Key Benefits:
-------------
- **Ensures Runtime Compliance**  
  - Verifies Python version, OS compatibility, and required system configurations.
- **Prevents Unsafe Execution**  
  - Blocks imports in non-compliant environments, reducing debugging overhead.
- **Provides Detailed Validation Reports**  
  - Offers clear, structured error messages when validation fails.
- **Highly Configurable with SpyModel**  
  - Define granular execution rules that adapt to your project’s needs.

More on ImportSpy’s validation system:  
`Understanding ImportSpy <https://importspy.readthedocs.io/en/latest/understanding_importspy_index.html>`_

How It Works ⚙️
===============

ImportSpy operates **at the moment of import**, intercepting execution requests  
to validate **whether the importing module meets declared constraints**.

1. **Define Execution Constraints** → The developer specifies **SpyModel rules**.  
2. **Intercept Import Operations** → ImportSpy **captures metadata** at runtime.  
3. **Validate Execution Context** → Checks **Python version, OS, dependencies, and system variables**.  
4. **Block or Approve Execution** → If the environment is invalid, **ImportSpy prevents import execution**.  

Learn more:  
`Spy Execution Flow <https://importspy.readthedocs.io/en/latest/spy_execution_flow.html>`_

Example: Ensuring Execution Compliance 📜
=========================================

A developer wants to **restrict execution** of their module to:
- **Python 3.10+**
- **Linux OS**
- **x86_64 architecture**
- **A required environment variable (`APP_SECRET_KEY`)**

Using **ImportSpy’s SpyModel**, the developer enforces these rules:

.. code-block:: python

    from importspy.models import SpyModel, Deployment, Runtime, System, Python
    from importspy.constants import Config

    class MyModuleSpy(SpyModel):
        deployments = [
            Deployment(
                runtimes=[
                    Runtime(
                        arch=Config.ARCH_X86_64,
                        systems=[
                            System(
                                os=Config.OS_LINUX,
                                pythons=[
                                    Python(
                                        version="3.10",
                                        interpreter=Config.INTERPRETER_CPYTHON,
                                        modules=[]
                                    )
                                ],
                                envs={"APP_SECRET_KEY": None}
                            )
                        ]
                    )
                ]
            )
        ]

When an external module imports **MyModule**, ImportSpy **verifies execution context**:
- ✅ If it matches the SpyModel, execution proceeds.  
- ❌ If Python version is incorrect, OS is unsupported, or a required variable is missing, **ImportSpy blocks execution**.

More real-world use cases:  
`Use Cases Index <https://importspy.readthedocs.io/en/latest/use_cases_index.html>`_

Installation 📦
===============

ImportSpy is available on PyPI:

.. code-block:: bash

    pip install importspy

Getting started guide:  
`Installation Guide <https://importspy.readthedocs.io/en/latest/get_started/installation.html>`_

Get Involved 🛠️
================

**ImportSpy is open-source** and your contributions make it better!  

Ways to contribute:
-------------------
- **Report issues & suggest features** on GitHub.  
- **Submit pull requests** to improve ImportSpy.  
- **Enhance the documentation** for new users.  

Contribute:  
`GitHub Repository <https://github.com/atellaluca/ImportSpy>`_

License 📜
==========

ImportSpy is released under the **MIT License**.

`Read the full license <https://github.com/atellaluca/ImportSpy/blob/main/LICENSE>`_

Sponsorship ❤️
===============

Support ImportSpy’s Development!
--------------------------------

ImportSpy is a **community-driven project** dedicated to improving  
module validation and execution security in Python.

Ways to support:
----------------
- **Sponsor the project on GitHub Sponsors**  
- **Share ImportSpy with your network**  
- **Give a ⭐️ on GitHub to show your support!**

`Sponsor ImportSpy <https://github.com/sponsors/atellaluca>`_  
`GitHub Repository <https://github.com/atellaluca/ImportSpy>`_

For full documentation, visit:  
`ImportSpy Docs <https://importspy.readthedocs.io>`_
