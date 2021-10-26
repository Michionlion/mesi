"""Utility functions dealing with paths."""

from os.path import sep
from pathlib import Path
from typing import Tuple


def paths(one: str, two: str) -> Tuple[Path, Path]:
    """Convert (str, str) to (Path, Path)."""
    return (Path(one), Path(two))


def normpath(path: str) -> str:
    """Normalize path str to use os.path.sep."""
    return path.replace("/", sep)


def normpaths(one: str, two: str) -> Tuple[str, str]:
    """Normalize (str, str) to use os.path.sep."""
    return normpath(one), normpath(two)
