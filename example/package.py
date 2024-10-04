from importspy import Spy
from types import ModuleType
import inspect
from plugin_interface import Plugin

def condition(module: ModuleType) -> bool:
    for class_name, class_obj in inspect.getmembers(module, inspect.isclass):
        if issubclass(class_obj, Plugin) and class_obj is not Plugin:
            return True
    return False

print(Spy().importspy(validation=condition))