External Mode
=============

Overview
--------

In **external mode**, ImportSpy acts as a **standalone validator**, allowing you to  
check the integrity and correctness of a Python module **from the outside**,  
without embedding any validation logic within the module itself.

The core idea is to use a YAML-based file (called an **import contract**)  
to describe the structural and runtime expectations for a target module,  
and then validate it **before executing** any business logic.

This mode is ideal for:

- Plugin or extension validation
- Pre-deployment checks in CI/CD pipelines
- Security auditing of third-party modules
- Runtime enforcement for framework-based architectures

How It Works
------------

1. Define the **import contract** (`spymodel.yml`) for the module you want to validate.
2. Run the ImportSpy CLI tool with the path to the module and contract.
3. ImportSpy loads the module, extracts its metadata, and compares it against the contract.
4. If validation fails, execution is blocked and detailed errors are shown.

Usage Example
-------------

To validate a Python module using an external contract:

.. code-block:: bash

    importspy -s spymodel.yml -l DEBUG extension.py

This command:

- Uses `spymodel.yml` as the import contract.
- Runs the validation with `DEBUG` log verbosity.
- Validates the module `extension.py`.

CLI Reference
-------------

.. code-block:: text

    Usage: importspy [OPTIONS] [MODULEPATH]

    CLI command to validate a Python module against a YAML-defined import contract.

    Arguments:
      modulepath            Path to the Python module to load and validate.

    Options:
      --version, -v               Show the version and exit.
      --spymodel, -s TEXT         Path to the import contract file (.yml). [default: spymodel.yml]
      --log-level, -l [DEBUG|INFO|WARNING|ERROR]
                                  Log level for output verbosity.
      --install-completion        Install shell completion.
      --show-completion           Show shell completion snippet.
      --help                      Show this message and exit.

Execution Flow
--------------

The external validation process involves:

1. **Parsing the import contract** (YAML → SpyModel)
2. **Loading the target module dynamically**
3. **Extracting its structure, classes, functions, variables**
4. **Reading runtime info (OS, Python version, interpreter, etc.)**
5. **Validating the actual metadata against contract rules**
6. **Raising an exception if violations are found**

This guarantees that the module complies with strict runtime and structural expectations.

Best Practices
--------------

- Keep import contracts under version control
- Validate before execution, not after
- Use in automated CI pipelines or manual audits
- Structure contracts clearly using :doc:`contract_structure`

Related Topics
--------------

- :doc:`contract_structure` – Detailed YAML schema and contract rules
- :doc:`spy_execution_flow` – Full validation lifecycle explanation
- :doc:`embedded_mode` – For modules that validate their importers from within
