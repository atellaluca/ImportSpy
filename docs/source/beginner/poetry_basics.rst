Using Poetry with ImportSpy
===========================

Poetry is the **official packaging and dependency management tool** used in ImportSpy.  
It ensures reproducibility, streamlines development workflows, and enables better collaboration.  
This guide will help you understand how to use Poetry within ImportSpy’s ecosystem and learn why it’s essential.

Why Poetry?
-----------

Poetry offers a modern alternative to legacy tools like `pip`, `setup.py`, and `requirements.txt`.  
It provides:

- ✅ **Isolated virtual environments** with automatic activation
- ✅ **Declarative dependency management** via `pyproject.toml`
- ✅ **Lockfile consistency** with `poetry.lock`
- ✅ **Integrated build and publishing workflow**
- ✅ **Support for multiple dependency groups** (dev, docs, ci, etc.)

Installing Poetry
-----------------

You can install Poetry with the official script:

.. code-block:: bash

   curl -sSL https://install.python-poetry.org | python3 -

Verify installation:

.. code-block:: bash

   poetry --version

Setting Up ImportSpy
--------------------

1. Clone the repository:

   .. code-block:: bash

      git clone https://github.com/atellaluca/importspy.git
      cd importspy

2. Install all project dependencies:

   .. code-block:: bash

      poetry install

3. Activate the virtual environment (optional):

   .. code-block:: bash

      poetry shell

Dependency Management
---------------------

Add dependencies:

.. code-block:: bash

   poetry add pydantic
   poetry add --group dev pytest

Remove dependencies:

.. code-block:: bash

   poetry remove pydantic

Update dependencies:

.. code-block:: bash

   poetry update                # Update all
   poetry update pydantic      # Update a specific one

Best practice:  
✅ Always commit `poetry.lock` to your VCS to ensure reproducibility.

Understanding the `pyproject.toml`
----------------------------------

.. code-block:: toml

   [tool.poetry]
   name = "importspy"
   version = "0.2.0"
   description = "A validation and compliance framework for Python modules."
   authors = ["Luca Atella <atellaluca@outlook.it>"]

   [tool.poetry.dependencies]
   python = "^3.10"
   pydantic = "^2.9.2"

   [tool.poetry.group.dev.dependencies]
   pytest = "^8.3.3"

   [tool.poetry.group.docs.dependencies]
   sphinx = "^7.2"
   furo = "^2024.8.6"

   [tool.poetry.scripts]
   importspy = "importspy.cli:validate"

To run CLI commands defined in the `pyproject.toml`:

.. code-block:: bash

   poetry run importspy --help

Versioning and Releases
-----------------------

ImportSpy follows Semantic Versioning (SemVer).  
You can bump versions like this:

.. code-block:: bash

   poetry version patch | minor | major

Build and publish (requires authentication):

.. code-block:: bash

   poetry build
   poetry publish

Exporting Requirements
----------------------

If you need a `requirements.txt` (e.g., for Docker or legacy tooling):

.. code-block:: bash

   poetry export -f requirements.txt --output requirements.txt

Next Steps
----------

Now that you’ve configured Poetry, continue learning about ImportSpy’s internals:

- :doc:`python_reflection`
- :doc:`pydantic_in_importspy`
