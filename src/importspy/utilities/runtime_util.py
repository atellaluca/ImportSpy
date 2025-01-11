import logging
import platform

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

class RuntimeUtil:
    

    def extract_arch(self) -> str:
        """
        Extract the current hardware architecture of the system.

        This function retrieves the machine's hardware architecture using the `platform` module and returns it as a string. 
        The architecture describes the hardware type, such as `x86_64` for 64-bit Intel/AMD processors or `arm64` for 64-bit ARM processors.

        Returns:
        --------
        - **str**: A string representing the current hardware architecture of the system.

        Example Usage:
        --------------
        ```python
        arch = extract_arch()
        print(arch)
        # Output: 'x86_64', 'arm64', or similar based on the system
        ```

        Notes:
        ------
        - The output depends on the hardware of the machine and not the operating system.
        - This function is useful for determining compatibility with specific binaries or packages.
        """
        return platform.machine()
