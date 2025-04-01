.. list-table:: ImportSpy Validation Errors
   :widths: 30 70
   :header-rows: 1

   * - **Error Type**
     - **Description**
   * - Missing Elements
     - A required function, class, method, or attribute is missing from the imported module or structure defined in the import contract.
   * - Type Mismatches
     - A return type, argument annotation, or class attribute annotation does not match the expected contract value.
   * - Environmental Issues
     - One or more required environment variables are missing or have invalid values in the current execution environment.
   * - Architecture and Runtime Errors
     - The current CPU architecture or Python interpreter version does not match those specified in the import contract.
   * - Module Filename Mismatch
     - The actual filename of the Python module does not match the `filename` field declared in the import contract.
   * - Version Mismatch
     - The module’s `__version__` attribute does not match the version specified in the import contract.
   * - Variable Missing
     - A declared top-level (global) variable is not found in the module being validated.
   * - Variable Value Mismatch
     - A top-level variable exists, but its value differs from the one declared in the import contract.
   * - Function Return Type Mismatch
     - A function's return annotation does not match the annotation specified in the contract.
   * - Function Argument Mismatch
     - One or more arguments of a function do not match in name, annotation, or default value.
   * - Class Missing
     - A required class is not present in the module.
   * - Class Attribute Missing
     - A class is missing one or more attributes as specified in the import contract.
   * - Class Attribute Type Mismatch
     - A class attribute exists but its type or annotation does not match the declared expectations.
   * - Superclass Mismatch
     - A class does not inherit from one or more superclasses listed in the import contract.
   * - Unsupported Operating System
     - The current OS is not included in the list of allowed platforms (e.g., Linux, Windows, macOS).
   * - Missing Required Runtime
     - A required runtime (architecture, system, or Python interpreter version) is not satisfied.
   * - Unsupported Python Interpreter
     - The Python interpreter (e.g., CPython, IronPython) is not supported by the contract.
