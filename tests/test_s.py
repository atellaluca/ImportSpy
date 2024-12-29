import pytest
import inspect
from types import ModuleType
from importspy import Spy
from importspy.errors import Errors
from examples.plugin_based_architecture.plugin_interface import Plugin
from importspy.models import SpyModel
from typing import List
import logging

logger = logging.getLogger("/".join(__file__.split('/')[-1:]))
logger.addHandler(logging.NullHandler())

class PluginSpy(SpyModel):
    superclasses: List[str] = ['Plugin']

class EnvSpy(SpyModel):
    env_vars: dict = {"CI": "true", "GITHUB_ACTIONS": "true"}
    
def condition(module: ModuleType):
    for class_name, class_obj in inspect.getmembers(module, inspect.isclass):
        if issubclass(class_obj, Plugin) and class_obj is not Plugin:
            return True
    return False

class TestSpy:
    
    def test_importspy(self, spy_instance, mock_import_functions):
        imported_module = spy_instance.importspy()
        assert imported_module.__name__ == 'mock_module'

    def test_importspy_recursion_error(self, spy_instance, monkeypatch):
        monkeypatch.setattr('inspect.stack', lambda: [
            inspect.FrameInfo(None, 'same_file.py', 1, None, None, None),
            inspect.FrameInfo(None, 'same_file.py', 1, None, None, None)
        ])

        with pytest.raises(ValueError) as excinfo:
            spy_instance.importspy()

        assert str(excinfo.value) == Errors.ANALYSIS_RECURSION_WARNING
