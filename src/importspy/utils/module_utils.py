import inspect
import importlib.util
import sys
from types import ModuleType

def inspect_module():
    """
    Inspect the stack to find the calling module and re-import it dynamically.

    This method analyzes the call stack to identify the module from which the current function 
    was called, and then attempts to re-import that module. If recursion is detected (i.e., 
    if the caller's module is the same as the current frame's module), a `ValueError` is raised.

    :raises ValueError: 
        If recursion within the same module is detected, meaning that the caller and the current 
        frame originated from the same module.
    :return: 
        A tuple containing the current frame and caller frame information.
    :rtype: tuple (inspect.FrameInfo, inspect.FrameInfo)
    """
    stack = inspect.stack()
    current_frame = stack[1]
    caller_frame = stack[-1]
    return current_frame, caller_frame
    
def get_info_module(caller_frame: inspect.FrameInfo) -> ModuleType | None:
    """
    Retrieve module information from a given caller frame.

    This function takes the caller frame information and retrieves the corresponding module
    using the `inspect.getmodule` method. This can be used to identify the module where
    a function call originates.

    :param caller_frame: 
        The caller frame information obtained from the call stack.
    :type caller_frame: inspect.FrameInfo

    :return: 
        The module information for the caller frame, or None if the module cannot be determined.
    :rtype: ModuleType | None
    """
    info_module = inspect.getmodule(caller_frame.frame)
    return info_module

def load_module(info_module: ModuleType) -> ModuleType | None:
    """
    Load the module dynamically from its file location.

    Given a module's information, this method re-imports the module dynamically from the 
    file where it is located. This is useful when modifications are made to a module, and 
    it needs to be reloaded without restarting the interpreter.

    :param info_module: 
        The module information used to locate and load the module.
    :type info_module: ModuleType

    :return: 
        The reloaded module if the loading is successful, or None if it fails.
    :rtype: ModuleType | None
    """
    spec = importlib.util.spec_from_file_location(info_module.__name__, info_module.__file__)
    if spec and spec.loader:
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        sys.modules[module.__name__] = module
        return module
    return None