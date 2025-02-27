Error Table
===========

The following table lists all validation errors that ImportSpy may raise.

.. list-table:: ImportSpy Validation Errors
   :widths: 30 70
   :header-rows: 1

   * - Error Type
     - Description
   * - Missing Elements
     - A required function, class, or attribute is missing from the imported module.
   * - Type Mismatches
     - A function’s return type or parameter types do not match expected values.
   * - Environmental Issues
     - A required environment variable is missing or has an unexpected value.
   * - Architecture and Runtime Errors
     - The CPU architecture or Python runtime version is incompatible.
   * - Module Filename Mismatch
     - The expected module filename does not match the actual filename.
   * - Version Mismatch
     - The expected module version does not match the detected version.
   * - Variable Missing
     - A required global variable is missing from the module.
   * - Variable Value Mismatch
     - A global variable exists but its value is different from the expected one.
   * - Function Return Type Mismatch
     - The function's return type does not match the expected type.
   * - Function Argument Mismatch
     - A function argument does not match the expected name, type, or default value.
   * - Class Missing
     - A required class is missing from the module.
   * - Class Attribute Missing
     - A required attribute is missing from a class.
   * - Class Attribute Type Mismatch
     - A class attribute exists but has a different type than expected.
   * - Superclass Mismatch
     - A class is missing a required superclass declaration.
   * - Unsupported Operating System
     - The detected OS is not among the supported operating systems.
   * - Missing Required Runtime
     - A required runtime configuration is not present.
   * - Unsupported Python Interpreter
     - The detected Python interpreter does not match the expected one.
