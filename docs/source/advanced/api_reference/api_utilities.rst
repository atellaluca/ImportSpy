Utilities & Mixins
==================

ImportSpy includes **utility functions and mixins** that enhance its **runtime validation,  
module inspection, and execution environment verification**. These components serve as  
the **support layer** for ImportSpy’s validation mechanisms, enabling dynamic analysis  
of **imported modules, system configurations, and runtime constraints**.

Utility Modules ⚙️
-------------------

ImportSpy’s **utility modules** provide essential functions to ensure that Python modules  
are correctly structured and executed in a **validated environment**. These utilities enable:

- **Dynamic module inspection** → Retrieve metadata, extract function/class attributes, and verify compliance.
- **System introspection** → Identify the **operating system**, **Python version**, and **hardware architecture**.
- **Cross-platform execution consistency** → Ensure modules run in compatible environments.

ModuleUtil 🏗️
^^^^^^^^^^^^^

The `ModuleUtil` class provides **tools for dynamically inspecting Python modules**,  
retrieving function/class metadata, and enforcing **runtime validation rules**.

.. autoclass:: importspy.utilities.module_util.ModuleUtil
   :members:
   :undoc-members:
   :show-inheritance:

SystemUtil 🖥️
^^^^^^^^^^^^^^

The `SystemUtil` class retrieves **system-level information**, such as the **operating system**  
name and the current **environment variables**, ensuring ImportSpy can enforce OS-based validation.

.. autoclass:: importspy.utilities.system_util.SystemUtil
   :members:
   :undoc-members:
   :show-inheritance:

PythonUtil 🐍
^^^^^^^^^^^^^

The `PythonUtil` class **analyzes the Python runtime environment**, verifying that modules  
are executed in a **compatible Python version and implementation**.

.. autoclass:: importspy.utilities.python_util.PythonUtil
   :members:
   :undoc-members:
   :show-inheritance:

RuntimeUtil 🚀
^^^^^^^^^^^^^^

The `RuntimeUtil` class extracts **hardware architecture details**, ensuring  
ImportSpy prevents execution in **unsupported system configurations**.

.. autoclass:: importspy.utilities.runtime_util.RuntimeUtil
   :members:
   :undoc-members:
   :show-inheritance:

Mixins 🔄
---------

Mixins in Python are **reusable classes that provide specific behavior**  
without requiring full class inheritance. They are designed to **extend functionality**  
in a modular way, allowing ImportSpy to **apply validation logic dynamically**  
without duplicating code across multiple components.

If you're new to **mixins**, you can refer to the official Python documentation:  
`Mixins in Python <https://realpython.com/inheritance-composition-python/#using-mixins-in-python>`_

In ImportSpy, mixins allow for **annotation-based validation** by enforcing compliance  
rules on function signatures, attributes, and types.

AnnotationValidatorMixin 🏷️
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The `AnnotationValidatorMixin` class is responsible for validating **function annotations**,  
ensuring that functions follow expected **type hints** and structural rules.  
This mixin is particularly useful when combined with **Pydantic**, a powerful library  
for **data validation and serialization in Python**.

For more information on **Pydantic's role in type validation**, visit:  
`Pydantic Documentation <https://docs.pydantic.dev/latest/>`_

.. autoclass:: importspy.mixins.annotations_validator_mixin.AnnotationValidatorMixin
   :members:
   :undoc-members:
   :show-inheritance: