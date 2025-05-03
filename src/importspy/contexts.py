"""
importspy.context
=================

This module defines context-aware validation classes used in ImportSpy
to generate precise and meaningful error messages during contract enforcement.

Each context class encapsulates the structural role of an element
(such as a variable, function argument, or class attribute) and provides
methods to render human-readable labels and formatted error strings.

By localizing the rendering logic and scope-specific semantics,
these classes ensure clarity, traceability, and consistency in validation reports.

These context-aware abstractions are essential to separate structural expectations
from dynamic enforcement, giving ImportSpy the ability to issue expressive,
actionable diagnostics across scopes and validation levels.
"""

from typing import Union, Sequence
from .errors import Errors
from .constants import Constants


class Context:
    """
    Abstract base class for all validation contexts in ImportSpy.

    A context defines the semantic and structural scope of an element under validation.
    It provides interface methods for generating context-aware error messages
    related to missing, mismatched, or invalid elements.
    """

    def __init__(self, scope: str):
        """
        Parameters
        ----------
        scope : str
            A Scope constant string that identifies the validation context type.
        """
        self.scope = scope


class SimpleVariableContext(Context):
    """
    Context for variables without type annotations.

    Typically used for simple key-value definitions such as environment variables,
    module-level constants, or untyped configuration fields.
    """

    def __init__(self):
        super().__init__(Constants.SCOPE_ENVIRONMENT)

    def render_label(self, name: str) -> str:
        """
        Create a human-readable label for the variable.

        Parameters
        ----------
        name : str
            The name of the variable.

        Returns
        -------
        str
            A formatted string like 'The environment variable "FOO"'.
        """
        return f'The environment variable "{name}"'

    def format_missing_error(self, name: str) -> str:
        return Errors.ELEMENT_MISSING.format(self.render_label(name))

    def format_mismatch_error(self, name: str, expected: str, actual: str) -> str:
        return Errors.ELEMENT_MISMATCH.format(self.render_label(name), expected, actual)

    def format_invalid_error(self, name: str, allowed: Union[Sequence[str], str], found: str) -> str:
        return Errors.ELEMENT_INVALID.format(self.render_label(name), allowed, found)


class TypedVariableContext(SimpleVariableContext):
    """
    Context for typed variables defined in code.

    Used for variables with type annotations, validated both for declared value
    and expected type compliance.
    """

    def __init__(self):
        super().__init__(Constants.SCOPE_VARIABLE)

    def render_label(self, name: str) -> str:
        """
        Create a human-readable label for the variable.

        Parameters
        ----------
        name : str
            The name of the variable.

        Returns
        -------
        str
            A formatted string like 'The variable "x"'.
        """
        return f'The variable "{name}"'

    def format_invalid_error(self, allowed: Union[Sequence[str], str], found: str) -> str:
        return Errors.ELEMENT_INVALID.format("The annotation", allowed, found)


class AttributeContext(TypedVariableContext):
    """
    Context for object or class attributes.

    Used when validating attributes that belong to classes or their instances,
    whether typed or not.
    """

    def __init__(self, classname: str):
        self.classname = classname
        super().__init__(Constants.SCOPE_CLASS_ATTRIBUTE)

    def render_label(self, type: str, name: str) -> str:
        """
        Create a human-readable label for a class or instance attribute.

        Parameters
        ----------
        type : str
            The attribute type ("class" or "instance").
        name : str
            The attribute name.

        Returns
        -------
        str
            A formatted string like 'The class attribute "foo" of class MyClass'.
        """
        return f'The {type} attribute "{name}" of class {self.classname}'


class FunctionArgumentContext(AttributeContext):
    """
    Context for arguments declared in functions.

    It includes the name of the function to provide scope-specific error messaging
    for each declared parameter.
    """

    def __init__(self, function_name: str):
        self.function_name = function_name
        super().__init__(Constants.SCOPE_FUNCTION_ARG)

    def render_label(self, name: str) -> str:
        """
        Create a label for a function argument.

        Parameters
        ----------
        name : str
            Argument name.

        Returns
        -------
        str
            A formatted string like 'The argument "x" of function "process"'.
        """
        return f'The argument "{name}" of function "{self.function_name}"'


class MethodArgumentContext(FunctionArgumentContext):
    """
    Context for arguments declared in class methods.

    Adds class name to scope representation to form fully qualified labels.
    """

    def __init__(self, classname: str):
        self.classname = classname
        super().__init__(Constants.SCOPE_METHOD_ARG_IN_CLASS)

    def render_label(self, name: str, method_name: str) -> str:
        """
        Create a label for a method argument within a class.

        Parameters
        ----------
        name : str
            Argument name.
        method_name : str
            Method name.

        Returns
        -------
        str
            A formatted string like 'The argument "id" of method "save" of class "User"'.
        """
        return (
            f'The argument "{name}" of method "{method_name}" '
            f'of class "{self.classname}"'
        )
