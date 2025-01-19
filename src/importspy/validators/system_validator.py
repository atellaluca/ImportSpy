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
                 systems_1:List[System],
                 systems_2:List[System]):
        if not systems_1:
            return
        if not systems_2:
            raise(ValueError(Errors.ELEMENT_MISSING.format(systems_1)))
        cv = CommonValidator()
        system_2 = systems_2[0]
        for system_1 in systems_1:
            if system_1.os == system_2.os:
                if system_1.envs:
                    cv.dict_validate(system_1.envs, system_2.envs, Errors.ENV_VAR_MISSING, Errors.ENV_VAR_MISMATCH)
                if system_1.pythons:
                    self._python_validator.validate(system_1.pythons, system_2.pythons)
                return