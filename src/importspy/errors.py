"""
importspy.errors
=================

Centralized error messaging for ImportSpy's validation system.

The `Errors` class collects all exceptions and warning messages raised during 
ImportSpy's inspection and validation process. This includes structural mismatches, 
runtime violations, and argument inconsistencies found during contract enforcement.

By consolidating these messages into a single location:

- Developers can reuse consistent, human-readable phrasing across the codebase.
- Error strings are easier to update and internationalize.
- Each message includes placeholders (`{0}`, `{1}`, etc.) to inject context-specific
  information at runtime, making diagnostics more informative.

These messages are primarily raised when validating Python modules against their
import contracts (usually defined in `.yml` files).

Categories covered:
-------------------
- 🔁 General Warnings (e.g., recursion detection)
- 📦 Module & Variable Validation
- 🧩 Function, Class & Inheritance Validation
- ⚙️  Runtime Context Validation (OS, architecture, version)
- 🧪 Annotation and Type Constraints

Usage:
------

.. code-block:: python

    from importspy.errors import Errors

    raise ValueError(
        Errors.CLASS_ATTRIBUTE_MISSING.format("extension_name", "Extension")
    )
"""

class Errors:
    
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