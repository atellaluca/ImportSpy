from pydantic import BaseModel
from typing import Optional, List
from types import ModuleType
from .utils import spy_module_utils
import logging

logger = logging.getLogger("/".join(__file__.split('/')[-2:]))
logger.addHandler(logging.NullHandler())

class ClassModel(BaseModel):
    """
    Model representing a class within a module.

    This class serves as a data structure to encapsulate the information about a specific class,
    including its name, methods, and superclasses.

    Attributes:
        name (Optional[str]): The name of the class. It can be `None` if the name is not available. Defaults to `None`.
        methods (Optional[List[str]]): A list of method names defined in the class. Defaults to an empty list.
        superclasses (Optional[List[str]]): A list of names of the superclasses from which this class inherits. Defaults to an empty list.

    Example:
        >>> class_model = ClassModel(
        ...     name="MyClass", 
        ...     methods=["method1", "method2"], 
        ...     superclasses=["BaseClass"]
        ... )
    """
    name: Optional[str] = None
    methods: Optional[List[str]] = []
    superclasses: Optional[List[str]] = []



class SpyModel(BaseModel):
    """
    Model representing metadata of a module, including information about its functions and classes.

    This model encapsulates details about a Python module, including its name, version, and the 
    functions and classes defined within it. It allows for structured representation of module metadata.

    Attributes:
        filename (Optional[str]): The name of the module file. It can be `None` if the name is not available. Defaults to `None`.
        version (Optional[str]): The version of the module. It can be `None` if the version is not available. Defaults to `None`.
        functions (Optional[List[str]]): A list of function names defined in the module. Defaults to an empty list.
        classes (Optional[List[ClassModel]]): A list of classes defined in the module, represented by `ClassModel`. Defaults to an empty list.
        superclasses (Optional[List[str]]): A list of superclasses from which module-level classes inherit. Defaults to an empty list.

    Example:
        >>> spy_model = SpyModel(
        ...     filename="MyModule.py",
        ...     version="1.0.0",
        ...     functions=["my_function"],
        ...     classes=[
        ...         ClassModel(name="MyClass", methods=["my_method"], superclasses=["BaseClass"])
        ...     ]
        ... )

    Validator:
        from_module:
            Class method that extracts information from a `ModuleType` object and populates the fields of the `SpyModel`.
            This includes extracting the module filename, version, functions, and classes.
    
    Args:
        info_module (ModuleType): The module from which to extract metadata.
    """
    filename: Optional[str] = None
    version: Optional[str] = None
    functions: Optional[List[str]] = []
    classes: Optional[List[ClassModel]] = []

    @classmethod
    def from_module(cls, info_module: ModuleType):
        info_module = spy_module_utils.load_module(info_module)
        logger.debug(f"Create SpyModel from info_module: {ModuleType}")
        filename = "/".join(info_module.__file__.split('/')[-1:])
        version = spy_module_utils.extract_version(info_module)
        functions = spy_module_utils.extract_functions(info_module)
        classes = [
            ClassModel(name=name, methods=methods, superclasses=superclasses)
            for name, methods, superclasses in spy_module_utils.extract_classes(info_module)
        ]
        spy_module_utils.unload_module(info_module)
        logger.debug("Unload module")
        logger.debug(f"filename: {filename}, version: {version}, function: {functions}, classes: {classes}")
        return cls(
            filename=filename,
            version=version,
            functions=functions,
            classes=classes
        )

