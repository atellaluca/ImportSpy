from ..models import Python
from ..errors import Errors
from .module_validator import ModuleValidator
from ..log_manager import LogManager
from ..constants import Constants
from typing import List, Optional

class PythonValidator:
    """
    Validates Python configurations for structural consistency.

    This class compares a list of expected Python configurations (`pythons_1`) with 
    a list of actual Python configurations (`pythons_2`), ensuring that their 
    versions, interpreters, and modules match the expected structure.

    Validation Outcomes:
    ---------------------
    1. **Validation Not Necessary (Returns `None`)**:
       - `pythons_1` is empty, indicating no Python configurations to validate.

    2. **Validation Completed Successfully (Returns `None`)**:
       - All Python configurations in `pythons_1` align with the structure of `pythons_2`.

    3. **Validation Error (Raises `ValueError`)**:
       - Mismatched or missing versions, interpreters, or modules.
       - `pythons_2` is not provided while `pythons_1` is defined.
    """

    def __init__(self):
        """
        Initializes the PythonValidator.

        Creates an instance of `ModuleValidator` to handle validation of modules within Python configurations.
        """
        self.logger = LogManager().get_logger(self.__class__.__name__)
        self._module_validator = ModuleValidator()

    def validate(self,
                 pythons_1: List[Python],
                 pythons_2: Optional[List[Python]]) -> Optional[None]:
        """
        Validates a list of expected Python configurations against actual configurations.

        Parameters:
        -----------
        pythons_1 : List[Python]
            The list of expected Python configurations to validate.
        pythons_2 : List[Python], optional
            The list of actual Python configurations to validate against.

        Returns:
        --------
        None
            - If `pythons_1` is empty (validation not necessary).
            - If validation completes successfully.

        Raises:
        -------
        ValueError
            - If `pythons_2` is missing but `pythons_1` is defined.
            - If discrepancies are found in versions, interpreters, or modules.
        """
        # Case 1: Validation not necessary
        if not pythons_1:
            return

        # Case 2: Error - `pythons_2` is missing
        if not pythons_2:
            raise ValueError(Errors.ELEMENT_MISSING.format(pythons_1))

        # Validate each Python configuration
        python_2 = pythons_2[0]
        for python_1 in pythons_1:
            self.logger.debug(
                Constants.LOG_MESSAGE_TEMPLATE.format(
                    operation="Python validating",
                    status="Progress",
                    details=f"Expected python: {python_1} ; Current python: {python_2}"
                )
            )
            if self._is_python_match(python_1, python_2):
                # Validate modules if present
                if python_2.modules:
                    self._module_validator.validate(python_1.modules, python_2.modules[0])
                return

    def _is_python_match(self, python_1: Python, python_2: Python) -> bool:
        """
        Checks if two Python configurations match based on version and interpreter.

        Parameters:
        -----------
        python_1 : Python
            The expected Python configuration.
        python_2 : Python
            The actual Python configuration.

        Returns:
        --------
        bool
            - `True` if the configurations match based on defined criteria.
            - `False` otherwise.
        """
        # Match both version and interpreter if both are defined
        if python_1.version and python_1.interpreter:
            return (
                python_1.version == python_2.version and
                python_1.interpreter == python_2.interpreter
            )

        # Match version only
        if python_1.version:
            return python_1.version == python_2.version

        # Match interpreter only
        if python_1.interpreter:
            return python_1.interpreter == python_2.interpreter

        # Default to True if no specific criteria are defined
        return True
