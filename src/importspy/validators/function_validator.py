"""
Module: Function Validator

This module defines the `FunctionValidator` class, which provides functionality for validating 
the compliance of function definitions between two sets of `Function` objects. 

The validation includes:
- Verifying function names.
- Ensuring consistency in argument annotations.
- Validating return type annotations.

The module is essential for maintaining structural and functional integrity across modules or 
classes during runtime validation.

Key Features:
-------------
- Comprehensive validation of function properties.
- Context-aware error reporting, including function names and class context.

Example Usage:
--------------
```python
from importspy.models import Function, Argument
from importspy.validators.function_validator import FunctionValidator

func1 = Function(name="process_data", arguments=[], return_annotation="dict")
func2 = Function(name="process_data", arguments=[], return_annotation="dict")
FunctionValidator().validate([func1], [func2])
"""

from ..models import Function
from ..errors import Errors
from typing import List

class FunctionValidator:

    """
    Validates the compliance of functions between two sets of `Function` objects.

    The `FunctionValidator` is used to ensure that functions in one set match the expected 
    structure and properties of functions in another set. This includes validating the function 
    name, argument annotations, and return type annotations.

    Use Cases:
    ----------
    - Validating the compliance of external modules against predefined specifications.
    - Ensuring structural integrity during runtime validation of function signatures.
    - Detecting mismatches in function definitions, argument types, and return types.

    Methods:
    --------
    - `validate`: Validates two lists of `Function` objects for compliance.

    Example:
    --------
    ```python
    from importspy.models import Function, Argument
    from importspy.validators.function_validator import FunctionValidator

    func1 = Function(name="process_data", arguments=[], return_annotation="dict")
    func2 = Function(name="process_data", arguments=[], return_annotation="dict")
    FunctionValidator().validate([func1], [func2])
    ```
    This ensures that the function `process_data` in both lists is consistent in structure 
    and annotations.
    """

    def validate(self,
                 functions_1:List[Function],
                 functions_2:List[Function],
                 classname:str="",
                 *args):
        """
        Validates compliance between two lists of `Function` objects.

        This method ensures that functions in the first list match those in the second list 
        in terms of names, argument annotations, and return type annotations.

        Parameters:
        -----------
        functions_1 : List[Function]
            The first list of `Function` objects to validate.
        functions_2 : List[Function]
            The second list of `Function` objects to validate against.
        classname : str, optional
            The name of the class containing the functions, used for error context.
        *args : 
            Additional arguments for error message formatting.

        Raises:
        -------
        ValueError
            If a function is missing in `functions_2` or if there is a mismatch in return 
            type annotations between corresponding functions.

        Example:
        --------
        ```python
        from importspy.models import Function, Argument
        from importspy.validators.function_validator import FunctionValidator

        func1 = Function(name="process_data", arguments=[], return_annotation="dict")
        func2 = Function(name="process_data", arguments=[], return_annotation="dict")
        FunctionValidator().validate([func1], [func2])
        ```
        In this example, validation passes as the function names and return annotations match.
        """
        if not functions_1:
            return
        for function_1 in functions_1:
            if function_1 not in functions_2:
                raise ValueError(Errors.FUNCTIONS_MISSING.format(
                    "Method" 
                    if classname 
                    else "", 
                    function_1.name,
                    "Class:" 
                    if classname
                    else "", 
                    classname
                    )
                )
        for function_1 in functions_1:
            function_2 =  next((func for func in functions_2 if func.name == function_1.name), None)
            if function_1.return_annotation and \
                function_1.return_annotation != function_2.return_annotation:
                raise ValueError(Errors.ANNONATION_MISMATCH.format(*args, function_1.name))
            

