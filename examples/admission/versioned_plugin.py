"""Use a declared external dependency."""

from packaging.version import Version


def normalize(value: str) -> str:
    return str(Version(value))
