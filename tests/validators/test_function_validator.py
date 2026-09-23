import pytest
from importspy.models import Function
from typing import List
from importspy.validators import FunctionValidator

from importspy.violation_systems import FunctionContractViolation, Bundle

from importspy.constants import Errors, Contexts

import re


class TestFunctionValidator:
    validator = FunctionValidator()

    @pytest.fixture
    def data_1(self):
        return [
            Function(
                name="function",
            )
        ]

    @pytest.fixture
    def data_2(self):
        return [Function(name="getname", return_annotation="str")]

    @pytest.fixture
    def data_3(self):
        return [Function(name="function", return_annotation="int")]

    @pytest.fixture
    def data_4(self):
        return [Function(name="function", return_annotation="str")]

    @pytest.fixture
    def function_contract(self, functionbundle: Bundle):
        return FunctionContractViolation(Contexts.MODULE_CONTEXT, functionbundle)

    @pytest.fixture
    def function_return_annotation_setter(self, data_3: Function):
        data_3[0].return_annotation = "str"

    def test_function_match(
        self,
        data_1: List[Function],
        data_4: List[Function],
        function_contract: FunctionContractViolation,
    ):
        assert self.validator.validate(data_1, data_4, function_contract) is None

    def test_function_mismatch(self, data_2: List[Function], function_contract):
        assert self.validator.validate(None, data_2, function_contract) is None

    @pytest.mark.usefixtures("function_return_annotation_setter")
    def test_function_missing_name(
        self,
        data_2: List[Function],
        data_3: List[Function],
        function_contract: FunctionContractViolation,
    ):
        key = Errors.FUNCTIONS_DINAMIC_PAYLOAD[Errors.ENTITY_MESSAGES][
            function_contract.context
        ]
        function_contract.bundle[key] = data_2[0].name
        with pytest.raises(
            ValueError,
            match=re.escape(
                function_contract.missing_error_handler(Errors.ENTITY_MESSAGES)
            ),
        ):
            self.validator.validate(data_2, data_3, function_contract)

    def test_function_return_annotation_mismatch(
        self,
        data_3: List[Function],
        data_4: List[Function],
        function_contract: FunctionContractViolation,
    ):
        mock_bundle = Bundle()
        mock_bundle[Errors.KEY_FILE_NAME] = "testmodule.py"
        mock_bundle[Errors.KEY_FUNCTION_NAME] = "function"
        mock_contract_violation = FunctionContractViolation(
            Contexts.MODULE_CONTEXT, mock_bundle
        )
        with pytest.raises(
            ValueError,
            match=re.escape(
                mock_contract_violation.mismatch_error_handler(
                    data_4[0].return_annotation,
                    data_3[0].return_annotation,
                    Errors.ENTITY_MESSAGES,
                )
            ),
        ):
            self.validator.validate(data_4, data_3, function_contract)

    def test_function_mismatch_2(self, function_contract: FunctionContractViolation):
        assert self.validator.validate(None, None, function_contract) is None

    def test_function_mismatch_3(
        self, data_2: List[Function], function_contract: FunctionContractViolation
    ):
        assert self.validator.validate(None, data_2, function_contract) is None

    def test_function_mismatch_5(
        self, data_3: List[Function], function_contract: FunctionContractViolation
    ):
        mock_bundle = Bundle()
        mock_bundle[Errors.KEY_FILE_NAME] = "testmodule.py"
        mock_bundle[Errors.KEY_FUNCTIONS_1] = data_3
        mock_contract_violation = FunctionContractViolation(
            Contexts.MODULE_CONTEXT, mock_bundle
        )
        with pytest.raises(
            ValueError,
            match=re.escape(
                mock_contract_violation.missing_error_handler(
                    Errors.COLLECTIONS_MESSAGES
                )
            ),
        ):
            self.validator.validate(data_3, None, function_contract)
