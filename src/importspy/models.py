from pydantic import BaseModel, field_validator
from typing import (
    Optional, 
    List
)
from types import ModuleType
from .utils import spy_module_utils
from .constants import Constants
from .errors import Errors
import logging

logger = logging.getLogger("/".join(__file__.split('/')[-2:]))
logger.addHandler(logging.NullHandler())

class ClassModel(BaseModel):
    """
    A model representing the expected structure of a Python class within a module.

    This class allows developers to specify the expected attributes, methods, and inheritance hierarchy 
    of a class, enabling validation of external modules to ensure adherence to these expectations.

    Attributes:
        name (str): The name of the class. This field is required and must uniquely identify the class.
        class_attr (Optional[List[str]]): A list of class attribute names expected to be defined. Defaults to an empty list.
        instance_attr (Optional[List[str]]): A list of instance attribute names expected to be defined. Defaults to an empty list.
        methods (Optional[List[str]]): A list of method names expected to be defined in the class. Defaults to an empty list.
        superclasses (Optional[List[str]]): A list of superclass names from which the class is expected to inherit. Defaults to an empty list.

    Example:
        ```python
        class_model = ClassModel(
            name="MyClass",
            methods=["method1", "method2"],
            superclasses=["BaseClass"]
        )
        ```
        This defines a `ClassModel` for a class named `MyClass`, which is expected to have two methods (`method1`, `method2`) 
        and inherit from `BaseClass`.
    """

    name: str
    class_attr: Optional[List[str]] = []
    instance_attr: Optional[List[str]] = []
    methods: Optional[List[str]] = []
    superclasses: Optional[List[str]] = []

class SpyModule(BaseModel):
    """
    A model defining the expected structure and metadata of a Python module.

    This class provides a framework for declaring the expected elements of a module, such as its filename, 
    version, variables, functions, and classes. It supports validation of external modules against these 
    expectations.

    Attributes:
        filename (Optional[str]): The name of the module file. Defaults to `None`.
        version (Optional[str]): The expected version of the module. Defaults to `None`.
        variables (Optional[dict]): A dictionary of expected variables in the module. Defaults to an empty dictionary.
        functions (Optional[List[str]]): A list of function names expected in the module. Defaults to an empty list.
        classes (Optional[List[ClassModel]]): A list of expected class structures, represented by `ClassModel`. Defaults to an empty list.
        env_vars (Optional[dict]): A dictionary of required environment variables. Defaults to an empty dictionary.

    Example:
        ```python
        spy_module = SpyModule(
            filename="MyModule.py",
            version="1.0.0",
            functions=["my_function"],
            classes=[
                ClassModel(name="MyClass", methods=["my_method"], superclasses=["BaseClass"])
            ],
            env_vars={"CI": "true"}
        )
        ```
        This defines a `SpyModule` for a module named `MyModule.py`, version 1.0.0, expected to contain a function 
        `my_function` and a class `MyClass` with specific attributes and methods.
    """

    filename: Optional[str] = ""
    version: Optional[str] = ""
    variables: Optional[dict] = {}
    functions: Optional[List[str]] = []
    classes: Optional[List[ClassModel]] = []
    env_vars: Optional[dict] = {}

class SpyArchModule(BaseModel):

    """
    A model for validating a module's compatibility with a specific system architecture.

    This class combines a module definition (`SpyModule`) with a system architecture (`arch`), ensuring 
    that the module meets the requirements for the given architecture.

    Attributes:
        arch (str): The architecture for which the module is validated. Must be one of the `Constants.KNOWN_ARCHITECTURES`.
        module (SpyModule): The module definition being validated for the given architecture.

    Validators:
        validate_arch: Ensures that the provided architecture is recognized within `Constants.KNOWN_ARCHITECTURES`.

    Raises:
        ValueError: If the provided architecture is not recognized.

    Example:
        ```python
        spy_arch_module = SpyArchModule(
            arch="x86_64",
            module=SpyModule(
                filename="example.py",
                functions=["example_function"]
            )
        )
        ```
        This defines a `SpyArchModule` for an `x86_64` architecture with a module `example.py` containing the function `example_function`.
    """
    
    arch: str
    module: SpyModule

    @field_validator('arch')
    def validate_arch(cls, value:str):
        if value not in Constants.KNOWN_ARCHITECTURES:
            raise ValueError(Errors.INVALID_ARCHITECTURE.format(value, Constants.KNOWN_ARCHITECTURES))
        return value

class SpyModel(SpyModule):

    """
    An extension of `SpyModule` that supports architecture-specific validations via `SpyArchModule`.

    This class provides the ability to associate a module definition with multiple architecture-specific validations, 
    enabling a more comprehensive representation of a module's compatibility across different environments.

    Attributes:
        spies (Optional[List[SpyArchModule]]): A list of `SpyArchModule` instances representing architecture-specific 
            module validations. Defaults to an empty list.

    Class Methods:
        from_module(info_module: ModuleType) -> SpyModel:
            Extracts metadata from a Python module and creates a `SpyModel` instance representing its structure and metadata.

    Example:
        ```python
        spy_model = SpyModel.from_module(my_module)
        ```
        This extracts metadata from `my_module` and creates a `SpyModel` instance, which can then be used to validate 
        external modules against a predefined structure.
    """

    spies: Optional[List[SpyArchModule]] = []

    @classmethod
    def from_module(cls, info_module: ModuleType):
        """
        Dynamically extracts metadata from a Python module and creates a `SpyModel` instance representing 
        its structure and expected metadata.
    
        This method is designed to automate the process of generating a `SpyModel` by introspecting an 
        existing Python module. It collects metadata such as the module's filename, version, variables, 
        functions, and classes, along with environment variables and architecture information, to build a 
        comprehensive `SpyModel`.
    
        Parameters:
            info_module (ModuleType): The Python module to introspect and extract metadata from.
    
        Returns:
            SpyModel: An instance of `SpyModel` populated with metadata from the provided module.
    
        Raises:
            ImportError: If the specified module cannot be loaded.
            ValueError: If the extracted metadata does not meet the `SpyModel` requirements.
    
        Steps:
            1. Load the module using `spy_module_utils.load_module`.
            2. Extract metadata such as filename, version, variables, functions, and classes.
            3. Validate architecture compatibility using `SpyArchModule`.
            4. Unload the module to prevent resource leakage.
    
        Example:
            ```python
            import my_module
            spy_model = SpyModel.from_module(my_module)
            ```
            This extracts the metadata from `my_module` and creates a `SpyModel` instance that reflects 
            its structure. The returned `SpyModel` can then be used for validation or other integration checks.
    
        Notes:
            - This method uses utility functions from `spy_module_utils` to extract metadata efficiently.
            - Ensure that the module being analyzed does not create circular dependencies or recursion issues.
        """
        info_module = spy_module_utils.load_module(info_module)
        logger.debug(f"Create SpyModel from info_module: {ModuleType}")
        filename = "/".join(info_module.__file__.split('/')[-1:])
        version = spy_module_utils.extract_version(info_module)
        variables = spy_module_utils.extract_variables(info_module)
        functions = spy_module_utils.extract_functions(info_module)
        classes = [
            ClassModel(name=name, 
                       class_attr=class_attr, 
                       instance_attr=instance_attr,
                       methods=methods,
                       superclasses=superclasses)
            for 
            name,
            class_attr,
            instance_attr,
            methods,
            superclasses 
            in spy_module_utils.extract_classes(info_module)
        ]
        env_vars = spy_module_utils.extract_env_vars()
        arch = spy_module_utils.extract_arch()
        spy_module_utils.unload_module(info_module)
        logger.debug("Unload module")
        logger.debug(f"filename: {filename}, version: {version}, \
                     functions: {functions}, classes: {classes}")
        return cls(
            spies = [
                SpyArchModule(
                    arch=arch,
                    module=SpyModule(
                        
                    )
                )
            ],
            filename=filename,
            version=version,
            variables=variables,
            functions=functions,
            classes=classes,
            env_vars=env_vars
        )
