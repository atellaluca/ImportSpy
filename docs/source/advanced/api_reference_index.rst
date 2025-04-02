api_reference_index
===================

API Reference: Internals & Extensibility
----------------------------------------

This section provides a **complete reference guide** to ImportSpy's internal API — designed for developers and contributors who want to:

- 🔍 Understand how ImportSpy operates under the hood  
- 🛠️ Extend its validation logic with custom models and validators  
- ⚙️ Integrate runtime enforcement into existing architectures  

Whether you're writing plugins, debugging structural mismatches, or integrating ImportSpy into a CI/CD pipeline, this reference exposes all the essential **building blocks** behind the framework.

🧩 What You'll Find Inside
---------------------------

🔹 **Core API**  
   The runtime logic powering ImportSpy’s contract enforcement.  
   Includes import interceptors, validation orchestration, and execution gating.

🔹 **Model Layer**  
   Formal Pydantic-based representations of everything from modules and attributes  
   to Python interpreters, environments, and deployment matrices.

🔹 **Utility Layer**  
   Introspection helpers for analyzing imports, resolving dependencies,  
   reading metadata, or reflecting on runtime state.

📚 Each module in this section is fully documented with:
- Class definitions  
- Method signatures  
- Expected behavior  
- Extension guidance  
- Real-world usage examples  

.. toctree::
   :maxdepth: 2
   :caption: API Modules

   api_reference/api_core
   api_reference/api_models
   api_reference/api_utilities

🧠 Use this reference to go beyond configuration — and shape ImportSpy around your architecture, policies, and execution model.
