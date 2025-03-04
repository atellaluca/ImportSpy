from ..models import (
    Runtime,
)
from typing import List
from ..errors import Errors
from .system_validator import SystemValidator

class RuntimeValidator:
    """
    Validates runtime configurations for architectural consistency.

    This class compares a list of expected runtime configurations (`runtimes_1`) with
    a list of actual runtime configurations (`runtimes_2`). It ensures that their 
    architectures match and validates the systems within the runtimes.

    Validation Outcomes:
    ---------------------
    1. **Validation Not Necessary (Returns `None`)**:
       - `runtimes_1` is empty, indicating no runtimes to validate.

    2. **Validation Completed Successfully (Returns `None`)**:
       - All runtimes in `runtimes_1` align with the structure of `runtimes_2`.

    3. **Validation Error (Raises `ValueError`)**:
       - `runtimes_2` is not provided while `runtimes_1` is defined.
       - Mismatched architectures or missing system configurations.
    """

    def __init__(self):
        """
        Initializes the RuntimeValidator.

        Creates an instance of `SystemValidator` to handle validation of systems within runtimes.
        """
        self._system_validator = SystemValidator()

    def validate(self, runtimes_1: List[Runtime], runtimes_2: List[Runtime]) -> None:
        """
        Validates a list of expected runtime configurations against actual configurations.

        Parameters:
        -----------
        runtimes_1 : List[Runtime]
            The list of expected runtime configurations to validate.
        runtimes_2 : List[Runtime]
            The list of actual runtime configurations to validate against.

        Returns:
        --------
        None
            - If `runtimes_1` is empty (validation not necessary).
            - If validation completes successfully.

        Raises:
        -------
        ValueError
            - If `runtimes_2` is missing but `runtimes_1` is defined.
            - If discrepancies are found in architectures or systems.
        """
        # Case 1: Validation not necessary
        if not runtimes_1:
            return

        # Case 2: Error - `runtimes_2` is missing
        if not runtimes_2:
            raise ValueError(Errors.ELEMENT_MISSING.format(runtimes_1))

        # Validate each runtime configuration
        runtime_2 = runtimes_2[0]
        for runtime_1 in runtimes_1:
            # Match architecture
            if runtime_1.arch == runtime_2.arch:
                # Validate systems if present
                if runtime_1.systems:
                    self._system_validator.validate(runtime_1.systems, runtime_2.systems)
                return
