"""Installed package metadata is the version authority; source checkout fallback."""

from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

try:
    __version__ = version("importspy")
except PackageNotFoundError:
    # A source tree may be used without installation. Do not duplicate the version.
    import re

    metadata = Path(__file__).resolve().parents[2] / "pyproject.toml"
    match = (
        re.search(r'^version\s*=\s*"([^"]+)"', metadata.read_text(), re.MULTILINE)
        if metadata.is_file()
        else None
    )
    __version__ = match.group(1) if match else "0+uninstalled"
