"""
Module: Python Utilities

This module provides utility functions for extracting details about the current Python runtime environment, 
including the version and implementation type.

Key Features:
-------------
- Retrieve the current Python version.
- Identify the Python implementation type (e.g., CPython, PyPy, etc.).

Example Usage:
--------------
```python
from importspy.utilities.python_util import PythonUtil

python_util = PythonUtil()
version = python_util.extract_python_version()
implementation = python_util.extract_python_implementation()

print(f"Python Version: {version}")
print(f"Python Implementation: {implementation}")
"""

import logging
import platform

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())
    
class PythonUtil:

    """
    Utility class for Python runtime information retrieval.

    The `PythonUtil` class provides methods to extract details about the Python runtime, including 
    its version and implementation type. These utilities are useful for verifying compatibility with 
    specific Python features or environments.

    Methods:
    --------
    - `extract_python_version`: Returns the current Python version as a string.
    - `extract_python_implementation`: Returns the current Python implementation type.

    Example:
    --------
    ```python
    from importspy.utilities.python_util import PythonUtil

    python_util = PythonUtil()
    version = python_util.extract_python_version()
    implementation = python_util.extract_python_implementation()

    print(f"Python Version: {version}")
    print(f"Python Implementation: {implementation}")
    ```
    """

    def extract_python_version(self) -> str:
        """
        Retrieve the current Python version.

        This method uses the `platform` module to obtain the Python version currently running 
        the application, formatted as a string (e.g., "3.10.5").

        Returns:
        --------
        - **str**: The Python version string (e.g., "3.10.5").

        Example Usage:
        --------------
        ```python
        python_util = PythonUtil()
        version = python_util.extract_python_version()
        print(f"Python Version: {version}")
        # Output: '3.10.5'
        ```

        Notes:
        ------
        - Useful for verifying Python version compatibility for libraries or runtime features.
        """
        return platform.python_version()
    
    def extract_python_implementation(self) -> str:
        """
        Retrieve the Python implementation type.

        This method uses the `platform` module to identify the Python implementation currently 
        running the application (e.g., CPython, PyPy, Jython).

        Returns:
        --------
        - **str**: The Python implementation type (e.g., "CPython", "PyPy").

        Example Usage:
        --------------
        ```python
        python_util = PythonUtil()
        implementation = python_util.extract_python_implementation()
        print(f"Python Implementation: {implementation}")
        # Output: 'CPython', 'PyPy', etc.
        ```

        Notes:
        ------
        - Helps in determining the underlying implementation for compatibility or optimization purposes.
        """
        return platform.python_implementation()
