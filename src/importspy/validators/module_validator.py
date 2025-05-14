"""
importspy.validators.module_validator
=====================================

Validator for Python modules and their internal structures.

This module provides the `ModuleValidator` class, responsible for checking
that a Python module conforms to the expectations defined in an import contract.

It validates:
- Module filename and version
- Declared global variables
- Top-level functions
- Declared classes, including their attributes, methods, and superclasses

Delegates detailed checks to:
- `AttributeValidator`
- `FunctionValidator`
- `CommonValidator`
"""

from ..models import Module
from ..errors import Errors
from .variable_validator import VariableValidator
from .function_validator import FunctionValidator
from typing import List, Optional


class ModuleValidator:
    """
    Validator for full Python module metadata and structure.

    Attributes
    ----------
    _attribute_validator : AttributeValidator
        Responsible for validating class attributes.
    _function_validator : FunctionValidator
        Validates top-level and class methods.
    """

    def __init__(self):
        """
        Initialize the validator with attribute and function checkers.
        """
        self._variable_validator = VariableValidator()
        self._attribute_validator = AttributeValidator()
        self._function_validator = FunctionValidator()

    def validate(
        self,
        modules_1: List[Module],
        module_2: Optional[Module]
    ) -> Optional[None]:
        """
        Validate one or more expected modules against the actual loaded module.

        Parameters
        ----------
        modules_1 : List[Module]
            List of expected module definitions from the import contract.
        module_2 : Optional[Module]
            The actual module extracted from the system for validation.

        Returns
        -------
        None
            Returns None when:
            - No modules to validate (`modules_1` is empty).
            - Validation is successful.

        Raises
        ------
        ValueError
            Raised if:
            - `module_2` is missing.
            - Filename or version mismatches.
            - Variables differ in name or value.
            - Missing or invalid functions, classes, attributes, or superclasses.

        Example
        -------
        >>> validator = ModuleValidator()
        >>> validator.validate([expected_module], actual_module)
        """
        if not modules_1:
            return

        if not module_2:
            raise ValueError(Errors.ELEMENT_MISSING.format(modules_1))

        for module_1 in modules_1:
            # Check filename
            if module_1.filename and module_1.filename != module_2.filename:
                raise ValueError(Errors.FILENAME_MISMATCH.format(module_1.filename, module_2.filename))

            # Check version
            if module_1.version and module_1.version != module_2.version:
                raise ValueError(Errors.VERSION_MISMATCH.format(module_1.version, module_2.version))

            self._variable_validator.validate(
                module_1.variables,
                module_2.variables)

            # Validate top-level functions
            self._function_validator.validate(
                module_1.functions,
                module_2.functions
            )

            # Validate classes and class contents
            if module_1.classes:
                for class_1 in module_1.classes:
                    class_2 = next((cls for cls in module_2.classes if cls.name == class_1.name), None)
                    if not class_2:
                        raise ValueError(Errors.CLASS_MISSING.format(class_1.name))

                    # Class attribute check
                    self._attribute_validator.validate(
                        class_1.attributes,
                        class_2.attributes,
                        class_1.name
                    )

                    # Method (function) check
                    self._function_validator.validate(
                        class_1.methods,
                        class_2.methods,
                        classname=class_1.name
                    )

                    # Superclass check
                    CommonValidator().list_validate(
                        class_1.superclasses,
                        class_2.superclasses,
                        Errors.CLASS_SUPERCLASS_MISSING,
                        class_2.name
                    )

        return
