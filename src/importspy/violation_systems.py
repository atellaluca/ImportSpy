"""
This module defines the hierarchy of contract violation classes used by ImportSpy.

Each violation type corresponds to a validation context (e.g., environment, runtime, module structure),
and provides structured, human-readable error messages when the importing module does not meet the
contract’s requirements.

The base interface `ContractViolation` defines the common error interface, while specialized classes
like `VariableContractViolation` or `RuntimeContractViolation` define formatting logic for each scope.

Violations carry a dynamic `Bundle` object, which collects contextual metadata needed for
formatting error messages and debugging failed imports.
"""

from abc import ABC, abstractmethod
from collections.abc import MutableMapping
from dataclasses import dataclass, field
from typing import Optional, Any, Iterator
from .constants import Errors


class ContractViolation(ABC):
    """
    Abstract base interface for all contract violations.

    Defines the core methods for rendering structured error messages,
    including context resolution and label generation.

    Properties:
    -----------
    - `context`: Validation context (e.g., environment, class, runtime)
    - `label(spec)`: Retrieves the field name or reference used in error text.
    - `missing_error_handler(spec)`: Formats error when required entity is missing.
    - `mismatch_error_handler(expected, actual, spec)`: Formats error when values differ.
    - `invalid_error_handler(allowed, found, spec)`: Formats error when a value is invalid.
    """

    @property
    @abstractmethod
    def context(self) -> str:
        pass

    @abstractmethod
    def label(self, spec: str) -> str:
        pass

    @abstractmethod
    def missing_error_handler(self, spec: str) -> str:
        pass

    @abstractmethod
    def mismatch_error_handler(self, expected: Any, actual: Any, spec: str) -> str:
        pass

    @abstractmethod
    def invalid_error_handler(self, allowed: Any, found: Any, spec: str) -> str:
        pass


class BaseContractViolation(ContractViolation):
    """
    Base implementation of a contract violation.

    Includes default implementations of error formatting methods.
    """

    def __init__(self, context: str, bundle: 'Bundle'):
        self._context = context
        self.bundle = bundle
        super().__init__()

    @property
    def context(self) -> str:
        return self._context

    def missing_error_handler(self, spec: str) -> str:
        return (
            f"{Errors.CONTEXT_INTRO[self.context]}: "
            f"{Errors.ERROR_MESSAGE_TEMPLATES[Errors.Category.MISSING][spec][Errors.TEMPLATE_KEY].format(label=self.label(spec))} - "
            f"{Errors.ERROR_MESSAGE_TEMPLATES[Errors.Category.MISSING][spec][Errors.SOLUTION_KEY].capitalize()}"
        )

    def mismatch_error_handler(self, expected: Any, actual: Any, spec: str) -> str:
        return (
            f"{Errors.CONTEXT_INTRO[self.context]}: "
            f"{Errors.ERROR_MESSAGE_TEMPLATES[Errors.Category.MISMATCH][spec][Errors.TEMPLATE_KEY].format(label=self.label(spec), expected=expected, actual=actual)} - "
            f"{Errors.ERROR_MESSAGE_TEMPLATES[Errors.Category.MISMATCH][spec][Errors.SOLUTION_KEY].capitalize()}"
        )

    def invalid_error_handler(self, allowed: Any, found: Any, spec: str) -> str:
        return (
            f"{Errors.CONTEXT_INTRO[self.context]}: "
            f"{Errors.ERROR_MESSAGE_TEMPLATES[Errors.Category.INVALID][spec][Errors.TEMPLATE_KEY].format(label=self.label(spec), expected=allowed, actual=found)} - "
            f"{Errors.ERROR_MESSAGE_TEMPLATES[Errors.Category.INVALID][spec][Errors.SOLUTION_KEY].capitalize()}"
        )


class VariableContractViolation(BaseContractViolation):
    """
    Contract violation handler for variables (module, class, environment, etc.).

    Includes scope information to distinguish between types of variables.
    """

    def __init__(self, scope: str, context: str, bundle: 'Bundle'):
        super().__init__(context, bundle)
        self.scope = scope

    def label(self, spec: str) -> str:
        return Errors.VARIABLES_LABEL_TEMPLATE[self.scope][spec][self.context].format(**self.bundle)


class FunctionContractViolation(BaseContractViolation):
    """
    Contract violation handler for function signature mismatches.
    """

    def __init__(self, context: str, bundle: 'Bundle'):
        super().__init__(context, bundle)

    def label(self, spec: str) -> str:
        return Errors.FUNCTIONS_LABEL_TEMPLATE[spec][self.context].format(**self.bundle)


class RuntimeContractViolation(BaseContractViolation):
    """
    Contract violation handler for runtime architecture mismatches.
    """

    def __init__(self, context: str, bundle: 'Bundle'):
        super().__init__(context, bundle)

    def label(self, spec: str) -> str:
        return Errors.RUNTIME_LABEL_TEMPLATE[spec].format(**self.bundle)


class SystemContractViolation(BaseContractViolation):
    """
    Contract violation handler for system-level mismatches (OS, environment variables).
    """

    def __init__(self, context: str, bundle: 'Bundle'):
        super().__init__(context, bundle)

    def label(self, spec: str) -> str:
        return Errors.SYSTEM_LABEL_TEMPLATE[spec].format(**self.bundle)

class PythonContractViolation(BaseContractViolation):
    """
    Contract violation handler for Python version and interpreter mismatches.
    """

    def __init__(self, context: str, bundle: 'Bundle'):
        super().__init__(context, bundle)

    def label(self, spec: str) -> str:
        return Errors.PYTHON_LABEL_TEMPLATE[spec].format(**self.bundle)


class ModuleContractViolation(BaseContractViolation):
    """
    Contract violation handler for module-level mismatches (filename, version, structure).
    """

    def __init__(self, context: str, bundle: 'Bundle'):
        super().__init__(context, bundle)

    def label(self, spec: str) -> str:
        return Errors.MODULE_LABEL_TEMPLATE[spec][self.context].format(**self.bundle)


@dataclass
class Bundle(MutableMapping):
    """
    Shared mutable state passed to all violation handlers.

    The bundle is a dynamic container used to inject contextual values
    (like module name, attribute name, or class name) into error templates.
    """

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
