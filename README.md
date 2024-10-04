# 🕵️‍♂️ ImportSpy

![ImportSpy Image](https://github.com/atellaluca/ImportSpy/blob/main/assets/ImportSpy.png)

[![GitHub issues](https://img.shields.io/github/issues/atellaluca/ImportSpy?style=flat-square)](https://github.com/atellaluca/ImportSpy/issues)
[![GitHub stars](https://img.shields.io/github/stars/atellaluca/ImportSpy?style=flat-square)](https://github.com/atellaluca/ImportSpy/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/atellaluca/ImportSpy?style=flat-square)](https://github.com/atellaluca/ImportSpy/network)
[![GitHub license](https://img.shields.io/github/license/atellaluca/ImportSpy?style=flat-square)](https://github.com/atellaluca/ImportSpy/blob/master/LICENSE)

**ImportSpy** is a tool that allows you to monitor and dynamically trace imported modules in a Python script, with advanced features like module re-importing and optional validation. The core of the package is the `Spy` class, which inspects the stack and safely re-imports modules, even handling recursion detection.

---

## 🔍 What is ImportSpy?

ImportSpy is a Python package designed to track and monitor imported modules during script execution. Using the `Spy` class, you can inspect the stack, identify the module that called the function, and dynamically re-import it, with the option to add a validation function to ensure the module is correctly loaded.

Recursion detection and the use of `importlib` for dynamic import management make ImportSpy a powerful tool for developers who want more control over the modules being loaded.

---

## 🚨 Key Features

- **Dynamic Import with Validation**: The `Spy` class allows dynamic re-importing of modules, with an optional validation function that checks if the imported module meets specific criteria.
- **Recursion Detection**: ImportSpy automatically detects recursion, raising an error if the module being imported is the same as the calling module.
- **Stack Inspection**: Uses the `inspect` module to access the stack and identify the context in which a module is being imported.
- **Custom Import Handling**: By using `importlib`, ImportSpy gives you control over how and when a module is imported, providing flexibility for complex projects.

---

## 💼 Use Cases

- **Debugging Complex Projects**: Track which modules are loaded and when, especially in projects that need dynamic imports or where you want to avoid redundant module loading.
- **Dependency Optimization**: The ability to validate imported modules and detect recursion helps you optimize how dependencies are managed, reducing potential errors or conflicts.
- **Plugin-Based Systems**: When developing modular architectures that extend via plugins, ImportSpy helps monitor which modules are imported by plugins and validates their correct integration.
- **Import Validation**: The optional validation function allows you to apply custom logic to ensure that the imported module meets your project’s requirements.

---

## 📦 Installation

Setting up ImportSpy is simple! You can install it directly from PyPI with:

```bash
pip install importspy
```

Then, start using it by importing and configuring the Spy:

```python
from importspy import Spy

module = Spy().importspy(validation=lambda mod: hasattr(mod, 'required_attribute'))

if module:
    print(f"Module {module.__name__} imported successfully!")
else:
    print("Module import failed validation.")
```

---

## 📚 Documentation

You can find the full documentation for ImportSpy at [this link](https://importspy.readthedocs.io).

The documentation includes:
- Detailed usage examples
- API reference for the `Spy` class
- Configuration options
- Best practices for integrating ImportSpy in your Python projects

---

## 🚀 How to Use ImportSpy

The core of ImportSpy is the `Spy` class, designed to facilitate dynamic import monitoring. Here’s how to use it to re-import a module with optional validation:

1. **Create a `Spy` instance**: Start by creating an instance of the `Spy` class.
2. **Use `importspy` to dynamically re-import a module**: Call the `importspy` method to re-import the calling module. You can also pass an optional validation function.
3. **Handle recursion errors**: If the method detects recursion within the same module (the caller and current frames originate from the same file), a `ValueError` is raised to prevent infinite loops.

### Example

```python
from importspy import Spy

spy = Spy()

# Dynamically re-import the calling module with validation
module = spy.importspy(validation=lambda mod: mod.__name__ == "target_module")

# If the module is valid, proceed with the code
if module:
    print(f"Module {module.__name__} imported and validated!")
else:
    print("Module import failed or did not pass validation.")
```

### How it works:

- **Dynamic Import**: The `importspy` method inspects the call stack to identify which module triggered the import and re-imports it dynamically using `importlib.util`.
- **Optional Validation**: You can pass a validation function that checks the module after it's imported. The function must return `True` for the module to be considered valid.
- **Recursion Detection**: ImportSpy prevents the re-importing of the same module by detecting recursion and raising an error if the current and caller modules are the same.

---

## 🔧 Handling Dynamic Imports and Recursion

The `importspy` method uses the `inspect` library to identify the module that called the function. It then uses `importlib.util` to dynamically re-import that module. You can also provide an optional validation function to perform checks on the imported module.

---

## 🌟 Why Use ImportSpy?

ImportSpy gives you detailed and configurable control over the modules imported in your Python projects. With the ability to dynamically re-import modules and validate imports, ImportSpy is a valuable tool for improving dependency management and optimizing the import flow.

---

## 🛠️ Contributing

We welcome contributions! If you’d like to help improve ImportSpy, please check out our [contributing guide](https://github.com/atellaluca/ImportSpy/blob/main/CONTRIBUTING.md) to get started. Whether it’s reporting bugs, proposing new features, or submitting pull requests, we’re happy to collaborate with you!

---

## 📄 License

This project is licensed under the **MIT License**—see the [LICENSE](https://github.com/atellaluca/ImportSpy/blob/main/LICENSE) file for details.

---

## 📫 Contact

Have questions or suggestions? Feel free to reach out! We’re always happy to hear how ImportSpy is being used in your Python projects.

---

## 🕵️‍♂️ Spy on Your Imports Today!

Don’t let imports slow your project down. Add **ImportSpy** to your toolkit and take control of your dependencies. Happy coding! 🎉
