"""Main CLI entrypoint."""

from math import inf
from pathlib import Path
from typing import List, Optional

import typer

from mesi import compare, display, prepare, verify

mesi_cli = typer.Typer(add_completion=False)


def version_callback(execute: bool):
    """Display version and exit if execute is True."""
    if execute:
        display.print_version()
        raise typer.Exit()


@mesi_cli.command()
def main(
    files: List[Path] = typer.Argument(..., help="Files to compare"),
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        help="Show version and exit",
        callback=version_callback,
        is_eager=True,
    ),
    threshold: float = typer.Option(
        inf, help="Distances below this threshold will be shown", metavar="NUMBER"
    ),
    table_format: str = typer.Option(
        "pipe",
        help="Format to use for results table displayed with tabulate",
        metavar="FORMAT",
    ),
    ignore_whitespace: bool = typer.Option(
        False, help="Ignore whitespace in compared files"
    ),
    ignore_invalid: bool = typer.Option(
        False, help="Allow comparison to continue if some files do not exist"
    ),
    full_paths: bool = typer.Option(
        False, help="Print full paths for files instead of only distinct elements"
    ),
    algorithm: str = typer.Option(
        "levenshtein",
        help=f"String distance algorithm to use  [{', '.join(compare.DISTANCE_FUNCTIONS.keys())}]",
        metavar="ALGORITHM",
    ),
    average: bool = typer.Option(
        False, help="Display the average of the computed distances"
    ),
    distribution: bool = typer.Option(
        False, help="Display the distribution of the computed distances"
    ),
):
    """Calculate the similarity between all possible pairs among the given files.

    For examples and more details on algorithms, table formats, and other options
    visit: https://pypi.org/project/mesi.
    """
    comparable_files, invalid = verify.filter_non_files(files)
    if invalid and not ignore_invalid:
        display.print_error_invalid_given(invalid)
        raise typer.Exit(2)
    if not verify.is_comparable(comparable_files):
        if invalid:
            display.print_error_not_enough_valid(files)
            raise typer.Exit(3)
        else:
            display.print_error_not_comparable(comparable_files)
            raise typer.Exit(4)

    try:
        combinations = prepare.all_possible_combinations(comparable_files)
        distances = compare.calculate_distances(
            combinations, algorithm, ignore_whitespace
        )
        display.print_distances(distances, threshold, table_format, full_paths)

        if average or distribution:
            display.print_divider("Statistics")

        if average:
            display.print_average_distance(distances, threshold)

        if distribution:
            display.print_distance_distribution(distances, threshold)
    except ValueError as err:
        display.print_error(err)
        raise typer.Exit(1)
