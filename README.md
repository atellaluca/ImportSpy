# ImportSpy

![ImportSpy Image](https://github.com/atellaluca/ImportSpy/blob/main/assets/ImportSpy.png)

[![GitHub issues](https://img.shields.io/github/issues/atellaluca/ImportSpy?style=flat-square)](https://github.com/atellaluca/ImportSpy/issues)
[![GitHub stars](https://img.shields.io/github/stars/atellaluca/ImportSpy?style=flat-square)](https://github.com/atellaluca/ImportSpy/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/atellaluca/ImportSpy?style=flat-square)](https://github.com/atellaluca/ImportSpy/network)
[![GitHub license](https://img.shields.io/github/license/atellaluca/ImportSpy?style=flat-square)](https://github.com/atellaluca/ImportSpy/blob/master/LICENSE)

**ImportSpy** is a Python package designed to monitor and dynamically trace the imported modules in Python scripts, providing advanced features like module re-importing, validation, and proactive integration for plugin-based architectures. With ImportSpy, your code can react to imports dynamically, enabling a new level of control and modularity.

## Table of Contents
1. [What is ImportSpy?](#what-is-importspy)
2. [Key Features](#key-features)
3. [Use Cases](#use-cases)
4. [Installation](#installation)
5. [Documentation](#documentation)
6. [How to Use ImportSpy](#how-to-use-importspy)
7. [Usage Example](#usage-example)
8. [Handling Dynamic Imports and Recursion](#handling-dynamic-imports-and-recursion)
9. [Why Use ImportSpy?](#why-use-importspy)
10. [Contributing](#contributing)
11. [License](#license)
12. [Contact](#contact)

---

## What is ImportSpy?

**ImportSpy** is a Python package designed to track, monitor, and validate the importation of modules during script execution. By leveraging the `Spy` class, developers can dynamically re-import modules, apply validation functions, and ensure that each import adheres to the expected behavior and structure.

ImportSpy provides powerful features like **recursion detection** to prevent redundant imports, **stack inspection** for a clear picture of module interactions, and the ability to validate modules dynamically. This makes it an ideal solution for plugin-based architectures and projects requiring enhanced modularity.

## Key Features

- **Dynamic Import with Validation**: The `Spy` class allows for the dynamic re-importation of modules with an optional validation function. This function can check if the imported module meets specific requirements, ensuring correct usage.
- **Recursion Detection**: Automatically detects and prevents recursion by raising an error if a module attempts to import itself repeatedly, avoiding infinite loops.
- **Stack Inspection for Proactive Behavior**: Uses the `inspect` module to determine the context of an import. This enables your framework to adopt **proactive behavior**, executing specific actions when a plugin imports the framework itself.
- **Custom Import Handling**: Through `importlib`, ImportSpy offers flexibility in how modules are imported, letting developers control when and how modules are loaded. This is useful in complex, modular projects where dependencies must be carefully managed.
- **Plugin Isolation and Validation**: Ensures each plugin operates in its own execution context, validating the integration of new plugins to maintain system stability and avoid conflicts.

## Use Cases

### 1. Debugging Complex Projects
Monitor which modules are imported and when. ImportSpy helps you gain insight into dynamic imports, especially in scenarios with intricate dependencies or where multiple modules interact in complex ways.

### 2. Dependency Optimization
Use ImportSpy to identify and validate dependencies dynamically, reducing the potential for redundant imports or dependency conflicts. The validation step helps developers ensure that the imported module matches the expected version and meets functional requirements.

### 3. Plugin-Based Architectures
ImportSpy is particularly well-suited for **plugin-based systems**. When developing a modular architecture that relies on plugins, ImportSpy can monitor the imports performed by those plugins and validate their correct integration. Additionally, it enables the framework to respond proactively based on which plugin is importing it, providing increased control.

### 4. Import Validation for Security
With ImportSpy, you can apply a validation function during imports to ensure that only authorized or trusted modules are loaded, improving the security of your application. This is particularly important in open or extensible environments where plugins from third parties might be introduced.

## Installation
Setting up ImportSpy is simple! You can install it directly from PyPI with:

```sh
pip install importspy
```

Then, start using it by importing and configuring the `Spy` class:

```python
from importspy import Spy
import inspect
from types import ModuleType

# Example validation function to ensure the module has a required attribute
module = Spy().importspy(validation=lambda mod: hasattr(mod, 'required_attribute'))

if module:
    print(f"Module {module.__name__} imported successfully!")
else:
    print("Module import failed validation.")
```

## Documentation
You can find the full documentation for ImportSpy [here](https://importspy.readthedocs.io).

The documentation includes:
- Detailed usage examples
- API reference for the `Spy` class
- Configuration options
- Best practices for integrating ImportSpy into your Python projects

## How to Use ImportSpy

The core of ImportSpy is the `Spy` class, designed to facilitate dynamic import monitoring and reactivity. Here’s how to use it:

1. **Create a `Spy` instance**: Start by creating an instance of the `Spy` class.
2. **Use `importspy` to dynamically re-import a module**: Call the `importspy` method to dynamically re-import the calling module. Optionally, pass a validation function to ensure the module meets custom requirements.
3. **Handle recursion errors**: ImportSpy detects recursion, and a `ValueError` is raised if recursion is detected within the same module to prevent infinite loops.

## Usage Example

**Plugin Validation Example**

This example demonstrates how to use ImportSpy to dynamically import and validate a plugin that extends a base `Plugin` class.

1. **Setting up the Spy in your main project**:

```python
from importspy import Spy
import inspect
from types import ModuleType

class Plugin:
    pass

def condition(module: ModuleType) -> bool:
    for class_name, class_obj in inspect.getmembers(module, inspect.isclass):
        if issubclass(class_obj, Plugin) and class_obj is not Plugin:
            return True
    return False

# Import the plugin using Spy with the validation function
imported_module = Spy().importspy(validation=condition)

print(imported_module)
```

2. **Creating a plugin**:

```python
from your_package import Plugin

class MyPlugin(Plugin):
    def add_extension(self):
        print("The extension was added")
```

## Handling Dynamic Imports and Recursion

ImportSpy uses the `inspect` library to identify the module that called the function and `importlib.util` to dynamically re-import that module. This approach enables **dynamic import management** and **optional validation** to ensure correctness.

## Why Use ImportSpy?

ImportSpy provides detailed, configurable control over the modules in your Python project. By using features like **dynamic re-import**, **context-based validation**, and **proactive response capabilities**, ImportSpy helps manage dependencies, enhance modularity, and secure the import process, making it a powerful addition to any Python developer's toolkit.

## Contributing
We welcome contributions! If you’d like to help improve ImportSpy, please check out our [contributing guide](https://github.com/atellaluca/ImportSpy/blob/main/CONTRIBUTING.md) to get started. Whether it's reporting bugs, proposing new features, or submitting pull requests, we are eager to collaborate.

## License
This project is licensed under the MIT License - see the [LICENSE](https://github.com/atellaluca/ImportSpy/blob/main/LICENSE) file for details.

## Contact
Have questions or suggestions? Feel free to reach out! We’re always interested in hearing how ImportSpy is being used in your Python projects.

---
**Spy on Your Imports Today!** 🕵️‍♂️ 
