class Config:
    """
    Static configuration container for ImportSpy.

    This class centralizes all constant values used for runtime validation,
    defining supported architectures, operating systems, Python versions,
    interpreter implementations, attribute classifications, and annotation types.
    These constants ensure consistency and safety during contract enforcement
    across diverse execution environments.

    Attributes:
        ARCH_x86_64 (str): Identifier for the x86_64 CPU architecture.
        ARCH_AARCH64 (str): Identifier for the AArch64 architecture.
        ARCH_ARM (str): Identifier for the ARM architecture.
        ARCH_ARM64 (str): Identifier for the ARM64 architecture.
        ARCH_I386 (str): Identifier for the i386 (32-bit Intel) architecture.
        ARCH_PPC64 (str): Identifier for the PowerPC 64-bit architecture.
        ARCH_PPC64LE (str): Identifier for PowerPC 64-bit Little Endian architecture.
        ARCH_S390X (str): Identifier for IBM s390x architecture.

        OS_WINDOWS (str): Identifier for Windows operating systems.
        OS_LINUX (str): Identifier for Linux operating systems.
        OS_MACOS (str): Identifier for macOS (Darwin-based) operating systems.

        PYTHON_VERSION_3_13 (str): Supported Python version 3.13.
        PYTHON_VERSION_3_12 (str): Supported Python version 3.12.
        PYTHON_VERSION_3_11 (str): Supported Python version 3.11.
        PYTHON_VERSION_3_10 (str): Supported Python version 3.10.
        PYTHON_VERSION_3_9 (str): Supported Python version 3.9.

        INTERPRETER_CPYTHON (str): Identifier for CPython interpreter.
        INTERPRETER_PYPY (str): Identifier for PyPy interpreter.
        INTERPRETER_JYTHON (str): Identifier for Jython interpreter.
        INTERPRETER_IRON_PYTHON (str): Identifier for IronPython interpreter.
        INTERPRETER_STACKLESS (str): Identifier for Stackless Python.
        INTERPRETER_MICROPYTHON (str): Identifier for MicroPython interpreter.
        INTERPRETER_BRYTHON (str): Identifier for Brython interpreter.
        INTERPRETER_PYSTON (str): Identifier for Pyston interpreter.
        INTERPRETER_GRAALPYTHON (str): Identifier for GraalPython interpreter.
        INTERPRETER_RUSTPYTHON (str): Identifier for RustPython interpreter.
        INTERPRETER_NUITKA (str): Identifier for Nuitka interpreter.
        INTERPRETER_TRANSCRYPT (str): Identifier for Transcrypt interpreter.

        CLASS_TYPE (str): Label for class-level attributes in contract definitions.
        INSTANCE_TYPE (str): Label for instance-level attributes in contract definitions.

        ANNOTATION_INT (str): Annotation identifier for integers.
        ANNOTATION_FLOAT (str): Annotation identifier for floats.
        ANNOTATION_STR (str): Annotation identifier for strings.
        ANNOTATION_BOOL (str): Annotation identifier for booleans.
        ANNOTATION_LIST (str): Annotation identifier for generic lists.
        ANNOTATION_DICT (str): Annotation identifier for generic dictionaries.
        ANNOTATION_TUPLE (str): Annotation identifier for generic tuples.
        ANNOTATION_SET (str): Annotation identifier for sets.
        ANNOTATION_OPTIONAL (str): Annotation identifier for optional values.
        ANNOTATION_UNION (str): Annotation identifier for union types.
        ANNOTATION_ANY (str): Annotation identifier for untyped (any) values.
        ANNOTATION_CALLABLE (str): Annotation identifier for callable objects.
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
