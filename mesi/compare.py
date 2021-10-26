"""Calculate distances between file contents."""

import re
from pathlib import Path
from typing import Dict, List, Tuple

import polyleven
import textdistance

from mesi import display

WHITESPACE = re.compile(r"\s+")
DISTANCE_FUNCTIONS = {
    "hamming": textdistance.hamming.distance,
    "mlipns": textdistance.mlipns.distance,
    "levenshtein": polyleven.levenshtein,
    "damerau-levenshtein": textdistance.damerau_levenshtein.distance,
    "jaro": textdistance.jaro.distance,
    "jaro-winkler": textdistance.jaro_winkler.distance,
    "strcmp95": textdistance.strcmp95.distance,
    "needleman-wunsch": textdistance.needleman_wunsch.distance,
    "gotoh": textdistance.gotoh.distance,
    "smith-waterman": textdistance.smith_waterman.distance,
    "jaccard": textdistance.jaccard.distance,
    "sorensen-dice": textdistance.sorensen_dice.distance,
    "tversky": textdistance.tversky.distance,
    "overlap": textdistance.overlap.distance,
    "tanimoto": textdistance.tanimoto.distance,
    "cosine": textdistance.cosine.distance,
    "monge-elkan": textdistance.monge_elkan.distance,
    "bag": textdistance.bag.distance,
    "longest-common-subsequence": textdistance.lcsseq.distance,
    "longest-common-substring": textdistance.lcsstr.distance,
    "ratcliff-obershelp": textdistance.ratcliff_obershelp.distance,
    "arithmetic-coding": textdistance.arith_ncd.distance,
    "rle": textdistance.rle_ncd.distance,
    "bwt-rle": textdistance.bwtrle_ncd.distance,
    "square-root": textdistance.sqrt_ncd.distance,
    "entropy": textdistance.entropy_ncd.distance,
    "bz2": textdistance.bz2_ncd.distance,
    "lzma": textdistance.lzma_ncd.distance,
    "zlib": textdistance.zlib_ncd.distance,
    "mra": textdistance.mra.distance,
    "editex": textdistance.editex.distance,
    "prefix": textdistance.prefix.distance,
    "postfix": textdistance.postfix.distance,
    "length": textdistance.length.distance,
    "identity": textdistance.identity.distance,
    "matrix": textdistance.matrix.distance,
}


def get_contents(
    pair: Tuple[Path, Path], remove_whitespace: bool = False
) -> Tuple[str, str]:
    """Get the contents.

    Args:
        pair (Tuple[Path, Path]): The pair of Paths to get the contents from.
        remove_whitespace (bool): Whether to remove whitespace from contents.

    Returns:
        Tuple[str, str]: The contents of the given Paths
    """
    first = pair[0].read_text()
    second = pair[1].read_text()
    if remove_whitespace:
        first = WHITESPACE.sub("", first)
        second = WHITESPACE.sub("", second)
    return first, second


def calculate_distances(
    combinations: List[Tuple[Path, Path]], algorithm: str, ignore_whitespace: bool
) -> Dict[Tuple[Path, Path], float]:
    """Calculate distances.

    Args:
        combinations (Iterable[Tuple[Path, Path]]): The combinations to calculate distance for.
        algorithm (str): The algorithm to use to calculate distance.

    Raises:
        ValueError: If the algorithm given is not a valid distance algorithm

    Returns:
        Dict[Tuple[Path, Path], float]: Dict mapping combination to calculated distance
    """
    distance_algorithm = DISTANCE_FUNCTIONS.get(algorithm)
    if distance_algorithm is None:
        raise ValueError(f"{algorithm} is not a valid distance algorithm")

    distances = dict()
    for pair in display.comparison_progressbar(combinations):
        distances[pair] = distance_algorithm(*get_contents(pair, ignore_whitespace))
    return distances
