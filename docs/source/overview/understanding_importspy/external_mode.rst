External Mode
=============

External mode allows you to use ImportSpy as a **standalone validator**, without embedding any logic in the module being validated.

It’s ideal for teams who want to enforce structure and runtime compliance from the outside —  
during **CI checks**, **code review gates**, or **manual inspections** of dynamic modules, plugins, or extensions.

What Is External Validation?
----------------------------

In this mode, ImportSpy runs from the command line and:

- Loads the target module dynamically  
- Parses a separate **YAML import contract**  
- Validates the module’s **structure**, **metadata**, and **runtime compatibility**  
- Blocks execution if any contract rule is violated

It’s perfect for use cases where **you don’t own the module**, or want to **validate before running anything at all**.

Typical Use Cases
------------------

- ✅ Pre-deployment contract checks in CI/CD pipelines  
- ✅ Validating plugins before registering them in a host application  
- ✅ Enforcing runtime assumptions for sandboxed or remote code  
- ✅ Auditing third-party extensions for structural and environmental compliance

How to Use It
-------------

1. Write your import contract (usually `spymodel.yml`):

.. code-block:: yaml

   filename: extension.py
   classes:
     - name: Extension
       methods:
         - name: run
           arguments:
             - name: self

2. Run the validation using the ImportSpy CLI:

.. code-block:: bash

   importspy -s spymodel.yml -l DEBUG extension.py

This will:

- Load `extension.py`  
- Parse `spymodel.yml`  
- Validate all structure, types, env vars, OS, interpreter, and Python version  
- Print any errors or mismatches to the terminal  
- Exit with an error if validation fails

Full CLI Reference
-------------------

.. code-block:: text

    Usage: importspy [OPTIONS] [MODULEPATH]

    CLI command to validate a Python module against a YAML-defined import contract.

    Arguments:
      modulepath              Path to the Python module to load and validate.

    Options:
      --version, -v               Show ImportSpy version and exit.
      --spymodel, -s TEXT         Path to the import contract file (.yml). [default: spymodel.yml]
      --log-level, -l [DEBUG|INFO|WARNING|ERROR]
                                  Log level for output verbosity.
      --install-completion        Install completion for the current shell.
      --show-completion           Output shell snippet for autocompletion.
      --help                      Show this message and exit.

How External Validation Works 🔍
--------------------------------

Here’s what happens under the hood:

1. 📥 **Contract is loaded** → Parsed from YAML into an internal `SpyModel`  
2. 🧠 **Module is dynamically loaded** → No execution is triggered, just inspection  
3. 🏗️ **Structure is reconstructed** → Classes, methods, attributes, annotations, etc.  
4. 🌐 **Runtime context is gathered** → OS, architecture, interpreter, Python version, env vars  
5. ⚖️ **Contract is evaluated** → Actual vs expected values are compared deeply  
6. ❌ **Violations are raised** → A detailed `ValueError` is thrown with full diagnostics

All of this happens **before any code is executed**, ensuring a safe, validated runtime context.

Best Practices 🧪
-----------------

- Keep `.yml` contracts **under version control**  
- Integrate into **CI/CD** to block broken modules from reaching production  
- Use `--log-level DEBUG` to get full trace information when testing  
- Validate all external plugins **before dynamic loading**  
- Combine with :doc:`contract_structure` for clean, declarative specs

Comparison to Embedded Mode
----------------------------

External mode:

- ✅ Validates modules **without modifying them**  
- ✅ Decouples validation logic from business logic  
- ✅ Ideal for **automated pipelines** and **security reviews**

If you want the **imported module to enforce rules about its importer**,  
see :doc:`embedded_mode`.

Related Topics
--------------

- :doc:`contract_structure` – Full breakdown of contract syntax and nesting  
- :doc:`spy_execution_flow` – Internals of validation lifecycle  
- :doc:`embedded_mode` – For runtime protection from inside the validated module
