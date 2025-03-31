"""
importspy.persistences
=======================

This module defines the interfaces and implementations for handling **import contracts** —  
external YAML files used by ImportSpy to validate the structure and runtime expectations  
of dynamically loaded Python modules.

Currently, YAML is the only supported contract format, but the architecture is fully  
extensible via the `Parser` interface.

All file access operations are wrapped in safe error handling using `handle_persistence_error`,  
which raises human-readable exceptions when contract files are missing, corrupted, or unreadable.
"""

from abc import ABC, abstractmethod
from ruamel.yaml import YAML
import functools


class Parser(ABC):
    """
    Abstract interface for import contract parsers.

    A contract parser is responsible for loading and saving `.yml` files  
    that describe the expected structure of a Python module. This abstraction  
    allows ImportSpy to support multiple formats (e.g., YAML, JSON, TOML) in the future.

    Subclasses must implement both `save()` and `load()` methods.
    """

    @abstractmethod
    def save(self, data: dict, filepath: str):
        """
        Serializes the given import contract (as a Python dictionary) and writes it to a file.

        Parameters:
        -----------
        data : dict
            A dictionary representation of the import contract.

        filepath : str
            The path where the contract should be saved (usually with `.yml` extension).
        """
        pass

    @abstractmethod
    def load(self, filepath: str) -> dict:
        """
        Loads and parses an import contract from a file into a Python dictionary.

        Parameters:
        -----------
        filepath : str
            Path to the `.yml` contract file.

        Returns:
        --------
        dict
            The parsed contract as a dictionary.
        """
        pass


class PersistenceError(Exception):
    """
    Custom exception raised when there is a problem reading or writing import contracts.

    This error wraps low-level I/O or parsing issues and presents them in a way  
    that is meaningful to end users.
    """

    def __init__(self, msg: str):
        """
        Initializes the `PersistenceError`.

        Parameters:
        -----------
        msg : str
            A human-readable error message describing the failure.
        """
        super().__init__(msg)


def handle_persistence_error(func):
    """
    Decorator that wraps file I/O operations in safe error handling.

    If the decorated function raises any exception (e.g., file not found, malformed YAML),
    a `PersistenceError` is raised with a descriptive message instead.

    This helps ensure that ImportSpy fails gracefully during contract handling.

    Parameters:
    -----------
    func : Callable
        The function to decorate.

    Returns:
    --------
    Callable
        The wrapped function.
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
    YAML-based implementation of the `Parser` interface.

    This parser reads and writes import contracts from `.yml` files using the `ruamel.yaml` library.
    It preserves indentation, flow style, and quotes to ensure consistent structure across validations.
    """

    def __init__(self):
        """
        Initializes the YAML parser and applies default formatting rules for readability.
        """
        self.yaml = YAML()
        self._yml_configuration()

    def _yml_configuration(self):
        """
        Applies consistent formatting to YAML output:

        - Disables flow style for better readability
        - Sets indentation rules for mappings and sequences
        - Preserves quotes for exact string representation
        """
        self.yaml.default_flow_style = False
        self.yaml.indent(mapping=2, sequence=4, offset=2)
        self.yaml.preserve_quotes = True

    @handle_persistence_error
    def save(self, data: dict, filepath: str):
        """
        Saves an import contract to a `.yml` file.

        Parameters:
        -----------
        data : dict
            The contract content as a dictionary.

        filepath : str
            The output path where the YAML file will be saved.
        """
        with open(filepath, "w") as file:
            self.yaml.dump(data, file)

    @handle_persistence_error
    def load(self, filepath: str) -> dict:
        """
        Loads an import contract from a `.yml` file and parses it into a dictionary.

        Parameters:
        -----------
        filepath : str
            Path to the YAML file.

        Returns:
        --------
        dict
            A Python dictionary containing the contract structure.
        """
        with open(filepath) as file:
            data = self.yaml.load(file)
            return dict(data)
