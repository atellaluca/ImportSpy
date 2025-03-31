"""
importspy.config
=================

Static constants used internally by ImportSpy during validation and testing.

The `Config` class provides a curated set of reference values for use within the framework,
including supported operating systems, architectures, Python interpreters, and annotation types.

These values are used to:
- Populate and validate import contracts during development.
- Run test suites across multiple architectures and environments.
- Provide default references for validators and compatibility checks.

This module was previously exposed to users, but is now intended for internal use only.
"""

class Config:
    """
    Internal reference constants for validation, testing, and contract generation.

    This class is used by validators, test cases, and tools that need to assert compatibility
    with specific operating systems, Python interpreters, annotation types, or deployment targets.

    Attributes:
    -----------
    KNOWN_ARCHITECTURES : list[str]
        Standard architectures supported by ImportSpy (e.g., x86_64, arm64).

    SUPPORTED_OS : list[str]
        Operating systems supported in import contracts (e.g., Windows, Linux, macOS).

    SUPPORTED_PYTHON_INTERPRETERS : list[str]
        Interpreter identifiers validated during runtime checks (e.g., CPython, PyPy).

    SUPPORTED_CLASS_ATTRIBUTE_TYPES : list[str]
        Valid types for class attributes: 'class' or 'instance'.

    SUPPORTED_ANNOTATIONS : list[str]
        Allowed annotation types for variables, arguments, and return values.

    Example:
    --------
    These constants are used when creating test contracts or performing type assertions:

    .. code-block:: python

        from importspy.config import Config

        if architecture not in Config.KNOWN_ARCHITECTURES:
            raise ValueError("Unsupported architecture")

        if annotation not in Config.SUPPORTED_ANNOTATIONS:
            raise ValueError("Unsupported type annotation")
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
