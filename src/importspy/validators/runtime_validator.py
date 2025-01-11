from ..models import Runtime
from ..models import System
from typing import List
from ..errors import Errors
from .system_validator import SystemValidator

class RuntimeValidator:

    def validate(self,
                 runtimes_1:List[Runtime],
                 runtime_2:Runtime):
        self._check_runtimes(runtimes_1, runtime_2)
        for runtime_1 in runtimes_1:
            if runtime_1.systems:
                system_2:System = runtime_2.systems[0]
                SystemValidator().validate(runtime_1.systems, system_2)
                return
    
    def _check_runtimes(self,
                        runtimes_1:List[Runtime],
                        runtime_2: Runtime):
        for runtime_1 in runtimes_1:
            if runtime_1.arch == runtime_2.arch:
                return
        raise ValueError(Errors.RUNTIME_MISSING.format(runtime_2))