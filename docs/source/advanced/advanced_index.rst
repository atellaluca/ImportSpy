Advanced Topics & Internals of ImportSpy
========================================

Welcome to the advanced section of ImportSpy’s documentation — built for developers, integrators, and contributors who want to **go beyond usage** and dive into **how ImportSpy works under the hood**.

Whether you're building runtime enforcement pipelines, customizing structural validators, or embedding ImportSpy into multi-tenant plugin architectures, this section provides the **deep technical foundation** to unlock ImportSpy's full capabilities.

🧠 Who This Is For
-------------------

- Engineers building **custom validation flows**
- Contributors exploring the **internal mechanics** of ImportSpy
- Teams integrating ImportSpy into **CI/CD, containers, and plugin frameworks**
- Architects enforcing **organization-wide import policies**

🔍 What You’ll Explore
-----------------------

This section is structured into two complementary areas:

🏗️ **Architectural Internals**  
   - A deep technical exploration of ImportSpy’s runtime model, validation stack, and modular design.  
   - Learn how ImportSpy inspects environments, builds validation contexts, and enforces contracts in both embedded and CLI modes.

🛠️ **Extension & Integration Points**  
   - Discover how to write custom validators, extend `SpyModel`, inject runtime policies, or build tooling on top of ImportSpy’s API.  
   - Ideal for integrating with internal frameworks, policy engines, or advanced CI/CD pipelines.

📚 **API Reference**  
   - Browse a fully documented catalog of internal components:
     - `SpyModel`, `Function`, `Attribute`, `Deployment`, `Validator`, etc.
   - Includes type annotations, usage patterns, and extension strategies.

This section balances **low-level documentation** with **real-world extensibility guidance**.

.. toctree::
   :maxdepth: 2
   :caption: Explore the Internals

   architecture_index
   api_reference_index

🚀 Whether you're enforcing security boundaries or writing custom validators, this section is your blueprint for building with — and on top of — ImportSpy.
