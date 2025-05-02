"""
importspy.validators.function_validator
=======================================

Validator for function declarations and signatures.

This module defines the `FunctionValidator`, responsible for verifying that functions
defined in a Python module (or class) match those specified in an import contract.
It ensures that:
- Each expected function is present.
- Return annotations are correct.
- Function arguments match in name, annotation, and value.

This validator uses `ArgumentValidator` to validate function arguments.
"""

from ..models import Function
from ..errors import Errors
from ..constants import Constants
from typing import List, Optional
from ..log_manager import LogManager
from .argument_validator import ArgumentValidator


class FunctionValidator:
    """
    Validator for function declarations and signatures.

    Attributes
    ----------
    logger : logging.Logger
        Logger used for debug tracing.
    _argument_validator : ArgumentValidator
        Helper validator to handle argument validation.
    """

    def __init__(self):
        """
        Initialize the function validator and argument checker.
        """
        self.logger = LogManager().get_logger(self.__class__.__name__)
        self._argument_validator = ArgumentValidator()

    def validate(
        self,
        functions_1: List[Function],
        functions_2: List[Function],
        classname: Optional[str] = ""
    ) -> Optional[bool]:
        """
        Validate a list of expected functions against actual module functions.

        Parameters
        ----------
        functions_1 : List[Function]
            The list of expected functions (from import contract).
        functions_2 : List[Function]
            The actual functions extracted from the module.
        classname : Optional[str], default=""
            If validating class methods, the class name (for error context).

        Returns
        -------
        Optional[bool]
            True if validation passes, None if nothing to validate.

        Raises
        ------
        ValueError
            If:
            - A function is missing.
            - Return annotations differ.
            - Argument validation fails.

        Example
        -------
        >>> validator = FunctionValidator()
        >>> validator.validate(expected_functions, actual_functions, classname="MyService")
        """
        context_name = f"method in class {classname}" if classname else "function"

        self.logger.debug(
            Constants.LOG_MESSAGE_TEMPLATE.format(
                operation="Function validating",
                status="Starting",
                details=f"Expected functions: {functions_1} ; Current functions: {functions_2}"
            )
        )

        if not functions_1:
            self.logger.debug(
                Constants.LOG_MESSAGE_TEMPLATE.format(
                    operation="Check if functions_1 is not none",
                    status="Finished",
                    details="No functions to validate"
                )
            )
            return None

        if not functions_2:
            self.logger.debug(
                Constants.LOG_MESSAGE_TEMPLATE.format(
                    operation="Checking functions_2 when functions_1 is missing",
                    status="Finished",
                    details="No actual functions found"
                )
            )
            raise ValueError(Errors.ELEMENT_MISSING.format(functions_1))

        for function_1 in functions_1:
            self.logger.debug(
                Constants.LOG_MESSAGE_TEMPLATE.format(
                    operation="Function validating",
                    status="Progress",
                    details=f"Current function: {function_1}"
                )
            )
            if function_1.name not in {f.name for f in functions_2}:
                self.logger.debug(
                    Constants.LOG_MESSAGE_TEMPLATE.format(
                        operation="Checking if function_1 is in functions_2",
                        status="Finished for function missing",
                        details=f"function_1: {function_1}; functions_2: {functions_2}"
                    )
                )
                raise ValueError(
                    Errors.FUNCTIONS_MISSING.format(context_name, function_1.name)
                )

        for function_1 in functions_1:
            function_2 = next((f for f in functions_2 if f.name == function_1.name), None)
            if not function_2:
                raise ValueError(Errors.ELEMENT_MISSING.format(function_1))

            self._argument_validator.validate(
                function_1.arguments,
                function_2.arguments,
                function_1.name,
                classname
            )

            if function_1.return_annotation and function_1.return_annotation != function_2.return_annotation:
                raise ValueError(
                    Errors.FUNCTION_RETURN_ANNOTATION_MISMATCH.format(
                        context_name,
                        function_1.name,
                        function_1.return_annotation,
                        function_2.return_annotation
                    )
                )

        self.logger.debug(
            Constants.LOG_MESSAGE_TEMPLATE.format(
                operation="Function validating",
                status="Completed",
                details="Validation successful."
            )
        )
