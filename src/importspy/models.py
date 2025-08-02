"""
models.py
==========

Defines the structural and contextual data models used across ImportSpy.
These models represent modules, variables, functions, classes, runtimes,
systems, and environments involved in contract-based validation.

This module powers both embedded validation and CLI checks, enabling ImportSpy
to introspect, serialize, and enforce compatibility rules at multiple levels:
from source code structure to runtime platform details.
"""

from pydantic import BaseModel
from typing import Optional, Union, List
from types import ModuleType

from .utilities.module_util import (
    ModuleUtil, ClassInfo, ArgumentInfo,
    FunctionInfo, AttributeInfo, VariableInfo
)
from .utilities.runtime_util import RuntimeUtil
from .utilities.system_util import SystemUtil
from .utilities.python_util import PythonUtil
from .constants import Constants, Contexts, Errors
from .config import Config
import logging

logger = logging.getLogger("/".join(__file__.split('/')[-2:]))
logger.addHandler(logging.NullHandler())


class Python(BaseModel):
    """
    Represents a Python runtime environment.

    Includes:
    - Python version
    - Interpreter type (e.g., CPython, PyPy)
    - List of loaded modules
    Used in validating runtime compatibility.
    """
    version: Optional[str] = None
    interpreter: Optional[Constants.SupportedPythonImplementations] = None
    modules: list['Module']

    def __str__(self):
        return f"{self.interpreter} v{self.version}"

    def __repr__(self):
        return str(self)


class Environment(BaseModel):
    """
    Represents runtime environment variables and secrets.
    Used for validating runtime configuration.
    """
    variables: Optional[list['Variable']] = None
    secrets: Optional[list[str]] = None

    def __str__(self):
        return f"variables: {self.variables} | secrets: {self.secrets}"

    def __repr__(self):
        return str(self)


class System(BaseModel):
    """
    Represents a full OS environment within a deployment system.

    Includes:
    - OS type
    - Environment variables
    - Python runtimes
    Used to validate cross-platform compatibility.
    """
    os: Constants.SupportedOS
    environment: Optional[Environment] = None
    pythons: list[Python]

    def __str__(self):
        return f"{self.os.value}"

    def __repr__(self):
        return str(self)


class Runtime(BaseModel):
    """
    Represents a runtime deployment context.

    Defined by CPU architecture and associated systems.
    """
    arch: Constants.SupportedArchitectures
    systems: list[System]

    def __str__(self):
        return f"{self.arch}"

    def __repr__(self):
        return str(self)


class Variable(BaseModel):
    """
    Represents a top-level variable in a Python module.

    Includes:
    - Name
    - Optional annotation
    - Optional static value
    Used to enforce structural consistency.
    """
    name: str
    annotation: Optional[Constants.SupportedAnnotations] = None
    value: Optional[Union[int, str, float, bool, None]] = None

    @classmethod
    def from_variable_info(cls, variables_info: list[VariableInfo]):
        return [cls(
            name=var_info.name,
            value=var_info.value,
            annotation=var_info.annotation
        ) for var_info in variables_info]

    def __str__(self):
        type_part = f": {self.annotation}" if self.annotation else ""
        return f"{self.name}{type_part} = {self.value}"

    def __repr__(self):
        return str(self)


class Attribute(Variable):
    """
    Represents a class-level attribute.

    Extends Variable with attribute type (e.g., class or instance).
    """
    type: Constants.SupportedClassAttributeTypes

    @classmethod
    def from_attributes_info(cls, attributes_info: list[AttributeInfo]):
        return [cls(
            type=attr_info.type,
            name=attr_info.name,
            value=attr_info.value,
            annotation=attr_info.annotation
        ) for attr_info in attributes_info]


class Argument(Variable, BaseModel):
    """
    Represents a function/method argument.

    Includes:
    - Name
    - Optional type annotation
    - Optional default value
    Used to check call signatures.
    """
    @classmethod
    def from_arguments_info(cls, arguments_info: list[ArgumentInfo]):
        return [cls(
            name=arg_info.name,
            annotation=arg_info.annotation,
            value=arg_info.value
        ) for arg_info in arguments_info]


class Function(BaseModel):
    """
    Represents a callable entity.

    Includes:
    - Name
    - List of arguments
    - Optional return annotation
    """
    name: str
    arguments: Optional[list[Argument]] = None
    return_annotation: Optional[Constants.SupportedAnnotations] = None

    @classmethod
    def from_functions_info(cls, functions_info: list[FunctionInfo]):
        return [cls(
            name=func_info.name,
            arguments=Argument.from_arguments_info(func_info.arguments),
            return_annotation=func_info.return_annotation
        ) for func_info in functions_info]

    def __str__(self):
        args = ", ".join(str(arg) for arg in self.arguments) if self.arguments else ""
        return f"{self.name}({args}) -> {self.return_annotation}"

    def __repr__(self):
        return str(self)


class Class(BaseModel):
    """
    Represents a Python class declaration.

    Includes:
    - Name
    - Attributes (class/instance)
    - Methods
    - Superclasses (recursive)
    """
    name: str
    attributes: Optional[list[Attribute]] = None
    methods: Optional[list[Function]] = None
    superclasses: Optional[list['Class']] = None

    @classmethod
    def from_class_info(cls, extracted_classes: list[ClassInfo]):
        return [cls(
            name=name,
            attributes=Attribute.from_attributes_info(attributes),
            methods=Function.from_functions_info(methods),
            superclasses=cls.from_class_info(superclasses)
        ) for name, attributes, methods, superclasses in extracted_classes]

    def get_class_attributes(self) -> List[Attribute]:
        if self.attributes:
            return [attr for attr in self.attributes if attr.type == Config.CLASS_TYPE]

    def get_instance_attributes(self) -> List[Attribute]:
        if self.attributes:
            return [attr for attr in self.attributes if attr.type == Config.INSTANCE_TYPE]


class Module(BaseModel):
    """
    Represents a Python module.

    Includes:
    - Filename
    - Version (if extractable)
    - Top-level variables, functions, and classes
    """
    filename: Optional[str] = None
    version: Optional[str] = None
    variables: Optional[list[Variable]] = None
    functions: Optional[list[Function]] = None
    classes: Optional[list[Class]] = None

    def __str__(self):
        return f"Module: {self.filename or 'unknown'} (v{self.version or '-'})"

    def __repr__(self):
        return str(self)


class SpyModel(Module):
    """
    High-level model used by ImportSpy for validation.

    Extends the module representation with runtime metadata and
    platform-specific deployment constraints (architecture, OS, interpreter, etc).
    """
    deployments: Optional[list[Runtime]] = None

    @classmethod
    def from_module(cls, info_module: ModuleType):
        """
        Build a SpyModel instance by extracting structure and metadata
        from an actual Python module object.
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
        envs = Variable.from_variable_info(system_utils.extract_envs())

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


class Error(BaseModel):
    """
    Describes a structured validation error.

    Includes the context, error type, message, and resolution steps.
    Used to serialize feedback during contract enforcement.
    """
    context: Contexts
    title: str
    category: Errors.Category
    description: str
    solution: str
