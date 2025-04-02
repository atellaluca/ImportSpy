Integration Best Practices
===========================

ImportSpy is most powerful when it’s seamlessly integrated into your development lifecycle.  
It acts as a **structural firewall** — ensuring that Python modules are only executed in validated environments,  
with predictable interfaces and runtime guarantees.

To get the most out of ImportSpy, it’s essential to follow practices that promote **clarity, maintainability**,  
and long-term compliance.

Contract Design Principles
---------------------------

A good import contract is:

- 🧠 **Readable** → Easy to understand by developers and reviewers  
- 🔁 **Reusable** → Avoids repetition by isolating shared environments  
- 🔧 **Maintainable** → Easy to update as your system evolves  
- 🎯 **Targeted** → Matches how your code is actually deployed, not just idealized setups

Design your contracts with these goals in mind — and treat them as part of your project’s architecture.

Modularize Your Contracts 🧱
----------------------------

Avoid monolithic `.yml` files with everything mixed together.

Instead:

- Create **separate `deployments:` blocks** for each OS, architecture, or runtime  
- Group constraints based on **real deployment contexts** (e.g., CI, Docker, staging)  
- Keep **top-level structure global**, and specialize deeper in deployment-specific modules  
- Use **baseline declarations** to enforce a minimum structure across all environments

This makes your contracts scalable, and keeps them aligned with your actual execution model.

Match Contracts to Real Environments ⚙️
----------------------------------------

Don't write constraints that don't reflect reality.

- ✅ In production: lock down OS, interpreter, variables, and structure  
- ⚠️ In development: relax constraints slightly for flexibility  
- 🧪 In CI: validate structure early, fail fast, and log everything

ImportSpy’s power comes from accuracy — so your contract should describe **how your code really runs**, not how you wish it did.

Reduce Duplication 🔁
----------------------

Avoid repeating validation rules between modules.

Strategies:

- Define shared `deployments:` blocks and reuse them across multiple contracts  
- Use generation tools to inject common blocks  
- Extract reusable parts (e.g., shared classes or envs) into templated components

Keeping contracts DRY improves maintainability and reduces the chance of silent mismatches.

Structure Contracts Clearly 🏗️
-------------------------------

A recommended hierarchy:

1. `filename`, `version`, and top-level `variables`  
2. `functions` (optional, with argument specs)  
3. `classes`, with:
   - `attributes` (instance/class, with optional types and values)  
   - `methods`, defined like functions  
   - `superclasses`  
4. `deployments`, each with:
   - `arch`, `os`, and optional `envs`  
   - `pythons`, with version/interpreter/modules  
   - `modules`, repeating structure at the environment level if needed

This structure allows deep validation of runtime-specific behavior.

Validate Where It Matters 🌍
----------------------------

ImportSpy is perfect for verifying:

- Plugins or dynamic modules running in cloud or hybrid environments  
- Modules that depend on env-specific config (e.g., secrets, endpoints)  
- Microservices where drift between containers or hosts can break integrations

Explicitly declare:

- OS and architecture  
- Required environment variables  
- Supported Python versions and interpreters

Consistency across environments starts with precise expectations.

Embed ImportSpy in Your Pipeline 🧪
-----------------------------------

Use the CLI tool during CI builds and before deployments:

.. code-block:: bash

   importspy -s spymodel.yml -l DEBUG path/to/module.py

Fail the build if the contract isn't satisfied.  
This catches integration issues **before** they reach staging or production.

Consider combining ImportSpy with:

- Linting (e.g., `ruff`, `flake8`)  
- Typing (e.g., `mypy`)  
- Unit and integration tests  
- Security scanners

ImportSpy adds **structural guarantees** on top of these tools.

Choose Enforcement Mode Strategically 👥
----------------------------------------

ImportSpy supports strict and soft enforcement:

- **Strict Mode** → Violations raise `ValueError`. Use in CI and production.  
- **Debug Logging** → Add `--log-level DEBUG` to trace without halting execution.  
- **Soft Mode** (planned) → Logs validation failures as warnings. Ideal for onboarding or dry runs.

Adapt validation levels to your team's tolerance for risk and your deployment maturity.

Final Advice 🎯
---------------

ImportSpy is not a replacement for testing — it complements it.

It ensures your modules are used **only where and how they’re meant to be**,  
preventing drift, mismatches, and unexpected runtime behavior.

To integrate ImportSpy effectively:

- 📁 Keep contracts clean and modular  
- 🔄 Update them alongside the code they protect  
- ⚙️ Match them to real-world runtimes  
- 🚦 Automate validation in CI/CD  
- 🔐 Use strict enforcement in trusted production pipelines

ImportSpy helps you build **modular, secure, and future-proof Python systems** — one contract at a time.
