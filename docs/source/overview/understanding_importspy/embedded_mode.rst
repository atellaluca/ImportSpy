Embedded Mode
=============

Embedded mode allows a Python module to **protect itself** at runtime.

Unlike external validation, where checks are triggered from outside, embedded mode runs ImportSpy **from within the module**,  
verifying whether the environment that imported it complies with a declared contract.

It’s a powerful mechanism to ensure that **your module only runs in safe, predictable, and validated contexts**.

What Is Embedded Validation?
-----------------------------

In embedded mode, the validated module:

- ✅ Includes ImportSpy directly in its own code  
- ✅ Loads a local `.yml` import contract (e.g., `spymodel.yml`)  
- ✅ Introspects the caller (who is importing it)  
- ✅ Validates the **importing environment**, not itself  
- ❌ Refuses to execute if validation fails

This is ideal for:

- Plugins in plugin-based architectures  
- Shared packages used across teams or platforms  
- Sensitive modules with **runtime assumptions** (OS, interpreter, env vars)  
- Security-hardened components

How It Works
------------

Here’s the execution flow:

1. 🧠 The module runs `Spy().importspy(...)` when imported  
2. 📁 It parses its import contract (`spymodel.yml`)  
3. 👀 It introspects the **importing module** (via stack trace)  
4. 🔍 The importing context is matched against the contract:
   - OS, CPU, Python version, interpreter  
   - Required env vars  
   - Module structure and metadata  
5. ❌ If validation fails, a `ValueError` is raised and execution is blocked  
6. ✅ If validation passes, the importing module is returned and can be used programmatically

🔒 This creates a **Zero-Trust contract gate** — your module is only usable when the importing context is compliant.

Example Usage
--------------

Inside your protected module (e.g., `package.py`):

.. code-block:: python

   from importspy import Spy
   import logging

   caller_module = Spy().importspy(filepath="spymodel.yml", log_level=logging.DEBUG)

   # You now have access to the validated importer
   caller_module.Foo().get_bar()

Minimal Contract Example
-------------------------

Here’s a simplified import contract for embedded validation:

.. code-block:: yaml

   filename: extension.py
   variables:
     plugin_name: my_plugin
   classes:
     - name: Extension
       methods:
         - name: run
           arguments:
             - name: self
   deployments:
     - arch: x86_64
       systems:
         - os: linux
           pythons:
             - version: 3.12.8
               interpreter: CPython

This contract says:

- Only modules named `extension.py`  
- With a class `Extension` containing a `run(self)` method  
- Are allowed to import this module  
- Only on Linux + x86_64 + Python 3.12.8 + CPython

If even one condition is not satisfied, execution is halted immediately.

Why Use Embedded Mode?
-----------------------

- ✅ The module validates **who is importing it**  
- ✅ Ensures runtime safety without relying on external checks  
- ✅ Makes plugins and extensions **self-defensive**  
- ✅ Protects against unverified execution contexts in dynamic systems  
- ✅ Integrates smoothly into plugin registries or dynamic loaders

Best Practices
--------------

- Always run embedded validation **at the top** of your module  
- Version control both the module and its contract together  
- Use detailed contracts in production, relaxed ones in dev/test  
- Log validation steps using `log_level=logging.DEBUG` for traceability

Comparison to External Mode
----------------------------

Use embedded mode when:

- You want **tight control over where your module is used**  
- You are building a **plugin** or **shared extension**  
- You need to **validate the importing environment**, not just structure

Use :doc:`external_mode` when you want to validate a module from the outside (e.g., in CI/CD).

Related Topics
--------------

- :doc:`contract_structure` – Learn how to define rich, nested import contracts  
- :doc:`spy_execution_flow` – Understand how validation works under the hood  
- :doc:`external_mode` – External validation for static and pipeline use cases
