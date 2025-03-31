from abc import ABC, abstractmethod
from ruamel.yaml import YAML
import functools

class Parser(ABC):
    """
    Abstract base class for data persistence strategies.

    Implementations of this interface must provide methods for saving and 
    loading Python dictionaries from and to external file formats.
    """

    @abstractmethod
    def save(self, data: dict, filepath: str):
        """
        Persists a dictionary to a specified file path.

        Parameters:
        -----------
        data : dict
            The data to be serialized.

        filepath : str
            The target file path where data should be saved.
        """
        pass

    @abstractmethod
    def load(self, filepath: str) -> dict:
        """
        Loads and deserializes data from a file into a Python dictionary.

        Parameters:
        -----------
        filepath : str
            Path to the file containing serialized data.

        Returns:
        --------
        dict
            The deserialized content.
        """
        pass


class PersistenceError(Exception):
    """
    Custom exception for errors related to data persistence.
    """

    def __init__(self, msg: str):
        """
        Initializes the `PersistenceError`.

        Parameters:
        -----------
        msg : str
            Description of the error.
        """
        super().__init__(msg)


def handle_persistence_error(func):
    """
    Decorator to catch and raise a `PersistenceError` when persistence operations fail.

    Parameters:
    -----------
    func : Callable
        The function to wrap.

    Returns:
    --------
    Callable
        The wrapped function with error handling.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            raise PersistenceError("An error occurred while handling data persistence. "
                                   "Please check the file path, format, or permissions.")
    return wrapper


class YamlParser(Parser):
    """
    YAML-based implementation of the `Parser` interface.

    Provides methods to serialize and deserialize Python dictionaries
    using the YAML format with custom formatting preferences.
    """

    def __init__(self):
        """
        Initializes the YAML parser and sets custom formatting options.
        """
        self.yaml = YAML()
        self._yml_configuration()

    def _yml_configuration(self):
        """
        Applies default configuration to the YAML serializer:
        - Disables flow style
        - Sets indentation for mapping and sequences
        - Preserves quotes
        """
        self.yaml.default_flow_style = False
        self.yaml.indent(mapping=2, sequence=4, offset=2)
        self.yaml.preserve_quotes = True  

    @handle_persistence_error
    def save(self, data: dict, filepath: str):
        """
        Saves a dictionary to a YAML file.

        Parameters:
        -----------
        data : dict
            The data to save.

        filepath : str
            Path to the output YAML file.
        """
        with open(filepath, "w") as file:
            self.yaml.dump(data, file)

    @handle_persistence_error
    def load(self, filepath: str) -> dict:
        """
        Loads a dictionary from a YAML file.

        Parameters:
        -----------
        filepath : str
            Path to the input YAML file.

        Returns:
        --------
        dict
            The loaded data.
        """
        with open(filepath) as file:
            data = self.yaml.load(file)
            return dict(data)
