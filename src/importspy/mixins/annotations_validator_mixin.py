"""
Annotation Validation Mixin
===========================

Provides a mixin to enforce that type annotations used in contracts are valid 
and compatible with ImportSpy’s supported annotation types.

This mixin is typically used inside models or validation layers where annotations 
play a key role in describing expected structures.

Example
-------
.. code-block:: python

    from importspy.mixins.annotations_validator_mixin import AnnotationValidatorMixin

    class Custom(AnnotationValidatorMixin):
        def process(self, value: str):
            return self.validate_annotation(value)
"""

from ..constants import Constants
from ..errors import Errors
from typing import Union

class AnnotationValidatorMixin:
    """
    Mixin for validating type annotations in contract definitions.

    This class helps enforce consistency across all annotation fields used
    within ImportSpy, ensuring that only supported types are allowed.

    Methods
    -------
    validate_annotation(value: Union[str, None]) -> Union[str, None]
        Checks whether a given annotation is recognized and allowed.

    Example
    -------
    >>> AnnotationValidatorMixin.validate_annotation("List[int]")
    'List[int]'

    >>> AnnotationValidatorMixin.validate_annotation("CustomType")
    ValueError: Invalid annotation: expected one of [...]
    """

    @staticmethod
    def validate_annotation(value: Union[str, None]) -> Union[str, None]:
        """
        Validate a type annotation against supported annotations.

        Parameters
        ----------
        value : Union[str, None]
            The annotation string to validate (e.g., "int", "List[str]").

        Returns
        -------
        Union[str, None]
            The same value if it's valid or None if no annotation provided.

        Raises
        ------
        ValueError
            If the annotation type is not supported by ImportSpy.
        """
        if not value:
            return None
        base = value.split("[")[0]
        if base not in Constants.SUPPORTED_ANNOTATIONS:
            raise ValueError(
                Errors.INVALID_ANNOTATION.format(value, Constants.SUPPORTED_ANNOTATIONS)
            )
        return value
