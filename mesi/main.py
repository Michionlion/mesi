"""Main CLI entrypoint."""

from pathlib import Path
from typing import List

import typer

mesi_cli = typer.Typer(add_completion=False)


@mesi_cli.command()
def main(
    files: List[Path] = typer.Argument(..., help="Files to compare"),
):
    """Calculate the similarity between all possible pairs among the given files."""
    pass
