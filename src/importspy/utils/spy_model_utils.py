from importspy.models import SpyModel

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
        raise ValueError(f"Filename mismatch: {spy_model_1.filename} != {spy_model_2.filename}")
    if spy_model_1.version and spy_model_1.version != spy_model_2.version:
        raise ValueError(f"Version mismatch: {spy_model_1.version} != {spy_model_2.version}")
    spy_model_2_env_vars = spy_model_2.env_vars
    for expected_key, expected_value in spy_model_1.env_vars.items():
        if expected_key in spy_model_2_env_vars:
            if expected_value != spy_model_2_env_vars[expected_key]:
                raise ValueError(f"Value mismatch for environment variable '{expected_key}': expected '{expected_value}', found '{spy_model_2_env_vars[expected_key]}'."
            ) 
        else:
            raise ValueError(f"Missing environment variable: '{expected_key}'. Ensure it is defined in the system.")
    spy_model_2_variables = spy_model_2.variables
    for expected_key, expected_value in spy_model_1.variables.items():
        if expected_key in spy_model_2_variables:
            if expected_value != spy_model_2_variables[expected_key]:
                raise ValueError(f"Value mismatch for variable '{expected_key}': expected '{expected_value}', found '{spy_model_2_variables[expected_key]}'."
            )
        else:
            raise ValueError(f"Missing variable: '{expected_key}'. Ensure it is defined.")
    if spy_model_1.functions and not set(spy_model_1.functions).issubset(spy_model_2.functions):
        raise ValueError("Functions mismatch: Some functions are not present in the second model.")
    for class_1 in spy_model_1.classes:
        class_2 = next((cls for cls in spy_model_2.classes if cls.name == class_1.name), None)
        if not class_2:
            raise ValueError(f"Class not found: {class_1.name}")
        if class_1.class_attr and not set(class_1.class_attr).issubset(class_2.class_attr):
            raise ValueError(f"Class attributes mismatch in {class_1.name}")
        if class_1.instance_attr and not set(class_1.instance_attr).issubset(class_2.instance_attr):
            raise ValueError(f"Instance attributes mismatch in {class_1.name}")
        if class_1.methods and not set(class_1.methods).issubset(class_2.methods):
            raise ValueError(f"Methods mismatch in {class_1.name}")
        if class_1.superclasses and not set(class_1.superclasses).issubset(class_2.superclasses):
            raise ValueError(f"Superclass mismatch in {class_1.name}")
    return True
