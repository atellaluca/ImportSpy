"""
importspy.validators.python_validator
=====================================

Validator for Python runtime configurations.

This module defines the `PythonValidator` class, responsible for validating
the Python version, interpreter, and associated modules declared in an
import contract against the actual Python runtime context.

Delegates module-level validation to `ModuleValidator`.
"""

from ..models import Python
from ..errors import Errors
from .module_validator import ModuleValidator
from ..log_manager import LogManager
from ..constants import Constants
from typing import List, Optional


class PythonValidator:
    """
    Validates Python runtime configuration and associated modules.

    Attributes
    ----------
    logger : logging.Logger
        Logger instance for debugging and tracing.
    _module_validator : ModuleValidator
        Validator for modules within the Python configuration.
    """

    def __init__(self):
        """
        Initialize the validator and internal module validator.
        """
        self.logger = LogManager().get_logger(self.__class__.__name__)
        self._module_validator = ModuleValidator()

    def validate(
        self,
        pythons_1: List[Python],
        pythons_2: Optional[List[Python]]
    ) -> Optional[None]:
        """
        Validate a list of expected Python environments against actual ones.

        Parameters
        ----------
        pythons_1 : List[Python]
            Expected Python configurations from the contract.
        pythons_2 : Optional[List[Python]]
            Actual Python runtime details extracted from the system.

        Returns
        -------
        None
            Returned when:
            - `pythons_1` is empty (no validation needed).
            - Validation succeeds.

        Raises
        ------
        ValueError
            If `pythons_2` is missing or does not match
            the declared expectations in `pythons_1`.

        Example
        -------
        >>> validator = PythonValidator()
        >>> validator.validate([expected_python], [actual_python])
        """
        if not pythons_1:
            return

        if not pythons_2:
            raise ValueError(Errors.ELEMENT_MISSING.format(pythons_1))

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
                if python_2.modules:
                    self._module_validator.validate(python_1.modules, python_2.modules[0])
                return

    def _is_python_match(
        self,
        python_1: Python,
        python_2: Python
    ) -> bool:
        """
        Determine whether two Python configurations match.

        Parameters
        ----------
        python_1 : Python
            Expected configuration.
        python_2 : Python
            Actual system configuration.

        Returns
        -------
        bool
            `True` if the two configurations match according to the declared criteria,
            otherwise `False`.

        Matching Criteria
        -----------------
        - If both version and interpreter are defined: match both.
        - If only version is defined: match version.
        - If only interpreter is defined: match interpreter.
        - If none are defined: match anything (default `True`).
        """
        if python_1.version and python_1.interpreter:
            return (
                python_1.version == python_2.version and
                python_1.interpreter == python_2.interpreter
            )

        if python_1.version:
            return python_1.version == python_2.version

        if python_1.interpreter:
            return python_1.interpreter == python_2.interpreter

        return True
