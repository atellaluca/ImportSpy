Core Engine: Classes, Controllers, and Contracts
================================================

This section documents the **core subsystems of ImportSpy** — the internal machinery that powers its runtime validation engine, CLI interface, and contract execution model.

These APIs are essential for:

- 🧠 Understanding how validation requests are orchestrated  
- 🔄 Hooking into the enforcement lifecycle  
- 🛠 Extending ImportSpy for custom validation, logging, or policy enforcement  

Each class below plays a **central role in ImportSpy’s internal flow**, and is fully documented for integration and contribution use cases.

Spy Class 🕵️‍♂️
^^^^^^^^^^^^^^^^^

The `Spy` class is the **central controller** of ImportSpy’s validation pipeline.

It handles:

- Contract parsing and validation  
- Import-time introspection of the calling environment  
- Runtime orchestration for embedded validation  
- Entry point for dynamic execution enforcement

.. autoclass:: importspy.s.Spy
   :members:
   :undoc-members:
   :show-inheritance:

Contract Parsers 💾
^^^^^^^^^^^^^^^^^^^^

Import contracts are defined externally as `.yml` files and parsed into structured models.

- `Parser` is the abstract interface that defines contract loading behavior.  
- `YamlParser` is the default parser implementation supporting YAML-based contracts.  
- `handle_persistence_error` is a decorator for consistent exception wrapping and traceability.

.. autoclass:: importspy.persistences.Parser
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: importspy.persistences.YamlParser
   :members:
   :undoc-members:
   :show-inheritance:

.. autofunction:: importspy.persistences.handle_persistence_error

.. autoclass:: importspy.persistences.PersistenceError
   :members:
   :undoc-members:
   :show-inheritance:

Log Manager 📝
^^^^^^^^^^^^^^^

The `LogManager` provides **structured logging** across both CLI and embedded modes.  
It supports log-level control (`DEBUG`, `INFO`, `ERROR`, etc.) and unified message formatting.

.. autoclass:: importspy.log_manager.LogManager
   :members:
   :undoc-members:
   :show-inheritance:

Error Messaging ⚠️
^^^^^^^^^^^^^^^^^^^^

The `Errors` class contains standardized error templates used across ImportSpy.  
It defines **consistent, user-facing messages** for contract violations, misconfigurations, and environment mismatches.

.. autoclass:: importspy.errors.Errors
   :members:
   :undoc-members:
   :show-inheritance:

Constants 📌
^^^^^^^^^^^^

All shared constants, labels, and tags used by the validation engine, parsers, and CLI.  
These are used to maintain **naming consistency** across internal modules.

.. autoclass:: importspy.constants.Constants
   :members:
   :undoc-members:
   :show-inheritance:

Configuration ⚙️
^^^^^^^^^^^^^^^^

The `Config` class defines **runtime settings and execution context** for ImportSpy.

It allows developers to:

- Customize behavior based on validation mode  
- Register external contract paths  
- Modify enforcement flags dynamically

.. autoclass:: importspy.config.Config
   :members:
   :undoc-members:
   :show-inheritance:
