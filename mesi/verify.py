"""Verify user input for comparisons."""

from pathlib import Path
from typing import Iterable, List, Sized, Tuple


def is_valid_file(file: Path) -> bool:
    """Check that a Path is valid.

    Args:
        file (Path): A Path to check.
    Returns:
        True if the Path is a valid file and can be compared.
    """
    return file.is_file()


def filter_non_files(files: Iterable[Path]) -> Tuple[List[Path], List[Path]]:
    """Filter files that do not exist from a given list.

    Args:
        files (Iterable[Path]): A list of Paths to check for existence.
    Returns:
        A tuple containing list of Paths without directories or non-existent files, and a list of the Paths removed.
    """
    validated = [file for file in files if is_valid_file(file)]
    rejected = [file for file in files if not is_valid_file(file)]
    return validated, rejected


def is_comparable(files: Sized) -> bool:
    """Check if a list contains enough files to run a comparison with.

    Args:
        files (Sized): A list of files to check.
    """
    return len(files) > 1
