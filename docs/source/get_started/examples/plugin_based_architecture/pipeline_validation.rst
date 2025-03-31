Pipeline Validation Example
===========================

This example demonstrates how to use **ImportSpy** as a CLI tool  
to validate a Python module against a declared SpyModel definition (`.yml`).

Unlike embedded validation, here the module **does not know** it's being validated.  
Validation happens externally — ideal for **pipelines, CI/CD, pre-commit checks**, or manual review.

Use Case 🔁
-----------

Imagine you're developing a plugin or step that needs to conform to a specific structure.  
Rather than embedding the validation logic, you use ImportSpy in your automation flow  
to verify the plugin **before it's executed**.

Structure 📁
------------

.. code-block::

    pipeline_validation/
    ├── extension.py         # The module to validate
    ├── plugin_interface.py  # Base class required by the SpyModel
    └── spymodel.yml         # Declares the expected structure

How to Run ▶️
-------------

1️⃣ Ensure ImportSpy is installed:

.. code-block:: bash

    pip install importspy

2️⃣ From within the `pipeline_validation/` directory, run:

.. code-block:: bash

    importspy -s spymodel.yml extension.py

✅ If the module is compliant, you'll see:

.. code-block:: text

    ✅ Module is compliant with SpyModel!

❌ If not compliant, ImportSpy will raise a descriptive error, e.g.:

.. code-block:: text

    ❌ Module is NOT compliant with SpyModel!

    Reason:
      Missing attribute 'instance' in class 'Extension': extension_instance_name_WRONG

Testing a Failure 🔥
---------------------

To try it yourself, edit `spymodel.yml` and intentionally rename a method or attribute  
(e.g., change `add_extension` to `add_extension_WRONG`), then rerun the command.

ImportSpy will catch the inconsistency and display an exact error message.

Why This Matters 🎯
-------------------

This validation mode is **non-intrusive** and perfect for:

- Continuous Integration pipelines  
- Validating third-party or untrusted code  
- Ensuring architectural compliance before deployment  

You can include this command in GitHub Actions, GitLab CI, or any build script —  
making structural compliance part of your quality gate. ✅
