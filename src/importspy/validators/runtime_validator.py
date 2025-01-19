from ..models import (
    Runtime,
    System
)
from typing import List
from ..errors import Errors
from .system_validator import SystemValidator

class RuntimeValidator:

    def __init__(self):
        self._system_validator = SystemValidator()
    
    def validate(self, runtime_1: Runtime, runtime_2: Runtime):
        if not runtime_1:
            return
        if not runtime_2:
            raise(ValueError(Errors.ELEMENT_MISSING.format(runtime_1)))
        if runtime_1.arch == runtime_2.arch:
            if runtime_2.systems:
                self._systems_validate(runtime_1.systems, runtime_2.systems[0])
            return True
        return False
    
    def _systems_validate(self, systems_1:List[System], system_2:System):
        for system_1 in systems_1:
            self._system_validator.validate(system_1, system_2)
