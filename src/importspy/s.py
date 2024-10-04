import inspect
import importlib.util
import sys
from typing import Callable
from types import ModuleType
from .errors import Errors

class Spy:

    def importspy(self, 
                   validation: Callable[[ModuleType], bool] | 
                   None = None) -> ModuleType:
        stack = inspect.stack()
        current_frame : inspect.FrameInfo = stack[1]
        caller_frame: inspect.FrameInfo = stack[-1]
        if current_frame.filename == caller_frame.filename:
            raise ValueError(Errors.ANALYSIS_RECURSION_WARNING)
        info_module = inspect.getmodule(caller_frame.frame)
        spec = importlib.util.spec_from_file_location(info_module.__name__, info_module.__file__)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        sys.modules[module.__name__] = module
        return module if not validation else module if validation(module) else None