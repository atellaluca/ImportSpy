"""
Command-line interface (CLI) for validating Python modules against ImportSpy contracts.

This module defines the `importspy` CLI command, enabling local and automated validation
of a Python file against a YAML-based SpyModel contract. It is designed for use in
CI/CD pipelines, plugin systems, or developer workflows.

Features:
- Loads and executes the specified Python module.
- Parses the YAML contract file describing expected structure and runtime conditions.
- Validates that the module complies with the declared interface and environment.
- Provides user-friendly CLI feedback, including optional logging.

Use cases:
- Enforcing structure of external plugins before loading.
- Automating validation in GitHub Actions or other CI tools.
- Assuring consistency in modular libraries or educational tools.

Example:
    importspy ./examples/my_plugin.py -s ./contracts/expected.yml --log-level DEBUG

Note:
    Validation is powered by the core `Spy` class.
    Validation errors are caught and displayed with enhanced CLI formatting.
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
    Decorator that formats validation errors for CLI output.

    Intercepts `ValueError` raised by the `Spy.importspy()` call and presents
    the error reason in a readable, styled terminal message.

    Used to wrap the main `importspy()` CLI command.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
            typer.echo(typer.style("Module is compliant with the import contract.", fg=typer.colors.GREEN, bold=True))
        except ValueError as ve:
            typer.echo(typer.style("Module is NOT compliant with the import contract.", fg=typer.colors.RED, bold=True))
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
    modulepath: Optional[str] = typer.Argument(
        str,
        help="Path to the Python module to load and validate."
    ),
    spymodel_path: Optional[str] = typer.Option(
        "spymodel.yml",
        "--spymodel",
        "-s",
        help="Path to the import contract file (.yml)."
    ),
    log_level: Optional[LogLevel] = typer.Option(
        None,
        "--log-level",
        "-l",
        help="Log level for output verbosity."
    )
) -> ModuleType:
    """
    Validates a Python module against a YAML-defined SpyModel contract.

    Args:
        version (bool, optional): Show ImportSpy version and exit.
        modulepath (str): Path to the Python module to validate.
        spymodel_path (str, optional): Path to the YAML contract file. Defaults to `spymodel.yml`.
        log_level (LogLevel, optional): Set logging verbosity (DEBUG, INFO, WARNING, ERROR).

    Returns:
        ModuleType: The validated Python module (if compliant).

    Raises:
        ValueError: If the module does not conform to the contract.
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
    Displays the current version of ImportSpy and exits the process.

    Args:
        value (bool): If True, prints the version and exits immediately.
    """
    if value:
        typer.secho(f"ImportSpy v{__version__}", fg="cyan", bold=True)
        raise typer.Exit()

def main():
    """
    CLI entry point.

    Executes the `importspy` Typer app, allowing CLI usage like:

        $ importspy my_module.py -s my_contract.yml
    """
    app()
