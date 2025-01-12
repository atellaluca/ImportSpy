"""
Module: Runtime Utilities

This module provides utility functions for extracting runtime-related information about the system. 
It includes methods for retrieving the system's hardware architecture.

Key Features:
-------------
- Extracts hardware architecture for compatibility checks.
- Facilitates runtime validation in multi-platform environments.

Example Usage:
--------------
```python
from importspy.utilities.runtime_util import RuntimeUtil

runtime_util = RuntimeUtil()
architecture = runtime_util.extract_arch()
print(f"System Architecture: {architecture}")
"""

import logging
import platform

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

class RuntimeUtil:
    """
    Utility class for runtime-related operations and system information retrieval.

    The `RuntimeUtil` class offers methods to extract key details about the system's runtime 
    environment, such as the hardware architecture. These utilities are particularly valuable 
    for validating runtime requirements in multi-platform software.

    Methods:
    --------
    - `extract_arch`: Retrieves the current hardware architecture of the system.

    Example:
    --------
    ```python
    from importspy.utilities.runtime_util import RuntimeUtil

    runtime_util = RuntimeUtil()
    architecture = runtime_util.extract_arch()
    print(f"Architecture: {architecture}")
    ```
    """

    def extract_arch(self) -> str:
        """
        Retrieve the current hardware architecture of the system.

        This method determines the machine's architecture using the `platform` module, returning 
        it as a string. The architecture reflects the type of hardware (e.g., `x86_64` for 64-bit 
        Intel/AMD processors, `arm64` for 64-bit ARM processors).

        Returns:
        --------
        - **str**: A string representing the current hardware architecture (e.g., 'x86_64', 'arm64').

        Example Usage:
        --------------
        ```python
        runtime_util = RuntimeUtil()
        architecture = runtime_util.extract_arch()
        print(f"Architecture: {architecture}")
        # Output: 'x86_64', 'arm64', etc., depending on the machine
        ```

        Notes:
        ------
        - The architecture is derived from the machine's hardware and is independent of the operating system.
        - Useful for verifying compatibility with specific binaries, dependencies, or configurations.
        """
        return platform.machine()
