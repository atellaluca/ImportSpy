import pytest
from importspy import (
    Module,
    Config
)
from importspy.validators.module_validator import ModuleValidator
from importspy.errors import Errors
import re

class TestModuleValidator:
    
    validator = ModuleValidator()

    @pytest.fixture
    def data_1(self):
        return Module(
            filename="module.py",
        )
    
    @pytest.fixture
    def data_2(self):
        return Module(
            filename="package.py",
            version="0.1.0"
        )
    
    @pytest.fixture
    def filename_setter(self, data_1):
        data_1.filename="package.py"

    
    @pytest.fixture
    def version_unsetter(self, data_2):
        data_2.version=None

    @pytest.fixture
    def variables_setter(self, data_2:Module):
        data_2.variables={
            "attempt":4,
            "msg": "Hi!" 
        }

    @pytest.fixture
    def data_3(self):
        return Module(
            filename="package.py",
            version="0.1.0",
            variables={
                "attempt":4,
                "msg": "Hello!" 
            }
        )
    
    @pytest.fixture
    def variables_msg_setter(self, data_3:Module):
        data_3.variables['msg'] = "Hi!"

    @pytest.mark.usefixtures("filename_setter")
    @pytest.mark.usefixtures("version_unsetter")
    def test_module_match(self, data_1:Module, data_2:Module):
        assert self.validator.validate(data_1, data_2)

    @pytest.mark.usefixtures("filename_setter")
    @pytest.mark.usefixtures("variables_setter")
    @pytest.mark.usefixtures("variables_msg_setter")
    def test_module_match_1(self, data_2:Module, data_3:Module):
        assert self.validator.validate(data_2, data_3)
    
    def test_module_match_2(self, data_2, data_3):
        assert self.validator.validate(data_2, data_3)
    
    def test_module_mismatch(self, data_2:Module):
        assert self.validator.validate(None, data_2) is None

    def test_module_mismatch_2(self, data_2, data_3):
        with pytest.raises(
            ValueError,
            match=Errors.VAR_MISSING.format(data_3.variables)
        ):
            self.validator.validate(data_3, data_2)
    
    @pytest.mark.usefixtures("version_unsetter")
    def test_module_mismatch_3(self, data_1:Module, data_2:Module):
        with pytest.raises(ValueError,
                           match=re.escape(
                               Errors.FILENAME_MISMATCH.format(data_1.filename,
                                                               data_2.filename)
                                                               )
        ):
            self.validator.validate(data_1, data_2)
        
    def test_module_mismatch_4(self, data_1, data_2):
        with pytest.raises(ValueError,
                           match=re.escape(
                               Errors.FILENAME_MISMATCH.format(data_1.filename,
                                                               data_2.filename)
                                                               )
        ):
            self.validator.validate(data_1, data_2)