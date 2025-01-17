from ..models import (
    SpyModel,
    Runtime,
)
from .runtime_validator import RuntimeValidator
from .module_validator import ModuleValidator
from typing import List

class SpyModelValidator:

    def __init__(self):
        self._runtime_validator = RuntimeValidator()
        self._module_validator = ModuleValidator()

    def validate(self,
                  spy_model_1: SpyModel,
                  spy_model_2: SpyModel):
        self._runtimes_validate(spy_model_1.deployments, spy_model_2.deployments[0])        
        self._module_validator.validate([spy_model_1], 
                                       spy_model_2
                                        .deployments[0]
                                        .systems[0]
                                        .pythons[0]
                                        .modules[0])
    
    def _runtimes_validate(self, runtimes_1:List[Runtime], runtime_2:Runtime):
        if not runtimes_1:
            return
        for runtime_1 in runtimes_1:
            self._runtime_validator.validate(runtime_1, runtime_2)
            return
        