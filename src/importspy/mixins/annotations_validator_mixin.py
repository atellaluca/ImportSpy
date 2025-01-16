"""
Module: Annotation Validation Mixin

This module provides a mixin class `AnnotationValidatorMixin` for validating type annotations 
used within the ImportSpy framework. It ensures that annotations conform to a predefined 
set of supported types, enhancing compatibility and validation consistency.
"""

from ..constants import Constants
from ..errors import Errors
from typing import Union

class AnnotationValidatorMixin:

    """
    A mixin for validating type annotations in ImportSpy models.

    The `AnnotationValidatorMixin` class provides a static method for validating type annotations 
    against a list of supported annotations defined in the `Constants` module. This mixin ensures 
    that annotations used in models and validation processes conform to expected standards.

    Key Features:
    --------------
    - Validates annotations to prevent unsupported or incorrect types.
    - Raises informative errors when an annotation is invalid.

    Example Usage:
    --------------
    ```python
    from importspy.mixins.annotations_validator_mixin import AnnotationValidatorMixin

    class SomeModel(AnnotationValidatorMixin):
        @staticmethod
        def validate_field(value: str):
            return AnnotationValidatorMixin.validate_annotation(value)

    model = SomeModel()
    valid_annotation = model.validate_field("List[int]")
    print(valid_annotation)  # Output: "List[int]"
    ```
    """

    @staticmethod
    def validate_annotation(value: Union[str, None]) -> Union[str, None]:
        """
        Validate a type annotation against a list of supported annotations.

        Parameters:
        -----------
        value : Union[str, None]
            The type annotation to validate. Can be a string or None.

        Returns:
        --------
        - **Union[str, None]**: The validated annotation if it is supported, or None if the input is None.

        Raises:
        -------
        - **ValueError**: If the annotation is not in the list of supported annotations.
        """
        if not value:
            return None
        if value and value.split("[")[0] not in Constants.SUPPORTED_ANNOTATIONS:
            raise ValueError(
                Errors.INVALID_ANNOTATION.format(value, Constants.SUPPORTED_ANNOTATIONS)
            )
        return value

