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