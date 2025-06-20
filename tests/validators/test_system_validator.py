import pytest
from importspy.models import (
    System,
    Environment,
    Variable
)
from importspy.config import Config

from importspy.constants import (
    Contexts,
    Constants
)

from importspy.validators import SystemValidator
from importspy.constants import Errors
import re
from typing import List

from importspy.violation_systems import (
    Bundle,
    SystemContractViolation,
    VariableContractViolation
)

class TestSystemValidator:

    validator = SystemValidator()

    @pytest.fixture
    def data_1(self):
        return [System(
            os=Constants.SupportedOS.OS_LINUX,
            environment=Environment(
                variables=[Variable(
                    name="CI",
                    value="true"
                )]
            ),
            pythons=[]
        )]
    
    @pytest.fixture
    def data_2(self):
        return [System(
            os=Constants.SupportedOS.OS_LINUX,
            pythons=[]
        )]
    
    @pytest.fixture
    def systembundle(self) -> Bundle:
        bundle = Bundle()
        return bundle
    
    @pytest.fixture
    def variable_contract(self, systembundle) -> VariableContractViolation:
        return VariableContractViolation(Errors.SCOPE_VARIABLE, Contexts.ENVIRONMENT_CONTEXT, systembundle)
    
    @pytest.fixture
    def system_contract(self, systembundle) -> SystemContractViolation:
        return SystemContractViolation(Contexts.RUNTIME_CONTEXT, systembundle)
    
    @pytest.fixture
    def os_windows_setter(self, data_1:List[System]):
        data_1[0].os = Constants.SupportedOS.OS_WINDOWS
    
    @pytest.fixture
    def envs_setter(self, data_2):
        data_2[0].environment = Environment(variables=[(Variable(name="CI", value="true"))])

    @pytest.mark.usefixtures("envs_setter")
    def test_system_os_match(self, data_1:List[System], data_2:List[System], system_contract: SystemContractViolation):
        assert self.validator.validate(data_1, data_2, system_contract) == data_1[0].pythons
    
    def test_system_os_match_2(self, data_1:List[System], data_2:List[System], system_contract: SystemContractViolation):
        assert self.validator.validate(data_2, data_1, system_contract) == data_2[0].pythons
    
    def test_system_os_mismatch(self, data_1:List[System], data_2:List[System], system_contract: SystemContractViolation):
        mock_contract = VariableContractViolation(
            Errors.SCOPE_VARIABLE,
            Contexts.ENVIRONMENT_CONTEXT,
            Bundle(
                state= { 
                    Errors.KEY_ENVIRONMENT_1 : data_1[0].environment,
                    Errors.KEY_ENVIRONMENT_VARIABLE_NAME: "CI"
                }
            )
        )
        with pytest.raises(ValueError,
                           match=re.escape(
                               mock_contract.missing_error_handler(Errors.COLLECTIONS_MESSAGES)
                           )
        ):
            self.validator.validate(data_1, data_2, system_contract)

    @pytest.mark.usefixtures("os_windows_setter")
    def test_system_os_mismatch_1(self, data_1:List[System], data_2:List[System], system_contract: SystemContractViolation):
        bundle: Bundle = Bundle()
        bundle[Errors.KEY_SYSTEMS_1] = data_1
        mock_contract = SystemContractViolation(
            Contexts.RUNTIME_CONTEXT,
            bundle
        )
        with pytest.raises(ValueError,
                           match=re.escape(
                               mock_contract.missing_error_handler(Errors.COLLECTIONS_MESSAGES)
                           )
        ):
            self.validator.validate(data_1, data_2, system_contract)
    
    def test_system_mismatch(self, data_2:List[System], system_contract: SystemContractViolation):
        assert self.validator.validate(None, data_2, system_contract) is None
    
    def test_system_mismatch_1(self, data_2:List[System], system_contract: SystemContractViolation):
        bundle: Bundle = Bundle()
        bundle[Errors.KEY_SYSTEMS_1] = data_2
        mock_contract = SystemContractViolation(
            Contexts.RUNTIME_CONTEXT,
            bundle
        )
        with pytest.raises(ValueError,
                           match=re.escape(
                               mock_contract.missing_error_handler(Errors.COLLECTIONS_MESSAGES)
                           )
        ):
            self.validator.validate(data_2, None, system_contract)