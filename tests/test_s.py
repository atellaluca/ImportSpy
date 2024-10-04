import pytest
import inspect
from types import ModuleType
from importspy.errors import Errors
from example.plugin_interface import Plugin

def condition(module: ModuleType):
    for class_name, class_obj in inspect.getmembers(module, inspect.isclass):
        if issubclass(class_obj, Plugin) and class_obj is not Plugin:
            return True
    return False

class TestSpy:
    
    def test_find_imported_module_without_validation(self, spy_instance, mock_import_functions):
        imported_module = spy_instance.find_imported_module()
        assert imported_module.__name__ == 'mock_module'

    def test_find_imported_module_with_plugin_validation(self, spy_instance, mock_import_functions):
        imported_module = spy_instance.find_imported_module(condition)
        assert imported_module.__name__ == 'mock_module'
 
    def test_find_imported_module_no_plugin(self, spy_instance, mock_import_no_plugin):
        imported_module = spy_instance.find_imported_module(condition)
        assert imported_module is None

    def test_find_imported_module_recursion_error(self, spy_instance, monkeypatch):
        monkeypatch.setattr('inspect.stack', lambda: [
            inspect.FrameInfo(None, 'same_file.py', 1, None, None, None),
            inspect.FrameInfo(None, 'same_file.py', 1, None, None, None)
        ])

        with pytest.raises(ValueError) as excinfo:
            spy_instance.find_imported_module()

        assert str(excinfo.value) == Errors.ANALYSIS_RECURSION_WARNING
