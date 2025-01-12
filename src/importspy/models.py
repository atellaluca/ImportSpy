from pydantic import (
    BaseModel,
    field_validator,
    Field
)
from .mixins.annotations_validator_mixin import AnnotationValidatorMixin
from typing import (
    Optional, 
    List,
    Union
)
from types import ModuleType
from .utilities.module_util import (
    ModuleUtil, 
    ClassInfo
)
from .utilities.runtime_util import RuntimeUtil
from .utilities.system_util import SystemUtil
from .utilities.python_util import PythonUtil
from .constants import Constants
from .errors import Errors
import logging

"""
This module defines the core models for ImportSpy, facilitating the inspection and validation 
of runtime conditions and module structures in Python.

It provides a hierarchy of classes to represent:
- Python runtime environments.
- System configurations.
- Module metadata, including functions, classes, attributes, and their relationships.

The `SpyModel` class extends these capabilities by enabling dynamic validation of modules 
against predefined models.

Key Features:
-------------
- Models runtime metadata (`Python`, `System`, `Runtime`).
- Describes module elements like attributes, arguments, functions, and classes.
- Supports validation and adaptation for dynamic module inspection.

Examples:
---------
```python
from importspy.models import SpyModel

spy_model = SpyModel(
    filename="example.py",
    classes=[
        Class(
            name="ServiceHandler",
            methods=[
                Function(name="start_service", arguments=[Argument(name="config", annotation="dict")])
            ]
        )
    ]
)
```
"""

logger = logging.getLogger("/".join(__file__.split('/')[-2:]))
logger.addHandler(logging.NullHandler())

class Python(BaseModel):
    """
    Represents the Python runtime environment, including the version, interpreter, 
    and loaded modules.

    Attributes:
    -----------
    version : Optional[str]
        The version of the Python runtime.
    interpreter : Optional[str]
        The name of the Python interpreter (e.g., CPython, PyPy).
    modules : Optional[List['Module']]
        A list of loaded modules in the runtime.
    """
    version: Optional[str]
    interpreter: Optional[str]
    modules: Optional[List['Module']] = None

class System(BaseModel):
    """
    Encapsulates details of the operating system and its associated Python runtimes.

    Attributes:
    -----------
    os : Optional[str]
        The name of the operating system (e.g., Linux, Windows).
    envs : Optional[dict]
        Environment variables for the system (hidden in repr).
    pythons : Optional[List[Python]]
        A list of Python runtimes available on the system.
    """
    os: Optional[str] = None
    envs: Optional[dict] = Field(default=None, repr=False)
    pythons: Optional[List[Python]] = None

class Runtime(BaseModel):
    """
    Defines the runtime environment, including architecture and systems.

    Attributes:
    -----------
    arch : Optional[str]
        The architecture of the runtime (e.g., x86_64, ARM64).
    systems : Optional[List[System]]
        A list of systems included in the runtime.

    Methods:
    --------
    validate_arch(value: str) -> str
        Validates that the given architecture is supported.
    """

    arch: Optional[str] = None
    systems: Optional[List[System]] = None

    @field_validator('arch')
    def validate_arch(cls, value:str):
        if value not in Constants.KNOWN_ARCHITECTURES:
            raise ValueError(Errors.INVALID_ARCHITECTURE.format(value, Constants.KNOWN_ARCHITECTURES))
        return value

class Attribute(AnnotationValidatorMixin, BaseModel):
    """
    Represents a class or instance attribute with optional type annotations and values.

    Attributes:
    -----------
    type : str
        The type of attribute (e.g., "class", "instance").
    name : str
        The name of the attribute.
    annotation : Optional[str]
        The annotation of the attribute (e.g., "int", "str").
    value : Optional[Union[int, str, float, bool, None]]
        The value assigned to the attribute.

    Methods:
    --------
    validate_arch(value: str) -> str
        Validates the type of the attribute against supported attribute types.

    validate_annotation(value: str) -> str
        Validates the annotation of the attribute.
    """
    type: str
    name: str
    annotation: Optional[str] = None
    value: Optional[Union[int, str, float, bool, None]] = None

    @field_validator('type')
    def validate_arch(cls, value:str):
        if value not in Constants.SUPPORTED_CLASS_ATTRIBUTE_TYPES:
            raise ValueError(Errors.INVALID_ATTRIBUTE_TYPE.format(value, Constants.SUPPORTED_CLASS_ATTRIBUTE_TYPES))
        return value
    
    @field_validator("annotation")
    def validate_annotation(cls, value):
        return cls.validate_annotation(value)

class Argument(AnnotationValidatorMixin, BaseModel):
    """
    Encodes the properties of a function or method argument.

    Attributes:
    -----------
    name : str
        The name of the argument.
    annotation : Optional[str]
        The annotation of the argument (e.g., "int", "str").
    value : Optional[Union[str, int, float, bool, list, dict]]
        The default value of the argument, if any.

    Methods:
    --------
    validate_annotation(value: str) -> str
        Validates the annotation of the argument.
    """
    name:str
    annotation: Optional[str] = None
    value: Optional[Union[str, int, float, bool, list, dict]] = None

    @field_validator("annotation")
    def validate_annotation(cls, value):
        return super().validate_annotation(value)

class Function(AnnotationValidatorMixin, BaseModel):
    """
    Represents a function or method with its arguments and return type.

    Attributes:
    -----------
    name : str
        The name of the function or method.
    arguments : Optional[List[Argument]]
        A list of arguments for the function or method.
    return_annotation : Optional[str]
        The annotation of the function's return type.

    Methods:
    --------
    validate_annotation(value: str) -> str
        Validates the annotation of the return type.
    """
    name: str
    arguments: Optional[List[Argument]] = None
    return_annotation: Optional[str] = None

    @field_validator("return_annotation")
    def validate_annotation(cls, value):
        return super().validate_annotation(value)
    
class Class(BaseModel):
    """
    Represents a Python class with its attributes, methods, and superclasses.

    Attributes:
    -----------
    name : str
        The name of the class.
    attributes : Optional[List[Attribute]]
        A list of attributes defined in the class.
    methods : Optional[List[Function]]
        A list of methods defined in the class.
    superclasses : Optional[List[str]]
        A list of names of the class's superclasses.
    """
    name: str
    attributes: Optional[List[Attribute]] = None
    methods: Optional[List[Function]] = None
    superclasses: Optional[List[str]] = None

class Module(BaseModel):
    """
    Encapsulates metadata about a Python module, including its filename, version, 
    variables, functions, and classes.

    Attributes:
    -----------
    filename : Optional[str]
        The filename of the module.
    version : Optional[str]
        The version of the module.
    variables : Optional[dict]
        A dictionary of global variables in the module.
    functions : Optional[List[Function]]
        A list of functions defined in the module.
    classes : Optional[List[Class]]
        A list of classes defined in the module.
    """
    filename: Optional[str] = None
    version: Optional[str] = None
    variables: Optional[dict] = None
    functions: Optional[List[Function]] = None
    classes: Optional[List[Class]] = None

class Deployment(BaseModel):
    """
    Represents a deployment environment containing multiple runtimes.

    Attributes:
    -----------
    runtimes : Optional[List[Runtime]]
        A list of runtimes in the deployment environment.
    environment : Optional[str]
        The name or identifier of the deployment environment.
    """
    runtimes: Optional[List[Runtime]] = None
    environment: Optional[str] = None
    
class SpyModel(Module):
    """
    Extends the `Module` model to define the structure and conditions expected of 
    a validated Python module.

    Attributes:
    -----------
    deployments : Optional[List[Deployment]]
        A list of deployment environments associated with the module.

    Methods:
    --------
    from_module(info_module: ModuleType) -> SpyModel
        Dynamically constructs a `SpyModel` from a loaded Python module.

    _classes_adaper(extracted_classes: List[ClassInfo]) -> List[Class]
        Adapts extracted class metadata into `Class` instances.
    """
    deployments: Optional[List[Deployment]] = None

    @classmethod
    def from_module(cls, info_module: ModuleType):
        module_utils = ModuleUtil()
        runtime_utils = RuntimeUtil()
        sytem_utils = SystemUtil()
        python_utils = PythonUtil()
        info_module = module_utils.load_module(info_module)
        logger.debug(f"Create SpyModel from info_module: {ModuleType}")
        filename = "/".join(info_module.__file__.split('/')[-1:])
        version = module_utils.extract_version(info_module)
        variables = module_utils.extract_variables(info_module)
        functions = module_utils.extract_functions(info_module)
        classes = cls._classes_adaper(module_utils.extract_classes(info_module))
        arch = runtime_utils.extract_arch()
        os = sytem_utils.extract_os()
        python_version = python_utils.extract_python_version()
        interpreter = python_utils.extract_python_implementation()
        envs = sytem_utils.extract_envs()
        module_utils.unload_module(info_module)
        logger.debug("Unload module")
        logger.debug(f"filename: {filename}, version: {version}, \
                     functions: {functions}, classes: {classes}")
        return cls(
            deployments = [
                Deployment(
                    environment=Constants.DIE_ENVIRONMENT,
                    runtimes=[
                        Runtime(
                            arch=arch,
                            systems=[
                                System(
                                    os=os,
                                    envs=envs,
                                    pythons=[
                                        Python(
                                            version=python_version,
                                            interpreter=interpreter,
                                            modules=[
                                                Module(
                                                    filename=filename,
                                                    version=version,
                                                    variables=variables,
                                                    functions=functions,
                                                    classes=classes
                                                )
                                            ]
                                            
                                        )
                                    ]
                                    
                                ),
                            ]
                        )
                    ]
                )
            ]
        )
    
    @classmethod
    def _classes_adaper(cls, extracted_classes:List[ClassInfo]):
        classes = []
        for name, class_attr, instance_attr, methods, superclasses in extracted_classes:
            classes.append(Class(name=name,
                  attributes=[
                        Attribute(
                            type=Constants.INSTANCE_TYPE,
                            name=name,
                            value=value
                        )
                        for name, value in instance_attr
                        ]
                      + [
                        Attribute(
                            type=Constants.CLASS_TYPE,
                            name=name,
                            value=value
                        )
                        for name, value in class_attr  
                    ],
                  methods=[
                      Function(
                          name=method.name,
                          arguments=[
                              Argument(
                                  name=arg.name,
                                  annotation=arg.annotation,
                                  value=arg.value
                              )
                              for arg in method.arguments
                          ],
                          return_annotation=None
                      ) 
                      for method in methods
                  ],
                  superclasses=superclasses
                )
            )
        return classes
