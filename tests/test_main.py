"""Test the main module."""

import os
import shutil
from pathlib import Path
from typing import Callable, List, Tuple

import pytest
from typer.testing import CliRunner

from mesi import main

runner = CliRunner()


class TmpFileSetup:
    def __init__(self, parent: Path):
        self.parent = parent

    def __enter__(self) -> List[Path]:
        self.cwd = os.getcwd()
        os.chdir(self.parent)
        tmpfiles = []
        for (path, contents) in self.files:
            if path.parent:
                path.parent.mkdir(parents=True, exist_ok=True)
            path.touch()
            path.write_text(contents)
            tmpfiles.append(path)
        return tmpfiles

    def __exit__(self, *args):
        os.chdir(self.cwd)
        shutil.rmtree(self.parent)

    def __call__(self, files: List[Tuple[Path, str]]) -> "TmpFileSetup":
        self.files = files
        return self


@pytest.fixture
def setup_env(tmp_path: Path) -> TmpFileSetup:
    return TmpFileSetup(tmp_path)


@pytest.mark.parametrize(
    "files, input, expected",
    [
        (
            [
                (Path("test-1/hello.txt"), "hello from test-1"),
                (Path("test-2/hello.txt"), "hi from test-2"),
            ],
            ["test-1/hello.txt", "test-2/hello.txt"],
            "| test-1          | test-2          |          5 |",
        ),
        (
            [
                (Path("test-1/json.txt"), "this is a test"),
                (Path("test-2/jqsn.txt"), "this is a test"),
            ],
            ["test-1/json.txt", "test-2/jqsn.txt"],
            "| test-1/json.txt | test-2/jqsn.txt |          0 |",
        ),
    ],
)
def test_main(
    setup_env: Callable[..., TmpFileSetup],
    files: List[Tuple[Path, str]],
    input: List[str],
    expected: str,
):
    """Check that main.mesi_cli does not raise with valid input."""
    with setup_env(files):
        result = runner.invoke(main.mesi_cli, input)
        print(result.output)
        assert expected in result.output
        assert result.exit_code == 0
