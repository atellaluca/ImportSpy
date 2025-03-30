from abc import ABC, abstractmethod
from ruamel.yaml import YAML
import functools

class Parser(ABC):

    @abstractmethod
    def save(self, data:dict, filepath:str):
        pass

    @abstractmethod
    def load(self, filepath:str) -> dict:
        pass

class PersistenceError(Exception):

    def __init__(self, msg:str):
        super().__init__(msg)

def handle_persistence_error(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            PersistenceError("An error occurred while handling data persistence. Please check the file path, format, or permissions.")
    return wrapper

class YamlParser(Parser):

    def __init__(self):
        self.yaml = YAML()
        self._yml_configuration()

    def _yml_configuration(self):
        self.yaml.default_flow_style = False
        self.yaml.indent(mapping=2, sequence=4, offset=2)
        self.yaml.preserve_quotes = True  

    @handle_persistence_error
    def save(self, data:dict, filepath:str):
        with open(filepath, "w") as file:
            self.yaml.dump(data, file)

    @handle_persistence_error
    def load(self, filepath:str) -> dict:
        with open(filepath) as file:
            data = self.yaml.load(file)
            data = dict(data)
            return data

