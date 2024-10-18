from importspy.models import SpyModel

def is_subset(spy_model_1: SpyModel, spy_model_2: SpyModel) -> bool:
    """
    Determine if the first SpyModel is a subset of the second SpyModel.

    This function provides a proactive way to validate that a module (represented by `spy_model_1`) 
    adheres to the structure and rules defined by another module (represented by `spy_model_2`).
    This validation ensures that the importing module contains all the required functions, 
    classes, methods, superclasses, filename, and version specified in the `SpyModel`.

    In a **proactive programming** approach, this function is used to ensure that the importing 
    module complies with the expected structure defined by the developer's code. If any field 
    in `spy_model_1` is empty (such as functions, classes, etc.), it is ignored during the validation.

    Parameters:
    -----------

    - **spy_model_1** (`SpyModel`): The first `SpyModel` that contains the structure and rules to be validated against another module.
    - **spy_model_2** (`SpyModel`): The second `SpyModel` that represents the module being validated.

    Returns:
    --------

    - **bool**: Returns `True` if all non-empty attributes (functions, classes, methods, superclasses, filename, and version) in `spy_model_1` are present in `spy_model_2`. Otherwise, it returns `False`.


    How it works:
    -------------

    - **Filename validation**: If a filename is provided in `spy_model_1`, it checks whether the filename in `spy_model_2` matches.
    - **Version validation**: If a version is specified in `spy_model_1`, it ensures that `spy_model_2` has the same version.
    - **Functions and classes validation**: It checks whether all functions and classes defined in `spy_model_1` are present in `spy_model_2`, along with their respective methods and superclasses.
    
    This function helps ensure that any importing module respects the rules set by the developer, 
    reducing the risk of improper usage and integration issues.
    """
    if spy_model_1.filename and spy_model_1.filename != spy_model_2.filename:
        return False
    if spy_model_1.version and spy_model_1.version != spy_model_2.version:
        return False
    if spy_model_1.variables:
        if not set(spy_model_1.variables).issubset(spy_model_2.variables):
            return False
    if spy_model_1.functions:
        if not set(spy_model_1.functions).issubset(spy_model_2.functions):
            return False
    for class_1 in spy_model_1.classes:
        class_2 = next((cls for cls in spy_model_2.classes if cls.name == class_1.name or class_1.name is None), None)
        if not class_2:
            return False
        if class_1.class_attr:
            if not set(class_1.class_attr).issubset(class_2.class_attr):
                return False
        if class_1.instance_attr:
            if not set(class_1.instance_attr).issubset(class_2.instance_attr):
                return False
        if class_1.methods:
            if not set(class_1.methods).issubset(class_2.methods):
                return False
        if class_1.superclasses:
            if not set(class_1.superclasses).issubset(class_2.superclasses):
                return False
    
    return True
