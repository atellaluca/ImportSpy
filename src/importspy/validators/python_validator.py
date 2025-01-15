from ..models import Python
from typing import List
from .module_validator import ModuleValidator
from ..errors import Errors

class PythonValidator:

    def validate(self,
                 python_1:Python,
                 python_2:Python):
        if not python_1:
            return False
        if python_1.version == python_2.version \
            and python_1.interpreter == python_2.interpreter:
            return True
        return False