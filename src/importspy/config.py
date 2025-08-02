class Config:
    
    """
    Static configuration for ImportSpy.

    This class defines the baseline constants used during runtime and structural
    validation of Python modules. Values declared here represent the supported
    options for platforms, interpreters, Python versions, class attribute types,
    and type annotations within a SpyModel contract.

    These constants are used internally to validate compatibility and enforce
    declared constraints across diverse environments.

    Categories:
    ----------
    • Architectures: CPU instruction sets (e.g. x86_64, arm64).
    • Operating Systems: Target OS identifiers (e.g. linux, windows).
    • Python Versions: Compatible interpreter versions.
    • Interpreters: Supported Python implementations.
    • Attribute Types: Class vs. instance variables.
    • Type Annotations: Accepted runtime-compatible types.

    Examples:
    ---------
    - A contract may require `arch: x86_64` and `interpreter: CPython`.
    - A method argument may be annotated with `Optional[str]`.
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

    # Supported Python Version
    PYTHON_VERSION_3_13 = "3.13"
    PYTHON_VERSION_3_12 = "3.12"
    PYTHON_VERSION_3_11 = "3.11"
    PYTHON_VERSION_3_10 = "3.10"
    PYTHON_VERSION_3_9 = "3.9"

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
