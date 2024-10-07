from importspy import Spy
from importspy.models import SpyModel, ClassModel
from typing import List

class PluginSpy(SpyModel):
    classes: List[ClassModel] = [ClassModel(superclasses=["Plugin"])]

print(Spy().importspy(spymodel=PluginSpy))