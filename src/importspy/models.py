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
    ClassInfo
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
    version: Optional[str]
    interpreter: Optional[str]
    modules: Optional[List['Module']] = None

class System(BaseModel):

    os: Optional[str] = None
    envs: Optional[dict] = Field(default=None, repr=False)
    pythons: Optional[List[Python]] = None

class Runtime(BaseModel):

    arch: Optional[str] = None
    systems: Optional[List[System]] = None

    @field_validator('arch')
    def validate_arch(cls, value:str):
        if value not in Constants.KNOWN_ARCHITECTURES:
            raise ValueError(Errors.INVALID_ARCHITECTURE.format(value, Constants.KNOWN_ARCHITECTURES))
        return value

class Attribute(BaseModel):
    type: str
    name: str
    value: Optional[Union[int, str, float, bool, None]] = None

    @field_validator('type')
    def validate_arch(cls, value:str):
        if value not in Constants.ATTRIBUTE_TYPES:
            raise ValueError(Errors.INVALID_ATTRIBUTE_TYPE.format(value, Constants.ATTRIBUTE_TYPES))
        return value
    

class Class(BaseModel):
    name: str
    attributes: Optional[List[Attribute]] = None
    methods: Optional[List[str]] = None
    superclasses: Optional[List[str]] = None

class Module(BaseModel):
    filename: Optional[str] = None
    version: Optional[str] = None
    variables: Optional[dict] = None
    functions: Optional[List[str]] = None
    classes: Optional[List[Class]] = None

class Deployment(BaseModel):
    runtimes: Optional[List[Runtime]] = None
    environment: Optional[str] = None
    
class SpyModel(Module):
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
        classes = cls._class_adaper(module_utils.extract_classes(info_module))
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
    
    def _class_adaper(extracted_classes:List[ClassInfo]):
        classes = []
        for name, class_attr, instance_attr, methods, superclasses in extracted_classes:
            classes.append(Class(name=name,
                  attributes=
                    [
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
                  methods=methods,
                  superclasses=superclasses
                )
            )
        return classes
