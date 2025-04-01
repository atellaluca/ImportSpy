"""
importspy.validators.attribute_validator
========================================

This module implements the validation logic for class and instance attributes
within modules inspected by ImportSpy.

The `AttributeValidator` ensures that attributes declared in the import contract
match the ones actually defined in the module under inspection in terms of:
- Existence
- Type annotation
- Default value
"""

from ..models import Attribute
from ..errors import Errors
from ..constants import Constants
from typing import List
from importspy.log_manager import LogManager


class AttributeValidator:
    """
    Validator for class and instance attributes.

    Compares expected attributes (from the import contract) with those
    extracted from the inspected module. Ensures attribute names,
    annotations, and values are consistent.

    Attributes
    ----------
    logger : logging.Logger
        Internal logger used for debug tracing during validation.

    Methods
    -------
    validate(attrs_1, attrs_2, classname)
        Performs full validation of attributes for a given class.
    """

    def __init__(self):
        """
        Initializes the AttributeValidator with scoped logging.
        """
        self.logger = LogManager().get_logger(self.__class__.__name__)

    def validate(
        self,
        attrs_1: List[Attribute],
        attrs_2: List[Attribute],
        classname: str
    ):
        """
        Validates expected vs actual attributes in a class definition.

        Parameters
        ----------
        attrs_1 : List[Attribute]
            List of attributes defined in the import contract.

        attrs_2 : List[Attribute]
            List of attributes found in the actual module.

        classname : str
            The name of the class whose attributes are being validated.

        Returns
        -------
        bool
            True if all attributes match expectations.

        Raises
        ------
        ValueError
            - If required attributes are missing.
            - If type annotations differ.
            - If attribute values differ.

        Example
        -------
        >>> validator = AttributeValidator()
        >>> validator.validate(
        ...     attrs_1=[Attribute(name="path", value="/tmp", annotation="str", type="class")],
        ...     attrs_2=[Attribute(name="path", value="/tmp", annotation="str", type="class")],
        ...     classname="Config"
        ... )
        True
        """
        self.logger.debug(f"Type of attrs_1: {type(attrs_1)}")
        self.logger.debug(
            Constants.LOG_MESSAGE_TEMPLATE.format(
                operation="Attribute validating",
                status="Starting",
                details=f"Expected attributes: {attrs_1} ; Current attributes: {attrs_2}"
            )
        )

        if not attrs_1:
            self.logger.debug(
                Constants.LOG_MESSAGE_TEMPLATE.format(
                    operation="Check if attrs_1 is not none",
                    status="Finished",
                    details=f"No expected attributes; attrs_1: {attrs_1}"
                )
            )
            return

        if not attrs_2:
            self.logger.debug(
                Constants.LOG_MESSAGE_TEMPLATE.format(
                    operation="Checking attrs_2 when attrs_1 is missing",
                    status="Finished",
                    details=f"No actual attributes found; attrs_2: {attrs_2}"
                )
            )
            raise ValueError(Errors.ELEMENT_MISSING.format(attrs_1))

        for attr_1 in attrs_1:
            self.logger.debug(f"Type of attr_1: {type(attr_1)}")
            self.logger.debug(
                Constants.LOG_MESSAGE_TEMPLATE.format(
                    operation="Attribute validating",
                    status="Progress",
                    details=f"Current attr_1: {attr_1}"
                )
            )
            if attr_1.name not in {attr.name for attr in attrs_2}:
                self.logger.debug(Constants.LOG_MESSAGE_TEMPLATE.format(
                    operation="Checking if attr_1 is in attrs_2",
                    status="Finished",
                    details=Errors.CLASS_ATTRIBUTE_MISSING.format(
                        attr_1.type,
                        f"{attr_1.name}={attr_1.value}",
                        classname
                    )
                ))
                raise ValueError(
                    Errors.CLASS_ATTRIBUTE_MISSING.format(
                        attr_1.type,
                        f"{attr_1.name}={attr_1.value}",
                        classname
                    )
                )

        for attr_1 in attrs_1:
            attr_2 = next((attr for attr in attrs_2 if attr.name == attr_1.name), None)
            if not attr_2:
                raise ValueError(Errors.ELEMENT_MISSING.format(attrs_1))

            if attr_1.annotation and attr_1.annotation != attr_2.annotation:
                raise ValueError(
                    Errors.CLASS_ATTRIBUTE_MISMATCH.format(
                        Constants.ANNOTATION,
                        attr_1.type,
                        attr_1.name,
                        attr_1.annotation,
                        attr_2.annotation
                    )
                )

            if attr_1.value != attr_2.value:
                raise ValueError(
                    Errors.CLASS_ATTRIBUTE_MISMATCH.format(
                        Constants.VALUE,
                        attr_1.type,
                        attr_1.name,
                        attr_1.value,
                        attr_2.value
                    )
                )

        return True
