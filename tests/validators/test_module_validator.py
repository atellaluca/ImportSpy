import pytest
from importspy import (
    Module
)
from importspy.validators.module_validator import ModuleValidator
from importspy.errors import Errors
import re
from typing import List

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
    def filename_setter(self, data_1:List[Module]):
        data_1[0].filename="package.py"

    
    @pytest.fixture
    def version_unsetter(self, data_2:List[Module]):
        data_2[0].version=None

    @pytest.fixture
    def variables_setter(self, data_2:List[Module]):
        data_2[0].variables={
            "attempt":4,
            "msg": "Hi!" 
        }

    @pytest.fixture
    def data_3(self):
        return [Module(
            filename="package.py",
            version="0.1.0",
            variables={
                "attempt":4,
                "msg": "Hello!" 
            }
        )]
    
    @pytest.fixture
    def variables_msg_setter(self, data_3:List[Module]):
        data_3[0].variables['msg'] = "Hi!"

    @pytest.mark.usefixtures("filename_setter")
    @pytest.mark.usefixtures("version_unsetter")
    def test_module_match(self, data_1:List[Module], data_2:List[Module]):
        assert self.validator.validate(data_1, data_2[0]) is None

    @pytest.mark.usefixtures("filename_setter")
    @pytest.mark.usefixtures("variables_setter")
    @pytest.mark.usefixtures("variables_msg_setter")
    def test_module_match_1(self, data_2:List[Module], data_3:List[Module]):
        assert self.validator.validate(data_2, data_3[0]) is None
    
    def test_module_match_2(self, data_2:List[Module], data_3:List[Module]):
        assert self.validator.validate(data_2, data_3[0]) is None
    
    def test_module_mismatch(self, data_2:List[Module]):
        assert self.validator.validate(None, data_2[0]) is None

    def test_module_mismatch_2(self, data_2:List[Module], data_3:List[Module]):
        with pytest.raises(
            ValueError,
            match=Errors.VAR_MISSING.format(data_3[0].variables)
        ):
            self.validator.validate(data_3, data_2[0])
    
    @pytest.mark.usefixtures("version_unsetter")
    def test_module_mismatch_3(self, data_1:List[Module], data_2:List[Module]):
        with pytest.raises(ValueError,
                           match=re.escape(
                               Errors.FILENAME_MISMATCH.format(data_1[0].filename,
                                                               data_2[0].filename)
                                                               )
        ):
            self.validator.validate(data_1, data_2[0])
        
    def test_module_mismatch_4(self, data_1:List[Module], data_2:List[Module]):
        with pytest.raises(ValueError,
                           match=re.escape(
                               Errors.FILENAME_MISMATCH.format(data_1[0].filename,
                                                               data_2[0].filename)
                                                               )
        ):
            self.validator.validate(data_1, data_2[0])