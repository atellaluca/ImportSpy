from importspy import Spy
from importspy.models import SpyModel, ClassModel
from typing import List

class MyLibrarySpy(SpyModel):
    """
    Defines the expected structure and rules for modules that import the developer's code.

    This SpyModel enforces that any module importing this code must include:
    - A function named 'required_function'.
    - A class named 'MyRequiredClass' that implements two specific methods: 'required_method1' and 'required_method2'.

    This proactive approach helps prevent misuse of the developer's code and ensures proper integration.
    """
    functions: List[str] = ["required_function"]  # The importing module must define a function named "required_function"
    classes: List[ClassModel] = [
        ClassModel(
            name="MyRequiredClass",  # The importing module must define a class named "MyRequiredClass"
            methods=["required_method1", "required_method2"]  # The class must implement these two methods
        )
    ]

# Instantiate ImportSpy to validate the importing module
spy = Spy()

# Dynamically import the module and check if it complies with the rules
module = spy.importspy(spymodel=MyLibrarySpy)

# Check if the module follows the rules defined by the developer
if module:
    print(f"Module {module.__name__} is using your library correctly!")
else:
    print("The importing module does not comply with the rules.")
