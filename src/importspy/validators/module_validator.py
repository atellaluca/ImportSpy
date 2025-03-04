from ..models import Module
from ..errors import Errors
from .attribute_validator import AttributeValidator
from .function_validator import FunctionValidator
from .common_validator import CommonValidator
from typing import List, Optional

class ModuleValidator:
    """
    Validates Python modules for structural consistency.

    This class compares a list of expected modules (`modules_1`) with an actual module (`module_2`),
    ensuring alignment in filenames, versions, variables, functions, and class definitions.

    Validation Outcomes:
    ---------------------
    1. **Validation Not Necessary (Returns `None`)**:
       - `modules_1` is empty, indicating no modules to validate.

    2. **Validation Completed Successfully (Returns `None`)**:
       - All modules in `modules_1` align with the structure of `module_2`.

    3. **Validation Error (Raises `ValueError`)**:
       - Mismatched or missing filenames, versions, variables, functions, or classes.
       - `module_2` is not provided while `modules_1` is defined.
    """

    def __init__(self):
        """
        Initializes the ModuleValidator.

        Creates instances of `AttributeValidator` and `FunctionValidator` for
        validating attributes and functions respectively.
        """
        self._attribute_validator = AttributeValidator()
        self._function_validator = FunctionValidator()

    def validate(self, 
                 modules_1: List[Module], 
                 module_2: Optional[Module]) -> Optional[None]:
        """
        Validates a list of modules against a single module.

        Parameters:
        -----------
        modules_1 : List[Module]
            The list of expected modules to validate.
        module_2 : Module, optional
            The actual module to validate against.

        Returns:
        --------
        None
            - If `modules_1` is empty (validation not necessary).
            - If validation completes successfully.

        Raises:
        -------
        ValueError
            - If `module_2` is missing but `modules_1` is defined.
            - If discrepancies are found in filenames, versions, variables, functions, or classes.
        """
        # Case 1: Validation not necessary
        if not modules_1:
            return

        # Case 2: Error - `module_2` is missing
        if not module_2:
            raise ValueError(Errors.ELEMENT_MISSING.format(modules_1))

        # Validate each module in the list
        for module_1 in modules_1:
            # Validate module filename
            if module_1.filename and module_1.filename != module_2.filename:
                raise ValueError(Errors.FILENAME_MISMATCH.format(module_1.filename, module_2.filename))

            # Validate module version
            if module_1.version and module_1.version != module_2.version:
                raise ValueError(Errors.VERSION_MISMATCH.format(module_1.version, module_2.version))

            # Validate module variables
            common_validator = CommonValidator()
            common_validator.dict_validate(
                module_1.variables,
                module_2.variables,
                Errors.VAR_MISSING,
                Errors.VAR_MISMATCH
            )

            # Validate module functions
            self._function_validator.validate(module_1.functions, module_2.functions)

            # Validate classes within the module
            if module_1.classes:
                for class_1 in module_1.classes:
                    class_2 = next((cls for cls in module_2.classes if cls.name == class_1.name), None)
                    if not class_2:
                        raise ValueError(Errors.CLASS_MISSING.format(class_1.name))

                    # Validate class attributes
                    self._attribute_validator.validate(class_1.attributes, class_2.attributes, class_1.name)

                    # Validate class methods
                    self._function_validator.validate(class_1.methods, class_2.methods, classname=class_1.name)

                    # Validate superclasses
                    common_validator.list_validate(
                        class_1.superclasses,
                        class_2.superclasses,
                        Errors.CLASS_SUPERCLASS_MISSING,
                        class_2.name
                    )

        # Case 3: Validation completed successfully
        return
