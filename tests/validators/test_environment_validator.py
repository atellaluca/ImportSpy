import pytest
import re
from importspy.validators import SystemValidator
from importspy.models import (
    Environment,
    Variable
)

from importspy.violation_systems import (
    VariableContractViolation,
    SystemContractViolation,
    Bundle
)

from importspy.constants import (
    Errors, 
    Contexts
)

class TestEnvironmentValidator:

    validator = SystemValidator.EnvironmentValidator()

    @pytest.fixture
    def data_1(self):
        return Environment(
            variables=[
                Variable(
                    name="CI",
                    value=True
                ),
                Variable(
                    name="CONTAINER_TYPE",
                    value="Docker"
                ),
            ],
            secrets=[
                "SECRET_KEY",
                "HASH_CODE",
                "TOKEN"
            ]
        )
    
    @pytest.fixture
    def data_2(self, data_1):
        return data_1
    
    @pytest.fixture
    def data_3(self):
        return Environment(
            variables=[
                Variable(
                    name="CI",
                    value=True
                )
            ]
        )
    
    @pytest.fixture
    def data_4(self):
        return Environment(
            secrets=[
                "SECRET_KEY",
                "HASH_CODE",
            ]
        )
    
    @pytest.fixture
    def data_5(self):
        return Environment(
            secrets=[
                "SECRET_KEY",
                "HASH_CODE",
                "A_SURGI"
            ]
        )

    
    @pytest.fixture
    def variable_contract(self, systembundle) -> VariableContractViolation:
        return VariableContractViolation(Errors.SCOPE_VARIABLE, Contexts.ENVIRONMENT_CONTEXT, systembundle)
    
    def test_environment_match(self, data_1:Environment, data_2:Environment):
        bundle: Bundle = Bundle()
        bundle[Errors.KEY_ENVIRONMENT_1] = data_1
        self.validator.validate(data_1, data_2, bundle)
    
    def test_environment_match_1(self, data_3:Environment, data_2:Environment):
        bundle: Bundle = Bundle()
        bundle[Errors.KEY_ENVIRONMENT_1] = data_3
        self.validator.validate(data_3, data_2, bundle)
    
    def test_enviroment_mismatch(self, data_2: Environment, data_3:Environment):
        bundle: Bundle = Bundle()
        bundle[Errors.KEY_ENVIRONMENT_1] = data_2
        bundle[Errors.KEY_ENVIRONMENT_VARIABLE_NAME] = "CONTAINER_TYPE"
        mock_contract = VariableContractViolation(
            Errors.SCOPE_VARIABLE,
            Contexts.ENVIRONMENT_CONTEXT,
            bundle
        )
        with pytest.raises(ValueError,
                           match=re.escape(
                               mock_contract.missing_error_handler(Errors.ENTITY_MESSAGES)
                           )
        ):
            self.validator.validate(data_2, data_3, bundle)
    
    def test_enviroment_mismatch_2(self, data_5: Environment, data_4:Environment):
        bundle: Bundle = Bundle()
        bundle[Errors.KEY_ENVIRONMENT_1] = data_5
        bundle[Errors.KEY_ENVIRONMENT_VARIABLE_NAME] = "A_SURGI"
        mock_contract = VariableContractViolation(
            Errors.SCOPE_VARIABLE,
            Contexts.ENVIRONMENT_CONTEXT,
            bundle
        )
        with pytest.raises(ValueError,
                           match=re.escape(
                               mock_contract.missing_error_handler(Errors.ENTITY_MESSAGES)
                           )
        ):
            self.validator.validate(data_5, data_4, bundle)
