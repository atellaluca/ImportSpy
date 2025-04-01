Best Practices for Integrating ImportSpy
========================================

Effectively integrating ImportSpy into a Python project requires a **structured approach** that promotes clarity, maintainability, and reliable execution across environments. ImportSpy acts as a **validation layer**, and its effectiveness depends on how well **import contracts** (defined as `.yml` files) are designed and managed.

A well-written contract should be:

- **Readable** – Easy to understand for developers and maintainers.
- **Scalable** – Adaptable as new environments and dependencies are introduced.
- **Maintainable** – Structured to minimize duplication and maximize reuse.

By applying the following best practices, teams can leverage ImportSpy without adding unnecessary overhead or complexity.

Designing Modular Import Contracts 🧱
-------------------------------------

Avoid creating monolithic `.yml` files that mix unrelated validation logic.  
Instead, adopt a modular design that reflects the architecture of the system:

- **Separate deployment scenarios** into distinct `deployments:` blocks.
- **Define runtime conditions independently** – such as `os`, `architecture`, and `interpreter`.
- **Avoid repetition** by reusing common configurations where possible.

This approach allows you to manage contracts that cover:

- Multiple environments (CI, production, staging).
- Platform variations (Windows, Linux, ARM, x86_64).
- Python runtime variations (e.g., CPython, PyPy).

Structuring the Contract Hierarchically 🏗️
-------------------------------------------

Each import contract can express nested constraints:

1. **Module metadata** (`filename`, `version`, `variables`).
2. **Classes**, each with:
   - `attributes`
   - `methods`
   - `superclasses`
3. **Deployments**, each with:
   - `arch`
   - List of `systems`, each having:
     - `os`
     - `envs` (environment variables)
     - List of `pythons`, each specifying:
       - `version`
       - `interpreter`
       - List of nested `modules` (re-validating structure at runtime)

This structure ensures that validation logic **mirrors the real-world deployment hierarchy**.

Maintaining Runtime Relevance ⚙️
--------------------------------

An import contract must reflect **real, expected runtime conditions**. Don’t hardcode constraints that don't match how your software is actually deployed.

- In **CI pipelines**, allow flexibility but check for critical dependencies.
- In **production**, apply strict runtime enforcement (exact interpreter, architecture, env vars).
- Avoid assumptions about the host system unless explicitly controlled.

Keep your contracts versioned and updated alongside the modules they describe.

Avoiding Duplication 🔄
------------------------

Don’t repeat validation logic across contracts. If multiple modules share the same environment or runtime expectations:

- Define shared `deployments:` entries that are reused.
- Use templating tools or contract generators if necessary.
- Extract shared constraints into include-able components.

This makes the contracts easier to maintain and minimizes the risk of inconsistencies.

Validating External Environments 🌍
------------------------------------

ImportSpy is ideal for validating that modules are not imported in environments that lack:

- Required OS and architecture.
- Critical `envs` (e.g., `DATABASE_URL`, `PLATFORM_KEY`).
- Specific Python versions or interpreter types.

**Declare these explicitly** in the `deployments:` section. This ensures consistent behavior in:

- Local development environments.
- Docker containers.
- Cloud-based runtimes.
- Virtual environments or remote builds.

Enforcing Consistency Through CI/CD 🧪
--------------------------------------

Integrate ImportSpy checks early in your testing pipeline:

- Run ImportSpy as a **validation step before tests**, using the CLI:

  .. code-block:: bash

     importspy -s spymodel.yml -l DEBUG mymodule.py

- Fail fast if contract validation fails.
- Log mismatches and mismatched environments explicitly.
- Combine with other linting, testing, and build tools.

This ensures that structural issues are caught **before deployment**.

Matching ImportSpy to Team Workflows 👥
---------------------------------------

Choose how to handle contract violations depending on your risk profile:

- **Strict mode**: Block execution entirely if violations occur (default behavior).
- **Debug mode**: Use `--log-level DEBUG` to trace execution without stopping.
- **Warning-only mode**: (Coming soon) Log issues without raising exceptions.

Teams should treat ImportSpy as part of their **software quality gate**, customizing its usage across development, staging, and production environments.

Final Thoughts 🔚
------------------

ImportSpy is not a replacement for tests or linters — it is a **complementary layer** that ensures modules are **only executed in environments where they’re guaranteed to behave as expected**.

To get the most out of ImportSpy:

- Keep your import contracts clean, hierarchical, and runtime-aware.
- Integrate validation checks into CI/CD pipelines.
- Use strict enforcement for high-assurance deployments.
- Update contracts alongside your codebase.

By following these best practices, ImportSpy becomes a **predictability enabler** in modern Python software — enforcing not just what your code does, but **where and how it can run safely**.
