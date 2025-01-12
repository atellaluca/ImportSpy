"""
Module: System Utilities

This module provides utility functions for interacting with the system environment and retrieving 
information about the operating system and environment variables.

Key Features:
-------------
- Extracts the operating system's name in a standardized format.
- Retrieves all environment variables as a dictionary for debugging or validation purposes.

Example Usage:
--------------
```python
from importspy.utilities.system_util import SystemUtil

system_util = SystemUtil()
os_name = system_util.extract_os()
env_vars = system_util.extract_envs()
"""

import os
import logging
import platform

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

class SystemUtil:

    """
    Utility class for system-level operations and environment management.

    The `SystemUtil` class provides methods for retrieving system information, such as the operating 
    system name and current environment variables. These utilities are useful for validating runtime 
    environments or diagnosing issues related to system configuration.

    Methods:
    --------
    - `extract_os`: Returns the name of the operating system in lowercase.
    - `extract_envs`: Retrieves all current environment variables as a dictionary.

    Example:
    --------
    ```python
    from importspy.utilities.system_util import SystemUtil

    system_util = SystemUtil()
    os_name = system_util.extract_os()
    env_vars = system_util.extract_envs()
    ```
    """

    def extract_os(self) -> str:
        """
        Retrieve the name of the operating system in lowercase format.

        This method uses the `platform.system()` function to get the name of the operating system 
        and converts it to lowercase for consistency.

        Parameters:
        -----------
        None

        Returns:
        --------
        - **str**: The name of the operating system (e.g., 'windows', 'linux', 'darwin').

        Example Usage:
        --------------
        ```python
        system_util = SystemUtil()
        os_name = system_util.extract_os()
        print(os_name)
        # Output: 'linux'
        ```

        Notes:
        ------
        - This method is helpful for normalizing OS-specific behavior in multi-platform applications.
        """
        return platform.system().lower()

    def extract_envs(self) -> dict:
        """
        Extract all current environment variables and their values as a dictionary.

        This method retrieves all environment variables from the current system's execution context 
        and returns them in a key-value pair format.

        Parameters:
        -----------
        None

        Returns:
        --------
        - **dict**: A dictionary where:
            - **Key** (`str`): The name of an environment variable.
            - **Value** (`str`): The value of the environment variable.

        Example Usage:
        --------------
        ```python
        system_util = SystemUtil()
        env_vars = system_util.extract_envs()
        print(env_vars)
        # Output: {'PATH': '/usr/bin:/bin', 'HOME': '/home/user', ...}
        ```

        Notes:
        ------
        - Useful for debugging and validating runtime environments.
        - Be cautious of sensitive data (e.g., API keys) in the environment variables.
        """
        return dict(os.environ)