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
from ..models import (
    System,
    Environment
)
from ..errors import Errors
from .python_validator import PythonValidator
from ..constants import Constants
from .variable_validator import VariableValidator
from ..contexts import SimpleVariableContext

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
        self._environment_validator = SystemValidator.EnvironmentValidator()

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
        
        system_2 = systems_2[0]

        for system_1 in systems_1:
            if system_1.os == system_2.os:
                if system_1.environment:
                    self._environment_validator.validate(system_1.environment, system_2.environment)
                if system_1.pythons:
                    self._python_validator.validate(system_1.pythons, system_2.pythons)
                return

    class EnvironmentValidator:

        def __init__(self):
            self._variable_validator = VariableValidator(context=SimpleVariableContext(Constants.SCOPE_ENVIRONMENT))
        
        def validate(self,
                    environment_1:Environment,
                    environment_2: Environment):
            
            if not environment_1:
                return

            if not environment_2:
                raise ValueError(Errors.ELEMENT_MISSING.format(environment_1))
            
            variables_2 = environment_2.variables

            if environment_1.variables:
                variables_1 = environment_1.variables
                self._variable_validator.validate(variables_1, variables_2)
                return