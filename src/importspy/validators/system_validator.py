from ..models import (
    System,
    Python
)
from ..errors import Errors
from .common_validator import CommonValidator
from .python_validator import PythonValidator
from typing import List

class SystemValidator:

    def __init__(self):
        self._python_validator = PythonValidator()

    def validate(self,
                 system_1:System,
                 system_2:System):
        if not system_1:
            return
        if not system_2:
            raise(ValueError(Errors.ELEMENT_MISSING.format(system_1)))
        cv = CommonValidator()
        if system_1.os == system_2.os:
            if system_1.envs:
                cv.dict_validate(system_1.envs, system_2.envs, Errors.ENV_VAR_MISSING, Errors.ENV_VAR_MISMATCH)
            if system_1.pythons:
                self._pythons_validate(system_1.pythons, system_2.pythons[0])
            return True
        return False
    
    def _pythons_validate(self, pythons_1:List[Python], python_2:Python):
        for python_1 in pythons_1:
            self._python_validator.validate(python_1, python_2)