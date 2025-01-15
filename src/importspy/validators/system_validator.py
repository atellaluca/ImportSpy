from ..models import System
from ..errors import Errors
from .common_validator import CommonValidator

class SystemValidator:

    def validate(self,
                 system_1:System,
                 system_2:System):
        cv = CommonValidator()
        if system_1.os == system_2.os:
            return cv.dict_validate(system_1.envs, system_2.envs, Errors.ENV_VAR_MISSING, Errors.ENV_VAR_MISMATCH)
        return False
        
        