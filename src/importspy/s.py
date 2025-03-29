from types import ModuleType
from .models import SpyModel
from .utilities.module_util import ModuleUtil
from .validators.spymodel_validator import SpyModelValidator
from .log_manager import LogManager
from typing import Optional
import logging

class Spy:
    """
    Provides functionality for dynamic introspection, validation, and management of Python modules.

    The `Spy` class integrates with `LogManager` for centralized logging and supports 
    the validation of module structures against a provided `SpyModel`. It enables the 
    dynamic loading and inspection of modules while ensuring compliance with predefined 
    structures.

    Attributes:
    -----------
    logger : logging.Logger
        Logger instance for the `Spy` class, managed by `LogManager`.

    Methods:
    --------
    - `__init__()`: Initializes the `Spy` instance and sets up the logger.
    - `importspy(spymodel, log_level)`: Imports and validates a module dynamically.
    - `_spy_module()`: Retrieves module metadata and detects recursion.

    Example:
    --------
    .. code-block:: python

        from importspy.spy import Spy

        spy = Spy()
        module = spy.importspy(log_level=logging.DEBUG)
    """

    def __init__(self):
        """
        Initializes the `Spy` instance.

        This method sets up the logger instance for the `Spy` class using `LogManager`. 

        Attributes:
        -----------
        logger : logging.Logger
            The logger instance for the class.

        Example:
        --------
        .. code-block:: python

            spy = Spy()
        """
        self.logger = LogManager().get_logger(self.__class__.__name__)

    def importspy(self,
                  filename: Optional[str] = None,
                  log_level: Optional[int] = None) -> ModuleType:
        pass


    def importspy(self, 
                  spymodel: Optional[SpyModel] = None, 
                  log_level: Optional[int] = None) -> ModuleType:
        """
        Dynamically imports and validates a Python module.

        If a `SpyModel` is provided, this method ensures that the loaded module 
        adheres to its predefined structure. It also configures logging if it 
        hasn't already been set.

        Parameters:
        -----------
        spymodel : Optional[SpyModel]
            An optional instance of `SpyModel` that defines the expected structure 
            of the module to be imported.

        log_level : Optional[int]
            The logging level to configure for the logger. If not provided, the 
            system's current logging level is used as the default.

        Returns:
        --------
        ModuleType
            The dynamically loaded module.

        Raises:
        -------
        RuntimeError
            If an attempt is made to reconfigure the `LogManager` after it has 
            already been configured.

        ValueError
            If recursion is detected during module analysis, raising a warning 
            to avoid infinite loops.

        Notes:
        ------
        - If logging is not configured explicitly, it sets up the logger using
          either the provided `log_level` or the system's default logging level.
        - This method leverages `ModuleUtil` to inspect and load the target module.

        Example:
        --------
        .. code-block:: python

            spy = Spy()
            module = spy.importspy(log_level=logging.DEBUG)
        """

        def _configure_logging():
            """Ensures `LogManager` is configured properly before module import."""
            log_manager = LogManager()
            if not log_manager.configured:
                system_log_level = logging.getLogger().getEffectiveLevel()
                log_manager.configure(level=log_level or system_log_level)

        def _load_and_validate_module() -> ModuleType:
            """
            Loads the module and validates it against the `SpyModel`, if provided.

            Returns:
            --------
            ModuleType
                The dynamically loaded module.

            Raises:
            -------
            ValueError
                If recursion is detected in the module being analyzed.
            """
            module_util = ModuleUtil()
            info_module = _inspect_module()
            self.logger.debug(f"info_module: {info_module}")

            if spymodel:
                self.logger.debug(f"SpyModel detected: {spymodel}")
                spy_module = SpyModel.from_module(info_module)
                self.logger.debug(f"Spy module: {spy_module}")
                SpyModelValidator().validate(spymodel(), spy_module)

            return module_util.load_module(info_module)

        def _inspect_module() -> ModuleType:
            """
            Inspects the caller module and retrieves metadata.

            Returns:
            --------
            ModuleType
                The caller's module metadata.

            Raises:
            -------
            ValueError
                If recursion is detected during module analysis.
            """
            module_util = ModuleUtil()
            current_frame, caller_frame = module_util.inspect_module()
            if current_frame.filename == caller_frame.filename:
                raise ValueError("Recursion detected during module analysis.")

            info_module = module_util.get_info_module(caller_frame)
            self.logger.debug(f"Spy info_module: {info_module}")
            return info_module

        # Main logic
        _configure_logging()
        return _load_and_validate_module()
