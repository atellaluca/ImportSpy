"""
importspy.s
===========

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
from .models import SpyModel
from .utilities.module_util import ModuleUtil
from .validators.spymodel_validator import SpyModelValidator
from .log_manager import LogManager
from .persistences import Parser, YamlParser
from typing import Optional
import logging


class Spy:
    """
    The `Spy` class is the core engine of ImportSpy — it handles validation, introspection, 
    and enforcement of structural contracts for Python modules.

    This class is designed to support both:

    - **Embedded validation**, where it is imported and executed inside the module under control.
    - **CLI-based or pipeline validation**, where an external tool invokes Spy programmatically.

    ImportSpy uses declarative **import contracts**, written as human-readable YAML files, 
    to describe what a valid module should contain. These contracts define expected classes, 
    attributes, methods, and even environmental constraints (like Python version or OS).

    The `Spy` class dynamically loads the target module, extracts its metadata, and checks 
    for compliance against the contract. If validation fails, descriptive errors are raised 
    before the module can be used improperly.

    Attributes:
    -----------
    logger : logging.Logger
        Logger instance used to track validation steps and internal processing.

    parser : Parser
        Parser responsible for loading the import contract from disk (currently supports YAML).

    Methods:
    --------
    - `__init__()` → Initializes logger and default parser.
    - `importspy(filepath, log_level, info_module)` → Validates a specified or inferred module.
    - `_configure_logging(log_level)` → Sets logging level based on user/system config.
    - `_validate_module(contract, info_module)` → Compares a module to the contract definition.
    - `_inspect_module()` → Introspects the call stack to locate the calling module.
    """

    def __init__(self):
        """
        Initializes the `Spy` instance.

        This method sets up:
        - the logging system for capturing all validation and introspection steps
        - the default parser (`YamlParser`) for loading `.yml` import contracts
        """
        self.logger = LogManager().get_logger(self.__class__.__name__)
        self.parser: Parser = YamlParser()

    def importspy(self,
                  filepath: Optional[str] = None,
                  log_level: Optional[int] = None,
                  info_module: Optional[ModuleType] = None) -> ModuleType:
        """
        Loads and validates a Python module based on an import contract.

        This is the primary method used to validate a module, whether in embedded mode
        (by inspecting the importer), or in external mode (via CLI or script).

        Parameters:
        -----------
        filepath : Optional[str]
            Path to the `.yml` contract file defining the expected structure.

        log_level : Optional[int]
            Logging level for output verbosity. Uses system default if not provided.

        info_module : Optional[ModuleType]
            Optional reference to the module to validate. If not provided,
            the calling module is inferred via stack inspection.

        Returns:
        --------
        ModuleType
            The module that was validated.

        Raises:
        -------
        RuntimeError
            If logging is misconfigured or reconfigured unexpectedly.

        ValueError
            If a recursion pattern is detected (e.g., a module validating itself).
        """
        self._configure_logging(log_level)
        spymodel: SpyModel = SpyModel(**self.parser.load(filepath=filepath))
        if not info_module:
            info_module = self._inspect_module()
        return self._validate_module(spymodel, info_module)

    def _configure_logging(self, log_level: Optional[int] = None):
        """
        Configures ImportSpy's logging system for runtime use.

        If a log level is provided, it overrides the system's default. This method ensures
        the logger is only configured once, preventing duplicate log handlers.

        Parameters:
        -----------
        log_level : Optional[int]
            The desired log level (e.g., logging.INFO, logging.DEBUG).
        """
        log_manager = LogManager()
        if not log_manager.configured:
            system_log_level = logging.getLogger().getEffectiveLevel()
            log_manager.configure(level=log_level or system_log_level)

    def _validate_module(self, spymodel: SpyModel, info_module: ModuleType) -> ModuleType:
        """
        Compares a module's structure against the loaded import contract.

        This includes checking for:
        - required classes and methods
        - expected variable names and values
        - inheritance and method signatures

        Parameters:
        -----------
        spymodel : SpyModel
            Parsed import contract used as the validation baseline.

        info_module : ModuleType
            The actual module being validated.

        Returns:
        --------
        ModuleType
            The validated module.

        Raises:
        -------
        ValueError
            If the module does not conform to the expected structure.
        """
        self.logger.debug(f"info_module: {info_module}")
        if spymodel:
            self.logger.debug(f"Import contract detected: {spymodel}")
            spy_module = SpyModel.from_module(info_module)
            self.logger.debug(f"Extracted module structure: {spy_module}")
            SpyModelValidator().validate(spymodel, spy_module)
        return ModuleUtil().load_module(info_module)

    def _inspect_module(self) -> ModuleType:
        """
        Introspects the call stack to determine which module called `importspy()`.

        This is used primarily in embedded mode to locate the external plugin
        or module that triggered the validation. It prevents the system from
        analyzing itself (recursive inspection).

        Returns:
        --------
        ModuleType
            The module that imported or triggered validation.

        Raises:
        -------
        ValueError
            If recursion is detected (i.e., the same module is inspecting itself).
        """
        module_util = ModuleUtil()
        current_frame, caller_frame = module_util.inspect_module()
        if current_frame.filename == caller_frame.filename:
            raise ValueError("Recursion detected during module analysis.")

        info_module = module_util.get_info_module(caller_frame)
        self.logger.debug(f"Inferred caller module: {info_module}")
        return info_module
