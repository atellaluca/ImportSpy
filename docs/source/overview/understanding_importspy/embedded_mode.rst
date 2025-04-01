Embedded Mode
=============

In **embedded mode**, ImportSpy is executed *inside* the protected module itself.

This means that a module embeds its own import contract and executes ImportSpy to validate the environment from which it is being imported. This model is particularly effective for **plugin systems**, **extensions**, and **cross-runtime libraries**, where you want to ensure that your module is used *only* in compliant environments.

Overview
--------

- The contract is stored in a YAML file (import contract).
- The protected module executes the validation at the top of its file.
- If the importing context does not meet the requirements, execution is halted.

Execution Flow
--------------

.. image:: https://raw.githubusercontent.com/atellaluca/ImportSpy/refs/heads/main/assets/ImportSpy.png
   :align: center
   :alt: Embedded Execution Flow

The flow consists of the following steps:

1. The module detects who is importing it via runtime introspection.
2. It loads the import contract (usually `spymodel.yml`).
3. It compares the importing environment against the declared contract.
4. If validation fails, it blocks execution with a detailed error.

This is a **Zero-Trust validation mechanism**: if the contract isn't satisfied, nothing runs.

Example: Minimal Contract
-------------------------

Here’s an example import contract used in embedded mode:

.. code-block:: yaml

    filename: extension.py
    variables:
      engine: docker
      plugin_name: plugin name
      plugin_description: plugin description
    classes:
      - name: Extension
        attributes:
          - type: instance
            name: extension_instance_name
            value: extension_instance_value
          - type: class
            name: extension_name
            value: extension_value
        methods:
          - name: __init__
            arguments:
              - name: self
          - name: add_extension
            arguments:
              - name: self
              - name: msg
                annotation: str
            return_annotation: str
          - name: remove_extension
            arguments:
              - name: self
          - name: http_get_request
            arguments:
              - name: self
        superclasses:
          - Plugin
      - name: Foo
        methods:
          - name: get_bar
            arguments:
              - name: self
    deployments:
      - arch: x86_64
        systems:
          - os: windows
            pythons:
              - version: 3.12.8
                interpreter: CPython
                modules:
                  - filename: extension.py
                    variables:
                      author: Luca Atella
              - version: 3.12.4
                modules:
                  - filename: addons.py
              - interpreter: IronPython
                modules:
                  - filename: addons.py
          - os: linux
            pythons:
              - version: 3.12.8
                interpreter: CPython
                modules:
                  - filename: extension.py
                    variables:
                      author: Luca Atella

Developer Notes
---------------

- Embedded mode is ideal for reusable plugins, extensions, and modules intended to run in dynamic environments.
- The validation happens *inside the module*, which means the module actively protects itself.
- Use `Spy().importspy(filepath="spymodel.yml")` at the beginning of the module to activate the validation.

Next Steps
----------

🔗 See also: :doc:`external_mode`
