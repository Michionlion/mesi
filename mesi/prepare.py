"""Prepare user input for comparisons."""

from itertools import combinations
from pathlib import Path
from typing import List, Tuple


def all_possible_combinations(files: List[Path]) -> List[Tuple[Path, Path]]:
    """Generate all possible pair combinations of files.

    Args:
        files (List[Path]): A list of Paths to pair.

    Returns:
        List[Tuple[Path, Path]]: A list of the generated pairs.
    """
    return list(combinations(files, 2))
