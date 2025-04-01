CI/CD Integration with ImportSpy
================================

Ensuring the reliability and stability of software throughout the development lifecycle  
is a fundamental challenge, particularly in modern **Continuous Integration and Continuous Deployment (CI/CD)** pipelines.  
Automated workflows streamline software validation, testing, and deployment,  
but they also introduce the risk of **dependency drift**, uncontrolled module updates,  
and environmental discrepancies that can **compromise stability**.

ImportSpy strengthens CI/CD pipelines by enforcing **strict import contract compliance**  
on external dependencies, module structures, and runtime configurations.  
By integrating ImportSpy within CI/CD automation, development teams can ensure  
that all imported modules remain **predictable, validated, and structurally sound**  
across different execution environments.

Why Import Contract Enforcement Matters in CI/CD
------------------------------------------------

One of the biggest risks in CI/CD workflows is **dependency unpredictability**.  
A module that functions correctly in a **local development environment**  
may fail during **testing or production** due to:

- Differences in **Python versions** and **runtime interpreters**.
- System architecture variations between environments.
- Missing **environment variables or system dependencies**.
- **Unapproved modifications** to third-party dependencies.

These discrepancies can cause **silent failures** that are difficult to detect  
until software is already deployed. Traditional testing approaches focus on  
**functional correctness** but often lack mechanisms to enforce  
**structural validation and execution consistency**.

ImportSpy solves this problem by introducing **automated import contract enforcement**  
throughout the **CI/CD pipeline**, preventing breaking changes from propagating unnoticed.

How ImportSpy Enhances CI/CD Workflows
--------------------------------------

When integrated into a CI/CD workflow, ImportSpy performs continuous validation  
of external modules against their declared **import contracts (YAML files)**.  
This guarantees compliance with execution constraints and structural expectations.

**1. Validation During the Build Phase**

- Before packaging, ImportSpy ensures that the module structure complies with its import contract.
- Prevents broken imports, missing attributes, or incompatible methods from progressing.

**2. Enforcing Compliance During Testing**

- ImportSpy validates each module’s structure and environment during automated testing.
- Structural mismatches or unexpected mutations are detected early and reported clearly.

**3. Final Verification Before Deployment**

- Before pushing to production, ImportSpy ensures every module and its environment match the expected constraints.
- This minimizes the risk of post-deployment failures caused by misconfigurations.

CI/CD-Compatible CLI Integration
--------------------------------

ImportSpy includes a CLI tool specifically designed for integration in scripted pipelines:

.. code-block:: bash

    importspy -s spymodel.yml -l ERROR path/to/module.py

This command validates a module (`module.py`) against the constraints declared in `spymodel.yml`,  
reporting errors and halting the pipeline if the module does not comply.

It supports:
- Custom log levels (`DEBUG`, `INFO`, `WARNING`, `ERROR`)
- Absolute or relative module paths
- YAML import contracts

Compatible With All CI/CD Architectures
---------------------------------------

ImportSpy can be easily added to common CI/CD tools like GitHub Actions, GitLab CI, CircleCI, and Jenkins:

- **Dockerized Workflows** 🐳  
  Validate contract compliance before finalizing images.

- **Kubernetes Pipelines** ☸️  
  Enforce structure validation on startup containers or batch jobs.

- **Legacy or VM-Based Pipelines** 🖥️  
  Prevent configuration drift between test, staging, and prod environments.

Because ImportSpy runs lightweight validations without modifying the Python interpreter,  
it introduces **no runtime overhead**, making it ideal for automated pipelines.

Improving Security & Deployment Trust
-------------------------------------

ImportSpy helps protect your software supply chain by:

- Blocking unauthorized modules.
- Detecting tampered packages.
- Verifying runtime expectations.

It complements security tools like dependency scanners by **verifying behavior and structure**,  
not just known vulnerabilities.

Summary
-------

By integrating ImportSpy into CI/CD workflows, teams gain:

- **Structural validation at every stage**
- **Early detection of breaking changes**
- **Consistency across multiple environments**
- **Security through import contract enforcement**

This leads to more reliable deployments, reduced downtime, and confidence that  
each software artifact behaves as expected in every runtime context.

To learn how to define import contracts, see :doc:`contract_structure`.  
