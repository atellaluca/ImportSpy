"""
Module: Common Validator

This module defines the `CommonValidator` class, which provides utility methods for 
validating lists and dictionaries. It facilitates checks for missing or mismatched elements 
in data structures, ensuring consistency during validation processes.

.. note::
   This module is marked for future refactoring. The functionality provided by the `CommonValidator` 
   will be integrated into more specialized validators to enhance modularity and maintainability.

Key Features:
-------------
- Validation of missing elements in lists and dictionaries.
- Detection of mismatches in dictionary key-value pairs.

Example Usage:
--------------
```python
from importspy.validators.common_validator import CommonValidator

cv = CommonValidator()
cv.list_validate([1, 2, 3], [1, 2], "Element {0} is missing.")
cv.dict_validate({"key": "value"}, {"key": "wrong_value"}, "Key {0} is missing.", "Mismatch: {0}")
"""

class CommonValidator:

    """
    Provides utility methods for list and dictionary validation.

    The `CommonValidator` class is designed to perform generic validation tasks, such as checking for 
    missing elements in lists or mismatched key-value pairs in dictionaries. It is commonly used across 
    the ImportSpy framework to support higher-level validation processes.

    .. warning::
       This class is scheduled for refactoring. Its functionality will be replaced by more modular 
       and specialized validation utilities in upcoming versions.

    Methods:
    --------
    - `list_validate`: Validates the presence of elements in a list.
    - `dict_validate`: Validates the presence and correctness of key-value pairs in dictionaries.

    Example:
    --------
    ```python
    from importspy.validators.common_validator import CommonValidator

    cv = CommonValidator()
    cv.list_validate([1, 2, 3], [1, 2], "Element {0} is missing.")
    cv.dict_validate({"key": "value"}, {"key": "wrong_value"}, "Key {0} is missing.", "Mismatch: {0}")
    ```
    """

    def list_validate(self,
                      list1:list, 
                      list2:list, 
                      missing_error:str, 
                      *args):
        """
        Validates that all elements in `list1` are present in `list2`.

        This method iterates over `list1` and checks if each element is present in `list2`. 
        If any element is missing, it raises a `ValueError` with a customizable error message.

        Parameters:
        -----------
        list1 : list
            The list containing elements to validate.
        list2 : list
            The list to check against for missing elements.
        missing_error : str
            The error message template for missing elements. Use `{0}` as a placeholder for 
            the missing element.
        *args : tuple
            Additional arguments to format the error message.

        Raises:
        -------
        ValueError
            If an element in `list1` is not found in `list2`.

        Example:
        --------
        ```python
        cv = CommonValidator()
        cv.list_validate([1, 2, 3], [1, 2], "Element {0} is missing.")
        ```
        """
        if not list1:
            return
        for expected_element in list1:
            if expected_element not in list2:
                raise ValueError(missing_error.format(expected_element, *args))
    
    def dict_validate(self,
                      dict1:dict, 
                      dict2:dict,
                      missing_error:str,
                      mismatch_error:str):
        """
        Validates that all keys in `dict1` are present in `dict2` and that their values match.

        This method iterates over `dict1` and ensures that each key exists in `dict2` and 
        has the same value. If a key is missing or a value mismatches, it raises a `ValueError` 
        with a customizable error message.

        Parameters:
        -----------
        dict1 : dict
            The dictionary containing keys and values to validate.
        dict2 : dict
            The dictionary to check against for missing keys or mismatched values.
        missing_error : str
            The error message template for missing keys. Use `{0}` as a placeholder for the key.
        mismatch_error : str
            The error message template for mismatched values. Use `{0}` for the key, `{1}` for 
            the expected value, and `{2}` for the actual value.

        Raises:
        -------
        ValueError
            If a key in `dict1` is missing in `dict2` or its value does not match.

        Example:
        --------
        ```python
        cv = CommonValidator()
        cv.dict_validate(
            {"key": "value"},
            {"key": "wrong_value"},
            "Key {0} is missing.",
            "Mismatch for key {0}: expected {1}, found {2}."
        )
        ```
        """
        if not dict1:
            return
        if not dict2:
            return False
        for expected_key, expected_value in dict1.items():
            if expected_key in dict2:
                if expected_value != dict2[expected_key]:
                    raise ValueError(mismatch_error.format(expected_key, expected_value, dict2[expected_key]))
            else:
                raise ValueError(missing_error.format(expected_key))
        return True