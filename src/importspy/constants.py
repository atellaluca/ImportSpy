from .config import Config

"""
Constants Module for ImportSpy

This module defines the `Constants` class, which serves as a centralized repository for 
predefined values and configurations used across the ImportSpy framework. By consolidating 
these constants, the module ensures consistency and maintainability while facilitating 
multi-environment and multi-architecture compatibility.

The constants include supported architectures, operating systems, Python implementations, 
class attribute types, annotations, and other runtime-specific configurations.

This module complements the `Config` module by segregating internally used constants 
from those meant for external configuration.
"""

class Constants:
    """
    Centralized Repository for Internal Constants in ImportSpy.

    The `Constants` class provides a predefined set of values to standardize and simplify 
    runtime checks, validations, and configurations. It encapsulates all constants needed 
    internally within the ImportSpy framework, differentiating them from user-configurable 
    settings in the `Config` class.

    Features:
    ---------
    - **Architectural Compatibility**: Lists known architectures and supported operating systems.
    - **Python Implementation Support**: Defines a range of supported Python interpreters.
    - **Class and Annotation Types**: Specifies supported class attribute types and annotations.
    - **Internal Metadata**: Includes constants for metadata keys (e.g., `NAME`, `VALUE`).

    Attributes:
    -----------
    KNOWN_ARCHITECTURES : list[str]
        List of known architectures supported by ImportSpy.
    SUPPORTED_OS : list[str]
        List of operating systems supported by ImportSpy.
    SUPPORTED_PYTHON_IMPLEMENTATION : list[str]
        Supported Python implementations.
    SUPPORTED_CLASS_ATTRIBUTE_TYPES : list[str]
        Types of class attributes recognized by ImportSpy.
    SUPPORTED_ANNOTATIONS : list[str]
        Supported annotations for functions, arguments, and variables.
    NAME : str
        Key representing the name of an entity.
    VALUE : str
        Key representing the value of an entity.
    CLASS_TYPE : str
        Type identifier for class-level attributes.
    INSTANCE_TYPE : str
        Type identifier for instance-level attributes.
    LOG_MESSAGE_TEMPLATE : str
        Standardized log message template.

    Example Usage:
    --------------
    .. code-block:: python

        from importspy.constants import Constants

        if runtime.arch not in Constants.KNOWN_ARCHITECTURES:
            raise ValueError(f"Unsupported architecture: {runtime.arch}")
    """
    
    KNOWN_ARCHITECTURES = [
        Config.ARCH_x86_64, 
        Config.ARCH_AARCH64, 
        Config.ARCH_ARM, 
        Config.ARCH_ARM64, 
        Config.ARCH_I386, 
        Config.ARCH_PPC64, 
        Config.ARCH_PPC64LE, 
        Config.ARCH_S390X
    ]

    SUPPORTED_OS = [
        Config.OS_WINDOWS,
        Config.OS_LINUX, 
        Config.OS_MACOS
    ]

    SUPPORTED_PYTHON_IMPLEMENTATION = [
        Config.INTERPRETER_CPYTHON,
        Config.INTERPRETER_PYPY,
        Config.INTERPRETER_JYTHON,
        Config.INTERPRETER_IRON_PYTHON,
        Config.INTERPRETER_MICROPYTHON,
        Config.INTERPRETER_BRYTHON,
        Config.INTERPRETER_PYSTON,
        Config.INTERPRETER_GRAALPYTHON,
        Config.INTERPRETER_RUSTPYTHON,
        Config.INTERPRETER_NUITKA,
        Config.INTERPRETER_TRANSCRYPT
    ]
    
    SUPPORTED_CLASS_ATTRIBUTE_TYPES = [
        Config.CLASS_TYPE,
        Config.INSTANCE_TYPE
    ]

    NAME = "Name"
    VALUE = "Value"
    ANNOTATION = "Annotation"

    CLASS_TYPE = Config.CLASS_TYPE
    INSTANCE_TYPE = Config.INSTANCE_TYPE

    SUPPORTED_ANNOTATIONS = [
        Config.ANNOTATION_INT,
        Config.ANNOTATION_FLOAT,
        Config.ANNOTATION_STR,
        Config.ANNOTATION_BOOL,
        Config.ANNOTATION_LIST,
        Config.ANNOTATION_DICT,
        Config.ANNOTATION_TUPLE,
        Config.ANNOTATION_SET,
        Config.ANNOTATION_OPTIONAL,
        Config.ANNOTATION_UNION,
        Config.ANNOTATION_ANY,
        Config.ANNOTATION_CALLABLE,
        Config.ANNOTATION_LIST,
        Config.ANNOTATION_DICT,
        Config.ANNOTATION_TUPLE
    ]

    LOG_MESSAGE_TEMPLATE = (
        "[Operation: {operation}] [Status: {status}] "
        "[Details: {details}]"
    )
