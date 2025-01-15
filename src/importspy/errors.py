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
    used throughout the ImportSpy framework. These messages are designed to address common 
    validation failures and runtime issues, promoting consistency and clarity in debugging 
    and user feedback.

    Key Features:
    --------------
    - **Centralized Storage**: All error messages are defined in one place, improving maintainability.
    - **Dynamic Placeholders**: Most messages include placeholders to dynamically insert 
      specific details (e.g., variable names, expected values, and actual values).
    - **Comprehensive Coverage**: Addresses a wide range of validation scenarios, from module-level 
      issues to runtime architecture compatibility.

    Use Cases:
    ----------
    The `Errors` class is integral to ImportSpy's validation processes, ensuring clear and 
    consistent communication when constraints are violated. It is utilized by validators, 
    utilities, and the core SpyModel to report issues.

    Attributes:
    -----------
    **General Warnings:**
    - `ANALYSIS_RECURSION_WARNING (str)`: Indicates potential recursion during analysis, 
      which could lead to stack overflow or performance issues.

    **Module Validation Errors:**
    - `FILENAME_MISMATCH (str)`: Reports a mismatch between the expected and actual filenames.
    - `VERSION_MISMATCH (str)`: Reports a version mismatch for a module.
    - `ENV_VAR_MISMATCH (str)`: Reports a mismatch in environment variable values.
    - `ENV_VAR_MISSING (str)`: Indicates a missing environment variable.
    - `VAR_MISMATCH (str)`: Indicates a mismatch between expected and actual variable values.
    - `VAR_MISSING (str)`: Indicates a missing variable in the module.

    **SpyModel Validation Errors:**
    - `FUNCTIONS_MISSING (str)`: Reports a missing function in the module.
    - `ANNOTATION_MISMATCH (str)`: Indicates a mismatch in function argument annotations.
    - `CLASS_MISSING (str)`: Indicates a missing class in the module.
    - `CLASS_ATTRIBUTE_MISSING (str)`: Indicates a missing attribute in a class.
    - `CLASS_ATTRIBUTE_MISMATCH (str)`: Indicates a mismatch in class attribute values.
    - `CLASS_SUPERCLASS_MISSING (str)`: Indicates a missing superclass in the class hierarchy.

    **Attribute and Argument Validation Errors:**
    - `INVALID_ATTRIBUTE_TYPE (str)`: Reports an invalid attribute type.
    - `INVALID_ANNOTATION (str)`: Reports an invalid annotation for a function argument or return type.

    Example Usage:
    --------------
    ```python
    if some_condition_fails:
        raise ValueError(Errors.FILENAME_MISMATCH.format(expected_filename, actual_filename))

    if invalid_architecture:
        raise ValueError(Errors.INVALID_ARCHITECTURE.format(detected_arch, Errors.KNOWN_ARCHITECTURES))
    ```
    """

    ANALYSIS_RECURSION_WARNING = (
        "Warning: You cannot analyze the code that itself handles analysis, as this may result "
        "in uncontrolled deep recursion. To avoid potential performance issues or stack overflow "
        "errors, ensure that the analysis process does not recursively attempt to evaluate itself."
    )

    # Module validation
    FILENAME_MISMATCH  = "Filename mismatch: {0} != {1}"
    VERSION_MISMATCH = "Version mismatch: {0} != {1}"
    ENV_VAR_MISMATCH = "Value mismatch for environment variable '{0}': expected '{1}', found '{2}'."
    ENV_VAR_MISSING = "Missing environment variable: '{0}'. Ensure it is defined in the system."
    VAR_MISMATCH = "Value mismatch for variable '{0}': expected '{1}', found '{2}'"
    VAR_MISSING = "Missing variable: '{0}'. Ensure it is defined."
    FUNCTIONS_MISSING = "Missing {0}: '{1}'. Ensure it is defined in {2} {3}"
    ANNONATION_MISMATCH = "Annotation mismatch for {0} {2}. Ensure it is defined in {0} {1}"
    CLASS_MISSING = "Missing class: {0}. Ensure it is defined."
    CLASS_ATTRIBUTE_MISSING = "Missing {0} attribute: '{1}'. Ensure it is defined in class '{2}'."
    CLASS_ATTRIBUTE_MISMATCH = "{0} mismatch for {1} attribute '{2}': expected '{3}', found '{4}'."
    CLASS_SUPERCLASS_MISSING = "Missing class superclass: '{0}'. Make sure that '{1}' extends {0}."
    INVALID_ATTRIBUTE_TYPE = "Invalid attribute type '{0}'. Support attributes are: {1}"

    # Runtime validation
    INVALID_ARCHITECTURE = "Invalid architecture '{0}'. Support architectures are: {1}"

    # Attribute and Argument validation
    INVALID_ANNOTATION = "Invalid annotation '{0}'. Support annotations are: {1}"