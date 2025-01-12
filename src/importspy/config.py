class Config:

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

    ANNOTATION_INT = "int",
    ANNOTATION_FLOAT = "float",
    ANNOTATION_STR = "str",
    ANNOTATION_BOOL = "bool", 
    ANNOTATION_LIST = "list",
    ANNOTATION_DICT = "dict",
    ANNOTATION_TUPLE = "tuple",
    ANNOTATION_SET = "set",
    ANNOTATION_OPTIONAL = "Optional",
    ANNOTATION_UNION = "Union",
    ANNOTATION_ANY = "Any",
    ANNOTATION_CALLABLE = "Callable",
    ANNOTATION_LIST = "List",
    ANNOTATION_DICT = "Dict",
    ANNOTATION_TUPLE = "Tuple"