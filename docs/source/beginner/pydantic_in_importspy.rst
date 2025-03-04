Pydantic in ImportSpy: Enforcing Data Validation
================================================

Pydantic is a **powerful data validation and serialization library**  
that ImportSpy leverages to **ensure structural integrity and enforce compliance rules dynamically**.

📌 **Why does ImportSpy use Pydantic?**  
Python is a **dynamically typed language**, which means that modules and objects can change at runtime.  
This flexibility, while powerful, can lead to **unexpected errors, missing attributes, or type inconsistencies**.

Pydantic helps **prevent these issues** by providing:

- ✅ **Strict data validation** at runtime.  
- ✅ **Automatic type enforcement** for module attributes.  
- ✅ **Error handling and structured validation messages**.  

By integrating **Pydantic with ImportSpy**, we ensure that every module meets **predefined validation constraints**,  
preventing incorrect or non-compliant modules from being executed.

**1. Understanding Pydantic: A Quick Primer** 🌟 
------------------------------------------------

Before diving into **how ImportSpy uses Pydantic**, let’s take a quick look at its **core principles**.

🔹 **What is Pydantic?**  
Pydantic is a **data validation and settings management library** that allows you to:

✅ **Define structured data models** using Python classes.  
✅ **Enforce strict type validation** at runtime.  
✅ **Automatically parse and validate data** from various sources (JSON, dictionaries, environment variables).  

📌 **Example: A Simple Pydantic Model**
.. code-block:: python

   from pydantic import BaseModel

   class User(BaseModel):
       name: str
       age: int

   u = User(name="Alice", age=25)  # ✅ Valid
   u = User(name="Bob", age="twenty")  # ❌ Error: age must be an int

Pydantic automatically **raises an error if the data does not match the expected type**.

**2. How ImportSpy Uses Pydantic** 🛠
-------------------------------------

ImportSpy uses **Pydantic models** to define and enforce **strict validation rules** for modules.  
Instead of trusting that imported modules follow the expected structure, ImportSpy **explicitly validates them**  
before allowing execution.

✅ **Defining a Validation Model in ImportSpy**
ImportSpy defines **validation models** using Pydantic, ensuring that every module meets **predefined structural constraints**.

📌 **Example: Validating a Module’s Structure**
.. code-block:: python

   from pydantic import BaseModel
   from typing import List

   class ModuleSchema(BaseModel):
       name: str
       version: str
       functions: List[str]

This model ensures that:

- Every module has a **name** (string).  
- It includes a **version** (string).  
- It defines a list of **expected functions**.  

✅ **Applying Validation at Runtime**  
When ImportSpy inspects an imported module, it dynamically extracts **metadata**  
(such as its name, version, and available functions) and validates it against the Pydantic model.

📌 **Example: Checking if a Module Meets the Validation Criteria**
.. code-block:: python

   import inspect
   import some_module  # Example external module

   module_data = {
       "name": some_module.__name__,
       "version": getattr(some_module, "__version__", "unknown"),
       "functions": [name for name, _ in inspect.getmembers(some_module, inspect.isfunction)]
   }

   validated_module = ModuleSchema(**module_data)  # ✅ Raises an error if the structure is incorrect

If `some_module` **does not meet the required structure**,  
Pydantic **automatically raises an error**, preventing execution.

**3. Dynamic Validation of Imported Modules** 🔬
------------------------------------------------

ImportSpy does not just validate **static module structures**.  
It also applies **dynamic validation rules**, ensuring that modules **adapt correctly to changing environments**.

✅ **Validating Runtime Constraints**  
Besides structure, ImportSpy can validate **Python version compatibility** using Pydantic.

📌 **Example: Enforcing Minimum Python Version**
.. code-block:: python

   from pydantic import BaseModel, Field

   class RuntimeSchema(BaseModel):
       python_version: str = Field(..., regex=r"^3\.[89]|3\.1[0-9]$")  # Accepts Python 3.8+

   runtime_data = {"python_version": "3.10"}
   RuntimeSchema(**runtime_data)  # ✅ Passes

   runtime_data = {"python_version": "3.7"}
   RuntimeSchema(**runtime_data)  # ❌ Raises an error: Incompatible Python version

This approach ensures that **only compatible modules** are executed,  
preventing errors due to unsupported Python versions.

**4. Handling Validation Failures** ⚠
--------------------------------------

If a module **fails validation**, ImportSpy provides **detailed error messages** using Pydantic’s built-in error reporting.

📌 **Example: Catching Validation Errors**
.. code-block:: python

   from pydantic import ValidationError

   try:
       invalid_module = ModuleSchema(name="example", version=1.2, functions="not_a_list")
   except ValidationError as e:
       print(e.json())

✅ **Structured Error Messages**
Pydantic provides **clear, structured validation errors**, making debugging easier.

📌 **Example Output:**
.. code-block:: json

   [
       {
           "loc": ["version"],
           "msg": "str type expected",
           "type": "type_error.str"
       },
       {
           "loc": ["functions"],
           "msg": "value is not a valid list",
           "type": "type_error.list"
       }
   ]

These messages **immediately identify** where the module structure is incorrect,  
helping developers **quickly resolve validation issues**.

**5. Why Pydantic is Essential for ImportSpy** 📌 
-------------------------------------------------

By integrating **Pydantic**, ImportSpy **ensures** that:

✅ **Imported modules follow strict structural validation.**  
✅ **Only compatible Python versions are allowed.**  
✅ **Invalid modules are blocked before execution.**  
✅ **Developers receive clear error messages when validation fails.**  

Pydantic’s **powerful validation engine** allows ImportSpy to provide **real-time enforcement of module compliance**,  
making Python’s dynamic import system **more robust, predictable, and secure**.

**6. Further Resources** 📚
---------------------------

Want to learn more about Pydantic? Check out these resources:

- **Official Pydantic Documentation** → 🔗 `https://docs.pydantic.dev/latest/`
- **ImportSpy’s Validation System** → :doc:`../overview/understanding_importspy/validation_and_compliance`
- **Best Practices for Structuring Python Modules** → 🔗 `https://docs.python.org/3/tutorial/modules.html`

**Final Thoughts** 🎯 
---------------------

Pydantic plays a **key role in ImportSpy**, enabling **real-time validation**  
of module structures, runtime configurations, and Python environment constraints.

By leveraging Pydantic’s **powerful type enforcement and error handling**,  
ImportSpy ensures that imported modules remain **predictable, secure, and compliant**.

🚀 **Next Steps:**
- **Explore ImportSpy’s Reflection System** → :doc:`python_reflection`