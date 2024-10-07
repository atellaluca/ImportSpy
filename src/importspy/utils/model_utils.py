from importspy.models import SpyModel

def is_subset(spy_model_1: SpyModel, spy_model_2: SpyModel) -> bool:
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

    
