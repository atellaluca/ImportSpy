"""
Defines interfaces and implementations for handling **import contracts** —  
external YAML files used by ImportSpy to validate the structure and runtime expectations  
of dynamically loaded Python modules.

Currently, only YAML is supported, but the architecture is extensible via the `Parser` interface.

All file I/O operations are wrapped in `handle_persistence_error`, ensuring clear error  
messages in case of missing, malformed, or inaccessible contract files.
"""

from abc import ABC, abstractmethod
from ruamel.yaml import YAML
import functools


class Parser(ABC):
    """
    Abstract base class for import contract parsers.

    Parsers are responsible for loading and saving `.yml` contract files that define
    a module’s structural and runtime expectations. This abstraction enables future
    support for additional formats (e.g., JSON, TOML).

    Subclasses must implement `save()` and `load()`.
    """

    @abstractmethod
    def save(self, data: dict, filepath: str):
        """
        Serializes the contract (as a dictionary) and writes it to disk.

        Parameters:
        -----------

        data : dict
            Dictionary containing the contract structure.

        filepath : str
            Target path for saving the contract (typically `.yml`).
        """
        pass

    @abstractmethod
    def load(self, filepath: str) -> dict:
        """
        Parses a contract file and returns it as a dictionary.

        Parameters:
        -----------

        filepath : str
            Path to the contract file on disk.

        Returns:
        --------

        dict
            Parsed contract data.
        """
        pass


class PersistenceError(Exception):
    """
    Raised when contract loading or saving fails due to I/O or syntax issues.

    This exception wraps low-level errors and provides human-readable feedback.
    """

    def __init__(self, msg: str):
        """
        Initialize the error with a descriptive message.

        Parameters:
        -----------

        msg : str
            Explanation of the failure.
        """
        super().__init__(msg)


def handle_persistence_error(func):
    """
    Decorator for wrapping parser I/O methods with user-friendly error handling.

    Catches all exceptions and raises a `PersistenceError` with a generic message.
    This ensures ImportSpy fails gracefully if a contract file is missing,
    malformed, or inaccessible.

    Parameters:
    -----------
    func : Callable
        The I/O method to wrap.

    Returns:
    --------

    Callable
        A wrapped version that raises `PersistenceError` on failure.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            raise PersistenceError(
                "An error occurred while handling the import contract. "
                "Please check the file path, format, or permissions."
            )
    return wrapper


class YamlParser(Parser):
    """
    YAML-based contract parser implementation.

    Uses `ruamel.yaml` to read and write `.yml` files that define import contracts.  
    Preserves formatting, indentation, and quotes for consistent serialization.
    """

    def __init__(self):
        """
        Initializes the YAML parser and configures output formatting.
        """
        self.yaml = YAML()
        self._yml_configuration()

    def _yml_configuration(self):
        """
        Applies formatting rules to YAML output:

        - Disables flow style
        - Sets consistent indentation
        - Preserves quotes in strings
        """
        self.yaml.default_flow_style = False
        self.yaml.indent(mapping=2, sequence=4, offset=2)
        self.yaml.preserve_quotes = True

    @handle_persistence_error
    def save(self, data: dict, filepath: str):
        """
        Saves a contract dictionary to a `.yml` file.

        Parameters:
        -----------

        data : dict
            Contract structure.

        filepath : str
            Destination file path.
        """
        with open(filepath, "w") as file:
            self.yaml.dump(data, file)

    @handle_persistence_error
    def load(self, filepath: str) -> dict:
        """
        Loads and parses a `.yml` contract into a Python dictionary.

        Parameters:
        -----------
        
        filepath : str
            Path to the contract file.

        Returns:
        --------
        dict
            Parsed contract structure.
        """
        with open(filepath) as file:
            data = self.yaml.load(file)
            return dict(data)
