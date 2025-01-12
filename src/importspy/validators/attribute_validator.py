"""
Module: Attribute Validator

This module defines the `AttributeValidator` class, which is responsible for validating 
attributes in a class context. It ensures that attributes in one list match those in another 
list based on their names and values, raising appropriate errors when discrepancies are found.

Key Features:
-------------
- Validates the presence of attributes in two lists.
- Compares attribute values and raises errors for mismatches.
- Supports class-level attribute validation within the ImportSpy framework.

Example Usage:
--------------
```python
from importspy.validators.attribute_validator import AttributeValidator
from importspy.models import Attribute

validator = AttributeValidator()
validator.validate(attrs_1, attrs_2, classname="MyClass")
"""

from ..models import Attribute
from ..errors import Errors
from ..constants import Constants
from typing import List

class AttributeValidator:

    """
    Validates attributes for presence and value consistency within classes.

    The `AttributeValidator` class checks if a list of attributes (`attrs_1`) matches 
    another list of attributes (`attrs_2`). It ensures both the presence of required attributes 
    and the correctness of their values, providing detailed error messages when validation fails.

    Methods:
    --------
    - `validate`: Compares two lists of attributes and raises errors for missing attributes 
      or value mismatches.

    Example:
    --------
    ```python
    from importspy.validators.attribute_validator import AttributeValidator
    from importspy.models import Attribute

    validator = AttributeValidator()
    validator.validate(attrs_1, attrs_2, classname="MyClass")
    ```
    """

    def validate(self,
                 attrs_1: List[Attribute],
                 attrs_2: List[Attribute], classname:str):
        """
        Validates attributes for presence and value consistency.

        This method compares two lists of `Attribute` objects to ensure that all attributes 
        in `attrs_1` exist in `attrs_2` and have matching values. If discrepancies are found, 
        an appropriate error is raised with a detailed message.

        Parameters:
        -----------
        attrs_1 : List[Attribute]
            The list of attributes to validate.
        attrs_2 : List[Attribute]
            The list of attributes to check against.
        classname : str
            The name of the class being validated. Used for contextual error messages.

        Raises:
        -------
        ValueError
            - If an attribute in `attrs_1` is missing in `attrs_2`.
            - If an attribute's value in `attrs_1` does not match the corresponding value in `attrs_2`.

        Example:
        --------
        ```python
        from importspy.validators.attribute_validator import AttributeValidator
        from importspy.models import Attribute

        validator = AttributeValidator()
        validator.validate(attrs_1, attrs_2, classname="MyClass")
        ```
        """
        if not attrs_1:
            return
        for attr_1 in attrs_1:
            if attr_1 not in attrs_2:
                raise ValueError(Errors.CLASS_ATTRIBUTE_MISSING.format(attr_1.type, f"{attr_1.name}={attr_1.value}", classname))
        for attr_1 in attrs_1:
            attr_2 =  next((attr for attr in attrs_2 if attr.name == attr_1.name), None)
            if attr_1.value != attr_2.value:
                raise ValueError(Errors.CLASS_ATTRIBUTE_MISMATCH.format(Constants.VALUE, attr_1.type, attr_1.name, attr_1.value, attr_2.value))
                