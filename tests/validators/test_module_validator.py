import pytest
from importspy.models import (
    Module,
    Variable
)
from importspy.validators import ModuleValidator
from importspy.violation_systems import (
    Bundle,
    ModuleContractViolation
)
from importspy.constants import Errors
import re
from typing import List
from importspy.constants import Contexts

class TestModuleValidator:
    
    validator = ModuleValidator()

    @pytest.fixture
    def data_1(self):
        return [Module(
            filename="module.py",
        )]
    
    @pytest.fixture
    def data_2(self):
        return [Module(
            filename="package.py",
            version="0.1.0"
        )]

    @pytest.fixture
    def data_3(self):
        return [Module(
            filename="package.py",
            version="0.2.0"
        )]
    
    @pytest.fixture
    def module_contract(self, methodbundle:Bundle) -> ModuleContractViolation:
        return ModuleContractViolation(Contexts.RUNTIME_CONTEXT, methodbundle)
    
    @pytest.fixture
    def filename_setter(self, data_1:List[Module]):
        data_1[0].filename="package.py"

    
    @pytest.fixture
    def version_unsetter(self, data_2:List[Module]):
        data_2[0].version=None

    @pytest.fixture
    def variables_setter(self, data_2:List[Module]):
        data_2[0].variables=[
            Variable(
                name="attempt",
                value=4
            ),
            Variable(
                name="msg",
                value="Hi!"
            )
        ]

    @pytest.fixture
    def data_3(self):
        return [Module(
            filename="package.py",
            version="0.1.0",
            variables=[
                Variable(
                    name="attempt",
                    value=4
                )
            ]
        )]
    
    @pytest.fixture
    def variables_msg_setter(self, data_3:List[Module]):
        data_3[0].variables.append(Variable(name="msg", value="Hi!"))

    @pytest.mark.usefixtures("filename_setter")
    @pytest.mark.usefixtures("version_unsetter")
    def test_module_match(self, data_1:List[Module], data_2:List[Module], module_contract:ModuleContractViolation):
        assert self.validator.validate(data_1, data_2[0], module_contract) is None

    @pytest.mark.usefixtures("filename_setter")
    @pytest.mark.usefixtures("variables_setter")
    @pytest.mark.usefixtures("variables_msg_setter")
    def test_module_match_1(self, data_2:List[Module], data_3:List[Module], module_contract:ModuleContractViolation):
        assert self.validator.validate(data_2, data_3[0], module_contract) is None
    
    def test_module_match_2(self, data_2:List[Module], data_3:List[Module], module_contract:ModuleContractViolation):
        assert self.validator.validate(data_2, data_3[0], module_contract) is None
    
    def test_module_mismatch(self, data_2:List[Module], module_contract:ModuleContractViolation):
        assert self.validator.validate(None, data_2[0], module_contract) is None
    
    @pytest.mark.usefixtures("version_unsetter")
    def test_module_mismatch_1(self, data_1:List[Module], data_2:List[Module], module_contract:ModuleContractViolation):
        with pytest.raises(ValueError,
                           match=re.escape(
                               module_contract.mismatch_error_handler(data_1[0].filename, data_2[0].filename, Errors.ENTITY_MESSAGES)
                           )
        ):
            self.validator.validate(data_1, data_2[0], module_contract)
    
    @pytest.mark.usefixtures("version_unsetter")
    def test_module_mismatch_1(self, data_3:List[Module], data_2:List[Module], module_contract:ModuleContractViolation):
        with pytest.raises(ValueError,
                           match=re.escape(
                               module_contract.mismatch_error_handler(data_3[0].version, data_2[0].version, Errors.ENTITY_MESSAGES)
                           )
        ):
            self.validator.validate(data_3, data_2[0], module_contract)