from ..models import Python
from ..errors import Errors
from .module_validator import ModuleValidator
from ..log_manager import LogManager
from ..constants import Constants
from typing import List

class PythonValidator:

    def __init__(self):
        self.logger = LogManager().get_logger(self.__class__.__name__)
        self._module_validator = ModuleValidator()

    def validate(self,
                 pythons_1:List[Python],
                 pythons_2:List[Python]):
        self.logger.debug(
            Constants.LOG_MESSAGE_TEMPLATE.format(
                operation="Python validating",
                status="Starting",
                details=f"Expected python: {pythons_1} ; Current python: {pythons_2}"
            )
        )
        if not pythons_1:
            return
        if not pythons_2:
            raise(ValueError(Errors.ELEMENT_MISSING.format(pythons_1)))
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
                return
    
    def _is_python_match(self, python_1:Python, python_2:Python):
        if python_1.version and python_1.interpreter:
            return (
                python_1.version == python_2.version  
                    and python_1.interpreter == python_2.interpreter
            )
        if python_1.version:
            return python_1.version == python_2.version
        if python_1.interpreter:
            return python_1.interpreter == python_2.interpreter
        return True
        