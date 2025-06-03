import pytest
from importspy.models import (
    Attribute
)

from importspy.validators import VariableValidator

from typing import List

import re

from importspy.constants import (
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
        return VariableContractViolation(Errors.SCOPE_VARIABLE, Contexts.CLASS_CONTEXT, class_type_bundle)
    
    @pytest.fixture
    def instance_type_contract(self, instance_type_bundle):
        return VariableContractViolation(Errors.SCOPE_VARIABLE, Contexts.CLASS_CONTEXT, instance_type_bundle)

    
    @pytest.fixture
    def attribute_value_setter(self, data_3:Attribute):
        data_3[0].value = "value"

    def test_attribute_match(self, data_1:List[Attribute], data_4:List[Attribute], class_type_contract):
        assert self.validator.validate(data_1, data_4, class_type_contract) is None

    @pytest.mark.usefixtures("attribute_value_setter")
    def test_attribute_match_1(self, data_2:List[Attribute], data_3:List[Attribute], instance_type_contract):
        assert self.validator.validate(data_2, data_3, instance_type_contract) is None
    
    def test_attribute_mismatch(self, data_2:List[Attribute], class_type_contract):
        assert self.validator.validate(None, data_2, class_type_contract) is None

    def test_attribute_mismatch_1(self, data_3, data_4, class_type_contract):
        mock_bundle = Bundle()
        mock_bundle[Errors.KEY_ATTRIBUTE_NAME] = "class_attribute"
        mock_bundle[Errors.KEY_ATTRIBUTE_TYPE] = "class"
        mock_bundle[Errors.KEY_CLASS_NAME] = "TestClass"
        mock_contract_violation = VariableContractViolation(Errors.SCOPE_VARIABLE, Contexts.CLASS_CONTEXT, mock_bundle)
        with pytest.raises(ValueError,
                           match=re.escape(
                               mock_contract_violation.missing_error_handler(
                                   Errors.ENTITY_MESSAGES
                           ))):
            self.validator.validate(data_4, data_3, class_type_contract)
    
    def test_attribute_mismatch_2(self, instance_type_contract):
        assert self.validator.validate(None, None, instance_type_contract) is None
    
    def test_attribute_mismatch_3(self, data_2:List[Attribute], instance_type_contract):
        assert self.validator.validate(None, data_2, instance_type_contract) is None
    
    @pytest.fixture
    def attribute_annotation_setter(self, data_3:Attribute):
        data_3[0].annotation = "str"
    
    @pytest.mark.usefixtures("attribute_value_setter")
    @pytest.mark.usefixtures("attribute_annotation_setter")
    def test_attribute_match_3(self, data_2:List[Attribute], data_3:List[Attribute], instance_type_contract):
        assert self.validator.validate(data_2, data_3, instance_type_contract) is None
    
    @pytest.mark.usefixtures("attribute_value_setter")
    @pytest.mark.usefixtures("attribute_annotation_setter")
    def test_attribute_mismatch_5(self, data_2:List[Attribute], data_3:List[Attribute], instance_type_contract):
        mock_bundle = Bundle()
        mock_bundle[Errors.KEY_ATTRIBUTE_NAME] = "instance_attribute"
        mock_bundle[Errors.KEY_ATTRIBUTE_TYPE] = "instance"
        mock_bundle[Errors.KEY_CLASS_NAME] = "TestClass"
        mock_contract_violation = VariableContractViolation(Errors.SCOPE_VARIABLE, Contexts.CLASS_CONTEXT, mock_bundle)
        with pytest.raises(
            ValueError,
            match=re.escape(
                mock_contract_violation.mismatch_error_handler(data_3[0].annotation, data_2[0].annotation, Errors.ENTITY_MESSAGES)
            )
        ):
            self.validator.validate(data_3, data_2, instance_type_contract)
    
    def test_attribute_mismatch_6(self, data_3:List[Attribute], instance_type_contract):
        mock_bundle = Bundle()
        mock_bundle[Errors.KEY_ATTRIBUTES_1] = data_3
        mock_bundle[Errors.KEY_CLASS_NAME] = "TestClass"
        mock_contract_violation = VariableContractViolation(Errors.SCOPE_VARIABLE, Contexts.CLASS_CONTEXT, mock_bundle)
        with pytest.raises(
            ValueError,
            match=re.escape(
                mock_contract_violation.missing_error_handler(Errors.COLLECTIONS_MESSAGES)
            )
        ):
            self.validator.validate(data_3, None, instance_type_contract)