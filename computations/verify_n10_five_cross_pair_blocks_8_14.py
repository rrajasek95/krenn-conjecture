#!/usr/bin/env python3
"""Exact torus-minor audit of five-cross pair blocks 8 through 14."""

from __future__ import annotations

import importlib.util
from collections import Counter
from itertools import combinations
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
        for index in range(7, 14)
    )
    expected_pairs = (
        ((0, 8, 1, 0), (5, 8, 1, 2)),
        ((0, 8, 1, 0), (6, 8, 0, 2)),
        ((0, 8, 1, 0), (6, 8, 1, 2)),
        ((0, 8, 1, 0), (6, 8, 2, 2)),
        ((0, 8, 1, 0), (7, 8, 0, 2)),
        ((0, 8, 1, 0), (7, 8, 1, 2)),
        ((0, 8, 1, 0), (7, 8, 2, 2)),
    )
    require(
        pair_survivors[7:14] == expected_pairs,
        "pair-block order changed",
    )
    require(
        tuple(len(audit["system_signatures"]) for audit in audits)
        == (719, 265, 400, 294, 148, 215, 204),
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
            (612, 278, 5),
            (0, 0, 0),
            (207, 28, 0),
            (0, 0, 0),
            (0, 0, 0),
            (207, 6, 0),
            (0, 0, 0),
        ),
        "block frontier census changed",
    )
    rich_records = Counter(
        {
            (5, "excluded"): 25_484,
            (6, "excluded"): 24_600,
            (4, "excluded"): 8_144,
            (3, "excluded"): 800,
            (5, "affine"): 274,
            (6, "affine"): 204,
            (4, "affine"): 118,
            (3, "affine"): 16,
        }
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
    require(audits[0]["records"] == rich_records, "rich block census changed")
    require(
        all(audits[index]["records"] == empty_records for index in (1, 3, 4, 6)),
        "affine-empty block census changed",
    )
    require(
        audits[2]["records"] == sparse_records
        and audits[5]["records"] == sparse_records,
        "sparse block census changed",
    )

    for audit in audits[1:]:
        require(not audit["exceptions"], "a new generic minor exception appeared")
    global_monomials = sum(
        len(audit["determinants"]) - len(audit["exceptions"])
        for audit in audits
    )
    require(global_monomials == 307, "global monomial count changed")

    exceptional_supports = [
        case[0] for case, _determinant in audits[0]["exceptions"]
    ]
    require(len(exceptional_supports) == 5, "exceptional support count changed")
    special_samples = {
        exceptional_supports[0]: {
            "-d+e": (1, 2, 3, 1, 1),
            "d+e": (1, 2, 3, 1, -1),
        },
        exceptional_supports[1]: {
            "-d+e": (1, 2, 3, 1, 1),
            "d+e": (1, 2, 3, 1, -1),
        },
        exceptional_supports[2]: {
            "-c+e": (1, 2, 1, 3, 1),
            "c+e": (1, 2, 1, 3, -1),
        },
        exceptional_supports[3]: {
            "d+e": (1, 2, 3, 1, -1),
        },
        exceptional_supports[4]: {
            "-c+d": (1, 2, 1, 1, 3),
            "c+d": (1, 2, 1, -1, 3),
        },
    }
    divisor_certificates = palette.close_exceptional_divisors(
        five,
        bounded,
        data,
        audits[0]["exceptions"],
        special_samples,
    )
    require(len(divisor_certificates) == 9, "divisor chart count changed")

    next_pair = pair_survivors[14]
    require(
        next_pair == ((0, 8, 1, 2), (1, 8, 1, 0)),
        "next pair block changed",
    )
    affine_cache = {}
    scanned_novel = 0
    affine_seen = 0
    first_case = None
    first_record = None
    for right_triple in combinations(right_coordinates, 3):
        support = next_pair + right_triple
        grades = tuple(
            bounded.support_permanents(data, support, (bounded.Q(1),) * 5)
        )
        if len(grades) < 3:
            continue
        scanned_novel += 1
        if grades not in affine_cache:
            affine_cache[grades] = bounded.exact_affine_system(data, grades)
        system = affine_cache[grades]
        if not system[0]:
            continue
        affine_seen += 1
        case = (support, grades, system)
        saturation = five.torus_affine_saturation(
            four,
            bounded,
            data,
            (case,),
            ("a", "b", "c", "d", "e"),
        )
        if saturation[0]:
            first_case = case
            first_record = five.five_cell_determinants(
                bounded,
                data,
                support,
                tuple(map(bounded.Q, (1, 2, 3, 5, 7))),
            )
            break
    expected_support = (
        (0, 8, 1, 2),
        (1, 8, 1, 0),
        (0, 9, 0, 0),
        (3, 9, 1, 2),
        (4, 9, 1, 0),
    )
    require(
        (scanned_novel, affine_seen) == (1712, 2)
        and first_case is not None
        and first_case[0] == expected_support,
        "next-block prefix changed",
    )
    require(
        first_case[1] == (338, 345, 3, 743, 750)
        and first_case[2]
        == (
            True,
            (4,),
            ((bounded.Q(0), bounded.Q(0), bounded.Q(0), bounded.Q(0),
              bounded.Q(1), bounded.Q(-1)),),
            24,
        ),
        "next-block exact affine system changed",
    )
    expressions = five.permanent_expressions(
        bounded,
        data,
        first_case[0],
        first_case[1],
        ("a", "b", "c", "d", "e"),
    )
    require(
        expressions == ("a*d", "a*e", "b*c", "b*d", "b*e"),
        "next-block permanent map changed",
    )
    expected_minor = (("-1", 1), ("a", 9), ("b", 3), ("d", 12))
    require(
        first_record is not None
        and first_record[3]["base"] == expected_minor
        and first_record[3]["aug0"] == expected_minor,
        "next-block determinant changed",
    )

    closed_in_complete_blocks = 14 * 59_640 - 2_352
    require(closed_in_complete_blocks == 832_608, "closed block count changed")
    remaining = 11_614_176 - closed_in_complete_blocks - scanned_novel
    require(remaining == 10_779_856, "remaining frontier count changed")
    print("N=10 five-cross pair blocks 8-14: exact PASS")
    print("complete pair blocks audited: 7; supports: 417480")
    print("affine candidates: 1026; torus candidates: 312")
    print("literal exclusions: 307 global monomials + 5 divisor supports")
    print("exceptional divisor charts: 9; literal survivors: 0")
    print("cumulative closed new grade-3-to-6 supports: 832608")
    print("next block prefix: 1712 new supports closed")
    print("first torus case: be=1; base=aug0=-a^9*b^3*d^12")
    print("remaining unaudited grade-3-to-6 supports: 10779856")


if __name__ == "__main__":
    main()
