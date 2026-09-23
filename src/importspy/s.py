"""Compatibility API for validating modules that have already executed.

Use ``AdmissionEngine`` for static admission before execution. The deprecated
``Spy`` API performs runtime introspection and cannot provide that guarantee.
"""

import warnings
from types import ModuleType

from .constants import Contexts, Errors
from .log_manager import LogManager
from .models import SpyModel
from .persistences import Parser, YamlParser
from .utilities.module_util import ModuleUtil
from .validators import (
    ModuleValidator,
    PythonValidator,
    RuntimeValidator,
    SystemValidator,
)
from .violation_systems import (
    Bundle,
    ModuleContractViolation,
    PythonContractViolation,
    RuntimeContractViolation,
    SystemContractViolation,
)


class Spy:
    """Legacy runtime validation for already loaded modules.

    ``importspy`` remains available throughout 0.5 and is scheduled for removal
    in 1.0. Runtime introspection can invoke dynamic Python attributes and must
    only be used with trusted, already admitted modules.
    """

    def __init__(self) -> None:
        self._log_manager = LogManager()
        self.logger = self._log_manager.get_logger(self.__class__.__name__)
        self.parser: Parser = YamlParser()

    def importspy(
        self,
        filepath: str | None = None,
        log_level: int | None = None,
        info_module: ModuleType | None = None,
    ) -> ModuleType:
        """Validate and return the same already loaded module without reloading.

        Deprecated since 0.5; use ``AdmissionEngine.check`` for pre-execution
        admission. If ``info_module`` is omitted, inspect the caller's module.
        A contract file is required. Validation failures raise ``ValueError``.
        """
        warnings.warn(
            "Spy.importspy is deprecated and validates already executed modules only; "
            "use AdmissionEngine.check for static admission. Removal is planned for 1.0.",
            DeprecationWarning,
            stacklevel=2,
        )
        if filepath is None:
            raise ValueError("A contract filepath is required for Spy.importspy.")
        self._configure_logging(log_level)
        spymodel = SpyModel.model_validate(self.parser.load(filepath=filepath))
        if info_module is None:
            info_module = self._inspect_module()
        return self._validate_module(spymodel, info_module)

    def _configure_logging(self, log_level: int | None = None) -> None:
        if not self._log_manager.configured and log_level is not None:
            self._log_manager.configure(level=log_level)

    def _validate_module(
        self, spymodel: SpyModel, info_module: ModuleType
    ) -> ModuleType:
        """Apply structural and optional deployment constraints to runtime state."""
        self.logger.debug("Validate already loaded module: %s", info_module.__name__)
        bundle = Bundle()
        observed = SpyModel.from_module(info_module)
        bundle[Errors.KEY_FILE_NAME] = observed.filename
        bundle[Errors.KEY_MODULE_NAME] = observed.filename

        module_validator = ModuleValidator()
        module_contract = ModuleContractViolation(Contexts.RUNTIME_CONTEXT, bundle)
        module_validator.validate([spymodel], observed, module_contract)

        if not spymodel.deployments:
            return info_module
        observed_deployments = observed.deployments or []
        runtime = RuntimeValidator().validate(
            spymodel.deployments,
            observed_deployments,
            RuntimeContractViolation(Contexts.RUNTIME_CONTEXT, bundle),
        )
        if runtime is None:
            return info_module
        observed_runtime = observed_deployments[0]
        pythons = SystemValidator().validate(
            runtime.systems,
            observed_runtime.systems,
            SystemContractViolation(Contexts.RUNTIME_CONTEXT, bundle),
        )
        if not pythons:
            return info_module
        modules = PythonValidator().validate(
            pythons,
            observed_runtime.systems[0].pythons,
            PythonContractViolation(Contexts.RUNTIME_CONTEXT, bundle),
        )
        module_validator.validate(modules, observed, module_contract)
        return info_module

    def _inspect_module(self) -> ModuleType:
        module_util = ModuleUtil()
        current_frame, caller_frame = module_util.inspect_module()
        if current_frame.filename == caller_frame.filename:
            raise ValueError("Recursion detected during module analysis.")
        info_module = module_util.get_info_module(caller_frame)
        if info_module is None:
            raise ValueError("The calling module could not be identified.")
        return info_module
