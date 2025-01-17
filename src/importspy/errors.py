"""
Centralized Error Messaging for ImportSpy

This module defines the `Errors` class, which acts as a repository for all error and warning 
messages used across the ImportSpy framework. By consolidating error messages into a single 
location, this module ensures consistency, maintainability, and clarity in the communication 
of issues encountered during runtime validation or model analysis.

The error messages are formatted with placeholders to dynamically populate context-specific 
details, allowing for precise and informative error reporting.
"""

class Errors:
    """
    Centralized Repository for Error Messages in ImportSpy

    The `Errors` class provides a comprehensive collection of error and warning messages 
    used throughout the ImportSpy framework. These messages address common validation 
    failures and runtime issues, promoting consistency and clarity in debugging and user feedback.

    Features:
    - Centralized storage for all error messages.
    - Dynamic placeholders for context-specific details.
    - Coverage for module validation, runtime issues, and argument/attribute validation.

    Example Usage:
    --------------
    ```python
    if some_condition_fails:
        raise ValueError(Errors.FILENAME_MISMATCH.format(expected="module.py", found="package.py"))

    if invalid_architecture:
        raise ValueError(Errors.INVALID_ARCHITECTURE.format(found_architecture, expected_architectures))
    ```
    """

    # General warnings
    ANALYSIS_RECURSION_WARNING = (
        "Warning: Analysis recursion detected. Avoid analyzing code that itself handles analysis, "
        "to prevent stack overflow or performance issues."
    )

    # Module validation
    FILENAME_MISMATCH = "Filename mismatch: expected '{0}', found '{1}'."
    VERSION_MISMATCH = "Version mismatch: expected '{0}', found '{1}'."
    ENV_VAR_MISMATCH = "Environment variable value mismatch: expected '{0}', found '{1}'."
    ENV_VAR_MISSING = "Missing environment variable: '{0}'. Ensure it is defined in the system."
    VAR_MISMATCH = "Variable value mismatch: expected '{0}', found '{1}'."
    VAR_MISSING = "Missing variable: '{0}'. Ensure it is defined."
    FUNCTIONS_MISSING = "Missing {0}: '{1}'. Ensure it is defined."
    FUNCTION_RETURN_ANNOTATION_MISMATCH = (
        "Return annotation mismatch for {0} '{1}': expected '{2}', found '{3}'."
    )
    ARGUMENT_MISMATCH = "Argument mismatch for {0} '{1}': expected '{2}', found '{3}'."
    CLASS_MISSING = "Missing class: '{0}'. Ensure it is defined."
    CLASS_ATTRIBUTE_MISSING = "Missing attribute '{0}' in class '{1}'."
    CLASS_ATTRIBUTE_MISMATCH = (
        "Attribute value mismatch for '{0}' in class '{1}': expected '{2}', found '{3}'."
    )
    CLASS_SUPERCLASS_MISSING = (
        "Missing superclass '{0}' in class '{1}'. Ensure that '{1}' extends '{0}'."
    )
    INVALID_ATTRIBUTE_TYPE = "Invalid attribute type: '{0}'. Supported types are: {1}."

    # Runtime validation
    INVALID_ARCHITECTURE = "Invalid architecture: expected '{0}', found '{1}'."
    INVALID_OS = "Invalid Operating System: expected one of {0}, but found '{1}'."

    # Argument and annotation validation
    INVALID_ANNOTATION = "Invalid annotation: expected one of {0}, but found '{1}'."
    ARGUMENT_MISSING = "Missing argument '{0}' in {1}."

    ELEMENT_MISSING = (
        "{0} is declared but missing in the system. "
        "Ensure it is properly defined and implemented."
    )
