from pydantic import (
    BaseModel,
    field_validator,
    Field
)

from typing import (
    Optional, 
    List,
    Union
)
from types import ModuleType
from .utilities.module_util import (
    ModuleUtil, 
    ClassInfo,
    ArgumentInfo,
    FunctionInfo,
    AttributeInfo,
    VariableInfo
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

    version: Optional[str] = None
    interpreter: Optional[str] = None
    modules: List['Module']

    @field_validator('version')
    def validate_version(cls, value:str):
        if ".".join(value.split(".")[:2]) not in Constants.SUPPORTED_PYTHON_VERSION:
            raise(ValueError(Errors.INVALID_PYTHON_VERSION.format(Constants.SUPPORTED_PYTHON_VERSION, value)))
        return value
    
    @field_validator('interpreter')
    def validate_interpreter(cls, value:str):
        if value not in Constants.SUPPORTED_PYTHON_IMPLEMENTATION:
            raise(ValueError(Errors.INVALID_PYTHON_INTERPRETER.format(Constants.SUPPORTED_PYTHON_IMPLEMENTATION, value)))
        return value

class System(BaseModel):
    os: str
    envs: Optional[dict] = Field(default=None, repr=False)
    pythons: List[Python]

    @field_validator('os')
    def validate_os(cls, value: str):
        if value not in Constants.SUPPORTED_OS:
            raise ValueError(Errors.INVALID_OS.format(Constants.SUPPORTED_OS, value))
        return value

class Runtime(BaseModel):

    arch: str
    systems: List[System]

    @field_validator('arch')
    def validate_arch(cls, value: str):
        if value not in Constants.KNOWN_ARCHITECTURES:
            raise ValueError(Errors.INVALID_ARCHITECTURE.format(value, Constants.KNOWN_ARCHITECTURES))
        return value

class Variable(BaseModel):

    name: str
    annotation: Optional[str] = None
    value: Optional[Union[int, str, float, bool, None]] = None

    @field_validator("annotation")
    def validate_annotation(cls, value):

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

        return [Variable(
            name=var_info.name,
            value=var_info.value,
            annotation=var_info.annotation
        ) for var_info in variables_info]

class Attribute(Variable):

    type: str

    @field_validator('type')
    def validate_type(cls, value: str):
        if value not in Constants.SUPPORTED_CLASS_ATTRIBUTE_TYPES:
            raise ValueError(Errors.INVALID_ATTRIBUTE_TYPE.format(value, Constants.SUPPORTED_CLASS_ATTRIBUTE_TYPES))
        return value
    
    @classmethod
    def from_attributes_info(cls, attributes_info: List[AttributeInfo]):
        return [Attribute(
            type=attr_info.type,
            name=attr_info.name,
            value=attr_info.value,
            annotation=attr_info.annotation
        ) for attr_info in attributes_info]
    
class Argument(Variable, BaseModel):
    
    @classmethod
    def from_arguments_info(cls, arguments_info: List[ArgumentInfo]):
        """
        Converts extracted function parameters into `Argument` instances.

        :param arguments_info: A list of extracted argument metadata.
        :type arguments_info: List[ArgumentInfo]
        :return: A list of `Argument` objects.
        :rtype: List[Argument]
        """
        return [Argument(
            name=arg_info.name,
            annotation=arg_info.annotation,
            value=arg_info.value
        ) for arg_info in arguments_info]

class Function(BaseModel):

    name: str
    arguments: Optional[List[Argument]] = None
    return_annotation: Optional[str] = None

    @field_validator("return_annotation")
    def validate_annotation(cls, value):
        return CommonValidator.validate_annotation(value)
    
    @classmethod
    def from_functions_info(cls, functions_info: List[FunctionInfo]):

        return [Function(
            name=func_info.name,
            arguments=Argument.from_arguments_info(func_info.arguments),
            return_annotation=func_info.return_annotation
        ) for func_info in functions_info]
    
class Class(BaseModel):

    name: str
    attributes: Optional[List[Attribute]] = None
    methods: Optional[List[Function]] = None
    superclasses: Optional[List[str]] = None

    @classmethod
    def from_class_info(cls, extracted_classes: List[ClassInfo]):

        return [Class(
            name=name,
            attributes=Attribute.from_attributes_info(attributes),
            methods=Function.from_functions_info(methods),
            superclasses=superclasses
        ) for name, attributes, methods, superclasses in extracted_classes]

class Module(BaseModel):

    filename: Optional[str] = None
    version: Optional[str] = None
    variables: Optional[List[Variable]] = None
    functions: Optional[List[Function]] = None
    classes: Optional[List[Class]] = None

class SpyModel(Module):

    deployments: Optional[List[Runtime]] = None

    @classmethod
    def from_module(cls, info_module: ModuleType):

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

class CommonValidator:

    @classmethod
    def validate_annotation(cls, value):
        if not value:
            return None
        base = value.split("[")[0]
        if base not in Constants.SUPPORTED_ANNOTATIONS:
            raise ValueError(
                Errors.INVALID_ANNOTATION.format(value, Constants.SUPPORTED_ANNOTATIONS)
            )
        return value