Understanding ImportSpy 🔍
==========================

Welcome to the **technical heart** of ImportSpy.

This section provides a full breakdown of how ImportSpy works,  
why it matters in modern modular architectures, and how you can harness its full potential.

ImportSpy isn’t just a utility — it’s a **runtime contract enforcement framework**.  
It brings validation to the import system by ensuring that external modules conform to **predefined structural rules and runtime constraints**.  
Whether used in embedded or CLI mode, ImportSpy guarantees **predictability, security, and compliance** before code ever runs.

Why This Section Matters ⚠️
----------------------------

Modern systems are complex.  
You rely on dynamically loaded modules, plugins, APIs, microservices — often across multiple environments.

But with this flexibility comes risk:

- Missing or incompatible methods, attributes, or classes  
- Subtle mismatches in Python versions, OS, or interpreters  
- Unexpected behavior caused by configuration drift or structural divergence  
- Modules that silently break contracts and cause late-stage failures

ImportSpy intercepts these issues **before execution**, making validation **a first-class citizen** of your architecture.

What You’ll Learn Here 📘
--------------------------

This section guides you through ImportSpy’s internals, starting from high-level concepts to runtime execution flow:

- :doc:`understanding_importspy/introduction`  
  A clear introduction to ImportSpy’s core mission and use cases.

- :doc:`understanding_importspy/defining_import_contracts`  
  Learn how to describe structural and environmental expectations through YAML contracts.

- :doc:`understanding_importspy/contract_structure`  
  Understand the schema and semantics of a well-formed import contract.

- :doc:`understanding_importspy/spy_execution_flow`  
  Discover how ImportSpy intercepts imports and validates modules in real time.

- :doc:`understanding_importspy/embedded_mode`  
  Explore how modules can protect themselves by validating their importers at runtime.

- :doc:`understanding_importspy/external_mode`  
  Understand CLI-based validation and its role in automation, CI/CD, and review pipelines.

- :doc:`understanding_importspy/validation_and_compliance`  
  Dive into the validation engine and what it checks (types, names, annotations, OS, versions, etc).

- :doc:`understanding_importspy/error_handling`  
  See how ImportSpy produces actionable, clear error messages when something doesn’t match.

- :doc:`understanding_importspy/integration_best_practices`  
  Apply ImportSpy cleanly in real projects — plugins, microservices, libraries, or secure APIs.

- :doc:`understanding_importspy/ci_cd_integration`  
  Integrate ImportSpy into your continuous delivery pipeline for automated contract enforcement.

Who This Is For 👨‍💻👩‍💻
---------------------------

This section is written for:

- **Developers** using ImportSpy in plugin-based or multi-module Python apps  
- **Architects** designing extensible, contract-driven software systems  
- **DevOps and Security Engineers** aiming to validate runtime boundaries and block unknowns  
- **Open Source Maintainers** who want to ensure compatibility across environments

Ready to see how ImportSpy works under the hood?  
Let’s explore the architecture that makes dynamic imports deterministic.

.. toctree::
   :maxdepth: 2
   :caption: Understanding ImportSpy:

   understanding_importspy/introduction
   understanding_importspy/defining_import_contracts
   understanding_importspy/contract_structure
   understanding_importspy/spy_execution_flow
   understanding_importspy/embedded_mode
   understanding_importspy/external_mode
   understanding_importspy/validation_and_compliance
   understanding_importspy/error_handling
   understanding_importspy/integration_best_practices
   understanding_importspy/ci_cd_integration
