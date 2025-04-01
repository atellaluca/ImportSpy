Managing ImportSpy with Poetry
==============================

**Poetry** is the official dependency management and packaging tool used in ImportSpy.  
It ensures **dependency consistency, streamlined versioning, and isolated environments**, making development and contribution more efficient.  

This guide will help you:  

- ✅ Set up ImportSpy using Poetry  
- 🔄 Manage dependencies and update packages  
- 🚀 Handle versioning and releases  
- 📝 Understand ImportSpy’s `pyproject.toml` configuration  
- 👥 Follow best practices for collaboration and contribution  

Why ImportSpy Uses Poetry 🛠️
----------------------------

Traditional package management with `pip` and `requirements.txt` can lead to **dependency conflicts and inconsistencies**.  
Poetry provides a **modern approach** with:

- ✅ **Reproducible environments** — Locked dependencies with `poetry.lock`  
- ✅ **Automatic Virtual Environments** — Isolated Python environments  
- ✅ **Simplified Versioning** — Integrated SemVer version bumping and publishing  
- ✅ **Grouped Dependencies** — Logical separation of dev/docs/runtime dependencies  

Installing Poetry 💾
--------------------

Install Poetry:

.. code-block:: bash

   curl -sSL https://install.python-poetry.org | python3 -

Check that it’s working:

.. code-block:: bash

   poetry --version

Setting Up ImportSpy 📦
-----------------------

1️⃣ **Clone the repo**:

.. code-block:: bash

   git clone https://github.com/atellaluca/importspy.git
   cd importspy

2️⃣ **Install dependencies**:

.. code-block:: bash

   poetry install

3️⃣ **(Optional) Enter shell manually**:

.. code-block:: bash

   poetry shell

Use `exit` to leave the environment.

Dependency Management 🔄
------------------------

**Add dependencies**:

.. code-block:: bash

   poetry add requests
   poetry add --group dev pytest

**Remove dependencies**:

.. code-block:: bash

   poetry remove requests

**Update packages**:

.. code-block:: bash

   poetry update
   poetry update requests

**Important differences**:

- `poetry install` → Uses `poetry.lock`, ensures **exact versions**  
- `poetry update` → Updates versions **within constraints** from `pyproject.toml`

Team best practice:  
👉 Always **commit `poetry.lock`** to avoid version drift.

Versioning and Releases 🚀
--------------------------

ImportSpy follows **Semantic Versioning (SemVer)**.

Update version with:

.. code-block:: bash

   poetry version patch|minor|major
   poetry build
   poetry publish  # Requires authentication

Handling Conflicts ⚖️
----------------------

Use:

.. code-block:: bash

   poetry show --tree              # See dependency graph
   poetry lock --no-update         # Rebuild lock without updates
   poetry add foo@latest           # Force update single package

Exporting for Pip-based Systems 📦
----------------------------------

To share a `requirements.txt`:

.. code-block:: bash

   poetry export -f requirements.txt --output requirements.txt

Then:

.. code-block:: bash

   pip install -r requirements.txt

Understanding `pyproject.toml` 📝
---------------------------------

.. code-block:: toml

   [tool.poetry]
   name = "importspy"
   version = "0.1.12"
   description = "A validation and compliance framework for Python modules."
   authors = ["Luca Atella <atellaluca@outlook.it>"]

   [tool.poetry.dependencies]
   python = "^3.10"
   pydantic = "^2.9.2"

   [tool.poetry.group.dev.dependencies]
   pytest = "^8.3.3"

   [tool.poetry.group.docs.dependencies]
   sphinx = ">=5,<9"
   furo = "^2024.8.6"

Defining CLI Commands 🖥️
-------------------------

Poetry supports entry points for CLI tools:

.. code-block:: toml

   [tool.poetry.scripts]
   importspy-validate = "importspy.cli:validate"

Usage:

.. code-block:: bash

   poetry run importspy-validate

Next Steps 🔍
-------------

Now that you understand Poetry’s role in ImportSpy, continue with:

- :doc:`python_reflection` — Learn how ImportSpy uses Python's introspection tools  
- :doc:`pydantic_in_importspy` — See how validation models power the framework
