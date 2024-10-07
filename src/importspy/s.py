import warnings
from typing import Callable
from types import ModuleType
from .errors import Errors
from .models import SpyModel
from .utils import module_utils, model_utils
import logging

logger = logging.getLogger("/".join(__file__.split('/')[-2:]))
logger.addHandler(logging.NullHandler())

class Spy:

    def importspy(self,
                   spymodel: SpyModel | None = None, 
                   validation: Callable[[ModuleType], bool] | 
                   None = None) -> ModuleType:
        """
        [Deprecated since version 0.1.6] Dynamically imports the module that called this function,
        with an optional validation step.

        .. warning::
            This function is deprecated as of version 0.1.6 due to a security vulnerability where 
            the module is imported before being validated, which may allow malicious code to execute 
            prior to validation.

        :param validation: 
            A callable that takes the imported module as an argument and returns a boolean indicating 
            whether the module passes validation. If `None`, no validation is performed. This parameter 
            is deprecated due to security concerns.
        :type validation: Callable[[ModuleType], bool] | None

        :return: 
            The imported module, or `None` if the validation function is provided and fails.
        :rtype: ModuleType | None

        :deprecated: 
            Since 0.1.6, the method is vulnerable because the validation occurs after the module is loaded.
            It will be removed in future versions. Use the `importspy` method with `SpyModel` instead.
        """
        info_module = self._spy_module()
        logger.debug(f"info_module: {info_module}")
        if spymodel:
            logger.debug(f"SpyModel detected: {spymodel}")
            spy_module = SpyModel.from_module(info_module)
            logger.debug(f"Spy module: {spy_module}")
            return module_utils.load_module(info_module) if model_utils.is_subset(spymodel(), spy_module) else None
        elif validation:
            warnings.warn(
                "The `importspy` method with validation is deprecated as of version 0.1.6 due to a security vulnerability. "
                "It will be removed in future versions. Please use the `importspy` method with SpyModel instead.",
                DeprecationWarning
            )
            module = module_utils.load_module(info_module)
            return module if validation(module) else None
        return module_utils.load_module(info_module)
        
        
    
    def _spy_module(self) -> ModuleType | None:
        current_frame, caller_frame = module_utils.inspect_module()
        if current_frame.filename == caller_frame.filename:
            raise ValueError(Errors.ANALYSIS_RECURSION_WARNING)
        info_module = module_utils.get_info_module(caller_frame)
        logger.debug(f"Spy info_module: {info_module}")
        return info_module
