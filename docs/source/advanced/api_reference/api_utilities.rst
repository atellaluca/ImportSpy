Utilities & Mixins
==================

ImportSpy includes a set of **utility modules and mixins** designed to support its  
**runtime validation, contract enforcement, and module inspection capabilities**.

These components form the **underlying foundation** of ImportSpy’s validation engine,  
providing low-level access to system, runtime, and environment information—ensuring  
that **every validation step is executed with context-aware accuracy**.

Utility Modules ⚙️
------------------

Utility modules are responsible for gathering **system metadata**, **module structure**,  
and **runtime information**, making it possible to validate whether a module is being  
executed in a **compliant and compatible environment**.

Key capabilities include:

- 📦 **Dynamic module inspection** – Discover classes, functions, annotations, and variables.  
- 🧠 **Environment introspection** – Detect the current OS, Python version, and architecture.  
- 🧩 **Cross-platform compatibility** – Verify whether modules are compatible with the target environment.

ModuleUtil 🏗️
^^^^^^^^^^^^^

The `ModuleUtil` class offers **reflection-based introspection of Python modules**.  
It supports dynamic loading, unloading, and deep inspection of classes, functions,  
variables, inheritance hierarchies, and annotations.

.. autoclass:: importspy.utilities.module_util.ModuleUtil
   :members:
   :undoc-members:
   :show-inheritance:

SystemUtil 🖥️
^^^^^^^^^^^^^

The `SystemUtil` class extracts **system-level information**, such as the operating system  
and environment variables, which are crucial for OS-specific validations.

.. autoclass:: importspy.utilities.system_util.SystemUtil
   :members:
   :undoc-members:
   :show-inheritance:

PythonUtil 🐍
^^^^^^^^^^^^^

The `PythonUtil` class analyzes the **Python runtime environment**.  
It identifies the interpreter (e.g., CPython, PyPy) and validates version compatibility.

.. autoclass:: importspy.utilities.python_util.PythonUtil
   :members:
   :undoc-members:
   :show-inheritance:

RuntimeUtil 🚀
^^^^^^^^^^^^^^

The `RuntimeUtil` class provides details about the system’s **hardware architecture**.  
This is especially useful for enforcing platform-specific constraints in contracts.

.. autoclass:: importspy.utilities.runtime_util.RuntimeUtil
   :members:
   :undoc-members:
   :show-inheritance:

Mixins 🔄
---------

Mixins in Python are **modular, reusable behavior components** that can be combined  
with other classes without full inheritance. ImportSpy leverages mixins to extend  
its validation logic in a **clean, non-invasive way**.

If you're new to Python mixins, check out:  
`Mixins in Python (Real Python) <https://realpython.com/inheritance-composition-python/#using-mixins-in-python>`_

AnnotationValidatorMixin 🏷️
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The `AnnotationValidatorMixin` enables **type-safe validation** of annotations  
used in functions, arguments, and variable declarations.  
It ensures that all annotations match the types supported by ImportSpy's contract system.

.. autoclass:: importspy.mixins.annotations_validator_mixin.AnnotationValidatorMixin
   :members:
   :undoc-members:
   :show-inheritance:
