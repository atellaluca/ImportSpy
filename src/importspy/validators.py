"""ImportSpy Contract Validators

This module defines structural and runtime validators for comparing
expected contract definitions against observed runtime representations.

Each validator compares a specific domain (e.g., Python version, environment variables,
module structure, class layout) using ImportSpy's SpyModel structures.

If mismatches or missing elements are detected, specialized `ContractViolation`
objects raise informative `ValueError` exceptions enriched with context bundles.

Used both in embedded runtime validation and CLI mode.
"""

from typing import List
from .models import (
    Runtime, System, Environment, Python, Module,
    Variable, Function, Class
)
from .violation_systems import (
    RuntimeContractViolation, SystemContractViolation,
    VariableContractViolation, PythonContractViolation,
    ModuleContractViolation, BaseContractViolation,
    FunctionContractViolation, Bundle
)
from .constants import Constants, Contexts, Errors
from .config import Config
from .log_manager import LogManager


class RuntimeValidator:
    """Validates architecture compatibility between runtime collections."""

    def validate(
        self,
        runtimes_1: List[Runtime],
        runtimes_2: List[Runtime],
        contract_violation: RuntimeContractViolation
    ) -> None:
        """Compare runtime architectures and raise if no match is found.

        Args:
            runtimes_1: Declared runtime requirements.
            runtimes_2: Observed runtime environments.
            contract_violation: Violation reporter instance.

        Returns:
            Runtime: The matching runtime, if found.

        Raises:
            ValueError: If runtimes_2 is empty or no arch matches.
        """
        if not runtimes_1:
            return

        bundle = contract_violation.bundle
        bundle[Errors.KEY_RUNTIMES_1] = runtimes_1

        if not runtimes_2:
            raise ValueError(contract_violation.missing_error_handler(Errors.COLLECTIONS_MESSAGES))

        runtime_2 = runtimes_2[0]

        for runtime_1 in runtimes_1:
            if runtime_1.arch == runtime_2.arch:
                return runtime_1

        raise ValueError(contract_violation.missing_error_handler(Errors.COLLECTIONS_MESSAGES))


class SystemValidator:
    """Validates operating system and environment compatibility."""

    def __init__(self):
        self._environment_validator = self.EnvironmentValidator()

    def validate(
        self,
        systems_1: List[System],
        systems_2: List[System],
        contract_violation: SystemContractViolation
    ) -> None:
        """Compare systems and delegate to environment validation.

        Args:
            systems_1: Expected system definitions.
            systems_2: Runtime-observed systems.
            contract_violation: Violation context and bundle.

        Returns:
            List[Python]: Matching Python objects if validation passes.

        Raises:
            ValueError: If no matching OS or missing environment.
        """
        if not systems_1:
            return

        bundle = contract_violation.bundle
        bundle[Errors.KEY_SYSTEMS_1] = systems_1

        if not systems_2:
            raise ValueError(contract_violation.missing_error_handler(Errors.COLLECTIONS_MESSAGES))

        system_2 = systems_2[0]

        for system_1 in systems_1:
            if system_1.os == system_2.os:
                if system_1.environment:
                    self._environment_validator.validate(system_1.environment, system_2.environment, bundle)
                return system_1.pythons

        raise ValueError(contract_violation.missing_error_handler(Errors.COLLECTIONS_MESSAGES))

    class EnvironmentValidator:
        """Validates environment-level variables and configuration."""

        def validate(
            self,
            environment_1: Environment,
            environment_2: Environment,
            bundle: Bundle
        ):
            """Compare two environments' variable lists.

            Args:
                environment_1: Expected environment.
                environment_2: Observed environment.
                bundle: Violation context and data.

            Raises:
                ValueError: On missing or mismatched variables.
            """
            if not environment_1:
                return

            bundle[Errors.KEY_ENVIRONMENT_1] = environment_1

            if not environment_2:
                raise ValueError(
                    VariableContractViolation(
                        Errors.SCOPE_VARIABLE,
                        Contexts.ENVIRONMENT_CONTEXT,
                        bundle
                    ).missing_error_handler(Errors.COLLECTIONS_MESSAGES)
                )

            variables_2 = environment_2.variables

            if environment_1.variables:
                variables_1 = environment_1.variables
                VariableValidator().validate(
                    variables_1,
                    variables_2,
                    VariableContractViolation(
                        Errors.SCOPE_VARIABLE,
                        Contexts.ENVIRONMENT_CONTEXT,
                        bundle
                    )
                )
            
            self._secrets_validator(environment_1, environment_2, bundle)
        
        def _secrets_validator(
                self, 
                environment_1:Environment,
                environment_2:Environment,
                bundle: Bundle
                ):
            if not environment_1.secrets:
                return
            if not environment_2.secrets:
                raise ValueError(VariableContractViolation(Errors.SCOPE_VARIABLE, Contexts.ENVIRONMENT_CONTEXT, bundle).missing_error_handler(Errors.COLLECTIONS_MESSAGES))
            for secret_1 in environment_1.secrets:
                if not secret_1 in environment_2.secrets:
                    bundle[Errors.KEY_ENVIRONMENT_VARIABLE_NAME] = secret_1
                    raise ValueError(VariableContractViolation(Errors.SCOPE_VARIABLE, Contexts.ENVIRONMENT_CONTEXT, bundle).missing_error_handler(Errors.ENTITY_MESSAGES))
            


                




class PythonValidator:
    """Validates Python version and interpreter compatibility."""

    def validate(
        self,
        pythons_1: List[Python],
        pythons_2: List[Python],
        contract_violation: PythonContractViolation
    ) -> None:
        """Ensure that Python version/interpreter match expectations.

        Args:
            pythons_1: Contract-defined expectations.
            pythons_2: Runtime-detected Python instances.
            contract_violation: Context bundle and error factory.

        Returns:
            List[Module]: Modules associated with the matched Python.

        Raises:
            ValueError: On missing or mismatched Python definitions.
        """
        if not pythons_1:
            return

        bundle = contract_violation.bundle
        bundle[Errors.KEY_PYTHONS_1] = pythons_1

        if not pythons_2:
            raise ValueError(contract_violation.missing_error_handler(Errors.COLLECTIONS_MESSAGES))

        python_2 = pythons_2[0]
        for python_1 in pythons_1:
            if self._is_python_match(python_1, python_2, contract_violation):
                return python_1.modules

        raise ValueError(contract_violation.missing_error_handler(Errors.COLLECTIONS_MESSAGES))

    def _is_python_match(
        self,
        python_1: Python,
        python_2: Python,
        contract_violation: PythonContractViolation
    ) -> bool:
        """Internal logic to compare Python version and interpreter."""
        bundle = contract_violation.bundle
        bundle[Errors.KEY_PYTHON_1] = python_1

        if python_1.version and python_1.interpreter:
            return (
                python_1.version == python_2.version and
                python_1.interpreter == python_2.interpreter
            )

        if python_1.version:
            return python_1.version == python_2.version

        if python_1.interpreter:
            return python_1.interpreter == python_2.interpreter

        return False


class ModuleValidator:
    """Validates modules, including structure, variables, functions, and classes."""

    def __init__(self):
        self.variable_validator = VariableValidator()
        self.function_validator = FunctionValidator()
        self.class_validator = ClassValidator()

    def validate(
        self,
        modules_1: List[Module],
        module_2: Module,
        contract_violation: ModuleContractViolation
    ):
        """Validate module structure against expected SpyModel.

        Args:
            modules_1: List of expected module definitions.
            module_2: Observed runtime module.
            contract_violation: Context bundle.

        Raises:
            ValueError: On mismatch or missing module details.
        """
        bundle = contract_violation.bundle
        if not modules_1:
            return

        bundle[Errors.KEY_MODULES_1] = modules_1

        if not module_2:
            raise ValueError(contract_violation.missing_error_handler(Errors.COLLECTIONS_MESSAGES))

        for module_1 in modules_1:
            bundle[Errors.KEY_MODULE_NAME] = module_1.filename
            bundle[Errors.KEY_MODULE_VERSION] = module_1.version

            if module_1.filename and module_1.filename != module_2.filename:
                raise ValueError(contract_violation.mismatch_error_handler(module_1.filename, module_2.filename, Errors.ENTITY_MESSAGES))

            if module_1.version and module_1.version != module_2.version:
                raise ValueError(contract_violation.mismatch_error_handler(module_1.version, module_2.version, Errors.ENTITY_MESSAGES))

            self.variable_validator.validate(
                module_1.variables,
                module_2.variables,
                VariableContractViolation(
                    Errors.SCOPE_VARIABLE,
                    Contexts.MODULE_CONTEXT,
                    bundle
                )
            )

            self.function_validator.validate(
                module_1.functions,
                module_2.functions,
                FunctionContractViolation(
                    Contexts.MODULE_CONTEXT,
                    bundle
                )
            )

            self.class_validator.validate(
                module_1.classes,
                module_2.classes,
                ModuleContractViolation(
                    Contexts.CLASS_CONTEXT,
                    bundle
                )
            )


class ClassValidator:
    """Validates class structure, attributes, and methods."""

    def __init__(self):
        self.variable_validator = VariableValidator()
        self.function_validator = FunctionValidator()

    def validate(
        self,
        classes_1: List[Class],
        classes_2: List[Class],
        contract_violation: BaseContractViolation
    ):
        """Recursively validate class structure and inheritance.

        Args:
            classes_1: Expected class definitions.
            classes_2: Observed runtime classes.
            contract_violation: Shared context for error propagation.

        Raises:
            ValueError: On missing class, method, or attribute mismatch.
        """
        if not classes_1:
            return

        bundle = contract_violation.bundle
        bundle[Errors.KEY_CLASSES_1] = classes_1

        if not classes_2:
            raise ValueError(ModuleContractViolation(Contexts.CLASS_CONTEXT, bundle).missing_error_handler(Errors.COLLECTIONS_MESSAGES))

        for class_1 in classes_1:
            class_2 = next((cls for cls in classes_2 if cls.name == class_1.name), None)

            bundle[Errors.KEY_CLASS_NAME] = class_1.name

            if not class_2:
                raise ValueError(ModuleContractViolation(Contexts.CLASS_CONTEXT, bundle).missing_error_handler(Errors.ENTITY_MESSAGES))

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
                FunctionContractViolation(Contexts.CLASS_CONTEXT, bundle)
            )

            self.validate(
                class_1.superclasses,
                class_2.superclasses,
                ModuleContractViolation(Contexts.CLASS_CONTEXT, bundle)
            )


class VariableValidator:
    """Validates variables, attributes, and annotations."""

    def __init__(self):
        self.logger = LogManager().get_logger(self.__class__.__name__)

    def validate(
        self,
        variables_1: List[Variable],
        variables_2: List[Variable],
        contract_violation: VariableContractViolation
    ):
        """Validate variable existence, name, value, and annotation.

        Args:
            variables_1: Expected variables.
            variables_2: Actual runtime variables.
            contract_violation: Violation and error builder.

        Raises:
            ValueError: On missing or mismatched variables.
        """
        bundle = contract_violation.bundle

        self.logger.debug(f"Type of variables_1: {type(variables_1)}")
        self.logger.debug(
            Constants.LOG_MESSAGE_TEMPLATE.format(
                operation="Variable validating",
                status="Starting",
                details=f"Expected Variables: {variables_1} ; Actual Variables: {variables_2}"
            )
        )

        if not variables_1:
            self.logger.debug("No expected Variables to validate")
            return

        bundle[
            Errors.VARIABLES_DINAMIC_PAYLOAD[contract_violation.scope][Errors.COLLECTIONS_MESSAGES][contract_violation.context]
        ] = variables_1

        if not variables_2:
            raise ValueError(contract_violation.missing_error_handler(Errors.COLLECTIONS_MESSAGES))

        for var_1 in variables_1:
            bundle[Errors.VARIABLES_DINAMIC_PAYLOAD[contract_violation.scope][Errors.ENTITY_MESSAGES][contract_violation.context]] = var_1.name
            if var_1.name not in {var.name for var in variables_2}:
                raise ValueError(contract_violation.missing_error_handler(Errors.ENTITY_MESSAGES))

        for var_1 in variables_1:
            var_2 = next((v for v in variables_2 if v.name == var_1.name), None)
            if not var_2:
                raise ValueError(contract_violation.missing_error_handler(Errors.ENTITY_MESSAGES))

            if var_1.annotation and var_1.annotation != var_2.annotation:
                raise ValueError(contract_violation.mismatch_error_handler(var_1.annotation, var_2.annotation, Errors.ENTITY_MESSAGES))

            if var_1.value != var_2.value:
                raise ValueError(contract_violation.mismatch_error_handler(var_1.value, var_2.value, Errors.ENTITY_MESSAGES))


class FunctionValidator:
    """Validates functions, their arguments, and return annotations."""

    def __init__(self):
        self.argument_validator = VariableValidator()
        self.logger = LogManager().get_logger(self.__class__.__name__)

    def validate(
        self,
        functions_1: List[Function],
        functions_2: List[Function],
        contract_violation: BaseContractViolation
    ):
        """Compare function definitions across two modules or classes.

        Args:
            functions_1: Expected functions.
            functions_2: Observed functions.
            contract_violation: Violation context object.

        Raises:
            ValueError: On missing, unmatched, or misannotated functions.
        """
        bundle = contract_violation.bundle

        if not functions_1:
            self.logger.debug("No functions to validate")
            return

        bundle[Errors.FUNCTIONS_DINAMIC_PAYLOAD[Errors.COLLECTIONS_MESSAGES][contract_violation.context]] = functions_1

        if not functions_2:
            raise ValueError(contract_violation.missing_error_handler(Errors.COLLECTIONS_MESSAGES))

        for function_1 in functions_1:
            bundle[Errors.FUNCTIONS_DINAMIC_PAYLOAD[Errors.ENTITY_MESSAGES][contract_violation.context]] = function_1.name
            if function_1.name not in {f.name for f in functions_2}:
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
                    bundle
                )
            )

            if function_1.return_annotation and function_1.return_annotation != function_2.return_annotation:
                raise ValueError(contract_violation.mismatch_error_handler(
                    function_1.return_annotation,
                    function_2.return_annotation,
                    Errors.ENTITY_MESSAGES
                ))
