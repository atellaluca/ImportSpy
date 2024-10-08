import inspect
import importlib.util
import sys
from types import ModuleType
from typing import List
from collections import namedtuple
import importlib.metadata
import logging

"""
Module utilities for dynamic module inspection and loading.

This module provides a set of functions to inspect and dynamically load Python modules,
extracting relevant information such as functions, classes, and their respective superclasses.
It facilitates the analysis of modules at runtime, allowing for the retrieval of metadata
and re-importation of modified modules without restarting the interpreter.

Functions:
    inspect_module() -> tuple:
        Inspects the stack to find the calling module and re-import it dynamically.
        
    get_info_module(caller_frame: inspect.FrameInfo) -> ModuleType | None:
        Retrieves module information from a given caller frame.
        
    load_module(info_module: ModuleType) -> ModuleType | None:
        Loads the module dynamically from its file location.
        
    extract_version(info_module: ModuleType) -> str | None:
        Extracts the version of the specified module, if available.
        
    extract_functions(info_module: ModuleType) -> List[str] | None:
        Extracts a list of function names defined in the specified module.
        
    extract_classes(info_module: ModuleType) -> List[ClassInfo]:
        Extracts class information (name, methods, superclasses) from the specified module.
        
    extract_superclasses(module: ModuleType) -> List[str]:
        Extracts a list of all unique superclasses defined in the specified module.
"""


logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

ClassInfo = namedtuple('ClassInfo', ['name', 'methods', 'superclasses'])

def inspect_module() -> tuple:
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
    logger.debug(f"Stack detected: {stack}")
    current_frame = stack[1]
    logger.debug(f"Current frame: {current_frame}")
    caller_frame = stack[-1]
    logger.debug(f"Caller frame: {caller_frame}")
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
    logger.debug("Run load_module")
    spec = importlib.util.spec_from_file_location(info_module.__name__, info_module.__file__)
    if spec and spec.loader:
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        sys.modules[module.__name__] = module
        return module
    return None

def unload_module(module: ModuleType):
    logger.debug("Run unload_module")
    module_name = module.__name__
    if module_name in sys.modules:
        try:
            del sys.modules[module_name]
            if module_name in globals():
                globals().pop(module_name, None)
        except Exception as e:
            logger.error(f"Error while unloading the module {module_name}: {e}")
    else:
        logger.warning(f"The module {module_name} is not loaded and cannot be unloaded.")

def extract_version(info_module: ModuleType) -> str | None:
    """
    Extract the version of the specified module, if available.

    This function checks if the module has a `__version__` attribute. If not, it attempts to
    retrieve the version using the `importlib.metadata.version` function. If the module is not found
    in the package metadata, it returns None.

    :param info_module: 
        The module from which to extract the version.
    :type info_module: ModuleType

    :return: 
        The version of the module as a string, or None if the version is not available.
    :rtype: str | None
    """
    if hasattr(info_module, '__version__'):
        return info_module.__version__
    try:
        return importlib.metadata.version(info_module.__name__)
    except importlib.metadata.PackageNotFoundError:
        return None


def extract_functions(info_module: ModuleType) -> List[str] | None:
    """
    Extract a list of function names defined in the specified module.

    This function inspects the provided module and gathers all functions that are defined 
    within it, returning their names as a list.

    :param info_module: 
        The module from which to extract function names.
    :type info_module: ModuleType

    :return: 
        A list of function names defined in the module, or None if there are no functions.
    :rtype: List[str] | None
    """
    functions = [
            func_name
            for func_name, obj in inspect.getmembers(info_module, inspect.isfunction)
            if obj.__module__ == info_module.__name__
        ]
    return functions

def extract_classes(info_module: ModuleType) -> List[ClassInfo]:
    """
    Extract class information (name, methods, superclasses) from the specified module.

    This function inspects the provided module and gathers information about all classes defined 
    within it. For each class, it retrieves its name, methods, and superclasses.

    :param info_module: 
        The module from which to extract class information.
    :type info_module: ModuleType

    :return: 
        A list of `ClassInfo` namedtuples containing class names, methods, and superclasses.
    :rtype: List[ClassInfo]
    """
    classes = []
    for class_name, cls_obj in inspect.getmembers(info_module, inspect.isclass):
            if cls_obj.__module__ == info_module.__name__:
                methods = [
                    method_name for method_name, _ in inspect.getmembers(cls_obj, inspect.isfunction)
                ]
                superclasses = [base.__name__ for base in cls_obj.__bases__]
                current_class = ClassInfo(class_name, methods, superclasses)
                classes.append(current_class)
    return classes

def extract_superclasses(module: ModuleType) -> List[str]:
    """
    Extract a list of all unique superclasses defined in the specified module.

    This function inspects the provided module to identify all classes and retrieves their
    superclasses. It returns a list of unique superclass names.

    :param module: 
        The module from which to extract superclass information.
    :type module: ModuleType

    :return: 
        A list of unique superclass names defined in the module.
    :rtype: List[str]
    """
    superclasses = set()
    logger.debug("Extract superclasses...")
    for class_name, cls_obj in inspect.getmembers(module, inspect.isclass):
        logger.debug(f"Current class name: {class_name}")
        if cls_obj.__module__ == module.__name__:
            for base in cls_obj.__bases__:
                superclasses.add(base.__name__)
                logger.debug(f"Add {superclasses} to set, {superclasses}")
    logger.debug(f"Superclasses: {superclasses}")
    return list(superclasses)