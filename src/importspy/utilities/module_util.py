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
.. code-block:: python

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
from typing import List, Optional
from collections import namedtuple

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

ClassInfo = namedtuple('ClassInfo', ["name", "attributes", "methods", "superclasses"])
FunctionInfo = namedtuple('FunctionInfo', ["name", "arguments", "return_annotation"])
ArgumentInfo = namedtuple('ArgumentInfo', ["name", "annotation", "value"])
AttributeInfo = namedtuple('AttributeInfo', ["type", "name", "annotation", "value"])
VariableInfo = namedtuple('VariableInfo', ["name", "annotation", "value"])


class ModuleUtil:
    """
    Utility class for dynamic module inspection and metadata extraction.

    The `ModuleUtil` class provides methods to inspect, load, unload, and analyze Python 
    modules at runtime. These utilities are essential for enabling ImportSpy's dynamic 
    validation of runtime conditions.

    Methods:
    --------
    - `inspect_module()`: Retrieve current and caller frames.
    - `get_info_module()`: Extract module from a caller frame.
    - `load_module()`: Dynamically reload a module.
    - `unload_module()`: Remove module from memory.
    - `extract_version()`: Retrieve version of a module.
    - `extract_variables()`: Extract global variables.
    - `extract_functions()`: Extract top-level functions.
    - `extract_classes()`: Extract class definitions.
    - `extract_superclasses()`: Collect all used base classes.
    """

    def inspect_module(self) -> tuple:
        """
        Retrieve the current and caller frames from the stack.

        Returns:
        --------
        tuple
            A tuple containing the current and caller frame.
        """
        stack = inspect.stack()
        current_frame = stack[1]
        caller_frame = stack[-1]
        return current_frame, caller_frame

    def get_info_module(self, caller_frame: inspect.FrameInfo) -> ModuleType | None:
        """
        Retrieves the module object from a caller frame.

        Parameters:
        -----------
        caller_frame : inspect.FrameInfo
            The frame to analyze.

        Returns:
        --------
        ModuleType | None
            The resolved module or None if not found.
        """
        return inspect.getmodule(caller_frame.frame)

    def load_module(self, info_module: ModuleType) -> ModuleType | None:
        """
        Dynamically reload a module.

        Parameters:
        -----------
        info_module : ModuleType
            The module reference.

        Returns:
        --------
        ModuleType | None
            The reloaded module.
        """
        spec = importlib.util.spec_from_file_location(info_module.__name__, info_module.__file__)
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            sys.modules[module.__name__] = module
            return module
        return None

    def unload_module(self, module: ModuleType):
        """
        Removes a module from memory.

        Parameters:
        -----------
        module : ModuleType
            The module to unload.
        """
        module_name = module.__name__
        if module_name in sys.modules:
            del sys.modules[module_name]
            globals().pop(module_name, None)

    def extract_version(self, info_module: ModuleType) -> str | None:
        """
        Retrieves version metadata for the module.

        Parameters:
        -----------
        info_module : ModuleType

        Returns:
        --------
        str | None
            The version string if found.
        """
        if hasattr(info_module, '__version__'):
            return info_module.__version__
        try:
            return importlib.metadata.version(info_module.__name__)
        except importlib.metadata.PackageNotFoundError:
            return None

    def extract_annotation(self, annotation) -> Optional[str]:
        """
        Converts annotations to string format for validation.
        """
        if annotation == inspect._empty or not annotation:
            return None
        if isinstance(annotation, type):
            return annotation.__name__
        return str(annotation)

    def extract_variables(self, info_module: ModuleType) -> dict:
        variables_info:List[VariableInfo] = []
        for name, value in inspect.getmembers(info_module):
            if not name.startswith('__') and not inspect.ismodule(value) and not inspect.isfunction(value) and not inspect.isclass(value):
                annotation = self.extract_annotation(type(value))
                variables_info.append(VariableInfo(name=name, annotation=annotation, value=value))
        return variables_info

    def extract_functions(self, info_module: ModuleType) -> List[FunctionInfo]:
        """
        Extracts function definitions from the module.

        Returns:
        --------
        List[FunctionInfo]
        """
        functions_info: List[FunctionInfo] = []
        for name, obj in inspect.getmembers(info_module, inspect.isfunction):
            if obj.__module__ == info_module.__name__:
                functions_info.append(self._extract_function(name, obj))
        return functions_info

    def _extract_function(self, name: str, obj: FunctionType) -> FunctionInfo:
        """
        Builds metadata for a function.
        """
        return FunctionInfo(
            name,
            self._extract_arguments(obj),
            self.extract_annotation(inspect.signature(obj).return_annotation)
        )

    def _extract_arguments(self, obj: FunctionType) -> List[ArgumentInfo]:
        """
        Retrieves argument names and annotations.
        """
        args = []
        for name, param in inspect.signature(obj).parameters.items():
            value = param.default if param.default is not inspect.Signature.empty else None
            args.append(ArgumentInfo(name=name, annotation=self.extract_annotation(param.annotation), value=value))
        return args

    def extract_methods(self, cls_obj) -> List[FunctionInfo]:
        """
        Extracts all method definitions from a class.
        """
        methods: List[FunctionInfo] = []
        for name, obj in inspect.getmembers(cls_obj, inspect.isfunction):
            if obj.__module__ == cls_obj.__module__:
                methods.append(self._extract_function(name, obj))
        return methods

    def extract_attributes(self, cls_obj, info_module: ModuleType) -> List[AttributeInfo]:
        """
        Extracts class-level and instance-level attributes.
        """
        attributes: List[AttributeInfo] = []
        annotations = getattr(cls_obj, '__annotations__', {})
        for attr_name, value in cls_obj.__dict__.items():
            if not callable(value) and not attr_name.startswith('__'):
                attributes.append(AttributeInfo(
                    name=attr_name,
                    value=value,
                    type="class",
                    annotation=self.extract_annotation(annotations.get(attr_name))
                ))
        if cls_obj.__module__ == info_module.__name__:
            init_method = cls_obj.__dict__.get('__init__')
            if init_method:
                for line in inspect.getsourcelines(init_method)[0]:
                    line = line.strip()
                    if line.startswith('self.') and '=' in line:
                        parts = line.split('=')
                        attr_name = parts[0].strip().split('.')[1]
                        attr_value = parts[1].strip().strip('"')
                        attributes.append(AttributeInfo(
                            name=attr_name,
                            value=attr_value,
                            type="instance",
                            annotation=self.extract_annotation(annotations.get(attr_name))
                        ))
        return attributes

    def extract_classes(self, info_module: ModuleType) -> List[ClassInfo]:
        """
        Extracts class definitions from the module.

        Returns:
        --------
        List[ClassInfo]
        """
        classes = []
        for name, cls in inspect.getmembers(info_module, inspect.isclass):
            attributes = self.extract_attributes(cls, info_module)
            methods = self.extract_methods(cls)
            superclasses = [base.__name__ for base in cls.__bases__ if base.__name__ != "object"]
            classes.append(ClassInfo(name, attributes, methods, superclasses))
        return classes

    def extract_superclasses(self, module: ModuleType) -> List[str]:
        """
        Extracts unique superclass names from all classes.

        Returns:
        --------
        List[str]
        """
        superclasses = set()
        for name, cls in inspect.getmembers(module, inspect.isclass):
            if cls.__module__ == module.__name__:
                for base in cls.__bases__:
                    superclasses.add(base.__name__)
        return list(superclasses)
