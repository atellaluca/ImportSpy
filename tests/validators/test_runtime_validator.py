import pytest
from importspy import (
    Runtime,
    Config
)
from importspy.constants import Constants
from importspy.validators.runtime_validator import RuntimeValidator
from importspy.errors import Errors
import re
from typing import List

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
    def arch_arm_setter(self, data_1:List[Runtime]):
        data_1[0].arch = Config.ARCH_ARM

    def test_runtime_arch_match(self, data_1:List[Runtime], data_2:List[Runtime]):
        assert self.validator.validate(data_1, data_2) is None

    def test_runtime_arch_invalid(self):
        with pytest.raises(ValueError,
                           match=re.escape(Errors.INVALID_ARCHITECTURE.format("A invalid value", Constants.KNOWN_ARCHITECTURES))):
            Runtime(
                arch="A invalid value",
                systems=[]
            )
    
    @pytest.mark.usefixtures("arch_arm_setter")
    def test_runtime_arch_mismatch(self, data_1:List[Runtime], data_2:List[Runtime]):
        assert self.validator.validate(data_1, data_2) is None