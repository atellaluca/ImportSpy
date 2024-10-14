from typing import Callable
from types import ModuleType
from .errors import Errors
from .models import SpyModel
from .utils import spy_model_utils, spy_module_utils
import logging
import warnings

logger = logging.getLogger("/".join(__file__.split('/')[-2:]))
logger.addHandler(logging.NullHandler())

class Spy:
    """
    The `Spy` class is responsible for dynamic module importation and validation. It enables developers to ensure
    that imported modules adhere to predefined rules or structures as specified by a `SpyModel`, or alternatively,
    custom validation logic.

    This class allows for flexible, runtime import of Python modules with optional validation, enhancing security 
    and promoting adherence to standards across projects.

    .. warning::

        Use caution when dynamically importing code, particularly from untrusted sources, to avoid executing malicious code.
    """

    def importspy(self, spymodel: SpyModel | None = None, validation: Callable[[ModuleType], bool] | None = None) -> ModuleType:
        """
        Dynamically imports the module that called this function, with optional validation against a `SpyModel` 
        or a custom validation function.

        This method imports a module at runtime and verifies that it complies with predefined rules. The rules 
        can be specified using a `SpyModel` or (for backward compatibility) a custom validation function.

        Parameters:
        -----------
        spymodel : SpyModel, optional
            An instance of `SpyModel` that defines the rules the imported module should follow. If provided, 
            the module is only loaded if it adheres to the model.
        validation : Callable[[ModuleType], bool], optional
            A deprecated validation function that returns `True` if the module passes validation. 
            It will be removed in future versions.

        Returns:
        --------
        ModuleType
            The imported module if it passes the validation, or `None` if it does not comply or no validation 
            is applied.

        Raises:
        -------
        DeprecationWarning
            If the `validation` parameter is used, a warning is raised as this parameter will be removed in 
            future versions.

        .. warning::

            The `validation` parameter is deprecated as of version 0.1.6 due to security concerns. Use the 
            `SpyModel` for validation instead.

        Example:
        --------
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
                "The `validation` parameter is deprecated as of version 0.1.6 due to security vulnerabilities. "
                "It will be removed in future versions. Please use the `importspy` method with `SpyModel` instead.",
                DeprecationWarning
            )
            module = spy_module_utils.load_module(info_module)
            return module if validation(module) else None
        return spy_module_utils.load_module(info_module)

    def _spy_module(self) -> ModuleType | None:
        """
        Retrieves information about the calling module that invoked this method.

        This method inspects the current execution context to identify the module that called `importspy`. 
        It prevents recursion by ensuring the current module is not the same as the caller, avoiding unintended 
        behavior.

        Returns:
        --------
        ModuleType | None
            The module object of the caller, or `None` if recursion or another issue is detected.

        Raises:
        -------
        ValueError
            Raised if recursion is detected, meaning the current module is the same as the calling module.
        """
        current_frame, caller_frame = spy_module_utils.inspect_module()
        if current_frame.filename == caller_frame.filename:
            raise ValueError(Errors.ANALYSIS_RECURSION_WARNING)
        info_module = spy_module_utils.get_info_module(caller_frame)
        logger.debug(f"Spy info_module: {info_module}")
        return info_module
