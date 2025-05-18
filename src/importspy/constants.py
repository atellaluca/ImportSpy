from .config import Config
from enum import Enum


class Constants:
    """
    Constants used internally by ImportSpy's runtime validation engine.

    This class defines the canonical reference values used during import contract
    validation, including supported architectures, operating systems, Python
    interpreters, annotation types, and structural metadata keys.

    Unlike `Config`, which defines values dynamically from the runtime or user
    environment, `Constants` serves as the fixed baseline for what ImportSpy
    considers valid and contract-compliant.
    """

    class SupportedArchitectures:

        Config.ARCH_x86_64 
        Config.ARCH_AARCH64 
        Config.ARCH_ARM
        Config.ARCH_ARM64 
        Config.ARCH_I386 
        Config.ARCH_PPC64 
        Config.ARCH_PPC64LE 
        Config.ARCH_S390X

    class SupportedOS:

        Config.OS_WINDOWS
        Config.OS_LINUX 
        Config.OS_MACOS

    class SupportedPythonVersions(str, Enum):

        Config.PYTHON_VERSION_3_13
        Config.PYTHON_VERSION_3_12
        Config.PYTHON_VERSION_3_11
        Config.PYTHON_VERSION_3_10
        Config.PYTHON_VERSION_3_9

    class SupportedPythonImplementations(str, Enum):
        
        Config.INTERPRETER_CPYTHON
        Config.INTERPRETER_PYPY
        Config.INTERPRETER_JYTHON
        Config.INTERPRETER_IRON_PYTHON
        Config.INTERPRETER_MICROPYTHON
        Config.INTERPRETER_BRYTHON
        Config.INTERPRETER_PYSTON
        Config.INTERPRETER_GRAALPYTHON
        Config.INTERPRETER_RUSTPYTHON
        Config.INTERPRETER_NUITKA
        Config.INTERPRETER_TRANSCRYPT
    
    class SupportedClassAttributeTypes(str, Enum):

        Config.CLASS_TYPE
        Config.INSTANCE_TYPE

    NAME = "Name"
    VALUE = "Value"
    ANNOTATION = "Annotation"

    CLASS_TYPE = Config.CLASS_TYPE
    INSTANCE_TYPE = Config.INSTANCE_TYPE

    class SupportedAnnotations(str, Enum):
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

    LOG_MESSAGE_TEMPLATE = (
        "[Operation: {operation}] [Status: {status}] "
        "[Details: {details}]"
    )

class Contexts(str, Enum):

    RUNTIME_CONTEXT = "runtime"
    ENVIRONMENT_CONTEXT = "environment"
    MODULE_CONTEXT = "module"
    CLASS_CONTEXT = "class"

class Errors:
    """
    Defines reusable templates for error generation.
    """

    TEMPLATE_KEY = "template"
    SOLUTION_KEY = "solution"
    SCOPE_VARIABLE = "variable"
    SCOPE_ARGUMENT = "argument"

    CONTEXT_INTRO = {
        Contexts.RUNTIME_CONTEXT: "Runtime constraint violation",
        Contexts.ENVIRONMENT_CONTEXT: "Environment validation failure",
        Contexts.MODULE_CONTEXT: "Module structural inconsistency",
        Contexts.CLASS_CONTEXT: "Class contract violation"
    }

    class Category(str, Enum):

        MISSING = "missing"
        MISMATCH = "mismatch"
        INVALID = "invalid"

    VARIABLES_LABEL_TEMPLATE = {
        
        SCOPE_VARIABLE: {
            Contexts.ENVIRONMENT_CONTEXT: 'The environment variable "{environment_variable_name}"',
            Contexts.MODULE_CONTEXT: 'The variable "{variable_name}" in module "{module_name}"',
            Contexts.CLASS_CONTEXT: 'The {attribute_type} attribute "{attribute_name}" in class "{class_name}"'
        },
        SCOPE_ARGUMENT: {
            Contexts.MODULE_CONTEXT: 'The argument "{argument_name}" of function "{function_name}"',
            Contexts.CLASS_CONTEXT: 'The argument "{argument_name}" of method "{method_name}" in class "{class_name}"',
        }
    }

    FUNCTIONS_LABEL_TEMPLATE = {
        Contexts.MODULE_CONTEXT: 'The function "{function_name}" in module "{module_name}"',
        Contexts.CLASS_CONTEXT: 'The method "{method_name}" in class "{class_name}"'
    }

    ERROR_MESSAGE_TEMPLATES = {
        Category.MISSING: {
            TEMPLATE_KEY: "{label} is declared but missing.",
            SOLUTION_KEY: "Ensure it is properly defined and implemented."
        },
        Category.MISMATCH: {
            TEMPLATE_KEY: "{label} does not match the expected value. Expected: {expected!r}, Found: {actual!r}.",
            SOLUTION_KEY: "Check the implementation or update the contract accordingly."
        },
        Category.INVALID: {
            TEMPLATE_KEY: "{label} has an invalid value. Allowed values: {allowed}. Found: {found!r}.",
            SOLUTION_KEY: "Update the environment or contract accordingly."
        }
    }