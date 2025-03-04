"""
Configuration Constants for External Usage in ImportSpy

This module defines the `Config` class, which encapsulates constants intended for external 
configuration by developers integrating ImportSpy into their projects. It separates externally 
modifiable settings from internal constants to provide a clear distinction and enhance usability.

The `Config` class includes constants for:
- Supported system architectures.
- Compatible operating systems.
- Supported Python interpreters.
- Valid annotation types for function arguments and return values.

These constants ensure compatibility and flexibility across different environments.
"""

class Config:
    """
    Developer Configuration for ImportSpy.

    The `Config` class provides a structured collection of constants designed to be configurable 
    by developers integrating ImportSpy. These constants define supported architectures, operating 
    systems, Python interpreters, and annotation types, allowing users to adapt ImportSpy to their 
    specific runtime and validation requirements.

    Features:
    ---------
    - **Architecture Support**: Defines constants for commonly used system architectures.
    - **Operating System Compatibility**: Lists supported operating systems.
    - **Python Interpreter Support**: Includes major Python interpreters, from CPython to Nuitka.
    - **Annotation Types**: Enumerates valid annotation types for arguments, variables, and return values.

    Attributes:
    -----------
    KNOWN_ARCHITECTURES : list[str]
        List of supported system architectures.
    SUPPORTED_OS : list[str]
        List of supported operating systems.
    SUPPORTED_PYTHON_INTERPRETERS : list[str]
        List of supported Python interpreter types.
    SUPPORTED_CLASS_ATTRIBUTE_TYPES : list[str]
        Recognized types for class attributes.
    SUPPORTED_ANNOTATIONS : list[str]
        Valid annotation types for functions, arguments, and return values.

    Example Usage:
    --------------
    .. code-block:: python

        from importspy.config import Config

        if runtime.arch not in Config.KNOWN_ARCHITECTURES:
            raise ValueError("Unsupported architecture detected.")

        if runtime.os not in Config.SUPPORTED_OS:
            raise ValueError("Operating system not supported.")
    """

    # Supported Architectures
    ARCH_x86_64 = "x86_64"
    ARCH_AARCH64 = "aarch64"
    ARCH_ARM = "arm"
    ARCH_ARM64 = "arm64"
    ARCH_I386 = "i386"
    ARCH_PPC64 = "ppc64"
    ARCH_PPC64LE = "ppc64le"
    ARCH_S390X = "s390x"

    KNOWN_ARCHITECTURES = [
        ARCH_x86_64, ARCH_AARCH64, ARCH_ARM, ARCH_ARM64,
        ARCH_I386, ARCH_PPC64, ARCH_PPC64LE, ARCH_S390X
    ]

    # Supported Operating Systems
    OS_WINDOWS = "windows"
    OS_LINUX = "linux"
    OS_MACOS = "darwin"

    SUPPORTED_OS = [OS_WINDOWS, OS_LINUX, OS_MACOS]

    # Supported Python Interpreters
    INTERPRETER_CPYTHON = "CPython"
    INTERPRETER_PYPY = "PyPy"
    INTERPRETER_JYTHON = "Jython"
    INTERPRETER_IRON_PYTHON = "IronPython"
    INTERPRETER_STACKLESS = "Stackless"
    INTERPRETER_MICROPYTHON = "MicroPython"
    INTERPRETER_BRYTHON = "Brython"
    INTERPRETER_PYSTON = "Pyston"
    INTERPRETER_GRAALPYTHON = "GraalPython"
    INTERPRETER_RUSTPYTHON = "RustPython"
    INTERPRETER_NUITKA = "Nuitka"
    INTERPRETER_TRANSCRYPT = "Transcrypt"

    SUPPORTED_PYTHON_INTERPRETERS = [
        INTERPRETER_CPYTHON, INTERPRETER_PYPY, INTERPRETER_JYTHON,
        INTERPRETER_IRON_PYTHON, INTERPRETER_STACKLESS, INTERPRETER_MICROPYTHON,
        INTERPRETER_BRYTHON, INTERPRETER_PYSTON, INTERPRETER_GRAALPYTHON,
        INTERPRETER_RUSTPYTHON, INTERPRETER_NUITKA, INTERPRETER_TRANSCRYPT
    ]

    # Class Attribute Types
    CLASS_TYPE = "class"
    INSTANCE_TYPE = "instance"

    SUPPORTED_CLASS_ATTRIBUTE_TYPES = [CLASS_TYPE, INSTANCE_TYPE]

    # Annotation Types
    ANNOTATION_INT = "int"
    ANNOTATION_FLOAT = "float"
    ANNOTATION_STR = "str"
    ANNOTATION_BOOL = "bool"
    ANNOTATION_LIST = "list"
    ANNOTATION_DICT = "dict"
    ANNOTATION_TUPLE = "tuple"
    ANNOTATION_SET = "set"
    ANNOTATION_OPTIONAL = "Optional"
    ANNOTATION_UNION = "Union"
    ANNOTATION_ANY = "Any"
    ANNOTATION_CALLABLE = "Callable"
    ANNOTATION_LIST = "List"
    ANNOTATION_DICT = "Dict"
    ANNOTATION_TUPLE = "Tuple"

    SUPPORTED_ANNOTATIONS = [
        ANNOTATION_INT, ANNOTATION_FLOAT, ANNOTATION_STR, ANNOTATION_BOOL,
        ANNOTATION_LIST, ANNOTATION_DICT, ANNOTATION_TUPLE, ANNOTATION_SET,
        ANNOTATION_OPTIONAL, ANNOTATION_UNION, ANNOTATION_ANY, ANNOTATION_CALLABLE,
        ANNOTATION_LIST, ANNOTATION_DICT, ANNOTATION_TUPLE
    ]
