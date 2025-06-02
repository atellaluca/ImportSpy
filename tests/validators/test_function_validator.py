import pytest
from importspy.models import (
    Function
)
from typing import List
from importspy.validators import FunctionValidator
from importspy.constants import Errors
import re

class TestFunctionValidator:

    validator = FunctionValidator()

    @pytest.fixture
    def data_1(self):
        return [Function(
            name="function",
        )]
    
    @pytest.fixture
    def data_2(self):
        return [Function(
            name="getname",
            return_annotation="str"
        )]
    
    @pytest.fixture
    def data_3(self):
        return [Function(
            name="function",
            return_annotation="int"
        )]
    
    @pytest.fixture
    def data_4(self):
        return [Function(
            name="function",
            return_annotation="str"
        )]
    
    @pytest.fixture
    def class_type_contract(self, class_type_bundle):
        return VariableContractViolation(Errors.SCOPE_VARIABLE, Contexts.CLASS_CONTEXT, class_type_bundle)
    
    @pytest.fixture
    def function_return_annotation_setter(self, data_3:Function):
        data_3[0].return_annotation = "str"

    def test_function_match(self, data_1:List[Function], data_4:List[Function]):
        assert self.validator.validate(data_1, data_4, "classname")
    
    def test_function_mismatch(self, data_2:List[Function]):
        assert self.validator.validate(None, data_2, "classname") is None
    
    @pytest.mark.usefixtures("function_return_annotation_setter")
    def test_function_mismatch_1(self, data_2:List[Function], data_3:List[Function]):
        with pytest.raises(
            ValueError,
            match=re.escape(
                Errors.FUNCTIONS_MISSING.format("function", data_2[0].name)
            )
        ):
            self.validator.validate(data_2, data_3)

    def test_function_mismatch_1(self, data_3:List[Function], data_4:List[Function]):
        with pytest.raises(
            ValueError,
            match=re.escape(
                Errors.FUNCTION_RETURN_ANNOTATION_MISMATCH.format(
                    "method in class classname",
                    data_4[0].name,
                    data_4[0].return_annotation,
                    data_3[0].return_annotation
                )
            )
        ):
            self.validator.validate(data_4, data_3, "classname")
    
    def test_function_mismatch_2(self):
        assert self.validator.validate(None, None, "classname") is None
    
    def test_function_mismatch_3(self, data_2:List[Function]):
        assert self.validator.validate(None, data_2, "classname") is None
    
    def test_function_mismatch_5(self, data_3:List[Function]):
        with pytest.raises(
            ValueError,
            match=re.escape(Errors.ELEMENT_MISSING.format(data_3))
        ):
            self.validator.validate(data_3, None, "classname")