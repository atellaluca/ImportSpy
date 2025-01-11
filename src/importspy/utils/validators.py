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

    def validate(self,
                  spy_model_1: SpyModel,
                  spy_model_2: SpyModel) -> bool:
        deployment_2:Deployment = spy_model_2.deployments[0]
        DeploymentValidator().validate(spy_model_1.deployments, deployment_2)
        ModuleValidator().validate([spy_model_1], 
                                   spy_model_2
                                   .deployments[0]
                                   .runtimes[0]
                                   .systems[0]
                                   .pythons[0]
                                   .modules[0])

class DeploymentValidator:

    def validate(self,
                 deployments_1:List[Deployment],
                 deployment_2:Deployment):
        rv = RuntimeValidator()
        for deployment_1 in deployments_1:
            rv.validate(deployment_1.runtimes, deployment_2.runtimes[0])
    
class RuntimeValidator:

    def validate(self,
                 runtimes_1:List[Runtime],
                 runtime_2:Runtime):
        self._check_runtimes(runtimes_1, runtime_2)
        for runtime_1 in runtimes_1:
            if runtime_1.systems:
                system_2:System = runtime_2.systems[0]
                SystemValidator().validate(runtime_1.systems, system_2)
                return
    
    def _check_runtimes(self,
                        runtimes_1:List[Runtime],
                        runtime_2: Runtime):
        for runtime_1 in runtimes_1:
            if runtime_1.arch == runtime_2.arch:
                return
        raise ValueError(Errors.RUNTIME_MISSING.format(runtime_2))


class SystemValidator:

    def validate(self,
                 systems_1:List[System],
                 system_2:System):
        self._check_systems(systems_1, system_2)
        for system_1 in systems_1:
            if system_1.pythons: 
                python_2:Python = system_2.pythons[0]
                PythonValidator().validate(system_1.pythons, python_2)
                return
    
    def _check_systems(self,
                       systems_1:List[System],
                       system_2:System):
        cv = CommonValidator()
        for system_1 in systems_1:
            if system_1.os == system_2.os:
                cv.dict_validate(system_1.envs, system_2.envs, Errors.ENV_VAR_MISSING, Errors.ENV_VAR_MISMATCH)
                return
        raise ValueError(Errors.SYSTEM_MISSING.format(system_2))
        


class PythonValidator:

    def validate(self,
                 pythons_1:List[Python],
                 python_2:Python):
        self._check_pythons(pythons_1, python_2)
        for python_1 in pythons_1:
            if python_1.modules:
                ModuleValidator().validate(python_1.modules, python_2.modules[0])
    
    def _check_pythons(self,
                       pythons_1:List[Python],
                       python_2:Python):
        for python_1 in pythons_1:
            if python_1.version == python_2.version \
                and python_1.interpreter == python_2.interpreter:
                return
        raise ValueError(Errors.PYTHON_MISSING.format(python_2))

class ModuleValidator:

    def validate(self, 
                 modules_1:List[Module], 
                 module_2:Module):
        for module_1 in modules_1:
            if module_1.filename and module_1.filename != module_2.filename:
                raise ValueError(Errors.FILENAME_MISMATCH.format(module_1.filename, module_2.filename))
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
                AttributeValidator().validate(class_1.attributes, class_2.attributes, class_1.name)
                # Class methods validation
                common_validator.list_validate(class_1.methods, class_2.methods, Errors.CLASS_METHOD_MISSING, class_2.name)
                # Superclasses validation
                common_validator.list_validate(class_1.superclasses, class_2.superclasses, Errors.CLASS_SUPERCLASS_MISSING, class_2.name)

class AttributeValidator:

    def validate(self,
                 attrs_1: List[Attribute],
                 attrs_2: List[Attribute], classname:str):
        if not attrs_1:
            return
        for attr_1 in attrs_1:
            if attr_1 not in attrs_2:
                raise ValueError(Errors.CLASS_ATTRIBUTE_MISSING.format(attr_1.type, f"{attr_1.name}={attr_1.value}", classname))
        for attr_1 in attrs_1:
            attr_2 =  next((attr for attr in attrs_2 if attr == attr_1), None)
            if attr_1.value != attr_2.value:
                raise ValueError(Errors.CLASS_ATTRIBUTE_MISMATCH.format(Constants.VALUE, attr_1.type, attr_1.name, attr_1.value, attr_2.value))
                

class CommonValidator:

    def list_validate(self,
                      list1:list, 
                      list2:list, 
                      missing_error:str, 
                      *args):
        if not list1:
            return
        for expected_element in list1:
            if expected_element not in list2:
                raise ValueError(missing_error.format(expected_element, *args))
    
    def dict_validate(self,
                      dict1:dict, 
                      dict2:dict,
                      missing_error:str,
                      mismatch_error:str):
        if not dict1:
            return
        for expected_key, expected_value in dict1.items():
            if expected_key in dict2:
                if expected_value != dict2[expected_key]:
                    raise ValueError(mismatch_error.format(expected_key, expected_value, dict2[expected_key]))
            else:
                raise ValueError(missing_error.format(expected_key))