"""Python Runtime Utilities

Provides utility methods to inspect the active Python runtime environment,
such as the version number and interpreter implementation.

These utilities are useful within ImportSpy to evaluate whether the current
runtime context satisfies declared compatibility constraints in import contracts.
This includes checks for specific Python versions and interpreter families
(CPython, PyPy, IronPython, etc.).

Example:
    from importspy.utilities.python_util import PythonUtil
    util = PythonUtil()
    util.extract_python_version()
    > Output '3.12.0'
    util.extract_python_implementation()
    > Output: 'CPython'
"""

import logging
import platform

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class PythonUtil:
    """Utility class for inspecting Python runtime characteristics.

    Used internally by ImportSpy to validate runtime-specific conditions declared
    in `.yml` import contracts. This includes checking Python version and interpreter
    type during structural introspection and contract validation.
    """

    def extract_python_version(self) -> str:
        """Return the currently active Python version as a string.

        This method queries the runtime using `platform.python_version()` and is
        typically used to match version constraints defined in an import contract.

        Returns:
            str: The Python version string (e.g., "3.11.4").
        
        Example:
            PythonUtil().extract_python_version()
            > Output: '3.11.4'
        """
        return platform.python_version()

    def extract_python_implementation(self) -> str:
        """Return the implementation name of the running Python interpreter.

        Common values include "CPython", "PyPy", or "IronPython". This is
        essential in contexts where the implementation affects runtime behavior
        or compatibility with native extensions.

        Returns:
            str: The interpreter implementation (e.g., "CPython").
        
        Example:
            PythonUtil().extract_python_implementation()
            > Output: 'CPython'
        """
        return platform.python_implementation()
