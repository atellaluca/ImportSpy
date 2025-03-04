from ..models import Argument
from ..errors import Errors
from ..constants import Constants
from typing import (
    Optional,
    List
)
from importspy.log_manager import LogManager

class ArgumentValidator:

    def __init__(self):
        self.logger = LogManager().get_logger(self.__class__.__name__)

    def validate(self,
                 arguments_1: List[Argument],
                 arguments_2: List[Argument],
                 function_name:str,
                 class_name: Optional[str]=""
                 ):
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
                    details=f"There aren't any arguments; current arguments_1: {arguments_1}"
                )
            )
            return
        if not arguments_2:
            self.logger.debug(
                Constants.LOG_MESSAGE_TEMPLATE.format(
                    operation="Checking arguments_2 when arguments_1 is missing",
                    status="Finished",
                    details=f"There aren't any arguments_2; current arguments_2: {arguments_2}"
                )
            )
            raise(ValueError(Errors.ELEMENT_MISSING.format(arguments_1)))
        for argument_1 in arguments_1:
            self.logger.debug(
                Constants.LOG_MESSAGE_TEMPLATE.format(
                    operation="Argument validating",
                    status="Progress",
                    details=f"Current argument_1: {argument_1}"
                )
            )
            if argument_1.name not in set(map(lambda argument: argument.name, arguments_2)):
                Constants.LOG_MESSAGE_TEMPLATE.format(
                    operation="Checking if argument_1 is in arguments_2",
                    status="Finished",
                    details=Errors.ARGUMENT_MISSING.format(f"{argument_1.name}", context_name, )
                )
                raise ValueError(Errors.ARGUMENT_MISSING.format(f"{argument_1.name}", context_name))
        for argument_1 in arguments_1:
            argument_2:Argument =  next((argument for argument in arguments_2 if argument.name == argument_1.name), None)
            if not argument_2:
                raise(ValueError(Errors.ELEMENT_MISSING.format(argument_1)))
            if argument_1.annotation and argument_1.annotation != argument_2.annotation:
                raise ValueError(Errors.ARGUMENT_MISMATCH.format(Constants.ANNOTATION, argument_1.name, argument_1.annotation, argument_2.annotation))
            if argument_1.value != argument_2.value:
                raise ValueError(Errors.ARGUMENT_MISMATCH.format(Constants.VALUE, argument_1.name, argument_1.value, argument_2.value))
        return True
                