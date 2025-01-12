"""
Runtime Validation Utilities for ImportSpy

This module provides the `RuntimeValidator` class, responsible for validating `Runtime` 
configurations within a `SpyModel`. The validation ensures that runtime architectures 
and associated systems adhere to expected configurations.

Key Responsibilities:
- Validate multiple `Runtime` instances for compatibility.
- Delegate system-level validation to the `SystemValidator`.
- Enforce compliance with expected architectures and system configurations.
"""

from ..models import Runtime
from ..models import System
from typing import List
from ..errors import Errors
from .system_validator import SystemValidator

class RuntimeValidator:
    """
    Validator for Runtime Configurations in ImportSpy

    The `RuntimeValidator` class ensures that `Runtime` instances conform to the 
    expected architecture and system configurations defined within a `SpyModel`. 
    It integrates with the `SystemValidator` for detailed system-level validation.

    Key Features:
    --------------
    - **Architecture Validation**: Ensures that the architecture of a `Runtime` matches 
      the expected configuration.
    - **System Validation Integration**: Delegates system-level validation tasks to 
      the `SystemValidator`.
    - **Support for Multiple Runtimes**: Validates a list of `Runtime` instances against 
      a single expected configuration.

    Methods:
    --------
    - `validate(runtimes_1, runtime_2)`: Compares multiple `Runtime` instances against 
      an expected configuration.
    - `_check_runtimes(runtimes_1, runtime_2)`: Ensures architecture compatibility.

    Example Usage:
    --------------
    ```python
    from importspy.models import Runtime
    from importspy.validators.runtime_validator import RuntimeValidator

    expected_runtime = Runtime(arch="x86_64", systems=[...])
    actual_runtimes = [Runtime(arch="x86_64", systems=[...])]

    validator = RuntimeValidator()
    try:
        validator.validate(actual_runtimes, expected_runtime)
        print("Runtime validation passed.")
    except ValueError as e:
        print(f"Runtime validation failed: {e}")
    ```
    """

    def validate(self,
                 runtimes_1:List[Runtime],
                 runtime_2:Runtime):
        """
        Validates multiple `Runtime` instances against a single expected configuration.

        This method ensures that at least one `Runtime` in the provided list matches 
        the expected architecture and associated system configurations. It delegates 
        system-level validation to the `SystemValidator`.

        Parameters:
        -----------
        runtimes_1 : List[Runtime]
            A list of `Runtime` instances to validate.
        runtime_2 : Runtime
            The expected `Runtime` configuration.

        Raises:
        -------
        ValueError
            If no matching architecture is found or if system validation fails.

        Key Steps:
        ----------
        1. Check Architectures:
            - Validates that at least one `Runtime` in `runtimes_1` has a matching architecture.
        2. Validate Systems:
            - If systems are defined in the matching `Runtime`, delegates validation 
              to the `SystemValidator`.

        Example:
        --------
        ```python
        runtimes_1 = [Runtime(arch="x86_64", systems=[...])]
        runtime_2 = Runtime(arch="x86_64", systems=[...])

        validator = RuntimeValidator()
        validator.validate(runtimes_1, runtime_2)
        ```
        """
        self._check_runtimes(runtimes_1, runtime_2)
        for runtime_1 in runtimes_1:
            if runtime_1.systems:
                system_2:System = runtime_2.systems[0]
                SystemValidator().validate(runtime_1.systems, system_2)
                return
    
    def _check_runtimes(self,
                        runtimes_1:List[Runtime],
                        runtime_2: Runtime):
        """
        Validates that at least one `Runtime` in the list matches the expected architecture.

        Parameters:
        -----------
        runtimes_1 : List[Runtime]
            A list of `Runtime` instances to check.
        runtime_2 : Runtime
            The expected `Runtime` configuration.

        Raises:
        -------
        ValueError
            If no `Runtime` in the list has a matching architecture.

        Example:
        --------
        ```python
        runtimes_1 = [Runtime(arch="arm64"), Runtime(arch="x86_64")]
        runtime_2 = Runtime(arch="x86_64")

        validator = RuntimeValidator()
        validator._check_runtimes(runtimes_1, runtime_2)
        ```
        """
        for runtime_1 in runtimes_1:
            if runtime_1.arch == runtime_2.arch:
                return
        raise ValueError(Errors.RUNTIME_MISSING.format(runtime_2))