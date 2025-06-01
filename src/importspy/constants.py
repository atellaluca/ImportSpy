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

    class SupportedArchitectures(str, Enum):

        Config.ARCH_x86_64 
        Config.ARCH_AARCH64 
        Config.ARCH_ARM
        Config.ARCH_ARM64 
        Config.ARCH_I386 
        Config.ARCH_PPC64 
        Config.ARCH_PPC64LE 
        Config.ARCH_S390X

    class SupportedOS(str, Enum):

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
        INT = Config.ANNOTATION_INT
        FLOAT = Config.ANNOTATION_FLOAT
        STR = Config.ANNOTATION_STR
        BOOL = Config.ANNOTATION_BOOL
        LIST = Config.ANNOTATION_LIST
        DICT = Config.ANNOTATION_DICT
        TUPLE = Config.ANNOTATION_TUPLE
        SET = Config.ANNOTATION_SET
        OPTIONAL = Config.ANNOTATION_OPTIONAL
        UNION = Config.ANNOTATION_UNION
        ANY = Config.ANNOTATION_ANY
        CALLABLE = Config.ANNOTATION_CALLABLE
        LIST_TYPING = Config.ANNOTATION_LIST_TYPING
        DICT_TYPING = Config.ANNOTATION_DICT_TYPING
        TUPLE_TYPING = Config.ANNOTATION_TUPLE_TYPING

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

    ENTITY_MESSAGES = "entity"
    COLLECTIONS_MESSAGES = "collections"

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

    RUNTIME_LABEL_TEMPLATE = {

        ENTITY_MESSAGES: 'The runtime "{runtime_1}"',
        COLLECTIONS_MESSAGES: 'The runtimes "{runtimes_1}"'

    }

    SYSTEM_LABEL_TEMPLATE = {

        ENTITY_MESSAGES: 'The system "{system_1}"',
        COLLECTIONS_MESSAGES: 'The systems "{systems_1}"'

    }

    PYTHON_LABEL_TEMPLATE = {

        ENTITY_MESSAGES: 'The python "{python_1}"',
        COLLECTIONS_MESSAGES: 'The pythons "{pythons_1}"'

    }

    VARIABLES_LABEL_TEMPLATE = {
        
        SCOPE_VARIABLE: {

            ENTITY_MESSAGES: {

                Contexts.ENVIRONMENT_CONTEXT: 'The environment variable "{environment_variable_name}"',
                Contexts.MODULE_CONTEXT: 'The variable "{variable_name}" in module "{module_name}"',
                Contexts.CLASS_CONTEXT: 'The {attribute_type} attribute "{attribute_name}" in class "{class_name}"'

            },

            COLLECTIONS_MESSAGES: {

                Contexts.ENVIRONMENT_CONTEXT: 'The environment "{environment_1}"',
                Contexts.MODULE_CONTEXT: 'The variables "{variables_1}"',
                Contexts.CLASS_CONTEXT: 'The attributes "{attributes_1}"'

            }
        },

        SCOPE_ARGUMENT: {

            ENTITY_MESSAGES: {

                Contexts.MODULE_CONTEXT: 'The argument "{argument_name}" of function "{function_name}"',
                Contexts.CLASS_CONTEXT: 'The argument "{argument_name}" of method "{method_name}" in class "{class_name}"',

            },

            COLLECTIONS_MESSAGES: {

                Contexts.MODULE_CONTEXT: 'The arguments "{arguments_1}" of function "{function_name}"',
                Contexts.CLASS_CONTEXT: 'The arguments "{arguments_1}" of method "{method_name}", in class "{class_name}"'

            }

        }
        
    }

    FUNCTIONS_LABEL_TEMPLATE = {

        ENTITY_MESSAGES: {

            Contexts.MODULE_CONTEXT: 'The function "{function_name}" in module "{filename}"',
            Contexts.CLASS_CONTEXT: 'The method "{method_name}" in class "{class_name}"'

        },

        COLLECTIONS_MESSAGES: {

            Contexts.MODULE_CONTEXT: 'The functions "{functions_1}" in module "{filename}"',
            Contexts.CLASS_CONTEXT: 'The methods "{methods_1}" in class "{class_name}"'

        }

    }

    MODULE_LABEL_TEMPLATE = {
        
        ENTITY_MESSAGES: {

            Contexts.CLASS_CONTEXT: 'The class "{class_name}"',
            Contexts.RUNTIME_CONTEXT: 'The module "{filename}"',
            Contexts.ENVIRONMENT_CONTEXT: 'The version "{version}" of module "{filename}"'

        },

        COLLECTIONS_MESSAGES: {

            Contexts.CLASS_CONTEXT: 'The classes "{classes_1}" in module "{filename}"'

        }

    }

    KEY_RUNTIMES_1 = "runtimes_1"
    KEY_SYSTEMS_1 = "runtimes_1"
    KEY_PYTHONS_1 = "pythons_1"
    KEY_PYTHON_1 = "python_1"
    KEY_ENVIRONMENT_1 = "environment_1"
    KEY_ENVIRONMENT_VARIABLE_NAME = "environment_variable_name"
    KEY_MODULES_1 = "modules_1"
    KEY_VARIABLES_1 = "variables_1"
    KEY_ATTRIBUTES_1 = "attributes_1"
    KEY_ARGUMENTS_1 = "arguments_1"
    KEY_FUNCTIONS_1 = "functions_1"
    KEY_CLASSES_1 = "classes_1"

    KEY_VARIABLE_NAME = "variable_name"
    KEY_ARGUMENT_NAME = "argument_name"
    KEY_FUNCTION_NAME = "function_name"
    KEY_METHOD_NAME = "method_name"
    KEY_MODULE_NAME = "module_name"
    KEY_ATTRIBUTE_TYPE = "attribute_type"
    KEY_ATTRIBUTE_NAME = "attribute_name"
    KEY_CLASS_NAME = "class_name"
    KEY_MODULE_VERSION = "version"
    KEY_FILE_NAME = "filename"

    VARIABLES_DINAMIC_PAYLOAD = {

        SCOPE_VARIABLE: {

            ENTITY_MESSAGES: {

                Contexts.ENVIRONMENT_CONTEXT: KEY_ENVIRONMENT_VARIABLE_NAME,
                Contexts.MODULE_CONTEXT: KEY_VARIABLE_NAME,
                Contexts.CLASS_CONTEXT: KEY_ATTRIBUTE_NAME

            },

            COLLECTIONS_MESSAGES: {
                
                Contexts.ENVIRONMENT_CONTEXT: KEY_ENVIRONMENT_1,
                Contexts.MODULE_CONTEXT: KEY_VARIABLES_1,
                Contexts.CLASS_CONTEXT: KEY_ATTRIBUTES_1

            }
        },
        SCOPE_ARGUMENT: {

            ENTITY_MESSAGES: {
                
                Contexts.MODULE_CONTEXT: KEY_ARGUMENT_NAME,
                Contexts.CLASS_CONTEXT: KEY_ARGUMENT_NAME

            },

            COLLECTIONS_MESSAGES: {

                Contexts.MODULE_CONTEXT: KEY_ARGUMENTS_1,
                Contexts.CLASS_CONTEXT: KEY_ARGUMENTS_1

            }
            
        }

    }

    FUNCTIONS_DINAMIC_PAYLOAD = {
        Contexts.MODULE_CONTEXT: KEY_FUNCTION_NAME,
        Contexts.CLASS_CONTEXT: KEY_METHOD_NAME
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