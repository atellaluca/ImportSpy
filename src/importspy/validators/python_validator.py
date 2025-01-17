from ..models import Python
from typing import List
from .module_validator import ModuleValidator

class PythonValidator:

    def __init__(self):
        self._module_validator = ModuleValidator()

    def validate(self,
                 python_1:Python,
                 python_2:Python):
        if not python_1:
            return
        if python_1 and not python_2:
            return True
        if not python_2:
            return False
        self._module_validator.validate(python_1.modules, python_2.modules[0])
        if python_1.version == python_2.version \
            and python_1.interpreter == python_2.interpreter:
            return True
        return False