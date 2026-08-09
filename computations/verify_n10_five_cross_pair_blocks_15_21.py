#!/usr/bin/env python3
"""Exact torus-minor audit of five-cross pair blocks 15 through 21.

The one new feature in this batch is a three-component generic divisor.
Two codimension-two charts close its only torus intersections, so no literal
fixed-old cut-2 survivor remains in these seven blocks.
"""

from __future__ import annotations

import importlib.util
import subprocess
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


SAMPLES = {
    "be+1": (2, 1, 3, 5, -1),
    "bd+1": (2, 1, 3, -1, 5),
    "bd-1": (2, 1, 3, 1, 5),
    "bc+1": (2, 1, -1, 3, 5),
    "d+e": (2, 3, 5, 1, -1),
    "-d+e": (2, 3, 5, 1, 1),
    "c+d": (2, 3, 1, -1, 5),
    "c-d": (2, 3, 1, 1, 5),
    "-c+d": (2, 3, 1, 1, 5),
    "c+e": (2, 3, 1, 5, -1),
    "-c+e": (2, 3, 1, 5, 1),
}


def direct_divisor_samples(palette, exceptions):
    samples = {}
    for case, determinant in exceptions:
        divisors = palette.non_torus_factors(determinant[3]["base"])
        require(divisors <= set(SAMPLES), "unknown direct divisor appeared")
        samples[case[0]] = {divisor: SAMPLES[divisor] for divisor in divisors}
    return samples


def no_torus_zero(palette, equations, determinant_factors):
    determinant = palette.factor_expression(determinant_factors)
    generators = [f"({equation})" for equation in equations]
    generators.extend((f"({determinant})", "t*a*b*c*d*e-1"))
    lines = [
        "ring r=0,(a,b,c,d,e,t),dp;",
        f"ideal I={','.join(generators)};",
        "ideal G=std(I);",
        "reduce(1,G);",
    ]
    process = subprocess.run(
        ["Singular", "-q"],
        input="\n".join(lines),
        text=True,
        capture_output=True,
        check=True,
    )
    return process.stdout.strip() == "0"


def direct_cover_certificates(
    palette, five, bounded, data, exceptions, excluded_support
):
    """Close divisor supports whose first special charts cover each divisor."""
    certificates = []
    for case, determinant in exceptions:
        support = case[0]
        if support == excluded_support:
            continue
        generic_divisors = palette.non_torus_factors(
            determinant[3]["base"]
        )
        require(generic_divisors, "a monomial entered the divisor cover")
        require(
            all(
                palette.non_torus_factors(factors) == generic_divisors
                for name, factors in determinant[3].items()
                if name.startswith("aug")
            ),
            "generic base/augmented divisor supports separated",
        )
        for divisor in sorted(generic_divisors):
            special = five.five_cell_determinants(
                bounded,
                data,
                support,
                tuple(map(bounded.Q, SAMPLES[divisor])),
            )
            base_ok = palette.divisor_has_no_torus_zero(
                divisor, special[3]["base"]
            )
            augmented = tuple(
                name
                for name, factors in special[3].items()
                if name.startswith("aug")
                and palette.divisor_has_no_torus_zero(divisor, factors)
            )
            require(base_ok and augmented, "a direct divisor chart did not close")
            certificates.append((support, divisor, augmented[0]))
    return tuple(certificates)


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
        for index in range(14, 21)
    )
    expected_pairs = (
        ((0, 8, 1, 2), (1, 8, 1, 0)),
        ((0, 8, 1, 2), (2, 8, 0, 0)),
        ((0, 8, 1, 2), (2, 8, 1, 0)),
        ((0, 8, 1, 2), (2, 8, 2, 0)),
        ((0, 8, 1, 2), (3, 8, 1, 0)),
        ((0, 8, 1, 2), (4, 8, 1, 0)),
        ((0, 8, 1, 2), (5, 8, 1, 0)),
    )
    require(pair_survivors[14:21] == expected_pairs, "pair-block order changed")
    require(
        tuple(len(audit["system_signatures"]) for audit in audits)
        == (647, 298, 349, 295, 523, 541, 719),
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
            (207, 78, 35),
            (0, 0, 0),
            (207, 58, 0),
            (0, 0, 0),
            (612, 287, 8),
            (207, 78, 78),
            (612, 278, 5),
        ),
        "block frontier census changed",
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
    empty_records = Counter(
        {
            (5, "excluded"): 25_758,
            (6, "excluded"): 24_804,
            (4, "excluded"): 8_262,
            (3, "excluded"): 816,
        }
    )
    mixed_records = Counter(
        {
            (5, "excluded"): 25_653,
            (6, "excluded"): 24_804,
            (4, "excluded"): 8_176,
            (3, "excluded"): 800,
            (5, "affine"): 105,
            (4, "affine"): 86,
            (3, "affine"): 16,
        }
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
    require(
        audits[0]["records"] == audits[5]["records"] == sparse_records,
        "sparse block census changed",
    )
    require(
        audits[1]["records"] == audits[3]["records"] == empty_records,
        "affine-empty block census changed",
    )
    require(audits[2]["records"] == mixed_records, "mixed block census changed")
    require(
        audits[4]["records"] == audits[6]["records"] == rich_records,
        "rich block census changed",
    )

    global_monomials = sum(
        len(audit["determinants"]) - len(audit["exceptions"])
        for audit in audits
    )
    require(global_monomials == 653, "global monomial count changed")

    ordinary_exception_indices = (0, 4, 6)
    ordinary_certificates = []
    for index in ordinary_exception_indices:
        audit = audits[index]
        ordinary_certificates.extend(
            palette.close_exceptional_divisors(
                five,
                bounded,
                data,
                audit["exceptions"],
                direct_divisor_samples(palette, audit["exceptions"]),
            )
        )
    require(len(ordinary_certificates) == 53, "ordinary divisor charts changed")

    triple_support = (
        (0, 8, 1, 2),
        (4, 8, 1, 0),
        (1, 9, 1, 0),
        (3, 9, 1, 2),
        (4, 9, 0, 2),
    )
    middle_exceptions = audits[5]["exceptions"]
    divisor_census = Counter(
        tuple(sorted(palette.non_torus_factors(det[3]["base"])))
        for _case, det in middle_exceptions
    )
    require(
        divisor_census
        == Counter(
            {
                ("bc+1",): 59,
                ("bd+1",): 15,
                ("bd+1", "bd-1"): 3,
                ("-d+e", "bc+1", "d+e"): 1,
            }
        ),
        "middle-block divisor census changed",
    )
    direct_certificates = direct_cover_certificates(
        palette,
        five,
        bounded,
        data,
        middle_exceptions,
        triple_support,
    )
    require(len(direct_certificates) == 80, "direct middle charts changed")

    triple_case, triple_generic = next(
        item for item in middle_exceptions if item[0][0] == triple_support
    )
    require(
        triple_case[1] == (318, 338, 344, 750, 1571)
        and triple_case[2]
        == (
            True,
            (3,),
            (
                (
                    bounded.Q(0),
                    bounded.Q(0),
                    bounded.Q(0),
                    bounded.Q(1),
                    bounded.Q(0),
                    bounded.Q(-1),
                ),
            ),
            18,
        ),
        "three-divisor affine system changed",
    )
    require(
        five.permanent_expressions(
            bounded,
            data,
            triple_support,
            triple_case[1],
            ("a", "b", "c", "d", "e"),
        )
        == ("a*c", "a*d", "a*e", "b*c", "b*d"),
        "three-divisor permanent map changed",
    )
    expected_generic_base = (
        ("1", 1),
        ("-d+e", 1),
        ("d", 2),
        ("bc+1", 3),
        ("a", 4),
        ("b", 5),
        ("d+e", 6),
    )
    require(
        triple_generic[3]["base"] == triple_generic[3]["aug0"]
        == expected_generic_base,
        "three-divisor generic minor changed",
    )

    first_layer = {
        "-d+e": five.five_cell_determinants(
            bounded, data, triple_support, tuple(map(bounded.Q, SAMPLES["-d+e"]))
        ),
        "bc+1": five.five_cell_determinants(
            bounded, data, triple_support, tuple(map(bounded.Q, SAMPLES["bc+1"]))
        ),
        "d+e": five.five_cell_determinants(
            bounded, data, triple_support, tuple(map(bounded.Q, SAMPLES["d+e"]))
        ),
    }
    require(
        all(
            not palette.divisor_has_no_torus_zero(divisor, record[3]["base"])
            for divisor, record in first_layer.items()
        ),
        "the three-divisor branch unexpectedly closed in one layer",
    )
    require(
        tuple(
            tuple(sorted(palette.non_torus_factors(record[3]["base"])))
            for record in first_layer.values()
        )
        == (
            ("bc+1", "d+e"),
            ("-d+e", "d+e"),
            ("-d+e", "bc+1"),
        ),
        "first-layer intersection factors changed",
    )

    double_charts = (
        (
            ("-d+e", "bc+1"),
            five.five_cell_determinants(
                bounded,
                data,
                triple_support,
                tuple(map(bounded.Q, (2, 1, -1, 1, 1))),
            ),
        ),
        (
            ("d+e", "bc+1"),
            five.five_cell_determinants(
                bounded,
                data,
                triple_support,
                tuple(map(bounded.Q, (2, 1, -1, 1, -1))),
            ),
        ),
    )
    for equations, record in double_charts:
        require(
            no_torus_zero(palette, equations, record[3]["base"])
            and any(
                name.startswith("aug")
                and no_torus_zero(palette, equations, factors)
                for name, factors in record[3].items()
            ),
            "a codimension-two intersection chart did not close",
        )

    closed_this_batch = 7 * 59_640
    require(closed_this_batch == 417_480, "batch support count changed")
    closed_cumulative = 832_608 + closed_this_batch
    remaining = 11_614_176 - closed_cumulative
    require(
        (closed_cumulative, remaining) == (1_250_088, 10_364_088),
        "cumulative frontier arithmetic changed",
    )
    require(
        pair_survivors[21] == ((0, 8, 1, 2), (6, 8, 0, 0)),
        "next pair block changed",
    )

    print("N=10 five-cross pair blocks 15-21: exact PASS")
    print("complete pair blocks audited: 7; supports: 417480")
    print("affine candidates: 1845; torus candidates: 779")
    print("literal exclusions: 653 global monomials + 126 divisor supports")
    print("special charts: 53 ordinary + 80 direct + 2 codimension-two")
    print("literal survivors: 0")
    print("cumulative closed new grade-3-to-6 supports: 1250088")
    print("remaining unaudited grade-3-to-6 supports: 10364088")


if __name__ == "__main__":
    main()
