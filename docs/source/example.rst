Example Usage of ImportSpy
===========================

This section demonstrates a basic example of how **ImportSpy** can be used to enforce rules for modules importing your code. In this example, we define rules that an importing module must follow using **SpyModel**, and we validate the importing module to ensure it complies.

The example is made up of two distinct files. The first file, ``developer_code.py``, contains the rules defined by the developer using **ImportSpy**. These rules outline how external modules are expected to interact with the developer's code. The second file, ``importing_module.py``, simulates a module that imports the developer's code and follows the specified rules, ensuring that the import is compliant with the developer's expectations.

developer_code.py
-----------------

In ``developer_code.py``, the developer defines the expected structure for any importing module. This is done using **SpyModel**, which specifies that the importing module must have:

- A function named ``required_function``.
- A class named ``MyRequiredClass`` with two methods: ``required_method1`` and ``required_method2``.

.. literalinclude:: ../../examples/import_validation/developer_code.py
   :language: python
   :caption: Code for defining rules in developer_code.py

importing_module.py
-------------------

In ``importing_module.py``, the importing module implements the structure required by ``developer_code.py``. It defines a class called ``MyRequiredClass``, which includes the two methods specified by the developer. Additionally, the module provides the function ``required_function``, ensuring that it fully complies with the expectations set in the developer's code.

.. literalinclude:: ../../examples/import_validation/importing_module.py
   :language: python
   :caption: Code for the importing module in importing_module.py

How it Works
------------

1. **Defining the rules**: The developer uses **SpyModel** to declare that any module importing this code must follow specific rules regarding functions and classes.
2. **Validation**: When `developer_code.py` is executed, it dynamically imports `importing_module.py` and validates its structure.
3. **Success or Failure**: 
   - If the importing module adheres to the rules, a success message is printed: 
   ```
   Module importing_module is using your library correctly!
   ```
   - If the importing module does not comply, an error message is printed:
   ```
   The importing module does not comply with the rules.
   ```

How to Run the Example
----------------------

1. **Create the files**: Place `developer_code.py` and `importing_module.py` in the root of your project directory.
2. **Run the validation**: Execute `developer_code.py` to validate `importing_module.py`.
3. **Check the output**: Depending on whether `importing_module.py` follows the defined rules, you will see either a success or failure message in the console.

This example demonstrates how **ImportSpy** can be used to proactively control how your code is imported and ensure that importing modules adhere to specific rules, reducing misuse and ensuring proper integration.
