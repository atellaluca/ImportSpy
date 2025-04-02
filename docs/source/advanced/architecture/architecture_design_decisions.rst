Design Principles Behind ImportSpy
==================================

ImportSpy was built to answer a fundamental question in dynamic Python environments:

🔐 *"How can we guarantee that modules are imported only under the conditions they were designed for?"*

Unlike traditional linters or static analyzers, ImportSpy enforces **live structural contracts** at the moment of import. This section details the architectural decisions that enable ImportSpy to operate securely, predictably, and scalably across both **runtime validation** and **automated pipelines**.

Why Runtime Validation? 🧠
--------------------------

Python is dynamic. That’s its strength—and its risk.

Most tools operate **before execution** (e.g. `mypy`, `flake8`), but these tools can’t:

- Detect runtime-only configurations (e.g. `os.environ`, `importlib`).
- Block a plugin from loading in an unauthorized host.
- Enforce interpreter or architecture constraints **at runtime**.

✨ **ImportSpy validates code *as it’s being imported***—right where behavior matters.  
It defers enforcement to the **moment of execution**, where guarantees can be *proven*.

Why Validate the Importing Environment? 🔄
------------------------------------------

ImportSpy inverts the typical validation direction.

Instead of saying:

> “This plugin must look like X.”

It asks:

> “Is the context trying to use this plugin *safe enough* to do so?”

Modules don’t just exist—they **run somewhere**.  
By inspecting the **caller**, ImportSpy ensures:

- Plugins are loaded only in verified systems.
- The host respects the structure, env vars, interpreter, etc.
- No unauthorized module can silently consume sensitive logic.

📌 **This is fundamental to plugin security, cross-runtime compliance, and containerized deployments.**

Why Declarative Import Contracts? 📜
------------------------------------

Validation logic shouldn’t live inside Python files.

Instead, ImportSpy uses **external YAML contracts** that describe:

- Expected runtime constraints (e.g. `os: linux`, `python: 3.12`)
- Structural contracts (functions, classes, attributes)
- Deployment variation (e.g. different rules for Windows vs Linux)

These contracts are parsed into a runtime `SpyModel`—an internal abstraction built with Pydantic.

Benefits:

- ✅ Easy to version
- ✅ Works across both embedded and CLI validation
- ✅ Enables testing, linting, and reuse
- ✅ No invasive logic in the codebase

Why Python Introspection? 🔍
----------------------------

ImportSpy is powered by Python’s built-in runtime introspection features:

- `inspect.stack()` to find the caller
- `getmembers()`, `isfunction()`, `isclass()` to rebuild module structure
- `sys`, `platform`, and `os` to gather system metadata

This allows ImportSpy to:

- Mirror the structure of any module
- Dynamically analyze real-time execution state
- Validate *what’s really there*—not what’s assumed

By using native reflection instead of static assumptions, ImportSpy gains **flexibility and truthfulness**.

Why Two Validation Modes? ⚙️
-----------------------------

ImportSpy supports two usage models:

### 1. Embedded Mode (Validation from inside the module)

- Great for plugins and reusable components
- Self-protecting modules: reject imports from unverified hosts
- Guarantees runtime safety at every import

### 2. External Mode (Validation from CI/CD or CLI)

- Ideal for pre-deployment validation
- Works well in test automation, pipelines, and secure releases
- Ensures modules are structurally valid before execution

Both use the same contract schema.  
Both use the same engine.  
Both improve trust.

Why Block on Failure? 🚫
------------------------

ImportSpy adopts a **zero-trust default**:

- ❌ Invalid environment? → Raise `ValidationError`
- ❌ Mismatched structure? → Abort import
- ✅ Fully compliant? → Proceed as normal

This prevents:

- Unexpected side effects
- Code being “partially valid”
- Runtime surprises in production

Errors are detailed, categorized, and explain *what failed, where, and why*.

Performance Tradeoffs & Optimizations 🧮
----------------------------------------

Runtime validation adds overhead. But ImportSpy minimizes it through:

- 🧠 **Caching** of introspection results
- 🔍 **Selective analysis** (skip unused layers)
- 🧱 **Lazy evaluation** of module components
- 📉 **Short-circuiting** at first contract breach

Result: validation is fast enough for real-time enforcement—even inside plugins.

Core Design Principles 🧭
--------------------------

These ideas guide ImportSpy’s architecture:

- **Declarative-first** – Let contracts define validation, not Python logic.
- **Zero-trust imports** – Always verify before executing.
- **Context-aware validation** – Enforce structure *and* environment.
- **Cross-environment readiness** – Design for CI, containers, local, and cloud.
- **Developer ergonomics** – Errors are clear. Contracts are readable. Setup is fast.

Next Steps 🔬
-------------

To see these principles in action:

- Dive into :doc:`architecture_runtime_analysis` → How runtime environments are captured
- Or explore :doc:`architecture_validation_engine` → How actual validation decisions are made
