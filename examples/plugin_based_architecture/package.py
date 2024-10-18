from importspy import Spy
from importspy.models import SpyModel, ClassModel
from importspy.utils import spy_model_utils
from typing import List

class PluginSpy(SpyModel):
    variables: List[str] = ["plugin_name", "plugin_description"]
    classes: List[ClassModel] = [
        ClassModel(
            class_attr=["extension_name"],
            instance_attr=["extension_instance_name"],
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