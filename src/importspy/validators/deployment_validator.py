"""
Module: Deployment Validator

This module provides the `DeploymentValidator` class, which ensures the structural and runtime 
compliance of `Deployment` objects. It validates that a list of deployments matches the expected 
runtime specifications of a given deployment.

The validation process includes:
- Iterative validation of runtime environments in deployments.
- Ensuring consistency in runtime configurations across deployments.

Key Features:
-------------
- Runtime validation for deployment structures.
- Seamless integration with the `RuntimeValidator` for nested validation.

Example Usage:
--------------
```python
from importspy.models import Deployment
from importspy.validators.deployment_validator import DeploymentValidator

deployment_1 = Deployment(runtimes=[...])  # Define your runtime
deployment_2 = Deployment(runtimes=[...])  # Define another runtime
DeploymentValidator().validate([deployment_1], deployment_2)
```

This ensures that deployment_2 is consistent with the list of deployment_1 objects.


"""
from ..models import Deployment
from .runtime_validator import RuntimeValidator
from typing import List

class DeploymentValidator:

    """
    Validates the compliance of `Deployment` objects against expected specifications.

    The `DeploymentValidator` ensures that all runtimes within a list of deployments are consistent 
    with the specified deployment. This includes validating nested runtime configurations and their 
    adherence to defined standards.

    Use Cases:
    ----------
    - Validating multiple deployment configurations for consistency.
    - Ensuring runtime compatibility within a deployment structure.

    Methods:
    --------
    - `validate`: Validates a list of `Deployment` objects against a single `Deployment`.

    Example:
    --------
    ```python
    from importspy.models import Deployment
    from importspy.validators.deployment_validator import DeploymentValidator

    deployment_1 = Deployment(runtimes=[...])  # Define your runtime
    deployment_2 = Deployment(runtimes=[...])  # Define another runtime
    DeploymentValidator().validate([deployment_1], deployment_2)
    ```
    This ensures that `deployment_2` conforms to the runtime expectations of the `deployment_1` list.
    """

    def validate(self,
                 deployments_1:List[Deployment],
                 deployment_2:Deployment):
        """
        Validates a list of `Deployment` objects against a single `Deployment`.

        This method ensures that all runtimes within the `deployments_1` list are consistent 
        with the specified `deployment_2`. It uses the `RuntimeValidator` to validate individual 
        runtime configurations.

        Parameters:
        -----------
        deployments_1 : List[Deployment]
            A list of `Deployment` objects to validate.
        deployment_2 : Deployment
            The target `Deployment` object to validate against.

        Raises:
        -------
        ValueError
            If any runtime in `deployments_1` does not match the specifications of `deployment_2`.

        Example:
        --------
        ```python
        from importspy.models import Deployment
        from importspy.validators.deployment_validator import DeploymentValidator

        deployment_1 = Deployment(runtimes=[...])  # Define your runtime
        deployment_2 = Deployment(runtimes=[...])  # Define another runtime
        DeploymentValidator().validate([deployment_1], deployment_2)
        ```
        In this example, the `DeploymentValidator` ensures that `deployment_2` matches the 
        runtime configurations of the `deployment_1` list.
        """
        rv = RuntimeValidator()
        for deployment_1 in deployments_1:
            rv.validate(deployment_1.runtimes, deployment_2.runtimes[0])