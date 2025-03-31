"""
Command-line interface for ImportSpy import contract validation.

This module defines the CLI entry point `importspy`, which enables developers and CI/CD pipelines
to validate Python modules against a declared import contract written in YAML format.

Overview:
---------
The CLI allows structural and runtime compliance checks through:
- Dynamic import of a Python module from file.
- Parsing of the import contract from a `.yml` file.
- Validation of the module’s structure and metadata.
- Clear CLI feedback with styled messages.
- Optional log verbosity control for debugging purposes.

Main Command:
-------------
- `importspy`: Validates a Python module against an import contract definition.

Decorators:
-----------
- `handle_validation_error`: Intercepts and formats validation errors
  to improve user experience from the terminal.

Usage Examples:
---------------
Basic validation:

.. code-block:: bash

    importspy ./examples/my_module.py

With contract and log level:

.. code-block:: bash

    importspy ./my_module.py --spymodel contracts/example.yml --log-level DEBUG

Options:
--------
--spymodel / -s : str
    Path to the YAML file containing the import contract. Default: `spymodel.yml`.

--log-level / -l : str
    Log verbosity. Accepts: DEBUG, INFO, WARNING, ERROR.

--version / -v
    Show ImportSpy’s current version.

Notes:
------
- Validation is handled by the `Spy` core class.
- This command is ideal for local development, CI enforcement, or release pipelines.
- Validation issues are surfaced through color-coded output, not raw exceptions.
"""

import typer
import sys
import importlib.util
from typing import Optional
from types import ModuleType
from pathlib import Path
from importspy import (
    Spy,
    __version__
)
from enum import Enum
import logging
import functools

def handle_validation_error(func):
    """
    Intercepts validation errors and formats them for CLI output.

    Provides color-coded feedback based on validation result.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
            typer.echo(typer.style("✅ Module is compliant with the import contract!", fg=typer.colors.GREEN, bold=True))
        except ValueError as ve:
            typer.echo(typer.style("❌ Module is NOT compliant with the import contract.", fg=typer.colors.RED, bold=True))
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
        version: Optional[bool] = typer.Option(
            None,
            "--version",
            "-v",
            callback=lambda value: show_version(value),
            is_eager=True,
            help="Show the version and exit."
        ),
        modulepath: Optional[str] = typer.Argument(str, help="Path to the Python module to load and validate."),
        spymodel_path: Optional[str] = typer.Option(
            "spymodel.yml", "--spymodel", "-s", help="Path to the import contract file (.yml)."
        ),
        log_level: Optional[LogLevel] = typer.Option(
            None, "--log-level", "-l", help="Log level for output verbosity."
        )
) -> ModuleType:
    """
    CLI command to validate a Python module against a YAML-defined import contract.
    """
    module_path = Path(modulepath).resolve()
    module_name = module_path.stem
    spec = importlib.util.spec_from_file_location(module_name, str(module_path))
    info_module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = info_module
    spec.loader.exec_module(info_module)

    Spy().importspy(
        filepath=spymodel_path,
        log_level=logging.getLevelNamesMapping()[log_level] if log_level else None,
        info_module=info_module
    )

def show_version(value: bool):
    """
    Displays the current ImportSpy version and exits.
    """
    if value:
        typer.secho(f"ImportSpy v{__version__}", fg="cyan", bold=True)
        raise typer.Exit()

def main():
    """
    Entry point for CLI execution.
    """
    app()
