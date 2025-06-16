import pytest
from importspy.models import (
    Runtime
)
from importspy.config import Config

from importspy.validators import RuntimeValidator
from importspy.constants import (
    Errors,
    Constants,
    Contexts
)

import re
from typing import List
from importspy.violation_systems import (
    Bundle,
    RuntimeContractViolation
)

class TestRuntimeValidator:

    validator = RuntimeValidator()

    @pytest.fixture
    def data_1(self):
        return [Runtime(
            arch=Config.ARCH_ARM64,
            systems=[]
        )]
    
    @pytest.fixture
    def data_2(self):
        return [Runtime(
            arch=Config.ARCH_ARM64,
            systems=[]
        )]
    
    @pytest.fixture
    def runtimebundle(self) -> Bundle:
        bundle = Bundle()
        return bundle
    
    @pytest.fixture
    def runtime_contract(self, runtimebundle: Bundle) -> RuntimeContractViolation:
        return RuntimeContractViolation(context=Contexts.RUNTIME_CONTEXT, bundle=runtimebundle)
    
    @pytest.fixture
    def arch_arm_setter(self, data_1:List[Runtime]):
        data_1[0].arch = Config.ARCH_ARM

    def test_runtime_arch_match(self, data_1:List[Runtime], data_2:List[Runtime], runtime_contract):
        assert self.validator.validate(data_1, data_2, runtime_contract) == data_1[0]
    
    @pytest.mark.usefixtures("arch_arm_setter")
    def test_runtime_arch_mismatch(self, data_1:List[Runtime], data_2:List[Runtime], runtime_contract):
        mock_contract = RuntimeContractViolation(
            Contexts.RUNTIME_CONTEXT,
            Bundle(
                state= { Errors.KEY_RUNTIMES_1 : data_1 }
            )
        )
        with pytest.raises(ValueError,
                           match=re.escape(
                               mock_contract.missing_error_handler(Errors.COLLECTIONS_MESSAGES)
                           )
        ):
            assert self.validator.validate(data_1, data_2, runtime_contract) is None