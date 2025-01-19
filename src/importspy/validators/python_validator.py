from ..models import Python
from ..errors import Errors
from .module_validator import ModuleValidator
from ..log_manager import LogManager
from ..constants import Constants

class PythonValidator:

    def __init__(self):
        self.logger = LogManager().get_logger(self.__class__.__name__)
        self._module_validator = ModuleValidator()

    def validate(self,
                 python_1:Python,
                 python_2:Python):
        self.logger.debug(
            Constants.LOG_MESSAGE_TEMPLATE.format(
                operation="Python validating",
                status="Starting",
                details=f"Expected python: {python_1} ; Current python: {python_2}"
            )
        )
        if not python_1:
            return
        if not python_2:
            raise(ValueError(Errors.ELEMENT_MISSING.format(python_1)))
        if python_1.version == python_2.version \
            and python_1.interpreter == python_2.interpreter:
            if python_2.modules:
                self._module_validator.validate(python_1.modules, python_2.modules[0])
            return True
        return False