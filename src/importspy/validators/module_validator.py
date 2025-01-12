"""
Module for Validating Modules and Their Components in ImportSpy.

This module contains the `ModuleValidator` class, which is responsible for 
validating the structural and behavioral integrity of modules in Python. By 
checking filenames, versions, variables, functions, classes, and their associated 
attributes and methods, the validator ensures that modules conform to expected 
specifications.

Classes:
--------
- ModuleValidator: Performs comprehensive validations on modules, ensuring compliance 
  with predefined expectations.

Dependencies:
-------------
- `models.Module`: Represents the structure and metadata of a Python module.
- `attribute_validator.AttributeValidator`: Validates class attributes within modules.
- `function_validator.FunctionValidator`: Validates functions and methods within modules.
- `common_validator.CommonValidator`: Handles generic validation tasks, such as dictionary 
  and list comparisons.
- `errors.Errors`: Provides centralized error messages.

"""

from ..models import Module
from typing import List
from ..errors import Errors
from .attribute_validator import AttributeValidator
from .function_validator import FunctionValidator
from .common_validator import CommonValidator

class ModuleValidator:

    """
    Validates Python modules and their components.

    The `ModuleValidator` class ensures that Python modules meet specific requirements, 
    including file properties, versions, variables, functions, and classes. It leverages 
    specialized validators for attributes and functions, while delegating general list 
    and dictionary validation to the `CommonValidator`.

    Methods:
    --------
    - validate(modules_1: List[Module], module_2: Module): Validates a list of modules 
      against a reference module, checking for compatibility across all key components.

    Use Case:
    ---------
    This class is integral to the ImportSpy framework, supporting module-level validation 
    in complex runtime environments and deployments.

    Example:
    --------
    ```python
    from importspy.validators.module_validator import ModuleValidator
    from importspy.models import Module

    reference_module = Module(filename="main.py", version="1.0.0")
    modules_to_validate = [Module(filename="main.py", version="1.0.0")]

    try:
        ModuleValidator().validate(modules_to_validate, reference_module)
        print("Modules validated successfully.")
    except ValueError as e:
        print(f"Module validation failed: {e}")
    ```
    """

    def validate(self, 
                 modules_1:List[Module], 
                 module_2:Module):
        """
        Validates a list of modules against a reference module.

        This method ensures that the provided modules in `modules_1` align with the 
        properties and structure of the `module_2` reference module. Validation includes 
        checks on filenames, versions, variables, functions, and classes, with errors 
        raised for any discrepancies.

        Parameters:
        -----------
        modules_1: List[Module]
            A list of modules to validate.

        module_2: Module
            The reference module against which validation is performed.

        Raises:
        -------
        ValueError:
            Raised if any module in `modules_1` fails to match the reference module's 
            properties or structure.

        """
        for module_1 in modules_1:
            if module_1.filename and module_1.filename != module_2.filename:
                raise ValueError(Errors.FILENAME_MISMATCH.format(module_1.filename, module_2.filename))
            if module_1.version and module_1.version != module_2.version:
                raise ValueError(Errors.VERSION_MISMATCH.format(module_1.version, module_2.version))
            common_validator = CommonValidator()
            #Variables validation
            common_validator.dict_validate(module_1.variables, module_2.variables, Errors.VAR_MISSING, Errors.VAR_MISMATCH)
            #Functions validation
            common_validator.list_validate(module_1.functions, module_2.functions, Errors.FUNCTIONS_MISSING)
            for class_1 in module_1.classes:
                class_2 = next((cls for cls in module_2.classes if cls.name == class_1.name), None)
                if not class_2:
                    raise ValueError(Errors.CLASS_MISSING.format(class_1.name))
                # Class attributes validation
                AttributeValidator().validate(class_1.attributes, class_2.attributes, class_1.name)
                # Class methods validation
                FunctionValidator().validate(class_1.methods, class_2.methods, classname=class_1.name)

                # Superclasses validation
                common_validator.list_validate(class_1.superclasses, class_2.superclasses, Errors.CLASS_SUPERCLASS_MISSING, class_2.name)