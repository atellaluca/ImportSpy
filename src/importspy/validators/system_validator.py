"""
importspy.validators.system_validator
======================================

Validator for system-level configurations.

This module defines the `SystemValidator` class, responsible for validating
operating systems, environment variables, and Python interpreter settings
within a runtime context. 

Delegates:
- Environment and key-value matching to `CommonValidator`
- Python version/interpreter matching to `PythonValidator`
"""

from typing import List
from ..models import System
from ..errors import Errors
from .common_validator import CommonValidator
from .python_validator import PythonValidator


class SystemValidator:
    """
    Validates system-level execution environments.

    This includes:
    - Operating system matching
    - Environment variable validation
    - Python configuration checks (via `PythonValidator`)

    Attributes
    ----------
    _python_validator : PythonValidator
        Handles validation of nested Python interpreter configurations.
    """

    def __init__(self):
        """
        Initialize the system validator and prepare supporting validators.
        """
        self._python_validator = PythonValidator()

    def validate(
        self,
        systems_1: List[System],
        systems_2: List[System]
    ) -> None:
        """
        Validate declared system expectations against actual system properties.

        Parameters
        ----------
        systems_1 : List[System]
            Expected system configurations as declared in the import contract.
        systems_2 : List[System]
            Actual detected system environment.

        Returns
        -------
        None
            Returned when:
            - `systems_1` is empty (no validation required).
            - Validation completes successfully without mismatches.

        Raises
        ------
        ValueError
            - If `systems_2` is missing but expected.
            - If operating systems do not match.
            - If environment variables mismatch or are missing.
            - If any Python interpreter configuration fails validation.

        Example
        -------
        >>> validator = SystemValidator()
        >>> validator.validate([expected_system], [actual_system])
        """
        if not systems_1:
            return

        if not systems_2:
            raise ValueError(Errors.ELEMENT_MISSING.format(systems_1))

        cv = CommonValidator()
        system_2 = systems_2[0]

        for system_1 in systems_1:
            if system_1.os == system_2.os:
                if system_1.envs:
                    cv.dict_validate(
                        system_1.envs,
                        system_2.envs,
                        Errors.ENV_VAR_MISSING,
                        Errors.ENV_VAR_MISMATCH
                    )
                if system_1.pythons:
                    self._python_validator.validate(system_1.pythons, system_2.pythons)
                return
