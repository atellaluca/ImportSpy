"""importspy.config

Static configuration definitions for ImportSpy.

This module declares platform-wide constants used throughout ImportSpy
for validating compatibility and structural expectations declared in
SpyModel contracts. These values represent the officially supported
CPU architectures, operating systems, Python interpreters, version targets,
class attribute types, and accepted type annotations.
"""

class Config:
    """Static configuration container for ImportSpy validation.

    This class defines constants used during runtime and structural validation
    of Python modules. All values reflect supported targets or accepted types
    declared in `.yml` contracts interpreted by ImportSpy.

    Attributes:
        Architectures (str): Supported CPU architectures (e.g., "x86_64").
        Operating Systems (str): Accepted OS identifiers (e.g., "linux").
        Python Versions (str): Known compatible Python interpreter versions.
        Interpreters (str): Recognized Python implementation names.
        Attribute Types (str): Whether class-level or instance-level variables.
        Annotation Types (str): Type annotations allowed in contract validation.

    These constants are typically used in:
    - Runtime environment checks
    - Contract-based validation
    - Enforcement of developer-specified constraints
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

    # Supported Operating Systems
    OS_WINDOWS = "windows"
    OS_LINUX = "linux"
    OS_MACOS = "darwin"

    # Supported Python Versions
    PYTHON_VERSION_3_13 = "3.13"
    PYTHON_VERSION_3_12 = "3.12"
    PYTHON_VERSION_3_11 = "3.11"
    PYTHON_VERSION_3_10 = "3.10"

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

    # Class Attribute Types
    CLASS_TYPE = "class"
    INSTANCE_TYPE = "instance"

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
    ANNOTATION_LIST_TYPING = "List"
    ANNOTATION_DICT_TYPING = "Dict"
    ANNOTATION_TUPLE_TYPING = "Tuple"
