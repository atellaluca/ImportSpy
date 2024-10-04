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
        """
        Imports the module that called this function dynamically, with an optional validation step.
        
        This method inspects the stack to find the caller's module and re-imports it dynamically.
        If a validation function is provided, the module is returned only if it passes the validation.
        Raises a ValueError if recursion within the same module is detected.

        :param validation: 
            A callable that takes the imported module as an argument and returns 
            a boolean indicating whether the module passes validation. If `None`, 
            no validation is performed.
        :type validation: Callable[[ModuleType], bool] | None

        :raises ValueError: 
            If the method detects recursion within the same module, i.e., when 
            the caller and current frames originate from the same file.

        :return: 
            The imported module, or `None` if the validation function is provided and fails.
        :rtype: ModuleType | None
        """
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