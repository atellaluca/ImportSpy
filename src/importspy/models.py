"""
importspy.models
----------------

This module defines the core data models used by ImportSpy for contract-based
runtime validation of Python modules. It includes structural representations
of variables, functions, classes, and full modules, as well as runtime and
system-level metadata required to enforce import contracts across execution contexts.
"""

from pydantic import BaseModel, field_validator, Field
from typing import Optional, List, Union
from types import ModuleType

from .utilities.module_util import (
    ModuleUtil, ClassInfo, ArgumentInfo,
    FunctionInfo, AttributeInfo, VariableInfo
)
from .utilities.runtime_util import RuntimeUtil
from .utilities.system_util import SystemUtil
from .utilities.python_util import PythonUtil
from .constants import Constants
from .errors import Errors
import logging

logger = logging.getLogger("/".join(__file__.split('/')[-2:]))
logger.addHandler(logging.NullHandler())


class Python(BaseModel):
    """
    Represents a specific Python runtime configuration.

    Includes the Python version, interpreter type, and the list of loaded modules.
    Used to validate compatibility between caller and callee environments.
    """
    version: Optional[str] = None
    interpreter: Optional[str] = None
    modules: List['Module']

    @field_validator('version')
    def validate_version(cls, value: str):
        """
        Validate that the Python version is within supported versions.
        """
        if ".".join(value.split(".")[:2]) not in Constants.SUPPORTED_PYTHON_VERSION:
            raise ValueError(Errors.INVALID_PYTHON_VERSION.format(Constants.SUPPORTED_PYTHON_VERSION, value))
        return value

    @field_validator('interpreter')
    def validate_interpreter(cls, value: str):
        """
        Validate that the interpreter is among the supported Python implementations.
        """
        if value not in Constants.SUPPORTED_PYTHON_IMPLEMENTATION:
            raise ValueError(Errors.INVALID_PYTHON_INTERPRETER.format(Constants.SUPPORTED_PYTHON_IMPLEMENTATION, value))
        return value

class Environment(BaseModel):
    """
    Represents a set of environment variables and secret keys
    defined for the system or application runtime.
    """
    variables: Optional[List['Variable']] = None
    secrets: Optional[List[str]] = None

class System(BaseModel):
    """
    Represents the system environment, including OS, environment variables,
    and Python runtimes configured within the system.
    """
    os: str
    environment: Optional[Environment] = None
    pythons: List[Python]

    @field_validator('os')
    def validate_os(cls, value: str):
        """
        Validate that the provided OS is among the supported platforms.
        """
        if value not in Constants.SUPPORTED_OS:
            raise ValueError(Errors.INVALID_OS.format(Constants.SUPPORTED_OS, value))
        return value


class Runtime(BaseModel):
    """
    Represents the deployment runtime, identified by CPU architecture and
    the list of supported systems associated with that architecture.
    """
    arch: str
    systems: List[System]

    @field_validator('arch')
    def validate_arch(cls, value: str):
        """
        Validate that the CPU architecture is known and supported.
        """
        if value not in Constants.KNOWN_ARCHITECTURES:
            raise ValueError(Errors.INVALID_ARCHITECTURE.format(value, Constants.KNOWN_ARCHITECTURES))
        return value


class Variable(BaseModel):
    """
    Represents a declared variable within a Python module, including optional type
    annotation and value. Used for structural validation of the importing module.
    """
    name: str
    annotation: Optional[str] = None
    value: Optional[Union[int, str, float, bool, None]] = None

    @field_validator("annotation")
    def validate_annotation(cls, value):
        """
        Validate that the annotation is supported by the current contract.
        """
        if not value:
            return None
        base = value.split("[")[0]
        if base not in Constants.SUPPORTED_ANNOTATIONS:
            raise ValueError(
                Errors.INVALID_ANNOTATION.format(value, Constants.SUPPORTED_ANNOTATIONS)
            )
        return value

    @classmethod
    def from_variable_info(cls, variables_info: List[VariableInfo]):
        """
        Convert a list of extracted VariableInfo into Variable instances.
        """
        return [Variable(
            name=var_info.name,
            value=var_info.value,
            annotation=var_info.annotation
        ) for var_info in variables_info]


class Attribute(Variable):
    """
    Represents a class attribute, extending Variable with a 'type' indicator
    (e.g., 'class', 'instance'). Used in class-level contract validation.
    """
    type: str

    @field_validator('type')
    def validate_type(cls, value: str):
        """
        Validate that the attribute type is among supported class attribute types.
        """
        if value not in Constants.SUPPORTED_CLASS_ATTRIBUTE_TYPES:
            raise ValueError(Errors.INVALID_ATTRIBUTE_TYPE.format(value, Constants.SUPPORTED_CLASS_ATTRIBUTE_TYPES))
        return value

    @classmethod
    def from_attributes_info(cls, attributes_info: List[AttributeInfo]):
        """
        Convert a list of AttributeInfo objects into Attribute instances.
        """
        return [Attribute(
            type=attr_info.type,
            name=attr_info.name,
            value=attr_info.value,
            annotation=attr_info.annotation
        ) for attr_info in attributes_info]


class Argument(Variable, BaseModel):
    """
    Represents a function argument, including its name, type annotation, and default value.
    Used to validate callable structures and type consistency.
    """
    @classmethod
    def from_arguments_info(cls, arguments_info: List[ArgumentInfo]):
        """
        Convert a list of ArgumentInfo into Argument instances.
        """
        return [Argument(
            name=arg_info.name,
            annotation=arg_info.annotation,
            value=arg_info.value
        ) for arg_info in arguments_info]


class Function(BaseModel):
    """
    Represents a callable function, including its name, argument signature,
    and return type annotation.
    """
    name: str
    arguments: Optional[List[Argument]] = None
    return_annotation: Optional[str] = None

    @field_validator("return_annotation")
    def validate_annotation(cls, value):
        """
        Validate that the return annotation is supported.
        """
        return CommonValidator.validate_annotation(value)

    @classmethod
    def from_functions_info(cls, functions_info: List[FunctionInfo]):
        """
        Convert a list of FunctionInfo into Function instances.
        """
        return [Function(
            name=func_info.name,
            arguments=Argument.from_arguments_info(func_info.arguments),
            return_annotation=func_info.return_annotation
        ) for func_info in functions_info]


class Class(BaseModel):
    """
    Represents a Python class, including its attributes, methods, and declared superclasses.
    Used to enforce object-level validation rules in contracts.
    """
    name: str
    attributes: Optional[List[Attribute]] = None
    methods: Optional[List[Function]] = None
    superclasses: Optional[List[str]] = None

    @classmethod
    def from_class_info(cls, extracted_classes: List[ClassInfo]):
        """
        Convert a list of extracted class definitions into Class instances.
        """
        return [Class(
            name=name,
            attributes=Attribute.from_attributes_info(attributes),
            methods=Function.from_functions_info(methods),
            superclasses=superclasses
        ) for name, attributes, methods, superclasses in extracted_classes]


class Module(BaseModel):
    """
    Represents a full Python module, including its filename, version,
    and all its internal components (variables, functions, classes).
    """
    filename: Optional[str] = None
    version: Optional[str] = None
    variables: Optional[List[Variable]] = None
    functions: Optional[List[Function]] = None
    classes: Optional[List[Class]] = None


class SpyModel(Module):
    """
    Extends the base Module structure with additional deployment metadata.

    SpyModel is the top-level object representing a module's structure and its
    runtime/environment constraints. This is the core of ImportSpy's contract model.
    """
    deployments: Optional[List[Runtime]] = None

    @classmethod
    def from_module(cls, info_module: ModuleType):
        """
        Create a SpyModel from a loaded Python module, extracting its metadata
        and attaching runtime/system context.
        """
        module_utils = ModuleUtil()
        runtime_utils = RuntimeUtil()
        system_utils = SystemUtil()
        python_utils = PythonUtil()

        info_module = module_utils.load_module(info_module)
        logger.debug(f"Create SpyModel from info_module: {ModuleType}")

        filename = "/".join(info_module.__file__.split('/')[-1:])
        version = module_utils.extract_version(info_module)
        variables = Variable.from_variable_info(module_utils.extract_variables(info_module))
        functions = Function.from_functions_info(module_utils.extract_functions(info_module))
        classes = Class.from_class_info(module_utils.extract_classes(info_module))

        arch = runtime_utils.extract_arch()
        os = system_utils.extract_os()
        python_version = python_utils.extract_python_version()
        interpreter = python_utils.extract_python_implementation()
        envs = system_utils.extract_envs()

        module_utils.unload_module(info_module)
        logger.debug("Unload module")

        return cls(
            filename=filename,
            deployments=[
                Runtime(
                    arch=arch,
                    systems=[
                        System(
                            os=os,
                            environment=Environment(
                                variables=envs
                            ),
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
                        )
                    ]
                )
            ]
        )


class CommonValidator:
    """
    Provides shared validation utilities for type annotations and other structural elements.
    """

    @classmethod
    def validate_annotation(cls, value):
        """
        Validate a type annotation against the supported base annotations.
        """
        if not value:
            return None
        base = value.split("[")[0]
        if base not in Constants.SUPPORTED_ANNOTATIONS:
            raise ValueError(
                Errors.INVALID_ANNOTATION.format(value, Constants.SUPPORTED_ANNOTATIONS)
            )
        return value
