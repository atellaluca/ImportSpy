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
    
    def validate(self, runtimes_1: List[Runtime], runtimes_2: List[Runtime]):
        if not runtimes_1:
            return
        if not runtimes_2:
            raise(ValueError(Errors.ELEMENT_MISSING.format(runtimes_1)))
        runtime_2 = runtimes_2[0]
        for runtime_1 in runtimes_1:
            if runtime_1.arch == runtime_2.arch:
                if runtime_1.systems:
                    self._system_validator.validate(runtime_1.systems, runtime_2.systems)
                return
