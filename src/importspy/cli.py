"""
Command-line interface for ImportSpy module validation and execution.

This module exposes a CLI command `importspy` that enables users to load and validate
a Python module against a structural specification defined in a SpyModel file (e.g., YAML).

Key functionalities:
--------------------
- Dynamically imports a Python module from a given file path.
- Loads a SpyModel definition (e.g., from `spymodel.yml`).
- Validates the structure of the module against the defined SpyModel.
- Provides human-readable CLI feedback with color-coded messages.
- Supports configurable log verbosity via log level options.

Commands:
---------
- `importspy`: Validates the provided module file using a SpyModel definition.

Decorators:
-----------
- `handle_validation_error`: Wraps the CLI command to catch validation errors and 
  print meaningful output without raising exceptions.

Usage:
------
.. code-block:: bash

    python -m importspy.cli importspy ./examples/my_module.py --spymodel config/spymodel.yml --log-level DEBUG

Arguments:
----------
modulepath : str
    Path to the Python module to validate.

--spymodel / -s : str, optional
    Path to the SpyModel file (default: `spymodel.yml`).

--log-level / -l : str, optional
    Logging verbosity level. Accepts: DEBUG, INFO, WARNING, ERROR.

Notes:
------
- This CLI tool is intended for developers who want to verify structural
  compliance of their modules during development, CI, or pre-deployment checks.
- The SpyModel file should follow the expected schema defined by ImportSpy.
- Validation errors do not crash the CLI but are reported with colored feedback.

"""

import typer
import sys
import importlib.util
from typing import Optional
from types import ModuleType
from pathlib import Path
from importspy import Spy
from enum import Enum
import logging
import functools

def handle_validation_error(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
            typer.echo(typer.style("✅ Module is compliant with SpyModel!", fg=typer.colors.GREEN, bold=True))
        except ValueError as ve:
            typer.echo(typer.style("❌ Module is NOT compliant with SpyModel.", fg=typer.colors.RED, bold=True))
            typer.echo()
            typer.secho("Reason:", fg="magenta", bold=True)
            typer.echo(f"  {typer.style(str(ve), fg='yellow')}")
    return wrapper


class LogLevel(str, Enum):

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"

app = typer.Typer()

@app.command()
@handle_validation_error
def importspy(
        modulepath: Optional[str] = typer.Argument(str, help="Path to the Python module to load."),
        spymodel_path: Optional[str] = typer.Option(
            "spymodel.yml", "--spymodel", "-s", help="Path to the SpyModel YAML file."
        ),
        log_level: Optional[LogLevel] = typer.Option(
            None, "--log-level", "-l", help="Log level for output verbosity."
        )
        ) -> ModuleType:
    module_path = Path(modulepath).resolve()
    module_name = module_path.stem
    spec = importlib.util.spec_from_file_location(module_name, str(module_path))
    info_module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = info_module
    spec.loader.exec_module(info_module)
    Spy().importspy(
        filepath=spymodel_path,
        log_level= logging.getLevelNamesMapping()[log_level] if log_level else None,
        info_module=info_module
    )

def main():
    app()