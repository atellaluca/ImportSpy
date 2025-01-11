from ..models import Python
from typing import List
from .module_validator import ModuleValidator
from ..errors import Errors

class PythonValidator:

    def validate(self,
                 pythons_1:List[Python],
                 python_2:Python):
        self._check_pythons(pythons_1, python_2)
        for python_1 in pythons_1:
            if python_1.modules:
                ModuleValidator().validate(python_1.modules, python_2.modules[0])
    
    def _check_pythons(self,
                       pythons_1:List[Python],
                       python_2:Python):
        for python_1 in pythons_1:
            if python_1.version == python_2.version \
                and python_1.interpreter == python_2.interpreter:
                return
        raise ValueError(Errors.PYTHON_MISSING.format(python_2))