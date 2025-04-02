Understanding Python Reflection in ImportSpy
============================================

Why Reflection Matters 🪞
--------------------------

Python's reflection capabilities allow code to inspect, analyze, and interact with itself at runtime.  
This is central to how **ImportSpy** validates modules dynamically — it doesn't just look at source code,  
it actively examines **what exists and how it behaves** at the moment of import.

In a system where plugins or modules are loosely coupled, this allows ImportSpy to:

- Validate structural expectations (`classes`, `functions`, `attributes`).
- Detect runtime constraints (`interpreter`, `version`, `environment`).
- Prevent unexpected or unauthorized imports.

Core Python Reflection Tools 🔍
-------------------------------

ImportSpy uses several key components of Python’s reflection toolbox:

**1. `inspect`** — Runtime introspection

.. code-block:: python

   import inspect

   def foo(): pass

   print(inspect.isfunction(foo))          # True
   print(inspect.getmembers(foo))          # List all members of the function object

**2. `getattr` / `hasattr` / `setattr`** — Attribute access and mutation

.. code-block:: python

   class User: name = "Alice"

   u = User()
   print(getattr(u, "name"))               # "Alice"
   print(hasattr(u, "email"))              # False
   setattr(u, "email", "a@example.com")    # Dynamically add attribute

**3. `importlib`** — Dynamic module loading

.. code-block:: python

   import importlib

   mod = importlib.import_module("math")
   print(mod.sqrt(16))                     # 4.0

These techniques allow ImportSpy to analyze **any arbitrary Python module** during validation.

How ImportSpy Uses Reflection 🧠
--------------------------------

ImportSpy doesn’t hardcode validation rules into your code.  
Instead, it reads a YAML contract, parses it into a structured `SpyModel`, and:

1. **Intercepts the importing context**  
   → via `inspect.stack()` to determine *who* is importing the validated module.

2. **Loads the target module**  
   → via `importlib` or by extracting from `sys.modules`.

3. **Validates its structure**  
   → using `inspect.getmembers()` to check for methods, annotations, and base classes.

4. **Checks runtime environment**  
   → including Python version, interpreter type, and required variables.

This **dynamic, contract-driven validation** is only possible thanks to Python's reflective architecture.

Reflection in Embedded Mode vs CLI Mode 🔁
------------------------------------------

In **Embedded Mode**, reflection is used by the validated module itself:

- It calls `Spy().importspy(...)`
- Uses `inspect.stack()` to identify the **caller**
- Then validates that external environment using reflection

In **CLI Mode**, reflection is applied directly to the target file:

- `importspy -s contract.yml module.py`
- ImportSpy dynamically loads and introspects the module
- Checks all runtime constraints before it can be deployed

Best Practices & Pitfalls ⚠️
----------------------------

Reflection is powerful — but should be used wisely:

✅ **Cache inspection results** to avoid repeat analysis  
❌ Avoid calling unknown or unsafe methods with `getattr()` blindly  
✅ Combine with type checks (`callable`, `isinstance`) before execution  
❌ Don’t mutate live objects unless you're in full control

Example: safe method invocation

.. code-block:: python

   if hasattr(module, "run") and callable(module.run):
       module.run()

Takeaway 🧠
-----------

Reflection is what makes ImportSpy possible.

By using `inspect`, `importlib`, and Python’s runtime model, ImportSpy can:

- Enforce validation without altering your code
- Dynamically adapt to different environments
- Offer a robust, runtime-safe contract enforcement system

Explore more:

- :doc:`pydantic_in_importspy`
- `https://docs.python.org/3/library/inspect.html`
