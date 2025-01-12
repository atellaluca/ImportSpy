"""
System Validation Utilities for ImportSpy

This module provides validation mechanisms to ensure compatibility and correctness 
of system-level configurations. It includes the `SystemValidator` class, which performs 
comparative validation of system attributes such as operating systems and environment 
variables across multiple system configurations.

The utilities in this module are integral to ImportSpy's runtime validation processes, 
helping enforce adherence to predefined `SpyModel` structures.
"""

from ..models import(
    System,
    Python
)
from typing import List
from ..errors import Errors
from .common_validator import CommonValidator
from .python_validator import PythonValidator

class SystemValidator:

    """
    Validator for System-Level Configurations

    The `SystemValidator` class is responsible for validating the compatibility of 
    system configurations. It compares a list of expected systems with an actual 
    system instance, ensuring consistency in operating system types, environment 
    variables, and Python versions.

    Key Features:
    --------------
    - Validates system configurations, including OS and environment variables.
    - Integrates with the `PythonValidator` to verify Python runtime consistency.
    - Raises informative errors when mismatches are detected.

    Methods:
    --------
    - `validate(systems_1, system_2)`: Compares a list of expected systems with a given system instance.
    - `_check_systems(systems_1, system_2)`: Internal method to validate OS and environment variable consistency.

    Example Usage:
    --------------
    ```python
    from importspy.models import System
    from importspy.validators.system_validator import SystemValidator

    systems_expected = [System(os="linux", envs={"ENV_VAR": "value"})]
    system_actual = System(os="linux", envs={"ENV_VAR": "value"})

    validator = SystemValidator()
    try:
        validator.validate(systems_expected, system_actual)
        print("System validation passed.")
    except ValueError as e:
        print(f"System validation failed: {e}")
    ```
    This example demonstrates how the `SystemValidator` can validate system configurations.
    """

    def validate(self,
                 systems_1:List[System],
                 system_2:System):
        """
        Validates a list of expected systems against a single system instance.

        This method ensures that each expected system in the list matches the 
        given system instance in terms of operating system type, environment 
        variables, and Python configurations. If mismatches are found, a 
        `ValueError` is raised with details.

        Parameters:
        -----------
        systems_1 : List[System]
            A list of `System` objects representing expected configurations.
        system_2 : System
            A `System` object representing the actual configuration to validate.

        Raises:
        -------
        ValueError
            If the system configurations do not match.

        Notes:
        ------
        This method delegates Python validation to the `PythonValidator`.
        """
        self._check_systems(systems_1, system_2)
        for system_1 in systems_1:
            if system_1.pythons: 
                python_2:Python = system_2.pythons[0]
                PythonValidator().validate(system_1.pythons, python_2)
                return
    
    def _check_systems(self,
                       systems_1:List[System],
                       system_2:System):
        """
        Internal method to validate operating systems and environment variables.

        This method compares the OS and environment variables of each expected 
        system with the actual system. If a match is found, the validation passes; 
        otherwise, a `ValueError` is raised.

        Parameters:
        -----------
        systems_1 : List[System]
            A list of `System` objects representing expected configurations.
        system_2 : System
            A `System` object representing the actual configuration.

        Raises:
        -------
        ValueError
            If no matching system is found or environment variables mismatch.

        Notes:
        ------
        This method uses `CommonValidator` for environment variable validation.
        """
        cv = CommonValidator()
        for system_1 in systems_1:
            if system_1.os == system_2.os:
                cv.dict_validate(system_1.envs, system_2.envs, Errors.ENV_VAR_MISSING, Errors.ENV_VAR_MISMATCH)
                return
        raise ValueError(Errors.SYSTEM_MISSING.format(system_2))