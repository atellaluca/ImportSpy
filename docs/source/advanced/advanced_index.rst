Advanced Topics and Internal Architecture
=========================================

ImportSpy is built upon a **robust and extensible architecture** that balances flexibility,  
runtime performance, and deep structural validation. This section is tailored for **advanced developers,  
contributors, and integrators** seeking to explore the inner workings of ImportSpy, extend its behavior,  
or adopt it within custom runtime frameworks and validation layers.

🔬 Unlocking the Full Power of ImportSpy
----------------------------------------

To fully leverage ImportSpy in advanced scenarios—such as **plugin orchestration, dynamic runtime validation,  
cross-environment compatibility enforcement, or CI/CD rule injection**—it’s essential to understand:

🧱 **Architecture Deep-Dive**  
   - Explore the core execution pipeline, including how ImportSpy performs **environment introspection**,  
     dynamically builds the execution model, and enforces import contracts in both **embedded** and **external** modes.

🛠️ **Extending ImportSpy**  
   - Learn how to plug in custom validators, intercept runtime decisions, or inject organization-specific rules  
     through ImportSpy's **modular validator system**.

📚 **API Reference**  
   - A comprehensive, fully documented overview of all **core classes**, **validators**, and **internal models**  
     (like `SpyModel`, `Function`, `Attribute`, etc.), useful for building custom compliance layers or tooling.

Each section offers **practical guidance, annotated examples**, and **advanced customization techniques**  
for integrating ImportSpy into sophisticated development workflows.

.. toctree::
   :maxdepth: 2

   architecture_index
   api_reference_index
