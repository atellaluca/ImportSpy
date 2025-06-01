from typing import List
from .models import (
    Runtime,
    System,
    Environment,
    Python,
    Module,
    Variable,
    Function,
    Class
)

from .violation_systems import (
    RuntimeContractViolation,
    SystemContractViolation,
    VariableContractViolation,
    PythonContractViolation,
    ModuleContractViolation,
    BaseContractViolation,
    FunctionContractViolation,
    Bundle
)

from .constants import (
    Constants, 
    Contexts,
    Errors
)

from .config import Config

from .log_manager import LogManager

class RuntimeValidator:

    def __init__(self, bundle:Bundle):
        self.bundle = bundle

    def validate(
        self,
        runtimes_1: List[Runtime],
        runtimes_2: List[Runtime]
    ):
        if not runtimes_1:
            return
        
        self.bundle[Errors.KEY_RUNTIMES_1] = runtimes_1

        if not runtimes_2:
            raise ValueError(
                RuntimeContractViolation(
                    Contexts.RUNTIME_CONTEXT,
                    self.bundle
                ).missing_error_handler(Errors.COLLECTIONS_MESSAGES))

        runtime_2 = runtimes_2[0]

        for runtime_1 in runtimes_1:
            if runtime_1.arch == runtime_2.arch:
                return runtime_1
        raise ValueError(RuntimeContractViolation(
            Contexts.RUNTIME_CONTEXT,
            self.bundle
        ).missing_error_handler(Errors.COLLECTIONS_MESSAGES))
        

class SystemValidator:


    def __init__(self, bundle:Bundle):

        self.bundle = bundle
        self._environment_validator = SystemValidator.EnvironmentValidator()

    def validate(
        self,
        systems_1: List[System],
        systems_2: List[System]
    ) -> None:
        
        if not systems_1:
            return
        
        self.bundle[Errors.KEY_SYSTEMS_1] = systems_1

        if not systems_2:
            raise ValueError(
                SystemContractViolation(
                    Contexts.RUNTIME_CONTEXT,
                    self.bundle
                ).missing_error_handler(Errors.COLLECTIONS_MESSAGES))
        
        system_2 = systems_2[0]

        for system_1 in systems_1:
            if system_1.os == system_2.os:
                if system_1.environment:
                    self._environment_validator.validate(system_1.environment, system_2.environment)
                return system_1.pythons
        raise ValueError(
                SystemContractViolation(
                    Contexts.RUNTIME_CONTEXT,
                    self.bundle
                ).missing_error_handler(Errors.COLLECTIONS_MESSAGES))

    class EnvironmentValidator:

        def __init__(self, bundle:Bundle):
            self.bundle = bundle
        
        def validate(self,
                    environment_1: Environment,
                    environment_2: Environment
            ):
            
            if not environment_1:
                return
            
            self.bundle[Errors.KEY_ENVIRONMENT_1] = environment_1

            if not environment_2:
                raise ValueError(
                VariableContractViolation(
                    Contexts.ENVIRONMENT_CONTEXT,
                    self.bundle
                ).missing_error_handler(Errors.COLLECTIONS_MESSAGES))
            
            variables_2 = environment_2.variables

            if environment_1.variables:
                variables_1 = environment_1.variables
                VariableValidator().validate(variables_1, variables_2)
                return

class PythonValidator:

    def __init__(self, bundle:Bundle):
        self.bundle = bundle

    def validate(
        self,
        pythons_1: List[Python],
        pythons_2: List[Python]
    ):
        if not pythons_1:
            return
        
        self.bundle[Errors.KEY_PYTHONS_1] = pythons_1

        if not pythons_2:
            raise ValueError(
                PythonContractViolation(
                    Contexts.RUNTIME_CONTEXT,
                    self.bundle
                ).missing_error_handler(Errors.COLLECTIONS_MESSAGES))

        python_2 = pythons_2[0]
        for python_1 in pythons_1:

            if self._is_python_match(python_1, python_2):
                return python_1.modules

    def _is_python_match(
        self,
        python_1: Python,
        python_2: Python
    ) -> bool:
        """
        Determine whether two Python configurations match.

        Parameters
        ----------
        python_1 : Python
            Expected configuration.
        python_2 : Python
            Actual system configuration.

        Returns
        -------
        bool
            `True` if the two configurations match according to the declared criteria,
            otherwise `False`.

        Matching Criteria
        -----------------
        - If both version and interpreter are defined: match both.
        - If only version is defined: match version.
        - If only interpreter is defined: match interpreter.
        - If none are defined: match anything (default `True`).
        """
        self.bundle[Errors.KEY_PYTHON_1] = python_1
        if python_1.version and python_1.interpreter:
            return (
                python_1.version == python_2.version and
                python_1.interpreter == python_2.interpreter
            )

        if python_1.version:
            return python_1.version == python_2.version

        if python_1.interpreter:
            return python_1.interpreter == python_2.interpreter

        raise ValueError(
                PythonContractViolation(
                    Contexts.RUNTIME_CONTEXT,
                    self.bundle
                ).missing_error_handler(Errors.ENTITY_MESSAGES))

class ModuleValidator:

    def __init__(self, bundle:Bundle):
        self.bundle = bundle
        self.variable_validator:VariableValidator = VariableValidator()
        self.function_validator:FunctionValidator = FunctionValidator()
        self.class_validator:ClassValidator = ClassValidator()

    def validate(
        self,
        modules_1: List[Module],
        module_2: Module
    ):
        if not modules_1:
            return
        
        self.bundle[Errors.KEY_MODULES_1] = modules_1

        if not module_2:
            raise ValueError(
                ModuleContractViolation(
                    Contexts.RUNTIME_CONTEXT,
                    self.bundle
                ).missing_error_handler(Errors.COLLECTIONS_MESSAGES))

        for module_1 in modules_1:

            self.bundle[Errors.KEY_MODULE_NAME] = module_1.filename
            self.bundle[Errors.KEY_MODULE_VERSION] = module_1.version

            if module_1.filename and module_1.filename != module_2.filename:
                raise ValueError(
                ModuleContractViolation(
                    Contexts.RUNTIME_CONTEXT,
                    self.bundle
                ).mismatch_error_handler(module_1.filename, module_2.filename, Errors.ENTITY_MESSAGES))

            if module_1.version and module_1.version != module_2.version:
                raise ValueError(
                ModuleContractViolation(
                    Contexts.RUNTIME_CONTEXT,
                    self.bundle
                ).mismatch_error_handler(module_1.version, module_2.version, Errors.ENTITY_MESSAGES))

            self.variable_validator.validate(
                module_1.variables,
                module_2.variables,
                VariableContractViolation(
                    Errors.SCOPE_VARIABLE,
                    Contexts.MODULE_CONTEXT,
                    self.bundle
                )
            )

            self.function_validator.validate(
                module_1.functions,
                module_2.functions,
                FunctionContractViolation(
                    Contexts.MODULE_CONTEXT,
                    self.bundle
                )
            )

            self.class_validator.validate(
                module_1.classes,
                module_2.classes,
                ModuleContractViolation(
                    Contexts.CLASS_CONTEXT,
                    self.bundle
                )
            )


class ClassValidator:

    def __init__(self):
        
        self.variable_validator:VariableValidator = VariableValidator()
        self.function_validator:FunctionValidator = FunctionValidator()

    def validate(
            self,
            classes_1: List[Class],
            classes_2: List[Class],
            contract_violation: BaseContractViolation
    ):  
        if not classes_1:
            return
        
        bundle: Bundle = contract_violation.bundle
        bundle[Errors.KEY_CLASSES_1] = classes_1

        if not classes_2:
            raise ValueError(
                ModuleContractViolation(
                    Contexts.CLASS_CONTEXT,
                    bundle
                ).missing_error_handler(Errors.COLLECTIONS_MESSAGES))
        
        for class_1 in classes_1:
            class_2 = next((cls for cls in classes_2 if cls.name == class_1.name), None)
            
            bundle[Errors.KEY_CLASS_NAME] = class_1.name

            if not class_2:
                raise ValueError(
                    ModuleContractViolation(
                        Contexts.CLASS_CONTEXT,
                        bundle
                    ).missing_error_handler(Errors.ENTITY_MESSAGES)
                )
            
            bundle[Errors.KEY_ATTRIBUTE_TYPE] = Config.CLASS_TYPE

            self.variable_validator.validate(
                class_1.get_class_attributes(),
                class_2.get_class_attributes(),
                VariableContractViolation(Errors.SCOPE_ARGUMENT, Contexts.CLASS_CONTEXT, bundle)
            )

            bundle[Errors.KEY_ATTRIBUTE_TYPE] = Config.INSTANCE_TYPE

            self.variable_validator.validate(
                class_1.get_instance_attributes(),
                class_2.get_instance_attributes(),
                VariableContractViolation(Errors.SCOPE_ARGUMENT, Contexts.CLASS_CONTEXT, bundle)
            )

            self.function_validator.validate(
                class_1.methods,
                class_2.methods,
                FunctionContractViolation(
                    Contexts.CLASS_CONTEXT,
                    bundle
                )
            )

            self.function_validator.validate(
                class_1.methods,
                class_2.methods,
                classname=class_1.name
            )

            self.validate(class_1.superclasses,
                          class_2.superclasses,
                          ModuleContractViolation(
                              Contexts.CLASS_CONTEXT,
                              bundle
                          )
            )

class VariableValidator:

    def __init__(self):

        self.logger = LogManager().get_logger(self.__class__.__name__)

    def validate(
        self,
        variables_1: List[Variable],
        variables_2: List[Variable],
        contract_violation: BaseContractViolation
    ):
        bundle: Bundle = contract_violation.bundle
        self.logger.debug(f"Type of variables_1: {type(variables_1)}")
        self.logger.debug(
            Constants.LOG_MESSAGE_TEMPLATE.format(
                operation="Variable validating",
                status="Starting",
                details=f"Expected Variables: {variables_1} ; Actual Variables: {variables_2}"
            )
        )

        if not variables_1:
            self.logger.debug(
                Constants.LOG_MESSAGE_TEMPLATE.format(
                    operation="Check if variables_1 is not none",
                    status="Finished",
                    details="No expected Variables to validate"
                )
            )
            return
        
        bundle[Errors.KEY_VARIABLES_1] = variables_1

        if not variables_2:
            self.logger.debug(
                Constants.LOG_MESSAGE_TEMPLATE.format(
                    operation="Checking variables_2 when variables_1 is missing",
                    status="Finished",
                    details="No actual Variables found for validation"
                )
            )
            raise ValueError(contract_violation.missing_error_handler(Errors.COLLECTIONS_MESSAGES))

        for var_1 in variables_1:
            self.logger.debug(
                Constants.LOG_MESSAGE_TEMPLATE.format(
                    operation="Variable validating",
                    status="Progress",
                    details=f"Current var_1: {var_1}"
                )
            )
            bundle[Errors.VARIABLES_DINAMIC_PAYLOAD[contract_violation.context]] = var_1.name
            if var_1.name not in {var.name for var in variables_2}:
                raise ValueError(contract_violation.missing_error_handler(Errors.ENTITY_MESSAGES))

        for var_1 in variables_1:
            var_2 = next((var for var in variables_2 if var.name == var_1.name), None)
            if not var_2:
                raise ValueError(contract_violation.missing_error_handler(Errors.ENTITY_MESSAGES))

            if var_1.annotation and var_1.annotation != var_2.annotation:
                raise ValueError(contract_violation.mismatch_error_handler(var_1.annotation, var_2.annotation, Errors.ENTITY_MESSAGES))

            if var_1.value != var_2.value:
                raise ValueError(contract_violation.mismatch_error_handler(var_1.value, var_2.value, Errors.ENTITY_MESSAGES))

class FunctionValidator:

    def __init__(self):

        self.argument_validator:VariableValidator = VariableValidator()
        self.logger = LogManager().get_logger(self.__class__.__name__)

    def validate(
        self,
        functions_1: List[Function],
        functions_2: List[Function],
        contract_violation: BaseContractViolation
    ):
        
        bundle: Bundle = contract_violation.bundle
        self.logger.debug(
            Constants.LOG_MESSAGE_TEMPLATE.format(
                operation="Function validating",
                status="Starting",
                details=f"Expected functions: {functions_1} ; Current functions: {functions_2}"
            )
        )

        if not functions_1:
            self.logger.debug(
                Constants.LOG_MESSAGE_TEMPLATE.format(
                    operation="Check if functions_1 is not none",
                    status="Finished",
                    details="No functions to validate"
                )
            )
            return
        
        bundle[Errors.KEY_FUNCTIONS_1] = functions_1

        if not functions_2:
            self.logger.debug(
                Constants.LOG_MESSAGE_TEMPLATE.format(
                    operation="Checking functions_2 when functions_1 is missing",
                    status="Finished",
                    details="No actual functions found"
                )
            )
            raise ValueError(contract_violation.missing_error_handler(Errors.COLLECTIONS_MESSAGES))

        for function_1 in functions_1:
            bundle[Errors.FUNCTIONS_DINAMIC_PAYLOAD[contract_violation.context]] = function_1.name
            self.logger.debug(
                Constants.LOG_MESSAGE_TEMPLATE.format(
                    operation="Function validating",
                    status="Progress",
                    details=f"Current function: {function_1}"
                )
            )
            if function_1.name not in {f.name for f in functions_2}:
                self.logger.debug(
                    Constants.LOG_MESSAGE_TEMPLATE.format(
                        operation="Checking if function_1 is in functions_2",
                        status="Finished for function missing",
                        details=f"function_1: {function_1}; functions_2: {functions_2}"
                    )
                )
                raise ValueError(contract_violation.missing_error_handler(Errors.ENTITY_MESSAGES))

        for function_1 in functions_1:
            function_2 = next((f for f in functions_2 if f.name == function_1.name), None)
            if not function_2:
                raise ValueError(contract_violation.missing_error_handler(Errors.ENTITY_MESSAGES))

            self.argument_validator.validate(
                function_1.arguments,
                function_2.arguments,
                VariableContractViolation(
                    Errors.SCOPE_ARGUMENT,
                    Contexts.MODULE_CONTEXT,
                    bundle)
            )

            if function_1.return_annotation and function_1.return_annotation != function_2.return_annotation:
                raise ValueError(contract_violation.mismatch_error_handler(
                    function_1.return_annotation, 
                    function_2.return_annotation, 
                    Errors.ENTITY_MESSAGES
                    )
                )

        self.logger.debug(
            Constants.LOG_MESSAGE_TEMPLATE.format(
                operation="Function validating",
                status="Completed",
                details="Validation successful."
            )
        )