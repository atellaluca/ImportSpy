import pytest
from importspy.models import (
    System
)
from importspy.config import Config
from importspy.constants import Constants
from importspy.validators.system_validator import SystemValidator
from importspy.errors import Errors
import re
from typing import List

class TestSystemValidator:

    validator = SystemValidator()

    @pytest.fixture
    def data_1(self):
        return [System(
            os=Config.OS_LINUX,
            envs={"CI": "true"},
            pythons=[]
        )]
    
    @pytest.fixture
    def data_2(self):
        return [System(
            os=Config.OS_LINUX,
            pythons=[]
        )]
    
    @pytest.fixture
    def os_windows_setter(self, data_1:List[System]):
        data_1[0].os = Config.OS_WINDOWS
    
    @pytest.fixture
    def envs_setter(self, data_2):
        data_2[0].envs = {"CI": "true"}

    @pytest.mark.usefixtures("envs_setter")
    def test_system_os_match(self, data_1:List[System], data_2:List[System]):
        assert self.validator.validate(data_1, data_2) is None
    
    def test_system_os_match_2(self, data_1:List[System], data_2:List[System]):
        assert self.validator.validate(data_2, data_1) is None

    def test_system_os_invalid(self):
        with pytest.raises(ValueError,
                           match=re.escape(Errors.INVALID_OS.format(Constants.SUPPORTED_OS, "A invalid value"))):
            System(
                os="A invalid value",
                pythons=[]
            )
    
    def test_system_os_mismatch(self, data_1:List[System], data_2:List[System]):
        with pytest.raises(
            ValueError,
            match=re.escape(
                Errors.ENV_VAR_MISSING.format(data_1[0].envs)
            )
        ):
            self.validator.validate(data_1, data_2)

    @pytest.mark.usefixtures("os_windows_setter")
    def test_system_os_mismatch_1(self, data_1:List[System], data_2:List[System]):
        assert self.validator.validate(data_1, data_2) is None
    
    def test_system_mismatch(self, data_2:List[System]):
        assert self.validator.validate(None, data_2) is None
    
    def test_system_mismatch_1(self, data_2:List[System]):
        with pytest.raises(
            ValueError,
            match=re.escape(Errors.ELEMENT_MISSING.format(data_2))
        ):
            self.validator.validate(data_2, None)