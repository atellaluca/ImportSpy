"""
importspy.validators.spymodel_validator
========================================

Validator for top-level SpyModel objects.

This module defines the `SpyModelValidator` class, which orchestrates full-model validation,
including both runtime environments and declared modules. It is typically invoked as the
final step during the ImportSpy validation pipeline.
"""

from ..models import SpyModel
from .runtime_validator import RuntimeValidator
from .module_validator import ModuleValidator


class SpyModelValidator:
    """
    Validates the full structure of an ImportSpy model contract.

    The `SpyModelValidator` ensures that:
    - Declared runtime deployments (architecture + system + interpreter) match.
    - Declared module definitions (files, classes, functions) match.
    
    Delegates:
    ----------
    - Runtime inspection to `RuntimeValidator`
    - Module structure comparison to `ModuleValidator`

    Validation Scope:
    -----------------
    ✓ Architecture and OS validation  
    ✓ Interpreter and Python version match  
    ✓ Module filename, version, structure, functions, classes  

    This validator serves as the **entry point** for verifying SpyModel objects,
    typically loaded from YAML contracts and dynamically matched against live modules.

    Attributes
    ----------
    _runtime_validator : RuntimeValidator
        Validates runtime architecture and interpreter.
    _module_validator : ModuleValidator
        Validates classes, functions, and variables inside modules.
    """

    def __init__(self):
        """
        Initializes the SpyModelValidator with supporting sub-validators.
        """
        self._runtime_validator = RuntimeValidator()
        self._module_validator = ModuleValidator()

    def validate(
        self,
        spy_model_1: SpyModel,
        spy_model_2: SpyModel
    ) -> None:
        """
        Validates a declared SpyModel (from contract) against the active runtime SpyModel.

        Parameters
        ----------
        spy_model_1 : SpyModel
            The expected SpyModel structure (loaded from contract).
        spy_model_2 : SpyModel
            The actual SpyModel structure (derived from live inspection).

        Returns
        -------
        None
            If validation passes or `spy_model_1` has no runtime deployments to validate.

        Raises
        ------
        ValueError
            If architecture, interpreter, modules, or structural expectations are not met.

        Example
        -------
        >>> validator = SpyModelValidator()
        >>> validator.validate(spy_model_contract, spy_model_live)
        """
        # Validate runtime deployments
        self._runtime_validator.validate(spy_model_1.deployments, spy_model_2.deployments)

        # Navigate through the resolved runtime > system > python > module
        self._module_validator.validate(
            [spy_model_1],
            spy_model_2
                .deployments[0]
                .systems[0]
                .pythons[0]
                .modules[0]
        )
