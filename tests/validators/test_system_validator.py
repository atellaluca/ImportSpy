import pytest
from importspy import (
    System,
    Config
)
from importspy.constants import Constants
from importspy.validators.system_validator import SystemValidator
from importspy.errors import Errors
import re

class TestRuntimeValidator:

    validator = SystemValidator()

    @pytest.fixture
    def data_1(self):
        return System(
            os=Config.OS_LINUX,
            envs={"CI": "true"},
            pythons=[]
        )
    
    @pytest.fixture
    def data_2(self):
        return System(
            os=Config.OS_LINUX,
            pythons=[]
        )
    
    @pytest.fixture
    def os_windows_setter(self, data_1:System):
        data_1.os = Config.OS_WINDOWS
    
    @pytest.fixture
    def envs_setter(self, data_2):
        data_2.envs = {"CI": "true"}

    @pytest.mark.usefixtures("envs_setter")
    def test_system_os_match(self, data_1:System, data_2:System):
        assert self.validator.validate(data_1, data_2)

    def test_system_os_invalid(self):
        with pytest.raises(ValueError,
                           match=re.escape(Errors.INVALID_OS.format("A invalid value", Constants.SUPPORTED_OS))):
            System(
                os="A invalid value",
                pythons=[]
            )
    
    def test_system_os_mismatch(self, data_1:System, data_2:System):
        assert self.validator.validate(data_1, data_2) is False

    @pytest.mark.usefixtures("os_windows_setter")
    def test_system_os_mismatch_1(self, data_1:System, data_2:System):
        assert self.validator.validate(data_1, data_2) is False