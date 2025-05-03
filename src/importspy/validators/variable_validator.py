"""
importspy.validators.variable_validator
=======================================

This module provides validation logic for variables, including standalone variables,
function arguments, class attributes, and environment variables.

Each validation runs in the context of a specific `Context` subclass, which encapsulates
label rendering and scoped error formatting for missing, mismatched, or invalid elements.

Author: ImportSpy Team
License: MIT
"""

from typing import List
from importspy.log_manager import LogManager
from importspy.models import Variable
from importspy.constants import Constants
from importspy.contexts import Context


class VariableValidator:
    """
    Validates lists of `Variable` instances within a given scope-aware context.

    This class compares expected and actual variables for:
    - Presence (missing variables)
    - Value equality
    - Annotation correctness (for typed contexts)

    Attributes
    ----------
    context : Context
        A `Context` subclass instance that defines how to format errors and describe the scope.
    logger : logging.Logger
        Logger used for structured debug output.
    """

    def __init__(self, context: Context):
        """
        Initialize the validator with a context.

        Parameters
        ----------
        context : Context
            A context object that encapsulates the validation scope and error message logic.
        """
        self.context = context
        self.logger = LogManager().get_logger(self.__class__.__name__)

    def validate(
        self,
        variables_1: List[Variable],
        variables_2: List[Variable],
    ):
        """
        Validate two sets of variables for presence, value match, and type annotations.

        Parameters
        ----------
        variables_1 : List[Variable]
            The list of expected variables (from the contract).
        variables_2 : List[Variable]
            The list of actual variables (from the module/system).

        Raises
        ------
        ValueError
            If a variable is missing, has a mismatched value, or fails type annotation validation.
        """
        self.logger.debug(f"Context: {self.context.__class__.__name__} (scope={self.context.scope})")
        self.logger.debug(f"Type of variables_1: {type(variables_1)}")
        self.logger.debug(
            Constants.LOG_MESSAGE_TEMPLATE.format(
                operation="Variable validating",
                status="Starting",
                details=f"Expected Variables: {variables_1} ; Actual Variables: {variables_2}"
            )
        )

        if not variables_1:
            self.logger.debug(
                Constants.LOG_MESSAGE_TEMPLATE.format(
                    operation="Check if variables_1 is not none",
                    status="Finished",
                    details="No expected Variables to validate"
                )
            )
            return

        if not variables_2:
            self.logger.debug(
                Constants.LOG_MESSAGE_TEMPLATE.format(
                    operation="Checking variables_2 when variables_1 is missing",
                    status="Finished",
                    details="No actual Variables found for validation"
                )
            )
            raise ValueError(self.context.format_missing_error())

        for vars_1 in variables_1:
            self.logger.debug(
                Constants.LOG_MESSAGE_TEMPLATE.format(
                    operation="Variable validating",
                    status="Progress",
                    details=f"Current vars_1: {vars_1}"
                )
            )
            if vars_1.name not in {var.name for var in variables_2}:
                raise ValueError(self.context.format_missing_error())

        for vars_1 in variables_1:
            vars_2 = next((var for var in variables_2 if var.name == vars_1.name), None)
            if not vars_2:
                raise ValueError(self.context.format_missing_error())

            # Annotation mismatch (only if not validating env vars)
            if self.context.scope != Constants.SCOPE_ENVIRONMENT and vars_1.annotation and vars_1.annotation != vars_2.annotation:
                raise ValueError(
                    self.context.format_mismatch_error(vars_1.annotation, vars_2.annotation)
                )

            # Value mismatch
            if vars_1.value != vars_2.value:
                raise ValueError(
                    self.context.format_mismatch_error(vars_1.value, vars_2.value)
                )
