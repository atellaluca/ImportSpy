"""
Module: Module Utilities

This module provides a comprehensive set of utility functions for dynamic module inspection, 
loading, unloading, and metadata extraction. It is designed to support ImportSpy's runtime 
validation processes by enabling detailed analysis of Python modules.

Key Features:
-------------
- Inspect the calling stack and retrieve information about modules.
- Dynamically load and unload modules for runtime modifications.
- Extract metadata such as classes, functions, variables, and inheritance hierarchies from modules.

Example Usage:
--------------
```python
from importspy.utilities.module_util import ModuleUtil

module_util = ModuleUtil()
module_info = module_util.get_info_module(inspect.stack()[0])
print(f"Module Name: {module_info.__name__}")
"""

import inspect
import importlib.util
import sys
import importlib.metadata
import logging
from types import ModuleType, FunctionType
from typing import List, Tuple
from collections import namedtuple

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

ClassInfo = namedtuple('ClassInfo', [
    'name',
    'class_attr',
    'instance_attr',
    'methods',
    'superclasses'
    ])

FunctionInfo = namedtuple('FunctionInfo', [
    "name",
    "arguments",
    "return_annotation"
    ])

ArgumentInfo = namedtuple('ArgumentInfo', [
    "name",
    "annotation",
    "value"
    ])



class ModuleUtil:

    """
    Utility class for dynamic module inspection and metadata extraction.

    The `ModuleUtil` class provides methods to inspect, load, unload, and analyze Python 
    modules at runtime. These utilities are essential for enabling ImportSpy's dynamic 
    validation of runtime conditions.

    Methods:
    --------
    - `inspect_module`: Retrieve the current and caller frames from the stack.
    - `get_info_module`: Extract module information from a caller frame.
    - `load_module`: Dynamically load or reload a module from its file location.
    - `unload_module`: Unload a module from memory to allow re-importation.
    - `extract_version`: Retrieve version information from a module.
    - `extract_variables`: Extract global variables from a module.
    - `extract_functions`: Extract function definitions and metadata from a module.
    - `extract_classes`: Extract class definitions, attributes, methods, and inheritance information.
    - `extract_superclasses`: Identify all unique superclasses from a module.

    Example:
    --------
    ```python
    from importspy.utilities.module_util import ModuleUtil

    module_util = ModuleUtil()
    module = module_util.load_module(some_info_module)
    print(f"Loaded Module: {module.__name__}")
    ```
    """

    def inspect_module(self) -> tuple:
        """
        Retrieve the current and caller frames from the stack.

        This method inspects the execution stack and returns the current frame and the caller frame. 
        It is used to analyze the context in which a function is being executed.

        Returns:
        --------
        - **tuple (inspect.FrameInfo, inspect.FrameInfo)**: A tuple containing the current frame and 
          the caller frame.

        Example Usage:
        --------------
        ```python
        module_util = ModuleUtil()
        current_frame, caller_frame = module_util.inspect_module()
        print(f"Current Frame: {current_frame}")
        print(f"Caller Frame: {caller_frame}")
        ```
        """
        stack = inspect.stack()
        logger.debug(f"Stack detected: {stack}")
        current_frame = stack[1]
        logger.debug(f"Current frame: {current_frame}")
        caller_frame = stack[-1]
        logger.debug(f"Caller frame: {caller_frame}")
        return current_frame, caller_frame

    def get_info_module(self, caller_frame: inspect.FrameInfo) -> ModuleType | None:
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

    def load_module(self, info_module: ModuleType) -> ModuleType | None:
        """
        Dynamically load or reload a module from its file location.

        This method facilitates dynamic reloading of a module, ensuring that any changes made to 
        the module are immediately reflected without restarting the runtime.

        Parameters:
        -----------
        - **info_module** (`ModuleType`): The module to be loaded or reloaded.

        Returns:
        --------
        - **ModuleType | None**: The loaded module, or `None` if loading fails.

        Example Usage:
        --------------
        ```python
        module_util = ModuleUtil()
        module = module_util.load_module(some_info_module)
        print(f"Module Name: {module.__name__}")
        ```
        """
        logger.debug("Run load_module")
        spec = importlib.util.spec_from_file_location(info_module.__name__, info_module.__file__)
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            sys.modules[module.__name__] = module
            return module
        return None

    def unload_module(self, module: ModuleType):
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

    def extract_version(self, info_module: ModuleType) -> str | None:
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

    def extract_variables(self, info_module: ModuleType) -> dict:
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
    
    def extract_functions(self, 
                          info_module:ModuleType) -> List[FunctionInfo]:
        return [
            self._extract_function(func_name, obj)
            for func_name, obj in inspect.getmembers(info_module, inspect.isfunction)
            if obj.__module__ == info_module.__name__
        ]
    
    def _extract_function(self, func_name:str, obj: Tuple[str, FunctionType]):
        return FunctionInfo(
            func_name,
            self._extract_arguments(obj),
            None if inspect.signature(obj).return_annotation is inspect.Signature.empty
            else inspect.signature(obj).return_annotation
        )
    
    def _extract_arguments(self, obj):
        return [
            ArgumentInfo(
                name=arg_name,
                annotation=param.annotation if param.annotation is not inspect.Signature.empty else None,
                value=param.default if param.default is not inspect.Signature.empty else None
            )
            for arg_name, param in inspect.signature(obj).parameters.items()
            ]

    def extract_methods(self,
                        cls_obj):
        info_functions = inspect.getmembers(cls_obj, inspect.isfunction)
        return [
            self._extract_function(func_name, obj)
            for func_name, obj in info_functions
            if obj.__module__ == cls_obj.__module__
        ]

    def extract_classes(self, info_module: ModuleType) -> List[ClassInfo]:
        """
        Extract class metadata from a module.

        This method retrieves all class definitions within the specified module, including their 
        attributes, methods, and inheritance information.

        Parameters:
        -----------
        - **info_module** (`ModuleType`): The module from which to extract class information.

        Returns:
        --------
        - **List[ClassInfo]**: A list of `ClassInfo` named tuples representing the classes defined 
          in the module.

        Example Usage:
        --------------
        ```python
        module_util = ModuleUtil()
        classes = module_util.extract_classes(some_info_module)
        for class_info in classes:
            print(f"Class Name: {class_info.name}")
        ```
        """
        classes = []
        for class_name, cls_obj in inspect.getmembers(info_module, inspect.isclass):
            if cls_obj.__module__ == info_module.__name__:
                class_attr = [
                    (attr_name, attr_value) for attr_name, attr_value in cls_obj.__dict__.items() 
                    if not callable(attr_value) and not attr_name.startswith('__')
                ]
                instance_attr = []
                init_method = cls_obj.__dict__.get('__init__')
                if init_method:
                    source_lines = inspect.getsourcelines(init_method)[0]
                    for line in source_lines:
                        line = line.strip()
                        if line.startswith('self.') and '=' in line:
                            parts = line.split('=')
                            attr_name = parts[0].strip().split('.')[1]
                            attr_value = parts[1].strip().strip('"')
                            instance_attr.append((attr_name, attr_value))
                methods = [
                    method_info for method_info in self.extract_methods(cls_obj)
                ]
                superclasses = [base.__name__ for base in cls_obj.__bases__ if base.__name__ != "object"]
                current_class = ClassInfo(class_name, class_attr, instance_attr, methods, superclasses)
                classes.append(current_class)
        return classes

    def extract_superclasses(self, module: ModuleType) -> List[str]:
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