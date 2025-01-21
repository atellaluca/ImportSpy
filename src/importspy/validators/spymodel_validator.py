from ..models import (
    SpyModel,
    Runtime,
)
from .runtime_validator import RuntimeValidator
from .module_validator import ModuleValidator

class SpyModelValidator:
    """
    Validates the structure and configuration of SpyModel instances.

    This validator ensures that the provided `SpyModel` configurations (`spy_model_1`)
    align with the actual `SpyModel` instances (`spy_model_2`). It verifies deployments,
    runtime configurations, and modules to ensure consistency.

    Validation Outcomes:
    ---------------------
    1. **Validation Not Necessary (Returns `None`)**:
       - No deployments are defined in `spy_model_1`.

    2. **Validation Completed Successfully (Returns `None`)**:
       - All aspects of `spy_model_1` match those of `spy_model_2`.

    3. **Validation Error (Raises `ValueError`)**:
       - Discrepancies are found between `spy_model_1` and `spy_model_2`.
       - Missing configurations in `spy_model_2`.
    """

    def __init__(self):
        """
        Initializes the SpyModelValidator.

        Creates instances of `RuntimeValidator` and `ModuleValidator` to handle
        the validation of runtimes and modules within SpyModels.
        """
        self._runtime_validator = RuntimeValidator()
        self._module_validator = ModuleValidator()

    def validate(self,
                 spy_model_1: SpyModel,
                 spy_model_2: SpyModel) -> None:
        """
        Validates the structure of an expected `SpyModel` against an actual `SpyModel`.

        Parameters:
        -----------
        spy_model_1 : SpyModel
            The expected `SpyModel` configuration to validate.
        spy_model_2 : SpyModel
            The actual `SpyModel` instance to validate against.

        Returns:
        --------
        None
            - If validation is not necessary or completes successfully.

        Raises:
        -------
        ValueError
            - If any discrepancies or missing elements are detected in `spy_model_2`.
        """
        # Validate runtimes in the deployments
        self._runtime_validator.validate(spy_model_1.deployments, spy_model_2.deployments)

        # Validate modules in the first deployment's first system and Python configuration
        self._module_validator.validate(
            [spy_model_1],
            spy_model_2
                .deployments[0]
                .systems[0]
                .pythons[0]
                .modules[0]
        )
