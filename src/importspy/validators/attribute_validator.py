from ..models import Attribute
from ..errors import Errors
from ..constants import Constants
from typing import List
from importspy.log_manager import LogManager

class AttributeValidator:

    def __init__(self):
        self.logger = LogManager().get_logger(self.__class__.__name__)

    def validate(self,
                 attrs_1: List[Attribute],
                 attrs_2: List[Attribute],
                 classname:str):
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
                    details=f"There aren't any attributes; current attrs_1: {attrs_1}"
                )
            )
            return
        if attrs_1 and not attrs_2:
            self.logger.debug(
                Constants.LOG_MESSAGE_TEMPLATE.format(
                    operation="Checking attrs_1 and attrs_2",
                    status="Finished",
                    details=f"There aren't any attrs_2; current attrs_2: {attrs_2}"
                )
            )
            return True
        if not attrs_2:
            self.logger.debug(
                Constants.LOG_MESSAGE_TEMPLATE.format(
                    operation="Checking attrs_2 when attrs_1 is missing",
                    status="Finished",
                    details=f"There aren't any attrs_2; current attrs_2: {attrs_2}"
                )
            )
            return False
        for attr_1 in attrs_1:
            self.logger.debug(f"Type of attr_1: {type(attr_1)}")
            self.logger.debug(
                Constants.LOG_MESSAGE_TEMPLATE.format(
                    operation="Attribute validating",
                    status="Progress",
                    details=f"Current attr_1: {attr_1}"
                )
            )
            if attr_1.name not in set(map(lambda attr: attr.name, attrs_2)):
                Constants.LOG_MESSAGE_TEMPLATE.format(
                    operation="Checking if attr_1 is in attrs_2",
                    status="Finished",
                    details=Errors.CLASS_ATTRIBUTE_MISSING.format(attr_1.type, f"{attr_1.name}={attr_1.value}", classname)
                )
                raise ValueError(Errors.CLASS_ATTRIBUTE_MISSING.format(attr_1.type, f"{attr_1.name}={attr_1.value}", classname))
        for attr_1 in attrs_1:
            attr_2 =  next((attr for attr in attrs_2 if attr.name == attr_1.name), None)
            if attr_1.annotation and attr_1.annotation != attr_2.annotation:
                raise ValueError(Errors.CLASS_ATTRIBUTE_MISMATCH.format(Constants.ANNOTATION, attr_1.type, attr_1.name, attr_1.annotation, attr_2.annotation))
            if attr_1.value != attr_2.value:
                raise ValueError(Errors.CLASS_ATTRIBUTE_MISMATCH.format(Constants.VALUE, attr_1.type, attr_1.name, attr_1.value, attr_2.value))
            return True
                