"""Display or parse data objects to strs."""

import os
from pathlib import Path
from typing import Dict, Iterable, List, Tuple, TypeVar, Union

import importlib_metadata
from tabulate import TableFormat, tabulate
from tqdm import tqdm
from typer import colors, format_filename, secho, style, unstyle

SPACER = "', '"

T = TypeVar("T")


def get_file_name(file: Path) -> str:
    """Get a full file path.

    Args:
        file (Path): A Path to get the representation from.

    Returns:
        str: The full file path.
    """
    return format_filename(file)


def get_file_names(files: Iterable[Path]) -> List[str]:
    """Get a list of full file paths.

    Args:
        files (Iterable[Path]): A list of Paths to get the representations from.

    Returns:
        List[str]: The list of full file paths.
    """
    return [get_file_name(file) for file in files]


def get_file_list_str(files: Iterable[Path]) -> str:
    """Get a representation of a list of Paths.

    Args:
        files (Iterable[Path]): A list of Paths to represent.

    Returns:
        str: The calculated representation.
    """
    return f"'{SPACER.join(get_file_names(files))}'"


def get_distinct_file_names(pair: Tuple[Path, Path]) -> Tuple[str, str]:
    """Strip any common suffix and prefix.

    Args:
        pair (Tuple[Path, Path]): A tuple of two paths to strip.

    Returns:
        Tuple[str, str]: A tuple of two full file paths with common files or folders removed.
    """
    first = get_file_name(pair[0])
    second = get_file_name(pair[1])
    prefix = os.path.commonprefix((first, second))
    suffix = os.path.commonprefix((first[::-1], second[::-1]))[::-1]
    last_prefix_sep = prefix.rfind(os.path.sep)
    first_suffix_sep = suffix.find(os.path.sep)
    return (
        first[
            last_prefix_sep + 1 : -(len(suffix) - first_suffix_sep)
            if first_suffix_sep >= 0
            else len(first)
        ],
        second[
            last_prefix_sep + 1 : -(len(suffix) - first_suffix_sep)
            if first_suffix_sep >= 0
            else len(second)
        ],
    )


def comparison_progressbar(lst: List, **kwargs):
    """Show a progress bar for comparisons, yielding each item.

    Args:
        lst (List): A list of items to process.
    """
    return tqdm(lst, total=len(lst), unit="cmp", colour="blue", leave=False, **kwargs)


def print_divider(title=""):
    """Print a simple divider with an optional title."""
    title = f" {title} " if title else ""
    print(f"\n======{title}======\n")


def print_average_distance(
    distances: Dict[Tuple[Path, Path], float], distance_threshold: float
):
    """Print the average of the distances.

    Args:
        distances (Dict[Tuple[Path, Path], float]): A dictionary of comparisons to distances.
        distance_threshold (float): The threshold below which to count values.
    """
    values = list(filter(lambda x: x <= distance_threshold, distances.values()))
    avg = round(sum(values) / len(values), 2)

    print(f"> Average distance: {avg}")


def print_distance_distribution(
    distances: Dict[Tuple[Path, Path], float], distance_threshold: float
):
    """Print the distribution of the distances.

    Args:
        distances (Dict[Tuple[Path, Path], float]): A dictionary of comparisons to distances.
        distance_threshold (float): The threshold below which to count values.
    """
    print("> Distribution display is not yet supported")


def print_distances(
    distances: Dict[Tuple[Path, Path], float],
    distance_threshold: float,
    tablefmt: Union[TableFormat, str] = "pipe",
    full_paths=False,
):
    """Print comparisons and the associated distances in a table.

    Args:
        distances (Dict[Tuple[Path, Path], float]): A dictionary of comparisons to distances.
        distance_threshold (float): The threshold below which to display values.
        tablefmt (Union[TableFormat, str], optional): The format of the table to print. Defaults to "pipe".
        full_file_names (bool, optional): Whether to use the full file name or only the differing paths.
    """
    file_name_function = get_file_names if full_paths else get_distinct_file_names
    path_header = "Path" if full_paths else "Distinct Path"
    rows = [
        (
            *file_name_function(pair),
            style(distances[pair], bold=True),
        )
        for pair in distances
    ]
    filtered_rows = filter(
        lambda row: float(unstyle(row[-1])) <= distance_threshold, rows
    )
    if filtered_rows:
        rows = list(filtered_rows)
    else:
        secho(
            f"No distances below threshold of {distance_threshold}, showing all distances",
            fg=colors.RED,
        )
    rows.sort(key=lambda row: -float(unstyle(row[-1])))
    table = tabulate(
        rows,
        headers=[path_header, path_header, "Distance"],
        tablefmt=tablefmt,
        colalign=("left", "left", "decimal"),
    )
    secho(table)


def print_version():
    """Print version."""
    secho(
        f"{style('mesi', bold=True)} (version {style(importlib_metadata.version('mesi'), colors.CYAN)})"
    )


def print_error(err: Union[Exception, str]):
    """Print a styled error.

    Args:
        err (Union[Exception, str]): An error (either an Exception or just a description).
    """
    secho(
        f"Error: {style(str(err), fg=colors.RED, bold=False, italic=True)}",
        fg=colors.BRIGHT_RED,
        bold=True,
    )


def print_error_invalid_given(invalid: Iterable[Path]):
    """Print an error for if an invalid Path was provided by the user.

    Args:
        invalid (Iterable[Path]): A list of the invalid Paths provided.
    """
    print_error(
        f"Invalid files {get_file_list_str(invalid)} given (could be directories, or not exist); use --ignore-invalid to ignore!",
    )


def print_error_not_enough_valid(real_files: Iterable[Path]):
    """Print an error for if not enough valid Paths were provided by the user.

    Args:
        real_files (Iterable[Path]): A list of the Paths provided.
    """
    print_error(
        f"Given file list {get_file_list_str(real_files)} does not contain enough valid files to compare!",
    )


def print_error_not_comparable(files: Iterable[Path]):
    """Print an error for if not enough Paths were provided by the user.

    Args:
        files (Iterable[Path]): A list of the valid Paths provided.
    """
    print_error(
        f"Given file list {get_file_list_str(files)} is not comparable!",
    )
