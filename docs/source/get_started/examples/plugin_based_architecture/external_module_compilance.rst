External Module Compliance Example
==================================

This example demonstrates how **ImportSpy** can be embedded in a core package or framework  
to validate the structure and context of an **external module that imports it**.

Unlike typical validation tools, ImportSpy allows the imported module to perform compliance  
checks **on the module that imports it**, enabling powerful runtime guarantees and architectural control.

Why This Matters 📦
-------------------

In plugin-based architectures or distributed environments, plugins are often isolated and loaded dynamically.  
This example shows how to enforce **structural contracts** and ensure that only valid modules  
can interact with the system — preventing runtime failures, bugs, or security issues.

Key Concepts:
~~~~~~~~~~~~~

- **Spy-embedded validation**: the core module (`package.py`) introspects and validates the external caller (`extension.py`).
- **Runtime context awareness**: validated modules gain access to the caller’s context if compliant.
- **Ideal for**: plugin systems, RESTful extension APIs, modular platforms.

Project Structure 🧱
--------------------

.. code-block::

    external_module_compliance/
    ├── extension.py              # External plugin-like module
    ├── package.py                # Core module that validates its importer
    ├── plugin_interface.py       # Base class expected by the SpyModel
    └── spymodel.yml              # Validation model for structural compliance

How It Works 🔍
----------------

1. `extension.py` imports `package.py` (the validated core).
2. `package.py` runs `Spy().importspy(...)` using the rules defined in `spymodel.yml`.
3. If validation succeeds, `caller_module` is assigned to `extension.py`, and can be used directly.
4. If validation fails, an error is raised before anything else is executed.

Running the Example ▶️
-----------------------

To run the working example:

.. code-block:: bash

    cd examples/external_module_compliance
    python extension.py

Expected Output ✅
------------------

.. code-block:: text

    Foobar

This indicates that:
- `extension.py` passed validation against `spymodel.yml`
- `package.py` successfully introspected its importer
- The returned `caller_module` (which is `extension.py`) was used to call `Foo().get_bar()`

Intentional Failure Example ❌
-------------------------------

To see ImportSpy in action during failure, edit `spymodel.yml` like this:

.. code-block:: yaml

    - name: add_extension_WRONG

Then run the same command:

.. code-block:: bash

    python extension.py

You will see:

.. code-block:: text

    ValueError: Missing method in class Extension: 'add_extension_WRONG'. Ensure it is defined.

This is a real-time structural enforcement: the module is rejected because it does not meet the required contract.

Takeaways 💡
------------

- Spy-embedded mode allows modules to **control who can import them**.
- This approach is ideal when structural control is critical to system integrity.
- You can use the returned `caller_module` to perform contextual logic, like `caller_module.Foo().get_bar()`.

Next Steps 🎯
-------------

- Try adding/removing variables or methods in `extension.py` and updating the model.
- Explore more examples in :doc:`../pipeline_validation/index` for CLI and pipeline integration.
