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

ImportSpy
=========

**ImportSpy** is the ultimate Python library for proactive import control. Designed for complex and modular environments, ImportSpy ensures that external modules adhere to precise rules, improving the stability and security of your project.

Why ImportSpy?
--------------

ImportSpy allows developers to:

- **Define clear rules**: Specify required functions, classes, and environment variables for every module importing your code.
- **Validate imports**: Ensure external modules comply with these rules before they can interact with your code.
- **Improve project quality**: Reduce bugs caused by improper imports or misconfigured environments.

Key Features
============

🔒 Proactive Import Validation
------------------------------
Define what an external module must include to import your code:
 - Required functions and classes.
 - Mandatory methods and attributes.
 - Structural dependencies such as superclasses.

📋 **Environment Variable Validation**
--------------------------------------
Ensure the environment is correctly configured:
 - Check for critical environment variables.
 - Validate their values against predefined expectations.
 - Essential for CI/CD pipelines or distributed systems.

🧩 **Optimized for Modular Architectures**
------------------------------------------
Supports complex systems:
 - Prevents cyclic dependencies.
 - Facilitates seamless integration of plugins and scalable components.

🔄 **Import Monitoring**
------------------------
Gather data on how modules interact with your code:
 - Track external imports.
 - Provide valuable debugging insights.

Installation
============

You can install ImportSpy via PyPI with a single command:

.. code-block:: bash

    pip install importspy

Quick Start
-----------

Defining Validation Rules
^^^^^^^^^^^^^^^^^^^^^^^^^

Start by creating a ``SpyModel`` that defines what is expected from modules importing your code:

.. code-block:: python

    from importspy import Spy
    from importspy.models import SpyModel, ClassModel
    from typing import List, Optional

    
    class MyLibrarySpy(SpyModel):
        # Name of the expected module file
        filename: Optional[str] = "expected_module.py"
    
        # Expected version of the module
        version: Optional[str] = "1.0.0"
    
        # Required variables defined within the module (name-value pairs)
        variables: dict = {
            "default_timeout": "30",
            "max_connections": "100"
        }
    
        # Required functions
        functions: List[str] = ["process_data", "log_results"]
    
        # Required classes
        classes: List[ClassModel] = [
            ClassModel(
                name="DataProcessor",  # Class name
                class_attr=["processor_type", "status"],  # Required class-level attributes
                instance_attr=["input_data", "output_data"],  # Required instance-level attributes
                methods=["process", "save"],  # Required methods
                superclasses=["BaseProcessor"]  # Expected superclasses
            ),
            ClassModel(
                name="Logger",
                class_attr=["log_level"],
                instance_attr=["log_file"],
                methods=["log_message", "clear_logs"],
                superclasses=[]
            )
        ]
    
        # Required environment variables
        env_vars: dict = {
            "CI": "true",
            "DATA_PATH": "/data/"
        }

Validating During Import
^^^^^^^^^^^^^^^^^^^^^^^^

Use ImportSpy to validate a module:

.. code-block:: python

    spy = Spy()

    try:
        module = spy.importspy(spymodel=MyLibrarySpy)
        print(f"Module '{module.__name__}' complies with the specified rules.")
    except ValueError as ve:
        print(f"Validation error: {ve}")

Real-World Use Cases
--------------------

✅ **CI/CD Pipelines**
^^^^^^^^^^^^^^^^^^^^^^

Ensure the CI/CD environment has all the required variables:

.. code-block:: python

    env_vars: dict = {
        "CI": "true",
        "GITHUB_ACTIONS": "true"
    }

Outcome: Prevent errors caused by misconfigurations.

✅ **Plugin-Based Systems**
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Ensure each plugin properly implements the required classes:

.. code-block:: python

    classes: List[ClassModel] = [
        ClassModel(name="PluginInterface", methods=["initialize", "execute"])
    ]

Outcome: Smooth and predictable integration.

✅ **Modular Projects**
^^^^^^^^^^^^^^^^^^^^^^^

Avoid structural errors by defining rules for essential functions and attributes:

.. code-block:: python

    functions: List[str] = ["init_module", "shutdown"]

Outcome: Improved project stability and code quality.

How It Works
------------

1. **Define Rules**: Use ``SpyModel`` to specify requirements.
2. **Module Import**: When a module is imported, ImportSpy validates that the rules are met.
3. **Validation Outcome**:
   - Success: The import proceeds without issues.
   - Failure: A descriptive error is raised.

Why Choose ImportSpy?
---------------------

- **Enhances Security**: Blocks non-compliant imports, reducing the risk of bugs and vulnerabilities.
- **Simplifies Debugging**: Easily trace incorrect imports.
- **Supports Code Evolution**: Write code that defines rules for future integrations, preventing errors before they occur.

Support the Development of ImportSpy
-------------------------------------

**ImportSpy** is an open-source project passionately developed by a single developer from **Satriano di Lucania**, a small town in the beautiful region of Lucania, Italy. This project represents a unique solution for managing Python imports, but it requires **time**, **dedication**, and **resources** to grow and improve.

Why Your Support Matters
------------------------

By sponsoring **ImportSpy**, you can help:

- **Accelerate development**: Your support allows me to dedicate more time to creating new features, fixing bugs, and improving compatibility.
- **Keep the project up to date**: Ensure ImportSpy continues to support the latest Python versions and modern development needs.
- **Provide community support**: Expand documentation, create advanced examples, and respond to user inquiries.
- **Make the project sustainable**: Promote innovation in an open-source environment.

Every contribution, big or small, makes a difference and helps keep the project free and accessible for everyone.

How to Sponsor
--------------

You can sponsor ImportSpy directly on GitHub. As a sponsor, you will:

- **Be publicly recognized** (if desired) in the documentation and GitHub repository.
- **Influence project development** by suggesting features that meet your needs.
- **Receive priority support** for integrating ImportSpy into your projects.

💡 Sponsor ImportSpy now: `GitHub Sponsors <https://github.com/sponsors/atellaluca>`_


A Small Contribution, A Big Impact
-----------------------------------

Your support is not just an investment in ImportSpy but also in the open-source philosophy, which fosters innovation and collaboration within the Python community. Even a small contribution can make a big difference!

Thank you for believing in this project and helping take ImportSpy to the next level. ❤️

Access the Full Documentation
=============================

For detailed guidance on using **ImportSpy**, including advanced usage, API references, and examples, visit `our official documentation <https://importspy.readthedocs.io>`_.

The documentation is continually updated to ensure you have access to the latest features, best practices, and integration tips. Whether you're a beginner or an experienced developer, the documentation will help you unlock the full potential of ImportSpy.


Contribute to ImportSpy
-----------------------

Want to contribute? Add new features, provide feedback, or report bugs.

License
-------

This project is distributed under the MIT License. See the `LICENSE <https://github.com/atellaluca/ImportSpy/blob/main/LICENSE>`_ file for details.
