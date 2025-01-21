from typing import List, Dict
from ..errors import Errors
from ..constants import Constants
from ..log_manager import LogManager

class CommonValidator:
    """
    Provides common validation utilities for lists and dictionaries.

    This class contains reusable methods to validate:
    - Lists: Ensures that all elements in one list are present in another list.
    - Dictionaries: Validates that keys and values in one dictionary match those in another.

    Validation Outcomes:
    ---------------------
    1. **Valid:**
       - All elements in the expected list or dictionary match the actual list or dictionary.

    2. **No Validation Necessary:**
       - The expected list or dictionary is empty or undefined.

    3. **Invalid:**
       - Missing elements in the actual list or dictionary.
       - Mismatches between expected and actual values in dictionaries.

    Error Handling:
    ----------------
    - Raises `ValueError` with specific error messages in the following cases:
      - Missing elements in lists or dictionaries.
      - Value mismatches for specific keys in dictionaries.

    Attributes:
    -----------
    logger : LogManager
        A logging instance to provide detailed output for each validation step.
    """

    def __init__(self):
        """
        Initializes the CommonValidator with a logging instance.

        The logger provides detailed output for debugging purposes.
        """
        self.logger = LogManager().get_logger(self.__class__.__name__)

    def list_validate(self,
                      list1: List,
                      list2: List,
                      missing_error: str,
                      *args) -> None:
        """
        Validates that all elements in `list1` are present in `list2`.

        Parameters:
        -----------
        list1 : List
            The expected list of elements.
        list2 : List
            The actual list of elements to validate against.
        missing_error : str
            The error message to raise if an element in `list1` is not found in `list2`.
            It should include placeholders for dynamic values (e.g., `{0}`).
        *args : tuple
            Additional arguments to format the `missing_error` message.

        Returns:
        --------
        None
            No return value, but raises exceptions if validation fails.

        Raises:
        -------
        ValueError
            If any element in `list1` is missing from `list2`.

        Validation Logic:
        -----------------
        1. Skips validation if `list1` is empty or `None`.
        2. Skips validation if both lists are empty or `list2` is `None`.
        3. Raises a `ValueError` if an element in `list1` is not found in `list2`.

        Example Usage:
        --------------
        ```python
        validator = CommonValidator()
        expected = [1, 2, 3]
        actual = [1, 2]
        validator.list_validate(expected, actual, "Missing element: {0}")
        ```
        """
        self.logger.debug(
            Constants.LOG_MESSAGE_TEMPLATE.format(
                operation="List validating",
                status="Starting",
                details=f"Expected list: {list1} ; Current list: {list2}"
            )
        )

        if not list1:
            return
        if list1 and not list2:
            return
        if not list2:
            raise ValueError(Errors.ELEMENT_MISSING.format(list1))
        for expected_element in list1:
            if expected_element not in list2:
                raise ValueError(missing_error.format(expected_element, *args))

    def dict_validate(self,
                      dict1: Dict,
                      dict2: Dict,
                      missing_error: str,
                      mismatch_error: str) -> bool:
        """
        Validates that all keys and values in `dict1` match those in `dict2`.

        Parameters:
        -----------
        dict1 : Dict
            The expected dictionary.
        dict2 : Dict
            The actual dictionary to validate against.
        missing_error : str
            The error message to raise if a key in `dict1` is not found in `dict2`.
            It should include placeholders for dynamic values (e.g., `{0}`).
        mismatch_error : str
            The error message to raise if a value for a matching key in `dict1` 
            does not match the value in `dict2`. It should include placeholders 
            for dynamic values (e.g., `{0}`, `{1}`, `{2}`).

        Returns:
        --------
        bool
            - `True` if all validations pass.
            - Raises exceptions if validation fails.

        Raises:
        -------
        ValueError
            If any key is missing from `dict2`, or if values do not match.

        Validation Logic:
        -----------------
        1. Skips validation if `dict1` is empty or `None`.
        2. Raises a `ValueError` if `dict2` is missing or `None`.
        3. Iterates through keys in `dict1`:
           - Ensures the key exists in `dict2`.
           - Checks that the value for the key matches in both dictionaries.
           - Raises appropriate errors for missing keys or mismatched values.

        Example Usage:
        --------------
        ```python
        validator = CommonValidator()
        expected = {"key1": "value1", "key2": "value2"}
        actual = {"key1": "value1", "key2": "different_value"}
        validator.dict_validate(
            expected, 
            actual, 
            "Missing key: {0}", 
            "Value mismatch for {0}: expected {1}, found {2}"
        )
        ```
        """
        self.logger.debug(
            Constants.LOG_MESSAGE_TEMPLATE.format(
                operation="Dict validating",
                status="Starting",
                details=f"Expected dict: {dict1} ; Current dict: {dict2}"
            )
        )

        if not dict1:
            return True
        if not dict2:
            raise ValueError(missing_error.format(dict1))
        for expected_key, expected_value in dict1.items():
            if expected_key in dict2:
                if expected_value != dict2[expected_key]:
                    raise ValueError(mismatch_error.format(expected_key, expected_value, dict2[expected_key]))
            else:
                raise ValueError(missing_error.format(expected_key))
        return True
