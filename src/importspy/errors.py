class Errors:
    """
    A centralized repository for error messages used throughout the ImportSpy package.

    This class defines a comprehensive set of error and warning messages with placeholders 
    that can be dynamically populated at runtime. These messages are typically associated 
    with constraints not being met by `SpyModel` instances or related validation processes 
    within the ImportSpy framework. By centralizing error messages, this class ensures 
    consistency in error reporting and improves maintainability.

    Attributes:
        ANALYSIS_RECURSION_WARNING (str): Warning message indicating that analyzing 
            code handling its own analysis may lead to uncontrolled recursion. This typically 
            occurs when the code containing the `SpyModel` definition is executed instead of 
            the intended external module, leading to the analysis process inadvertently 
            evaluating itself. To prevent performance issues or stack overflow errors, ensure 
            that the analysis does not recursively process its own codebase.

        ### SpyModel validation errors
        FILENAME_MISMATCH (str): Error message for a mismatch between expected and 
            actual filenames. Includes placeholders for the filenames.
        VERSION_MISMATCH (str): Error message for a mismatch between expected and 
            actual versions. Includes placeholders for the versions.
        ENV_VAR_MISMATCH (str): Error message for a mismatch between expected and 
            actual environment variable values. Includes placeholders for the variable name, 
            expected value, and found value.
        ENV_VAR_MISSING (str): Error message for a missing environment variable. Includes a 
            placeholder for the variable name.
        VAR_MISMATCH (str): Error message for a mismatch between expected and 
            actual variable values. Includes placeholders for the variable name, expected value, 
            and found value.
        VAR_MISSING (str): Error message for a missing variable. Includes a placeholder 
            for the variable name.
        FUNCTIONS_MISSING (str): Error message for a missing function. Includes a placeholder 
            for the function name.
        CLASS_MISSING (str): Error message for a missing class. Includes a placeholder 
            for the class name.
        CLASS_ATTRIBUTE_MISSING (str): Error message for a missing class attribute. Includes 
            placeholders for the attribute name and class name.
        CLASS_INSTANCE_ATTRIBUTE_MISSING (str): Error message for a missing instance 
            attribute in a class. Includes placeholders for the attribute name and class name.
        CLASS_METHOD_MISSING (str): Error message for a missing method in a class. Includes 
            placeholders for the method name and class name.
        CLASS_SUPERCLASS_MISSING (str): Error message for a missing superclass in a class 
            hierarchy. Includes placeholders for the missing superclass and the current class.

        ### SpyArchModule validation errors
        INVALID_ARCHITECTURE (str): Error message for an invalid architecture. Includes placeholders 
            for the invalid architecture and the list of known architectures.
    """

    ANALYSIS_RECURSION_WARNING = (
        "Warning: You cannot analyze the code that itself handles analysis, as this may result "
        "in uncontrolled deep recursion. To avoid potential performance issues or stack overflow "
        "errors, ensure that the analysis process does not recursively attempt to evaluate itself."
    )

    # Module validation
    FILENAME_MISMATCH  = "Filename mismatch: {0} != {1}"
    VERSION_MISMATCH = "Version mismatch: {0} != {1}"
    ENV_VAR_MISMATCH = "Value mismatch for environment variable '{0}': expected '{1}', found '{2}'."
    ENV_VAR_MISSING = "Missing environment variable: '{0}'. Ensure it is defined in the system."
    VAR_MISMATCH = "Value mismatch for variable '{0}': expected '{1}', found '{2}'"
    VAR_MISSING = "Missing variable: '{0}'. Ensure it is defined."
    FUNCTIONS_MISSING = "Missing function: '{0}'. Ensure it is defined."
    CLASS_MISSING = "Missing class: {0}. Ensure it is defined."
    CLASS_ATTRIBUTE_MISSING = "Missing class attribute: '{0}'. Ensure it is defined in class '{1}'."
    CLASS_INSTANCE_ATTRIBUTE_MISSING = "Missing class instance attribute: '{0}'. Ensure it is defined in class '{1}'."
    CLASS_METHOD_MISSING = "Missing class method: '{0}'. Ensure it is defined in class '{1}'."
    CLASS_SUPERCLASS_MISSING = "Missing class superclass: '{0}'. Make sure that '{1}' extends {0}."
    INVALID_ATTRIBUTE_TYPE = "Invalid attribute type '{0}'. Known attributes are: {1}"

    # Runtime validation
    INVALID_ARCHITECTURE = "Invalid architecture '{0}'. Known architectures are: {1}"