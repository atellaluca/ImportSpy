.. image:: https://static.pepy.tech/badge/importspy
   :target: https://pepy.tech/project/importspy

.. image:: https://img.shields.io/github/actions/workflow/status/atellaluca/ImportSpy/python-package.yml?style=flat-square
   :target: https://github.com/atellaluca/ImportSpy/actions/workflows/python-package.yml

.. image:: https://img.shields.io/github/license/atellaluca/ImportSpy?style=flat-square
   :target: https://github.com/atellaluca/ImportSpy/blob/master/LICENSE

ImportSpy
=========

.. image:: https://raw.githubusercontent.com/atellaluca/ImportSpy/refs/heads/main/assets/ImportSpy.png
   :width: 830
   :alt: ImportSpy Image

Overview 🌀
--------

**ImportSpy** is an innovative Python library that redefines how developers manage module imports and runtime environments. By integrating robust validation through Pydantic models, ImportSpy empowers developers to enforce rules and standards for external modules interacting with their code. This approach ensures consistency, stability, and security across projects.

Key Features
============

🛡️ Proactive Import Validation
---------------------------

ImportSpy provides the capability to enforce strict rules on how modules interact with your code. Developers can define what is required from external modules, such as specific variables, methods, and class structures. This proactive approach ensures that only compliant modules integrate with your system, minimizing runtime errors and improving overall code reliability.

🏗️ Architecture-Aware Validation
-----------------------------

With support for architecture-specific rules via `SpyArchModule`, ImportSpy makes it possible to validate modules against platform constraints like `x86_64` or `ARM`. This feature is especially useful in distributed systems where compatibility between different environments must be ensured.

🌍 Environment Validation
-----------------------

ImportSpy simplifies the process of validating execution environments by verifying the presence and correctness of critical environment variables. This is particularly beneficial for CI/CD pipelines, ensuring consistent configurations across deployment environments.

🔍 Dynamic Module Metadata Extraction
-----------------------------------

ImportSpy can dynamically extract metadata from modules at runtime. This includes functions, variables, and classes. By using `SpyModel`, developers can validate that modules adhere to predefined structures and ensure alignment with expected behaviors.

📊 Debugging and Monitoring
-------------------------

ImportSpy tracks how external modules interact with your code, offering insights into runtime behavior. This feature enables developers to debug more effectively, identify integration issues, and maintain a robust system architecture.

⚙️ Installation
------------

Install ImportSpy using pip:

.. code-block:: bash

    pip install importspy

💡 Advanced Example: Plugin Validation
-----------------------------------

Here is a sophisticated use case leveraging ImportSpy to validate plugin implementations:

.. code-block:: python

    from importspy import Spy
    from importspy.models import SpyModel, ClassModel, SpyArchModule
    from importspy.constants import Constants
    from typing import List, Optional

    class PluginSpy(SpyModel):
        spies: List[SpyArchModule] = [
            SpyArchModule(
                arch=Constants.ARCH_x86_64,
                module=SpyModel(
                    variables={
                        "engine": "docker"
                    }
                )
            )
        ]
        variables: dict = {
            "plugin_name": "plugin name",
            "plugin_description": "plugin description"
        }
        classes: List[ClassModel] = [
            ClassModel(
                name="Extension",
                class_attr=["extension_name"],
                instance_attr=["extension_instance_name"],
                methods=["add_extension", "remove_extension", "http_get_request"],
                superclasses=["Plugin"]
            ),
            ClassModel(
                name="Foo",
                methods=["get_bar"]
            )
        ]
        filename: str = "extension.py"

    spy = Spy()

    try:
        module = spy.importspy(spymodel=PluginSpy)
        print(f"Module '{module.__name__}' complies with the specified rules.")
    except ValueError as ve:
        print(f"Validation error: {ve}")

What This Does:
---------------

This example demonstrates how ImportSpy can validate a plugin against defined structural rules. It checks the architecture, validates critical variables, and ensures the presence of specific classes with defined methods and attributes. This ensures smooth integration and consistent behavior across plugins.

🔧 How It Works
------------

Step 1: Define Rules with `SpyModel`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Using `SpyModel`, developers can specify the requirements for modules, including variables, functions, and classes. This creates a blueprint for how external modules should interact with the package.

Step 2: Validate During Import
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When a module imports the package, ImportSpy compares the module against the defined rules. Non-compliant modules are rejected, ensuring only compatible integrations proceed.

Step 3: Monitor and Debug
^^^^^^^^^^^^^^^^^^^^^^^^^

ImportSpy provides detailed insights into how modules interact with the package, enabling developers to troubleshoot and maintain alignment with the expected module structure.

📚 Case Study: Pydantic for Tool Innovation
----------------------------------------

Pydantic’s ability to perform dynamic data validation makes it a cornerstone for creating innovative tools like ImportSpy. Unlike static type checkers, Pydantic validates data structures at runtime, making it uniquely suited for Python’s dynamic ecosystem.

By leveraging Pydantic models, ImportSpy enforces strict validation rules on module interactions. This ensures consistency without sacrificing Python’s flexibility. Such an approach is rare in other programming languages, showcasing how Python can lead in innovative tooling.

Example: Leveraging Pydantic for Dynamic Module Validation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    from pydantic import BaseModel
    from typing import List, Optional

    class ClassModel(BaseModel):
        name: str
        class_attr: Optional[List[str]] = []
        instance_attr: Optional[List[str]] = []
        methods: Optional[List[str]] = []
        superclasses: Optional[List[str]] = []

    class SpyModel(BaseModel):
        filename: Optional[str] = ""
        version: Optional[str] = ""
        variables: Optional[dict] = {}
        functions: Optional[List[str]] = []
        classes: Optional[List[ClassModel]] = []
        env_vars: Optional[dict] = {}

This example shows how Pydantic allows ImportSpy to enforce structural requirements dynamically, enhancing the reliability of integrations.

🤝 Sponsorship
-----------

   💖 Support the development of ImportSpy and help make this project sustainable! Your sponsorship enables:

   🚀 Accelerated development with more time dedicated to creating features and fixing bugs.

   📘 Expanded documentation with detailed guides and comprehensive references.

   🌱 Continuous maintenance and improvement for evolving Python ecosystems.

You can sponsor ImportSpy on `GitHub Sponsors <https://github.com/sponsors/atellaluca>`_

Thank you for supporting ImportSpy and fostering innovation in the Python community! 🎉

🌟 Contributing
------------

ImportSpy is open-source and thrives on community contributions. Whether you want to report bugs, suggest features, or submit pull requests, your input is invaluable.

📝 License
-------

This project is licensed under the MIT License. See the `LICENSE <https://github.com/atellaluca/ImportSpy/blob/main/LICENSE>`_ file for details.

📖 Documentation
-------------

Explore the full documentation at `ImportSpy Docs <https://importspy.readthedocs.io>`_.

Stay up-to-date with the latest features, best practices, and examples to make the most of ImportSpy.
