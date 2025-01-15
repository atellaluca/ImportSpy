from ..models import (
    SpyModel,
    Runtime,
    System,
    Python,
    Module
)
from .runtime_validator import RuntimeValidator
from .system_validator import SystemValidator
from .module_validator import ModuleValidator
from .python_validator import PythonValidator
from typing import List

class SpyModelValidator:

    runtime_validator = RuntimeValidator()
    system_validator = SystemValidator()
    python_validator = PythonValidator()
    module_validator = ModuleValidator()

    def validate(self,
                  spy_model_1: SpyModel,
                  spy_model_2: SpyModel) -> bool:
        self._runtimes_validate(spy_model_1.deployments, spy_model_2.deployments[0])        
        self.module_validator.validate(spy_model_1, 
                                       spy_model_2
                                        .deployments[0]
                                        .systems[0]
                                        .pythons[0]
                                        .modules[0])
    
    def _runtimes_validate(self, runtimes_1:List[Runtime], runtime_2:Runtime):
        system_2 = runtime_2.systems[0]
        for runtime_1 in runtimes_1:
            self.runtime_validator.validate(runtime_1, runtime_2)
            self._systems_validate(runtimes_1, system_2)
            return

    def _systems_validate(self, systems_1:List[System], system_2:System):
        python_2 = system_1.pythons[0]
        for system_1 in systems_1:
            self.system_validator.validate(system_1, system_2)
            self._pythons_validate(system_1.pythons, python_2)
    
    def _pythons_validate(self, pythons_1:List[Python], python_2:Python):
        for python_1 in pythons_1:
            self.python_validator.validate(python_1, python_2)
            
    def _modules_validate(self, modules_1: List[Module], modules_2: List[Module]):
        for module_1 in modules_1:
            module_2 = next((module for module in modules_2 if module_1.filename == module_1.filename), None)
            self.module_validator.validate(module_1, module_2)
        