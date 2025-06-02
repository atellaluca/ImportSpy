import pytest
from importspy.models import (
    Python
)
from importspy.config import Config
from importspy.constants import Errors
from importspy.validators import PythonValidator
from typing import List
import re


class TestPythonValidator:

    validator = PythonValidator()

    @pytest.fixture
    def data_1(self):
        return [Python(
            version="3.13.9",
            modules=[]
        )]
    
    @pytest.fixture
    def data_2(self):
        return [Python(
            modules=[]
        )]
    
    @pytest.fixture
    def data_3(self):
        return [Python(
            interpreter=Config.INTERPRETER_IRON_PYTHON,
            modules=[]
        )]
    
    @pytest.fixture
    def data_4(self):
        return [Python(
            interpreter=Config.INTERPRETER_IRON_PYTHON,
            modules=[]
        )]
    
    @pytest.fixture
    def python_version_setter(self, data_2:List[Python]):
        data_2[0].version = "12.0.1"
    
    @pytest.fixture
    def python_interpreter_setter(self, data_3:List[Python]):
        data_3[0].interpreter = Config.INTERPRETER_GRAALPYTHON

    @pytest.mark.usefixtures("python_version_setter")
    def test_python_match(self, data_1:List[Python], data_2:List[Python]):
        assert self.validator.validate(data_1, data_2) is None

    def test_python_match_1(self, data_3:List[Python], data_4:List[Python]):
        assert self.validator.validate(data_3, data_4) is None
    
    def test_python_mismatch(self, data_2:List[Python]):
        assert self.validator.validate(None, data_2) is None

    @pytest.mark.usefixtures("python_interpreter_setter")
    def test_python_mismatch_1(self, data_3, data_4):
        assert self.validator.validate(data_4, data_3) is None
    
    def test_python_mismatch_2(self):
        assert self.validator.validate(None, None) is None
    
    def test_python_mismatch_3(self):
        assert self.validator.validate(None, None) is None
    
    def test_python_mismatch_4(self, data_2:List[Python]):
        assert self.validator.validate(None, data_2) is None
    
    def test_python_mismatch_5(self, data_3:List[Python]):
        with pytest.raises(
            ValueError,
            match=re.escape(
                    Errors.ELEMENT_MISSING.format(data_3)
                )
        ):
            self.validator.validate(data_3, None)