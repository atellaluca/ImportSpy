| Category   | Context       | Error Message |
|------------|---------------|---------------|
| `missing`  | `runtime`     | The runtime `CPython 3.12` is declared but missing. Ensure it is properly defined and implemented. |
|            | `environment` | The environment variable `DEBUG` is declared but missing. Ensure it is properly defined and implemented. |
|            | `module`      | The variable `plugin_name` in module `extension.py` is declared but missing. Ensure it is properly defined and implemented. |
|            | `class`       | The method `run` in class `Plugin` is declared but missing. Ensure it is properly defined and implemented. |
| `mismatch` | `runtime`     | The runtime `CPython 3.12` does not match the expected value. Expected: `CPython 3.11`, Found: `CPython 3.12`. Check the value and update the contract or implementation accordingly. |
|            | `environment` | The environment variable `LOG_LEVEL` does not match the expected value. Expected: `'INFO'`, Found: `'DEBUG'`. Check the value and update the contract or implementation accordingly. |
|            | `class`       | The class attribute `engine` in class `Extension` does not match the expected value. Expected: `'docker'`, Found: `'podman'`. Check the value and update the contract or implementation accordingly. |
| `invalid`  | `class`       | The argument `msg` of method `send` has an invalid value. Allowed values: `[str, None]`, Found: `42`. Update the value to one of the allowed options. |
