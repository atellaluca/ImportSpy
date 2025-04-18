from ..log_manager import LogManager
from ..models import Variable
from ..constants import Constants
from ..errors import Errors
from typing import List

class VariableValidator:

    def __init__(self):
        self.logger = LogManager().get_logger(self.__class__.__name__)

    def validate(
        self,
        variables_1: List[Variable],
        variables_2: List[Variable],
    ):
        self.logger.debug(f"Type of variables_1: {type(variables_1)}")
        self.logger.debug(
            Constants.LOG_MESSAGE_TEMPLATE.format(
                operation="Variable validating",
                status="Starting",
                details=f"Expected Variables: {variables_1} ; Current Variables: {variables_2}"
            )
        )

        if not variables_1:
            self.logger.debug(
                Constants.LOG_MESSAGE_TEMPLATE.format(
                    operation="Check if variables_1 is not none",
                    status="Finished",
                    details=f"No expected Variables; variables_1: {variables_1}"
                )
            )
            return

        if not variables_2:
            self.logger.debug(
                Constants.LOG_MESSAGE_TEMPLATE.format(
                    operation="Checking variables_2 when variables_1 is missing",
                    status="Finished",
                    details=f"No actual Variables found; variables_2: {variables_2}"
                )
            )
            raise ValueError(Errors.ELEMENT_MISSING.format(variables_1))

        for vars_1 in variables_1:
            self.logger.debug(
                Constants.LOG_MESSAGE_TEMPLATE.format(
                    operation="Variable validating",
                    status="Progress",
                    details=f"Current vars_1: {vars_1}"
                )
            )
            if vars_1.name not in {var.name for var in variables_2}:
                self.logger.debug(Constants.LOG_MESSAGE_TEMPLATE.format(
                    operation="Checking if vars_1 is in variables_2",
                    status="Finished",
                    details=Errors.VARIABLE_MISSING.format(
                        f"{vars_1.name}={vars_1.value}"
                    )
                ))
                raise ValueError(
                    Errors.VARIABLE_MISSING.format(
                        f"{vars_1.name}={vars_1.value}"
                    )
                )

        for vars_1 in variables_1:
            vars_2 = next((var for var in variables_2 if var.name == vars_1.name), None)
            if not vars_2:
                raise ValueError(Errors.ELEMENT_MISSING.format(variables_1))

            if vars_1.annotation and vars_1.annotation != vars_2.annotation:
                raise ValueError(
                    Errors.VARIABLE_MISMATCH.format(
                        Constants.ANNOTATION,
                        vars_1.name,
                        vars_1.annotation,
                        vars_2.annotation
                    )
                )

            if vars_1.value != vars_2.value:
                raise ValueError(
                    Errors.VARIABLE_MISMATCH.format(
                        Constants.VALUE,
                        vars_1.name,
                        vars_1.value,
                        vars_2.value
                    )
                )

        return True