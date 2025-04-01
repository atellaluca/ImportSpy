Error Handling in ImportSpy
===========================

Validation failures are inevitable in any dynamic Python environment.  
What makes ImportSpy stand out is its structured, transparent, and developer-friendly approach  
to **reporting and managing validation errors**, ensuring they become actionable steps toward stability—not obstacles.

ImportSpy does not merely detect errors. It classifies, documents, and reports them with precision,  
enabling fast resolution and long-term system compliance.

Structured Validation Feedback
------------------------------

ImportSpy provides highly structured error messages that include:

- **Error category** (e.g., structural, runtime, environmental)
- **Human-readable messages** with contextual information
- **Pre-formatted placeholders** to include names, values, or contracts involved
- **Hints on resolution**, based on best practices and expected module behavior

This makes every error **not just informative**, but also **diagnostic**, helping teams trace  
misalignments, inconsistencies, or violations quickly and accurately.

Error Categories
----------------

ImportSpy classifies validation failures into clear categories:

**Missing Elements**
  Raised when required modules, classes, functions, or attributes are not found.  
  This protects against incomplete implementations or outdated imports.

**Mismatched Types or Values**
  Triggered when a return annotation, argument type, or value does not match expectations.  
  Prevents breaking changes in APIs, especially in shared or inherited code.

**Environment Misconfigurations**
  Raised when expected environment variables are absent or misconfigured.  
  Also applies to version mismatches in interpreters, OS, or dependency layers.

**Runtime and Architecture Errors**
  Raised when the executing environment differs from the allowed runtime constraints:  
  unsupported Python version, OS, or CPU architecture.

Each of these categories helps isolate the nature of the failure and speed up resolution.

Error Table
-----------

All validation errors are documented in a central reference file.

.. include:: error_table.rst

Each entry includes:

- The constant (e.g., `Errors.CLASS_ATTRIBUTE_MISSING`)
- A dynamic template using `.format()`
- Description and suggested fix

These error definitions are raised across ImportSpy's internal validation layers,  
and remain consistent whether running in embedded or external validation mode.

Strict vs Soft Enforcement
--------------------------

ImportSpy supports two primary enforcement strategies:

**Strict Mode (default)**
  - Any validation error raises a `ValueError`
  - Execution halts immediately
  - Best for CI/CD pipelines, secure deployments, and production

**Soft Mode (planned)**
  - Warnings are logged, but execution proceeds
  - Useful for iterative development, onboarding new contracts, or dry runs

This separation allows ImportSpy to adapt to different risk profiles and team preferences.

Debugging and Traceability
--------------------------

Each error message includes enough context to trace:

- Which element failed validation (e.g., `function foo()`)
- Which part of the contract was not satisfied
- Which actual value or type caused the failure

Thanks to centralized logging (via `LogManager`) and custom exceptions (`PersistenceError`, `ValidationError`),  
ImportSpy provides full traceability across the stack—ideal for debugging remote systems,  
containerized environments, or CI runs.

Workflow Integration
--------------------

ImportSpy's errors are designed to surface clearly in:

- Terminal logs
- CI build outputs
- IDE consoles (when embedding ImportSpy in code)

In CLI mode, `ValueError` exceptions are reported with full context and can be parsed programmatically  
to integrate with dashboards or validation gates.

Best Practices
--------------

To avoid repetitive validation failures:

- Always run modules with `--log-level DEBUG` to see full inspection trace
- Keep contracts (`spymodel.yml`) up to date with structural changes
- Start in soft enforcement mode (dev) and escalate to strict mode (prod)
- Use error table as a checklist during integration

Final Notes
-----------

ImportSpy’s error handling system is a critical part of its Zero-Trust execution model.  
It helps development teams:

- Understand failure causes quickly
- Maintain clear and consistent module definitions
- Reduce debugging cycles through clear context
- Adopt proactive validation practices

Errors in ImportSpy are **not interruptions**—they are **contracts being enforced**.
