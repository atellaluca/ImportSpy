"""
Configuration Constants for External Usage in ImportSpy

This module defines the `Config` class, which encapsulates constants intended for external 
configuration by developers integrating ImportSpy into their projects. It segregates externally 
modifiable settings from internal constants to provide a clear distinction and enhance usability.

The `Config` class includes constants for supported architectures, operating systems, Python 
interpreters, and annotation types, ensuring compatibility and flexibility across diverse 
environments and use cases.
"""

class Config:

    """
    Developer Configuration for ImportSpy

    The `Config` class provides a collection of constants designed to be configurable by developers 
    integrating ImportSpy. These constants define supported architectures, operating systems, Python 
    interpreters, and annotation types, allowing users to adapt ImportSpy to their specific runtime 
    and validation requirements.

    Key Features:
    --------------
    - **Architecture Support**: Defines constants for commonly used system architectures.
    - **Operating System Compatibility**: Lists supported operating systems.
    - **Python Interpreter Support**: Includes major Python interpreters, from CPython to Nuitka.
    - **Annotation Types**: Enumerates valid annotation types for arguments, variables, and return values.

    Attributes:
    -----------
    ARCH_x86_64, ARCH_AARCH64, ... : str
        Constants representing supported system architectures (e.g., `x86_64`, `arm64`).
    OS_WINDOWS, OS_LINUX, OS_MACOS : str
        Constants representing supported operating systems.
    INTERPRETER_CPYTHON, INTERPRETER_PYPY, ... : str
        Constants representing supported Python interpreters.
    CLASS_TYPE, INSTANCE_TYPE : str
        Identifiers for class-level and instance-level attributes.
    ANNOTATION_INT, ANNOTATION_FLOAT, ... : str
        Valid annotation types for arguments and return values (e.g., `int`, `list`, `Optional`).

    Example Usage:
    --------------
    ```python
    from importspy.config import Config

    if runtime.arch not in Config.ARCH_x86_64:
        raise ValueError("Unsupported architecture detected.")
    ```
    This example demonstrates how to use `Config` constants to validate runtime conditions.
    """

    ARCH_x86_64 = "x86_64"
    ARCH_AARCH64 = "aarch64"
    ARCH_ARM = "arm"
    ARCH_ARM64 = "arm64"
    ARCH_I386 = "i386"
    ARCH_PPC64 = "ppc64"
    ARCH_PPC64LE = "ppc64le"
    ARCH_S390X = "s390x"

    OS_WINDOWS = "windows"
    OS_LINUX = "linux"
    OS_MACOS = "darwin"

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

    CLASS_TYPE = "class"
    INSTANCE_TYPE = "instance"

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