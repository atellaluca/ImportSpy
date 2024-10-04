import pytest
import inspect
import importlib.util
from types import ModuleType
from importspy import Spy
from example.plugin_interface import Plugin
@pytest.fixture
def spy_instance():
    return Spy()

@pytest.fixture
def mock_import_functions(monkeypatch):
    def mock_stack():
        return [
            inspect.FrameInfo(None, 'package.py', 1, None, None, None),
            inspect.FrameInfo(None, 's.py', 1, None, None, None),
            inspect.FrameInfo(None, 'extensions.py', 1, None, None, None),  
            
        ]
    
    monkeypatch.setattr(inspect, 'stack', mock_stack)

    def mock_getmodule(frame):
        mock_module = ModuleType('mock_module')
        mock_module.__file__ = 'extensions.py'
        return mock_module

    monkeypatch.setattr(inspect, 'getmodule', mock_getmodule)

    def mock_spec_from_file_location(name, location):
        class MockLoader:
            def exec_module(self, module):
                pass
        class MockSpec:
            loader = MockLoader()
        return MockSpec()

    monkeypatch.setattr(importlib.util, 'spec_from_file_location', mock_spec_from_file_location)

    def mock_module_from_spec(spec):
        mock_module = ModuleType('mock_module')
        class MyPlugin(Plugin):
            pass
        setattr(mock_module, 'MyPlugin', MyPlugin)
        return mock_module

    monkeypatch.setattr(importlib.util, 'module_from_spec', mock_module_from_spec)

@pytest.fixture
def mock_import_no_plugin(monkeypatch):
    def mock_stack():
        return [
            inspect.FrameInfo(None, 'package.py', 1, None, None, None),
            inspect.FrameInfo(None, 's.py', 1, None, None, None),
            inspect.FrameInfo(None, 'extensions.py', 1, None, None, None),  
            
        ]
    
    monkeypatch.setattr(inspect, 'stack', mock_stack)

    def mock_getmodule(frame):
        mock_module = ModuleType('mock_module')
        mock_module.__file__ = 'extensions.py'
        return mock_module

    monkeypatch.setattr(inspect, 'getmodule', mock_getmodule)

    def mock_spec_from_file_location(name, location):
        class MockLoader:
            def exec_module(self, module):
                pass
        class MockSpec:
            loader = MockLoader()
        return MockSpec()

    monkeypatch.setattr(importlib.util, 'spec_from_file_location', mock_spec_from_file_location)

    def mock_module_from_spec(spec):
        mock_module = ModuleType('mock_module')
        mock_module.__file__ = 'extensions.py'
        return mock_module

    monkeypatch.setattr(importlib.util, 'module_from_spec', mock_module_from_spec)