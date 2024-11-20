from importspy.models import SpyModel
from ..errors import Errors

def is_subset(spy_model_1: SpyModel, spy_model_2: SpyModel) -> bool:
    """
    Determine if the first SpyModel is a subset of the second SpyModel.

    This function checks whether all relevant attributes (such as functions, classes, methods, 
    superclasses, filename, and version) specified in `spy_model_1` are present in `spy_model_2`. 
    It throws a ValueError with a specific message indicating the type of mismatch.

    Parameters:
    -----------
    - **spy_model_1** (`SpyModel`): The SpyModel whose attributes are being validated.
    - **spy_model_2** (`SpyModel`): The SpyModel against which validation is performed.

    Returns:
    --------
    - **bool**: Returns `True` if `spy_model_1` is a subset of `spy_model_2`, else raises a ValueError.

    Raises:
    -------
    - **ValueError**: Descriptive error highlighting which validation check failed.

    Example usage:
    --------------
    ```
    try:
        result = is_subset(spy_model1, spy_model2)
        print("Validation successful:", result)
    except ValueError as ve:
        print("Validation error:", ve)
    ```
    """
    if spy_model_1.filename and spy_model_1.filename != spy_model_2.filename:
        raise ValueError(Errors.FILENAME_MISMATCH.format(spy_model_1.filename, spy_model_2.filename))
    if spy_model_1.version and spy_model_1.version != spy_model_2.version:
        raise ValueError(Errors.VERSION_MISMATCH.format(spy_model_1.version, spy_model_2.version))
    #Env vars validation
    dict_compare(spy_model_1.env_vars, spy_model_2.env_vars, Errors.ENV_VAR_MISSING, Errors.ENV_VAR_MISMATCH)
    #Variables validation
    dict_compare(spy_model_1.variables, spy_model_2.variables, Errors.VAR_MISSING, Errors.VAR_MISMATCH)
    #Functions validation
    list_compare(spy_model_1.functions, spy_model_2.functions, Errors.FUNCTIONS_MISSING)
    for class_1 in spy_model_1.classes:
        class_2 = next((cls for cls in spy_model_2.classes if cls.name == class_1.name), None)
        if not class_2:
            raise ValueError(Errors.CLASS_MISSING.format(class_1.name))
        # Class attributes validation
        list_compare(class_1.class_attr, class_2.class_attr, Errors.CLASS_ATTRIBUTE_MISSING, class_2.name)
        # Class instance attributes validation
        list_compare(class_1.instance_attr, class_2.instance_attr, Errors.CLASS_INSTANCE_ATTRIBUTE_MISSING, class_2.name)
        # Class methods validation
        list_compare(class_1.methods, class_2.methods, Errors.CLASS_METHOD_MISSING, class_2.name)
        # Superclasses validation
        list_compare(class_1.superclasses, class_2.superclasses, Errors.CLASS_SUPERCLASS_MISSING, class_2.name)
    return True

def list_compare(list1:list, list2:list, missing_error:str, *args):
    for expected_element in list1:
        if expected_element not in list2:
            raise ValueError(missing_error.format(expected_element, *args))

def dict_compare(dict1:dict, dict2:dict, missing_error:str, mismatch_error:str):
    for expected_key, expected_value in dict1.items():
        if expected_key in dict2:
            if expected_value != dict2[expected_key]:
                raise ValueError(mismatch_error.format(expected_key, expected_value, dict2[expected_key]))
        else:
            raise ValueError(missing_error.format(expected_key))