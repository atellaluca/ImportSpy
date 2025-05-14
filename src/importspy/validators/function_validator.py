from ..models import Function
from ..errors import Errors
from ..constants import Constants
from typing import List, Optional
from ..log_manager import LogManager
from .variable_validator import VariableValidator
from ..contexts import (
    Context,
    MethodArgumentContext
)


class FunctionValidator:

    def __init__(self):

        self._variable_validator = VariableValidator(context=current_context)

    def validate(
        self,
        functions_1: List[Function],
        functions_2: List[Function],
    ) -> Optional[bool]:
 
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
                    Errors.ELEMENT_MISMATCH.format(context_name, function_1.name)
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
