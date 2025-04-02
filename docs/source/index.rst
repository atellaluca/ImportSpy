Welcome to ImportSpy 🔎
========================

**ImportSpy** is a contract-based runtime validation framework that transforms how Python modules interact—making those interactions **predictable, secure, and verifiable**.  
It empowers developers to define, enforce, and validate **import contracts** that describe exactly how a module should behave when it is imported, under specific runtime conditions.

Whether you're working with **plugin-based systems**, **microservices**, or **cross-platform applications**, ImportSpy gives you **full control over integration boundaries**.  
It ensures that the modules importing your code—or the ones you're importing—adhere to **explicit structural and environmental rules**, avoiding silent failures, runtime crashes, or unpredictable behavior.

🔐 ImportSpy is not just about validation—it’s about **bringing discipline and clarity to the most dynamic part of Python: the import system**.

Why ImportSpy? 🚀
------------------

- **🧩 Bring Structure to Dynamic Systems**  
  Enforce well-defined contracts on imported modules: classes, methods, variables, versions, OS, interpreters, and more.
  
- **🔍 Runtime-Aware Validation**  
  Validate modules **based on actual runtime context**—OS, CPU architecture, Python interpreter, and version.

- **🔌 Built for Plugin Ecosystems**  
  Protect core logic from integration errors in environments where dynamic loading is common.

- **🧪 Two Powerful Modes**  
  In **embedded mode**, validate external modules *that import your code*, enforcing structure and context dynamically.  
  In **CLI mode**, validate any Python module against a contract—ideal for CI/CD pipelines and automated checks.

- **📜 Self-Documenting Contracts**  
  The `.yml` contract files double as **live documentation**, formalizing how modules are expected to behave.

What You'll Learn From This Documentation 📖
--------------------------------------------

This guide is designed to help you:

- Understand how ImportSpy works and **why it exists**
- Learn how to **define and apply import contracts**
- Explore **real-world use cases** across validation, compliance, CI/CD, security, and IoT integration
- Navigate through **beginner-friendly training material** that introduces reflection, Pydantic, Poetry, and more
- Dive into the **internals** of ImportSpy with detailed API references and architectural insights
- Discover how to **support or sponsor the project** to help it grow

How to Navigate This Documentation 🧭
-------------------------------------

- **👋 New to ImportSpy?** → Start with **Get Started** to see how it works, step by step.
- **📚 Want to understand the bigger picture?** → Visit the **Overview** section to explore the vision, story, and use cases.
- **🧠 Curious about internals?** → Explore **Advanced Documentation** for architecture, runtime analysis, and API design.
- **🎓 Need a learning space?** → Head to the **Beginner Section** to explore tools and practices relevant to ImportSpy.
- **💼 Interested in supporting ImportSpy?** → Visit the **Sponsorship** section to learn how to get involved.

Let’s build Python software that’s not just flexible, but also **reliable, validated, and future-proof**.  
**Welcome to the new standard for structural integration in Python.**

.. toctree::
   :maxdepth: 2
   :caption: 📌 Core Documentation

   vision
   overview
   get_started
   sponsorship

.. toctree::
   :maxdepth: 2
   :caption: 🎓 Beginner Resources

   beginner/beginner_index

.. toctree::
   :maxdepth: 2
   :caption: 🧠 Advanced Topics

   advanced/advanced_index
