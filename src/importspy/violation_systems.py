from abc import (
    ABC,
    abstractmethod
)

from dataclasses import (
    dataclass,
    field
)

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
    
    @abstractmethod
    def label(self, spec:str) -> str:
        pass
    
    @abstractmethod
    def missing_error_handler(self, spec:str) -> str:
        pass

    @abstractmethod
    def mismatch_error_handler(self, spec:str) -> str:
        pass

    @abstractmethod
    def invalid_error_handler(self, spec:str) -> str:
        pass

class BaseContractViolation(ContractViolation):

    def __init__(self, context, bundle:'Bundle'):
        
        self._context = context
        self.bundle = bundle
        super().__init__()

    @property
    def context(self) -> str:
        return self._context
    
    def missing_error_handler(self, spec:str) -> str:
        return f'{Errors.CONTEXT_INTRO[self.context]}: {Errors.ERROR_MESSAGE_TEMPLATES[Errors.Category.MISSING][Errors.TEMPLATE_KEY].format(label=self.label(spec))} - {Errors.ERROR_MESSAGE_TEMPLATES[self.category][Errors.SOLUTION_KEY].format(label=self.label(spec)).capitalize()}'

    def mismatch_error_handler(self, expected:Any, actual:Any, spec:str) -> str:
        return f'{Errors.CONTEXT_INTRO[self.context]}: {Errors.ERROR_MESSAGE_TEMPLATES[Errors.Category.MISMATCH][Errors.TEMPLATE_KEY].format(label=self.label(spec))} - {Errors.ERROR_MESSAGE_TEMPLATES[self.category][Errors.SOLUTION_KEY].format(label=self.label(spec), expected=expected, actual=actual).capitalize()}'

    def invalid_error_handler(self, allowed:Any, found:Any, spec:str) -> str:
        return f'{Errors.CONTEXT_INTRO[self.context]}: {Errors.ERROR_MESSAGE_TEMPLATES[Errors.Category.INVALID][Errors.TEMPLATE_KEY].format(label=self.label(spec))} - {Errors.ERROR_MESSAGE_TEMPLATES[self.category][Errors.SOLUTION_KEY].format(label=self.label(spec), expected=allowed, actual=found).capitalize()}'

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
    
    def label(self, spec:str) -> str:
        return Errors.FUNCTIONS_LABEL_TEMPLATE[spec][self.context].format(**self.bundle)

class RuntimeContractViolation(BaseContractViolation):

    def __init__(self, context:str, bundle:'Bundle'):
        super().__init__(context, bundle)
    
    def label(self, spec:str) -> str:
        return Errors.RUNTIME_LABEL_TEMPLATE[spec]

class SystemContractViolation(BaseContractViolation):

    def __init__(self, context:str, bundle:'Bundle'):
        super().__init__(context, bundle)
    
    def label(self, spec:str) -> str:
        return Errors.SYSTEM_LABEL_TEMPLATE[spec]

class PythonContractViolation(BaseContractViolation):

    def __init__(self, context:str, bundle:'Bundle'):
        super().__init__(context, bundle)
    
    @property
    def label(self, spec:str) -> str:
        return Errors.PYTHON_LABEL_TEMPLATE[spec]

class ModuleContractViolation(BaseContractViolation):

    def __init__(self, context:str, bundle:'Bundle'):
        super().__init__(context, bundle)
    
    @property
    def label(self, spec:str) -> str:
        return Errors.MODULE_LABEL_TEMPLATE[spec][self.context].format(**self.bundle)

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