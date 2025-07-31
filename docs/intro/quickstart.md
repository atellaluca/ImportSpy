# Quickstart

This quickstart shows how to use **ImportSpy in Embedded Mode** to protect a Python module from being imported in an invalid context.

---

## Step 1 — Install ImportSpy

If you haven’t already:

```bash
pip install importspy
```

---

## Step 2 — Create a contract (`spymodel.yml`)

This file defines the conditions under which your module can be imported.  
For example, it can require specific Python versions, operating systems, or structure in the calling module.

```yaml
filename: plugin.py
classes:
  - name: Plugin
    methods:
      - name: run
        arguments:
          - name: self
        return_annotation:
deployments:
  - arch: x86_64
    systems:
      - os: linux
        pythons:
          - version: 3.12
            interpreter: CPython
```

Save this file as `spymodel.yml`.

---

## Step 3 — Protect your module

Here’s how to use ImportSpy inside the module you want to protect (e.g. `plugin.py`):

```python
# plugin.py
from importspy import Spy

caller = Spy().importspy(filepath="spymodel.yml")

# Call something from the importer (for example)
caller.MyPlugin().run()
```

This checks the current environment and the module that is importing `plugin.py`.
If it doesn’t match the contract, ImportSpy raises an error and blocks the import.

---

## Step 4 — Create an importer

Write a simple module that tries to import `plugin.py`.

```python
# main.py
class MyPlugin:
    def run(self):
        print("Plugin running")

import plugin
```

---

## Step 5 — Run it

If the environment and structure of `main.py` match the contract, the import will succeed:

```bash
python main.py
```

Otherwise, you'll get a clear and structured error like:

```
[Structure Violation] Missing required class 'Plugin' in caller module.
```

---

## Next steps

- Learn more about [Embedded Mode](../modes/embedded.md)
- Explore [CLI Mode](../modes/cli.md) for validating modules from the outside
- Dive into [contract syntax](../contracts/syntax.md) to write more advanced rules
