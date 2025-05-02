"""
importspy.validators.common_validator
=====================================

Reusable validation logic for dictionary and list structures.

This module defines the `CommonValidator` class, which provides utility methods to validate
data structures commonly used in contract inspection:
- General list containment validation
- Key/value consistency between dictionaries

It is used across structural validators like:
- SystemValidator
- ModuleValidator
- RuntimeValidator
"""
from typing import List, Dict
from ..errors import Errors
from ..constants import Constants
from ..log_manager import LogManager


class CommonValidator:
    """
    Common validation utilities for iterable structures.

    This helper class enables reusable checks across all ImportSpy validators.  
    It ensures list and dict structures match between expected (from `.yml`)  
    and actual (live modules) data.

    Validation Modes:
    -----------------
    - list_validate(...) : All elements in list1 must exist in list2.
    - dict_validate(...) : All key/value pairs in dict1 must match dict2.

    Attributes
    ----------
    logger : logging.Logger
        A scoped logger for structured output and debugging.
    """

    def __init__(self):
        """
        Initializes the CommonValidator and its logger.
        """
        self.logger = LogManager().get_logger(self.__class__.__name__)

    def list_validate(
        self,
        list1: List,
        list2: List,
        missing_error: str,
        *args
    ) -> None:
        """
        Validates that all elements in `list1` exist in `list2`.

        Parameters
        ----------
        list1 : List
            The expected list of items.
        list2 : List
            The actual list to be validated.
        missing_error : str
            Error message format if an element is missing (e.g., "Missing: {0}").
        *args : tuple
            Optional dynamic context passed to `missing_error.format(...)`.

        Raises
        ------
        ValueError
            If any element from `list1` is not present in `list2`.

        Returns
        -------
        None

        Example
        -------
        >>> CommonValidator().list_validate(["A", "B"], ["A"], "Missing item: {0}")
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