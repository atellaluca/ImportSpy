"""
importspy.validators.argument_validator
=======================================

This module provides validation for function or method arguments
within Python modules being inspected by ImportSpy.

The `ArgumentValidator` compares declared arguments from the import contract
against the actual arguments found in the target module, ensuring:
- Name consistency
- Type annotation compliance
- Default value consistency

This validator is typically called from FunctionValidator or ClassValidator
as part of a full SpyModel validation.
"""

from ..models import Argument
from ..errors import Errors
from ..constants import Constants
from typing import Optional, List
from importspy.log_manager import LogManager


class ArgumentValidator:
    """
    Validates argument definitions within functions or methods.

    This class ensures that each expected argument matches its actual counterpart
    in terms of name, type annotation, and default value.

    Attributes
    ----------
    logger : logging.Logger
        Internal logger used for debug output.

    Methods
    -------
    validate(arguments_1, arguments_2, function_name, class_name="")
        Compare two sets of arguments and raise errors for mismatches.
    """

    def __init__(self):
        """
        Initialize the ArgumentValidator with a scoped logger.
        """
        self.logger = LogManager().get_logger(self.__class__.__name__)

    def validate(
        self,
        arguments_1: List[Argument],
        arguments_2: List[Argument],
        function_name: str,
        class_name: Optional[str] = ""
    ):
        """
        Validate function or method arguments for name, type, and value compliance.

        Parameters
        ----------
        arguments_1 : List[Argument]
            List of expected arguments defined in the import contract.

        arguments_2 : List[Argument]
            List of actual arguments found in the inspected module.

        function_name : str
            The name of the function or method being validated.

        class_name : Optional[str], default=""
            The name of the class containing the method (if any), used for error context.

        Returns
        -------
        bool
            True if validation passes without raising an exception.

        Raises
        ------
        ValueError
            - If expected arguments are missing.
            - If type annotations mismatch.
            - If default values differ.

        Example
        -------
        >>> validator = ArgumentValidator()
        >>> validator.validate(
        ...     arguments_1=[Argument(name="x", annotation="int")],
        ...     arguments_2=[Argument(name="x", annotation="int")],
        ...     function_name="my_function"
        ... )
        True
        """
        context_name = f"method {function_name}" if class_name else f"function {function_name}"

        self.logger.debug(
            Constants.LOG_MESSAGE_TEMPLATE.format(
                operation="Attribute validating",
                status="Starting",
                details=f"Expected attributes: {arguments_1} ; Current attributes: {arguments_2}"
            )
        )

        if not arguments_1:
            self.logger.debug(
                Constants.LOG_MESSAGE_TEMPLATE.format(
                    operation="Check if arguments_1 is not none",
                    status="Finished",
                    details=f"No declared arguments to validate; arguments_1: {arguments_1}"
                )
            )
            return

        if not arguments_2:
            self.logger.debug(
                Constants.LOG_MESSAGE_TEMPLATE.format(
                    operation="Checking arguments_2 when arguments_1 is missing",
                    status="Finished",
                    details=f"No actual arguments found; arguments_2: {arguments_2}"
                )
            )
            raise ValueError(Errors.ELEMENT_MISSING.format(arguments_1))

        for argument_1 in arguments_1:
            self.logger.debug(
                Constants.LOG_MESSAGE_TEMPLATE.format(
                    operation="Argument validating",
                    status="Progress",
                    details=f"Current argument_1: {argument_1}"
                )
            )
            if argument_1.name not in set(arg.name for arg in arguments_2):
                raise ValueError(Errors.ARGUMENT_MISSING.format(argument_1.name, context_name))

        for argument_1 in arguments_1:
            argument_2 = next((arg for arg in arguments_2 if arg.name == argument_1.name), None)

            if not argument_2:
                raise ValueError(Errors.ELEMENT_MISSING.format(argument_1))

            if argument_1.annotation and argument_1.annotation != argument_2.annotation:
                raise ValueError(
                    Errors.ARGUMENT_MISMATCH.format(
                        Constants.ANNOTATION,
                        argument_1.name,
                        argument_1.annotation,
                        argument_2.annotation
                    )
                )

            if argument_1.value != argument_2.value:
                raise ValueError(
                    Errors.ARGUMENT_MISMATCH.format(
                        Constants.VALUE,
                        argument_1.name,
                        argument_1.value,
                        argument_2.value
                    )
                )

        return True
