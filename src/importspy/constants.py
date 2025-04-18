from .config import Config


class Constants:
    """
    Constants used internally by ImportSpy's runtime validation engine.

    This class defines the canonical reference values used during import contract
    validation, including supported architectures, operating systems, Python
    interpreters, annotation types, and structural metadata keys.

    Unlike `Config`, which defines values dynamically from the runtime or user
    environment, `Constants` serves as the fixed baseline for what ImportSpy
    considers valid and contract-compliant.

    Attributes:
        KNOWN_ARCHITECTURES (List[str]):
            List of CPU architectures supported in runtime validation,
            including 'x86_64', 'arm64', 'i386', and others.

        SUPPORTED_OS (List[str]):
            List of supported operating systems: 'linux', 'windows', and 'darwin'.

        SUPPORTED_PYTHON_VERSION (List[str]):
            List of supported Python versions, e.g. '3.9', '3.10', '3.11', etc.

        SUPPORTED_PYTHON_IMPLEMENTATION (List[str]):
            Python interpreter implementations recognized by ImportSpy,
            such as 'CPython', 'PyPy', 'IronPython', and others.

        SUPPORTED_CLASS_ATTRIBUTE_TYPES (List[str]):
            Allowed attribute type classifications: 'class' and 'instance'.

        SUPPORTED_ANNOTATIONS (List[str]):
            Allowed annotation types used for validating variables,
            arguments, and return values. Includes types such as
            'int', 'str', 'Optional', 'Union', 'Callable', etc.

        NAME (str):
            Metadata key used for referencing object names in the model.

        VALUE (str):
            Metadata key used to represent literal values in contracts.

        ANNOTATION (str):
            Metadata key used to refer to a declared annotation in contracts.

        CLASS_TYPE (str):
            String literal used to label a class-level attribute type.

        INSTANCE_TYPE (str):
            String literal used to label an instance-level attribute type.

        LOG_MESSAGE_TEMPLATE (str):
            Template string for standardized log message formatting
            during contract evaluation and model parsing.
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

    SUPPORTED_PYTHON_VERSION=[
        Config.PYTHON_VERSION_3_13,
        Config.PYTHON_VERSION_3_12,
        Config.PYTHON_VERSION_3_11,
        Config.PYTHON_VERSION_3_10,
        Config.PYTHON_VERSION_3_9
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
