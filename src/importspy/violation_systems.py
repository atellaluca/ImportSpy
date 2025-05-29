from abc import (
    ABC,
    abstractmethod
)

from dataclasses import (
    dataclass,
    field
)

from .violation_systems import Bundle

from typing import (
    Optional,
    Any
)

from .constants import Errors

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

    def __init__(self, context, bundle:Bundle):
        
        self._context = context
        self.bundle = bundle
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

    def __init__(self, scope:str, context:str, bundle:'Bundle'):
        super().__init__(context, bundle)
        self.scope = scope
    
    @property
    def label(self) -> str:
        return Errors.VARIABLES_LABEL_TEMPLATE[self.scope][self.context].format(**self.bundle)

class FunctionContractViolation(BaseContractViolation):

    def __init__(self, context:str, bundle:'Bundle'):
        super().__init__(context, bundle)
    
    @property
    def label(self) -> str:
        return Errors.FUNCTIONS_LABEL_TEMPLATE[self.context].format(**self.bundle)

class RuntimeContractViolation(BaseContractViolation):

    def __init__(self, context:str, bundle:'Bundle'):
        super().__init__(context, bundle)
    
    @property
    def label(self) -> str:
        return self.bundle[Errors.KEY_RUNTIMES_1]

class SystemContractViolation(BaseContractViolation):

    def __init__(self, context:str, bundle:'Bundle'):
        super().__init__(context, bundle)
    
    @property
    def label(self) -> str:
        return self.bundle[Errors.KEY_SYSTEMS_1]

class PythonContractViolation(BaseContractViolation):

    def __init__(self, context:str, bundle:'Bundle'):
        super().__init__(context, bundle)
    
    @property
    def label(self) -> str:
        return self.bundle[Errors.KEY_PYTHON_1]

class ModuleContractViolation(BaseContractViolation):

    def __init__(self, context:str, bundle:'Bundle'):
        super().__init__(context, bundle)
    
    @property
    def label(self) -> str:
        return Errors.MODULE_LABEL_TEMPLATE[self.context].format(**self.bundle)

@dataclass
class Bundle:

    state: Optional[dict[str, Any]] = field(default_factory=dict)

    def __getitem__(self, key):
        return self.state[key]
    
    def __len__(self):
        return len(self.state)
    
    def __setitem__(self, key, value):
        self.state[key] = value
    
    def __repr__(self):
        return repr(self.state)