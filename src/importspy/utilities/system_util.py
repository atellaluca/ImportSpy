"""
System Utilities for ImportSpy
==============================

Provides tools to interact with the host system and environment variables.

This utility module helps ImportSpy detect and normalize runtime conditions, such as
the operating system or environment setup, ensuring compatibility checks work reliably.

Features:
---------
- Identifies the current operating system in a standardized lowercase format.
- Retrieves environment variables as a key-value dictionary.

Example:
--------
.. code-block:: python

    from importspy.utilities.system_util import SystemUtil

    util = SystemUtil()
    os_name = util.extract_os()
    env = util.extract_envs()
"""

import os
import logging
import platform

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

class SystemUtil:
    """
    System-level utility class for environment inspection.

    Offers support for OS detection and retrieval of environment variables.

    Methods
    -------
    extract_os() -> str
        Returns the lowercase name of the operating system (e.g., 'windows', 'linux').

    extract_envs() -> dict
        Returns a dictionary of all active environment variables.
    """

    def extract_os(self) -> str:
        """
        Return the operating system name in lowercase.

        Uses `platform.system()` for OS detection.

        Returns
        -------
        str
            'windows', 'linux', or 'darwin', depending on the system.

        Example
        -------
        >>> SystemUtil().extract_os()
        'linux'
        """
        return platform.system().lower()

    def extract_envs(self) -> dict:
        """
        Retrieve all current environment variables.

        Returns
        -------
        dict
            Dictionary of key-value environment variables.

        Example
        -------
        >>> SystemUtil().extract_envs()
        {'PATH': '/usr/bin:/bin', 'HOME': '/home/user', ...}
        """
        return dict(os.environ)
