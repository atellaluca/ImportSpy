Installation Guide
==================

Welcome to the **Installation Guide** for **ImportSpy**!  
This section will help you set up ImportSpy on your system and ensure that everything is correctly configured.

System Requirements 📌
----------------------

Before installing **ImportSpy**, make sure your environment meets the following requirements:

- **Python 3.10+** → ImportSpy requires a modern Python version to ensure compatibility with its validation system.
- **pip (latest version)** → Ensure `pip` is up-to-date for smooth installation.
- **Virtual Environment (Recommended)** → Helps isolate dependencies and prevents conflicts with other Python packages.

Setting Up ImportSpy ⚙️
------------------------

Follow these steps to install and configure **ImportSpy**:

1. **Create a Virtual Environment** (Recommended)

   To avoid dependency conflicts, it's best practice to install ImportSpy in a virtual environment.

   .. tabs::

      .. tab:: macOS / Linux

         .. code-block:: bash

            python3 -m venv venv
            source venv/bin/activate

      .. tab:: Windows

         .. code-block:: bash

            python3 -m venv venv
            venv\Scripts\activate

   Once activated, your terminal should indicate that the virtual environment is active.

2. **Install ImportSpy via pip**

   Now, install ImportSpy using **pip**:

   .. code-block:: bash

      pip install importspy

   This will fetch the latest stable version of ImportSpy and install it along with its dependencies.

Verifying the Installation ✅
-----------------------------

To confirm that ImportSpy is correctly installed, run:

   .. code-block:: bash

      importspy --version

If ImportSpy is installed correctly, you should see the version number printed in the terminal.  
If you encounter any issues, make sure:

- You're using **Python 3.10+**.
- The virtual environment is activated before running commands.
- `pip install importspy` completes without errors.

🎉 **Congratulations!** You’re now ready to use ImportSpy and start validating your modules! 🚀
