from ..models import (
    System,
    Python
)
from ..errors import Errors
from .common_validator import CommonValidator
from .python_validator import PythonValidator
from typing import List

class SystemValidator:
    """
    Validates the structure and configuration of system environments.

    This validator ensures that the provided `System` configurations (`systems_1`)
    align with the actual `System` instances (`systems_2`). It checks operating
    systems, environment variables, and Python configurations.

    Validation Outcomes:
    ---------------------
    1. **Validation Not Necessary (Returns `None`)**:
       - No systems are defined in `systems_1`.

    2. **Validation Completed Successfully (Returns `None`)**:
       - All aspects of `systems_1` match those of `systems_2`.

    3. **Validation Error (Raises `ValueError`)**:
       - Discrepancies are found between `systems_1` and `systems_2`.
       - Missing configurations in `systems_2`.
    """

    def __init__(self):
        """
        Initializes the SystemValidator.

        Creates an instance of `PythonValidator` to handle the validation
        of Python configurations within systems.
        """
        self._python_validator = PythonValidator()

    def validate(self,
                 systems_1: List[System],
                 systems_2: List[System]) -> None:
        """
        Validates the structure of expected `System` configurations against actual `System` instances.

        Parameters:
        -----------
        systems_1 : List[System]
            The expected list of `System` configurations to validate.
        systems_2 : List[System]
            The actual list of `System` instances to validate against.

        Returns:
        --------
        None
            - If validation is not necessary or completes successfully.

        Raises:
        -------
        ValueError
            - If any discrepancies or missing elements are detected in `systems_2`.
        """
        if not systems_1:
            return
        if not systems_2:
            raise ValueError(Errors.ELEMENT_MISSING.format(systems_1))

        cv = CommonValidator()
        system_2 = systems_2[0]

        for system_1 in systems_1:
            # Validate the operating system
            if system_1.os == system_2.os:
                # Validate environment variables
                if system_1.envs:
                    cv.dict_validate(
                        system_1.envs,
                        system_2.envs,
                        Errors.ENV_VAR_MISSING,
                        Errors.ENV_VAR_MISMATCH
                    )
                # Validate Python configurations
                if system_1.pythons:
                    self._python_validator.validate(system_1.pythons, system_2.pythons)
                return
