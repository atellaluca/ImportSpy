import pytest
from importspy.models import (
    Argument
)
from typing import List
from importspy.validators import VariableValidator
import re

from importspy.constants import (
    Errors,
    Contexts
)

from importspy.violation_systems import (
    VariableContractViolation, 
    Bundle
)

class TestArgumentValidator:

    validator = VariableValidator()

    @pytest.fixture
    def data_1(self) -> Argument:
        return [Argument(
            name="arg1",
            annotation="int",
            value=10
        )]

    @pytest.fixture
    def data_2(self) -> Argument:
        return [Argument(
            name="arg2",
            annotation="str",
            value="test"
        )]

    @pytest.fixture
    def data_3(self) -> Argument:
        return [Argument(
            name="arg1",
            annotation="int",
            value=20
        )]

    @pytest.fixture
    def data_4(self) -> Argument:
        return [Argument(
            name="arg1",
            annotation="int",
            value=10
        )]

    @pytest.fixture
    def contract_violation(self, functionbundle:Bundle) -> VariableContractViolation:
        return VariableContractViolation(Errors.SCOPE_ARGUMENT, Contexts.MODULE_CONTEXT, functionbundle)
    
    @pytest.fixture
    def argument_value_setter(self, data_3: List[Argument]):
        data_3[0].value = 10

    @pytest.fixture
    def argument_annotation_setter(self, data_3: List[Argument]):
        data_3[0].annotation = "str"

    def test_argument_match(self, data_1: List[Argument], data_4: List[Argument], contract_violation):
        assert data_1
        assert data_4
        assert self.validator.validate(data_1, data_4, contract_violation) is None

    @pytest.mark.usefixtures("argument_value_setter")
    def test_argument_match_1(self, data_1: List[Argument], data_3: List[Argument], contract_violation):
        assert data_1
        assert data_3
        assert self.validator.validate(data_1, data_3, contract_violation) is None

    def test_argument_mismatch_no_data(self, data_2: List[Argument], contract_violation):
        assert self.validator.validate(None, data_2, contract_violation) is None

    def test_argument_mismatch_1(self, data_3: List[Argument], data_4: List[Argument], contract_violation: VariableContractViolation):
        mock_bundle = Bundle()
        mock_bundle[Errors.KEY_ARGUMENT_NAME] = "arg1"
        mock_bundle[Errors.KEY_FUNCTION_NAME] = "test_function"
        mock_contract_violation = VariableContractViolation(Errors.SCOPE_ARGUMENT, Contexts.MODULE_CONTEXT, mock_bundle)
        with pytest.raises(ValueError,
                           match=re.escape(
                               mock_contract_violation.mismatch_error_handler(
                                   data_4[0].value,
                                   data_3[0].value,
                                   Errors.ENTITY_MESSAGES,
                               )
                           )):
            self.validator.validate(data_4, data_3, contract_violation)

    def test_argument_mismatch_2(self, contract_violation):
        assert self.validator.validate(None, None, contract_violation) is None

    def test_argument_mismatch_3(self, data_2: List[Argument], contract_violation):
        assert self.validator.validate(None, data_2, contract_violation) is None

    @pytest.mark.usefixtures("argument_value_setter")
    @pytest.mark.usefixtures("argument_annotation_setter")
    def test_argument_mismatch_5(self, data_1: List[Argument], data_3: List[Argument], contract_violation):
        mock_bundle = Bundle()
        mock_bundle[Errors.KEY_ARGUMENT_NAME] = "arg1"
        mock_bundle[Errors.KEY_FUNCTION_NAME] = "test_function"
        mock_contract_violation = VariableContractViolation(Errors.SCOPE_ARGUMENT, Contexts.MODULE_CONTEXT, mock_bundle)
        with pytest.raises(ValueError,
                           match=re.escape(
                               mock_contract_violation.mismatch_error_handler(
                                   data_3[0].annotation,
                                   data_1[0].annotation,
                                   Errors.ENTITY_MESSAGES,
                               )
                           )):
            self.validator.validate(data_3, data_1, contract_violation)

    def test_argument_mismatch_6(self, data_1: List[Argument], data_3: List[Argument], contract_violation):
        mock_bundle = Bundle()
        mock_bundle[Errors.KEY_ARGUMENT_NAME] = "arg1"
        mock_bundle[Errors.KEY_FUNCTION_NAME] = "test_function"
        mock_contract_violation = VariableContractViolation(Errors.SCOPE_ARGUMENT, Contexts.MODULE_CONTEXT, mock_bundle)
        with pytest.raises(ValueError,
                           match=re.escape(
                               mock_contract_violation.mismatch_error_handler(
                                   data_3[0].value,
                                   data_1[0].value,
                                   Errors.ENTITY_MESSAGES,
                               )
                           )):
            self.validator.validate(data_3, data_1, contract_violation)
    
    def test_argument_mismatch_7(self, data_1: List[Argument], contract_violation):
        mock_bundle = Bundle()
        mock_bundle[Errors.KEY_ARGUMENTS_1] = data_1
        mock_bundle[Errors.KEY_FUNCTION_NAME] = "test_function"
        mock_contract_violation = VariableContractViolation(Errors.SCOPE_ARGUMENT, Contexts.MODULE_CONTEXT, mock_bundle)
        with pytest.raises(ValueError,
                           match=re.escape(
                               mock_contract_violation.missing_error_handler(
                                   Errors.COLLECTIONS_MESSAGES,
                               )
                           )):
            self.validator.validate(data_1, None, contract_violation)

