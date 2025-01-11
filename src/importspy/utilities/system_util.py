import os
import logging
import platform

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

class SystemUtil:

    def extract_os(self) -> str:
        return platform.system().lower()

    def extract_envs(self) -> dict:
        """
        Extract all current environment variables and their values as a dictionary.

        This function retrieves all environment variables available in the system's current execution
        context and returns them in a dictionary format. Each key in the dictionary represents the
        name of an environment variable, and its corresponding value represents the value assigned 
        to that variable.

        Parameters:
        -----------
        None

        Returns:
        --------
        - **dict**: A dictionary where:
            - **Key** (`str`): The name of the environment variable.
            - **Value** (`str`): The value assigned to the environment variable.

        Example Usage:
        --------------
        ```python
        env_vars = extract_envs()
        print(env_vars)
        # Output: {'PATH': '/usr/bin:/bin', 'CI': 'true', ...}
        ```

        Notes:
        ------
        - This function is useful for debugging or validating the runtime environment.
        - It relies on `os.environ`, which reflects the environment at the time the function is called.
        - Sensitive data (e.g., API keys) might be included in the output; handle with care.
        """
        return dict(os.environ)