from types import ModuleType
from .errors import Errors
from .models import SpyModel
from .utils.die_utils import (
    ModuleUtils
)
from .utils.validators import SpyModelValidator
import logging

logger = logging.getLogger("/".join(__file__.split('/')[-2:]))
logger.addHandler(logging.NullHandler())

class Spy:
    """
    The `Spy` class is the central component of ImportSpy, designed to allow package developers to proactively control 
    and validate the conditions under which their package is executed when imported by an external module.

    This class provides functionality for:
    - Dynamically importing the external module that invoked the package.
    - Validating the external module against predefined rules or structures defined in a `SpyModel`.
    - Enforcing compliance with execution conditions, ensuring that the importing module adheres to expected 
      behaviors and structures.

    Use Case:
    ----------
    `Spy` is particularly useful for developers creating libraries or packages that require specific runtime 
    conditions to function correctly. For example, a library can use `Spy` to verify that the importing module 
    defines necessary environment variables, classes, or functions.

    Key Features:
    --------------
    - Dynamic runtime validation of external modules using `SpyModel`.
    - Prevention of recursive validation to avoid unintended behavior.
    - Integration with ImportSpy utilities for metadata extraction and comparison.

    .. warning::

        Be cautious when dynamically importing modules to avoid security risks. Ensure that proper validation 
        is in place to prevent the execution of malicious code.

    Attributes:
        logger (logging.Logger): A logger instance for tracking operations and debugging.

    Methods:
        - `importspy`: Dynamically imports and validates the external module that invoked the package.
        - `_spy_module`: Retrieves metadata about the calling module, ensuring no recursion occurs.
    """

    def importspy(self, spymodel: SpyModel | None = None) -> ModuleType:
        """
        Dynamically imports the external module that invoked the current package and validates it against 
        a `SpyModel`, ensuring adherence to predefined execution conditions.

        This method is specifically designed to allow package developers to enforce runtime constraints on external 
        modules that import their package. By defining a `SpyModel`, developers can specify the required structure 
        of the importing module, such as the presence of specific environment variables, functions, or classes.

        How It Works:
        -------------
        1. Identifies the calling module using `_spy_module`.
        2. If a `SpyModel` is provided:
            - Extracts the actual structure of the calling module using `SpyModel.from_module`.
            - Compares the extracted structure with the expected structure defined in the `SpyModel`.
            - Only imports the module if it conforms to the validation rules.
        3. If no `SpyModel` is provided, imports the module directly without validation.

        Parameters:
        -----------
        spymodel : SpyModel, optional
            An instance of `SpyModel` that defines the rules for validation. If provided, the external module is 
            validated against these rules before being imported.

        Returns:
        --------
        ModuleType
            The imported external module if it passes validation, or `None` if it does not comply with the `SpyModel`.

        Raises:
        -------
        ValueError
            If recursion is detected or the importing module fails validation.

        Example:
        --------
        ```python
        from importspy import Spy, SpyModel

        spy = Spy()
        my_spy_model = SpyModel(
            filename="example.py",
            functions=["function1"],
            classes=[ClassModel(name="MyClass", methods=["method1"])]
        )
        module = spy.importspy(spymodel=my_spy_model)
        ```
        In this example, the `Spy` instance dynamically imports `example.py` and validates it against the `SpyModel`. 
        The module is only imported if it contains `function1` and a class `MyClass` with the method `method1`.

        Notes:
        ------
        - This method is a proactive programming tool for package developers, ensuring the correctness of runtime 
          conditions for external modules interacting with their package.
        - It relies on `spy_module_utils` for loading and inspecting modules.
        """
        info_module = self._spy_module()
        module_util = ModuleUtils()
        logger.debug(f"info_module: {info_module}")
        if spymodel:
            logger.debug(f"SpyModel detected: {spymodel}")
            spy_module = SpyModel.from_module(info_module)
            logger.debug(f"Spy module: {spy_module}")
            return module_util.load_module(info_module) if SpyModelValidator().is_subset(spymodel(), spy_module) else None
        return module_util.load_module(info_module)

    def _spy_module(self) -> ModuleType | None:
        """
        Identifies and retrieves metadata about the external module that invoked the current package.
    
        This utility method inspects the execution context to determine the calling module. It ensures that the 
        current package does not analyze itself recursively, preventing unintended behavior during validation.
    
        Use Case:
        ----------
        `_spy_module` is used internally by `importspy` to identify the external module that is importing the current 
        package. This allows `Spy` to validate the external module's structure and adherence to predefined rules.
    
        Returns:
        --------
        ModuleType | None
            The module object representing the external caller, or `None` if recursion or another issue is detected.
    
        Raises:
        -------
        ValueError
            If recursion is detected (the current package is the same as the calling module).
    
        Example:
        --------
        ```python
        spy = Spy()
        calling_module = spy._spy_module()
        ```
        This retrieves the metadata of the module that called the `Spy` instance, allowing further validation.
    
        Notes:
        ------
        - Uses `spy_module_utils` to inspect and extract information about the calling module.
        - Ensures safety during dynamic imports by detecting and preventing recursion.
        - Raises a `ValueError` with `Errors.ANALYSIS_RECURSION_WARNING` if recursion is detected.
    """
        module_util = ModuleUtils()
        current_frame, caller_frame = module_util.inspect_module()
        if current_frame.filename == caller_frame.filename:
            raise ValueError(Errors.ANALYSIS_RECURSION_WARNING)
        info_module = module_util.get_info_module(caller_frame)
        logger.debug(f"Spy info_module: {info_module}")
        return info_module
