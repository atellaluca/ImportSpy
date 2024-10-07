from importspy.models import SpyModel

def is_subset(spy_model_1: SpyModel, spy_model_2: SpyModel) -> bool:
    """
    Check if the first SpyModel is a subset of the second SpyModel.

    This function compares two `SpyModel` instances to determine if the first model
    is a subset of the second model. It verifies that all non-empty functions and classes 
    defined in the first model are present in the second model, along with their respective 
    methods, superclasses, filename, and version. If any function, class, or other attribute
    in the first model is empty, it is ignored in the subset check.

    :param spy_model_1: 
        The first `SpyModel` instance to check.
    :type spy_model_1: SpyModel

    :param spy_model_2: 
        The second `SpyModel` instance against which the first model is checked.
    :type spy_model_2: SpyModel

    :return: 
        True if all non-empty functions, classes, and other attributes in `spy_model_1` 
        are also present in `spy_model_2`, False otherwise.
    :rtype: bool
    """
    if spy_model_1.filename and spy_model_1.filename != spy_model_2.filename:
        return False
    if spy_model_1.version and spy_model_1.version != spy_model_2.version:
        return False
    if spy_model_1.functions:
        if not set(spy_model_1.functions).issubset(spy_model_2.functions):
            return False
    for class_1 in spy_model_1.classes:
        class_2 = next((cls for cls in spy_model_2.classes if cls.name == class_1.name or class_1.name is None), None)
        if not class_2:
            return False
        if class_1.methods:
            if not set(class_1.methods).issubset(class_2.methods):
                return False
        if class_1.superclasses:
            if not set(class_1.superclasses).issubset(class_2.superclasses):
                return False
    return True


    
