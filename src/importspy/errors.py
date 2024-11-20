class Errors:
    
    
    ANALYSIS_RECURSION_WARNING = ("Warning: You cannot analyze the code that itself handles analysis, as this may result "
                                  "in uncontrolled deep recursion. To avoid potential performance issues or stack overflow "
                                  "errors, ensure that the analysis process does not recursively attempt to evaluate itself.")
    
    ### Spy model validation
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