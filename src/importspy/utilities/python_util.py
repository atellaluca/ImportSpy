import logging
import platform

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())
    
class PythonUtil:

    def extract_python_version(self) -> str:
        return platform.python_version()
    
    def extract_python_implementation(self) -> str:
        return platform.python_implementation()
