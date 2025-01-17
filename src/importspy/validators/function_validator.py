from ..models import Function
from ..errors import Errors
from ..constants import Constants
from typing import (
    List,
    Optional
)
from ..log_manager import LogManager

class FunctionValidator:

    def __init__(self):
        self.logger = LogManager().get_logger(self.__class__.__name__)

    def validate(self,
                 functions_1:List[Function],
                 functions_2:List[Function],
                 classname:Optional[str]="",
                 ):
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
                    details=f"There aren't any attributes; current functions_1: {functions_1}"
                )
            )
            return
        if functions_1 and not functions_2:
            self.logger.debug(
                Constants.LOG_MESSAGE_TEMPLATE.format(
                    operation="Checking functions_1 and functions_2",
                    status="Finished",
                    details=f"There aren't any functions_2; current functions_2: {functions_2}"
                )
            )
            return True
        if not functions_2:
            self.logger.debug(
                Constants.LOG_MESSAGE_TEMPLATE.format(
                    operation="Checking functions_2 when functions_1 is missing",
                    status="Finished",
                    details=f"There aren't any functions_2; current functions_2: {functions_2}"
                )
            )
            return False
        for function_1 in functions_1:
            self.logger.debug(
                Constants.LOG_MESSAGE_TEMPLATE.format(
                    operation="Function validating",
                    status="Progress",
                    details=f"Current functions_1: {functions_1}"
                )
            )
            if function_1.name not in set(map(lambda function: function.name, functions_2)):
                self.logger.debug(Constants.LOG_MESSAGE_TEMPLATE.format(
                    operation="Checking if function_1 is in functions_2",
                    status="Finished for function missing",
                    details=f"function_1: {function_1}; functions_2: {functions_2}")
                )
                raise ValueError(Errors.FUNCTIONS_MISSING.format(
                    context_name, 
                    function_1.name
                    )
                )
        for function_1 in functions_1:
            function_2 =  next((func for func in functions_2 if func.name == function_1.name), None)
            if function_1.return_annotation and \
                function_1.return_annotation != function_2.return_annotation:
                raise ValueError(Errors.FUNCTION_RETURN_ANNONATION_MISMATCH.format(context_name, function_1.name, function_1.return_annotation))
        return True

