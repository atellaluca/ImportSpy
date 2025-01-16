from importspy import (
    Spy,
    Config
)
from importspy.models import (
    SpyModel,
    Runtime,
    System,
    Python,
    Module,
    Class,
    Attribute,
    Function,
    Argument
    )

from typing import List

__version__ = None

class PluginSpy(SpyModel):
    filename: str = "extension.py"
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
            methods=[
                Function(
                    name="__init__",
                    arguments=[
                        Argument(
                             name="self"
                        )
                    ]
                ),
                Function(
                    name="add_extension",
                    arguments=[
                        Argument(
                            name="self"
                        ),
                        Argument(
                            name="msg",
                            annotation="str",
                        ),
                    ],
                    return_annotation="str"
                ),
                Function(
                    name="remove_extension",
                    arguments=[
                        Argument(
                            name="self"
                        )
                    ]
                ),
                Function(
                    name="http_get_request",
                    arguments=[
                        Argument(
                            name="self"
                        )
                    ]
                )
            ],
            superclasses=["Plugin"]
        ),
        Class(
            name="Foo",
            methods=[
                Function(
                    name="get_bar",
                    arguments=[
                        Argument(
                            name="self"
                        )
                    ]
                    )
            ],
        )]
    filename: str = "extension.py"

caller_module = Spy().importspy(spymodel=PluginSpy)

caller_module.Foo().get_bar()