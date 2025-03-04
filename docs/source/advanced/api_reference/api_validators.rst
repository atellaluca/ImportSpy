Validation System
=================

ImportSpy provides a **robust validation system** to enforce compliance with expected  
execution environments, ensuring that **modules are only imported in verified conditions**.  

Validators play a **crucial role** in maintaining **stability, security, and predictability**,  
preventing unexpected behavior caused by **incorrect execution environments or misconfigured system constraints**.

Understanding ImportSpy's Validation System 🔎
----------------------------------------------

The validation system operates at multiple levels:

- **Execution Environment Validation** → Confirms compatibility with Python versions, OS settings, and runtime constraints.  
- **Dependency Compliance** → Ensures that required dependencies and environment variables are correctly set before execution.  
- **Structural Expectations** → Ensures that the importing module meets predefined structural and configuration requirements.  

Each validator is responsible for **enforcing specific execution rules**,  
allowing ImportSpy to detect and handle inconsistencies **before a module is allowed to execute**.

SpyModelValidator 🏗️
---------------------

The `SpyModelValidator` is the **core validation engine** in ImportSpy.  
It **compares the execution environment** of an importing module against an expected `SpyModel` definition,  
ensuring that the execution conditions conform to predefined compliance rules.

.. autoclass:: importspy.validators.spymodel_validator.SpyModelValidator
   :members:
   :undoc-members:
   :show-inheritance:

Attribute Validator 🔤
----------------------

The `AttributeValidator` ensures that **required environment variables**  
are present in the execution context, preventing misconfigurations.

.. autoclass:: importspy.validators.attribute_validator.AttributeValidator
   :members:
   :undoc-members:
   :show-inheritance:

Function Validator 🛠️
----------------------

The `FunctionValidator` checks that **runtime execution constraints are met**,  
including **Python interpreter type, OS compatibility, and available system dependencies**.

.. autoclass:: importspy.validators.function_validator.FunctionValidator
   :members:
   :undoc-members:
   :show-inheritance:

Argument Validator 🎛️
----------------------

The `ArgumentValidator` ensures that **system configurations and environment variables**  
follow expected constraints, such as **required values and predefined formats**.

.. autoclass:: importspy.validators.argument_validator.ArgumentValidator
   :members:
   :undoc-members:
   :show-inheritance:

Module Validator 📦
-------------------

The `ModuleValidator` verifies that **the importing environment meets the required conditions**,  
ensuring that execution only proceeds in **approved system configurations**.

.. autoclass:: importspy.validators.module_validator.ModuleValidator
   :members:
   :undoc-members:
   :show-inheritance:

System Validator 🖥️
--------------------

The `SystemValidator` checks **operating system constraints**,  
ensuring that modules execute **only in explicitly approved OS environments**.

.. autoclass:: importspy.validators.system_validator.SystemValidator
   :members:
   :undoc-members:
   :show-inheritance:

Python Validator 🐍
-------------------

The `PythonValidator` ensures that the importing module **runs in a compatible Python environment**,  
checking for **minimum version requirements, interpreter type, and virtual environment constraints**.

.. autoclass:: importspy.validators.python_validator.PythonValidator
   :members:
   :undoc-members:
   :show-inheritance:

Runtime Validator 🚀
--------------------

The `RuntimeValidator` enforces **execution constraints** related to **hardware architecture,  
system dependencies, and required environment variables**, ensuring consistency across different execution environments.

.. autoclass:: importspy.validators.runtime_validator.RuntimeValidator
   :members:
   :undoc-members:
   :show-inheritance:
