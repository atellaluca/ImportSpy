from importspy import (
    Spy,
    Config
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
                    arch=Config.ARCH_x86_64,
                    systems=[
                        System(
                            os=Config.OS_LINUX
                        )
                    ]
                ),
                Runtime(
                    arch=Config.ARCH_ARM64,
                    systems=[
                        System(
                            os=Config.OS_MACOS
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
                    type=Config.INSTANCE_TYPE,
                    name="extension_instance_name",
                    value="extension_instance_value"
                ),
                Attribute(
                    type=Config.CLASS_TYPE,
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