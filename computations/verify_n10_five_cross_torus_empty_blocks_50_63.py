#!/usr/bin/env python3
"""Exact affine/torus closure of five-cross pair blocks 50 through 63."""

from __future__ import annotations

import importlib.util
from collections import Counter
from pathlib import Path


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def load_cache():
    path = Path(__file__).with_name(
        "verify_n10_five_cross_exact_matrix_transfer_cache.py"
    )
    spec = importlib.util.spec_from_file_location("matrix_cache", path)
    require(spec is not None and spec.loader is not None, "cannot load cache")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    cache = load_cache()
    palette = cache.load_palette()
    five = palette.load_five_frontier()
    four = five.load_four_closure()
    bounded = four.load_bounded_frontier()
    data = bounded.prepare()
    left_coordinates = tuple(
        coordinate for coordinate in data["coordinates"] if coordinate[1] == 8
    )
    right_coordinates = tuple(
        coordinate for coordinate in data["coordinates"] if coordinate[1] == 9
    )
    pair_survivors = five.universal_pair_survivors(
        data, left_coordinates, right_coordinates
    )
    require(len(pair_survivors) == 196, "pair-survivor count changed")
    expected_pairs = (
        ((1, 8, 1, 2), (7, 8, 0, 0)),
        ((1, 8, 1, 2), (7, 8, 1, 0)),
        ((1, 8, 1, 2), (7, 8, 2, 0)),
        ((2, 8, 0, 0), (2, 8, 0, 2)),
        ((2, 8, 0, 0), (2, 8, 1, 2)),
        ((2, 8, 0, 0), (2, 8, 2, 2)),
        ((2, 8, 0, 0), (3, 8, 1, 2)),
        ((2, 8, 0, 0), (4, 8, 1, 2)),
        ((2, 8, 0, 0), (5, 8, 1, 2)),
        ((2, 8, 0, 0), (6, 8, 0, 2)),
        ((2, 8, 0, 0), (6, 8, 1, 2)),
        ((2, 8, 0, 0), (6, 8, 2, 2)),
        ((2, 8, 0, 0), (7, 8, 0, 2)),
        ((2, 8, 0, 0), (7, 8, 1, 2)),
    )
    require(pair_survivors[49:63] == expected_pairs, "pair-block order changed")

    records = []
    frontiers = []
    for block in range(49, 63):
        record, affine_cases, torus_cases = cache.torus_pair_block(
            palette,
            five,
            four,
            bounded,
            data,
            pair_survivors[block],
            right_coordinates,
        )
        records.append(record)
        frontiers.append((len(affine_cases), len(torus_cases)))
    require(
        tuple(frontiers)
        == ((0, 0), (70, 0), (0, 0), (0, 0), (0, 0), (0, 0),
            (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0),
            (0, 0), (0, 0)),
        "affine/torus frontier changed",
    )

    empty_records = Counter(
        {
            (5, "excluded"): 25_758,
            (6, "excluded"): 24_804,
            (4, "excluded"): 8_262,
            (3, "excluded"): 816,
        }
    )
    small_affine_records = Counter(
        {
            (5, "excluded"): 25_740,
            (6, "excluded"): 24_752,
            (4, "excluded"): 8_262,
            (3, "excluded"): 816,
            (6, "affine"): 52,
            (5, "affine"): 18,
        }
    )
    same_vertex_records = Counter(
        {
            (6, "excluded"): 39_711,
            (4, "excluded"): 17_577,
            (2, "prior"): 2_268,
            (0, "prior"): 84,
        }
    )
    require(records[1] == small_affine_records, "affine block census changed")
    require(
        all(records[index] == same_vertex_records for index in (3, 4, 5)),
        "same-vertex census changed",
    )
    require(
        all(
            records[index] == empty_records
            for index in (0, 2, 6, 7, 8, 9, 10, 11, 12, 13)
        ),
        "affine-empty census changed",
    )

    audited_supports = 14 * 59_640
    prior_supports = 3 * 2_352
    closed_this_batch = audited_supports - prior_supports
    closed_cumulative = 2_917_656 + closed_this_batch
    remaining = 11_614_176 - closed_cumulative
    require(
        (audited_supports, prior_supports, closed_this_batch)
        == (834_960, 7_056, 827_904),
        "batch support arithmetic changed",
    )
    require(
        (closed_cumulative, remaining) == (3_745_560, 7_868_616),
        "cumulative frontier arithmetic changed",
    )

    print("N=10 five-cross pair blocks 50-63: exact PASS")
    print("complete pair blocks audited: 14; supports: 834960")
    print("prior zero/two-grade supports: 7056")
    print("new grade-3-to-6 supports closed: 827904")
    print("affine candidates: 70; torus candidates: 0")
    print("literal determinant/cache calls: 0")
    print("cumulative closed new grade-3-to-6 supports: 3745560")
    print("remaining unaudited grade-3-to-6 supports: 7868616")


if __name__ == "__main__":
    main()
