==================================
Running the Plugin-Based Example
==================================

This guide explains **how to execute the Plugin-Based Architecture example** using **ImportSpy**.  
By following these steps, you'll see **how ImportSpy enforces structure and validation** when dynamically loading plugins.

Prerequisites
-------------

Before running the example, make sure you have:

- **Python 3.8+ installed** (ImportSpy requires Python 3.8 or later).
- **ImportSpy installed**. If you haven't installed it yet, run:

  .. code-block:: bash

     pip install importspy

- **Cloned or downloaded the ImportSpy repository** (if using local examples):

  .. code-block:: bash

     git clone https://github.com/atellaluca/importspy.git
     cd importspy/examples/plugin_based_architecture

Steps to Run the Example
------------------------

1. **Navigate to the example directory**:

   .. code-block:: bash

      cd importspy/examples/plugin_based_architecture

2. **Run the validation script** (`extension.py`), which initializes ImportSpy and validates the plugin structure:

   .. code-block:: bash

      python extension.py

Expected Output
---------------

If the plugin (`extension.py`) follows the expected structure, you will see an output similar to:

   .. code-block:: text
      
      Foobar

If there are validation errors (e.g., missing attributes, incorrect types, or unsupported Python versions),  
ImportSpy will raise an exception with detailed error messages.

Testing Modifications
---------------------

Try making modifications to `extension.py` and observe how ImportSpy detects changes:

- **Remove a required attribute** → ImportSpy will throw a validation error.
- **Change the Python version in `package.py`** → The framework will enforce compatibility.
- **Add a new method** and update `package.py` to require it → Watch ImportSpy detect the changes.
Next Steps
----------

- **Understand the validation model** in `package.py`.
- **Explore the plugin implementation** in `extension.py`.
- **Dive deeper into ImportSpy's capabilities** in the :doc:`../overview`.
