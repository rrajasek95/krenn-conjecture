#!/usr/bin/env python3
"""Exact stabilizer and smallest unstructured four-cross frontier."""

from __future__ import annotations

import importlib.util
import subprocess
from collections import Counter
from itertools import combinations, permutations
from pathlib import Path


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def load_bounded_frontier():
    path = Path(__file__).with_name(
        "verify_n10_four_cross_minimal_frontier.py"
    )
    spec = importlib.util.spec_from_file_location("bounded", path)
    require(spec is not None and spec.loader is not None, "cannot load frontier")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def canonical_cells(cells):
    return tuple(
        sorted(
            (
                left,
                right,
                colour_l,
                colour_r,
                weight,
            )
            for (left, right), entries in cells.items()
            for colour_l, colour_r, weight in entries
            if weight
        )
    )


def transform_cells(cells, vertex_permutation, colour_permutation):
    transformed = []
    for (left, right), entries in cells.items():
        new_left = vertex_permutation[left]
        new_right = vertex_permutation[right]
        for colour_l, colour_r, weight in entries:
            mapped_l = colour_permutation[colour_l]
            mapped_r = colour_permutation[colour_r]
            if new_left < new_right:
                transformed.append(
                    (new_left, new_right, mapped_l, mapped_r, weight)
                )
            else:
                transformed.append(
                    (new_right, new_left, mapped_r, mapped_l, weight)
                )
    return tuple(sorted(record for record in transformed if record[-1]))


def discrete_stabilizer(data):
    base_key = canonical_cells(data["base"])
    cut = frozenset((2, 6, 7))
    stabilizer = []
    for vertex_permutation in permutations(range(8)):
        if frozenset(vertex_permutation[vertex] for vertex in cut) != cut:
            continue
        for colour_permutation in permutations(range(3)):
            if (
                transform_cells(
                    data["base"], vertex_permutation, colour_permutation
                )
                == base_key
            ):
                stabilizer.append((vertex_permutation, colour_permutation))
    return tuple(stabilizer)


def rational_string(value):
    if value.denominator == 1:
        return str(value.numerator)
    return f"({value.numerator}/{value.denominator})"


def permanent_polynomial_expressions(bounded, data, support, grade_indices):
    polynomials = {grade: {} for grade in grade_indices}
    for left_index, right_index in combinations(range(4), 2):
        grade = bounded.grade_for_coordinates(
            data, support[left_index], support[right_index]
        )
        if grade not in polynomials:
            continue
        monomial = tuple(
            1 if index in (left_index, right_index) else 0
            for index in range(4)
        )
        polynomials[grade][monomial] = (
            polynomials[grade].get(monomial, bounded.Q(0)) + 1
        )
    return tuple(
        bounded.polynomial_expression(polynomials[grade], ("a", "b", "c", "d"))
        for grade in grade_indices
    )


def torus_affine_saturation(bounded, data, survivors):
    lines = ["ring r=0,(a,b,c,d,t),dp;"]
    for case_index, (support, grades, system) in enumerate(survivors):
        permanent_expressions = permanent_polynomial_expressions(
            bounded, data, support, grades
        )
        equations = []
        for row in system[2]:
            terms = []
            for coefficient, expression in zip(row[:-1], permanent_expressions):
                if coefficient:
                    terms.append(f"({rational_string(coefficient)})*({expression})")
            if row[-1]:
                terms.append(f"-({rational_string(row[-1])})")
            equations.append("+".join(terms).replace("+-", "-") or "0")
        equations.append("t*a*b*c*d-1")
        lines.append(f"ideal I{case_index}={','.join(equations)};")
        lines.append(f"ideal G{case_index}=std(I{case_index});")
        lines.append(f'print("case{case_index}");')
        lines.append(f"reduce(1,G{case_index});")
    process = subprocess.run(
        ["Singular", "-q"],
        input="\n".join(lines),
        text=True,
        capture_output=True,
        check=True,
    )
    output = [line.strip() for line in process.stdout.splitlines() if line.strip()]
    records = {}
    for index in range(0, len(output), 2):
        require(output[index].startswith("case"), "saturation marker missing")
        case_index = int(output[index][4:])
        require(output[index + 1] in ("0", "1"), "unexpected saturation remainder")
        records[case_index] = output[index + 1] == "1"
    require(len(records) == len(survivors), "saturation record count changed")
    return records


def torus_monomial(factors):
    return all(factor in ("-1", "1", "a", "b", "c", "d") for factor, _ in factors)


def non_torus_factors(factors):
    return {
        factor
        for factor, _exponent in factors
        if factor not in ("-1", "1", "a", "b", "c", "d")
    }


def main() -> None:
    bounded = load_bounded_frontier()
    data = bounded.prepare()
    stabilizer = discrete_stabilizer(data)
    module = data["module"]
    two_cell = data["two_cell"]
    centres = tuple(
        coordinate for coordinate in data["coordinates"] if coordinate[1] == 8
    )
    opposites = tuple(
        coordinate for coordinate in data["coordinates"] if coordinate[1] == 9
    )
    centre_records = {}
    for centre in centres:
        grades = tuple(
            data["oriented_pair_to_grade"][(centre, opposite)]
            for opposite in opposites
            if (centre, opposite) in data["oriented_pair_to_grade"]
        )
        require(len(grades) == 63, "centre grade valency changed")
        generators = []
        for grade in grades:
            generators.extend(data["grade_data"][grade][1].values())
            generators.extend(data["grade_data"][grade][2].values())
        basis = module.rational_basis(generators)
        bad = {
            word: two_cell.quotient_remainder(row, basis)
            for word, row in data["residual_q"].items()
            if not module.rational_member(row, basis)
        }
        centre_records[centre] = len(basis), bad
    rank_census = Counter(rank for rank, _bad in centre_records.values())
    bad_census = Counter(
        tuple(
            (word, tuple(sorted(remainder.items())))
            for word, remainder in sorted(bad.items())
        )
        for _rank, bad in centre_records.values()
    )
    left_pairs = tuple(combinations(centres, 2))
    pair_records = {}
    for left_pair in left_pairs:
        grades = tuple(
            sorted(
                {
                    data["oriented_pair_to_grade"][(centre, opposite)]
                    for centre in left_pair
                    for opposite in opposites
                    if (centre, opposite) in data["oriented_pair_to_grade"]
                }
            )
        )
        generators = []
        for grade in grades:
            generators.extend(data["grade_data"][grade][1].values())
            generators.extend(data["grade_data"][grade][2].values())
        basis = module.rational_basis(generators)
        bad = {
            word: two_cell.quotient_remainder(row, basis)
            for word, row in data["residual_q"].items()
            if not module.rational_member(row, basis)
        }
        pair_records[left_pair] = len(grades), len(basis), bad
    pair_survivors = {
        left_pair: record
        for left_pair, record in pair_records.items()
        if not record[2]
    }
    survivor_shape_census = Counter(
        (
            left[0] == right[0],
            tuple(sorted((left[2], right[2]))),
            tuple(sorted((left[3], right[3]))),
        )
        for left, right in pair_survivors
    )
    survivor_pairs = tuple(sorted(pair_survivors))
    rectangle_orbit_records = Counter()
    affine_rectangle_survivors = []
    for left_index, left_pair in enumerate(survivor_pairs):
        for right_pair in survivor_pairs[left_index:]:
            support = left_pair + tuple(
                bounded.swap_new_coordinate(coordinate)
                for coordinate in right_pair
            )
            permanents = bounded.support_permanents(
                data, support, (bounded.Q(1),) * 4
            )
            grade_count = len(permanents)
            if grade_count <= 2:
                rectangle_orbit_records[(grade_count, "prior")] += 1
                continue
            system = bounded.exact_affine_system(data, tuple(permanents))
            rectangle_orbit_records[
                (grade_count, "affine" if system[0] else "excluded")
            ] += 1
            if system[0]:
                affine_rectangle_survivors.append(
                    (support, tuple(permanents), system)
                )
    saturation_records = torus_affine_saturation(
        bounded, data, affine_rectangle_survivors
    )
    torus_affine_survivors = tuple(
        affine_rectangle_survivors[index]
        for index, survives in saturation_records.items()
        if survives
    )
    sample_weights = tuple(map(bounded.Q, (1, 2, 3, 5)))
    actual_sample_records = tuple(
        (
            support,
            bounded.fast_actual_cut_record(data, support, sample_weights),
        )
        for support, _grades, _system in torus_affine_survivors
    )
    actual_sample_survivors = tuple(
        (support, record)
        for support, record in actual_sample_records
        if record[0]
    )
    determinant_records = tuple(
        (
            support,
            bounded.singular_determinants(data, support, sample_weights),
        )
        for support, _grades, _system in torus_affine_survivors
    )
    monomial_exclusions = tuple(
        (support, record)
        for support, record in determinant_records
        if torus_monomial(record[3]["base"])
        and any(
            name.startswith("aug") and torus_monomial(factors)
            for name, factors in record[3].items()
        )
    )
    determinant_survivors = tuple(
        (support, record)
        for support, record in determinant_records
        if (support, record) not in monomial_exclusions
    )
    exceptional_records = []
    for support, record in determinant_survivors:
        base_factors = {factor for factor, _exponent in record[3]["base"]}
        require(
            bool(base_factors & {"ac+1", "bc+1"}),
            "unexpected generic determinant survivor",
        )
        sample = (
            tuple(map(bounded.Q, (1, 2, -1, 3)))
            if "ac+1" in base_factors
            else tuple(map(bounded.Q, (2, 1, -1, 3)))
        )
        exceptional_records.append(
            (
                support,
                next(iter(base_factors & {"ac+1", "bc+1"})),
                bounded.singular_determinants(data, support, sample),
            )
        )

    identity = ((tuple(range(8)), tuple(range(3))),)
    require(stabilizer == identity, "anchored old-source stabilizer changed")
    expected_rank_census = Counter(
        {66: 15, 87: 12, 27: 9, 102: 9, 75: 6, 90: 3,
         72: 3, 60: 3, 93: 3, 78: 3, 84: 3, 69: 3}
    )
    require(rank_census == expected_rank_census, "centre rank census changed")
    centre_obstructions = Counter(
        tuple(sorted(bad[(1, 1, 1)].items()))
        for _rank, bad in centre_records.values()
        if set(bad) == {(1, 1, 1)}
    )
    expected_centre_obstructions = Counter(
        {
            ((1089, bounded.Q(1)), (1097, bounded.Q(1))): 44,
            ((1097, bounded.Q(1)),): 14,
            ((1089, bounded.Q(1)),): 14,
        }
    )
    require(
        centre_obstructions == expected_centre_obstructions
        and sum(bad_census.values()) == 72,
        "centre universal obstruction changed",
    )
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
    require(len(pair_records) == 2556, "two-centre pair count changed")
    require(len(pair_survivors) == 196, "two-centre survivor count changed")
    require(
        survivor_shape_census == expected_shapes,
        "two-centre survivor shapes changed",
    )
    expected_rectangles = Counter(
        {
            (4, "excluded"): 9651,
            (3, "excluded"): 6654,
            (2, "prior"): 2770,
            (0, "prior"): 140,
            (4, "affine"): 73,
            (3, "affine"): 18,
        }
    )
    require(
        rectangle_orbit_records == expected_rectangles,
        "reduced rectangle census changed",
    )
    require(len(affine_rectangle_survivors) == 91, "affine frontier changed")
    require(len(torus_affine_survivors) == 45, "torus affine frontier changed")
    require(not actual_sample_survivors, "generic actual-cut survivor appeared")
    require(len(monomial_exclusions) == 41, "global monomial exclusions changed")
    require(len(determinant_survivors) == 4, "exceptional divisor count changed")
    exceptional_factor_census = Counter(
        factor for _support, factor, _record in exceptional_records
    )
    require(
        exceptional_factor_census == Counter({"bc+1": 3, "ac+1": 1}),
        "exceptional divisor census changed",
    )
    for support, factor, special_record in exceptional_records:
        generic_record = next(
            record for candidate, record in determinant_survivors
            if candidate == support
        )
        require(
            non_torus_factors(generic_record[3]["base"]) == {factor}
            and any(
                name.startswith("aug")
                and non_torus_factors(factors) == {factor}
                for name, factors in generic_record[3].items()
            ),
            "generic exceptional-divisor cover changed",
        )
        require(
            torus_monomial(special_record[3]["base"])
            and any(
                name.startswith("aug") and torus_monomial(factors)
                for name, factors in special_record[3].items()
            ),
            "exceptional-divisor monomial cover changed",
        )

    three_grade_stars = len(centres) * len(tuple(combinations(range(63), 3)))
    require(three_grade_stars == 2_859_192, "three-grade star count changed")
    print("N=10 unstructured four-cross stabilizer frontier: exact PASS")
    print("old-source/cut-2 discrete stabilizer: identity only")
    print("three-grade stars excluded by centre-universal quotient: 2859192")
    print("two-centre sieve: 2556 pairs -> 196 survivors -> 19306 rectangles")
    print(f"reduced rectangle orbit records: {rectangle_orbit_records}")
    print("affine survivors: 91; nonzero-weight torus survivors: 45")
    print("literal determinants: 41 global monomial exclusions")
    print("second pivots: 3 selected at bc+1=0; 1 at ac+1=0; all monomial")
    print("fixed-old four-cross-cell frontier: no cut-2 survivor")


if __name__ == "__main__":
    main()
