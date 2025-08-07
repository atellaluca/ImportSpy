# ImportSpy

![License](https://img.shields.io/github/license/atellaluca/importspy)
[![PyPI Version](https://img.shields.io/pypi/v/importspy)](https://pypi.org/project/importspy/)
[![Docs](https://img.shields.io/badge/docs-online-blue)](https://atellaluca.github.io/ImportSpy/)
![Python Versions](https://img.shields.io/pypi/pyversions/importspy)
[![Build Status](https://img.shields.io/github/actions/workflow/status/atellaluca/ImportSpy/python-package.yml?branch=main)](https://github.com/atellaluca/ImportSpy/actions/workflows/python-package.yml)

**Runtime contract validation for Python imports.**  
_Enforce structure, Block invalid usage: stay safe at runtime._

![ImportSpy banner](https://raw.githubusercontent.com/atellaluca/ImportSpy/refs/heads/main/docs/assets/importspy-banner_500px.png)

---

## 🔍 What is ImportSpy?

**ImportSpy** lets your Python modules declare structured **import contracts** (via `.yml` files) to define:

- What environment they expect (OS, Python version, interpreter)
- What structure they must follow (classes, methods, variables)
- Who is allowed to import them

If the contract is not met, **ImportSpy blocks the import** — ensuring safe and predictable runtime behavior.

---

## ✨ Key Features

- ✅ Validate imports dynamically at runtime or via CLI  
- ✅ Block incompatible usage of internal or critical modules  
- ✅ Enforce module structure, arguments, annotations  
- ✅ Context-aware: Python version, OS, architecture, interpreter  
- ✅ Human-readable YAML contracts  
- ✅ Clear, CI-friendly violation messages  

---

## 📦 Installation

```bash
pip install importspy
```

> Requires Python 3.10+

---

## 📐 Architecture

![SpyModel UML](https://raw.githubusercontent.com/atellaluca/ImportSpy/refs/heads/main/docs/assets/importspy-spy-model-architecture.png)

ImportSpy is powered by a layered introspection model (`SpyModel`), which captures:

- `Runtime`: CPU architecture  
- `System`: OS and environment  
- `Python`: interpreter and version  
- `Module`: classes, functions, variables, annotations  

Each layer is validated against the corresponding section of your `.yml` contract.

---

## 📜 Example Contract

```yaml
filename: plugin.py
variables:
  - name: mode
    value: production
    annotation: str
classes:
  - name: Plugin
    methods:
      - name: run
        arguments:
          - name: self
          - name: data
            annotation: dict
        return_annotation: None
```

---

## 🔧 Modes of Use

### Embedded Mode – protect your own module

```python
from importspy import Spy

caller = Spy().importspy(filepath="spymodel.yml")
caller.Plugin().run()
```

![Embedded mode](https://raw.githubusercontent.com/atellaluca/ImportSpy/refs/heads/main/docs/assets/importspy-embedded-mode.png)

---

### CLI Mode – external validation in CI

```bash
importspy -s spymodel.yml -l DEBUG path/to/module.py
```

![CLI mode](https://raw.githubusercontent.com/atellaluca/ImportSpy/refs/heads/main/docs/assets/importspy-works.png)

---

## 🧠 How It Works

1. You define an import contract in `.yml`  
2. At runtime or via CLI, ImportSpy inspects:  
   - Who is importing the module  
   - What the system/environment looks like  
   - What the module structure provides  
3. If validation fails → the import is blocked  
4. If valid → the module runs safely  

---

## ✅ Tech Stack

- [Pydantic 2.x](https://docs.pydantic.dev) – schema validation  
- [Typer](https://typer.tiangolo.com) – CLI  
- [ruamel.yaml](https://yaml.readthedocs.io/) – YAML support  
- `inspect` + `sys` – runtime introspection  
- [Poetry](https://python-poetry.org) – dependency management  
- [Sphinx](https://www.sphinx-doc.org) + ReadTheDocs – documentation  

---

## 📘 Documentation

- **Full docs** → [importspy.readthedocs.io](https://importspy.readthedocs.io)  
- [Quickstart](https://importspy.readthedocs.io/en/latest/intro/quickstart.html)  
- [Contract syntax](https://importspy.readthedocs.io/en/latest/contracts/syntax.html)  
- [Violation system](https://importspy.readthedocs.io/en/latest/advanced/violations.html)  
- [API Reference](https://importspy.readthedocs.io/en/latest/api-reference.html)  

---

## 🚀 Ideal Use Cases

- Plugin-based frameworks (e.g., CMS, CLI, IDE)  
- CI/CD pipelines with strict integration  
- Security-regulated environments (IoT, medical, fintech)  
- Package maintainers enforcing internal boundaries  

---

## 💡 Why It Matters

Python’s flexibility comes at a cost:

- Silent runtime mismatches  
- Missing methods or classes  
- Platform-dependent failures  
- No enforcement over module consumers  

**ImportSpy brings governance**  
to how, when, and where modules are imported.

---

## ❤️ Contribute & Support

- ⭐ [Star on GitHub](https://github.com/atellaluca/ImportSpy)  
- 🐛 [File issues or feature requests](https://github.com/atellaluca/ImportSpy/issues)  
- 🤝 [Contribute](https://github.com/atellaluca/ImportSpy/blob/main/CONTRIBUTING.md)  
- 💖 [Sponsor on GitHub](https://github.com/sponsors/atellaluca)  

---

## 📜 License

MIT © 2024 – Luca Atella  
![ImportSpy logo](https://raw.githubusercontent.com/atellaluca/ImportSpy/refs/heads/main/docs/assets/importspy-logo_100px.png)
