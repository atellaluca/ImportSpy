Example of Usage
================

This section demonstrates how to use the `Spy` class from the `importspy` package with a validation function.

The following example shows how to dynamically import a module and check if it contains any classes that implement the `Plugin` interface.

Code Example
------------

.. literalinclude:: ../../example/package.py
   :language: python
   :linenos:

Explanation
-----------

1. The `condition` function uses `inspect.getmembers` to check for classes in the imported module.
2. The `Spy().importspy()` method is used to dynamically import the calling module and validate it using the `condition` function.

Requirements
------------

- A `Plugin` interface class must be defined in the `plugin_interface.py` module.
- The module being imported should contain at least one subclass of `Plugin` for the validation to succeed.

