import pytest
from importspy import (
    Python,
    Config
)
from importspy.validators.python_validator import PythonValidator


class TestRuntimeValidator:

    validator = PythonValidator()

    @pytest.fixture
    def data_1(self):
        return Python(
            version="12.0.1",
            modules=[]
        )
    
    @pytest.fixture
    def data_2(self):
        return Python(
            modules=[]
        )
    
    @pytest.fixture
    def data_3(self):
        return Python(
            interpreter=Config.INTERPRETER_IRON_PYTHON,
            modules=[]
        )
    
    @pytest.fixture
    def data_4(self):
        return Python(
            interpreter=Config.INTERPRETER_IRON_PYTHON,
            modules=[]
        )
    
    @pytest.fixture
    def python_version_setter(self, data_2:Python):
        data_2.version = "12.0.1"
    
    @pytest.fixture
    def python_interpreter_setter(self, data_3:Python):
        data_3.interpreter = Config.INTERPRETER_GRAALPYTHON

    @pytest.mark.usefixtures("python_version_setter")
    def test_python_match(self, data_1:Python, data_2:Python):
        assert self.validator.validate(data_1, data_2)

    def test_python_match_1(self, data_3:Python, data_4:Python):
        assert self.validator.validate(data_3, data_4)
    
    def test_python_mismatch(self, data_2:Python):
        assert self.validator.validate(None, data_2) is False

    @pytest.mark.usefixtures("python_interpreter_setter")
    def test_python_mismatch_1(self, data_3, data_4):
        assert self.validator.validate(data_3, data_4) is False