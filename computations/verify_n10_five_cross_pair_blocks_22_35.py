#!/usr/bin/env python3
"""Exact affine/torus/minor audit of five-cross pair blocks 22--35."""

from __future__ import annotations

import importlib.util
from collections import Counter
from pathlib import Path


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def load_palette():
    path = Path(__file__).with_name(
        "verify_n10_five_cross_affine_signature_palette.py"
    )
    spec = importlib.util.spec_from_file_location("signature_palette", path)
    require(spec is not None and spec.loader is not None, "cannot load palette")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    palette = load_palette()
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

    audits = tuple(
        palette.audit_pair_block(
            five,
            four,
            bounded,
            data,
            pair_survivors[index],
            right_coordinates,
        )
        for index in range(21, 35)
    )
    expected_pairs = (
        ((0, 8, 1, 2), (6, 8, 0, 0)),
        ((0, 8, 1, 2), (6, 8, 1, 0)),
        ((0, 8, 1, 2), (6, 8, 2, 0)),
        ((0, 8, 1, 2), (7, 8, 0, 0)),
        ((0, 8, 1, 2), (7, 8, 1, 0)),
        ((0, 8, 1, 2), (7, 8, 2, 0)),
        ((1, 8, 1, 0), (1, 8, 1, 2)),
        ((1, 8, 1, 0), (2, 8, 0, 2)),
        ((1, 8, 1, 0), (2, 8, 1, 2)),
        ((1, 8, 1, 0), (2, 8, 2, 2)),
        ((1, 8, 1, 0), (3, 8, 1, 2)),
        ((1, 8, 1, 0), (4, 8, 1, 2)),
        ((1, 8, 1, 0), (5, 8, 1, 2)),
        ((1, 8, 1, 0), (6, 8, 0, 2)),
    )
    require(pair_survivors[21:35] == expected_pairs, "pair-block order changed")
    require(
        tuple(len(audit["system_signatures"]) for audit in audits)
        == (324, 401, 265, 191, 221, 148, 251,
            325, 422, 382, 723, 304, 693, 283),
        "affine palette sizes changed",
    )
    require(
        tuple(
            (
                len(audit["affine_cases"]),
                len(audit["torus_cases"]),
                len(audit["exceptions"]),
            )
            for audit in audits
        )
        == (
            (0, 0, 0),
            (207, 28, 0),
            (0, 0, 0),
            (0, 0, 0),
            (207, 6, 0),
            (0, 0, 0),
            (70, 0, 0),
            (0, 0, 0),
            (70, 0, 0),
            (0, 0, 0),
            (207, 75, 58),
            (70, 27, 21),
            (207, 72, 29),
            (0, 0, 0),
        ),
        "block frontier census changed",
    )

    empty_records = Counter(
        {
            (5, "excluded"): 25_758,
            (6, "excluded"): 24_804,
            (4, "excluded"): 8_262,
            (3, "excluded"): 816,
        }
    )
    sparse_records = Counter(
        {
            (5, "excluded"): 25_704,
            (6, "excluded"): 24_651,
            (4, "excluded"): 8_262,
            (3, "excluded"): 816,
            (6, "affine"): 153,
            (5, "affine"): 54,
        }
    )
    same_vertex_records = Counter(
        {
            (6, "excluded"): 39_650,
            (4, "excluded"): 17_568,
            (2, "prior"): 2_268,
            (0, "prior"): 84,
            (6, "affine"): 61,
            (4, "affine"): 9,
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
    lower_affine_records = Counter(
        {
            (5, "excluded"): 25_758,
            (6, "excluded"): 24_804,
            (4, "excluded"): 8_208,
            (3, "excluded"): 800,
            (4, "affine"): 54,
            (3, "affine"): 16,
        }
    )
    require(
        all(audits[index]["records"] == empty_records
            for index in (0, 2, 3, 5, 7, 9, 13)),
        "affine-empty block census changed",
    )
    require(
        all(audits[index]["records"] == sparse_records
            for index in (1, 4, 10, 12)),
        "sparse block census changed",
    )
    require(
        audits[6]["records"] == same_vertex_records,
        "same-vertex block census changed",
    )
    require(
        audits[8]["records"] == small_affine_records,
        "small affine block census changed",
    )
    require(
        audits[11]["records"] == lower_affine_records,
        "lower affine block census changed",
    )

    global_monomials = sum(
        len(audit["determinants"]) - len(audit["exceptions"])
        for audit in audits
    )
    require(global_monomials == 100, "global monomial count changed")

    samples = {
        "ac+1": (1, 2, -1, 3, 5),
        "ad+1": (1, 2, 3, -1, 5),
        "ae+1": (1, 2, 3, 5, -1),
    }
    divisor_certificates = []
    divisor_census = Counter()
    for index in (10, 11, 12):
        audit = audits[index]
        special_samples = {}
        for case, determinant in audit["exceptions"]:
            divisors = palette.non_torus_factors(determinant[3]["base"])
            require(len(divisors) == 1, "a non-principal divisor appeared")
            divisor = next(iter(divisors))
            require(divisor in samples, "the principal divisor palette changed")
            divisor_census[divisor] += 1
            special_samples[case[0]] = {divisor: samples[divisor]}
        divisor_certificates.extend(
            palette.close_exceptional_divisors(
                five,
                bounded,
                data,
                audit["exceptions"],
                special_samples,
            )
        )
    require(
        divisor_census == Counter({"ae+1": 50, "ad+1": 47, "ac+1": 11}),
        "principal divisor census changed",
    )
    require(len(divisor_certificates) == 108, "divisor chart count changed")

    audited_supports = 14 * 59_640
    prior_supports = 2_352
    closed_this_batch = audited_supports - prior_supports
    require(
        (audited_supports, closed_this_batch) == (834_960, 832_608),
        "batch support arithmetic changed",
    )
    closed_cumulative = 1_250_088 + closed_this_batch
    remaining = 11_614_176 - closed_cumulative
    require(
        (closed_cumulative, remaining) == (2_082_696, 9_531_480),
        "cumulative frontier arithmetic changed",
    )
    require(
        pair_survivors[35] == ((1, 8, 1, 0), (6, 8, 1, 2)),
        "next pair block changed",
    )

    print("N=10 five-cross pair blocks 22-35: exact PASS")
    print("complete pair blocks audited: 14; supports: 834960")
    print("new grade-3-to-6 supports closed: 832608")
    print("affine candidates: 1038; torus candidates: 208")
    print("literal exclusions: 100 global monomials + 108 divisor supports")
    print("literal survivors: 0")
    print("cumulative closed new grade-3-to-6 supports: 2082696")
    print("remaining unaudited grade-3-to-6 supports: 9531480")


if __name__ == "__main__":
    main()
