from pydantic import BaseModel
from typing import (
    Optional, 
    List
)
from types import ModuleType
from .utils import spy_module_utils
import logging

logger = logging.getLogger("/".join(__file__.split('/')[-2:]))
logger.addHandler(logging.NullHandler())

class ClassModel(BaseModel):
    """
    A data model that defines the structure of a class within a Python module, allowing the developer to 
    proactively specify the expected structure of the class for external modules that import their code.

    `ClassModel` is part of the **proactive programming** approach enabled by `ImportSpy`, where developers 
    define in advance how imported modules should be structured, ensuring proper integration and usage.

    ## Attributes:
    - **name** (`str`): The name of the class. This field is required and must uniquely identify the class.
    - **class_attr* (`Optional[List[str]]`): A list of class attributes names that are expected to be present in the class. Defaults to an empty list.
    - *instance_attr* (`Optional[List[str]]`): A list of class isntance attributes names that are expected to be present in the class. Defaults to an empty list.
    - **methods** (`Optional[List[str]]`): A list of method names that are expected to be present in the class. Defaults to an empty list.
    - **superclasses** (`Optional[List[str]]`): A list of names of the superclasses from which this class inherits. Defaults to an empty list.

    ## Example:
    ```python
    class_model = ClassModel(
        name="MyClass",
        methods=["method1", "method2"],
        superclasses=["BaseClass"]
    )
    ```
    This defines a `ClassModel` where a class named `MyClass` is expected to have two methods (`method1`, `method2`) 
    and inherit from `BaseClass`. External modules importing your code can then be validated to follow this structure.
    """
    name: str
    class_attr: Optional[List[str]] = []
    instance_attr: Optional[List[str]] = []
    methods: Optional[List[str]] = []
    superclasses: Optional[List[str]] = []

class SpyModel(BaseModel):
    """
    A model that defines the expected structure of a Python module, allowing developers to declare in advance 
    how external modules that import their code should be organized, promoting **proactive programming**.

    `SpyModel` allows you to describe the expected metadata of a module, such as its functions, classes, and version, 
    ensuring that external modules adhere to the correct structure and usage of your code.

    ## Attributes:
    - **filename** (`Optional[str]`): The name of the module file. If the name is unavailable, it can be `None`. Defaults to `None`.
    - **version** (`Optional[str]`): The expected version of the module. Defaults to `None` if the version is not available.
    - **variables** (`Optional[dict]`): A dictionary of variables expected to be defined within the module. Each key represents the name of the variable, and its corresponding value represents the expected value. Defaults to an empty dictionary.
    - **functions** (`Optional[List[str]]`): A list of function names that are expected to be defined within the module. Defaults to an empty list.
    - **classes** (`Optional[List[ClassModel]]`): A list of class definitions within the module, represented by `ClassModel`. Defaults to an empty list.
    - **env_vars** (`Optional[dict]`):  A dictionary representing required environment variables. Each key is the variable name, and the corresponding value is the expected value. Defaults to an empty dictionary.

    ## Example:
    ```python
    spy_model = SpyModel(
        filename="MyModule.py",
        version="1.0.0",
        functions=["my_function"],
        classes=[
            ClassModel(name="MyClass", methods=["my_method"], superclasses=["BaseClass"])
        ],
        env_vars={"CI":"true", "GITHUB_ACTIONS:"true"}
    )
    ```
    This defines a `SpyModel` for a module called `MyModule.py`, version 1.0.0, that is expected to include a function 
    `my_function` and a class `MyClass` with a method `my_method`, inheriting from `BaseClass`. This model can be used to 
    validate external modules importing your code, ensuring that they follow this structure.

    ## Class Method:
    ### from_module(info_module: ModuleType) -> SpyModel:
    This method extracts metadata from an imported module and populates a `SpyModel` instance with the expected structure, 
    such as the module's filename, version, functions, and classes.

    - **Args**:
        - `info_module` (`ModuleType`): The module from which to extract the metadata.

    - **Returns**:
        - `SpyModel`: A `SpyModel` object that represents the structure and metadata of the given module, ready to be used 
          for validation.

    ## Example:
    ```python
    spy_model = SpyModel.from_module(my_module)
    ```
    This will extract the necessary metadata from `my_module` and create a `SpyModel` instance that describes the module's 
    structure, which can then be compared to the expected structure defined by the developer.
    """
    filename: Optional[str] = ""
    version: Optional[str] = ""
    variables: Optional[dict] = {}
    functions: Optional[List[str]] = []
    classes: Optional[List[ClassModel]] = []
    env_vars: Optional[dict] = {}

    @classmethod
    def from_module(cls, info_module: ModuleType):
        """
        Dynamically extracts metadata from a Python module and creates a `SpyModel` that represents 
        its structure.

        This method allows developers to proactively define the structure of modules that import their 
        code by extracting information like filename, version, functions, and classes, and populating a 
        `SpyModel` instance. This ensures that external modules adhere to the expected structure when they 
        interact with the developer's code.

        ## Parameters:
        - **info_module** (`ModuleType`): The Python module from which to extract the metadata.

        ## Returns:
        - **SpyModel**: A `SpyModel` populated with metadata such as the module's filename, version, functions, 
          and classes, based on the given module.

        ## Example:
        ```python
        spy_model = SpyModel.from_module(my_module)
        ```
        This extracts the metadata from `my_module` and creates a `SpyModel` instance that reflects the module's 
        structure, which can then be used for validation against a predefined model.
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
        spy_module_utils.unload_module(info_module)
        logger.debug("Unload module")
        logger.debug(f"filename: {filename}, version: {version}, \
                     functions: {functions}, classes: {classes}")
        return cls(
            filename=filename,
            version=version,
            variables=variables,
            functions=functions,
            classes=classes,
            env_vars=env_vars
        )

