"""
importspy.constants
====================

Central repository of internal constants for ImportSpy.

This module defines the `Constants` class, which provides all hardcoded values
used throughout the validation engine. These include supported architectures,
operating systems, annotation types, and structural metadata keys.

Unlike the `Config` class — which is dynamic and environment-aware —  
`Constants` acts as a fixed baseline of what ImportSpy considers valid and supported.

By consolidating these values in one place:
- Validation becomes more consistent and predictable.
- Runtime errors due to unsupported types are easier to detect and debug.
- Import contracts can be matched against a known, canonical source of truth.

These constants are particularly useful when defining or validating `.yml` import contracts.
"""

from .config import Config


class Constants:
    """
    Constants used internally by ImportSpy’s validation engine.

    This class includes:
    - Lists of supported architectures, OS, and Python interpreters.
    - Types of class attributes ImportSpy recognizes.
    - Allowed annotations for arguments, functions, and variables.
    - Metadata keys used during model extraction and comparison.

    Attributes:
    -----------
    KNOWN_ARCHITECTURES : list[str]
        Architectures supported in the `deployments` section of import contracts.

    SUPPORTED_OS : list[str]
        Operating systems considered valid during runtime validation.

    SUPPORTED_PYTHON_IMPLEMENTATION : list[str]
        Accepted Python interpreters (e.g., CPython, PyPy, Jython).

    SUPPORTED_CLASS_ATTRIBUTE_TYPES : list[str]
        Distinguishes between `class` and `instance` attribute levels.

    SUPPORTED_ANNOTATIONS : list[str]
        Set of annotation types supported by ImportSpy.

    NAME : str
        Metadata key for a named entity (e.g., class name, function name).

    VALUE : str
        Metadata key representing a literal value in import contracts.

    CLASS_TYPE : str
        String identifier for class-level attributes (`class`).

    INSTANCE_TYPE : str
        String identifier for instance-level attributes (`instance`).

    LOG_MESSAGE_TEMPLATE : str
        Template used to standardize logging output.

    Example:
    --------
    .. code-block:: python

        from importspy.constants import Constants

        if arch not in Constants.KNOWN_ARCHITECTURES:
            raise ValueError(f"Unsupported architecture: {arch}")

        if annotation not in Constants.SUPPORTED_ANNOTATIONS:
            raise ValueError(f"Unsupported type: {annotation}")
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
