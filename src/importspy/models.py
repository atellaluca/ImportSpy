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
    ClassInfo
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

    The `Python` class provides a structured representation of a Python runtime, including 
    its version, interpreter type, and associated modules. It is designed to facilitate 
    runtime-specific validations within the broader context of a system or deployment.

    Attributes:
    -----------
    version : Optional[str]
        The version of the Python runtime (e.g., `3.8`, `3.10`). Optional to allow flexibility 
        in scenarios where specific versions are not strictly required.
    interpreter : Optional[str]
        The type of Python interpreter used (e.g., `CPython`, `PyPy`, `Jython`). Optional to 
        accommodate cases where any interpreter is acceptable.
    modules : List['Module']
        A list of modules available within this Python runtime. These modules are subject to 
        validation based on the constraints defined in the corresponding `SpyModel`.

    Customization and Flexibility:
    ------------------------------
    The optional fields (`version` and `interpreter`) enable developers to:
    - Define only the runtime details that are relevant to their validation needs.
    - Support diverse Python environments without imposing rigid constraints.

    Use Case:
    ---------
    The `Python` class is ideal for scenarios where Python modules need to:
    - Validate compatibility with specific Python versions or interpreters.
    - Ensure that the required modules are present within the runtime.
    - Integrate seamlessly with system-level and deployment-level validation workflows.

    Validation Details:
    -------------------
    - **Version Matching**: Ensures the Python runtime matches the expected version when specified.
    - **Interpreter Discrimination**: Enables targeted validations for specific Python implementations.
    - **Module Validation**: Associates modules with the runtime for comprehensive validation.

    Integration:
    ------------
    The `Python` class integrates with system-level and runtime-level configurations, ensuring 
    that Python-specific constraints are respected during module execution.
    """

    version: Optional[str] = None
    interpreter: Optional[str] = None
    modules: List['Module']

class System(BaseModel):
    """
    Represents the system configuration for Python modules, including environment variables and operating system details.

    The `System` class provides a structured way to define and validate the system context 
    in which a Python module is executed. This includes the operating system, required 
    environment variables, and associated Python runtime configurations.

    Attributes:
    -----------
    os : str
        The operating system where the module is executed (e.g., `Linux`, `Windows`, `macOS`). 
        This allows discrimination and validation based on the target OS.
    envs : dict
        A dictionary of required environment variables and their expected values. These variables 
        ensure the system has the necessary configurations for the module's execution. 
        Defaults to an empty dictionary to allow flexibility.
    pythons : List[Python]
        A list of `Python` configurations available on the system, enabling runtime-specific 
        validation for multiple Python environments.

    Customization and Flexibility:
    ------------------------------
    The optional fields (`envs` and `pythons`) provide developers with the flexibility to:
    - Specify only the required details for their use case.
    - Adapt validations to different system contexts without enforcing unnecessary constraints.

    Use Case:
    ---------
    The `System` class is ideal for scenarios where Python modules need to:
    - Ensure the presence of specific environment variables before execution.
    - Validate compatibility with a target operating system.
    - Support multiple Python versions or implementations available on the system.

    Validation Details:
    -------------------
    - **Operating System Discrimination**: Enables targeted validations for specific OS types.
    - **Environment Variables Validation**: Ensures that all required environment variables 
      are defined and meet the expected criteria.
    - **Python Runtime Validation**: Associates multiple Python environments with the system 
      for comprehensive validation.

    Integration:
    ------------
    The `System` class integrates seamlessly with runtime-level and module-level validation, 
    ensuring that system-specific constraints are respected during execution.
    """
    
    os: str = Optional(False)
    envs: dict = Field(default=False, repr=False)
    pythons: List[Python]

class Runtime(BaseModel):
    """
    Represents the runtime configuration for Python modules, focusing on CPU architecture and associated systems.

    The `Runtime` class provides a structured representation of the runtime environment, 
    including the CPU architecture and associated systems. It allows developers to customize 
    and adapt Python module validations based on the target architecture.

    Attributes:
    -----------
    arch : str
        The CPU architecture of the runtime environment (e.g., `x86_64`, `ARM64`). Must 
        match one of the supported architectures defined in `Constants.KNOWN_ARCHITECTURES`.
    systems : List[System]
        A list of systems associated with the runtime, each represented by the `System` model.

    Customization and Flexibility:
    ------------------------------
    This class enables developers to:
    - Define specific CPU architectures for which Python modules should be validated.
    - Customize system-level configurations based on the architecture, ensuring accurate 
      and context-sensitive validation.

    Methods:
    --------
    validate_arch(cls, value: str):
        Validates the `arch` field to ensure it matches one of the supported CPU architectures 
        defined in `Constants.KNOWN_ARCHITECTURES`. Raises a `ValueError` if the architecture 
        is invalid.

    Use Case:
    ---------
    The `Runtime` class is essential for scenarios where the validation of Python modules 
    needs to adapt based on the target CPU architecture. For example, developers working 
    on cross-platform or edge computing applications can define separate validations for 
    architectures like `x86_64`, `ARM64`, or `aarch64`.

    Validation Details:
    -------------------
    - **Architecture Validation**: Ensures the specified `arch` is valid and supported by 
      the application. Provides actionable feedback for unsupported architectures.
    - **System Validation**: Associates a list of `System` objects with the runtime, allowing 
      detailed system-level validation tailored to the architecture.

    Integration:
    ------------
    This class integrates seamlessly with the overall validation framework, enabling fine-grained 
    control over runtime configurations and their compliance with defined constraints.
    """
    
    arch: str
    systems: List[System]

    @field_validator('arch')
    def validate_arch(cls, value:str):
        if value not in Constants.KNOWN_ARCHITECTURES:
            raise ValueError(Errors.INVALID_ARCHITECTURE.format(value, Constants.KNOWN_ARCHITECTURES))
        return value

class Attribute(AnnotationValidatorMixin, BaseModel):
    """
    Represents a class attribute in Python for validation purposes.

    The `Attribute` class provides a structured representation of attributes within Python 
    classes, including their type, name, optional type annotation, and optional value. 
    It leverages the `AnnotationValidatorMixin` to enforce constraints on type annotations.

    Attributes:
    -----------
    type : str
        The category of the attribute (e.g., class-level or instance-level). Must conform to 
        the types specified in `Constants.SUPPORTED_CLASS_ATTRIBUTE_TYPES`.
    name : str
        The name of the attribute.
    annotation : Optional[str]
        The type annotation for the attribute, if provided.
    value : Optional[Union[int, str, float, bool, None]]
        The default value of the attribute, if specified.

    Optional Fields:
    ----------------
    The optional attributes (`annotation` and `value`) allow developers to customize the 
    validation process. This flexibility ensures developers can enforce constraints only on 
    the fields relevant to their specific use case.

    Methods:
    --------
    validate_arch(cls, value: str):
        Validates the `type` field to ensure it matches one of the supported attribute types 
        defined in `Constants.SUPPORTED_CLASS_ATTRIBUTE_TYPES`.

    validate_annotation(cls, value):
        Validates the `annotation` field using the `AnnotationValidatorMixin`. Ensures the 
        annotation adheres to expected types and is correctly formatted.

    Flexibility:
    ------------
    - Supports partial validation by allowing optional fields (`annotation`, `value`) to remain 
      unset when not required.
    - Enables precise validation of class attributes, ensuring compliance with defined constraints.

    Validation Details:
    -------------------
    - **Type Validation**: Ensures that the `type` attribute matches one of the supported types 
      defined in `Constants.SUPPORTED_CLASS_ATTRIBUTE_TYPES`. Raises a `ValueError` for invalid types.
    - **Annotation Validation**: Uses the `AnnotationValidatorMixin` to validate the `annotation` 
      field for consistency and correctness.
    """

    type: str
    name: str
    annotation: Optional[str] = None
    value: Optional[Union[int, str, float, bool, None]] = None

    @field_validator('type')
    def validate_arch(cls, value:str):
        if value not in Constants.SUPPORTED_CLASS_ATTRIBUTE_TYPES:
            raise ValueError(Errors.INVALID_ATTRIBUTE_TYPE.format(value, Constants.SUPPORTED_CLASS_ATTRIBUTE_TYPES))
        return value
    
    @field_validator("annotation")
    def validate_annotation(cls, value):
        return cls.validate_annotation(value)

class Argument(AnnotationValidatorMixin, BaseModel):
    """
    Represents the parameters of a Python function for validation purposes.

    The `Argument` class encapsulates metadata about a single function parameter, including its 
    name, type annotation, and optional default value. It integrates with the 
    `AnnotationValidatorMixin` to enforce constraints on type annotations.

    Attributes:
    -----------
    name : str
        The name of the function parameter.
    annotation : Optional[str]
        The type annotation for the parameter, if specified.
    value : Optional[Union[str, int, float, bool, list, dict]]
        The default value of the parameter, if provided.

    Optional Fields:
    ----------------
    The optional attributes (`annotation` and `value`) allow developers to customize the 
    validation process, enabling them to focus on specific aspects of a function's parameters 
    while ignoring others. This flexibility is particularly useful for context-specific or 
    partial validation.

    Methods:
    --------
    validate_annotation(cls, value):
        Validates the `annotation` field using the `AnnotationValidatorMixin`. Ensures that 
        the annotation adheres to expected types and is correctly formatted.

    Flexibility:
    ------------
    - Supports partial validation by allowing optional fields (`annotation`, `value`) to remain 
      unset if not required.
    - Enables precise validation of function parameters, ensuring compliance with expected 
      annotations and values.
    """

    name:str
    annotation: Optional[str] = None
    value: Optional[Union[str, int, float, bool, list, dict]] = None

    @field_validator("annotation")
    def validate_annotation(cls, value):
        return super().validate_annotation(value)

class Function(AnnotationValidatorMixin, BaseModel):
    """
    Represents the structure and behavior of a Python function for validation purposes.

    The `Function` class encapsulates metadata about a Python function, enabling developers to 
    validate its name, arguments, and return annotations. It integrates with the 
    `AnnotationValidatorMixin` to enforce constraints on annotations.

    Attributes:
    -----------
    name : str
        The name of the function.
    arguments : Optional[List[Argument]]
        A list of `Argument` instances representing the function's parameters. Each argument 
        includes details such as its name, annotation, and optional value.
    return_annotation : Optional[str]
        The return type annotation of the function, if specified.

    Optional Fields:
    ----------------
    The optional attributes (`arguments` and `return_annotation`) provide developers with 
    flexibility to tailor validation. This allows focusing on specific aspects of the function 
    while ignoring others, enabling precise and context-specific validation.

    Methods:
    --------
    validate_annotation(cls, value):
        Validates the `return_annotation` field using the `AnnotationValidatorMixin`. Ensures 
        that the annotation is valid and adheres to expected types.

    Flexibility:
    ------------
    - Supports partial validation by allowing optional fields (`arguments`, `return_annotation`) 
      to remain unset if not needed.
    - Enables detailed validation of function definitions, including parameter annotations and 
      return types.
    """

    name: str
    arguments: Optional[List[Argument]] = None
    return_annotation: Optional[str] = None

    @field_validator("return_annotation")
    def validate_annotation(cls, value):
        return super().validate_annotation(value)
    
class Class(BaseModel):
    """
    Represents the structure and behavior of a Python class for validation purposes.

    The `Class` class encapsulates the metadata and composition of a Python class, enabling 
    developers to validate its attributes, methods, and inheritance hierarchy. It provides a 
    structured representation to enforce constraints on class definitions.

    Attributes:
    -----------
    name : str
        The name of the class.
    attributes : Optional[List[Attribute]]
        A list of `Attribute` instances representing class-level and instance-level attributes. 
        These include their types, names, and optional values.
    methods : Optional[List[Function]]
        A list of `Function` instances representing the class's methods. Each method includes 
        details about its name, arguments, and return annotations.
    superclasses : Optional[List[str]]
        A list of superclass names from which the class inherits.

    Optional Fields:
    ----------------
    The optional attributes (`attributes`, `methods`, and `superclasses`) allow developers to 
    tailor the validation to specific aspects of a class. This flexibility enables narrowing the 
    scope of validation to relevant fields while ignoring others, facilitating use in diverse 
    contexts and requirements.

    Methods:
    --------
    _from_class_info(cls, extracted_classes: List[ClassInfo]) -> List['Class']:
        A utility method to create a list of `Class` instances from raw class metadata. 
        This method processes extracted class information to build structured `Class` objects.

    Flexibility:
    ------------
    - Supports partial validation by allowing optional fields to remain unset if not required.
    - Enables detailed validation of class structures, including attributes, methods, and inheritance.
    """

    name: str
    attributes: Optional[List[Attribute]] = None
    methods: Optional[List[Function]] = None
    superclasses: Optional[List[str]] = None

    @classmethod
    def _from_class_info(cls, extracted_classes:List[ClassInfo]):
        classes = []
        for name, class_attr, instance_attr, methods, superclasses in extracted_classes:
            classes.append(Class(name=name,
                  attributes=[
                        Attribute(
                            type=Constants.INSTANCE_TYPE,
                            name=name,
                            value=value
                        )
                        for name, value in instance_attr
                        ]
                      + [
                        Attribute(
                            type=Constants.CLASS_TYPE,
                            name=name,
                            value=value
                        )
                        for name, value in class_attr  
                    ],
                  methods=[
                      Function(
                          name=method.name,
                          arguments=[
                              Argument(
                                  name=arg.name,
                                  annotation=arg.annotation,
                                  value=arg.value
                              )
                              for arg in method.arguments
                          ],
                          return_annotation=None
                      ) 
                      for method in methods
                  ],
                  superclasses=superclasses
                )
            )
        return classes

class Module(BaseModel):
    """
    Represents the structure and metadata of a Python module with flexible customization.

    The `Module` class provides a detailed representation of a Python module, allowing 
    developers to define and customize specific fields for validation. By making all 
    parameters optional, this class enables precise tailoring of module data, supporting 
    a wide range of validation use cases.

    Attributes:
    -----------
    filename : Optional[str]
        The file path or name of the module on the filesystem. This can be left unspecified 
        if the filename is not critical for validation.
    version : Optional[str]
        The version of the module, typically extracted from its metadata. Defaults to `None` 
        for cases where version information is not available or required.
    variables : Optional[dict]
        A dictionary representing the global variables defined in the module. This can be customized 
        to include only the variables relevant to the developer's validation needs.
    functions : Optional[List[Function]]
        A list of `Function` instances representing the module's functions. Developers can specify 
        this field to validate function signatures, arguments, and annotations.
    classes : Optional[List[Class]]
        A list of `Class` instances representing the module's classes. This allows for validation 
        of class attributes, methods, and inheritance structures.

    Flexibility:
    ------------
    The optional nature of these parameters ensures that developers can focus on the aspects of 
    a module that are relevant to their validation requirements, without being constrained by 
    unnecessary data.
    """

    filename: str
    version: Optional[str] = None
    variables: Optional[dict] = None
    functions: Optional[List[Function]] = None
    classes: Optional[List[Class]] = None

class SpyModel(Module):
    """
    Extends the `Module` class to allow developers to define constraints directly on a Python module,
    independent of the specific runtime.

    The `SpyModel` class enables the specification of module-level constraints that remain consistent 
    across different architectures, operating systems, or Python versions. This ensures that the constraints 
    defined in the SpyModel are validated universally, providing robust and predictable module behavior 
    in any environment.

    Attributes:
    -----------
    deployments : List[Runtime]
        A list of runtime deployments associated with this SpyModel.

    Methods:
    --------
    from_module(cls, info_module: ModuleType):
        Constructs a `SpyModel` instance from a given Python module.
    """

    deployments = List[Runtime]

    @classmethod
    def from_module(cls, info_module: ModuleType):
        """
        Creates a `SpyModel` instance from a Python module.

        This method extracts metadata such as functions, classes, and variables
        from the provided module. It also captures runtime and system information
        to build a complete model representation.

        Parameters:
        -----------
        info_module : ModuleType
            The Python module to analyze and convert into a SpyModel.

        Returns:
        --------
        SpyModel
            An instance of the `SpyModel` class representing the given module and
            its associated runtime configurations.

        Steps:
        ------
        1. Load the module and extract metadata:
           - Filename, version, variables, functions, and classes.
        2. Extract runtime and system details:
           - Architecture, OS, Python version, interpreter, and environment variables.
        3. Create and return a `SpyModel` instance with the extracted information.

        Raises:
        -------
        ValueError
            If any validation errors occur during metadata extraction or runtime validation.

        Example:
        --------
        ```python
        import my_module
        spy_model = SpyModel.from_module(my_module)
        print(spy_model)
        ```
        """
        module_utils = ModuleUtil()
        runtime_utils = RuntimeUtil()
        sytem_utils = SystemUtil()
        python_utils = PythonUtil()
        info_module = module_utils.load_module(info_module)
        logger.debug(f"Create SpyModel from info_module: {ModuleType}")
        filename = "/".join(info_module.__file__.split('/')[-1:])
        version = module_utils.extract_version(info_module)
        variables = module_utils.extract_variables(info_module)
        functions = module_utils.extract_functions(info_module)
        classes = Class._from_class_info(module_utils.extract_classes(info_module))
        arch = runtime_utils.extract_arch()
        os = sytem_utils.extract_os()
        python_version = python_utils.extract_python_version()
        interpreter = python_utils.extract_python_implementation()
        envs = sytem_utils.extract_envs()
        module_utils.unload_module(info_module)
        logger.debug("Unload module")
        logger.debug(f"filename: {filename}, version: {version}, \
                     functions: {functions}, classes: {classes}")
        return cls(
            deployments = [
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
