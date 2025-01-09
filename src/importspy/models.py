from pydantic import BaseModel, field_validator
from typing import (
    Optional, 
    List,
    Union
)
from types import ModuleType
from .utils.die_utils import (
    ModuleUtils,
    RuntimeUtils,
    SystemUtils,
    PythonUtils
)
from .constants import Constants
from .errors import Errors
import logging

logger = logging.getLogger("/".join(__file__.split('/')[-2:]))
logger.addHandler(logging.NullHandler())

class Python(BaseModel):
    version: Optional[str]
    interpreter: Optional[str]
    modules: Optional[List['Module']]

class System(BaseModel):
    os: Optional[str]
    envs: Optional[dict]
    pythons: Optional[List[Python]]

class Runtime(BaseModel):
    arch: Optional[str]
    systems: List[System]

    @field_validator('arch')
    def validate_arch(cls, value:str):
        if value not in Constants.KNOWN_ARCHITECTURES:
            raise ValueError(Errors.INVALID_ARCHITECTURE.format(value, Constants.KNOWN_ARCHITECTURES))
        return value

class Attribute(BaseModel):
    type: str
    name: str
    value: Optional[Union[int, str, float, bool, None]]

    @field_validator('type')
    def validate_arch(cls, value:str):
        if value not in Constants.ATTRIBUTE_TYPES:
            raise ValueError(Errors.INVALID_ATTRIBUTE_TYPE.format(value, Constants.ATTRIBUTE_TYPES))
        return value

class Class(BaseModel):
    name: str
    attributes: Optional[List[Attribute]]
    methods: Optional[List[str]]
    superclasses: Optional[List[str]]

class Module(BaseModel):
    filename: Optional[str]
    version: Optional[str]
    variables: Optional[dict]
    functions: Optional[List[str]]
    classes: Optional[List[Class]]

class Deployment(BaseModel):
    runtimes: Optional[List[Runtime]]
    environment: Optional[str]
    
class SpyModel(Module):
    deployments: Optional[List[Deployment]]

    @classmethod
    def from_module(cls, info_module: ModuleType):
        module_utils = ModuleUtils()
        runtime_utils = RuntimeUtils()
        sytem_utils = SystemUtils()
        python_utils = PythonUtils()
        info_module = module_utils.load_module(info_module)
        logger.debug(f"Create SpyModel from info_module: {ModuleType}")
        filename = "/".join(info_module.__file__.split('/')[-1:])
        version = module_utils.extract_version(info_module)
        variables = module_utils.extract_variables(info_module)
        functions = module_utils.extract_functions(info_module)
        classes = [
            Class(name=name,
                       class_attr=class_attr,
                       instance_attr=instance_attr,
                       methods=methods,
                       superclasses=superclasses)
            for
            name,
            class_attr,
            instance_attr,
            methods,
            superclasses
            in module_utils.extract_classes(info_module)
        ]
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
                            system=[
                                System(
                                    os=os,
                                    envs=envs,
                                    python=[
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
            ],
        )
