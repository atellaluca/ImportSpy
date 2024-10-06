Example of Usage
================

This section demonstrates how to use the `Spy` class from the `importspy` package, showcasing its ability to dynamically import and validate modules while ensuring security and modularity.

The following example shows how to dynamically import a module and validate whether it contains any classes that implement the `Plugin` interface, as well as illustrating ImportSpy's capabilities to manage plugin isolation and prevent dependency conflicts.

Code Example
------------

.. literalinclude:: ../../example/package.py
   :language: python
   :linenos:

Explanation
-----------

1. The `condition` function uses `inspect.getmembers` to check for classes in the imported module that extend the `Plugin` class. This ensures that only valid plugins are loaded.
2. The `Spy().importspy()` method is used to dynamically import the calling module and validate it using the `condition` function, allowing the framework to reactively integrate the plugin while maintaining control over its structure.
3. ImportSpy helps in **isolating plugins**, preventing them from interfering with each other by managing imports in separate contexts, which reduces the risk of dependency conflicts.

Requirements
------------

- A `Plugin` interface class must be defined in the `plugin_interface.py` module.
- The module being imported should contain at least one subclass of `Plugin` for the validation to succeed.
- ImportSpy should be installed and correctly configured in your environment to manage dynamic imports and validations effectively.
