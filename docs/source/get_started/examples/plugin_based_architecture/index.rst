Plugin-Based Architecture: Example Suite Overview
=================================================

Welcome to the **Plugin-Based Architecture** examples for ImportSpy.  
This section showcases how ImportSpy can be integrated into real-world modular systems to ensure **structural integrity**, **runtime compatibility**, and **import-time compliance**.

Why Plugins Need Validation 🧩
------------------------------

Modern applications are often built around **plugin systems**, **modular services**, or **runtime extensions** —  
components that are loaded dynamically and sometimes authored externally.

Without strict validation, these integrations can lead to:

- ❌ Unexpected runtime errors  
- ❌ Silent logic bugs due to mismatched interfaces  
- ❌ Security vulnerabilities in dynamic loading scenarios

ImportSpy solves this by enforcing **formal contracts** — ensuring that every module that is imported or interacted with follows a precise structure and runtime context.

What You'll Learn Here 🎯
--------------------------

In this section, you’ll explore two complementary validation modes:

.. list-table::
   :widths: 25 75
   :header-rows: 1

   * - Validation Mode
     - Description
   * - Embedded Mode
     - Validation is performed **inside the core module** (e.g. `package.py`) that is being imported.  
       When an external module (like `extension.py`) imports it, the core validates the importer.  
       Ideal for secure plugin frameworks, APIs, or modular applications.
   * - CLI Mode
     - Validation is performed **externally via the command line**, using `importspy -s contract.yml module.py`.  
       Perfect for CI/CD, static enforcement, or pre-deployment checks.

How to Run the Examples 🛠️
---------------------------

Make sure ImportSpy is installed:

.. code-block:: bash

   pip install importspy

Then:

- 🧪 **Embedded Validation**
  .. code-block:: bash

     cd examples/plugin_based_architecture
     python extension.py

- 🧪 **CLI Validation**
  .. code-block:: bash

     cd examples/plugin_based_architecture
     importspy -s spymodel.yml extension.py

Try editing the modules or the contract and rerun the validations —  
you’ll see how ImportSpy detects mismatches immediately.

Ready to Dive In? 🚀
--------------------

These examples provide a practical foundation for using ImportSpy in your own architecture.  
They demonstrate not just how validation works, but **where it fits** in modern Python workflows.

Navigate to a specific mode to explore:

.. toctree::
   :maxdepth: 1
   :caption: Validation Modes

   external_module_compilance
   pipeline_validation
