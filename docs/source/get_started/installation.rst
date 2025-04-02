Installation Guide
==================

Welcome to the **Installation Guide** for ImportSpy.  
This section will walk you through setting up ImportSpy in your environment — quickly, cleanly, and with confidence.

ImportSpy is designed to be lightweight and easy to integrate into any Python project that values **runtime validation**, **structural compliance**, and **predictable imports**.

System Requirements 📌
-----------------------

Before you begin, make sure your development environment meets the following requirements:

- **Python 3.10 or later**  
  ImportSpy relies on modern Python features and guarantees compatibility only from version 3.10 onward.

- **pip (latest version)**  
  To ensure smooth installation and dependency resolution.

- **Virtual Environment (Recommended)**  
  While optional, using a virtual environment is best practice for avoiding dependency conflicts and ensuring isolation.

Installing ImportSpy ⚙️
------------------------

1. **Create and Activate a Virtual Environment**

   While not mandatory, we strongly recommend installing ImportSpy in a virtual environment:

   .. tabs::

      .. tab:: macOS / Linux

         .. code-block:: bash

            python3 -m venv venv
            source venv/bin/activate

      .. tab:: Windows

         .. code-block:: bash

            python -m venv venv
            .\venv\Scripts\activate

   Once activated, your terminal should indicate that the environment is active.

2. **Install ImportSpy with pip**

   Now install ImportSpy directly from PyPI:

   .. code-block:: bash

      pip install importspy

   This command will install the latest stable version of ImportSpy and all required dependencies.

Verifying the Installation ✅
------------------------------

To confirm that ImportSpy is correctly installed and ready to use, run:

.. code-block:: bash

   importspy --version

If everything is set up correctly, the terminal will display the current version of ImportSpy.

Troubleshooting Tips 🧯
------------------------

If something goes wrong:

- Ensure you're using **Python 3.10+**
- Activate your virtual environment before running `pip install`
- If needed, upgrade pip:  
  .. code-block:: bash  
     python -m pip install --upgrade pip

You're Ready to Go 🎉
----------------------

That’s it! You’re now ready to start using ImportSpy to enforce module validation in your projects.

Continue to the next section to explore a working example and see ImportSpy in action:

📎 :doc:`example_overview`
