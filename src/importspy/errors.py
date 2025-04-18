class Errors:

    """
    Central repository for error messages used in ImportSpy’s validation engine.

    This class contains formatted string constants for every type of structural,
    semantic, and runtime validation error that can be raised during contract
    evaluation. These error messages provide actionable feedback and are used
    throughout ImportSpy's exception handling system.

    The format strings typically include placeholders for contextual details,
    such as expected and actual values, function names, class names, or
    annotation types. Grouped by category, these constants help keep the
    validation engine consistent and maintainable.

    Attributes:
        ANALYSIS_RECURSION_WARNING (str):
            General warning when the validation process detects recursive self-analysis.

        FILENAME_MISMATCH (str):
            Raised when the module filename does not match the expected contract.

        VERSION_MISMATCH (str):
            Triggered when the module version deviates from the one declared in the contract.

        ENV_VAR_MISSING (str):
            Raised when a required environment variable is not found in the system.

        ENV_VAR_MISMATCH (str):
            Indicates a mismatch between the expected and actual values of an environment variable.

        VAR_MISSING (str):
            Raised when a required variable is not present in the importing module.

        VAR_MISMATCH (str):
            Raised when a variable is present but its value does not match what the contract expects.

        FUNCTIONS_MISSING (str):
            Used when one or more expected functions are missing from the module.

        FUNCTION_RETURN_ANNOTATION_MISMATCH (str):
            Indicates a mismatch in the return type annotation of a function.

        VARIABLE_MISMATCH (str):
            Raised when a declared variable's value does not match the expected value.

        VARIABLE_MISSING (str):
            Raised when a declared variable is not found.

        ARGUMENT_MISMATCH (str):
            Raised when a function argument has an unexpected name or annotation.

        ARGUMENT_MISSING (str):
            Raised when a required argument is missing in the function signature.

        CLASS_MISSING (str):
            Triggered when a required class is not defined in the importing module.

        CLASS_ATTRIBUTE_MISSING (str):
            Raised when an expected attribute is not found in a class definition.

        CLASS_ATTRIBUTE_MISMATCH (str):
            Raised when an attribute exists but its value does not match what the contract expects.

        CLASS_SUPERCLASS_MISSING (str):
            Triggered when a required superclass is missing from a class declaration.

        INVALID_ATTRIBUTE_TYPE (str):
            Raised when an attribute has an unsupported type.

        INVALID_ARCHITECTURE (str):
            Triggered when the system architecture does not match any of the allowed values.

        INVALID_OS (str):
            Triggered when the operating system is not among those supported.

        INVALID_PYTHON_VERSION (str):
            Raised when the current Python version is not one of the accepted versions.

        INVALID_PYTHON_INTERPRETER (str):
            Raised when the Python interpreter is not among the supported ones.

        INVALID_ANNOTATION (str):
            Raised when a variable, argument, or return annotation is unsupported.

        ELEMENT_MISSING (str):
            Generic error for any expected element missing from the system or module context.
    """
    
    # General Warnings
    ANALYSIS_RECURSION_WARNING = (
        "Warning: Analysis recursion detected. Avoid analyzing code that itself handles analysis, "
        "to prevent stack overflow or performance issues."
    )

    # Module Validation Errors
    FILENAME_MISMATCH = "Filename mismatch: expected '{0}', found '{1}'."
    VERSION_MISMATCH = "Version mismatch: expected '{0}', found '{1}'."
    ENV_VAR_MISSING = "Missing environment variable: '{0}'. Ensure it is defined in the system."
    ENV_VAR_MISMATCH = "Environment variable value mismatch: expected '{0}', found '{1}'."
    VAR_MISSING = "Missing variable: '{0}'. Ensure it is defined."
    VAR_MISMATCH = "Variable value mismatch: expected '{0}', found '{1}'."
    FUNCTIONS_MISSING = "Missing {0}: '{1}'. Ensure it is defined."

    # Function and Class Validation Errors
    FUNCTION_RETURN_ANNOTATION_MISMATCH = (
        "Return annotation mismatch for {0} '{1}': expected '{2}', found '{3}'."
    )
    VARIABLE_MISMATCH = "Variable mismatch'{1}': expected '{2}', found '{3}'."
    VARIABLE_MISSING = "Missing variable '{0}'"
    ARGUMENT_MISMATCH = "Argument mismatch for {0} '{1}': expected '{2}', found '{3}'."
    ARGUMENT_MISSING = "Missing argument '{0}' in {1}."
    
    CLASS_MISSING = "Missing class: '{0}'. Ensure it is defined."
    CLASS_ATTRIBUTE_MISSING = "Missing attribute '{0}' in class '{1}'."
    CLASS_ATTRIBUTE_MISMATCH = (
        "Attribute value mismatch for '{0}' in class '{1}': expected '{2}', found '{3}'."
    )
    CLASS_SUPERCLASS_MISSING = (
        "Missing superclass '{0}' in class '{1}'. Ensure that '{1}' extends '{0}'."
    )
    INVALID_ATTRIBUTE_TYPE = "Invalid attribute type: '{0}'. Supported types are: {1}."

    # Runtime Validation Errors
    INVALID_ARCHITECTURE = "Invalid architecture: expected '{0}', found '{1}'."
    INVALID_OS = "Invalid Operating System: expected one of {0}, but found '{1}'."

    # Python Valitation Errors
    INVALID_PYTHON_VERSION = "Invalid python version: expected one of '{0}', but found '{1}'."
    INVALID_PYTHON_INTERPRETER = "Invalid python interpreter: expected one of '{0}', but found '{1}'."

    # Annotation Validation
    INVALID_ANNOTATION = "Invalid annotation: expected one of {0}, but found '{1}'."

    # Generic Element Missing
    ELEMENT_MISSING = (
        "{0} is declared but missing in the system. "
        "Ensure it is properly defined and implemented."
    )