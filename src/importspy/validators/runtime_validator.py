"""
importspy.validators.runtime_validator
======================================

Validator for runtime configurations.

This module defines the `RuntimeValidator` class, which ensures that the
runtime architecture and system-level environment of a Python module
conform to what is declared in its import contract.

Delegates system validation to `SystemValidator`.
"""

from ..models import Runtime
from ..errors import Errors
from .system_validator import SystemValidator
from typing import List


class RuntimeValidator:
    """
    Validates runtime architecture and system configurations.

    Attributes
    ----------
    _system_validator : SystemValidator
        Handles validation of OS and platform-specific system expectations.
    """

    def __init__(self):
        """
        Initialize the runtime validator and prepare the system validator.
        """
        self._system_validator = SystemValidator()

    def validate(
        self,
        runtimes_1: List[Runtime],
        runtimes_2: List[Runtime]
    ) -> None:
        """
        Validate expected runtime declarations against actual runtime data.

        Parameters
        ----------
        runtimes_1 : List[Runtime]
            The expected runtime environments declared in the contract.
        runtimes_2 : List[Runtime]
            The actual detected runtime environments from the host system.

        Returns
        -------
        None
            Returned when:
            - `runtimes_1` is empty (no validation required).
            - Validation completes successfully.

        Raises
        ------
        ValueError
            - If `runtimes_2` is missing but expectations are defined.
            - If the architectures do not match.
            - If any contained system-level configuration mismatches are detected.

        Example
        -------
        >>> validator = RuntimeValidator()
        >>> validator.validate([expected_runtime], [actual_runtime])
        """
        if not runtimes_1:
            return

        if not runtimes_2:
            raise ValueError(Errors.ELEMENT_MISSING.format(runtimes_1))

        runtime_2 = runtimes_2[0]

        for runtime_1 in runtimes_1:
            if runtime_1.arch == runtime_2.arch:
                if runtime_1.systems:
                    self._system_validator.validate(runtime_1.systems, runtime_2.systems)
                return
