ImportSpy
=========

.. image:: https://raw.githubusercontent.com/atellaluca/ImportSpy/refs/heads/main/assets/ImportSpy.png

.. image:: https://img.shields.io/github/issues/atellaluca/ImportSpy?style=flat-square
   :target: https://github.com/atellaluca/ImportSpy/issues

.. image:: https://img.shields.io/github/stars/atellaluca/ImportSpy?style=flat-square
   :target: https://github.com/atellaluca/ImportSpy/stargazers

.. image:: https://img.shields.io/github/forks/atellaluca/ImportSpy?style=flat-square
   :target: https://github.com/atellaluca/ImportSpy/network

.. image:: https://img.shields.io/github/license/atellaluca/ImportSpy?style=flat-square
   :target: https://github.com/atellaluca/ImportSpy/blob/master/LICENSE


Proactive Python Import Control Library
=======================================

**ImportSpy** is a lightweight Python library that provides **proactive control** over how your Python code is used when imported by other modules or packages. This ensures that external modules importing your code adhere to specific rules, preventing misuse and ensuring smooth integration in larger or modular Python projects. Designed for plugin-based systems or modular architectures, **ImportSpy** enables real-time validation and import tracking, ensuring that your code is integrated and used properly across diverse Python environments.

The ``importspy`` package gives developers even more control by allowing them to define custom validation rules for modules that import their code, ensuring that these modules conform to the expected structure and functionality. This is particularly valuable in modular systems or plugin-based architectures, where system stability and security depend on well-defined and consistent imports. 

With **ImportSpy**, developers can validate that importing modules meet predefined conditions, such as the presence of required functions or classes. It also allows real-time tracking of how the code is imported, making debugging and optimization more efficient. ImportSpy enhances modularity by preventing issues such as recursion or cyclic dependencies, promoting cleaner and more organized design structures. Additionally, it adds an extra layer of security by catching incorrect imports early and isolating modules to avoid conflicts.

This package is ideal for projects that require strict validation of how the code is imported and used, helping to ensure that external modules respect the structure you define and avoid potential misconfigurations or security risks.


Key Features of ImportSpy for Python Code Control
=================================================

- **Proactive control**: With ImportSpy, you can define rules in advance that enforce how your Python code is imported and used by other modules, ensuring compliance. **This allows you to write proactive code that prevents potential future issues** in other Python projects.
- **Dependency validation**: Automatically check that the importing modules respect the required structure, such as functions, classes, and methods. This ensures your Python dependencies are correctly handled.
- **Real-time import tracking**: Monitor how external modules interact with your code, providing valuable insights that help with debugging and optimization in Python development.
- **Error prevention**: Catch potential misuse of your code early, reducing bugs and improving integration stability when your Python code is used in third-party projects.
- **Lightweight and easy to use**: ImportSpy is designed to integrate seamlessly with existing Python projects without the need for complex configurations, making it ideal for Python developers of all levels.

Installation: Get Started with ImportSpy
========================================

You can easily install **ImportSpy** via pip, the Python package manager:

.. code-block:: bash

    pip install importspy

Usage Example: How to Use ImportSpy for Validating Python Modules
=================================================================

Here's a simple example showing how to use **ImportSpy** to validate that an importing Python module follows specific rules, such as requiring a particular function and class with specified methods:

.. code-block:: python

    # your_code.py

    from importspy import Spy
    from importspy.models import SpyModel, ClassModel
    from typing import List

    # Define the rules for how your Python code should be used
    class MyLibrarySpy(SpyModel):
        functions: List[str] = ["required_function"]  # Required function in the importing module
        classes: List[ClassModel] = [
            ClassModel(
                name="MyRequiredClass",  # Required class name
                methods=["required_method1", "required_method2"]  # Required methods in the class
            )
        ]

    # Check if the importing module complies with the rules
    module = Spy().importspy(spymodel=MyLibrarySpy)

    if module:
        print(f"Module {module.__name__} is using your library correctly!")
    else:
        print("The importing module is not complying with the rules.")

Example of a Compliant Importing Python Module
==============================================

A Python module that correctly imports and adheres to your defined rules might look like this:

.. code-block:: python

    # importing_module.py

    import your_code

    class MyRequiredClass:
        def required_method1(self):
            print("Method 1 implemented")

        def required_method2(self):
            print("Method 2 implemented")

    def required_function():
        print("Function implemented")

What Happens During Import Validation
=====================================

If the importing module correctly implements the required functions, classes, and methods, **ImportSpy** will provide this output:

.. code-block:: text

    Module importing_module is using your library correctly!

However, if the importing module does not meet the rules (for example, a function or class is missing), you'll see an error message like:

.. code-block:: text

    The importing module is not complying with the rules.

How Proactive Validation Works
==============================

For **ImportSpy** to trigger proactive validation, the external module (which is importing your code) must explicitly import the developer's code that integrates **ImportSpy**. This import process starts the validation mechanism.

Here's how it works:

1. **Define validation rules**: The developer uses **ImportSpy** to define a `SpyModel` that outlines the structure and behavior expected from the external module. This may include functions, classes, and specific methods.
2. **External module import**: When the external module imports the developer's code, **ImportSpy** performs a validation to check if the importing module adheres to the predefined rules.
3. **Validation outcome**: If the importing module complies with the rules (e.g., has the required functions and classes), the validation passes. Otherwise, an error message is returned, indicating non-compliance.

Example Workflow
================

In the developer's code:

.. code-block:: python

    # your_code.py

    from importspy import Spy
    from importspy.models import SpyModel, ClassModel
    from typing import List

    class MyLibrarySpy(SpyModel):
        functions: List[str] = ["required_function"]
        classes: List[ClassModel] = [
            ClassModel(
                name="MyRequiredClass",
                methods=["required_method1", "required_method2"]
            )
        ]

    spy = Spy()
    module = spy.importspy(spymodel=MyLibrarySpy)

    if module:
        print(f"Module {module.__name__} is using your library correctly!")
    else:
        print("The importing module is not complying with the rules.")

In the external module that imports the developer's code:

.. code-block:: python

    # importing_module.py

    import your_code

    class MyRequiredClass:
        def required_method1(self):
            print("Method 1 implemented")

        def required_method2(self):
            print("Method 2 implemented")

    def required_function():
        print("Function implemented")

Why Use ImportSpy in Your Python Development Projects?
======================================================

- **Ensure Python code quality**: Set up clear rules for how your code should be used in external Python projects, ensuring proper integration and reducing issues.
- **Improve debugging and development**: By tracking how your Python code is imported and used, you gain valuable insights that speed up the identification of potential problems.
- **Support modular Python architectures**: ImportSpy is particularly suited for modular or plugin-based Python projects, ensuring that all components interact as expected.
- **Proactive Python code**: ImportSpy helps you write code that proactively validates future integrations, preventing errors before they happen. This gives you greater control over your Python code's quality, even when it's used by other teams or developers.

Contributing to ImportSpy
=========================

We welcome contributions! If you find bugs, have suggestions, or want to contribute new features, feel free to open issues or submit pull requests to help improve **ImportSpy**. Whether it's bug reports, feature suggestions, or code contributions, your help is appreciated!

Sponsorship
===========

You can support the continued development of **ImportSpy** by becoming a sponsor. If you find this project useful and would like to help keep it growing, please consider `sponsoring the project on GitHub <https://github.com/sponsors/atellaluca>`_.

Your sponsorship will help us to dedicate more time to improvements, new features, and support for the community. Thank you for your generosity!

License
=======

This project is licensed under the MIT License. See the `LICENSE <https://github.com/atellaluca/ImportSpy/blob/docs-enhancement/LICENSE>`_ file for details.
