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

1. A `PluginSpy` class is defined, inheriting from `SpyModel`. It contains a list of classes, ensuring that at least one class is a subclass of `Plugin`.
2. The `Spy().importspy()` method is called with `spymodel=PluginSpy`, dynamically importing the calling module and validating it against the specified `PluginSpy` model. This integration allows the framework to reactively manage the plugin while maintaining control over its structure.
3. ImportSpy helps in **isolating plugins**, preventing them from interfering with each other by managing imports in separate contexts, which reduces the risk of dependency conflicts.

Requirements
------------

- A `Plugin` interface class must be defined in the `plugin_interface.py` module.
- The module being imported should contain at least one subclass of `Plugin` for the validation to succeed.
- ImportSpy should be installed and correctly configured in your environment to manage dynamic imports and validations effectively.
