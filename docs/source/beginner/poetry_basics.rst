Managing ImportSpy with Poetry
==============================

**Poetry** is the official dependency management and packaging tool used in ImportSpy.  
It ensures **dependency consistency, streamlined versioning, and isolated environments**, making development and contribution more efficient.  

This guide will help you:  

- **Set up ImportSpy using Poetry**
- **Manage dependencies and update packages correctly**
- **Handle versioning and releases effectively**
- **Understand ImportSpy’s `pyproject.toml` configuration**
- **Follow best practices for contributing to ImportSpy**  

Why ImportSpy Uses Poetry 🛠️
----------------------------

Traditional package management with `pip` and `requirements.txt` can lead to **dependency conflicts and inconsistencies**.  
Poetry provides a **modern approach** with:

✅ **Reproducible environments** → The `poetry.lock` file locks dependencies, preventing unexpected updates.  

✅ **Automatic Virtual Environments** → Isolates dependencies, avoiding conflicts with globally installed packages.  

✅ **Simplified Versioning and Releases** → Automates package version management for PyPI releases.  

✅ **Explicit Dependency Management** → Organizes dependencies into **core**, **development**, and **documentation** groups.  

Installing Poetry 💾
--------------------

Install Poetry with:

.. code-block:: bash

   curl -sSL https://install.python-poetry.org | python3 -

Verify installation:

.. code-block:: bash

   poetry --version

Setting Up ImportSpy 📦
-----------------------

1️⃣ **Clone the repository**  

.. code-block:: bash

   git clone https://github.com/atellaluca/importspy.git
   cd importspy

2️⃣ **Install dependencies**  

Poetry **creates and manages a virtual environment automatically** when you install dependencies:

.. code-block:: bash

   poetry install

3️⃣ **Activate the virtual environment manually (if needed)**  

Normally, Poetry activates the environment for you.  
If needed (e.g., inside an IDE), manually activate it:

.. code-block:: bash

   poetry shell

Use `exit` to leave the environment when done.

Dependency Management 🔄
------------------------

**Adding a New Dependency**  
To install a package and update `pyproject.toml`:

.. code-block:: bash

   poetry add <package-name>

For development-only dependencies:

.. code-block:: bash

   poetry add --group dev <package-name>

**Removing a Dependency**  
To remove an unused package:

.. code-block:: bash

   poetry remove <package-name>

**Updating Dependencies**  
To update **all dependencies** while keeping the same major versions:

.. code-block:: bash

   poetry update

To update **a specific package**:

.. code-block:: bash

   poetry update <package-name>

⚠️ **Poetry Install vs Poetry Update**
- `poetry install` → Installs the **exact versions** in `poetry.lock`, ensuring **full reproducibility** (best for teams).  
- `poetry update` → **Fetches newer versions** within allowed constraints (`pyproject.toml`), which might cause **unexpected changes**.  

🔹 **When to Use `poetry update`?**  
Use it when you need to **fetch new versions** of dependencies while maintaining compatibility.  
However, in a **team environment**, using `poetry update` without coordination **can cause inconsistencies**, since each contributor might get different versions.

🔹 **Scenario where `poetry update` could be problematic**  
Suppose Alice and Bob are both working on ImportSpy. Alice runs:

.. code-block:: bash

   poetry update

Her `poetry.lock` is updated with **newer dependency versions**.  
Bob, unaware of this, runs `poetry install`, which keeps his dependencies **unchanged**.  
Now, **Alice and Bob are running different versions of dependencies**, which may lead to unpredictable behavior.

🔹 **Solution?**  
If working in a team, **always commit `poetry.lock`** after updates and **sync with `poetry install`** instead of updating individually.

Versioning and Releases 🚀
--------------------------

ImportSpy follows **Semantic Versioning (SemVer)**:

🔹 **Patch release (bug fixes)** →  

.. code-block:: bash

   poetry version patch

🔹 **Minor release (new features, backward-compatible)** →  

.. code-block:: bash

   poetry version minor

🔹 **Major release (breaking changes)** →  

.. code-block:: bash

   poetry version major

After updating the version:

.. code-block:: bash

   poetry build
   poetry publish  # Requires PyPI authentication

Handling Dependency Conflicts ⚖️
--------------------------------

If Poetry detects **conflicting dependencies**, resolve them by:

1️⃣ Checking dependency constraints:

.. code-block:: bash

   poetry show --tree

2️⃣ Forcing dependency resolution:

.. code-block:: bash

   poetry lock --no-update  # Regenerates poetry.lock without changing versions

3️⃣ If necessary, update a single package:

.. code-block:: bash

   poetry add <package-name>@latest

🔹 **When to Use `poetry lock --no-update`?**  
This is useful **when dependencies change upstream**, but you want to **recreate `poetry.lock` without fetching new versions**.  
Example: The `pyproject.toml` has changed (e.g., a new dependency was added), but you want to retain the existing dependency tree.

Exporting Dependencies for External Environments 📜
---------------------------------------------------

To install dependencies **without Poetry**, export them as a `requirements.txt` file:

.. code-block:: bash

   poetry export -f requirements.txt --output requirements.txt

Then install them in a non-Poetry environment:

.. code-block:: bash

   pip install -r requirements.txt

Understanding `pyproject.toml` 📝
---------------------------------

The `pyproject.toml` file defines ImportSpy’s package configuration.

**Example Configuration:**

.. code-block:: toml

   [tool.poetry]
   name = "importspy"
   version = "0.1.12"
   description = "A validation and compliance framework for Python modules."
   authors = ["Luca Atella <atellaluca@outlook.it>"]
   license = "MIT"

   [tool.poetry.dependencies]
   python = "^3.10"
   pydantic = "^2.9.2"

   [tool.poetry.group.dev.dependencies]
   pytest = "^8.3.3"

   [tool.poetry.group.docs.dependencies]
   sphinx = ">=5,<9"
   furo = "^2024.8.6"

Defining CLI Commands with Poetry 🖥️
-------------------------------------

Poetry can define **custom scripts** for ImportSpy:

.. code-block:: toml

   [tool.poetry.scripts]
   importspy-validate = "importspy.cli:validate"

Now, you can run:

.. code-block:: bash

   poetry run importspy-validate

Next Steps 🔍
-------------

Now that you understand **Poetry’s role in ImportSpy**, explore:

- **How Python Reflection Works** → :doc:`python_reflection`
- **How ImportSpy Uses Pydantic** → :doc:`pydantic_in_importspy`
