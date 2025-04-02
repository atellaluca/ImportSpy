CI/CD Integration
=================

Modern CI/CD pipelines are powerful — but also fragile.

Between dynamic environments, dependency drift, and plugin chaos,  
it’s easy for code to pass local tests and **still fail at runtime**.

ImportSpy brings a layer of **predictability, structural assurance**, and **contract enforcement**  
to your automated workflows — making sure that every module behaves the way it should,  
in the environment where it’s going to run.

Why CI/CD Needs Structural Validation
-------------------------------------

Functional tests catch **what your code does**.  
ImportSpy ensures that it’s **running in the right place, with the right structure**.

Without structural validation, pipelines are vulnerable to:

- ❌ Hidden mismatches in **Python versions**, **interpreters**, or **platforms**  
- ❌ Missing or malformed **environment variables**  
- ❌ Untracked changes in shared modules or plugins  
- ❌ Non-compliant third-party code with unexpected APIs

These failures often appear **late**, when debugging is slow and costly.  
ImportSpy helps you catch them **early**, at build time — not post-deploy.

Where to Use ImportSpy in CI/CD
-------------------------------

**1. During the Build Phase 🧱**

Validate module structure before packaging:

.. code-block:: bash

   importspy -s spymodel.yml mymodule.py

This prevents broken contracts from ever making it into an artifact.

**2. During Testing 🔬**

Add ImportSpy validation before or alongside your unit tests:

.. code-block:: bash

   importspy -s spymodel.yml -l ERROR path/to/module.py

Catch unexpected mutations, missing methods, or API drift as part of CI.

**3. Before Deployment 🚀**

Use ImportSpy to verify:

- Environment constraints (OS, Python, interpreter)  
- Runtime assumptions (env vars, module-level variables)  
- Plugin compliance across distributed services

✅ If everything matches the contract, continue.  
❌ If anything is wrong, block the deploy.

Supported CI/CD Platforms
--------------------------

ImportSpy is CI-native and works anywhere:

- **GitHub Actions**  
  Add a step before your test matrix or deployment job.

- **GitLab CI**  
  Use it in before_script or as a job stage.

- **CircleCI / Jenkins**  
  Run via shell or Python-based jobs.

- **Docker / Kubernetes**  
  Validate plugins or runtime images before deployment.

- **Legacy or VM pipelines**  
  Enforce stability even in less dynamic stacks.

Minimal Example for GitHub Actions
----------------------------------

.. code-block:: yaml

   - name: Validate Plugin
     run: |
       pip install importspy
       importspy -s spymodel.yml extension.py

Any contract violations will raise a `ValueError` and halt the build.

Security Benefits
------------------

ImportSpy also strengthens your **software supply chain**:

- Blocks unexpected or tampered code  
- Prevents unauthorized plugin registration  
- Confirms that runtime conditions are exactly what you expect  
- Complements tools like `pip-audit`, `bandit`, or SAST engines

Think of it as **import-time policy enforcement**, directly in your build.

Best Practices for Integration
------------------------------

- 🔐 Treat ImportSpy as a **quality gate**, not just a linter  
- 💥 Use `-l ERROR` log level to fail fast and get clear diagnostics  
- 🔁 Keep contracts under version control with your code  
- 🧪 Validate early, not just at release  
- 🧭 Use strict contracts in production, relaxed ones in dev/test

Related Topics
--------------

- :doc:`contract_structure` – How to write import contracts  
- :doc:`external_mode` – Running validation externally  
- :doc:`spy_execution_flow` – See what happens during validation

Summary
-------

ImportSpy turns fragile CI pipelines into **predictable safety systems**.

It guarantees that:

- ✅ Every module is structurally sound  
- ✅ Every environment matches your expectations  
- ✅ Every build is trustworthy

No more surprises. No more silent regressions.  
Just clean, validated, future-proof Python — every time you deploy.
