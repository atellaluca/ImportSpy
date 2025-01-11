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
    Class,
    Attribute
    )

from typing import List

__version__ = None

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
                ),
                Runtime(
                    arch=Constants.ARCH_ARM64,
                    systems=[
                        System(
                            os=Constants.OS_MACOS
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
            attributes=[
                Attribute(
                    type=Constants.INSTANCE_TYPE,
                    name="extension_instance_name",
                    value="extension_instance_value"
                ),
                Attribute(
                    type=Constants.CLASS_TYPE,
                    name="extension_name",
                    value="extension_value"
                )
            ],
            methods=["__init__", "add_extension", "remove_extension", "http_get_request"],
            superclasses=["Plugin"]
        ),
        Class(
            name="Foo",
            methods=["get_bar"],
        )]
    filename: str = "extension.py"

caller_module = Spy().importspy(spymodel=PluginSpy)

caller_module.Foo().get_bar()