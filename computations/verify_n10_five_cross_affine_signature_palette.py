#!/usr/bin/env python3
"""Exact affine-signature and torus-minor palette at five cross cells."""

from __future__ import annotations

import importlib.util
import subprocess
from collections import Counter, defaultdict
from fractions import Fraction
from itertools import combinations
from pathlib import Path


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def load_five_frontier():
    path = Path(__file__).with_name(
        "verify_n10_five_cross_bounded_frontier.py"
    )
    spec = importlib.util.spec_from_file_location("five_frontier", path)
    require(spec is not None and spec.loader is not None, "cannot load frontier")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def sparse_key(vector):
    return tuple(sorted(vector.items()))


def basis_key(basis):
    return tuple((pivot, sparse_key(vector)) for pivot, vector in basis.items())


def table_key(table):
    return tuple(
        (word, sparse_key(vector)) for word, vector in sorted(table.items())
    )


def pair_shape(pair):
    left, right = pair
    return (
        left[0] == right[0],
        tuple(sorted((left[2], right[2]))),
        tuple(sorted((left[3], right[3]))),
    )


def exact_pair_signatures(data, pair_survivors, right_coordinates):
    module = data["module"]
    span_groups = defaultdict(list)
    grade_signature_ids = {}
    grade_ids = []
    for record in data["grade_data"]:
        signature = (basis_key(record[1]), table_key(record[2]), record[3])
        grade_ids.append(
            grade_signature_ids.setdefault(signature, len(grade_signature_ids))
        )
    leaf_maps = {}
    for left_pair in pair_survivors:
        grades = tuple(
            sorted(
                {
                    data["oriented_pair_to_grade"][(left, right)]
                    for left in left_pair
                    for right in right_coordinates
                    if (left, right) in data["oriented_pair_to_grade"]
                }
            )
        )
        generators = []
        for grade in grades:
            generators.extend(data["grade_data"][grade][1].values())
            generators.extend(data["grade_data"][grade][2].values())
        span_groups[basis_key(module.rational_basis(generators))].append(left_pair)
        leaf_signature = Counter(
            tuple(
                sorted(
                    grade_ids[data["oriented_pair_to_grade"][(left, right)]]
                    for left in left_pair
                    if (left, right) in data["oriented_pair_to_grade"]
                )
            )
            for right in right_coordinates
        )
        leaf_maps[left_pair] = tuple(sorted(leaf_signature.items()))
    return span_groups, grade_signature_ids, leaf_maps


def rational_constant(factor):
    try:
        Fraction(factor)
    except (ValueError, ZeroDivisionError):
        return False
    return True


def torus_monomial(factors):
    variables = {"a", "b", "c", "d", "e"}
    return all(
        factor in variables or rational_constant(factor)
        for factor, _exponent in factors
    )


def non_torus_factors(factors):
    variables = {"a", "b", "c", "d", "e"}
    return {
        factor
        for factor, _exponent in factors
        if factor not in variables and not rational_constant(factor)
    }


def factor_expression(factors):
    terms = []
    for factor, exponent in factors:
        term = f"({factor})"
        if exponent != 1:
            term += f"^{exponent}"
        terms.append(term)
    return "*".join(terms) if terms else "1"


def divisor_has_no_torus_zero(divisor, determinant_factors):
    determinant = factor_expression(determinant_factors)
    lines = [
        "ring r=0,(a,b,c,d,e,t),dp;",
        f"ideal I=({divisor}),({determinant}),t*a*b*c*d*e-1;",
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


def audit_pair_block(five, four, bounded, data, left_pair, right_coordinates):
    affine_cache = {}
    records = Counter()
    system_signatures = Counter()
    affine_cases = []
    for right_triple in combinations(right_coordinates, 3):
        support = left_pair + right_triple
        grades = tuple(
            bounded.support_permanents(data, support, (bounded.Q(1),) * 5)
        )
        grade_count = len(grades)
        if grade_count < 3:
            records[(grade_count, "prior")] += 1
            continue
        if grades not in affine_cache:
            affine_cache[grades] = bounded.exact_affine_system(data, grades)
        system = affine_cache[grades]
        system_signatures[system] += 1
        records[(grade_count, "affine" if system[0] else "excluded")] += 1
        if system[0]:
            affine_cases.append((support, grades, system))
    saturation = (
        five.torus_affine_saturation(
            four, bounded, data, affine_cases, ("a", "b", "c", "d", "e")
        )
        if affine_cases
        else {}
    )
    torus_cases = tuple(
        affine_cases[index]
        for index, survives in saturation.items()
        if survives
    )
    sample = tuple(map(bounded.Q, (1, 2, 3, 5, 7)))
    determinant_records = tuple(
        (
            case,
            five.five_cell_determinants(bounded, data, case[0], sample),
        )
        for case in torus_cases
    )
    exceptions = tuple(
        (case, determinant)
        for case, determinant in determinant_records
        if not (
            torus_monomial(determinant[3]["base"])
            and any(
                name.startswith("aug") and torus_monomial(factors)
                for name, factors in determinant[3].items()
            )
        )
    )
    return {
        "records": records,
        "system_signatures": system_signatures,
        "affine_cases": tuple(affine_cases),
        "torus_cases": torus_cases,
        "determinants": determinant_records,
        "exceptions": exceptions,
    }


def close_exceptional_divisors(
    five, bounded, data, exceptions, special_samples
):
    exception_map = {case[0]: determinant for case, determinant in exceptions}
    require(
        set(exception_map) == set(special_samples),
        "exceptional support palette changed",
    )
    certificates = []
    for support, determinant in exception_map.items():
        require(
            determinant[3]["base"] == determinant[3]["aug0"],
            "generic square/augmented minor pair changed",
        )
        divisors = non_torus_factors(determinant[3]["base"])
        require(
            divisors == set(special_samples[support]),
            "rank-divisor palette changed",
        )
        for divisor, weights in special_samples[support].items():
            special = five.five_cell_determinants(
                bounded,
                data,
                support,
                tuple(map(bounded.Q, weights)),
            )
            require(
                special[3]["base"] == special[3]["aug0"],
                "special square/augmented minor pair changed",
            )
            require(
                divisor_has_no_torus_zero(divisor, special[3]["base"]),
                "special pivot vanishes on its torus divisor",
            )
            certificates.append((support, divisor, special[3]["base"]))
    return tuple(certificates)


def main() -> None:
    five = load_five_frontier()
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

    span_groups, grade_signatures, leaf_maps = exact_pair_signatures(
        data, pair_survivors, right_coordinates
    )
    require(len(grade_signatures) == 1805, "individual grade signatures changed")
    require(len(span_groups) == 66, "two-centre span signatures changed")
    require(
        Counter(map(len, span_groups.values()))
        == Counter({3: 30, 1: 26, 9: 8, 6: 1, 2: 1}),
        "two-centre signature multiplicities changed",
    )
    require(len(set(leaf_maps.values())) == 196, "exact leaf maps collided")
    expected_shapes = Counter(
        {
            (False, (1, 1), (0, 2)): 56,
            (False, (0, 1), (0, 2)): 42,
            (False, (1, 2), (0, 2)): 42,
            (False, (0, 2), (0, 2)): 12,
            (True, (1, 1), (0, 2)): 8,
            (True, (0, 1), (0, 2)): 6,
            (True, (0, 2), (0, 2)): 6,
            (False, (0, 0), (0, 2)): 6,
            (True, (1, 2), (0, 2)): 6,
            (False, (2, 2), (0, 2)): 6,
            (True, (0, 0), (0, 2)): 3,
            (True, (2, 2), (0, 2)): 3,
        }
    )
    require(
        Counter(map(pair_shape, pair_survivors)) == expected_shapes,
        "ambient pair-shape census changed",
    )

    audits = tuple(
        audit_pair_block(
            five,
            four,
            bounded,
            data,
            pair_survivors[index],
            right_coordinates,
        )
        for index in range(7)
    )
    expected_frontiers = (
        (612, 204, 4),
        (207, 78, 0),
        (0, 0, 0),
        (207, 58, 0),
        (0, 0, 0),
        (612, 287, 2),
        (207, 78, 1),
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
        == expected_frontiers,
        "seven-block frontier census changed",
    )
    require(
        all(
            len(audit["determinants"])
            - len(audit["exceptions"])
            == sum(
                1
                for _case, determinant in audit["determinants"]
                if torus_monomial(determinant[3]["base"])
                and any(
                    name.startswith("aug") and torus_monomial(factors)
                    for name, factors in determinant[3].items()
                )
            )
            for audit in audits
        ),
        "global monomial palette changed",
    )

    s00 = (
        (0, 8, 1, 0), (0, 8, 1, 2), (3, 9, 1, 0),
        (3, 9, 1, 2), (4, 9, 0, 0),
    )
    s01 = (
        (0, 8, 1, 0), (0, 8, 1, 2), (3, 9, 1, 0),
        (3, 9, 1, 2), (4, 9, 0, 2),
    )
    s02 = (
        (0, 8, 1, 0), (0, 8, 1, 2), (3, 9, 1, 0),
        (4, 9, 0, 0), (5, 9, 1, 2),
    )
    s03 = (
        (0, 8, 1, 0), (0, 8, 1, 2), (3, 9, 1, 2),
        (4, 9, 0, 2), (5, 9, 1, 0),
    )
    block0_samples = {
        s00: {"-c+e": (1, 2, 1, 3, 1), "c+e": (1, 2, 1, 3, -1)},
        s01: {"d+e": (1, 2, 3, 1, -1)},
        s02: {"-c+d": (1, 2, 1, 1, 3), "c+d": (1, 2, 1, -1, 3)},
        s03: {"-c+d": (1, 2, 1, 1, 3), "c+d": (1, 2, 1, -1, 3)},
    }
    block0_certificates = close_exceptional_divisors(
        five, bounded, data, audits[0]["exceptions"], block0_samples
    )

    s50 = (
        (0, 8, 1, 0), (3, 8, 1, 2), (0, 9, 1, 2),
        (3, 9, 1, 0), (4, 9, 0, 0),
    )
    s51 = (
        (0, 8, 1, 0), (3, 8, 1, 2), (3, 9, 1, 0),
        (4, 9, 0, 0), (5, 9, 1, 2),
    )
    block5_samples = {
        s50: {"d+e": (1, 2, 3, 1, -1)},
        s51: {"c-d": (1, 2, 1, 1, 3), "c+d": (1, 2, 1, -1, 3)},
    }
    block5_certificates = close_exceptional_divisors(
        five, bounded, data, audits[5]["exceptions"], block5_samples
    )

    s60 = (
        (0, 8, 1, 0), (4, 8, 1, 2), (1, 9, 1, 2),
        (3, 9, 1, 0), (4, 9, 0, 0),
    )
    block6_samples = {
        s60: {"-d+e": (1, 2, 3, 1, 1), "d+e": (1, 2, 3, 1, -1)}
    }
    block6_certificates = close_exceptional_divisors(
        five, bounded, data, audits[6]["exceptions"], block6_samples
    )
    require(
        tuple(map(len, (block0_certificates, block5_certificates,
                        block6_certificates))) == (7, 3, 2),
        "divisor certificate count changed",
    )

    closed_novel = sum(
        sum(
            count
            for (grade_count, _status), count in audit["records"].items()
            if grade_count >= 3
        )
        for audit in audits
    )
    require(closed_novel == 415_128, "closed novel support count changed")
    require(
        tuple(len(audit["system_signatures"]) for audit in audits)
        == (182, 636, 295, 349, 350, 523, 551),
        "seven-block affine palette sizes changed",
    )

    eighth_pair = pair_survivors[7]
    scanned_novel = 0
    affine_seen = 0
    first_torus_case = None
    first_torus_record = None
    affine_cache = {}
    for right_triple in combinations(right_coordinates, 3):
        support = eighth_pair + right_triple
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
            four, bounded, data, (case,), ("a", "b", "c", "d", "e")
        )
        if saturation[0]:
            first_torus_case = case
            first_torus_record = five.five_cell_determinants(
                bounded,
                data,
                support,
                tuple(map(bounded.Q, (1, 2, 3, 5, 7))),
            )
            break
    expected_first_support = (
        (0, 8, 1, 0),
        (5, 8, 1, 2),
        (0, 9, 0, 0),
        (0, 9, 1, 2),
        (2, 9, 1, 0),
    )
    require(
        (scanned_novel, affine_seen) == (290, 1)
        and first_torus_case is not None
        and first_torus_case[0] == expected_first_support,
        "eighth-block first torus candidate changed",
    )
    require(
        first_torus_case[1] == (201, 165, 356, 1299)
        and first_torus_case[2]
        == (
            True,
            (0,),
            ((bounded.Q(1), bounded.Q(0), bounded.Q(0), bounded.Q(0),
              bounded.Q(-1)),),
            12,
        ),
        "eighth-block exact affine system changed",
    )
    first_expressions = five.permanent_expressions(
        bounded,
        data,
        first_torus_case[0],
        first_torus_case[1],
        ("a", "b", "c", "d", "e"),
    )
    require(
        first_expressions == ("a*e", "b*c", "b*d", "b*e"),
        "eighth-block permanent map changed",
    )
    expected_first_minor = (("1", 1), ("a", 3), ("b", 1), ("c", 4))
    require(
        first_torus_record is not None
        and first_torus_record[3]["base"] == expected_first_minor
        and first_torus_record[3]["aug0"] == expected_first_minor,
        "eighth-block first determinant changed",
    )

    remaining_novel = 11_614_176 - closed_novel - scanned_novel
    require(remaining_novel == 11_198_758, "remaining frontier count changed")
    affine_palette = tuple(len(audit["system_signatures"]) for audit in audits)
    print("N=10 five-cross affine-signature palette: exact PASS")
    print("pair survivors: 196; ambient shapes: 12; exact span signatures: 66")
    print("signature multiplicities: {1:26, 2:1, 3:30, 6:1, 9:8}")
    print("full exact leaf-map signatures: 196 (no source-faithful transfer)")
    print(f"first seven affine palette sizes: {affine_palette}")
    print("first seven pair blocks: 417480 supports; literal survivors: 0")
    print("closed new grade-3-to-6 supports: 415128")
    print("next block first torus candidate: ae=1; base=aug0=a^3*b*c^4")
    print("remaining unaudited grade-3-to-6 supports: 11198758")


if __name__ == "__main__":
    main()
