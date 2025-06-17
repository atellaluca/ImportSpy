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
from collections import namedtuple
from typing import List

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

VariableInfo = namedtuple('VariableInfo', ["name", "annotation", "value"])

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

    def extract_envs(self) -> List[VariableInfo]:
        """
        Return a list of environment variables available in the current process.

        Uses `os.environ.items()` to collect all key-value pairs.

        Returns
        -------
        List[VariableInfo]

            A list of VariableInfo instances, each representing an environment variable.

        Example
        -------
        >>> SystemUtil().extract_envs()
        [VariableInfo(name='PATH', value='/usr/bin'), VariableInfo(name='HOME', value='/home/user'), ...]
        """
        return [VariableInfo(name, None, value) for name, value in os.environ.items()]

