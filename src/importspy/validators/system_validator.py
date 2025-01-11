from ..models import(
    System,
    Python
)
from typing import List
from ..errors import Errors
from .common_validator import CommonValidator
from .python_validator import PythonValidator

class SystemValidator:

    def validate(self,
                 systems_1:List[System],
                 system_2:System):
        self._check_systems(systems_1, system_2)
        for system_1 in systems_1:
            if system_1.pythons: 
                python_2:Python = system_2.pythons[0]
                PythonValidator().validate(system_1.pythons, python_2)
                return
    
    def _check_systems(self,
                       systems_1:List[System],
                       system_2:System):
        cv = CommonValidator()
        for system_1 in systems_1:
            if system_1.os == system_2.os:
                cv.dict_validate(system_1.envs, system_2.envs, Errors.ENV_VAR_MISSING, Errors.ENV_VAR_MISMATCH)
                return
        raise ValueError(Errors.SYSTEM_MISSING.format(system_2))