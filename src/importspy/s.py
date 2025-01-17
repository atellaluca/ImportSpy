"""
Module: spy

This module provides the `Spy` class, which enables dynamic introspection and validation of Python modules. 
It integrates with the `LogManager` for centralized logging, ensuring that logging levels are configurable 
and consistent. The module also leverages `SpyModel` for model-based validation and `SpyModelValidator` 
to ensure that modules adhere to predefined structures.

Classes:
--------
Spy:
    Provides functionality to dynamically inspect and validate Python modules. 
    Uses `LogManager` for logging and supports optional logging level configuration.

Dependencies:
-------------
- LogManager: Manages logging configuration and logger instances.
- SpyModel: Represents the structure of a module for validation purposes.
- SpyModelValidator: Validates the structure and contents of a `SpyModel`.
- ModuleUtil: Provides utility functions for module introspection and information retrieval.
- Errors: Contains error messages and constants used throughout the framework.
- logging: Python's built-in logging module for logging functionalities.

Usage:
------
Example usage of the Spy class:
```python
from importspy.spy import Spy

spy = Spy()
module = spy.importspy(log_level=logging.DEBUG)
```
"""

from types import ModuleType
from .errors import Errors
from .models import SpyModel
from .utilities.module_util import ModuleUtil
from .validators.spymodel_validator import SpyModelValidator
from .log_manager import LogManager
from typing import Optional
import logging

class Spy:

    """
    Spy Class

    Provides functionality for dynamic introspection, validation, and management of Python modules. 
    The `Spy` class integrates with `LogManager` for centralized logging and supports the validation 
    of module structures against a provided `SpyModel`. It enables the dynamic loading and inspection 
    of modules while ensuring compliance with predefined structures.

    Attributes:
    -----------
    logger : logging.Logger
        Logger instance for the `Spy` class, managed by `LogManager`.

    Methods:
    --------
    __init__():
        Initializes the `Spy` instance and sets up the logger.

    importspy(spymodel: Optional[SpyModel] = None, log_level: Optional[int] = None) -> ModuleType:
        Imports and validates a SpyModel if provided. Configures logging if not already configured.

        Parameters:
        - spymodel: SpyModel, optional
            A SpyModel instance representing the expected structure of the module.
        - log_level: int, optional
            The logging level to configure for the logger. Defaults to the system's logging level if not provided.

        Returns:
        - ModuleType: The dynamically loaded module.

        Raises:
        - RuntimeError: If `LogManager` is already configured and an attempt to reconfigure is made.
        - ValueError: If recursion is detected during module analysis.

    _spy_module() -> ModuleType | None:
        Inspects the caller module and retrieves its information. Detects recursion in module analysis.

        Returns:
        - ModuleType: The caller's module information.

        Raises:
        - ValueError: If recursion is detected during module analysis.

    Usage:
    ------
    Example usage of the `Spy` class:
    ```python
    from importspy.spy import Spy

    spy = Spy()
    module = spy.importspy(log_level=logging.DEBUG)
    ```
    """
    
    def __init__(self):
        self.logger = LogManager().get_logger(self.__class__.__name__)

    def importspy(self, 
                  spymodel: Optional[SpyModel] = None, 
                  log_level: Optional[int] = None) -> ModuleType:
        """
        Import and validate a Python module dynamically.

        Configures logging if it hasn't already been set and dynamically loads
        a Python module. If a `SpyModel` is provided, validates the loaded module
        against the expected structure defined in the `SpyModel`.

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
        """

        def _configure_logging():
            """Ensure LogManager is configured."""
            log_manager = LogManager()
            if not log_manager.configured:
                system_log_level = logging.getLogger().getEffectiveLevel()
                log_manager.configure(level=log_level or system_log_level)

        def _load_and_validate_module() -> ModuleType:
            """Load the module and validate it against the SpyModel, if provided."""
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
            """Inspect the module to retrieve its metadata."""
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

