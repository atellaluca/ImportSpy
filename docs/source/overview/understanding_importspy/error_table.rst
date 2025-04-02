.. list-table:: ImportSpy Validation Errors
   :widths: 30 70
   :header-rows: 1

   * - **Error Type**
     - **Description**
   * - `Missing Elements`
     - A required **function**, **class**, **method**, or **attribute** is not found in the module or structure defined in the import contract.
   * - `Type Mismatch`
     - A return annotation, argument type, or class attribute type does **not match** the one declared in the contract.
   * - `Value Mismatch`
     - A variable or attribute exists but has a **different value** than expected (e.g., metadata mismatch).
   * - `Function Argument Mismatch`
     - A function's arguments do **not match in name, annotation, or default values**.
   * - `Function Return Type Mismatch`
     - The return type annotation of a function differs from the contract.
   * - `Class Missing`
     - A required class is **absent** from the module.
   * - `Class Attribute Missing`
     - One or more declared **class or instance attributes** are missing.
   * - `Class Attribute Type Mismatch`
     - A class attribute exists, but its **type or annotation** differs from what is expected.
   * - `Superclass Mismatch`
     - A class does not inherit from one or more required **superclasses** as declared.
   * - `Variable Missing`
     - A required **top-level variable** (e.g., `plugin_name`) is not defined in the module.
   * - `Variable Value Mismatch`
     - A variable exists but its value does not match the one declared in the contract.
   * - `Filename Mismatch`
     - The actual filename of the module differs from the one declared in `filename`.
   * - `Version Mismatch`
     - The module’s `__version__` (if defined) differs from the expected version.
   * - `Unsupported Operating System`
     - The current OS is **not included** in the allowed platforms (e.g., Linux, Windows, macOS).
   * - `Missing Required Runtime`
     - A required **architecture, OS, or interpreter version** is not satisfied.
   * - `Unsupported Python Interpreter`
     - The current interpreter (e.g., CPython, PyPy, IronPython) is not supported by the contract.
   * - `Missing Environment Variable`
     - A declared environment variable is **not present** in the current context.
   * - `Invalid Environment Variable`
     - An environment variable exists but contains an **unexpected value**.
