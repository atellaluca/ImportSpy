"""Runtime Environment Utilities

Provides a lightweight utility for querying the system's hardware architecture.

This module is used by ImportSpy to enforce architecture-specific constraints
defined in import contracts (e.g., allowing a plugin only on x86_64 or arm64).
It ensures that module imports are aligned with the intended deployment environment.
"""

import logging
import platform

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class RuntimeUtil:
    """Utility class to inspect system architecture.

    This class provides methods to retrieve runtime hardware architecture details,
    which are essential when validating platform-specific import constraints
    in ImportSpy's embedded or CLI modes.
    """

    def extract_arch(self) -> str:
        """Return the name of the machine's hardware architecture.

        Uses `platform.machine()` to retrieve the architecture string, which may vary
        depending on the underlying system (e.g., "x86_64", "arm64", "aarch64").
        This is typically used during contract validation to ensure that the importing
        environment matches expected deployment conditions.

        Returns:
            str: The system's hardware architecture.
        
        Example:
            RuntimeUtil().extract_arch()
            > Output: 'arm64'
        """
        return platform.machine()
