"""
Module for Python Validation within ImportSpy.

This module provides functionality for validating Python environments, 
ensuring that runtime configurations, interpreters, and associated modules 
comply with predefined expectations. The `PythonValidator` class facilitates 
the comparison of Python instances across deployments, with support for 
module-level validations.

Classes:
--------
- PythonValidator: Validates Python runtime properties and modules.

Dependencies:
-------------
- `models.Python`: The model representing a Python runtime.
- `module_validator.ModuleValidator`: A validator for module-specific validations.
- `errors.Errors`: Centralized error handling.

"""

from ..models import Python
from typing import List
from .module_validator import ModuleValidator
from ..errors import Errors

class PythonValidator:

    """
    Validates Python runtime environments and associated modules.

    The `PythonValidator` class ensures that Python versions, interpreters, 
    and modules align with the expected configuration. It performs both 
    runtime-level and module-level validations, raising appropriate errors 
    if discrepancies are found.

    Methods:
    --------
    - validate(pythons_1: List[Python], python_2: Python): Validates a list 
      of Python instances against a reference configuration.
    - _check_pythons(pythons_1: List[Python], python_2: Python): Ensures 
      compatibility of Python versions and interpreters.

    Use Case:
    ---------
    This class is integral to the ImportSpy framework, supporting validation 
    across complex deployment scenarios with multiple Python environments.

    Example:
    --------
    ```python
    from importspy.validators.python_validator import PythonValidator
    from importspy.models import Python

    python_config = Python(version="3.9.1", interpreter="CPython")
    python_list = [Python(version="3.9.1", interpreter="CPython")]
    
    try:
        PythonValidator().validate(python_list, python_config)
        print("Validation successful.")
    except ValueError as e:
        print(f"Validation failed: {e}")
    ```
    """

    def validate(self,
                 pythons_1:List[Python],
                 python_2:Python):
        """
        Validates a list of Python configurations against a reference Python configuration.

        This method ensures that all Python instances in `pythons_1` match the 
        expected version and interpreter in `python_2`. If any of the instances 
        contains modules, their validation is delegated to `ModuleValidator`.

        Parameters:
        -----------
        pythons_1: List[Python]
            A list of Python configurations to validate.

        python_2: Python
            The reference Python configuration against which validation is performed.

        Raises:
        -------
        ValueError:
            Raised if any Python instance in `pythons_1` fails validation.

        """
        self._check_pythons(pythons_1, python_2)
        for python_1 in pythons_1:
            if python_1.modules:
                ModuleValidator().validate(python_1.modules, python_2.modules[0])
    
    def _check_pythons(self,
                       pythons_1:List[Python],
                       python_2:Python):
        """
        Ensures compatibility of Python versions and interpreters.

        This method checks that at least one Python instance in `pythons_1` matches 
        the version and interpreter specified in `python_2`. If no match is found, 
        a `ValueError` is raised.

        Parameters:
        -----------
        pythons_1: List[Python]
            A list of Python configurations to check.

        python_2: Python
            The reference Python configuration for comparison.

        Raises:
        -------
        ValueError:
            Raised if no compatible Python configuration is found in `pythons_1`.

        """
        for python_1 in pythons_1:
            if python_1.version == python_2.version \
                and python_1.interpreter == python_2.interpreter:
                return
        raise ValueError(Errors.PYTHON_MISSING.format(python_2))