from abc import (
    ABC,
    abstractmethod
)

from dataclasses import dataclass, asdict

from typing import (
    Optional,
    Union,
    Any
)

from .constants import Errors
from .models import (
    System,
    Runtime,
    Module,
    Python
)

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

    def __init__(self, context):
        
        self._context = context
        super().__init__()

    @property
    def context(self) -> str:
        return self._context
    
    def missing_error_handler(self) -> str:
        return f'{Errors.CONTEXT_INTRO[self.context]}: {Errors.ERROR_MESSAGE_TEMPLATES[Errors.Category.MISSING][Errors.TEMPLATE_KEY].format(label=self.label)} - {Errors.ERROR_MESSAGE_TEMPLATES[self.category][Errors.SOLUTION_KEY].format(label=self.label).capitalize()}'

    def mismatch_error_handler(self, expected:Any, actual:Any) -> str:
        return f'{Errors.CONTEXT_INTRO[self.context]}: {Errors.ERROR_MESSAGE_TEMPLATES[Errors.Category.MISMATCH][Errors.TEMPLATE_KEY].format(label=self.label)} - {Errors.ERROR_MESSAGE_TEMPLATES[self.category][Errors.SOLUTION_KEY].format(label=self.label, expected=expected, actual=actual).capitalize()}'

    def invalid_error_handler(self, allowed:Any, found:Any) -> str:
        return f'{Errors.CONTEXT_INTRO[self.context]}: {Errors.ERROR_MESSAGE_TEMPLATES[Errors.Category.INVALID][Errors.TEMPLATE_KEY].format(label=self.label)} - {Errors.ERROR_MESSAGE_TEMPLATES[self.category][Errors.SOLUTION_KEY].format(label=self.label, expected=allowed, actual=found).capitalize()}'

class VariableContractViolation(BaseContractViolation):

    def __init__(self, scope:str, context:str, bundle:Union['ModuleBundle' ,'ClassBundle', 'EnvironmentBundle']):
        super().__init__(context)
        self.scope = scope
        self.bundle = bundle
    
    @property
    def label(self) -> str:
        return Errors.VARIABLES_LABEL_TEMPLATE[self.scope][self.context].format(**asdict(self.bundle))

class FunctionContractViolation(BaseContractViolation):

    def __init__(self, context:str, bundle:Union['ClassBundle', 'ModuleBundle']):
        super().__init__(context)
        self.bundle = bundle
    
    @property
    def label(self) -> str:
        return Errors.FUNCTIONS_LABEL_TEMPLATE[self.context].format(**asdict(self.bundle))

class RuntimeContractViolation(BaseContractViolation):

    def __init__(self, context:str, bundle:'RuntimeBundle'):
        super().__init__(context)
        self.bundle = bundle
    
    @property
    def label(self) -> str:
        return self.bundle.runtimes_1

class SystemContractViolation(BaseContractViolation):

    def __init__(self, context:str, bundle:'SystemBundle'):
        super().__init__(context)
        self.bundle = bundle
    
    @property
    def label(self) -> str:
        return self.bundle.systems_1

class PythonContractViolation(BaseContractViolation):

    def __init__(self, context:str, bundle:'PythonBundle'):
        super().__init__(context)
        self.bundle = bundle
    
    @property
    def label(self) -> str:
        return self.bundle.python_1


class ModuleContractViolation(BaseContractViolation):

    def __init__(self, context:str, bundle:'ModuleBundle'):
        super().__init__(context)
        self.bundle = bundle
    
    @property
    def label(self) -> str:
        return Errors.MODULE_LABEL_TEMPLATE[self.context].format(**asdict(self.bundle))
    
@dataclass
class ClassBundle:

    class_name: Optional[str] = None
    attribute_type: Optional[str] = None
    method_name: Optional[str] = None

@dataclass
class ModuleBundle:

    variable_name: Optional[str] = None
    module_1: Optional[Module] = None
    argument_name: Optional[str] = None
    function_name: Optional[str] = None

@dataclass
class EnvironmentBundle:

    environment_variable_name: Optional[str] = None

class RuntimeBundle:

    runtimes_1: Optional[list[Runtime]] = None

class SystemBundle:

    systems_1: Optional[list[System]] = None

class PythonBundle:

    python_1: Optional[Python] = None