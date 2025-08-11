"""System Utilities for ImportSpy

Provides tools to inspect the host operating system and environment variables.

This module supports ImportSpy by normalizing system-level information that may
affect import contract validation. It helps ensure that environmental conditions
are consistent and inspectable across different operating systems and deployment contexts.

Features:
    - Detects the current operating system in a normalized, lowercase format.
    - Retrieves all environment variables as a list of structured objects.

Example:
    from importspy.utilities.system_util import SystemUtil
    util = SystemUtil()
    util.extract_os()
    'linux'
    envs = util.extract_envs()
    envs[0]
    > Output: VariableInfo(name='PATH', annotation=None, value='/usr/bin')
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
    """Utility class for inspecting system-level properties.

    Used by ImportSpy to collect information about the current operating system
    and active environment variables. These details are typically validated
    against constraints defined in `.yml` import contracts.

    Methods:
        extract_os(): Return the normalized name of the current operating system.
        extract_envs(): Return all active environment variables as structured entries.
    """

    def extract_os(self) -> str:
        """Return the name of the operating system in lowercase format.

        This method uses `platform.system()` and normalizes the result
        to lowercase. It simplifies comparisons with import contract conditions
        that expect a canonical form such as "linux", "darwin", or "windows".

        Returns:
            str: The normalized operating system name (e.g., "linux", "windows").

        Example:
            SystemUtil().extract_os()
            > Output 'darwin'
        """
        return platform.system().lower()

    def extract_envs(self) -> List[VariableInfo]:
        """Return all environment variables as a list of structured objects.

        Collects all key-value pairs from `os.environ` and wraps them in
        `VariableInfo` namedtuples. The `annotation` field is reserved for
        optional type annotation metadata (currently set to `None`).

        Returns:
            List[VariableInfo]: A list of environment variables available
            in the current process environment.

        Example:
            envs = SystemUtil().extract_envs()
            envs[0]
            > Output: VariableInfo(name='PATH', annotation=None, value='/usr/bin')
        """
        return [VariableInfo(name, None, value) for name, value in os.environ.items()]
