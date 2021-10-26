"""Test the display module."""

from pathlib import Path
from typing import Tuple

import pytest
from helpers import pathutil

from mesi import display


@pytest.mark.parametrize(
    "input, expected",
    [
        (
            pathutil.paths("test-1/hello.txt", "test-2/hello.txt"),
            pathutil.normpaths("test-1", "test-2"),
        ),
        (
            pathutil.paths("test-1/json.txt", "test-1/jqsn.txt"),
            pathutil.normpaths("json.txt", "jqsn.txt"),
        ),
        (
            pathutil.paths("test-1/json.txt", "test-2/jqsn.txt"),
            pathutil.normpaths("test-1/json.txt", "test-2/jqsn.txt"),
        ),
    ],
)
def test_get_distinct_file_names(input: Tuple[Path, Path], expected: Tuple[str, str]):
    assert display.get_distinct_file_names(input) == expected
