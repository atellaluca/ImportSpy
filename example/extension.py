import package
from plugin_interface import Plugin

class Extension(Plugin):
    
    def add_extension(self):
        print("Extension has added")
    
    def remove_extension(self):
        print("Extension has removed")
    
    def http_get_request(self):
        print("done")

class Foo:

    def get_bar(self):
        print("Foobar")