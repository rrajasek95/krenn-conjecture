#!/usr/bin/env python3
"""Exact affine/torus closure of five-cross pair blocks 64 through 77."""

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
        ((2, 8, 0, 0), (7, 8, 2, 2)),
        ((2, 8, 0, 2), (2, 8, 1, 0)),
        ((2, 8, 0, 2), (2, 8, 2, 0)),
        ((2, 8, 0, 2), (3, 8, 1, 0)),
        ((2, 8, 0, 2), (4, 8, 1, 0)),
        ((2, 8, 0, 2), (5, 8, 1, 0)),
        ((2, 8, 0, 2), (6, 8, 0, 0)),
        ((2, 8, 0, 2), (6, 8, 1, 0)),
        ((2, 8, 0, 2), (6, 8, 2, 0)),
        ((2, 8, 0, 2), (7, 8, 0, 0)),
        ((2, 8, 0, 2), (7, 8, 1, 0)),
        ((2, 8, 0, 2), (7, 8, 2, 0)),
        ((2, 8, 1, 0), (2, 8, 1, 2)),
        ((2, 8, 1, 0), (2, 8, 2, 2)),
    )
    require(pair_survivors[63:77] == expected_pairs, "pair-block order changed")

    records = []
    frontiers = []
    for block in range(63, 77):
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
        == ((0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0),
            (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0),
            (70, 0), (0, 0)),
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
    same_vertex_records = Counter(
        {
            (6, "excluded"): 39_711,
            (4, "excluded"): 17_577,
            (2, "prior"): 2_268,
            (0, "prior"): 84,
        }
    )
    same_vertex_affine_records = Counter(
        {
            (6, "excluded"): 39_650,
            (4, "excluded"): 17_568,
            (2, "prior"): 2_268,
            (0, "prior"): 84,
            (6, "affine"): 61,
            (4, "affine"): 9,
        }
    )
    require(
        all(
            records[index] == empty_records
            for index in (0, 3, 4, 5, 6, 7, 8, 9, 10, 11)
        ),
        "affine-empty distinct-endpoint census changed",
    )
    require(
        all(records[index] == same_vertex_records for index in (1, 2, 13)),
        "same-vertex census changed",
    )
    require(
        records[12] == same_vertex_affine_records,
        "same-vertex affine census changed",
    )

    audited_supports = 14 * 59_640
    prior_supports = 4 * 2_352
    closed_this_batch = audited_supports - prior_supports
    closed_cumulative = 3_745_560 + closed_this_batch
    remaining = 11_614_176 - closed_cumulative
    require(
        (audited_supports, prior_supports, closed_this_batch)
        == (834_960, 9_408, 825_552),
        "batch support arithmetic changed",
    )
    require(
        (closed_cumulative, remaining) == (4_571_112, 7_043_064),
        "cumulative frontier arithmetic changed",
    )

    print("N=10 five-cross pair blocks 64-77: exact PASS")
    print("complete pair blocks audited: 14; supports: 834960")
    print("prior zero/two-grade supports: 9408")
    print("new grade-3-to-6 supports closed: 825552")
    print("affine candidates: 70; torus candidates: 0")
    print("literal determinant/cache calls: 0; new divisor types: 0")
    print("cumulative closed new grade-3-to-6 supports: 4571112")
    print("remaining unaudited grade-3-to-6 supports: 7043064")


if __name__ == "__main__":
    main()
