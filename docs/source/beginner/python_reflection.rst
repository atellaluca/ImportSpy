Understanding Python Reflection
===============================

Reflection is a **powerful feature** in Python that allows a program to **inspect and modify itself at runtime**.  
Think of it like **a mirror for your code**: just as a mirror lets you see your own face, reflection lets Python "look at itself"  
to analyze modules, functions, and classes dynamically.

🔍 **Why Reflection Matters in ImportSpy**  
ImportSpy **heavily relies on reflection** to validate external modules dynamically.  
Instead of analyzing code statically, ImportSpy inspects **what is actually present in a module at runtime**,  
ensuring that all dependencies follow strict validation rules before they are executed.

This guide covers:

- **What Reflection Is**, with beginner-friendly explanations and examples.  
- **How to Use Basic Reflection in Python**, before moving to advanced topics.  
- **How ImportSpy Uses Reflection** for dynamic module validation.  
- **Best Practices** and potential pitfalls when working with reflection.  

📌 **By the end of this guide, you will:**
- Understand **how reflection works** in Python.
- Know **how ImportSpy leverages reflection** to enforce compliance.
- Be able to **use reflection tools like `inspect`, `getattr()`, and `importlib` effectively**.

**1. Reflection Explained: The Mirror Analogy** 🌟 
--------------------------------------------------

Imagine you’re in a **dark room**, trying to describe yourself without a mirror.  
You know your hands and face are there, but you can’t see them.  
**This is like a Python module without reflection**—it has functions and classes,  
but without explicitly calling them, Python doesn’t "see" them.

Now, if you **turn on a light and look in a mirror**, you can see every detail.  
Reflection is that light: it allows Python to **examine its own structure** at runtime.

**2. First Steps with Python Reflection** 🛠 
--------------------------------------------

Before diving into ImportSpy’s advanced use of reflection, let’s explore its **basic building blocks**.

✅ **`dir()` – Listing Attributes in an Object**
.. code-block:: python

   class Person:
       def __init__(self, name):
           self.name = name

   p = Person("Alice")

   print(dir(p))  # Lists all attributes of the object

This command shows **everything that exists in the object**, including methods and variables.

✅ **`getattr()` – Accessing Attributes Dynamically**
.. code-block:: python

   print(getattr(p, "name"))  # Output: Alice

If we don’t know an object’s attributes beforehand, `getattr()` lets us access them **dynamically**.

✅ **`hasattr()` – Checking if an Attribute Exists**
.. code-block:: python

   print(hasattr(p, "age"))  # Output: False

This prevents errors when accessing unknown attributes.

✅ **`setattr()` – Modifying Attributes at Runtime**
.. code-block:: python

   setattr(p, "age", 30)  
   print(p.age)  # Output: 30

**3. Advanced Reflection Tools in Python** 🔬
---------------------------------------------

Once comfortable with basic reflection, we can use **more advanced tools**  
like `inspect` and `importlib`, which ImportSpy relies on heavily.

✅ **`inspect` – Extracting Function and Class Information**
.. code-block:: python

   import inspect

   class Sample:
       def method(self):
           return "Hello"

   print(inspect.getmembers(Sample, inspect.isfunction))
   # Output: [('method', <function Sample.method>)]

✅ **`importlib` – Dynamic Module Importing**
.. code-block:: python

   import importlib

   module_name = "math"
   math_module = importlib.import_module(module_name)

   print(math_module.sqrt(25))  # Output: 5.0

These tools allow ImportSpy to **analyze modules dynamically**,  
checking **which functions and attributes exist at runtime**.

**4. How ImportSpy Uses Reflection** 🚀 
---------------------------------------

Now that we understand **Python’s reflection tools**,  
let’s see **how ImportSpy leverages them for module validation**.

✅ **Tracking the Execution Stack**  
ImportSpy uses `inspect.stack()` to determine **which module is calling an import**  
and apply validation rules accordingly.

✅ **Dynamically Extracting Module Metadata**  
Using `inspect.getmodule()`, ImportSpy retrieves information about an imported module.

✅ **Enforcing Structural Compliance**  
By analyzing **functions, classes, and attributes at runtime**,  
ImportSpy ensures every module follows the correct validation model.

**5. Best Practices & Pitfalls of Reflection** ⚠ 
-------------------------------------------------

Reflection is powerful but can **cause performance issues and security risks**  
if not used correctly. Here’s what to keep in mind:

❌ **Avoid Overusing Reflection**  
Excessive use of `inspect` functions can **slow down execution**.

✅ **Cache Reflection Results**  
If you need to **check the same attributes multiple times**, store them in a variable.

❌ **Be Careful with `setattr()`**  
Modifying objects dynamically can **introduce bugs** if used improperly.

✅ **Always Validate Input Before Execution**  
Instead of blindly calling `getattr()`, ensure the function exists and is safe to execute.

🔹 **Example: Safe Execution of Methods**
.. code-block:: python

   method = getattr(module, "run", None)
   if method and callable(method):
      method()  # ✅ Safe execution

**6. Further Resources** 📚 
---------------------------

Want to go deeper? Here are some great resources:

- **Python’s Official Reflection Docs** → 🔗 `https://docs.python.org/3/library/inspect.html`
- **ImportSpy’s Validation Model** → :doc:`../overview/understanding_importspy/validation_and_compliance`
- **Dynamic Module Loading in Python** → 🔗 `https://docs.python.org/3/library/importlib.html`

**Final Thoughts** 🎯 
---------------------

Reflection is a **core component** of ImportSpy, allowing it to:

✅ **Dynamically inspect and validate imported modules.**  
✅ **Enforce strict compliance rules before execution.**  
✅ **Provide a flexible and adaptive validation framework.**  

By mastering Python’s reflection capabilities,  
you can **better understand how ImportSpy works** and use it effectively in your projects.  

🚀 **Next Steps:**
- **Explore ImportSpy’s Compliance Model** → :doc:`../overview/understanding_importspy/validation_and_compliance`
- **Learn About Pydantic’s Role in ImportSpy** → :doc:`pydantic_in_importspy`

