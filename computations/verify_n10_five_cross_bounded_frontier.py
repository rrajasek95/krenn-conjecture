#!/usr/bin/env python3
"""Exact topology and bounded tests at the fixed-old five-cross frontier."""

from __future__ import annotations

import importlib.util
import math
import subprocess
from collections import Counter
from itertools import combinations, product
from pathlib import Path


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def load_four_closure():
    path = Path(__file__).with_name(
        "verify_n10_four_cross_unstructured_stabilizer_frontier.py"
    )
    spec = importlib.util.spec_from_file_location("four_closure", path)
    require(spec is not None and spec.loader is not None, "cannot load closure")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def abstract_grade(left, right):
    left_vertex, left_old_colour, left_new_colour = left
    right_vertex, right_old_colour, right_new_colour = right
    if left_vertex == right_vertex:
        return None
    nodes = tuple(
        sorted(
            (
                (left_vertex, left_old_colour),
                (right_vertex, right_old_colour),
            )
        )
    )
    return nodes + (left_new_colour, right_new_colour)


def abstract_pair_grade_census(pair, coordinates):
    grades = sorted(
        {
            abstract_grade(left, right)
            for left in pair
            for right in coordinates
            if abstract_grade(left, right) is not None
        }
    )
    grade_index = {grade: index for index, grade in enumerate(grades)}
    masks = []
    for right in coordinates:
        mask = 0
        for left in pair:
            grade = abstract_grade(left, right)
            if grade is not None:
                mask |= 1 << grade_index[grade]
        masks.append(mask)
    census = Counter()
    for i, j, k in combinations(range(len(coordinates)), 3):
        census[(masks[i] | masks[j] | masks[k]).bit_count()] += 1
    return len(grades), census


def permanent_expressions(bounded, data, support, grade_indices, variables):
    polynomials = {grade: {} for grade in grade_indices}
    for left_index, right_index in combinations(range(len(support)), 2):
        grade = bounded.grade_for_coordinates(
            data, support[left_index], support[right_index]
        )
        if grade not in polynomials:
            continue
        monomial = tuple(
            1 if index in (left_index, right_index) else 0
            for index in range(len(support))
        )
        polynomials[grade][monomial] = (
            polynomials[grade].get(monomial, bounded.Q(0)) + 1
        )
    return tuple(
        bounded.polynomial_expression(polynomials[grade], variables)
        for grade in grade_indices
    )


def torus_affine_saturation(four, bounded, data, cases, variables):
    ring_variables = variables + ("t",)
    lines = [f"ring r=0,({','.join(ring_variables)}),dp;"]
    for case_index, (support, grades, system) in enumerate(cases):
        expressions = permanent_expressions(
            bounded, data, support, grades, variables
        )
        equations = []
        for row in system[2]:
            terms = []
            for coefficient, expression in zip(row[:-1], expressions):
                if coefficient:
                    terms.append(
                        f"({four.rational_string(coefficient)})*({expression})"
                    )
            if row[-1]:
                terms.append(f"-({four.rational_string(row[-1])})")
            equations.append("+".join(terms).replace("+-", "-") or "0")
        equations.append(f"t*{'*'.join(variables)}-1")
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
        require(output[index + 1] in ("0", "1"), "bad saturation remainder")
        records[case_index] = output[index + 1] == "1"
    require(len(records) == len(cases), "saturation record count changed")
    return records


def five_cell_determinants(bounded, data, support, sample_weights):
    module = data["module"]
    two_cell = data["two_cell"]
    columns_at_sample = bounded.evaluated_columns(data, support, sample_weights)
    labels, basis = bounded.independent_column_labels(module, columns_at_sample)
    polynomial_columns, polynomial_residual = bounded.raw_polynomial_data(
        data, support
    )
    pivot_rows = tuple(sorted(basis))
    require(len(labels) == len(pivot_rows), "pivot square changed")
    variables = ("a", "b", "c", "d", "e")

    cells = data["provenance"].add_weighted_coordinates(
        module,
        data["lifted_base"],
        tuple(zip(support, sample_weights)),
    )
    tensor = module.matching_tensor(data["provenance"].B10, cells)
    tensor = data["forced_pair"].tensor_difference(
        tensor,
        data["forced_pair"].delta_tensor(data["provenance"].B10),
    )
    residual_rows = data["forced_pair"].flatten_rows(
        tensor,
        data["provenance"].B10,
        (2, 6, 7),
        data["u_set"],
    )
    bad = {
        word: two_cell.quotient_remainder(vector, basis)
        for word, vector in residual_rows.items()
        if not module.rational_member(vector, basis)
    }

    matrices = []
    base_entries = [
        bounded.polynomial_expression(
            polynomial_columns[label].get(row, {}), variables
        )
        for row in pivot_rows
        for label in labels
    ]
    matrices.append(("base", len(labels), base_entries))
    for number, (word, remainder) in enumerate(sorted(bad.items())):
        extra_row = min(remainder)
        rows = pivot_rows + (extra_row,)
        entries = []
        for row in rows:
            for label in labels:
                entries.append(
                    bounded.polynomial_expression(
                        polynomial_columns[label].get(row, {}), variables
                    )
                )
            entries.append(
                bounded.polynomial_expression(
                    polynomial_residual.get(word, {}).get(row, {}), variables
                )
            )
        matrices.append((f"aug{number}", len(labels) + 1, entries))

    lines = ["ring r=0,(a,b,c,d,e),dp;"]
    for name, size, entries in matrices:
        lines.append(f"matrix {name}[{size}][{size}]={','.join(entries)};")
        lines.append(f'print("{name}");')
        lines.append(f"factorize(det({name}));")
    process = subprocess.run(
        ["Singular", "-q"],
        input="\n".join(lines),
        text=True,
        capture_output=True,
        check=True,
    )
    names = tuple(name for name, _size, _entries in matrices)
    return (
        len(labels),
        pivot_rows,
        bad,
        bounded.parse_factorizations(process.stdout, names),
    )


def torus_monomial(factors):
    return all(
        factor in ("-1", "1", "a", "b", "c", "d", "e")
        for factor, _exponent in factors
    )


def universal_pair_survivors(data, left_coordinates, right_coordinates):
    module = data["module"]
    two_cell = data["two_cell"]
    survivors = []
    for left_pair in combinations(left_coordinates, 2):
        grades = {
            data["oriented_pair_to_grade"][(left, right)]
            for left in left_pair
            for right in right_coordinates
            if (left, right) in data["oriented_pair_to_grade"]
        }
        generators = []
        for grade in grades:
            generators.extend(data["grade_data"][grade][1].values())
            generators.extend(data["grade_data"][grade][2].values())
        basis = module.rational_basis(generators)
        if all(
            module.rational_member(row, basis)
            for row in data["residual_q"].values()
        ):
            survivors.append(left_pair)
    return tuple(survivors)


def reduced_grade_census(data, pair_survivors, right_coordinates):
    census = Counter()
    two_grade_masks = set()
    for left_pair in pair_survivors:
        masks = []
        for right in right_coordinates:
            mask = 0
            for left in left_pair:
                grade = data["oriented_pair_to_grade"].get((left, right))
                if grade is not None:
                    mask |= 1 << grade
            masks.append(mask)
        for i in range(70):
            left_mask = masks[i]
            for j in range(i + 1, 71):
                pair_mask = left_mask | masks[j]
                for k in range(j + 1, 72):
                    mask = pair_mask | masks[k]
                    grade_count = mask.bit_count()
                    census[grade_count] += 1
                    if grade_count == 2:
                        two_grade_masks.add(mask)
    return census, two_grade_masks


def mask_indices(mask):
    indices = []
    while mask:
        low = mask & -mask
        indices.append(low.bit_length() - 1)
        mask ^= low
    return tuple(indices)


def main() -> None:
    four = load_four_closure()
    bounded = four.load_bounded_frontier()
    data = bounded.prepare()
    coordinates = tuple(product(range(8), range(3), range(3)))
    left_coordinates = tuple(
        coordinate for coordinate in data["coordinates"] if coordinate[1] == 8
    )
    right_coordinates = tuple(
        coordinate for coordinate in data["coordinates"] if coordinate[1] == 9
    )
    require(
        left_coordinates == tuple(sorted(left_coordinates))
        and right_coordinates == tuple(sorted(right_coordinates)),
        "cross-coordinate order changed",
    )

    identity = ((tuple(range(8)), tuple(range(3))),)
    require(
        four.discrete_stabilizer(data) == identity,
        "anchored old-source stabilizer changed",
    )
    key_to_grade = {}
    grade_to_key = {}
    for left in left_coordinates:
        abstract_left = (left[0], left[2], left[3])
        for right in right_coordinates:
            grade = data["oriented_pair_to_grade"].get((left, right))
            key = abstract_grade(
                abstract_left, (right[0], right[2], right[3])
            )
            require((grade is None) == (key is None), "grade support changed")
            if grade is None:
                continue
            require(
                key_to_grade.get(key, grade) == grade
                and grade_to_key.get(grade, key) == key,
                "abstract grade partition changed",
            )
            key_to_grade[key] = grade
            grade_to_key[grade] = key
    require(len(key_to_grade) == 2268, "permanent grade count changed")

    one_side_orbits = math.comb(72, 5)
    star_orbits = 72 * math.comb(72, 4)
    two_three_orbits = math.comb(72, 2) * math.comb(72, 3)
    require(
        (one_side_orbits, star_orbits, two_three_orbits)
        == (13_991_544, 74_072_880, 152_439_840),
        "five-cell topology count changed",
    )
    require(
        one_side_orbits + star_orbits + two_three_orbits
        == math.comb(144, 5) // 2 == 240_504_264,
        "five-cell forced-pair orbit total changed",
    )
    star_grade_census = Counter(
        {
            grade_count: 72
            * math.comb(63, grade_count)
            * math.comb(9, 4 - grade_count)
            for grade_count in range(5)
        }
    )
    require(
        star_grade_census
        == Counter(
            {4: 42_887_880, 3: 25_732_728, 2: 5_062_176,
             1: 381_024, 0: 9_072}
        ),
        "star grade census changed",
    )

    pair_types = (
        (72, ((0, 0, 0), (0, 0, 1))),
        (72, ((0, 0, 0), (0, 1, 0))),
        (144, ((0, 0, 0), (0, 1, 1))),
        (756, ((0, 0, 0), (1, 0, 0))),
        (1512, ((0, 0, 0), (1, 0, 1))),
    )
    require(sum(multiplicity for multiplicity, _pair in pair_types) == 2556,
            "abstract pair-type count changed")
    two_three_grade_census = Counter()
    pair_type_records = []
    for multiplicity, pair in pair_types:
        valency, census = abstract_pair_grade_census(pair, coordinates)
        pair_type_records.append((multiplicity, valency, census))
        for grade_count, count in census.items():
            two_three_grade_census[grade_count] += multiplicity * count
    same_vertex_census = Counter({6: 39_711, 4: 17_577, 2: 2_268, 0: 84})
    require(
        pair_type_records
        == [
            (72, 126, same_vertex_census),
            (72, 126, same_vertex_census),
            (144, 126, same_vertex_census),
            (756, 123, Counter({5: 25_758, 6: 24_804, 4: 8_100,
                                3: 930, 2: 48})),
            (1512, 126, Counter({5: 25_758, 6: 24_804, 4: 8_262,
                                 3: 816})),
        ],
        "abstract pair-type records changed",
    )
    require(
        two_three_grade_census
        == Counter(
            {6: 67_692_240, 5: 58_419_144, 4: 23_677_920,
             3: 1_936_872, 2: 689_472, 0: 24_192}
        ),
        "two-plus-three grade census changed",
    )

    module = data["module"]
    two_cell = data["two_cell"]
    centre_obstructions = 0
    for centre in left_coordinates:
        grades = {
            data["oriented_pair_to_grade"][(centre, opposite)]
            for opposite in right_coordinates
            if (centre, opposite) in data["oriented_pair_to_grade"]
        }
        require(len(grades) == 63, "centre valency changed")
        generators = []
        for grade in grades:
            generators.extend(data["grade_data"][grade][1].values())
            generators.extend(data["grade_data"][grade][2].values())
        basis = module.rational_basis(generators)
        if any(
            not module.rational_member(row, basis)
            for row in data["residual_q"].values()
        ):
            centre_obstructions += 1
    require(centre_obstructions == 72, "centre-universal star closure changed")

    pair_survivors = universal_pair_survivors(
        data, left_coordinates, right_coordinates
    )
    require(len(pair_survivors) == 196, "pair-universal survivor count changed")
    reduced_census, two_grade_masks = reduced_grade_census(
        data, pair_survivors, right_coordinates
    )
    require(
        reduced_census
        == Counter(
            {6: 5_338_608, 5: 4_224_312, 4: 1_917_432,
             3: 133_824, 2: 72_576, 0: 2_688}
        ),
        "pair-reduced grade census changed",
    )
    sharing_pairs = set(
        data["three_cell"].sharing_grade_pairs(
            data["provenance"], data["representatives"]
        )
    )
    require(
        all(mask_indices(mask) in sharing_pairs for mask in two_grade_masks),
        "a reduced two-grade support is not covered by sharing exclusion",
    )

    structured_supports = []
    affine_census = Counter()
    affine_survivors = []
    for left_pair in pair_survivors:
        if not (
            left_pair[0][0] == left_pair[1][0]
            and left_pair[0][2] == left_pair[1][2]
        ):
            continue
        for right_vertex in range(8):
            if right_vertex == left_pair[0][0]:
                continue
            for right_old_colour in range(3):
                support = left_pair + tuple(
                    (right_vertex, 9, right_old_colour, new_colour)
                    for new_colour in range(3)
                )
                permanents = bounded.support_permanents(
                    data, support, (bounded.Q(1),) * 5
                )
                require(len(permanents) == 6, "structured grade count changed")
                system = bounded.exact_affine_system(data, tuple(permanents))
                affine_census[(system[0], len(system[1]), system[3])] += 1
                structured_supports.append(support)
                if system[0]:
                    affine_survivors.append((support, tuple(permanents), system))
    expected_affine_census = Counter(
        {
            (False, 6, 0): 138,
            (False, 0, 0): 84,
            (False, 0, 36): 16,
            (False, 0, 30): 14,
            (False, 0, 18): 7,
            (True, 6, 0): 6,
            (False, 0, 12): 6,
            (False, 1, 0): 6,
            (True, 0, 36): 4,
            (False, 0, 24): 2,
            (False, 6, 18): 2,
            (True, 6, 18): 2,
            (False, 6, 12): 2,
            (True, 0, 54): 2,
            (False, 0, 54): 2,
            (False, 0, 48): 1,
        }
    )
    require(len(structured_supports) == 294, "structured support count changed")
    require(affine_census == expected_affine_census, "affine census changed")
    require(len(affine_survivors) == 14, "structured affine frontier changed")
    variables = ("a", "b", "c", "d", "e")
    structured_saturation = torus_affine_saturation(
        four, bounded, data, affine_survivors, variables
    )
    torus_survivors = tuple(
        affine_survivors[index]
        for index, survives in structured_saturation.items()
        if survives
    )
    require(len(torus_survivors) == 6, "structured torus frontier changed")
    sample_weights = tuple(map(bounded.Q, (1, 2, 3, 5, 7)))
    determinant_records = tuple(
        five_cell_determinants(bounded, data, support, sample_weights)
        for support, _grades, _system in torus_survivors
    )
    require(
        all(
            torus_monomial(record[3]["base"])
            and any(
                name.startswith("aug") and torus_monomial(factors)
                for name, factors in record[3].items()
            )
            for record in determinant_records
        ),
        "a structured literal determinant survivor appeared",
    )
    expected_determinants = Counter(
        {
            (20, (("-1", 1), ("a", 9), ("c", 8), ("d", 1))): 1,
            (20, (("1", 1), ("a", 9), ("c", 8), ("d", 1))): 1,
            (21, (("-1", 1), ("a", 4), ("c", 3), ("d", 1))): 2,
            (21, (("1", 1), ("a", 4), ("c", 3), ("d", 1))): 2,
        }
    )
    require(
        Counter((record[0], record[3]["base"]) for record in determinant_records)
        == expected_determinants,
        "structured determinant census changed",
    )

    first_pair = pair_survivors[0]
    initial_affine = []
    affine_cache = {}
    scanned = 0
    for right_triple in combinations(right_coordinates, 3):
        support = first_pair + right_triple
        grades = tuple(
            bounded.support_permanents(data, support, (bounded.Q(1),) * 5)
        )
        if len(grades) < 3:
            continue
        if grades not in affine_cache:
            affine_cache[grades] = bounded.exact_affine_system(data, grades)
        system = affine_cache[grades]
        scanned += 1
        if system[0]:
            initial_affine.append((support, grades, system))
            if not system[2]:
                break
    require((scanned, len(initial_affine)) == (1094, 6),
            "initial affine scan changed")
    initial_saturation = torus_affine_saturation(
        four, bounded, data, initial_affine, variables
    )
    initial_torus = tuple(
        initial_affine[index]
        for index, survives in initial_saturation.items()
        if survives
    )
    smallest_support = (
        (0, 8, 1, 0),
        (0, 8, 1, 2),
        (0, 9, 0, 0),
        (3, 9, 1, 0),
        (3, 9, 1, 2),
    )
    require(
        len(initial_torus) == 1 and initial_torus[0][0] == smallest_support,
        "smallest torus-affine candidate changed",
    )
    smallest_expressions = permanent_expressions(
        bounded, data, smallest_support, initial_torus[0][1], variables
    )
    require(
        smallest_expressions == ("a*d", "a*e", "b*d", "b*e"),
        "smallest candidate permanent map changed",
    )
    smallest_record = five_cell_determinants(
        bounded, data, smallest_support, sample_weights
    )
    expected_smallest_minor = (
        ("-1", 1), ("a", 9), ("d", 8), ("e", 1)
    )
    require(
        smallest_record[0] == 20
        and smallest_record[3]["base"] == expected_smallest_minor
        and smallest_record[3]["aug0"] == expected_smallest_minor,
        "smallest candidate determinant changed",
    )

    print("N=10 five-cross bounded frontier: exact PASS")
    print(
        "five-cell support orbits: one-side=13991544; "
        "stars=74072880; two-plus-three=152439840"
    )
    print(f"star permanent-grade census: {star_grade_census}")
    print(f"two-plus-three permanent-grade census: {two_three_grade_census}")
    print("centre-universal quotient excludes every one-plus-four star")
    print("two-centre sieve: 2556 pairs -> 196; supports -> 11689440")
    print(f"pair-reduced permanent-grade census: {reduced_census}")
    print("old-node 2x3 bicliques: 294 -> affine 14 -> torus 6 -> literal 0")
    print("smallest torus-affine five-cell candidate: monomially excluded")
    print("scope: 11614176 grade-3-to-6 two-plus-three supports remain open")


if __name__ == "__main__":
    main()
