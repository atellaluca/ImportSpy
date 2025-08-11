"""
Core validation logic for ImportSpy.

This module defines the `Spy` class, the central component responsible for dynamically 
inspecting and validating Python modules against **import contracts** (YAML files that declare 
expected structure and execution context). 

The validation can be triggered in two ways:

- **Embedded validation**: when the `Spy` is embedded inside a core module and validates its importer.
- **External validation (CLI/pipeline)**: when a separate process uses `Spy` to check a module before runtime.

Validation covers classes, attributes, functions, and environmental settings like OS, Python version,
and interpreter.

This module is typically used as the entry point for programmatic validation workflows.
"""

from types import ModuleType
from .models import (
    SpyModel,
    Runtime,
    Python,
    Module
)
from .utilities.module_util import ModuleUtil
from .validators import (
    RuntimeValidator,
    SystemValidator,
    PythonValidator,
    ModuleValidator
)
from .log_manager import LogManager
from .persistences import Parser, YamlParser
from typing import (
    Optional,
    List
)
import logging
from .violation_systems import (
    Bundle,
    ModuleContractViolation,
    RuntimeContractViolation,
    SystemContractViolation,
    PythonContractViolation
)
from .constants import Contexts


class Spy:
    """
    Core validation engine for ImportSpy.

    The `Spy` class is responsible for loading a target module, extracting its structure,
    and validating it against a YAML-based import contract. This ensures that the importing
    module satisfies all declared structural and runtime constraints.

    It supports two modes:
    - **Embedded mode**: validates the caller of the current module
    - **External/CLI mode**: validates an explicitly provided module

    Attributes:
    -----------

    logger : logging.Logger
        Structured logger for validation diagnostics.

    parser : Parser 
        Parser used to load import contracts (defaults to YAML).
        
    """

    def __init__(self):
        """
        Initialize the Spy instance.

        Sets up a dedicated logger and the default YAML parser
        """
        self.logger = LogManager().get_logger(self.__class__.__name__)
        self.parser: Parser = YamlParser()

    def importspy(self,
                  filepath: Optional[str] = None,
                  log_level: Optional[int] = None,
                  info_module: Optional[ModuleType] = None) -> ModuleType:
        """
        Main entry point for validation.

        Loads and validates a Python module against the contract defined in the given YAML file.
        If no module is explicitly provided, introspects the call stack to infer the caller.

        Parameters:
        -----------

        filepath : Optional[str]
            Path to the `.yml` import contract.

        log_level : Optional[int]
            Log verbosity level (e.g., `logging.DEBUG`).

        info_module : Optional[ModuleType]
            The module to validate. If `None`, uses the importer via stack inspection.

        Returns:
        --------
        ModuleType
            The validated module.

        Raises:
        -------
        RuntimeError
            If logging setup fails.

        ValueError
            If recursion is detected (e.g., a module is validating itself).
        """
        self._configure_logging(log_level)
        spymodel: SpyModel = SpyModel(**self.parser.load(filepath=filepath))
        if not info_module:
            info_module = self._inspect_module()
        return self._validate_module(spymodel, info_module)

    def _configure_logging(self, log_level: Optional[int] = None):
        """
        Set up logging for validation.

        If not already configured, applies the provided or default log level
        using ImportSpy’s centralized logging system.

        Parameters:
        -----------
        log_level : Optional[int]
            Logging level to use (e.g., `logging.INFO`, `logging.DEBUG`).
        """
        log_manager = LogManager()
        if not log_manager.configured:
            system_log_level = logging.getLogger().getEffectiveLevel()
            log_manager.configure(level=log_level or system_log_level)

    def _validate_module(self, spymodel: SpyModel, info_module: ModuleType) -> ModuleType:
        """
        Perform all validation steps against the loaded module.

        This includes contract-level, runtime, system, and Python environment checks.
        All contract violations are collected in a `Bundle`.

        Parameters:
        -----------
        spymodel : SpyModel
            The expected contract loaded from file.

        info_module : ModuleType
            The actual module to inspect and validate.

        Returns:
        --------
        ModuleType
            The validated module, reloaded after introspection.
        """
        self.logger.debug(f"info_module: {info_module}")
        if spymodel:
            bundle = Bundle()
            module_validator = ModuleValidator()
            self.logger.debug(f"Import contract detected: {spymodel}")
            spy_module = SpyModel.from_module(info_module)
            self.logger.debug(f"Extracted module structure: {spy_module}")

            module_contract = ModuleContractViolation(Contexts.MODULE_CONTEXT, bundle)
            module_validator.validate([spymodel], spy_module.deployments[0].systems[0].pythons[0].modules[0], module_contract)

            runtime_contract = RuntimeContractViolation(Contexts.RUNTIME_CONTEXT, bundle)
            runtime = RuntimeValidator().validate(spymodel.deployments, spy_module.deployments, runtime_contract)

            system_contract = SystemContractViolation(Contexts.RUNTIME_CONTEXT, bundle)
            pythons = SystemValidator().validate(runtime.systems, spy_module.deployments[0].systems, system_contract)

            python_contract = PythonContractViolation(Contexts.RUNTIME_CONTEXT, bundle)
            modules = PythonValidator().validate(pythons, spy_module.deployments[0].systems[0].pythons, python_contract)

            module_validator.validate(modules, spy_module.deployments[0].systems[0].pythons[0].modules[0], module_contract)

        return ModuleUtil().load_module(info_module)

    def _inspect_module(self) -> ModuleType:
        """
        Infer the module that invoked validation (embedded mode).

        This prevents a module from validating itself and ensures that
        ImportSpy targets the correct caller in the stack.

        Returns:
        --------
        
        ModuleType
            The inferred external module.

        Raises:
        -------
        ValueError
            If a module attempts to validate itself.
        """
        module_util = ModuleUtil()
        current_frame, caller_frame = module_util.inspect_module()
        if current_frame.filename == caller_frame.filename:
            raise ValueError("Recursion detected during module analysis.")
        info_module = module_util.get_info_module(caller_frame)
        self.logger.debug(f"Inferred caller module: {info_module}")
        return info_module
