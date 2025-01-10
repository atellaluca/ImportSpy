from importspy.models import (
    SpyModel,
    Module,
    Deployment,
    Runtime,
    System,
    Python,
    Attribute
)

from ..constants import Constants

from typing import (
    List
)
from ..errors import Errors

class SpyModelValidator:

    def is_subset(self,
                  spy_model_1: SpyModel,
                  spy_model_2: SpyModel) -> bool:
        """
        Determine if the first SpyModel is a subset of the second SpyModel.
    
        This function checks whether all relevant attributes (such as functions, classes, methods, 
        superclasses, filename, and version) specified in `spy_model_1` are present in `spy_model_2`. 
        It throws a ValueError with a specific message indicating the type of mismatch.
    
        Parameters:
        -----------
        - **spy_model_1** (`SpyModel`): The SpyModel whose attributes are being validated.
        - **spy_model_2** (`SpyModel`): The SpyModel against which validation is performed.
    
        Returns:
        --------
        - **bool**: Returns `True` if `spy_model_1` is a subset of `spy_model_2`, else raises a ValueError.
    
        Raises:
        -------
        - **ValueError**: Descriptive error highlighting which validation check failed.
    
        Example usage:
        --------------
        ```
        try:
            result = is_subset(spy_model1, spy_model2)
            print("Validation successful:", result)
        except ValueError as ve:
            print("Validation error:", ve)
        ```
        """
        deployment_2:Deployment = spy_model_2.deployments[0]
        deployment_validator = DeploymentValidator()
        for deployment_1 in spy_model_1.deployments:
            deployment_validator.validate(deployment_1, deployment_2)
        return True

class DeploymentValidator:

    def validate(self,
                 deployment_1:Deployment,
                 deployment_2:Deployment):
        runtime_2:Runtime = deployment_2.runtimes[0]
        runtime_validator = RuntimeValidator()
        for runtime_1 in deployment_1.runtimes:
            runtime_validator.validate(runtime_1, runtime_2)
    
class RuntimeValidator:

    def validate(self,
                 runtime_1:Runtime,
                 runtime_2:Runtime):
        if runtime_1.arch and \
            runtime_1.arch == runtime_2.arch \
                and runtime_1.systems:
            system_2:System = runtime_2.systems[0] if runtime_2.systems else None
            if not system_2:
                raise ValueError(Errors.SYSTEM_MISSING.format(system_1))
            system_validator = SystemValidator()
            for system_1 in runtime_1.systems:
                system_validator.validate(system_1, system_2)

class SystemValidator:

    def validate(self,
                 system_1:System,
                 system_2:System):
        common_validator = CommonValidator()
        if system_1.os and system_1.os == system_2.os:
            common_validator.dict_validate(system_1.envs, system_2.envs, Errors.ENV_VAR_MISSING, Errors.ENV_VAR_MISMATCH)
            python_2:Python = system_2.pythons[0]
            python_validator = PythonValidator()
            for python_1 in system_1.pythons:
                python_validator.validate(python_1, python_2)


class PythonValidator:

    def validate(self,
                 python_1:Python,
                 python_2:Python):
        if python_1.version == python_2.version and python_1.interpreter == python_2.interpreter:
            module_validator = ModuleValidator()
            module_2 = python_2.modules[0]
            for module_1 in python_1.modules:
                module_validator.validate(module_1, module_2)


class ModuleValidator:

    def validate(self, 
                 module_1:Module, 
                 module_2:Module):
        if module_1.filename and module_1.filename != module_2.filename:
            raise ValueError(Errors.FILENAME_MISMATCH.format(module_2.filename, module_2.filename))
        if module_1.version and module_1.version != module_2.version:
            raise ValueError(Errors.VERSION_MISMATCH.format(module_1.version, module_2.version))
        common_validator = CommonValidator()
        #Variables validation
        common_validator.dict_validate(module_1.variables, module_2.variables, Errors.VAR_MISSING, Errors.VAR_MISMATCH)
        #Functions validation
        common_validator.list_validate(module_1.functions, module_2.functions, Errors.FUNCTIONS_MISSING)
        for class_1 in module_1.classes:
            class_2 = next((cls for cls in module_2.classes if cls.name == class_1.name), None)
            if not class_2:
                raise ValueError(Errors.CLASS_MISSING.format(class_1.name))
            # Class attributes validation
            AttributeValidator().validate(class_1.attributes, class_2.attributes)
            # Class methods validation
            common_validator.list_validate(class_1.methods, class_2.methods, Errors.CLASS_METHOD_MISSING, class_2.name)
            # Superclasses validation
            common_validator.list_validate(class_1.superclasses, class_2.superclasses, Errors.CLASS_SUPERCLASS_MISSING, class_2.name)

class AttributeValidator:

    def validate(self,
                 attrs_1: List[Attribute],
                 attrs_2: List[Attribute]):
        for attr_1 in attrs_1:
            if attr_1 not in attrs_2:
                raise ValueError(Errors.CLASS_ATTRIBUTE_MISSING.format(attr_1.type, attr_1))
        for attr_1 in attrs_1:
            for attr_2 in attrs_2:
                if attr_1.name != attr_2.name:
                    raise ValueError(Errors.CLASS_ATTRIBUTE_MISMATCH.format(Constants.NAME, attr_1.type, attr_1.name, attr_1.name, attr_2.name))
                if attr_1.value != attr_2.value:
                    raise ValueError(Errors.CLASS_ATTRIBUTE_MISMATCH.format(Constants.VALUE, attr_1.type, attr_1.name, attr_1.value, attr_2.value))
                

class CommonValidator:

    def list_validate(self,
                      list1:list, 
                      list2:list, 
                      missing_error:str, 
                      *args):
        for expected_element in list1:
            if expected_element not in list2:
                raise ValueError(missing_error.format(expected_element, *args))
    
    def dict_validate(self,
                      dict1:dict, 
                      dict2:dict,
                      missing_error:str,
                      mismatch_error:str):
        for expected_key, expected_value in dict1.items():
            if expected_key in dict2:
                if expected_value != dict2[expected_key]:
                    raise ValueError(mismatch_error.format(expected_key, expected_value, dict2[expected_key]))
            else:
                raise ValueError(missing_error.format(expected_key))