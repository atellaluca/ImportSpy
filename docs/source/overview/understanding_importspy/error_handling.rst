Error Handling in ImportSpy
============================

Validation errors are not failures — they are **enforced expectations**.

ImportSpy treats every contract violation as a **signal**, not just a disruption.  
Its error system is designed to be **precise, informative, and traceable**,  
helping developers identify and resolve problems early, consistently, and with confidence.

Why Structured Errors Matter
----------------------------

In complex Python systems, especially those using plugins, microservices, or dynamic loading,  
errors can be vague and hard to reproduce.

ImportSpy solves this by generating:

- 🧠 **Human-readable messages** with contextual hints  
- 🧩 **Categorized errors**, sorted by validation layer  
- 🛠️ **Diagnostic templates** that identify the cause and expected structure  
- 🔎 **Traceable exceptions**, usable in CLI, IDE, or CI pipelines

Whether you’re debugging a failing import or enforcing a strict policy in production,  
ImportSpy makes validation feedback **clear, consistent, and useful**.

Error Categories
-----------------

ImportSpy groups errors into well-defined categories to simplify resolution:

Missing Elements
~~~~~~~~~~~~~~~~

Raised when a required function, class, attribute, or variable is **not present**.

Example:  
`Missing method in class Extension: 'run'`

Type or Value Mismatch
~~~~~~~~~~~~~~~~~~~~~~~

Triggered when types, annotations, or literal values do not match.

Example:  
`Return type mismatch: expected 'str', found 'None'`

Environmental Misconfiguration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Raised when runtime assumptions are unmet, such as:

- Missing environment variables  
- Incompatible OS or interpreter  
- Python version mismatch

Example:  
`Missing required environment variable: API_KEY`

Unsupported Runtime
~~~~~~~~~~~~~~~~~~~

Validation fails if the runtime environment does not match any declared `deployment`.

Example:  
`Unsupported Python version: 3.7. Expected: 3.12.8`

The goal of these categories is to **pinpoint root causes** and prevent regression over time.

Reference Error Table
----------------------

All known validation errors are defined in a centralized table:

.. include:: error_table.rst

Each entry includes:

- A symbolic error constant (e.g., `Errors.CLASS_ATTRIBUTE_MISSING`)  
- A dynamic message template  
- A short description and suggested resolution

These errors are **reused consistently across embedded and CLI validation**.

Enforcement Strategies
-----------------------

ImportSpy enforces contracts in strict mode by default:

Strict Mode (Default)
~~~~~~~~~~~~~~~~~~~~~~

- ❌ Any error raises a `ValueError`  
- ⛔ Execution halts immediately  
- 🔐 Recommended for CI/CD, production, and regulated systems

Soft Mode (Future Feature)
~~~~~~~~~~~~~~~~~~~~~~~~~~

- ⚠️ Errors are downgraded to warnings  
- 🔁 Execution proceeds  
- 🧪 Ideal for development, onboarding, or exploratory validation

Traceability and Debugging
---------------------------

Every raised exception includes:

- The failing **element** (function, class, attribute, etc.)  
- The **context** of the violation (e.g., deployment block or module scope)  
- The **expected vs actual** values/types

Thanks to integrated logging (`LogManager`) and specific exception classes (`ValidationError`, `PersistenceError`),  
ImportSpy ensures traceability across:

- Local debugging  
- Containerized runtimes  
- CI pipelines  
- Logging dashboards

Developer-Focused Feedback
---------------------------

Validation errors are formatted to be helpful across:

- Terminal sessions and shell scripts  
- IDE consoles with embedded validation  
- CI output logs for quality gates or metrics

If you're using ImportSpy in CLI mode, errors are printed with full detail —  
ready to be parsed, logged, or even turned into automated reports.

Best Practices
--------------

- ✅ Run with `--log-level DEBUG` to get full trace on failure  
- ✅ Keep `spymodel.yml` in version control and in sync with module changes  
- ✅ Use error messages as checklists during onboarding or code review  
- ✅ Integrate the error table into your internal docs or linting rules

Errors Are Enforced Contracts
------------------------------

ImportSpy’s validation model is **contract-first** — if a rule is declared, it’s enforced.

That means errors are not just problems — they’re confirmations that the system is working.  
By treating every validation failure as a source of insight, ImportSpy helps your team:

- Identify problems early  
- Understand context clearly  
- Move toward stronger modularity and runtime safety

📌 Errors are not interruptions.  
They are the **boundary where safety begins**.
