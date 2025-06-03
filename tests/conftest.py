import pytest

from importspy.violation_systems import Bundle

from importspy.constants import (
    Errors,
    Contexts
)

@pytest.fixture
def modulebundle() -> Bundle:
    bundle = Bundle()
    bundle[Errors.KEY_FILE_NAME] = "testmodule.py"
    bundle[Errors.KEY_MODULE_VERSION] = "0.1.0"
    return bundle

@pytest.fixture
def classbundle(modulebundle) -> Bundle:
    modulebundle[Errors.KEY_CLASS_NAME] = "TestClass"
    return modulebundle

@pytest.fixture
def functionbundle(modulebundle) -> Bundle:
    modulebundle[Errors.FUNCTIONS_DINAMIC_PAYLOAD[Errors.ENTITY_MESSAGES][Contexts.MODULE_CONTEXT]] = "test_function"
    return modulebundle

@pytest.fixture
def methodbundle(classbundle) -> Bundle:
    classbundle[Errors.FUNCTIONS_DINAMIC_PAYLOAD[Errors.ENTITY_MESSAGES][Contexts.CLASS_CONTEXT]] = "test_method"
    return classbundle