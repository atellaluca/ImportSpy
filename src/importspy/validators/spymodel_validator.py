"""
SpyModel Validation Utilities for ImportSpy

This module provides the `SpyModelValidator` class, which is responsible for ensuring 
that a `SpyModel` instance conforms to the expected structure and runtime requirements. 
Validation includes comparing deployments, modules, and their associated configurations.

Key Responsibilities:
- Validate `SpyModel` deployments using the `DeploymentValidator`.
- Validate modules within the runtime system using the `ModuleValidator`.
- Ensure compliance with predefined expectations at various levels of the `SpyModel`.
"""

from ..models import (
    SpyModel,
    Deployment
)
from .deployment_validator import DeploymentValidator
from .module_validator import ModuleValidator

class SpyModelValidator:

    """
    Validator for SpyModel Structures

    The `SpyModelValidator` class validates `SpyModel` instances, ensuring that their 
    structure, deployments, and associated modules comply with expected configurations. 
    It serves as a high-level orchestrator, delegating specific validation tasks to 
    `DeploymentValidator` and `ModuleValidator`.

    Key Features:
    --------------
    - Validates deployments within a `SpyModel`.
    - Ensures module compliance within the runtime system.
    - Supports multi-layered validation for complex runtime configurations.

    Methods:
    --------
    - `validate(spy_model_1, spy_model_2)`: Compares two `SpyModel` instances to ensure 
      structural and functional compliance.

    Example Usage:
    --------------
    ```python
    from importspy.models import SpyModel
    from importspy.validators.spymodel_validator import SpyModelValidator

    spy_model_1 = SpyModel(deployments=[...])  # Expected SpyModel
    spy_model_2 = SpyModel(deployments=[...])  # Actual SpyModel

    validator = SpyModelValidator()
    try:
        validator.validate(spy_model_1, spy_model_2)
        print("SpyModel validation passed.")
    except ValueError as e:
        print(f"SpyModel validation failed: {e}")
    ```
    This example demonstrates how the `SpyModelValidator` ensures that a runtime structure adheres 
    to the expected `SpyModel` configuration.
    """


    def validate(self,
                  spy_model_1: SpyModel,
                  spy_model_2: SpyModel) -> bool:
        """
        Validates the structure and runtime configuration of two `SpyModel` instances.

        This method ensures that the deployments and modules defined in `spy_model_1` 
        conform to the expectations set by `spy_model_2`. It leverages the 
        `DeploymentValidator` and `ModuleValidator` to perform multi-level validation.

        Parameters:
        -----------
        spy_model_1 : SpyModel
            The expected `SpyModel` instance, defining the validation criteria.
        spy_model_2 : SpyModel
            The actual `SpyModel` instance to validate against the criteria.

        Returns:
        --------
        bool
            Returns `True` if validation is successful.

        Raises:
        -------
        ValueError
            If validation fails at any level (e.g., deployment or module validation).

        Key Steps:
        ----------
        1. Validate Deployments:
            - Compares the deployments in `spy_model_1` with those in `spy_model_2` 
              using the `DeploymentValidator`.
        2. Validate Modules:
            - Ensures the compliance of modules within the runtime system of 
              `spy_model_2` using the `ModuleValidator`.

        Example:
        --------
        ```python
        spy_model_1 = SpyModel(deployments=[...])
        spy_model_2 = SpyModel(deployments=[...])

        validator = SpyModelValidator()
        try:
            validator.validate(spy_model_1, spy_model_2)
            print("Validation passed.")
        except ValueError as e:
            print(f"Validation failed: {e}")
        ```
        """
        deployment_2:Deployment = spy_model_2.deployments[0]
        DeploymentValidator().validate(spy_model_1.deployments, deployment_2)
        ModuleValidator().validate([spy_model_1], 
                                   spy_model_2
                                   .deployments[0]
                                   .runtimes[0]
                                   .systems[0]
                                   .pythons[0]
                                   .modules[0])