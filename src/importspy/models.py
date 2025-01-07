from pydantic import BaseModel, field_validator
from typing import (
    Optional, 
    List,
    Any
)
from types import ModuleType
from .utils import spy_module_utils
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
    os: Optional[dict]
    envs: Optional[List[str]]
    python: Optional[List[Python]]

class Runtime(BaseModel):
    arch: Optional[str]
    system: List[System]

    @field_validator('arch')
    def validate_arch(cls, value:str):
        if value not in Constants.KNOWN_ARCHITECTURES:
            raise ValueError(Errors.INVALID_ARCHITECTURE.format(value, Constants.KNOWN_ARCHITECTURES))
        return value

class Attribute(BaseModel):
    type: str
    name: str
    value: Optional[Any]

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
    runtime: Optional[Runtime]
    deployments: Optional[Deployment]
