External Module Compliance (Embedded Mode Example)
==================================================

This example demonstrates one of ImportSpy’s most powerful features:  
**embedded validation**, where a module being imported can validate **who is importing it**.

Unlike traditional tools that validate their own structure, ImportSpy allows a module to **control its consumers** —  
ensuring that only fully compliant modules can interact with it.

Why This Matters 🔐
--------------------

In plugin architectures, dynamic systems, or modular platforms, core components are often imported by untrusted or external code.  
Without structural guarantees, this opens the door to:

- Runtime crashes from missing methods  
- Silent logic errors due to incompatible extensions  
- Unpredictable behaviors across environments

ImportSpy solves this by allowing the core module to define a **YAML-based contract**, and reject importers that don’t match.

Use Cases ✅
~~~~~~~~~~~~

- Plugin systems with strict APIs  
- Modular backends with third-party integration  
- Secure extensions and validation gateways  
- Projects needing **controlled extensibility** from external modules

Project Structure 📁
---------------------

.. code-block::

    external_module_compliance/
    ├── extension.py              # External module trying to import the core
    ├── package.py                # Core module protected by ImportSpy
    ├── plugin_interface.py       # Shared interface definition
    └── spymodel.yml              # Structural contract for external validation

How It Works 🧠
----------------

1. `extension.py` tries to import `package.py`
2. Inside `package.py`, ImportSpy runs in **embedded mode**:
   .. code-block:: python

      caller_module = Spy().importspy(filepath="spymodel.yml")

3. The contract in `spymodel.yml` defines what `extension.py` must contain (e.g., classes, methods, variables)
4. If the contract is satisfied:
   - `caller_module` is assigned to `extension.py`  
   - The validated importer can be used directly, like:  
     `caller_module.Foo().get_bar()`
5. If not, ImportSpy raises an error and **prevents usage of the module**.

Run the Example ▶️
--------------------

From the root of the project, run:

.. code-block:: bash

    cd examples/plugin_based_architecture/external_module_compliance
    python extension.py

Expected Output:

.. code-block:: text

    Foobar

This means:

- The importer (`extension.py`) passed validation  
- The core module (`package.py`) verified its importer before doing anything  
- You now have **runtime-level confidence** in how the system integrates

Simulating a Failure ❌
------------------------

To see ImportSpy in action, try this:

1. Open `spymodel.yml`
2. Modify a method name (e.g., `add_extension` → `add_extension_WRONG`)
3. Run the example again:

.. code-block:: bash

    python extension.py

Expected output:

.. code-block:: text

    ValueError: Missing method in class Extension: 'add_extension_WRONG'. Ensure it is defined.

🛑 This is **real-time structural enforcement**.  
The module is immediately blocked for violating the import contract.

Key Takeaways 🧩
-----------------

- ImportSpy’s **embedded mode** empowers a module to **control who is allowed to import it**
- It guarantees that plugins, extensions, or third-party modules conform to the contract before any code runs
- The returned `caller_module` gives you full access to the validated importer — just like any other module object
- This pattern is ideal when **predictability, structure, and security** are non-negotiable

Next Steps 🔄
-------------

- Try editing the contract and module to explore different validations
- Combine this with :doc:`pipeline_validation` to enforce contracts in CI/CD pipelines
- Read more about embedded mode in :doc:`../../../overview/understanding_importspy/embedded_mode`
