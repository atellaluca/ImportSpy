# Installation

ImportSpy requires **Python 3.10 or newer**. Use a virtual environment for a local
project:

```bash
python -m venv .venv
# Activate .venv using the command for your shell.
python -m pip install importspy
importspy --version
importspy --help
```

The package includes the Python admission API and the `init`/`check` CLI.
Static admission is local and offline. Install your project's dependencies in the
same environment so distribution metadata can be resolved.

To upgrade:

```bash
python -m pip install --upgrade importspy
```

For development from a checkout, follow [CONTRIBUTING.md](https://github.com/atellaluca/ImportSpy/blob/main/CONTRIBUTING.md).
The repository's release metadata and CI matrix define supported interpreter
versions. A contract accepting an interpreter name does not establish that the
ImportSpy package or its dependencies support that interpreter.

Continue with the [quickstart](quickstart.md), or read the
[migration guide](../migration-0.5.md) when upgrading from 0.4.
