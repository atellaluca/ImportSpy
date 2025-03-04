import pytest
from importspy import (
    Argument,
    Config
)
from typing import List
from importspy.validators.argument_validator import ArgumentValidator
from importspy.errors import Errors
import re
from importspy.constants import Constants

class TestArgumentValidator:

    validator = ArgumentValidator()

    @pytest.fixture
    def data_1(self):
        return [Argument(
            name="arg1",
            annotation="int",
            value=10
        )]

    @pytest.fixture
    def data_2(self):
        return [Argument(
            name="arg2",
            annotation="str",
            value="test"
        )]

    @pytest.fixture
    def data_3(self):
        return [Argument(
            name="arg1",
            annotation="int",
            value=20
        )]

    @pytest.fixture
    def data_4(self):
        return [Argument(
            name="arg1",
            annotation="int",
            value=10
        )]

    @pytest.fixture
    def argument_value_setter(self, data_3: List[Argument]):
        data_3[0].value = 10

    @pytest.fixture
    def argument_annotation_setter(self, data_3: List[Argument]):
        data_3[0].annotation = "str"

    def test_argument_match(self, data_1: List[Argument], data_4: List[Argument]):
        assert self.validator.validate(data_1, data_4, "function_name")

    @pytest.mark.usefixtures("argument_value_setter")
    def test_argument_match_1(self, data_1: List[Argument], data_3: List[Argument]):
        assert self.validator.validate(data_1, data_3, "function_name")

    def test_argument_mismatch(self, data_2: List[Argument]):
        assert self.validator.validate(None, data_2, "function_name") is None

    def test_argument_mismatch_1(self, data_3: List[Argument], data_4: List[Argument]):
        with pytest.raises(ValueError,
                           match=re.escape(
                               Errors.ARGUMENT_MISMATCH.format(
                                   Constants.VALUE,
                                   data_4[0].name,
                                   data_4[0].value,
                                   data_3[0].value
                               )
                           )):
            self.validator.validate(data_4, data_3, "function_name")

    def test_argument_mismatch_2(self):
        assert self.validator.validate(None, None, "function_name") is None

    def test_argument_mismatch_3(self, data_2: List[Argument]):
        assert self.validator.validate(None, data_2, "function_name") is None

    @pytest.mark.usefixtures("argument_value_setter")
    @pytest.mark.usefixtures("argument_annotation_setter")
    def test_argument_mismatch_5(self, data_1: List[Argument], data_3: List[Argument]):
        arg_1 = data_3[0]
        arg_2 = data_1[0]
        with pytest.raises(
            ValueError,
            match=re.escape(Errors.ARGUMENT_MISMATCH.format(Constants.ANNOTATION, arg_1.name, arg_1.annotation, arg_2.annotation))
        ):
            self.validator.validate(data_3, data_1, "function_name")

    def test_argument_mismatch_6(self, data_1: List[Argument], data_3: List[Argument]):
        arg_1 = data_3[0]
        arg_2 = data_1[0]
        with pytest.raises(
            ValueError,
            match=re.escape(Errors.ARGUMENT_MISMATCH.format(Constants.VALUE, arg_1.name, arg_1.value, arg_2.value))
        ):
            self.validator.validate(data_3, data_1, "function_name")
    
    def test_argument_mismatch_7(self, data_1: List[Argument]):
        with pytest.raises(
            ValueError,
            match=re.escape(
                Errors.ELEMENT_MISSING.format(data_1)
            )
        ):
            self.validator.validate(data_1, None, "function_name")

