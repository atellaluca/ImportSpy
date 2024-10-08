import warnings
from typing import Callable
from types import ModuleType
from .errors import Errors
from .models import SpyModel
from .utils import spy_model_utils, spy_module_utils
import logging

logger = logging.getLogger("/".join(__file__.split('/')[-2:]))
logger.addHandler(logging.NullHandler())

class Spy:
    """
    A class responsible for dynamic module importation and validation against specified models.

    The `Spy` class facilitates the import of modules at runtime, allowing for optional validation
    against `SpyModel` instances. It provides a mechanism to ensure that dynamically imported modules
    conform to expected structures or behaviors, enhancing security and reliability.
    
    Methods:

        importspy(spymodel: SpyModel | None = None, 
                  validation: Callable[[ModuleType], bool] | None = None) -> ModuleType:

            Dynamically imports a module and validates it against a provided `SpyModel` or 
            a custom validation function.

        _spy_module() -> ModuleType | None:
        
            Inspects the calling module and returns information about it, raising an error
            if recursion is detected.

    .. warning::

        This class is designed to facilitate dynamic imports and should be used with caution.
        Ensure that the modules being imported are trusted to avoid executing malicious code.
        
    """

    def importspy(self,
                   spymodel: SpyModel | None = None, 
                   validation: Callable[[ModuleType], bool] | 
                   None = None) -> ModuleType:
        """
        Dynamically imports the module that invoked this function, with an optional validation step.

        This method allows for the import of a module and its validation against a specified `SpyModel`.
        Note that the validation process is only applicable if the `validation` parameter is provided.

        .. warning::
            The `validation` parameter is deprecated as of version 0.1.6 due to a security vulnerability 
            where the module is imported before being validated, potentially allowing malicious code to execute 
            prior to validation.

        :param spymodel: 
            An optional instance of `SpyModel` used to validate the imported module. 
            If provided, the module will be loaded only if it is a subset of the `spymodel`.
        :type spymodel: SpyModel | None

        :param validation: 
            A callable that takes the imported module as an argument and returns a boolean indicating 
            whether the module passes validation. If `None`, no validation is performed. 
            This parameter is deprecated and will be removed in future versions.
        :type validation: Callable[[ModuleType], bool] | None

        :return: 
            The imported module if it passes validation, or `None` if validation fails or no 
            `spymodel` is provided.
        :rtype: ModuleType | None

        :deprecated: 
            The `validation` parameter is deprecated due to security concerns. 
            It will be removed in future versions. Use the `importspy` method with `SpyModel` instead.
        """
        info_module = self._spy_module()
        logger.debug(f"info_module: {info_module}")
        if spymodel:
            logger.debug(f"SpyModel detected: {spymodel}")
            spy_module = SpyModel.from_module(info_module)
            logger.debug(f"Spy module: {spy_module}")
            return spy_module_utils.load_module(info_module) if spy_model_utils.is_subset(spymodel(), spy_module) else None
        elif validation:
            warnings.warn(
                "The `importspy` method with validation is deprecated as of version 0.1.6 due to a security vulnerability. "
                "It will be removed in future versions. Please use the `importspy` method with SpyModel instead.",
                DeprecationWarning
            )
            module = spy_module_utils.load_module(info_module)
            return module if validation(module) else None
        return spy_module_utils.load_module(info_module)
        
        
    
    def _spy_module(self) -> ModuleType | None:
        """
        Inspects the calling module and retrieves information about it.

        This method analyzes the current execution context to identify the module that called
        the `importspy` method. It raises an error if recursion is detected, preventing 
        unintended behavior or infinite loops.

        :raises ValueError: 
            If recursion is detected, indicating that the current module and the caller module 
            are the same, which is not permitted.

        :return: 
            The module object that contains information about the caller module.
        :rtype: ModuleType | None
        """
        current_frame, caller_frame = spy_module_utils.inspect_module()
        if current_frame.filename == caller_frame.filename:
            raise ValueError(Errors.ANALYSIS_RECURSION_WARNING)
        info_module = spy_module_utils.get_info_module(caller_frame)
        logger.debug(f"Spy info_module: {info_module}")
        return info_module
