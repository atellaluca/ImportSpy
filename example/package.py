from importspy import Spy
from importspy.models import SpyModel, ClassModel
from typing import List

class PluginSpy(SpyModel):
    classes: List[ClassModel] = [
        ClassModel(
            methods=["add_extension", "remove_extension", "http_get_request"],
            superclasses=["Plugin"]
        ),
        ClassModel(
            name="Foo",
            methods=["get_bar"]
        )]
    filename: str = "extension.py"

print(Spy().importspy(spymodel=PluginSpy))