# ImportSpy

![ImportSpy Image](https://github.com/atellaluca/ImportSpy/blob/main/assets/ImportSpy.png)

[![Downloads](https://static.pepy.tech/badge/importspy)](https://pepy.tech/project/importspy)
[![GitHub stars](https://img.shields.io/github/stars/atellaluca/ImportSpy?style=flat-square)](https://github.com/atellaluca/ImportSpy/stargazers)
[![GitHub issues](https://img.shields.io/github/issues/atellaluca/ImportSpy?style=flat-square)](https://github.com/atellaluca/ImportSpy/issues)
[![GitHub forks](https://img.shields.io/github/forks/atellaluca/ImportSpy?style=flat-square)](https://github.com/atellaluca/ImportSpy/network)
[![GitHub license](https://img.shields.io/github/license/atellaluca/ImportSpy?style=flat-square)](https://github.com/atellaluca/ImportSpy/blob/master/LICENSE)

# ImportSpy: Proactive Python Import Control Library

**ImportSpy** is a lightweight Python library that provides **proactive control** over how your Python code is used when imported by other modules or packages. This ensures that external modules importing your code adhere to specific rules, preventing misuse and ensuring smooth integration in larger or modular Python projects.

Designed for plugin-based systems or modular architectures, **ImportSpy** enables real-time validation and import tracking, making sure your code is integrated and used properly in diverse Python environments.

## Table of Contents

1. [Key Features of ImportSpy for Python Code Control](#key-features-of-importspy-for-python-code-control)
2. [Installation: Get Started with ImportSpy](#installation-get-started-with-importspy)
3. [Usage Example: How to Use ImportSpy for Validating Python Modules](#usage-example-how-to-use-importspy-for-validating-python-modules)
    - [Example of a Compliant Importing Python Module](#example-of-a-compliant-importing-python-module)
    - [What Happens During Import Validation](#what-happens-during-import-validation)
4. [Why Use ImportSpy in Your Python Development Projects?](#why-use-importspy-in-your-python-development-projects)
5. [Contributing to ImportSpy](#contributing-to-importspy)
6. [Sponsorship](#sponsorship)
7. [License](#license)

## Key Features of ImportSpy for Python Code Control

- **Proactive control**: With ImportSpy, you can define rules in advance that enforce how your Python code is imported and used by other modules, ensuring compliance. **This allows you to write proactive code that prevents potential future issues** in other Python projects.
- **Dependency validation**: Automatically check that the importing modules respect the required structure, such as functions, classes, and methods. This ensures your Python dependencies are correctly handled.
- **Real-time import tracking**: Monitor how external modules interact with your code, providing valuable insights that help with debugging and optimization in Python development.
- **Error prevention**: Catch potential misuse of your code early, reducing bugs and improving integration stability when your Python code is used in third-party projects.
- **Lightweight and easy to use**: ImportSpy is designed to integrate seamlessly with existing Python projects without the need for complex configurations, making it ideal for Python developers of all levels.

## Installation: Get Started with ImportSpy

You can easily install **ImportSpy** via pip, the Python package manager:

```bash
pip install importspy
```

## Usage Example: How to Use ImportSpy for Validating Python Modules

Here's a simple example showing how to use **ImportSpy** to validate that an importing Python module follows specific rules, such as requiring a particular function and class with specified methods:

```python
from importspy import Spy
from importspy.models import SpyModel, ClassModel

# Define the rules for how your Python code should be used
class MyLibrarySpy(SpyModel):
    functions = ["required_function"]  # Required function in the importing module
    classes = [
        ClassModel(
            name="MyRequiredClass",  # Required class name
            methods=["required_method1", "required_method2"]  # Required methods in the class
        )
    ]

# Check if the importing module complies with the rules
module = Spy().importspy(spymodel=MyLibrarySpy)

if module:
    print(f"Module {module.__name__} is using your library correctly!")
else:
    print("The importing module is not complying with the rules.")
```

### Example of a Compliant Importing Python Module

A Python module that correctly imports and adheres to your defined rules might look like this:

```python
# importing_module.py

class MyRequiredClass:
    def required_method1(self):
        print("Method 1 implemented")

    def required_method2(self):
        print("Method 2 implemented")

def required_function():
    print("Function implemented")
```

### What Happens During Import Validation

If the importing module correctly implements the required functions, classes, and methods, **ImportSpy** will provide this output:

```
Module importing_module is using your library correctly!
```

However, if the importing module does not meet the rules (for example, a function or class is missing), you'll see an error message like:

```
The importing module is not complying with the rules.
```

## Why Use ImportSpy in Your Python Development Projects?

- **Ensure Python code quality**: Set up clear rules for how your code should be used in external Python projects, ensuring proper integration and reducing issues.
- **Improve debugging and development**: By tracking how your Python code is imported and used, you gain valuable insights that speed up the identification of potential problems.
- **Support modular Python architectures**: ImportSpy is particularly suited for modular or plugin-based Python projects, ensuring that all components interact as expected.
- **Proactive Python code**: ImportSpy helps you write code that proactively validates future integrations, preventing errors before they happen. This gives you greater control over your Python code's quality, even when it's used by other teams or developers.

## Contributing to ImportSpy

We welcome contributions! If you find bugs, have suggestions, or want to contribute new features, feel free to open issues or submit pull requests to help improve **ImportSpy**. Whether it's bug reports, feature suggestions, or code contributions, your help is appreciated!

## Sponsorship

You can support the continued development of **ImportSpy** by becoming a sponsor. If you find this project useful and would like to help keep it growing, please consider [sponsoring the project on GitHub](https://github.com/sponsors/atellaluca).

Your sponsorship will help us to dedicate more time to improvements, new features, and support for the community. Thank you for your generosity!

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---