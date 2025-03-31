===========================
Core Components of ImportSpy
===========================

The **core components of ImportSpy** define its internal architecture for  
**validation logic**, **logging**, **contract parsing**, and **global configuration**.

These components are the backbone of ImportSpy’s enforcement engine,  
ensuring that every module validated — whether internally or via CLI —  
follows strict rules for structure, context, and runtime integrity.

Spy Class 🕵️‍♂️
----------------
The `Spy` class is **the primary controller** of ImportSpy.

It manages the full validation flow, including:

- Receiving external modules (from within code or via CLI)
- Configuring logging levels dynamically
- Coordinating contract parsing and validation against loaded modules
- Detecting recursion or misuse during introspection

.. autoclass:: importspy.s.Spy
   :members:
   :undoc-members:
   :show-inheritance:

Import Contracts & Parsers 💾
-----------------------------

ImportSpy supports **declarative validation** through **import contracts** —  
simple `.yml` files that define expected module structure, variables, classes,  
functions, and runtime environments.

To work with these contracts, ImportSpy uses a **pluggable parser interface**.  
Currently, YAML is the default and only supported format, but the architecture  
is designed to support future extensions (e.g. JSON, TOML).

The `Parser` abstract class defines the core methods required for a new format backend,  
while `YamlParser` provides a production-ready YAML implementation.

This parser is also what powers ImportSpy’s **CLI and pipeline validation**,  
allowing contracts to be injected externally without modifying the validated code.

.. autoclass:: importspy.persistences.Parser
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: importspy.persistences.YamlParser
   :members:
   :undoc-members:
   :show-inheritance:

The `handle_persistence_error` decorator is applied to persistence methods  
to catch and raise consistent, user-friendly errors when contract files  
are missing, unreadable, or malformed.

.. autofunction:: importspy.persistences.handle_persistence_error

.. autoclass:: importspy.persistences.PersistenceError
   :members:
   :undoc-members:
   :show-inheritance:

LogManager Class 📝
-------------------
The `LogManager` handles all log collection and formatting for ImportSpy.  
It ensures consistent output whether validation is performed in code,  
from a CLI command, or inside CI/CD pipelines.

Every validation step — including configuration, parsing, and inspection —  
is logged in real time, supporting both debugging and auditability.

.. autoclass:: importspy.log_manager.LogManager
   :members:
   :undoc-members:
   :show-inheritance:

Errors Class ⚠️
---------------
The `Errors` class centralizes **standardized error messages**  
used throughout ImportSpy’s validation process.

By consolidating messages here, ImportSpy ensures clear, structured feedback  
for every type of violation or inconsistency found during validation.

.. autoclass:: importspy.errors.Errors
   :members:
   :undoc-members:
   :show-inheritance:

Constants Class 📌
------------------
This class contains all **shared constants** used in ImportSpy —  
from validation rules and labels to keys used in contracts.

It keeps configuration consistent across internal modules and user-defined extensions.

.. autoclass:: importspy.constants.Constants
   :members:
   :undoc-members:
   :show-inheritance:

Config Class ⚙️
---------------
The `Config` class defines **global runtime settings** for ImportSpy.  
It governs how validation is executed, what options are active,  
and allows advanced users to tailor ImportSpy’s behavior  
for different environments or modes.

.. autoclass:: importspy.config.Config
   :members:
   :undoc-members:
   :show-inheritance:
