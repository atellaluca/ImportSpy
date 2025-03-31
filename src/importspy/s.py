from types import ModuleType
from .models import SpyModel
from .utilities.module_util import ModuleUtil
from .validators.spymodel_validator import SpyModelValidator
from .log_manager import LogManager
from .persistences import (
    Parser, YamlParser
)
from typing import Optional
import logging

class Spy:
    """
    Provides dynamic introspection, validation, and controlled loading of Python modules.

    The `Spy` class integrates centralized logging, introspection logic, 
    and validation mechanisms to ensure that dynamically loaded modules 
    adhere to a given structure defined by a `SpyModel`. It supports 
    structured configuration via external files (e.g., YAML) through pluggable parsers.

    Attributes:
    -----------
    logger : logging.Logger
        Logger instance associated with the `Spy` class.

    parser : Parser
        Parser instance responsible for loading model configurations from files.

    Methods:
    --------
    - `__init__()`: Initializes logger and default parser.
    - `importspy(filepath, log_level, info_module)`: Validates a given or inferred module using a `SpyModel`.
    - `_configure_logging(log_level)`: Ensures logging is set up correctly.
    - `_validate_module(spymodel, info_module)`: Validates a module against a given SpyModel.
    - `_inspect_module()`: Retrieves metadata about the calling module via stack introspection.

    Example:
    --------
    .. code-block:: python

        from importspy.spy import Spy

        spy = Spy()
        module = spy.importspy(filepath="spymodel.yml", log_level=logging.INFO)
    """

    def __init__(self):
        """
        Initializes the `Spy` instance.

        Sets up the logger and the default parser (`YamlParser`) used to 
        load serialized model configurations.

        Example:
        --------
        .. code-block:: python

            spy = Spy()
        """
        self.logger = LogManager().get_logger(self.__class__.__name__)
        self.parser: Parser = YamlParser()

    def importspy(self,
                  filepath: Optional[str] = None,
                  log_level: Optional[int] = None,
                  info_module: Optional[ModuleType] = None) -> ModuleType:
        """
        Imports and validates a Python module based on a SpyModel configuration.

        This method loads a serialized `SpyModel` definition from the specified 
        file path and validates the structure of the provided module. If no module 
        is explicitly provided via `info_module`, the calling module is introspected.

        Parameters:
        -----------
        filepath : Optional[str]
            Path to the configuration file containing the `SpyModel` definition.

        log_level : Optional[int]
            Logging level for the current operation. If not provided, the system default is used.

        info_module : Optional[ModuleType]
            The module object to be validated. If omitted, it is inferred from the call stack.

        Returns:
        --------
        ModuleType
            The dynamically validated module object.

        Raises:
        -------
        RuntimeError
            If `LogManager` was already configured and reconfiguration is attempted.

        ValueError
            If recursion is detected during module introspection.
        """
        self._configure_logging(log_level)
        spymodel: SpyModel = SpyModel(**self.parser.load(filepath=filepath))
        if not info_module:
            info_module = self._inspect_module()
        return self._validate_module(spymodel, info_module)

    def _configure_logging(self, log_level: Optional[int] = None):
        """
        Configures the logging system based on the given log level.

        Parameters:
        -----------
        log_level : Optional[int]
            Desired logging level. If not specified, uses the effective system log level.
        """
        log_manager = LogManager()
        if not log_manager.configured:
            system_log_level = logging.getLogger().getEffectiveLevel()
            log_manager.configure(level=log_level or system_log_level)

    def _validate_module(self, spymodel: SpyModel, info_module: ModuleType) -> ModuleType:
        """
        Validates the given module against a `SpyModel`.

        Parameters:
        -----------
        spymodel : SpyModel
            The reference model to validate the module against.

        info_module : ModuleType
            The reference to the object representing the module to be validated.

        Returns:
        --------
        ModuleType
            The validated module object.

        Raises:
        -------
        ValueError
            If the module does not match the SpyModel specification.
        """
        self.logger.debug(f"info_module: {info_module}")
        if spymodel:
            self.logger.debug(f"SpyModel detected: {spymodel}")
            spy_module = SpyModel.from_module(info_module)
            self.logger.debug(f"Spy module: {spy_module}")
            SpyModelValidator().validate(spymodel, spy_module)
        return ModuleUtil().load_module(info_module)

    def _inspect_module(self) -> ModuleType:
        """
        Inspects and retrieves metadata about the calling module.

        Uses stack frame inspection to determine which module initiated the importspy call.

        Returns:
        --------
        ModuleType
            The module being inspected.

        Raises:
        -------
        ValueError
            If recursion is detected (i.e., the current module is trying to inspect itself).
        """
        module_util = ModuleUtil()
        current_frame, caller_frame = module_util.inspect_module()
        if current_frame.filename == caller_frame.filename:
            raise ValueError("Recursion detected during module analysis.")

        info_module = module_util.get_info_module(caller_frame)
        self.logger.debug(f"Spy info_module: {info_module}")
        return info_module
