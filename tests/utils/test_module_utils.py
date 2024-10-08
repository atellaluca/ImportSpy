import pytest
from importspy.utils import spy_module_utils
from importspy import Spy
import logging

logger = logging.getLogger("/".join(__file__.split('/')[-2:]))
logger.addHandler(logging.NullHandler())

class TestModuleUtils:

    def test_extract_version(self, spy_instance:Spy, mock_import_functions):
        module = spy_instance.importspy()
        logger.debug(f"Module loaded: {module}")
        module.__version__ = "1.0.0"
        version = spy_module_utils.extract_version(module)
        logger.debug(f"Module version: {version}")
        assert version == "1.0.0"

    def test_extract_no_version(self, spy_instance:Spy, mock_import_functions):
        module = spy_instance.importspy()
        logger.debug(f"Module loaded: {module}")
        version = spy_module_utils.extract_version(module)
        logger.debug(f"Module version: {version}")
        assert version is None

    def test_inspect_module(self, spy_instance:Spy, mock_import_functions):
        current_frame, caller_frame = spy_module_utils.inspect_module()
        logger.debug(f"current frame: {current_frame}, caller frame: {caller_frame}")
        assert current_frame != caller_frame
        logger.debug(current_frame.filename)
        assert current_frame.filename == "package.py"
        assert caller_frame.filename == "extensions.py"

    def test_get_info_module(self, spy_instance:Spy, mock_import_functions):
        current_frame, caller_frame = spy_module_utils.inspect_module()
        info_module = spy_module_utils.get_info_module(caller_frame)
        assert info_module.__file__ == "extensions.py"
    
    def test_load_module(self, spy_instance:Spy, mock_import_functions):
        current_frame, caller_frame = spy_module_utils.inspect_module()
        info_module = spy_module_utils.get_info_module(caller_frame)
        spy_module_utils.load_module(info_module)
        assert info_module.__name__ == "mock_module"
