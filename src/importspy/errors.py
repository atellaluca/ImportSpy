from .constants import Scope

class Errors:
    """
    Central repository for error messages used in ImportSpy’s validation engine.

    All validation errors extend one of three generic templates:
    - ELEMENT_MISSING: expected but not found
    - ELEMENT_MISMATCH: found but does not match the declared contract
    - ELEMENT_INVALID: found but not allowed (invalid value from limited set)
    """

    # General Warnings
    ANALYSIS_RECURSION_WARNING = (
        "Warning: Analysis recursion detected. Avoid analyzing code that itself handles analysis, "
        "to prevent stack overflow or performance issues."
    )

    # Generic Templates
    ELEMENT_MISSING = (
        "{0} is declared but missing in the system. "
        "Ensure it is properly defined and implemented."
    )

    ELEMENT_MISMATCH = (
        "{0} is defined but its value does not match the expected one. "
        "Expected: {1!r}, Found: {2!r}. "
        "Check the implementation and update the contract or the code accordingly."
    )

    ELEMENT_INVALID = (
        "{0} has an invalid value. "
        "Allowed values: {1}. Found: {2!r}. "
        "Update the environment or contract accordingly."
    )

    # Module Validation Errors
    FILENAME_MISMATCH = ELEMENT_MISMATCH.format(
        "The module filename", "{0}", "{1}"
    )
    VERSION_MISMATCH = ELEMENT_MISMATCH.format(
        "The module version", "{0}", "{1}"
    )

    # Function and Class Validation
    FUNCTION_RETURN_ANNOTATION_MISMATCH = ELEMENT_MISMATCH.format(
        "The return annotation of {0} '{1}'", "{2}", "{3}"
    )

    CLASS_MISSING = ELEMENT_MISSING.format('The class "{0}"')
    CLASS_SUPERCLASS_MISSING = ELEMENT_MISSING.format(
        'The superclass "{0}" in class "{1}"'
    )

    # Annotation and Runtime Validation
    INVALID_ANNOTATION = ELEMENT_INVALID.format(
        "The annotation", "{allowed}", "{found}"
    )
    INVALID_ATTRIBUTE_TYPE = ELEMENT_INVALID.format(
        "The attribute type", "{allowed}", "{found}"
    )
    INVALID_ARCHITECTURE = ELEMENT_INVALID.format(
        "The system architecture", "{allowed}", "{found}"
    )
    INVALID_OS = ELEMENT_INVALID.format(
        "The operating system", "{allowed}", "{found}"
    )
    INVALID_PYTHON_VERSION = ELEMENT_INVALID.format(
        "The Python version", "{allowed}", "{found}"
    )
    INVALID_PYTHON_INTERPRETER = ELEMENT_INVALID.format(
        "The Python interpreter", "{allowed}", "{found}"
    )

    # Scoped MISSING Errors
    VARIABLE_MISSING_ERROR = ELEMENT_MISSING.format('The variable "{name}"')
    ENV_VAR_MISSING_ERROR = ELEMENT_MISSING.format('The environment variable "{name}"')
    FUNCTION_ARG_MISSING_ERROR = ELEMENT_MISSING.format('The argument "{name}" of function "{function}"')
    METHOD_ARG_IN_CLASS_MISSING_ERROR = ELEMENT_MISSING.format(
        'The argument "{name}" of method "{method}" of class "{class_name}"'
    )
    CLASS_ATTRIBUTE_MISSING_ERROR = ELEMENT_MISSING.format(
        'The class attribute "{name}" of class "{class_name}"'
    )
    INSTANCE_ATTRIBUTE_MISSING_ERROR = ELEMENT_MISSING.format(
        'The instance attribute "{name}" of class "{class_name}"'
    )

    # Scoped MISMATCH Errors
    VARIABLE_MISMATCH_ERROR = ELEMENT_MISMATCH.format('The variable "{name}"', "{expected}", "{actual}")
    ENV_VAR_MISMATCH_ERROR = ELEMENT_MISMATCH.format('The environment variable "{name}"', "{expected}", "{actual}")
    FUNCTION_ARG_MISMATCH_ERROR = ELEMENT_MISMATCH.format(
        'The argument "{name}" of function "{function}"', "{expected}", "{actual}"
    )
    METHOD_ARG_IN_CLASS_MISMATCH_ERROR = ELEMENT_MISMATCH.format(
        'The argument "{name}" of method "{method}" of class "{class_name}"',
        "{expected}", "{actual}"
    )
    CLASS_ATTRIBUTE_MISMATCH_ERROR = ELEMENT_MISMATCH.format(
        'The class attribute "{name}" of class "{class_name}"', "{expected}", "{actual}"
    )
    INSTANCE_ATTRIBUTE_MISMATCH_ERROR = ELEMENT_MISMATCH.format(
        'The instance attribute "{name}" of class "{class_name}"', "{expected}", "{actual}"
    )

    # Scope-to-message mapping
    SCOPE_ELEMENT_MISSING_ERRORS = {
        Scope.SCOPE_VARIABLE: VARIABLE_MISSING_ERROR,
        Scope.SCOPE_ENVIRONMENT: ENV_VAR_MISSING_ERROR,
        Scope.SCOPE_FUNCTION_ARG: FUNCTION_ARG_MISSING_ERROR,
        Scope.SCOPE_METHOD_ARG_IN_CLASS: METHOD_ARG_IN_CLASS_MISSING_ERROR,
        Scope.SCOPE_CLASS_ATTRIBUTE: CLASS_ATTRIBUTE_MISSING_ERROR,
        Scope.SCOPE_INSTANCE_ATTRIBUTE: INSTANCE_ATTRIBUTE_MISSING_ERROR,
    }

    SCOPE_ELEMENT_MISMATCH_ERRORS = {
        Scope.SCOPE_VARIABLE: VARIABLE_MISMATCH_ERROR,
        Scope.SCOPE_ENVIRONMENT: ENV_VAR_MISMATCH_ERROR,
        Scope.SCOPE_FUNCTION_ARG: FUNCTION_ARG_MISMATCH_ERROR,
        Scope.SCOPE_METHOD_ARG_IN_CLASS: METHOD_ARG_IN_CLASS_MISMATCH_ERROR,
        Scope.SCOPE_CLASS_ATTRIBUTE: CLASS_ATTRIBUTE_MISMATCH_ERROR,
        Scope.SCOPE_INSTANCE_ATTRIBUTE: INSTANCE_ATTRIBUTE_MISMATCH_ERROR,
    }
