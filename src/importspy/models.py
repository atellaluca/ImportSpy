"""
importspy.models
----------------

This module defines the core data models used by ImportSpy for contract-based
runtime validation of Python modules. It includes structural representations
of variables, functions, classes, and full modules, as well as runtime and
system-level metadata required to enforce import contracts across execution contexts.
"""

from pydantic import BaseModel

from typing import (
    Optional,
    Union,
    Any,
    List
)

from abc import (
    ABC,
    abstractmethod
)

from dataclasses import dataclass, asdict

from types import ModuleType

from .utilities.module_util import (
    ModuleUtil, ClassInfo, ArgumentInfo,
    FunctionInfo, AttributeInfo, VariableInfo
)
from .utilities.runtime_util import RuntimeUtil
from .utilities.system_util import SystemUtil
from .utilities.python_util import PythonUtil
from .constants import (
    Constants,
    Contexts,
    Errors
)
import logging

logger = logging.getLogger("/".join(__file__.split('/')[-2:]))
logger.addHandler(logging.NullHandler())


class Python(BaseModel):
    """
    Represents a specific Python runtime configuration.

    Includes the Python version, interpreter type, and the list of loaded modules.
    Used to validate compatibility between caller and callee environments.
    """
    version: Optional[Constants.SupportedPythonVersions] = None
    interpreter: Optional[Constants.SupportedPythonImplementations] = None
    modules: list['Module']

class Environment(BaseModel):
    """
    Represents a set of environment variables and secret keys
    defined for the system or application runtime.
    """
    variables: Optional[list['Variable']] = None
    secrets: Optional[list[str]] = None

class System(BaseModel):
    """
    Represents the system environment, including OS, environment variables,
    and Python runtimes configured within the system.
    """
    os: Constants.SupportedOS
    environment: Optional[Environment] = None
    pythons: list[Python]


class Runtime(BaseModel):
    """
    Represents the deployment runtime, identified by CPU architecture and
    the list of supported systems associated with that architecture.
    """
    arch: Constants.SupportedArchitectures
    systems: list[System]


class Variable(BaseModel):
    """
    Represents a declared variable within a Python module, including optional type
    annotation and value. Used for structural validation of the importing module.
    """
    name: str
    annotation: Optional[Constants.SupportedAnnotations] = None
    value: Optional[Union[int, str, float, bool, None]] = None

    @classmethod
    def from_variable_info(cls, variables_info: list[VariableInfo]):
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
    type: Constants.SupportedClassAttributeTypes

    @classmethod
    def from_attributes_info(cls, attributes_info: list[AttributeInfo]):
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
    def from_arguments_info(cls, arguments_info: list[ArgumentInfo]):
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
    arguments: Optional[list[Argument]] = None
    return_annotation: Optional[Constants.SupportedAnnotations] = None

    @classmethod
    def from_functions_info(cls, functions_info: list[FunctionInfo]):
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
    attributes: Optional[list[Attribute]] = None
    methods: Optional[list[Function]] = None
    superclasses: Optional[list[str]] = None

    @classmethod
    def from_class_info(cls, extracted_classes: list[ClassInfo]):
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
    variables: Optional[list[Variable]] = None
    functions: Optional[list[Function]] = None
    classes: Optional[list[Class]] = None


class SpyModel(Module):
    """
    Extends the base Module structure with additional deployment metadata.

    SpyModel is the top-level object representing a module's structure and its
    runtime/environment constraints. This is the core of ImportSpy's contract model.
    """
    deployments: Optional[list[Runtime]] = None

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

class Error(BaseModel):

    context: Contexts
    title: str
    category: Errors.Category
    description: str
    solution: str

    @classmethod
    def from_contract_violation(cls, contract_violation: 'ContractViolation'):
        tpl = Errors.ERROR_MESSAGE_TEMPLATES.get(contract_violation.category)
        title = Errors.CONTEXT_INTRO.get(contract_violation.context)
        description = tpl[Errors.TEMPLATE_KEY].format(label=contract_violation.label)
        solution = tpl[Errors.SOLUTION_KEY]
        return cls(
            context=contract_violation.context,
            title=title,
            category=contract_violation.category,
            description=description,
            solution=solution
        )

    def render_message(self) -> str:
        return f"[{self.title}] {self.description} {self.solution}"
        
class ContractViolation(ABC):

    @property
    @abstractmethod
    def context(self) -> str:
        pass
    
    @property
    @abstractmethod
    def category(self) -> str:
        pass
    
    @property
    @abstractmethod
    def label(self) -> str:
        pass
    
    @abstractmethod
    def missing_error_handler(self) -> str:
        pass

    @abstractmethod
    def mismatch_error_handler(self) -> str:
        pass

    @abstractmethod
    def invalid_error_handler(self) -> str:
        pass

class BaseContractViolation(ContractViolation):

    def __init__(self, context, category):
        
        self._context = context
        self._category = category
        super().__init__()

    @property
    def context(self) -> str:
        return self._context
    
    @property
    def category(self) -> str:
        return self._category
    
    def missing_error_handler(self) -> str:
        return f'{Errors.CONTEXT_INTRO[self.context]}: {Errors.ERROR_MESSAGE_TEMPLATES[self.category][Errors.TEMPLATE_KEY].format(label=self.label)} - {Errors.ERROR_MESSAGE_TEMPLATES[self.category][Errors.SOLUTION_KEY].format(label=self.label).capitalize()}'

    def mismatch_error_handler(self, expected:Any, actual:Any) -> str:
        return f'{Errors.CONTEXT_INTRO[self.context]}: {Errors.ERROR_MESSAGE_TEMPLATES[self.category][Errors.TEMPLATE_KEY].format(label=self.label)} - {Errors.ERROR_MESSAGE_TEMPLATES[self.category][Errors.SOLUTION_KEY].format(label=self.label, expected=expected, actual=actual).capitalize()}'

    def invalid_error_handler(self, allowed:Any, found:Any) -> str:
        return f'{Errors.CONTEXT_INTRO[self.context]}: {Errors.ERROR_MESSAGE_TEMPLATES[self.category][Errors.TEMPLATE_KEY].format(label=self.label)} - {Errors.ERROR_MESSAGE_TEMPLATES[self.category][Errors.SOLUTION_KEY].format(label=self.label, expected=allowed, actual=found).capitalize()}'

class VariableContractViolation(BaseContractViolation):

    def __init__(self, scope:str, context:str, category:str, bundle:Union['ModuleBundle' ,'ClassBundle', 'EnvironmentBundle']):
        super().__init__(context, category)
        self.scope = scope
        self.bundle = bundle
    
    @property
    def label(self) -> str:
        return Errors.VARIABLES_LABEL_TEMPLATE[self.scope][self.context].format(**asdict(self.bundle))

class FunctionContractViolation(BaseContractViolation):

    def __init__(self, context:str, category:str, bundle:Union['ClassBundle', 'ModuleBundle']):
        super().__init__(context, category)
        self.bundle = bundle
    
    @property
    def label(self) -> str:
        return Errors.FUNCTIONS_LABEL_TEMPLATE[self.context].format(**asdict(self.bundle))

class RuntimeContractViolation(BaseContractViolation):

    def __init__(self, context:str, category:str, bundle:'RuntimeBundle'):
        super().__init__(context, category)
        self.bundle = bundle
    
    @property
    def label(self) -> str:
        return self.bundle.runtimes_1
    
@dataclass
class ClassBundle:

    class_name: Optional[str] = None
    attribute_type: Optional[str] = None
    attribute_name: Optional[str] = None
    argument_name: Optional[str] = None
    method_name: Optional[str] = None

@dataclass
class ModuleBundle:

    variable_name: Optional[str] = None
    module_name: Optional[str] = None
    argument_name: Optional[str] = None
    function_name: Optional[str] = None

@dataclass
class EnvironmentBundle:

    environment_variable_name: Optional[str] = None

class RuntimeBundle:

    runtimes_1: Optional[List[Runtime]] = None



