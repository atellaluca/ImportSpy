Models & Validation
===================

ImportSpy structures its **validation and compliance process** through a series of **models and validators**.  
These models define **expected behaviors, structural rules, and runtime constraints** that external modules  
must follow when interacting with a project using ImportSpy.

The **SpyModel** serves as the **blueprint** for module validation, while **validators** enforce  
compliance across different layers of the system.

SpyModel 🏗️
------------
The `SpyModel` class is the **core abstraction** that defines the **expected structure and execution constraints**  
for modules being imported.

- Captures **module structures**, including classes, functions, attributes, and dependencies.
- Defines **execution constraints**, ensuring that modules run only in compatible Python environments.
- Supports **cross-environment validation**, preventing discrepancies between development and production.

.. autoclass:: importspy.models.SpyModel
   :members:
   :undoc-members:
   :show-inheritance:

Validators ✅
------------
ImportSpy includes a set of **validators** that enforce compliance with the **SpyModel**  
and ensure that **imported modules match predefined expectations**.

Each validator plays a specific role, such as:
- **Runtime validation** → Ensuring the correct **Python version and environment**.
- **Structural validation** → Verifying the **presence and consistency** of functions, classes, and attributes.
- **System validation** → Checking that required **dependencies, system variables, and OS constraints** are met.

For an in-depth breakdown of each validator, refer to:

.. toctree::
   :maxdepth: 1

   api_validators
