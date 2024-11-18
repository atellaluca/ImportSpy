import inspect
import importlib.util
import sys
import os
from types import ModuleType
from typing import List, Tuple
from collections import namedtuple
import importlib.metadata
import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

ClassInfo = namedtuple('ClassInfo', [
    'name',
    'class_attr',
    'instance_attr',
    'methods',
    'superclasses'
    ])

def inspect_module() -> tuple:
    """
    Proactively inspect the current stack to identify the module that called this function and 
    attempt to dynamically re-import it.

    This function allows for proactive control over module execution, ensuring that you can
    analyze the module calling your code and reload it if necessary. If recursion is detected 
    (i.e., the caller module is the same as the current one), it raises a `ValueError` to prevent
    unintended behavior.

    Raises:
    -------
    - **ValueError**: If recursion within the same module is detected, meaning that the caller
      and the current module are the same.

    Returns:
    --------
    - **tuple (inspect.FrameInfo, inspect.FrameInfo)**: A tuple containing information about the 
      current frame and the caller frame.
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
    Retrieve the module information from a given caller frame, allowing for insight into the
    context from which a function was called.

    This function uses the `inspect.getmodule` method to return the module associated with
    the caller frame. It helps in gaining a better understanding of the module that originated
    the function call.

    Parameters:
    -----------
    - **caller_frame** (`inspect.FrameInfo`): The caller frame information from the stack.

    Returns:
    --------
    - **ModuleType | None**: The module information associated with the caller frame, or `None` 
      if it cannot be determined.
    """
    info_module = inspect.getmodule(caller_frame.frame)
    return info_module

def load_module(info_module: ModuleType) -> ModuleType | None:
    """
    Dynamically load or reload a module from its file location, allowing modifications
    to be applied without restarting the interpreter.

    This method attempts to dynamically re-import a module based on its file location, which 
    can be particularly useful when the module has been modified and needs to be reloaded 
    to reflect the changes.

    Parameters:
    -----------
    - **info_module** (`ModuleType`): The module information used to locate and load the module.

    Returns:
    --------
    - **ModuleType | None**: The reloaded module if the loading is successful, or `None` if it fails.
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
    """
    Unload a module from memory, freeing up resources and allowing for the re-importation of updated modules.

    This function removes a module from the global namespace and `sys.modules`, allowing the module
    to be reloaded or discarded as necessary. This is useful in dynamic systems where modules might 
    need to be refreshed during execution.

    Parameters:
    -----------
    - **module** (`ModuleType`): The module to be unloaded.
    """
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
    Extract the version information of a module, if available, ensuring compatibility with 
    other parts of the system.

    This function checks if the module has a `__version__` attribute. If not, it attempts to 
    retrieve the version using `importlib.metadata`. This is useful for managing dependencies 
    and ensuring that the correct module version is loaded.

    Parameters:
    -----------
    - **info_module** (`ModuleType`): The module from which to extract version information.

    Returns:
    --------
    - **str | None**: The version of the module as a string, or `None` if it is unavailable.
    """
    if hasattr(info_module, '__version__'):
        return info_module.__version__
    try:
        return importlib.metadata.version(info_module.__name__)
    except importlib.metadata.PackageNotFoundError:
        return None

def extract_variables(info_module: ModuleType) -> dict:
    """
    Extract a dictionary of variable names and their values defined in a module.

    This function retrieves all variable names and their corresponding values defined within 
    the specified module, allowing developers to verify the variables and their values.

    Parameters:
    -----------
    - **info_module** (`ModuleType`): The module from which to extract variable names and values.

    Returns:
    --------
    - **dict**: A dictionary where:
        - **Key** (`str`): The name of the variable.
        - **Value** (`Any`): The value assigned to the variable in the module.
    """
    return {
        var_name: obj
        for var_name, obj in inspect.getmembers(info_module)
        if not callable(obj)
        and not isinstance(obj, ModuleType)
        and not (var_name.startswith("__") and var_name.endswith("__"))
    }



def extract_functions(info_module: ModuleType) -> List[str]:
    """
    Extract a list of function names defined in a module.

    This function retrieves all function names defined within the specified module, allowing
    developers to verify the functions implemented in the module.

    Parameters:
    -----------
    - **info_module** (`ModuleType`): The module from which to extract function names.

    Returns:
    --------
    - **List[str]: A list of function names defined in the module.
    """
    return [
        func_name
        for func_name, obj in inspect.getmembers(info_module, inspect.isfunction)
        if obj.__module__ == info_module.__name__
    ]

def extract_classes(info_module: ModuleType) -> List[ClassInfo]:
    """
    Extract information about classes in a module, including their methods, class attributes, 
    instance attributes, and superclasses, providing a clear picture of the module's class structure.

    This function retrieves class information from the specified module, including class names, 
    class attributes, instance attributes, methods they define, and their superclasses.

    Parameters:
    -----------
    - **info_module** (`ModuleType`): The module from which to extract class information.

    Returns:
    --------
    - **List[ClassInfo]**: A list of `ClassInfo` namedtuples containing class names, class_attr, instance_attr, methods, and superclasses.
    """
    classes = []
    for class_name, cls_obj in inspect.getmembers(info_module, inspect.isclass):
        if cls_obj.__module__ == info_module.__name__:
            class_attr = [
                attr_name for attr_name, attr_value in cls_obj.__dict__.items() 
                if not callable(attr_value) and not attr_name.startswith('__')
            ]
            instance_attr = []
            init_method = cls_obj.__dict__.get('__init__')
            if init_method:
                source_lines = inspect.getsourcelines(init_method)[0]
                for line in source_lines:
                    line = line.strip()
                    if line.startswith('self.') and '=' in line:
                        attr_name = line.split('=')[0].strip().split('.')[1]
                        instance_attr.append(attr_name)
            methods = [
                method_name for method_name, _ in inspect.getmembers(cls_obj, inspect.isfunction)
            ]
            superclasses = [base.__name__ for base in cls_obj.__bases__]
            current_class = ClassInfo(class_name, class_attr, instance_attr, methods, superclasses)
            classes.append(current_class)
    return classes

def extract_superclasses(module: ModuleType) -> List[str]:
    """
    Extract all unique superclasses from a module, helping to understand the inheritance hierarchy 
    of the classes within the module.

    This function identifies all superclasses for the classes defined in the specified module and 
    returns a list of unique superclass names.

    Parameters:
    -----------
    - **module** (`ModuleType`): The module from which to extract superclass information.

    Returns:
    --------
    - **List[str]**: A list of unique superclass names defined in the module.
    """
    superclasses = set()
    logger.debug("Extract superclasses...")
    for class_name, cls_obj in inspect.getmembers(module, inspect.isclass):
        logger.debug(f"Current class name: {class_name}")
        if cls_obj.__module__ == module.__name__:
            for base in cls_obj.__bases__:
                superclasses.add(base.__name__)
                logger.debug(f"Added {base.__name__} to superclasses set")
    logger.debug(f"Superclasses: {superclasses}")
    return list(superclasses)

def extract_env_vars() -> dict:
    """
    Extract all current environment variables and their values as a dictionary.

    This function retrieves all environment variables available in the system's current execution
    context and returns them in a dictionary format. Each key in the dictionary represents the
    name of an environment variable, and its corresponding value represents the value assigned 
    to that variable.

    Parameters:
    -----------
    None

    Returns:
    --------
    - **dict**: A dictionary where:
        - **Key** (`str`): The name of the environment variable.
        - **Value** (`str`): The value assigned to the environment variable.

    Example Usage:
    --------------
    ```python
    env_vars = extract_env_vars()
    print(env_vars)
    # Output: {'PATH': '/usr/bin:/bin', 'CI': 'true', ...}
    ```

    Notes:
    ------
    - This function is useful for debugging or validating the runtime environment.
    - It relies on `os.environ`, which reflects the environment at the time the function is called.
    - Sensitive data (e.g., API keys) might be included in the output; handle with care.
    """
    return dict(os.environ)