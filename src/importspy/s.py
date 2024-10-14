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
    Spy is a class responsible for dynamic module importation and validation, allowing you to ensure that
    imported modules follow expected rules or structures defined by `SpyModel` or custom validation logic.

    This class provides a flexible way to dynamically load Python modules at runtime, with optional validation
    steps that can improve security and enforce standards across your project.

    ## Key Methods:
    
    - **importspy**: Dynamically imports a module and validates it using `SpyModel` or a custom validation function.
    - **_spy_module**: Retrieves information about the calling module, with safeguards against recursion.

    .. warning::
        Use this class with caution when dynamically importing code, especially from untrusted sources. Always
        ensure that imported modules are secure to prevent the execution of malicious code.
    """

    def importspy(self, spymodel: SpyModel | None = None, validation: Callable[[ModuleType], bool] | None = None) -> ModuleType:
        """
        Dynamically imports the module that called this function and validates it against an optional `SpyModel` or
        custom validation logic.

        This method allows you to import a module at runtime and check if it follows predefined rules. The rules
        can be specified using a `SpyModel` or, for backward compatibility, a validation function.

        ### Parameters:

        - **spymodel** (`SpyModel | None`, optional): Defines the rules that the imported module should follow. 
          If provided, the module is loaded only if it matches the `SpyModel`.
        - **validation** (`Callable[[ModuleType], bool] | None`, optional): A custom validation function that takes
          the imported module and returns `True` if it passes validation. This parameter is deprecated and will be
          removed in future versions.

        ### Returns:
        - **ModuleType**: The imported module if it passes the validation. Returns `None` if validation fails or no
          validation is applied.

        ### Warning:
        The `validation` parameter is deprecated as of version 0.1.6 due to a security concern. In future versions, 
        only `SpyModel` will be supported for validation.

        ### Example:

        ```python
        spy = Spy()
        module = spy.importspy(spymodel=my_spy_model)
        ```
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
        Retrieves information about the calling module that invoked this method.

        This method inspects the calling context to identify the module from which the `importspy` method
        was invoked. It also prevents recursion by ensuring that the current module is not the same as the 
        calling module, which would lead to unintended behavior.

        ### Returns:
        - **ModuleType | None**: The module object representing the caller, or `None` if an error occurs.

        ### Raises:
        - **ValueError**: Raised if recursion is detected, meaning the current module and the calling module
          are the same.
        """
        current_frame, caller_frame = spy_module_utils.inspect_module()
        if current_frame.filename == caller_frame.filename:
            raise ValueError(Errors.ANALYSIS_RECURSION_WARNING)
        info_module = spy_module_utils.get_info_module(caller_frame)
        logger.debug(f"Spy info_module: {info_module}")
        return info_module