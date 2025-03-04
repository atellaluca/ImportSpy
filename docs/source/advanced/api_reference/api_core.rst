==================
Core Components
==================

The **core components of ImportSpy** define its **validation logic, logging mechanisms,  
error handling, and configuration settings**.  
These classes form the foundation of how ImportSpy **monitors, validates, and enforces compliance**  
when importing external modules.

This section provides an in-depth reference to the **most essential classes** in ImportSpy,  
each playing a **critical role** in module validation and enforcement.

Spy Class 🕵️‍♂️
----------------
The `Spy` class is **the central controller** of ImportSpy.  
It manages **module validation, enforcement rules, and runtime introspection**.

.. autoclass:: importspy.s.Spy
   :members:
   :undoc-members:
   :show-inheritance:

LogManager Class 📝
-------------------
Handles **log collection and reporting**, ensuring that every validation step  
is properly tracked and can be analyzed when debugging or auditing imports.

.. autoclass:: importspy.log_manager.LogManager
   :members:
   :undoc-members:
   :show-inheritance:

Errors Class ⚠️
---------------
Defines standardized **error messages and exception handling**  
for all validation failures, ensuring clarity when something goes wrong.

.. autoclass:: importspy.errors.Errors
   :members:
   :undoc-members:
   :show-inheritance:

Constants Class 📌
------------------
Contains **predefined constants** used across ImportSpy to maintain consistency  
in validation rules, configurations, and compliance checks.

.. autoclass:: importspy.constants.Constants
   :members:
   :undoc-members:
   :show-inheritance:

Config Class ⚙️
---------------
Manages **ImportSpy’s global settings**, defining how validation and enforcement rules  
are applied across different execution environments.

.. autoclass:: importspy.config.Config
   :members:
   :undoc-members:
   :show-inheritance:
