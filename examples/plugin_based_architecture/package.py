from importspy import (
    Spy,
    Constants
)
from importspy.models import (
    SpyModel,
    Deployment,
    Runtime,
    System,
    Python,
    Module,
    Class
    )

from typing import List

class PluginSpy(SpyModel):
    deployments: List[Deployment] = [
        Deployment(
            runtimes=[
                Runtime(
                    arch=Constants.ARCH_x86_64,
                    systems=[
                        System(
                            os=Constants.OS_LINUX
                        )
                    ]
                )
            ],
        )
    ]
    variables: dict = {"engine": "docker", "plugin_name":"plugin name", "plugin_description":"plugin description"}
    classes: List[Class] = [
        Class(
            name="Extension",
            class_attr=["extension_name"],
            instance_attr=["extension_instance_name"],
            methods=["add_extension", "remove_extension", "http_get_request"],
            superclasses=["Plugin"]
        ),
        Class(
            name="Foo",
            methods=["get_bar"]
        )]
    filename: str = "extension.py"

caller_module = Spy().importspy(spymodel=PluginSpy)

caller_module.Foo().get_bar()