from plugin_interface import Plugin

author = "Luca Atella"

plugin_name = "plugin name"
plugin_description = "plugin description"

engine = "docker"

class Extension(Plugin):

    extension_name = "extension_value"

    def __init__(self) -> None:
        self.extension_instance_name = "extension_instance_value"
    
    def add_extension(self, msg:str) -> str:
        print(msg)
        return "Extension has added"
    
    def remove_extension(self):
        print("Extension has removed")
    
    def http_get_request(self):
        print("done")

class Foo:

    def get_bar(self):
        print("Foobar")