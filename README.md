# ImportSpy

![ImportSpy Image](https://github.com/atellaluca/ImportSpy/blob/main/assets/ImportSpy.png)

[![GitHub issues](https://img.shields.io/github/issues/atellaluca/ImportSpy?style=flat-square)](https://github.com/atellaluca/ImportSpy/issues)
[![GitHub stars](https://img.shields.io/github/stars/atellaluca/ImportSpy?style=flat-square)](https://github.com/atellaluca/ImportSpy/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/atellaluca/ImportSpy?style=flat-square)](https://github.com/atellaluca/ImportSpy/network)
[![GitHub license](https://img.shields.io/github/license/atellaluca/ImportSpy?style=flat-square)](https://github.com/atellaluca/ImportSpy/blob/master/LICENSE)

**ImportSpy** is a Python package designed to monitor, validate, and dynamically manage module imports in real-time. With its robust features, it excels in plugin-based architectures, offering dynamic module re-importing, customizable validation, and recursion detection, making your code more modular, secure, and efficient.

## Table of Contents


1. [Key Features](#key-features)
2. [SpyModel: A Powerful Tool for Code Validation](#spymodel-a-powerful-tool-for-code-validation-and-retroactive-compatibility)
3. [Use Cases](#use-cases)
4. [Installation](#installation)
5. [Documentation](#documentation)
6. [How to Use ImportSpy](#how-to-use-importspy)
7. [Usage Example](#usage-example)
8. [Handling Dynamic Imports and Recursion](#handling-dynamic-imports-and-recursion)
9. [Why Use ImportSpy?](#why-use-importspy)
10. [Contributing](#contributing)
11. [Donations and Sponsorship](#donations-and-sponsorship)
12. [License](#license)
13. [Contact](#contact)

---

## Key Features
- **Dynamic Import with Validation**: Re-import modules dynamically and validate their content with custom models, ensuring that they meet your project’s structural and functional requirements.
- **SpyModel for Full Python Code Modeling and Retroactive Validation**: Define and validate the expected structure of Python code—including file names, versions, functions, and classes—and apply retroactive validation to ensure imported code adheres to required standards, even if written without prior validation considerations.
- **Recursion Detection**: Automatically detects and prevents recursion by raising an error when a module attempts to import itself.
- **Stack Inspection**: Trace import origins by inspecting the call stack, facilitating debugging and import tracking.
- **Plugin Isolation**: Perfect for plugin-based systems, ImportSpy isolates and validates plugins before integration, enhancing system modularity and stability.

## SpyModel: A Powerful Tool for Code Validation and Retroactive Compatibility

The `SpyModel` class in **ImportSpy** serves a critical role in ensuring that the code written by developers is fully compatible and executable when imported by other modules. It allows you to **retroactively validate** and enforce rules on existing code, ensuring that the imported code conforms to the expected structure and behavior. This means that even if the code was written without specific validation in mind, `SpyModel` makes it possible to retroactively apply those validations when the code is imported into other modules.

### SpyModel Attributes
- **filename**: *(Optional[str])* – Specifies the file name of the module to be imported, ensuring the correct module is being validated.
- **version**: *(Optional[str])* – Enforces version control by ensuring that the imported module matches a specific version, which is critical when working with different versions of a library or module.
- **functions**: *(Optional[List[str]])* – Defines a list of required functions that must be present in the imported module. This ensures that even pre-existing code meets functional expectations when imported.
- **classes**: *(Optional[List[ClassModel]])* – A list of class models that define the required classes and their methods. This ensures that existing classes in the imported module contain the necessary methods and behaviors required by the importing module.

### Example of Retroactive Code Validation with SpyModel

```python
from importspy import Spy
from importspy.models import SpyModel, ClassModel
from typing import List

# Define validation model for retroactive code validation
class PluginSpy(SpyModel):
    filename: str = "my_plugin.py"
    version: str = "1.0"
    functions: List[str] = ["setup", "teardown"]  # Ensure these functions exist
    classes: List[ClassModel] = [
        ClassModel(
            name="MyPluginClass",
            methods=["initialize", "shutdown"]  # Ensure these methods exist in the class
        )
    ]

# Use Spy to dynamically import and validate the module based on the retroactive model
module = Spy().importspy(spymodel=PluginSpy)

if module:
    print(f"Module {module.__name__} imported and validated retroactively!")
else:
    print("Module import failed retroactive validation.")
```

### How SpyModel Works Retroactively
- **Retroactive Enforcement**: Even if the code was written without specific validation, `SpyModel` can enforce compatibility rules when that code is imported into other modules. This enables developers to ensure the compatibility of legacy or third-party code without needing to modify the original codebase.
- **Dynamic Adaptation**: The importing module can specify which functions, classes, or methods the imported module should contain, ensuring the module behaves as expected without needing direct modifications.

---

## Use Cases

- **Dynamic Code Validation**: Ensure imported modules conform to predefined structures using `SpyModel`.
- **Plugin-Based Architectures**: Validate and isolate plugins before integration to ensure system stability.
- **Version-Specific Imports**: Ensure compatibility by enforcing version requirements on imported modules.

---

## Installation

Install **ImportSpy** with pip:

```bash
pip install importspy
```

---

## Documentation

Detailed documentation and advanced usage examples can be found [here](https://importspy.readthedocs.io).

---

## How to Use ImportSpy

1. **Create a `Spy` instance** and configure it with a validation model or `SpyModel` to define what the module should contain.
2. **Import the module** using `importspy` and pass the validation function or `SpyModel` to check its structure or content.
3. **Handle recursion errors** if a module attempts to import itself, raising a `ValueError` to avoid infinite loops.

---

## Usage Example

```python
from importspy import Spy
from importspy.models import SpyModel, ClassModel
from typing import List

class PluginSpy(SpyModel):
    filename: str = "my_plugin.py"
    version: str = "1.0"
    functions: List[str] = ["setup", "teardown"]
    classes: List[ClassModel] = [
        ClassModel(name="MyPluginClass", methods=["initialize", "shutdown"])
    ]

module = Spy().importspy(spymodel=PluginSpy)

if module:
    print(f"Module {module.__name__} imported successfully!")
else:
    print("Module import failed validation.")
```

---

## Handling Dynamic Imports and Recursion

ImportSpy uses `importlib` and `inspect` to manage dynamic imports and detect recursion, ensuring that modules are imported safely and meet the required criteria.

---

## Why Use ImportSpy?

ImportSpy provides powerful control over how modules are imported and validated, making it an essential tool for modular applications, plugin systems, and projects with dynamic dependencies.

---

## Contributing

We welcome contributions! Feel free to open issues or submit pull requests. See the `CONTRIBUTING.md` file for more details.

---

## Donations and Sponsorship

If you find ImportSpy useful and would like to support its continued development, consider sponsoring or donating:

- GitHub Sponsors: [Sponsor this project on GitHub](https://github.com/sponsors/atellaluca)
- PayPal: [Donate via PayPal](https://www.paypal.com/donate/?hosted_button_id=4SG8LU8ZZAM68)

Your support helps us maintain and improve the project. Thank you!

---

## License

This project is licensed under the MIT License.

---

## Contact

For questions, feel free to reach out via the GitHub repository.
