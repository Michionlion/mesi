"""Test the display module."""

from os.path import sep
from pathlib import Path
from typing import Tuple

import pytest

from mesi import display


def paths(one: str, two: str):
    return (Path(one), Path(two))


def normpath(one: str, two: str):
    return one.replace("/", sep), two.replace("/", sep)


@pytest.mark.parametrize(
    "input, expected",
    [
        (
            paths("test-1/hello.txt", "test-2/hello.txt"),
            normpath("test-1", "test-2"),
        ),
        (paths("test-1/json.txt", "test-1/jqsn.txt"), ("json.txt", "jqsn.txt")),
        (
            paths("test-1/json.txt", "test-2/jqsn.txt"),
            normpath("test-1/json.txt", "test-2/jqsn.txt"),
        ),
    ],
)
def test_get_distinct_file_names(input: Tuple[Path, Path], expected: Tuple[str, str]):
    assert display.get_distinct_file_names(input) == expected
