"""
importspy.errors
================

Defines standardized error message templates used across ImportSpy's
validation engine. These are grouped into three main categories:

- ELEMENT_MISSING: when an expected element is declared but not found.
- ELEMENT_MISMATCH: when an element exists but does not match the contract.
- ELEMENT_INVALID: when an element has a value not permitted by the contract.

These templates are used by Context classes and validation logic to produce
clear and consistent error messages during runtime or CLI contract validation.
"""

class Errors:
    """
    Central repository for error messages used in ImportSpy’s validation engine.

    Each validation error extends one of three base templates:
    - ELEMENT_MISSING: used when an expected item is missing entirely.
    - ELEMENT_MISMATCH: used when a found item differs from the declared value.
    - ELEMENT_INVALID: used when the value is not allowed from a predefined set.
    """

    # General Warnings
    ANALYSIS_RECURSION_WARNING = (
        "Warning: Analysis recursion detected. Avoid analyzing code that itself handles analysis, "
        "to prevent stack overflow or performance issues."
    )

    # Generic Error Templates
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

    # Specific Module-Level Validations (not scoped by Context)
    FILENAME_MISMATCH = ELEMENT_MISMATCH.format(
        "The module filename", "{0}", "{1}"
    )
    VERSION_MISMATCH = ELEMENT_MISMATCH.format(
        "The module version", "{0}", "{1}"
    )

    # Function and Class Validations
    FUNCTION_RETURN_ANNOTATION_MISMATCH = ELEMENT_MISMATCH.format(
        "The return annotation of {0} '{1}'", "{2}", "{3}"
    )
    CLASS_MISSING = ELEMENT_MISSING.format('The class "{0}"')
    CLASS_SUPERCLASS_MISSING = ELEMENT_MISSING.format(
        'The superclass "{0}" in class "{1}"'
    )

    # Runtime / Environment Constraint Violations
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
