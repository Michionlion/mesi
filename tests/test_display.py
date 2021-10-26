"""Test the display module."""

from pathlib import Path
from typing import Tuple

import pytest

from mesi import display


def path_tuple(one: str, two: str):
    return (Path(one), Path(two))


@pytest.mark.parametrize(
    "input, expected",
    [
        (
            path_tuple("test-1/hello.txt", "test-2/hello.txt"),
            ("test-1", "test-2"),
        ),
        (path_tuple("test-1/json.txt", "test-1/jqsn.txt"), ("json.txt", "jqsn.txt")),
        (
            path_tuple("test-1/json.txt", "test-2/jqsn.txt"),
            ("test-1/json.txt", "test-2/jqsn.txt"),
        ),
    ],
)
def test_get_distinct_file_names(input: Tuple[Path, Path], expected: Tuple[str, str]):
    assert display.get_distinct_file_names(input) == expected
