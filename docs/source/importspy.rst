importspy Package
=================

The `importspy` package provides advanced functionality for dynamically importing Python modules, while offering features to validate, monitor, and manage these imports. With ImportSpy, developers can not only track imports in real-time but also validate them based on custom conditions, isolate modules to avoid conflicts, and add a layer of security to prevent unauthorized or redundant imports.

ImportSpy is particularly useful for **plugin-based architectures**, allowing the framework to take proactive actions when imported by plugins, maintaining modularity and security. It includes tools to handle **recursion detection** and prevent issues that may arise from cyclical dependencies. ImportSpy is designed to provide greater control over your Python codebase, making your applications more robust, secure, and modular.

Spy Class
=========

.. automodule:: importspy.Spy
   :members:
   :undoc-members:
   :show-inheritance:

The `Spy` class is responsible for inspecting the stack and re-importing the calling module dynamically. It includes the following method:

Methods
-------

.. automethod:: importspy.Spy.importspy
