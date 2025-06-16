import pytest
from importspy.models import (
    Python
)
from importspy.config import Config
from importspy.constants import (
    Errors,
    Contexts
)

from importspy.validators import PythonValidator
from typing import List
import re

from importspy.violation_systems import (
    PythonContractViolation,
    Bundle
)


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
    def pythonbundle(self) -> Bundle:
        bundle = Bundle()
        bundle[Errors.KEY_PYTHON_1] = Python(
            version=Config.PYTHON_VERSION_3_13,
            interpreter=Config.INTERPRETER_IRON_PYTHON,
            modules=[]
        )
        return bundle
    
    @pytest.fixture
    def python_contract(self, pythonbundle: Bundle) -> PythonContractViolation:
        return PythonContractViolation(context=Contexts.RUNTIME_CONTEXT, bundle=pythonbundle)
    
    @pytest.fixture
    def python_version_setter(self, data_2:List[Python]):
        data_2[0].version = "12.0.1"
    
    @pytest.fixture
    def python_interpreter_setter(self, data_3:List[Python]):
        data_3[0].interpreter = Config.INTERPRETER_GRAALPYTHON

    def test_python_match(self, data_3:List[Python], data_4:List[Python], python_contract):
        assert self.validator.validate(data_3, data_4, python_contract) == data_3[0].modules
    
    def test_python_mismatch(self, data_2:List[Python], python_contract):
        assert self.validator.validate(None, data_2, python_contract) is None

    @pytest.mark.usefixtures("python_interpreter_setter")
    def test_python_mismatch_1(self, data_3, data_4, python_contract):
        mock_contract = PythonContractViolation(
            Contexts.RUNTIME_CONTEXT,
            Bundle(
                state= { Errors.KEY_PYTHONS_1 : data_4 }
            )
        )
        with pytest.raises(ValueError,
                           match=re.escape(
                               mock_contract.missing_error_handler(Errors.COLLECTIONS_MESSAGES)
                           )
        ):
            assert self.validator.validate(data_4, data_3, python_contract)
    
    def test_python_mismatch_2(self, python_contract):
        assert self.validator.validate(None, None, python_contract) is None
    
    def test_python_mismatch_3(self, python_contract):
        assert self.validator.validate(None, None, python_contract) is None
    
    def test_python_mismatch_4(self, data_2:List[Python], python_contract):
        assert self.validator.validate(None, data_2, python_contract) is None
    
    def test_python_mismatch_5(self, data_3:List[Python], python_contract):
        mock_contract = PythonContractViolation(
            Contexts.RUNTIME_CONTEXT,
            Bundle(
                state= { Errors.KEY_PYTHONS_1 : data_3 }
            )
        )
        with pytest.raises(ValueError,
                           match=re.escape(
                               mock_contract.missing_error_handler(Errors.COLLECTIONS_MESSAGES)
                           )
        ):
            self.validator.validate(data_3, None, python_contract)
    
    @pytest.mark.usefixtures("python_version_setter")
    def test_python_mismatch_6(self, data_1:List[Python], data_2:List[Python], python_contract:PythonContractViolation):
        mock_contract = PythonContractViolation(
            Contexts.RUNTIME_CONTEXT,
            Bundle(
                state= { Errors.KEY_PYTHONS_1 : data_1 }
            )
        )
        with pytest.raises(ValueError,
                           match=re.escape(
                               mock_contract.missing_error_handler(Errors.COLLECTIONS_MESSAGES)
                           )
        ):
            self.validator.validate(data_1, data_2, python_contract)