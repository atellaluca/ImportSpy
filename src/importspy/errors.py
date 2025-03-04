"""
Centralized Error Messaging for ImportSpy

This module defines the `Errors` class, which serves as a repository for all error 
and warning messages used across the ImportSpy framework. By consolidating error 
messages into a single location, this module ensures consistency, maintainability, 
and clarity in issue reporting.

Each error message includes placeholders (`{0}`, `{1}`, etc.), allowing for dynamic 
insertion of context-specific details at runtime.
"""

class Errors:
    """
    Centralized Repository for Error Messages in ImportSpy.

    The `Errors` class provides a structured collection of error and warning messages 
    used throughout the ImportSpy framework. These messages cover module validation, 
    runtime validation, attribute validation, and argument validation, ensuring 
    consistent and informative error reporting.

    Features:
    ---------
    - Centralized storage for all error messages.
    - Dynamic placeholders for runtime-specific details.
    - Coverage for module validation, runtime issues, and structural inconsistencies.

    Usage Example:
    --------------
    .. code-block:: python

        if some_condition_fails:
            raise ValueError(Errors.FILENAME_MISMATCH.format(expected="module.py", found="package.py"))

        if invalid_architecture:
            raise ValueError(Errors.INVALID_ARCHITECTURE.format(found_architecture, expected_architectures))

    Sections:
    ---------
    - General Warnings
    - Module Validation
    - Runtime Validation
    - Argument and Annotation Validation
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

    # Annotation Validation
    INVALID_ANNOTATION = "Invalid annotation: expected one of {0}, but found '{1}'."

    # Generic Element Missing
    ELEMENT_MISSING = (
        "{0} is declared but missing in the system. "
        "Ensure it is properly defined and implemented."
    )
