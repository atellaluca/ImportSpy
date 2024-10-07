from importspy import Spy
from importspy.models import SpyModel, ClassModel
from types import ModuleType
import inspect
from plugin_interface import Plugin
from typing import List

class PluginSpy(SpyModel):
    classes: List[ClassModel] = [ClassModel(superclasses=["Plugin"])]

def condition(module: ModuleType) -> bool:
    for class_name, class_obj in inspect.getmembers(module, inspect.isclass):
        if issubclass(class_obj, Plugin) and class_obj is not Plugin:
            return True
    return False

print(Spy().importspy(validation=condition))
print(Spy().importspy(spymodel=PluginSpy))