class Errors:
    
    ANALYSIS_RECURSION_WARNING = ("Warning: You cannot analyze the code that itself handles analysis, as this may result "
                                  "in uncontrolled deep recursion. To avoid potential performance issues or stack overflow "
                                  "errors, ensure that the analysis process does not recursively attempt to evaluate itself.")