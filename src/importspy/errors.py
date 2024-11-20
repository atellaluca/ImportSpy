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
    GENERIC_FUNCTIONS_MISMATCH = "Functions mismatch: Some functions are not defined."
    CLASS_MISSING = "Missing class: {0} Ensure it is defined."
    GENERIC_CLASS_ATTRIBUTES_MISMATCH = "Class attributes mismatch in Class {0}: some attributes are not defined in the class {0}."
    GENERIC_INSTANCE_ATTRIBUTES_MISMATCH = "Instance attributes mismatch in Class {0}: some attributes are not defined in the __init__ method of the class {0}."
    GENERIC_CLASS_METHODS_MISMATCH = "Methods mismatch in Class {0}: some attributes are not defined in the class {0}."
    GENERIC_CLASS_SUPERCLASSES_MISMATCH = "Superclass mismatch in Class: {0} some superclasses are not defined in the class {0}."