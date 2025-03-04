from ..models import Function
from ..errors import Errors
from ..constants import Constants
from typing import List, Optional
from ..log_manager import LogManager
from .argument_validator import ArgumentValidator

class FunctionValidator:
    """
    Validates the structure and attributes of functions in a Python module or class.

    The `FunctionValidator` ensures that functions in one module/class (`functions_1`)
    match their counterparts in another module/class (`functions_2`). This includes:
    - Checking for missing functions.
    - Validating function arguments.
    - Ensuring that return annotations match.

    Validation Outcomes:
    ---------------------
    1. **Valid (Returns `True`)**:
       - All functions in `functions_1` exist in `functions_2`, with matching attributes.

    2. **No Validation Necessary (Returns `None`)**:
       - `functions_1` is empty or undefined.

    3. **Invalid (Raises `ValueError`)**:
       - Missing functions in `functions_2`.
       - Mismatched return annotations.
       - Argument discrepancies detected during validation.

    Error Handling:
    ----------------
    - Raises `ValueError` with specific error messages when:
      - A function in `functions_1` is not found in `functions_2`.
      - Return annotations do not match.
      - Function arguments fail validation.

    Attributes:
    -----------
    logger : LogManager
        A logging instance for detailed validation output.
    _argument_validator : ArgumentValidator
        A helper validator to validate function arguments.
    """

    def __init__(self):
        """
        Initializes the FunctionValidator.

        Creates a logger for detailed debugging and an instance of `ArgumentValidator`
        for argument-level validation.
        """
        self.logger = LogManager().get_logger(self.__class__.__name__)
        self._argument_validator = ArgumentValidator()

    def validate(self,
                 functions_1: List[Function],
                 functions_2: List[Function],
                 classname: Optional[str] = "") -> Optional[bool]:
        """
        Validates a list of functions against another list of functions.

        Parameters:
        -----------
        functions_1 : List[Function]
            The expected list of functions.
        functions_2 : List[Function]
            The actual list of functions to validate against.
        classname : Optional[str]
            The name of the class containing the functions (if applicable).
            Defaults to an empty string for top-level functions.

        Returns:
        --------
        Optional[bool]
            - `True` if validation is successful.
            - `None` if validation is unnecessary (e.g., `functions_1` is empty or None).

        Raises:
        -------
        ValueError
            - If a function in `functions_1` is missing in `functions_2`.
            - If return annotations do not match.
            - If function arguments fail validation.

        Example Usage:
        --------------
        ```python
        validator = FunctionValidator()
        expected_functions = [Function(name="foo", return_annotation="int")]
        actual_functions = [Function(name="foo", return_annotation="int")]
        validator.validate(expected_functions, actual_functions, classname="MyClass")
        ```
        """
        context_name = f"method in class {classname}" if classname else "function"

        self.logger.debug(
            Constants.LOG_MESSAGE_TEMPLATE.format(
                operation="Function validating",
                status="Starting",
                details=f"Expected functions: {functions_1} ; Current functions: {functions_2}"
            )
        )

        # Skip validation if no functions are expected
        if not functions_1:
            self.logger.debug(
                Constants.LOG_MESSAGE_TEMPLATE.format(
                    operation="Check if functions_1 is not none",
                    status="Finished",
                    details=f"There aren't any functions; current functions_1: {functions_1}"
                )
            )
            return None

        # Raise error if functions_2 is empty or None
        if not functions_2:
            self.logger.debug(
                Constants.LOG_MESSAGE_TEMPLATE.format(
                    operation="Checking functions_2 when functions_1 is missing",
                    status="Finished",
                    details=f"There aren't any functions_2; current functions_2: {functions_2}"
                )
            )
            raise ValueError(Errors.ELEMENT_MISSING.format(functions_1))

        # Validate each function in functions_1
        for function_1 in functions_1:
            self.logger.debug(
                Constants.LOG_MESSAGE_TEMPLATE.format(
                    operation="Function validating",
                    status="Progress",
                    details=f"Current function: {function_1}"
                )
            )
            # Check if function_1 exists in functions_2
            if function_1.name not in set(map(lambda function: function.name, functions_2)):
                self.logger.debug(Constants.LOG_MESSAGE_TEMPLATE.format(
                    operation="Checking if function_1 is in functions_2",
                    status="Finished for function missing",
                    details=f"function_1: {function_1}; functions_2: {functions_2}")
                )
                raise ValueError(Errors.FUNCTIONS_MISSING.format(context_name, function_1.name))

        # Validate function attributes and arguments
        for function_1 in functions_1:
            function_2 = next((func for func in functions_2 if func.name == function_1.name), None)
            if not function_2:
                raise ValueError(Errors.ELEMENT_MISSING.format(function_1))
            self._argument_validator.validate(function_1.arguments, function_2.arguments, function_1.name, classname)
            if function_1.return_annotation and \
                function_1.return_annotation != function_2.return_annotation:
                raise ValueError(Errors.FUNCTION_RETURN_ANNOTATION_MISMATCH.format(
                    context_name, function_1.name, function_1.return_annotation, function_2.return_annotation))

        self.logger.debug(
            Constants.LOG_MESSAGE_TEMPLATE.format(
                operation="Function validating",
                status="Completed",
                details="Validation successful."
            )
        )
        return True
