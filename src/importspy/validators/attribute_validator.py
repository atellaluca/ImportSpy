from ..models import Attribute
from ..errors import Errors
from ..constants import Constants
from typing import List

class AttributeValidator:

    def validate(self,
                 attrs_1: List[Attribute],
                 attrs_2: List[Attribute], classname:str):
        if not attrs_1:
            return
        if attrs_1 and not attrs_2:
            return True
        if not attrs_2:
            return False
        for attr_1 in attrs_1:
            if attr_1 not in attrs_2:
                raise ValueError(Errors.CLASS_ATTRIBUTE_MISSING.format(attr_1.type, f"{attr_1.name}={attr_1.value}", classname))
        for attr_1 in attrs_1:
            attr_2 =  next((attr for attr in attrs_2 if attr.name == attr_1.name), None)
            if attr_1.value != attr_2.value:
                raise ValueError(Errors.CLASS_ATTRIBUTE_MISMATCH.format(Constants.VALUE, attr_1.type, attr_1.name, attr_1.value, attr_2.value))
                