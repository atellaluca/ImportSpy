from pydantic import BaseModel
from typing import Optional, List
from types import ModuleType


class FunctionModel(BaseModel):
    """
    Model representing a function within a module.

    :param name: The name of the function. It can be `None` if the name is not available.
    :type name: Optional[str]

    :example:
        function = FunctionModel(name="my_function")
    """
    name: Optional[str] = None


class ClassModel(BaseModel):
    """
    Model representing a class within a module.

    :param name: The name of the class. It can be `None` if the name is not available.
    :type name: Optional[str]

    :param methods: A list of method names defined in the class. Defaults to an empty list.
    :type methods: Optional[List[str]]

    :param superclasses: A list of names of the superclasses from which this class inherits. Defaults to an empty list.
    :type superclasses: Optional[List[str]]

    :example:
        class_model = ClassModel(name="MyClass", methods=["method1", "method2"], superclasses=["BaseClass"])
    """
    name: Optional[str] = None
    methods: Optional[List[str]] = []
    superclasses: Optional[List[str]] = []


class SpyModel(BaseModel):
    """
    Model representing metadata of a module, including information about its functions and classes.

    :param name: The name of the module. It can be `None` if the name is not available.
    :type name: Optional[str]

    :param version: The version of the module. It can be `None` if the version is not available.
    :type version: Optional[str]

    :param author: The name of the author of the module. It can be `None` if the author information is not available.
    :type author: Optional[str]

    :param functions: A list of functions defined in the module, represented by the `FunctionModel`. Defaults to an empty list.
    :type functions: Optional[List[FunctionModel]]

    :param classes: A list of classes defined in the module, represented by the `ClassModel`. Defaults to an empty list.
    :type classes: Optional[List[ClassModel]]

    :param superclasses: A list of superclasses from which module-level classes inherit. Defaults to an empty list.
    :type superclasses: Optional[List[str]]

    :example:
        spy_model = SpyModel(
            name="MyModule",
            version="1.0.0",
            author="John Doe",
            functions=[FunctionModel(name="my_function")],
            classes=[ClassModel(name="MyClass", methods=["my_method"], superclasses=["BaseClass"])]
        )
    """
    name: Optional[str] = None
    version: Optional[str] = None
    author: Optional[str] = None
    functions: Optional[List[FunctionModel]] = []
    classes: Optional[List[ClassModel]] = []
    superclasses: Optional[List[str]] = []
