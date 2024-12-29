from importspy import Spy
from importspy.models import SpyModel, ClassModel, SpyArchModule
from importspy.constants import Constants
from typing import List

class PluginSpy(SpyModel):
    spies: List[SpyArchModule] = [
        SpyArchModule(
            arch=Constants.ARCH_x86_64,
            module=SpyModel(
                variables={
                    "engine":"docker"
                }
            ))
    ]
    variables: dict = {"plugin_name":"plugin name", "plugin_description":"plugin description"}
    classes: List[ClassModel] = [
        ClassModel(
            name="Extension",
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