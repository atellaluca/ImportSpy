===========================================
Example Overview: Plugin-Based Architecture
===========================================

This section provides an in-depth look at a **Plugin-Based Architecture** example using **ImportSpy**.  
It demonstrates how to enforce structural and runtime compliance for dynamically loaded plugins.

Why This Example?
-----------------
This example is useful for:
- **Modular Systems** → Ensuring plugins conform to expected structures.
- **Microservices** → Validating dependencies across distributed components.
- **Extensible Applications** → Providing safety mechanisms when integrating external modules.

How It Works
------------
This example consists of **three main components**:

1. **Plugin Interface (`plugin_interface.py`)** → Defines a base class that all plugins must extend.
2. **Spy Model (`package.py`)** → Specifies validation rules using ImportSpy.
3. **Plugin Implementation (`extension.py`)** → Implements a plugin that adheres to the expected structure.

Each of these components plays a crucial role in ensuring that dynamically loaded plugins are **structurally valid** and **functionally safe**.

----------------------

📜 **Code Breakdown**
====================

Below, you'll find the complete source code for each file used in this example.

**1. Plugin Interface (`plugin_interface.py`)**
------------------------------------------------
This file defines a simple base class that plugins must inherit.

.. literalinclude:: ../../../examples/plugin_based_architecture/plugin_interface.py
   :language: python
   :caption: plugin_interface.py
   :linenos:

**2. Spy Model (`package.py`)**
---------------------------------
This file defines the validation rules for plugins using **ImportSpy**.

.. literalinclude:: ../../../examples/plugin_based_architecture/package.py
   :language: python
   :caption: package.py
   :linenos:

**3. Plugin Implementation (`extension.py`)**
----------------------------------------------
This file implements a plugin that follows the **PluginSpy** validation model.

.. literalinclude:: ../../../examples/plugin_based_architecture/extension.py
   :language: python
   :caption: extension.py
   :linenos:

Next Steps
==========
- **Run the example** following the guide in :doc:`run_example`.
- **Explore how validation works** in :doc:`package.py`.
- **Modify the plugin** in :doc:`extension` and test ImportSpy's validation mechanism.

