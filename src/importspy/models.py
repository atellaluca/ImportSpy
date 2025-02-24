from pydantic import (
    BaseModel,
    field_validator,
    Field
)
from .mixins.annotations_validator_mixin import AnnotationValidatorMixin
from typing import (
    Optional, 
    List,
    Union
)
from types import ModuleType
from .utilities.module_util import (
    ModuleUtil, 
    ClassInfo,
    ArgumentInfo,
    FunctionInfo,
    AttributeInfo
)
from .utilities.runtime_util import RuntimeUtil
from .utilities.system_util import SystemUtil
from .utilities.python_util import PythonUtil
from .constants import Constants
from .errors import Errors
import logging

logger = logging.getLogger("/".join(__file__.split('/')[-2:]))
logger.addHandler(logging.NullHandler())

class Python(BaseModel):
    """
    Represents the Python runtime configuration for module validation.

    This class encapsulates details about the Python runtime, such as version, interpreter type, 
    and available modules. It ensures that the execution environment aligns with predefined 
    validation criteria.

    :param version: (Optional) The Python version (e.g., `"3.8"`, `"3.10"`).
    :type version: Optional[str]
    :param interpreter: (Optional) The type of Python interpreter (e.g., `"CPython"`, `"PyPy"`).
    :type interpreter: Optional[str]
    :param modules: A list of modules available in the runtime.
    :type modules: List['Module']

    :raises ValueError: If the Python version or interpreter is unsupported.

    **Example Usage:**
    
    .. code-block:: python

        python_env = Python(version="3.10", interpreter="CPython", modules=[Module(filename="my_module.py")])
    
    .. seealso:: `System`, `Runtime`
    """
    version: Optional[str] = None
    interpreter: Optional[str] = None
    modules: List['Module']

class System(BaseModel):
    """
    Represents the system configuration, including the OS, environment variables, and Python runtimes.

    :param os: The operating system (`"Linux"`, `"Windows"`, `"macOS"`).
    :type os: str
    :param envs: Dictionary of required environment variables and expected values.
    :type envs: dict
    :param pythons: List of Python runtime configurations available on the system.
    :type pythons: List[Python]

    :raises ValueError: If the specified OS is not supported.

    **Example Usage:**
    
    .. code-block:: python

        system_env = System(os="Linux", envs={"ENV_VAR": "value"}, pythons=[Python(version="3.10")])
    
    .. warning:: Ensure all required environment variables are correctly set to prevent runtime issues.
    
    .. seealso:: `Python`, `Runtime`
    """
    os: str
    envs: dict = Field(default=None, repr=False)
    pythons: List[Python]

    @field_validator('os')
    def validate_os(cls, value: str):
        if value not in Constants.SUPPORTED_OS:
            raise ValueError(Errors.INVALID_OS.format(value, Constants.SUPPORTED_OS))
        return value

class Runtime(BaseModel):
    """
    Represents the runtime configuration, including CPU architecture and associated systems.

    This class enables validation of Python modules based on the target architecture.

    :param arch: The CPU architecture (`"x86_64"`, `"ARM64"`).
    :type arch: str
    :param systems: A list of system configurations associated with this runtime.
    :type systems: List[System]

    :raises ValueError: If the architecture is unsupported.

    **Example Usage:**
    
    .. code-block:: python

        runtime_env = Runtime(arch="ARM64", systems=[System(os="Linux")])
    
    .. note:: This class is particularly useful for cross-platform compatibility checks.
    
    .. seealso:: `System`
    """
    arch: str
    systems: List[System]

    @field_validator('arch')
    def validate_arch(cls, value: str):
        if value not in Constants.KNOWN_ARCHITECTURES:
            raise ValueError(Errors.INVALID_ARCHITECTURE.format(value, Constants.KNOWN_ARCHITECTURES))
        return value

class Attribute(AnnotationValidatorMixin, BaseModel):
    """
    Represents an attribute within a Python class for validation purposes.

    This class provides a structured way to validate class attributes, including type, 
    name, optional annotations, and default values.

    :param type: The category of the attribute (e.g., `"class-level"`, `"instance-level"`).
    :type type: str
    :param name: The name of the attribute.
    :type name: str
    :param annotation: (Optional) The expected type annotation of the attribute.
    :type annotation: Optional[str]
    :param value: (Optional) The default value of the attribute.
    :type value: Optional[Union[int, str, float, bool, None]]

    :raises ValueError: If the attribute type is not among the supported types.

    **Example Usage:**
    
    .. code-block:: python

        attr = Attribute(type="class-level", name="id", annotation="int", value=123)

    .. note:: This class enforces validation using the `AnnotationValidatorMixin`.
    """
    type: str
    name: str
    annotation: Optional[str] = None
    value: Optional[Union[int, str, float, bool, None]] = None

    @field_validator('type')
    def validate_arch(cls, value: str):
        """Validates the `type` field to ensure it matches supported attribute types."""
        if value not in Constants.SUPPORTED_CLASS_ATTRIBUTE_TYPES:
            raise ValueError(Errors.INVALID_ATTRIBUTE_TYPE.format(value, Constants.SUPPORTED_CLASS_ATTRIBUTE_TYPES))
        return value
    
    @field_validator("annotation")
    def validate_annotation(cls, value):
        """Validates the annotation field using `AnnotationValidatorMixin`."""
        return super().validate_annotation(value)
    
    @classmethod
    def from_attributes_info(cls, attributes_info: List[AttributeInfo]):
        """
        Creates a list of `Attribute` instances from extracted metadata.

        :param attributes_info: A list of extracted attribute information.
        :type attributes_info: List[AttributeInfo]
        :return: A list of `Attribute` objects.
        :rtype: List[Attribute]
        """
        return [Attribute(
            type=attr_info.type,
            name=attr_info.name,
            value=attr_info.value,
            annotation=attr_info.annotation
        ) for attr_info in attributes_info]

class Argument(AnnotationValidatorMixin, BaseModel):
    """
    Represents a function parameter in Python for validation.

    :param name: The name of the function parameter.
    :type name: str
    :param annotation: (Optional) The expected type annotation for the parameter.
    :type annotation: Optional[str]
    :param value: (Optional) The default value assigned to the parameter.
    :type value: Optional[Union[str, int, float, bool, list, dict]]

    :raises ValueError: If the annotation is invalid.

    **Example Usage:**
    
    .. code-block:: python

        arg = Argument(name="timeout", annotation="int", value=30)
    """
    name: str
    annotation: Optional[str] = None
    value: Optional[Union[str, int, float, bool, list, dict]] = None

    @field_validator("annotation")
    def validate_annotation(cls, value):
        """Validates the annotation field using `AnnotationValidatorMixin`."""
        return super().validate_annotation(value)
    
    @classmethod
    def from_arguments_info(cls, arguments_info: List[ArgumentInfo]):
        """
        Converts extracted function parameters into `Argument` instances.

        :param arguments_info: A list of extracted argument metadata.
        :type arguments_info: List[ArgumentInfo]
        :return: A list of `Argument` objects.
        :rtype: List[Argument]
        """
        return [Argument(
            name=arg_info.name,
            annotation=arg_info.annotation,
            value=arg_info.value
        ) for arg_info in arguments_info]

class Function(AnnotationValidatorMixin, BaseModel):
    """
    Represents a function structure in Python, including its name, parameters, and return type.

    :param name: The name of the function.
    :type name: str
    :param arguments: (Optional) A list of parameters accepted by the function.
    :type arguments: Optional[List[Argument]]
    :param return_annotation: (Optional) The expected return type of the function.
    :type return_annotation: Optional[str]

    :raises ValueError: If the return annotation is invalid.

    **Example Usage:**
    
    .. code-block:: python

        func = Function(
            name="compute",
            arguments=[Argument(name="x", annotation="int")],
            return_annotation="float"
        )
    """
    name: str
    arguments: Optional[List[Argument]] = None
    return_annotation: Optional[str] = None

    @field_validator("return_annotation")
    def validate_annotation(cls, value):
        """Validates the return annotation field using `AnnotationValidatorMixin`."""
        return super().validate_annotation(value)
    
    @classmethod
    def from_functions_info(cls, functions_info: List[FunctionInfo]):
        """
        Converts extracted function metadata into `Function` instances.

        :param functions_info: A list of extracted function information.
        :type functions_info: List[FunctionInfo]
        :return: A list of `Function` objects.
        :rtype: List[Function]
        """
        return [Function(
            name=func_info.name,
            arguments=Argument.from_arguments_info(func_info.arguments),
            return_annotation=func_info.return_annotation
        ) for func_info in functions_info]
    
class Class(BaseModel):
    """
    Represents a Python class structure, including its attributes, methods, and superclasses.

    :param name: The name of the class.
    :type name: str
    :param attributes: (Optional) A list of attributes associated with the class.
    :type attributes: Optional[List[Attribute]]
    :param methods: (Optional) A list of methods belonging to the class.
    :type methods: Optional[List[Function]]
    :param superclasses: (Optional) A list of superclasses inherited by this class.
    :type superclasses: Optional[List[str]]

    **Example Usage:**
    
    .. code-block:: python

        cls = Class(
            name="User",
            attributes=[Attribute(name="id", type="class-level", annotation="int")],
            methods=[Function(name="get_name", return_annotation="str")]
        )
    """
    name: str
    attributes: Optional[List[Attribute]] = None
    methods: Optional[List[Function]] = None
    superclasses: Optional[List[str]] = None

    @classmethod
    def _from_class_info(cls, extracted_classes: List[ClassInfo]):
        """
        Converts extracted class metadata into `Class` instances.

        :param extracted_classes: A list of extracted class information.
        :type extracted_classes: List[ClassInfo]
        :return: A list of `Class` objects.
        :rtype: List[Class]
        """
        return [Class(
            name=name,
            attributes=Attribute.from_attributes_info(attributes),
            methods=Function.from_functions_info(methods),
            superclasses=superclasses
        ) for name, attributes, methods, superclasses in extracted_classes]

class Module(BaseModel):
    """
    Represents a Python module, containing its metadata, functions, and classes.

    :param filename: The filename or path of the module.
    :type filename: str
    :param version: (Optional) The version of the module, if available.
    :type version: Optional[str]
    :param variables: (Optional) Dictionary of global variables within the module.
    :type variables: Optional[dict]
    :param functions: (Optional) A list of functions defined in the module.
    :type functions: Optional[List[Function]]
    :param classes: (Optional) A list of classes defined in the module.
    :type classes: Optional[List[Class]]

    **Example Usage:**
    
    .. code-block:: python

        mod = Module(filename="mymodule.py", version="1.0", functions=[], classes=[])
    """
    filename: str
    version: Optional[str] = None
    variables: Optional[dict] = None
    functions: Optional[List[Function]] = None
    classes: Optional[List[Class]] = None

class SpyModel(Module):
    """
    Defines constraints for a Python module, independent of the runtime.

    This class extends `Module`, allowing developers to define expectations for module structure, 
    deployment environments, and runtime compatibility.

    :param deployments: A list of runtime deployments associated with this SpyModel.
    :type deployments: Optional[List[Runtime]]

    **Method Summary:**
    
    - :meth:`from_module` → Creates a SpyModel from a Python module.

    **Example Usage:**
    
    .. code-block:: python

        import my_module
        spy_model = SpyModel.from_module(my_module)

    .. warning:: This class should be used when strict module validation is required.

    .. seealso:: `Module`, `Runtime`
    """
    deployments: Optional[List[Runtime]] = None

    @classmethod
    def from_module(cls, info_module: ModuleType):
        """
        Constructs a `SpyModel` from a Python module.

        This method extracts metadata such as functions, classes, and variables
        from the provided module, along with runtime details.

        :param info_module: The Python module to analyze.
        :type info_module: ModuleType
        :return: A `SpyModel` instance representing the module.
        :rtype: SpyModel
        :raises ValueError: If module metadata extraction fails.

        **Example Usage:**
        
        .. code-block:: python

            import my_module
            spy_model = SpyModel.from_module(my_module)
            print(spy_model)

        """
        module_utils = ModuleUtil()
        runtime_utils = RuntimeUtil()
        system_utils = SystemUtil()
        python_utils = PythonUtil()

        info_module = module_utils.load_module(info_module)
        logger.debug(f"Create SpyModel from info_module: {ModuleType}")

        filename = "/".join(info_module.__file__.split('/')[-1:])
        version = module_utils.extract_version(info_module)
        variables = module_utils.extract_variables(info_module)
        functions = module_utils.extract_functions(info_module)
        classes = Class._from_class_info(module_utils.extract_classes(info_module))

        arch = runtime_utils.extract_arch()
        os = system_utils.extract_os()
        python_version = python_utils.extract_python_version()
        interpreter = python_utils.extract_python_implementation()
        envs = system_utils.extract_envs()

        module_utils.unload_module(info_module)
        logger.debug("Unload module")

        return cls(
            filename=filename,
            deployments=[
                Runtime(
                    arch=arch,
                    systems=[
                        System(
                            os=os,
                            envs=envs,
                            pythons=[
                                Python(
                                    version=python_version,
                                    interpreter=interpreter,
                                    modules=[
                                        Module(
                                            filename=filename,
                                            version=version,
                                            variables=variables,
                                            functions=functions,
                                            classes=classes
                                        )
                                    ]
                                )
                            ]
                        ),
                    ]
                )
            ]
        )
