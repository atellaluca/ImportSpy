from typing import List
from .models import (
    Runtime,
    System,
    Environment,
    Python,
    Module
)

from .constants import Constants


class RuntimeValidator:

    def validate(
        self,
        runtimes_1: List[Runtime],
        runtimes_2: List[Runtime]
    ):
        if not runtimes_1:
            return

        if not runtimes_2:
            raise ValueError(Errors.ELEMENT_MISSING.format(runtimes_1))

        runtime_2 = runtimes_2[0]

        for runtime_1 in runtimes_1:
            if runtime_1.arch == runtime_2.arch:
                return runtime_1

class SystemValidator:


    def __init__(self):
        
        self._environment_validator = SystemValidator.EnvironmentValidator()

    def validate(
        self,
        systems_1: List[System],
        systems_2: List[System]
    ) -> None:
        
        if not systems_1:
            return

        if not systems_2:
            raise ValueError(Errors.ELEMENT_MISSING.format(systems_1))
        
        system_2 = systems_2[0]

        for system_1 in systems_1:
            if system_1.os == system_2.os:
                if system_1.environment:
                    self._environment_validator.validate(system_1.environment, system_2.environment)
                return system_1.pythons

    class EnvironmentValidator:
        
        def validate(self,
                    environment_1: Environment,
                    environment_2: Environment):
            
            if not environment_1:
                return

            if not environment_2:
                raise ValueError(Errors.ELEMENT_MISSING.format(environment_1))
            
            variables_2 = environment_2.variables

            if environment_1.variables:
                variables_1 = environment_1.variables
                VariableValidator().validate(variables_1, variables_2)
                return

class PythonValidator:

    def validate(
        self,
        pythons_1: List[Python],
        pythons_2: List[Python]
    ):
        if not pythons_1:
            return

        if not pythons_2:
            raise ValueError(Errors.ELEMENT_MISSING.format(pythons_1))

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
        if python_1.version and python_1.interpreter:
            return (
                python_1.version == python_2.version and
                python_1.interpreter == python_2.interpreter
            )

        if python_1.version:
            return python_1.version == python_2.version

        if python_1.interpreter:
            return python_1.interpreter == python_2.interpreter

        return True

class ModuleValidator:

    def validate(
        self,
        modules_1: List[Module],
        module_2: Module
    ):
        if not modules_1:
            return

        if not module_2:
            raise ValueError(Errors.ELEMENT_MISSING.format(modules_1))

        for module_1 in modules_1:

            if module_1.filename and module_1.filename != module_2.filename:
                raise ValueError(Errors.FILENAME_MISMATCH.format(module_1.filename, module_2.filename))

            if module_1.version and module_1.version != module_2.version:
                raise ValueError(Errors.VERSION_MISMATCH.format(module_1.version, module_2.version))

            self._variable_validator.validate(
                module_1.variables,
                module_2.variables)

            self._function_validator.validate(
                module_1.functions,
                module_2.functions
            )

            if module_1.classes:
                for class_1 in module_1.classes:
                    class_2 = next((cls for cls in module_2.classes if cls.name == class_1.name), None)
                    if not class_2:
                        raise ValueError(Errors.CLASS_MISSING.format(class_1.name))

                    self._attribute_validator.validate(
                        class_1.attributes,
                        class_2.attributes,
                        class_1.name
                    )

                    self._function_validator.validate(
                        class_1.methods,
                        class_2.methods,
                        classname=class_1.name
                    )

                    CommonValidator().list_validate(
                        class_1.superclasses,
                        class_2.superclasses,
                        Errors.CLASS_SUPERCLASS_MISSING,
                        class_2.name
                    )
            return

class VariableValidator:

    def __init__(self):
        
        self.logger = LogManager().get_logger(self.__class__.__name__)

    def validate(
        self,
        variables_1: List[Variable],
        variables_2: List[Variable],
    ):
        """
        Validate two sets of variables for presence, value match, and type annotations.

        Parameters
        ----------
        variables_1 : List[Variable]
            The list of expected variables (from the contract).
        variables_2 : List[Variable]
            The list of actual variables (from the module/system).

        Raises
        ------
        ValueError
            If a variable is missing, has a mismatched value, or fails type annotation validation.
        """
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

        if not variables_2:
            self.logger.debug(
                Constants.LOG_MESSAGE_TEMPLATE.format(
                    operation="Checking variables_2 when variables_1 is missing",
                    status="Finished",
                    details="No actual Variables found for validation"
                )
            )
            raise ValueError(self.context.format_missing_error())

        for vars_1 in variables_1:
            self.logger.debug(
                Constants.LOG_MESSAGE_TEMPLATE.format(
                    operation="Variable validating",
                    status="Progress",
                    details=f"Current vars_1: {vars_1}"
                )
            )
            if vars_1.name not in {var.name for var in variables_2}:
                raise ValueError(self.context.format_missing_error())

        for vars_1 in variables_1:
            vars_2 = next((var for var in variables_2 if var.name == vars_1.name), None)
            if not vars_2:
                raise ValueError(self.context.format_missing_error())

            if vars_1.annotation and vars_1.annotation != vars_2.annotation:
                raise ValueError(
                    self.context.format_mismatch_error(vars_1.annotation, vars_2.annotation)
                )

            if vars_1.value != vars_2.value:
                raise ValueError(
                    self.context.format_mismatch_error(vars_1.value, vars_2.value)
                )

class FunctionValidator:

    def __init__(self):

        self.logger = LogManager().get_logger(self.__class__.__name__)

    def validate(
        self,
        functions_1: List[Function],
        functions_2: List[Function],
    ):
 
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
            return None

        if not functions_2:
            self.logger.debug(
                Constants.LOG_MESSAGE_TEMPLATE.format(
                    operation="Checking functions_2 when functions_1 is missing",
                    status="Finished",
                    details="No actual functions found"
                )
            )
            raise ValueError(Errors.ELEMENT_MISSING.format(functions_1))

        for function_1 in functions_1:
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
                raise ValueError(
                    Errors.ELEMENT_MISMATCH.format(context_name, function_1.name)
                )

        for function_1 in functions_1:
            function_2 = next((f for f in functions_2 if f.name == function_1.name), None)
            if not function_2:
                raise ValueError(Errors.ELEMENT_MISSING.format(function_1))

            self._argument_validator.validate(
                function_1.arguments,
                function_2.arguments,
                function_1.name,
                classname
            )

            if function_1.return_annotation and function_1.return_annotation != function_2.return_annotation:
                raise ValueError(
                    Errors.FUNCTION_RETURN_ANNOTATION_MISMATCH.format(
                        function_1.name,
                        function_1.return_annotation,
                        function_2.return_annotation
                    )
                )

        self.logger.debug(
            Constants.LOG_MESSAGE_TEMPLATE.format(
                operation="Function validating",
                status="Completed",
                details="Validation successful."
            )
        )