from abc import (
    ABC,
    abstractmethod
)

from collections.abc import MutableMapping

from dataclasses import (
    dataclass,
    field
)

from typing import (
    Optional,
    Any,
    Iterator
)

from .constants import Errors

class ContractViolation(ABC):

    @property
    @abstractmethod
    def context(self) -> str:
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
        return f'{Errors.CONTEXT_INTRO[self.context]}: {Errors.ERROR_MESSAGE_TEMPLATES[Errors.Category.MISSING][spec][Errors.TEMPLATE_KEY].format(label=self.label(spec))} - {Errors.ERROR_MESSAGE_TEMPLATES[Errors.Category.MISSING][spec][Errors.SOLUTION_KEY].capitalize()}'

    def mismatch_error_handler(self, expected:Any, actual:Any, spec:str) -> str:
        return f'{Errors.CONTEXT_INTRO[self.context]}: {Errors.ERROR_MESSAGE_TEMPLATES[Errors.Category.MISMATCH][spec][Errors.TEMPLATE_KEY].format(label=self.label(spec), expected=expected, actual=actual)} - {Errors.ERROR_MESSAGE_TEMPLATES[Errors.Category.MISMATCH][spec][Errors.SOLUTION_KEY].capitalize()}'

    def invalid_error_handler(self, allowed:Any, found:Any, spec:str) -> str:
        return f'{Errors.CONTEXT_INTRO[self.context]}: {Errors.ERROR_MESSAGE_TEMPLATES[Errors.Category.INVALID][spec][Errors.TEMPLATE_KEY].format(label=self.label(spec), expected=allowed, actual=found)} - {Errors.ERROR_MESSAGE_TEMPLATES[Errors.Category.INVALID][spec][Errors.SOLUTION_KEY].capitalize()}'

class VariableContractViolation(BaseContractViolation):

    def __init__(self, scope:str, context:str, bundle:'Bundle'):
        super().__init__(context, bundle)
        self.scope = scope
    
    def label(self, spec:str) -> str:
        return Errors.VARIABLES_LABEL_TEMPLATE[self.scope][spec][self.context].format(**self.bundle)

class FunctionContractViolation(BaseContractViolation):

    def __init__(self, context:str, bundle:'Bundle'):
        super().__init__(context, bundle)
    
    def label(self, spec:str) -> str:
        return Errors.FUNCTIONS_LABEL_TEMPLATE[spec][self.context].format(**self.bundle)

class RuntimeContractViolation(BaseContractViolation):

    def __init__(self, context:str, bundle:'Bundle'):
        super().__init__(context, bundle)
    
    def label(self, spec:str) -> str:
        return Errors.RUNTIME_LABEL_TEMPLATE[spec].format(**self.bundle)

class SystemContractViolation(BaseContractViolation):

    def __init__(self, context:str, bundle:'Bundle'):
        super().__init__(context, bundle)
    
    def label(self, spec:str) -> str:
        return Errors.SYSTEM_LABEL_TEMPLATE[spec].format(**self.bundle)

class PythonContractViolation(BaseContractViolation):

    def __init__(self, context:str, bundle:'Bundle'):
        super().__init__(context, bundle)
    
    def label(self, spec:str) -> str:
        return Errors.PYTHON_LABEL_TEMPLATE[spec].format(**self.bundle)

class ModuleContractViolation(BaseContractViolation):

    def __init__(self, context:str, bundle:'Bundle'):
        super().__init__(context, bundle)
    
    def label(self, spec:str) -> str:
        return Errors.MODULE_LABEL_TEMPLATE[spec][self.context].format(**self.bundle)

@dataclass
class Bundle(MutableMapping):
    state: Optional[dict[str, Any]] = field(default_factory=dict)

    def __getitem__(self, key):
        return self.state[key]
    
    def __setitem__(self, key, value):
        self.state[key] = value

    def __delitem__(self, key):
        del self.state[key]

    def __iter__(self) -> Iterator:
        return iter(self.state)

    def __len__(self) -> int:
        return len(self.state)

    def __repr__(self):
        return repr(self.state)