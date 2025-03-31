"""
Runtime Environment Utilities
=============================

Provides a lightweight interface to query the system's hardware architecture.

This module supports ImportSpy in enforcing architecture-specific constraints
declared in import contracts.

Example
-------
.. code-block:: python

    from importspy.utilities.runtime_util import RuntimeUtil

    runtime = RuntimeUtil()
    print(runtime.extract_arch())
"""

import logging
import platform

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

class RuntimeUtil:
    """
    Utility class to retrieve system architecture details.

    Methods
    -------
    extract_arch() -> str
        Returns the machine’s hardware architecture.

    Example
    -------
    >>> RuntimeUtil().extract_arch()
    'x86_64'
    """

    def extract_arch(self) -> str:
        """
        Return the system architecture (e.g., 'x86_64', 'arm64').

        Uses the `platform.machine()` method to query the current hardware.

        Returns
        -------
        str
            Architecture name (e.g., 'x86_64', 'arm64').
        """
        return platform.machine()
