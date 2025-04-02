Pydantic in ImportSpy
======================

Why Pydantic Matters for ImportSpy 🧠
-------------------------------------

ImportSpy uses **Pydantic** as the foundation for its validation engine, enabling it to model and enforce strict structural and environmental expectations.

In a dynamic language like Python, where anything can change at runtime, Pydantic provides **deterministic enforcement** of expected module attributes, function signatures, return types, and environment variables.

By wrapping all validation logic in **Pydantic-based models**, ImportSpy transforms flexible contracts into **strict runtime guards**.

Core Advantages:

- ✅ Declarative schemas that model module structure and runtime constraints.
- ✅ Precise, readable errors that help developers fix violations quickly.
- ✅ Built-in support for complex types, enums, environment parsing, and more.

How Pydantic Is Used in ImportSpy 🔍
------------------------------------

All import contracts (`.yml`) are parsed and converted into nested **Pydantic models** during runtime or CLI validation. These models serve as the "expected shape" against which a module or runtime is validated.

Each layer of the import contract is mapped to a Pydantic model:

- A class like `Extension` in a plugin? → `ClassModel`.
- A function like `add_extension(msg: str) -> str`? → `FunctionModel`.
- An interpreter requirement? → `InterpreterModel`.
- OS/environment constraints? → `SystemModel`.

.. code-block:: python

   from pydantic import BaseModel
   from typing import List, Optional

   class MethodModel(BaseModel):
       name: str
       arguments: List[str]
       return_annotation: Optional[str] = None

   class ClassModel(BaseModel):
       name: str
       methods: List[MethodModel]

Validation Example 🧪
----------------------

Here’s a simplified validation use case.

.. code-block:: python

   class PluginContract(BaseModel):
       filename: str
       classes: List[ClassModel]

   contract = PluginContract(
       filename="extension.py",
       classes=[
           ClassModel(
               name="Extension",
               methods=[
                   MethodModel(name="add_extension", arguments=["self", "msg"], return_annotation="str")
               ]
           )
       ]
   )

Now at runtime, if a module lacks that method or returns the wrong type, ImportSpy fails **before** execution.

Runtime Failures Are Structured ⚠️
----------------------------------

Pydantic errors are deeply integrated with ImportSpy’s logging and debugging layers:

.. code-block:: json

   [
       {
           "loc": ["classes", 0, "methods", 0, "return_annotation"],
           "msg": "str type expected",
           "type": "type_error.str"
       }
   ]

This means: no silent failures, no vague logs.  
You know *exactly* what’s missing, and where.

Benefits Beyond Type Checking ✅
--------------------------------

- 🧩 **Cross-layer schema validation**: classes within modules, methods within classes, etc.
- 🛡️ **Zero-Trust enforcement**: if something’s missing, execution is blocked.
- 🔄 **Reusable contract definitions**: models are consistent across embedded and CLI mode.
- 📖 **Documentation as code**: import contracts double as machine- and human-readable specs.

Advanced Use: Dynamic Constraints
---------------------------------

Want to block execution in certain Python versions? Or only allow certain interpreters?

Pydantic makes it easy to write declarative rules:

.. code-block:: python

   from pydantic import BaseModel, validator

   class PythonRuntime(BaseModel):
       version: str

       @validator("version")
       def must_be_310_or_higher(cls, v):
           if v < "3.10":
               raise ValueError("Python version must be >= 3.10")
           return v

Conclusion 🎯
-------------

Pydantic is not just a convenience in ImportSpy — it’s the **core engine** behind runtime validation.

It provides a robust layer to define, enforce, and debug structural rules with confidence.

Next steps:

- :doc:`python_reflection` — Learn how ImportSpy introspects code dynamically.
- https://docs.pydantic.dev/ — Go deeper into advanced Pydantic use cases.
