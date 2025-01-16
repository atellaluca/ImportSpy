from ..models import System
from ..errors import Errors
from .common_validator import CommonValidator

class SystemValidator:

    def validate(self,
                 system_1:System,
                 system_2:System):
        if not system_1:
            return None
        if system_1 and not system_2:
            return True
        if not system_2:
            return False
        cv = CommonValidator()
        if system_1.os == system_2.os:
            if system_1.envs:
                return cv.dict_validate(system_1.envs, system_2.envs, Errors.ENV_VAR_MISSING, Errors.ENV_VAR_MISMATCH)
            return True
        return False
        
        