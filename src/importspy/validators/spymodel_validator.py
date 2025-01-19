from ..models import (
    SpyModel,
    Runtime,
)
from .runtime_validator import RuntimeValidator
from .module_validator import ModuleValidator

class SpyModelValidator:

    def __init__(self):
        self._runtime_validator = RuntimeValidator()
        self._module_validator = ModuleValidator()

    def validate(self,
                  spy_model_1: SpyModel,
                  spy_model_2: SpyModel):
        self._runtime_validator.validate(spy_model_1.deployments, spy_model_2.deployments)        
        self._module_validator.validate([spy_model_1], 
                                       spy_model_2
                                        .deployments[0]
                                        .systems[0]
                                        .pythons[0]
                                        .modules[0])
        