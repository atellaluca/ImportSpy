Plugin-Based Architecture: Example Overview
===========================================

This section provides a practical introduction to how **ImportSpy** can be used  
in the context of a **Plugin-Based Architecture**. Through two simplified examples,  
you'll explore how to enforce structural validation either from **within the code**  
or via **external CLI-based automation**.

Why This Example Matters 🧩
---------------------------

In modern, modular systems, plugins and extensions are dynamically loaded,  
sometimes authored by third parties or executed in isolation.  
ImportSpy enables you to **validate their structure, interface, and runtime context**  
before execution — ensuring predictability, safety, and architectural consistency.

This folder includes **two complementary validation modes**, each adapted to a different use case.

Validation Modes 🔍
--------------------

.. list-table::
   :widths: 25 75
   :header-rows: 1

   * - Validation Mode
     - Description
   * - Embedded Validation
     - Validation is embedded **inside the package** being imported.  
       The core module (e.g. `package.py`) uses ImportSpy to validate the external module that imported it.  
       Ideal for plugin systems, microservices, or isolated components.
   * - CLI/Pipeline Validation
     - The module is validated **externally via CLI**, using the `importspy` command.  
       This mode is decoupled, and fits well in CI/CD workflows, automation scripts, or static validation.

How to Run 🛠️
--------------

Make sure you have **ImportSpy installed**:

.. code-block:: bash

   pip install importspy

Then navigate to the desired example and follow the instructions in its page.

Quick commands:

- Embedded validation:

  .. code-block:: bash

     cd examples/plugin_based_architecture
     python extension.py

- CLI validation:

  .. code-block:: bash

     cd examples/plugin_based_architecture
     importspy -s spymodel.yml extension.py

Next Steps 🚀
-------------

Try modifying the examples and observe how ImportSpy validates structure in real time.  
This helps you understand where each validation mode is best applied — and how to adapt it to your architecture.

Example Navigation 📂
----------------------

.. toctree::
   :maxdepth: 1
   :caption: Validation Modes

   external_module_compilance
   pipeline_validation
