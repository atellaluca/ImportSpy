from types import ModuleType
from .errors import Errors
from .models import SpyModel
from .utilities.module_util import ModuleUtil
from .validators.spymodel_validator import SpyModelValidator
from typing import Optional
import logging

logger = logging.getLogger("/".join(__file__.split('/')[-2:]))
logger.addHandler(logging.NullHandler())

class Spy:
    """
    The `Spy` class serves as the core of ImportSpy, enabling developers to dynamically inspect and enforce 
    runtime compliance for external modules importing their package.

    By leveraging `SpyModel` validation, `Spy` ensures that importing modules adhere to defined structural 
    and behavioral expectations, promoting robust and predictable runtime interactions.

    Key Features:
    --------------
    - **Dynamic Module Inspection**: Identifies and retrieves metadata about the calling module.
    - **Validation via SpyModel**: Verifies compliance with user-defined models that specify expected structures 
      (functions, classes, attributes, etc.).
    - **Recursion Prevention**: Ensures safe execution by avoiding self-referential validation loops.
    - **Enhanced Multi-Architecture Support**: Integrates seamlessly into Python environments with diverse runtime 
      and architecture requirements.

    Methods:
    --------
    - `importspy(spymodel)`: Dynamically imports and validates the calling module against a `SpyModel`.
    - `_spy_module()`: Retrieves metadata about the module importing the current package.

    Notes:
    ------
    This class is tailored for Python developers building libraries that require strict validation of runtime 
    dependencies or operate in multi-architecture, multi-environment scenarios.

    Example Usage:
    --------------
    ```python
    from importspy import Spy, SpyModel

    spy = Spy()
    spy_model = SpyModel(filename="example.py", functions=["initialize"], classes=[])
    imported_module = spy.importspy(spymodel=spy_model)
    ```
    """

    def importspy(self, spymodel: Optional[SpyModel] = None) -> ModuleType:
        """
        Dynamically imports and validates the calling module against a `SpyModel`.

        This method is the primary interface for using ImportSpy. It identifies the external module that invoked 
        the current package, validates its structure against the rules defined in a `SpyModel`, and ensures that 
        all runtime expectations are met before importing the module.

        Parameters:
        -----------
        spymodel : SpyModel, optional
            The model that specifies the expected structure and properties of the importing module. If not provided, 
            the module is imported without validation.

        Returns:
        --------
        ModuleType
            The validated and imported module.

        Raises:
        -------
        ValueError
            If the module fails validation or recursion is detected during module inspection.

        Key Steps:
        ----------
        1. **Identify the Calling Module**:
            Uses `_spy_module` to locate the module invoking the current package.
        2. **Validation**:
            - Converts the calling module into a `SpyModel` representation.
            - Compares this representation with the provided `SpyModel` to check compliance.
        3. **Import**:
            If validation passes, dynamically imports and returns the module.

        Example:
        --------
        ```python
        from importspy import Spy, SpyModel
        from importspy.models import Class, Function, Argument

        # Initialize the Spy instance
        spy = Spy()

        # Define the validation model (SpyModel) for the external module
        spy_model = SpyModel(
            filename="example.py",  # Name of the file to validate
            variables={
                "MODULE_NAME": "string",  # Ensures the presence of a global variable
                "VERSION": "string"  # Checks the version variable
            },
            functions=[
                Function(
                    name="start_service",
                    arguments=[
                        Argument(name="config", annotation="dict")  # Expected argument for the function
                    ]
                ),
                Function(
                    name="stop_service",
                    arguments=[
                        Argument(name="signal", annotation="str")  # Expected argument for the function
                    ]
                )
            ],
            classes=[
                Class(
                    name="ServiceHandler",
                    methods=[
                        Function(
                            name="process_request",
                            arguments=[
                                Argument(name="request", annotation="dict"),  # Expected request argument
                                Argument(name="response", annotation="dict")  # Expected response argument
                            ]
                        ),
                        Function(
                            name="log_error",
                            arguments=[
                                Argument(name="error", annotation="str")  # Expected error argument
                            ]
                        )
                    ],
                    superclasses=["BaseService"]  # Ensures the class inherits from BaseService
                )
            ]
        )

        # Import and validate the specified module
        try:
            imported_module = spy.importspy(spymodel=spy_model)
            print(f"Module '{imported_module.__name__}' imported and validated successfully!")
        except ValueError as e:
            print(f"Module validation failed: {e}")
                ```
                Notes:
                ------
                - This method is designed for libraries with strict runtime requirements.
                - By enforcing runtime compliance, `importspy` ensures the stability and predictability of dependent modules.
                """
        info_module = self._spy_module()
        module_util = ModuleUtil()
        logger.debug(f"info_module: {info_module}")
        if spymodel:
            logger.debug(f"SpyModel detected: {spymodel}")
            spy_module = SpyModel.from_module(info_module)
            logger.debug(f"Spy module: {spy_module}")
            SpyModelValidator().validate(spymodel(), spy_module)
            return module_util.load_module(info_module)
        return module_util.load_module(info_module)

    def _spy_module(self) -> ModuleType | None:
        """
        Identifies and retrieves metadata about the external module importing the current package.

        This method inspects the execution context to locate the calling module, providing the foundation for 
        runtime validation and dynamic import functionality.

        Returns:
        --------
        ModuleType | None
            The metadata of the calling module, or `None` if recursion or other issues are detected.

        Raises:
        -------
        ValueError
            If recursion is detected, indicating that the package is analyzing itself.

        Use Case:
        ---------
        `_spy_module` is an internal utility used by `importspy` to enforce runtime compliance.

        Example:
        --------
        ```python
        spy = Spy()
        calling_module = spy._spy_module()
        ```

        Technical Details:
        ------------------
        - Relies on `ModuleUtil` for stack inspection and module extraction.
        - Checks for recursion by comparing the filenames of the current and calling frames.

        Notes:
        ------
        - This method ensures that dynamic imports do not lead to unintended behaviors or vulnerabilities.
        - Logging captures detailed metadata about the calling module for debugging purposes.
        """
        module_util = ModuleUtil()
        current_frame, caller_frame = module_util.inspect_module()
        if current_frame.filename == caller_frame.filename:
            raise ValueError(Errors.ANALYSIS_RECURSION_WARNING)
        info_module = module_util.get_info_module(caller_frame)
        logger.debug(f"Spy info_module: {info_module}")
        return info_module
