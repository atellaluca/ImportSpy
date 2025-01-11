from ..models import Module
from typing import List
from ..errors import Errors
from .attribute_validator import AttributeValidator
from .common_validator import CommonValidator

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