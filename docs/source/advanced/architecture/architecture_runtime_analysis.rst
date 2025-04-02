architecture_runtime_analysis
=============================

Understanding Runtime Analysis in ImportSpy
-------------------------------------------

ImportSpy doesn’t guess — it **knows exactly who’s importing your code, from where, and how**.

Its runtime analysis engine reconstructs the **real-time execution context** surrounding an import and evaluates whether it complies with the expectations declared in an **Import Contract**.

This section explains how ImportSpy leverages Python's introspection system to **enforce validation dynamically**, across both embedded and CLI modes.

🧠 What Makes ImportSpy Runtime-Aware?
---------------------------------------

At the heart of ImportSpy is a fundamental insight:

> A Python module isn’t just *defined* — it’s *executed in context.*

ImportSpy inspects that context to answer questions like:

- Who is importing this code?
- Is the environment approved (OS, Python version, interpreter)?
- Are expected environment variables and metadata in place?
- Does the runtime architecture match the contract?

Instead of assuming compliance, ImportSpy **validates the reality of execution** — and blocks code that violates it.

🧱 Key Layers of Runtime Analysis
----------------------------------

Here’s how ImportSpy turns Python’s dynamic nature into a validation pipeline:

1️⃣ **Call Stack Introspection**  
   - Uses `inspect.stack()` to trace back to the module attempting the import.
   - Identifies the **caller module**, not just the callee.

2️⃣ **Context Extraction**  
   - Gathers system metadata, including:
     - OS (Linux, macOS, Windows)
     - CPU architecture (e.g. `x86_64`, `arm64`)
     - Python version and interpreter (CPython, PyPy, IronPython)
     - Environment variables (e.g., `API_KEY`, `STAGE`)
     - Installed module structure (classes, functions, globals)

3️⃣ **SpyModel Construction**  
   - Dynamically builds an internal `SpyModel` from the importing context.
   - Matches structure and environment against the import contract.

4️⃣ **Validation Decision**  
   - Compares expected constraints from YAML or Python object.
   - Raises `ValidationError` if mismatches are found — or returns control if all checks pass.

🔍 Core Python Tools Behind the Magic
--------------------------------------

ImportSpy uses only built-in Python modules — no black magic, just introspection:

- `inspect.stack()` – call stack tracing
- `inspect.getmodule()` – resolve module context
- `platform.system()`, `platform.machine()` – OS and architecture
- `sys.version_info`, `platform.python_implementation()` – Python version and interpreter
- `os.environ` – environment variable resolution
- `getmembers()` – dynamic class/function structure extraction

These are the building blocks behind ImportSpy’s runtime truth-checking engine.

⚙️ Embedded vs External Mode: Runtime Differences
--------------------------------------------------

| Mode            | Validated Context          | Typical Use Case                                  |
|-----------------|----------------------------|---------------------------------------------------|
| **Embedded**    | The **importer** of a module | Plugin architectures, sandbox validation           |
| **External**    | The **module itself**        | CI pipelines, security audits, pre-release checks  |

Both modes rely on the **same runtime model**, but invert the direction of validation.

✅ Embedded Mode Example:
- `my_plugin.py` calls `import core_module.py`
- Inside `core_module`, validation ensures `my_plugin` is allowed to import it.

✅ CLI Mode Example:
- You run `importspy -s contract.yml my_plugin.py`
- ImportSpy checks if `my_plugin` complies with its declared structure and runtime constraints.

🚀 Why Runtime Analysis Changes the Game
-----------------------------------------

ImportSpy’s runtime model enables features few tools can offer:

- **Import-time contract enforcement** — with precise control over OS, interpreter, architecture
- **Real context validation** — no assumptions, just introspection
- **Full plugin safety** — modules can reject untrusted importers
- **CI/CD guarantees** — validate module deployment conditions at build time

Python’s flexibility is often seen as a liability — ImportSpy turns it into an *auditable gate*.

⚡ Performance Considerations
-----------------------------

Runtime analysis has a cost — but ImportSpy minimizes it through:

- **Lazy evaluation** — modules are only analyzed when loaded
- **Context caching** — previously computed SpyModels are reused
- **Selective enforcement** — system modules are skipped unless explicitly targeted

Validation takes milliseconds, not seconds — even in dynamic plugin workflows.

🔐 Final Takeaway
------------------

ImportSpy’s runtime analysis engine turns **introspection into validation**.

By deeply understanding **who is importing what, from where, and under which conditions**, ImportSpy enforces:

✅ Structural correctness  
✅ Environmental compliance  
✅ Runtime safety — across interpreters, containers, and pipelines

Whether you’re building a plugin system, securing a package, or hardening your CI,  
ImportSpy gives you the tools to **intercept, introspect, and enforce — right at import time.**

Next:
- :doc:`architecture_validation_engine` → See how the validator pipeline executes
- :doc:`architecture_design_decisions` → Understand the rationale behind ImportSpy’s runtime-first approach
