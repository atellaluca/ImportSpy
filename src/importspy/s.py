import warnings
from typing import Callable
from types import ModuleType
from .errors import Errors
from .models import SpyModel
from .utils import module_utils


class Spy:

    def importspy(self, 
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
        warnings.warn(
            "The `importspy` method with validation is deprecated as of version 0.1.6 due to a security vulnerability. "
            "It will be removed in future versions.",
            DeprecationWarning
        )
        info_module = self._spy_module()
        module = module_utils.load_module(info_module)
        return module if not validation else module if validation(module) else None
    
    def _spy_module(self) -> ModuleType | None:
        caller_frame, current_frame = module_utils.inspect_module()
        if current_frame.filename == caller_frame.filename:
            raise ValueError(Errors.ANALYSIS_RECURSION_WARNING)
        info_module = module_utils.get_info_module(caller_frame)
        return info_module
