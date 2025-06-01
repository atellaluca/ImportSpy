import pytest
from importspy.models import (
    Attribute
)

from importspy.validators import VariableValidator

from typing import List

import re

from importspy.constants import (
    Constants,
    Errors,
    Contexts
)

from importspy.violation_systems import (
    VariableContractViolation, 
    Bundle
)

from importspy.config import Config


class TestAttributeValidator:

    validator = VariableValidator()

    @pytest.fixture
    def data_1(self):
        return [Attribute(
            type=Config.CLASS_TYPE,
            name="class_attribute",
            value=4
        )]
    
    @pytest.fixture
    def data_2(self):
        return [Attribute(
            type=Config.INSTANCE_TYPE,
            name="instance_attribute",
            value="value"
        )]
    
    @pytest.fixture
    def data_3(self):
        return [Attribute(
            type=Config.INSTANCE_TYPE,
            name="instance_attribute",
            value=2
        )]
    
    @pytest.fixture
    def data_4(self):
        return [Attribute(
            type=Config.CLASS_TYPE,
            name="class_attribute",
            value=4
        )]
    
    @pytest.fixture
    def class_type_bundle(self, classbundle) -> Bundle:
        classbundle[Errors.KEY_ATTRIBUTE_TYPE] = Config.CLASS_TYPE
        return classbundle
    
    @pytest.fixture
    def instance_type_bundle(self, classbundle) -> Bundle:
        classbundle[Errors.KEY_ATTRIBUTE_TYPE] = Config.INSTANCE_TYPE
        return classbundle
    
    @pytest.fixture
    def class_type_contract(self, class_type_bundle):
        return VariableContractViolation(Errors.SCOPE_ARGUMENT, Contexts.CLASS_CONTEXT, class_type_bundle)
    
    @pytest.fixture
    def instance_type_contract(self, instance_type_bundle):
        return VariableContractViolation(Errors.SCOPE_ARGUMENT, Contexts.CLASS_CONTEXT, instance_type_bundle)

    
    @pytest.fixture
    def attribute_value_setter(self, data_3:Attribute):
        data_3[0].value = "value"

    def test_attribute_match(self, data_1:List[Attribute], data_4:List[Attribute]):
        assert self.validator.validate(data_1, data_4, "classname")

    @pytest.mark.usefixtures("attribute_value_setter")
    def test_attribute_match_1(self, data_2:List[Attribute], data_3:List[Attribute]):
        assert self.validator.validate(data_2, data_3, "classname")
    
    def test_attribute_mismatch(self, data_2:List[Attribute]):
        assert self.validator.validate(None, data_2, "classname") is None

    def test_attribute_mismatch_1(self, data_3, data_4):
        with pytest.raises(ValueError,
                           match=re.escape(
                               Errors.CLASS_ATTRIBUTE_MISSING.format(
                                   Config.CLASS_TYPE,
                                   f"{data_4[0].name}={data_4[0].value}",
                                   "classname"
                               )
                           )):
            self.validator.validate(data_4, data_3, "classname")
    
    def test_attribute_mismatch_2(self):
        assert self.validator.validate(None, None, "classname") is None
    
    def test_attribute_mismatch_3(self, data_2:List[Attribute]):
        assert self.validator.validate(None, data_2, "classname") is None
    
    @pytest.fixture
    def attribute_annotation_setter(self, data_3:Attribute):
        data_3[0].annotation = "str"
    
    @pytest.mark.usefixtures("attribute_value_setter")
    @pytest.mark.usefixtures("attribute_annotation_setter")
    def test_attribute_match_3(self, data_2:List[Attribute], data_3:List[Attribute]):
        assert self.validator.validate(data_2, data_3, "classname")
    
    @pytest.mark.usefixtures("attribute_value_setter")
    @pytest.mark.usefixtures("attribute_annotation_setter")
    def test_attribute_mismatch_5(self, data_2:List[Attribute], data_3:List[Attribute]):
        attr_1 = data_3[0]
        attr_2 = data_2[0]
        with pytest.raises(
            ValueError,
            match=re.escape(Errors.CLASS_ATTRIBUTE_MISMATCH.format(Constants.ANNOTATION, attr_1.type, attr_1.name, attr_1.annotation, attr_2.annotation))
        ):
            self.validator.validate(data_3, data_2, "classname")
    
    def test_attribute_mismatch_6(self, data_3:List[Attribute]):
        with pytest.raises(
            ValueError,
            match=re.escape(Errors.ELEMENT_MISSING.format(data_3))
        ):
            self.validator.validate(data_3, None, "classname")