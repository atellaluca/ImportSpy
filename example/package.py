from importspy import Spy
from importspy.models import SpyModel, ClassModel
from importspy.utils import spy_model_utils
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

caller_module = Spy().importspy(spymodel=PluginSpy)

caller_module.Foo().get_bar()