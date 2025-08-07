"""
Module utilities for runtime introspection and structure extraction.

This module provides utility functions for analyzing Python modules dynamically,
primarily to support ImportSpy's runtime validation mechanisms. It enables inspection
of modules, their metadata, and internal structure at runtime.

Features:
- Inspect the call stack and determine caller modules.
- Dynamically load and unload Python modules.
- Extract version information via metadata or attributes.
- Retrieve global variables, top-level functions, and class definitions.
- Analyze methods, attributes (class-level and instance-level), and superclasses.

Example:
    ```python
    from importspy.utilities.module_util import ModuleUtil
    import inspect

    module_util = ModuleUtil()
    info = module_util.get_info_module(inspect.stack()[0])
    print(info.__name__)
    ```
"""

import inspect
import importlib.util
import sys
import importlib.metadata
import logging
from types import ModuleType, FunctionType
from typing import List, Optional, Any
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
    Provides methods to inspect and extract structural metadata from Python modules.

    This class enables runtime inspection of loaded modules for metadata such as
    functions, classes, variables, inheritance hierarchies, and version information.
    It is a core component used by ImportSpy to validate structural contracts.
    """

    def inspect_module(self) -> tuple:
        """
        Retrieve the current and caller frames from the stack.

        Returns:
            tuple: A tuple with the current and the outermost caller frame.
        """
        stack = inspect.stack()
        current_frame = stack[1]
        caller_frame = stack[-1]
        return current_frame, caller_frame

    def get_info_module(self, caller_frame: inspect.FrameInfo) -> ModuleType | None:
        """
        Resolve a module object from a given caller frame.

        Args:
            caller_frame (inspect.FrameInfo): The caller frame to analyze.

        Returns:
            ModuleType | None: The resolved module or None if not found.
        """
        return inspect.getmodule(caller_frame.frame)

    def load_module(self, info_module: ModuleType) -> ModuleType | None:
        """
        Reload a module dynamically from its file location.

        Args:
            info_module (ModuleType): The module to reload.

        Returns:
            ModuleType | None: The reloaded module or None if loading fails.
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
        Unload a module from sys.modules and globals.

        Args:
            module (ModuleType): The module to unload.
        """
        module_name = module.__name__
        if module_name in sys.modules:
            del sys.modules[module_name]
            globals().pop(module_name, None)

    def extract_version(self, info_module: ModuleType) -> str | None:
        """
        Attempt to retrieve the version string from a module.

        Args:
            info_module (ModuleType): The target module.

        Returns:
            str | None: Version string if found, otherwise None.
        """
        if hasattr(info_module, '__version__'):
            return info_module.__version__
        try:
            return importlib.metadata.version(info_module.__name__)
        except importlib.metadata.PackageNotFoundError:
            return None

    def extract_annotation(self, annotation:Any) -> Optional[str]:
        """
        Convert a type annotation object into a string representation.

        Args:
            annotation: The annotation object to convert.

        Returns:
            Optional[str]: The extracted annotation string or None.
        """
        if annotation == inspect._empty or not annotation:
            return None
        if isinstance(annotation, type):
            return annotation.__name__
        return str(annotation)

    def extract_variables(self, info_module: ModuleType) -> List[VariableInfo]:
        """
        Extract top-level variable definitions from a module.

        Args:
            info_module (ModuleType): The module to analyze.

        Returns:
            List[VariableInfo]: List of variable metadata.
        """
        variables_info: List[VariableInfo] = []
        for name, value in inspect.getmembers(info_module):
            if not name.startswith('__') and not inspect.ismodule(value) and not inspect.isfunction(value) and not inspect.isclass(value):
                annotation = self.extract_annotation(type(value))
                variables_info.append(VariableInfo(name=name, annotation=annotation, value=value))
        return variables_info

    def extract_functions(self, info_module: ModuleType) -> List[FunctionInfo]:
        """
        Extract all functions defined at the top level of the module.

        Args:
            info_module (ModuleType): The target module.

        Returns:
            List[FunctionInfo]: Function metadata extracted from the module.
        """
        functions_info: List[FunctionInfo] = []
        for name, obj in inspect.getmembers(info_module, inspect.isfunction):
            if obj.__module__ == info_module.__name__:
                functions_info.append(self._extract_function(name, obj))
        return functions_info

    def _extract_function(self, name: str, obj: FunctionType) -> FunctionInfo:
        """
        Build structured metadata for a function.

        Args:
            name (str): Function name.
            obj (FunctionType): Function object.

        Returns:
            FunctionInfo: Extracted function metadata.
        """
        return FunctionInfo(
            name,
            self._extract_arguments(obj),
            self.extract_annotation(inspect.signature(obj).return_annotation)
        )

    def _extract_arguments(self, obj: FunctionType) -> List[ArgumentInfo]:
        """
        Extract arguments from a function's signature.

        Args:
            obj (FunctionType): Function object.

        Returns:
            List[ArgumentInfo]: List of function argument metadata.
        """
        args = []
        for name, param in inspect.signature(obj).parameters.items():
            value = param.default if param.default is not inspect.Signature.empty else None
            args.append(ArgumentInfo(name=name, annotation=self.extract_annotation(param.annotation), value=value))
        return args

    def extract_methods(self, cls_obj:Any) -> List[FunctionInfo]:
        """
        Extract method definitions from a class object.

        Args:
            cls_obj: The class to inspect.

        Returns:
            List[FunctionInfo]: Extracted method metadata.
        """
        methods: List[FunctionInfo] = []
        for name, obj in inspect.getmembers(cls_obj, inspect.isfunction):
            if obj.__module__ == cls_obj.__module__:
                methods.append(self._extract_function(name, obj))
        return methods

    def extract_attributes(self, cls_obj:Any, info_module: ModuleType) -> List[AttributeInfo]:
        """
        Extract both class-level and instance-level attributes.

        Args:
            cls_obj: The class to analyze.
            info_module (ModuleType): The module containing the class.

        Returns:
            List[AttributeInfo]: List of extracted attributes.
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
        Extract all class definitions from a module.

        Args:
            info_module (ModuleType): The module to inspect.

        Returns:
            List[ClassInfo]: Metadata about the module’s classes.
        """
        classes = []
        for name, cls in inspect.getmembers(info_module, inspect.isclass):
            attributes = self.extract_attributes(cls, info_module)
            methods = self.extract_methods(cls)
            superclasses = self.extract_superclasses(cls)
            classes.append(ClassInfo(name, attributes, methods, superclasses))
        return classes

    def extract_superclasses(self, cls:Any) -> List[ClassInfo]:
        """
        Extract base classes for a given class, recursively.

        Args:
            cls: The class whose base classes are being extracted.

        Returns:
            List[ClassInfo]: Metadata for each superclass.
        """
        superclasses = []
        for base in cls.__bases__:
            if base.__name__ == "object":
                continue
            module = sys.modules.get(base.__module__)
            if not module:
                continue
            superclasses.append(ClassInfo(
                base.__name__,
                self.extract_attributes(base, module),
                self.extract_methods(base),
                []
            ))
        return superclasses
