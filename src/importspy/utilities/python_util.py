"""
Python Runtime Utilities
========================

Provides helpers to inspect the active Python environment,
such as the interpreter implementation and version.

Useful in ImportSpy to validate compatibility constraints across Python versions
and runtime variants (e.g., CPython, PyPy, IronPython).

Example:
--------
.. code-block:: python

    from importspy.utilities.python_util import PythonUtil

    util = PythonUtil()
    print(util.extract_python_version())
    print(util.extract_python_implementation())
"""

import logging
import platform

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

class PythonUtil:
    """
    Utility class for querying Python runtime details.

    Methods
    -------
    extract_python_version() -> str
        Returns the current Python version (e.g., "3.11.2").

    extract_python_implementation() -> str
        Returns the Python interpreter name (e.g., "CPython", "PyPy").
    """

    def extract_python_version(self) -> str:
        """
        Return the active Python version.

        Returns
        -------
        str
            Python version string (e.g., '3.11.2').

        Example
        -------
        >>> PythonUtil().extract_python_version()
        '3.11'
        """
        python_version = platform.python_version()
        return ".".join(python_version.split(".")[:2])

    def extract_python_implementation(self) -> str:
        """
        Return the Python implementation type.

        Returns
        -------
        str
            Python interpreter name (e.g., 'CPython', 'PyPy').

        Example
        -------
        >>> PythonUtil().extract_python_implementation()
        'CPython'
        """
        return platform.python_implementation()
