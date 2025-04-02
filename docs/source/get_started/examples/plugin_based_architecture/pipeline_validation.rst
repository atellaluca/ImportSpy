Pipeline Validation (CLI Mode Example)
======================================

This example demonstrates how to use **ImportSpy** in **CLI mode** to validate a Python module against a declared import contract.

In this scenario, validation is **external and decoupled** — the module being validated has no awareness of ImportSpy.  
This makes it ideal for **CI/CD pipelines**, **automated pre-deployment checks**, or **manual compliance validation** during code review.

Why This Mode Is Powerful 🎯
----------------------------

Unlike embedded mode (where the validated module uses ImportSpy internally),  
CLI mode allows you to **treat validation as an independent, enforceable policy**.

This is especially useful when:

- You’re validating **third-party plugins or contributors' code**  
- You want **full separation of concerns** between business logic and validation  
- You’re integrating ImportSpy into **automated pipelines**

Project Structure 📁
---------------------

.. code-block::

    pipeline_validation/
    ├── extension.py         # The module to validate
    ├── plugin_interface.py  # Shared base class expected by the contract
    └── spymodel.yml         # Contract declaring expected structure and runtime

How It Works ⚙️
----------------

1. The contract in `spymodel.yml` defines the structure, environment, and runtime context expected from `extension.py`
2. ImportSpy is invoked from the command line to **validate `extension.py` against the contract**
3. If validation passes ✅, the pipeline continues  
   If it fails ❌, the pipeline halts with an explicit error

Running the Example ▶️
-----------------------

First, make sure ImportSpy is installed:

.. code-block:: bash

   pip install importspy

Then run:

.. code-block:: bash

   cd examples/plugin_based_architecture/pipeline_validation
   importspy -s spymodel.yml extension.py

If the module matches the contract, you’ll see something like:

.. code-block:: text

   ✅ Validation passed: extension.py complies with contract.

If it fails, you’ll get a detailed, actionable error:

.. code-block:: text

   ❌ Validation failed

   Reason:
     Missing attribute 'instance' in class 'Extension': extension_instance_name_WRONG

Try Breaking It 🔧
-------------------

To see the validator in action:

1. Open `spymodel.yml`  
2. Change an attribute, method, or variable name (e.g., `add_extension` → `add_extension_WRONG`)
3. Run the command again  
4. ImportSpy will immediately detect the structural mismatch and explain why

Key Takeaways 💡
-----------------

- **CLI mode** is perfect for validating modules *before execution*  
- You can enforce architectural contracts without modifying the validated code  
- Works seamlessly in CI/CD pipelines, GitHub Actions, or any build process  
- Makes **structural integrity** a core part of your development workflow

What’s Next?
-------------

- Try integrating this step into your CI/CD pipeline (e.g., GitHub Actions or GitLab CI)
- Explore :doc:`external_module_compilance` to learn how embedded mode complements this approach
- Read more about CLI mode in :doc:`../../../overview/understanding_importspy/external_mode`
