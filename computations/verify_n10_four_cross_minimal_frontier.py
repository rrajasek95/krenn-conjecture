#!/usr/bin/env python3
"""Exact minimal four-cross-cell frontier on the anchored N=10 lift."""

from __future__ import annotations

import importlib.util
import subprocess
from collections import Counter, defaultdict
from fractions import Fraction
from itertools import combinations
from pathlib import Path


Q = Fraction
CUT = 2


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def load_three_cell_frontier():
    path = Path(__file__).with_name(
        "verify_n10_fixed_old_arbitrary_cross_frontier.py"
    )
    spec = importlib.util.spec_from_file_location("three_cell", path)
    require(spec is not None and spec.loader is not None, "cannot load frontier")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def sparse_key(vector):
    return tuple(sorted(vector.items()))


def basis_key(basis):
    return tuple((pivot, sparse_key(vector)) for pivot, vector in basis.items())


def table_key(table):
    return tuple((word, sparse_key(vector)) for word, vector in sorted(table.items()))


def quotient_table(table, basis, two_cell):
    return {
        word: two_cell.quotient_remainder(vector, basis)
        for word, vector in table.items()
    }


def exact_affine_system(data, grade_indices):
    """Necessary universal-cylinder equations in the listed permanent scalars."""
    module = data["module"]
    two_cell = data["two_cell"]
    q_basis = module.rational_basis(
        [
            vector
            for grade_index in grade_indices
            for vector in data["grade_data"][grade_index][1].values()
        ]
    )
    residual = quotient_table(data["residual_q"], q_basis, two_cell)
    directions = [
        quotient_table(data["grade_data"][grade_index][2], q_basis, two_cell)
        for grade_index in grade_indices
    ]
    equations = []
    words = set(residual)
    for table in directions:
        words.update(table)
    for word in words:
        vectors = [residual.get(word, {})] + [
            table.get(word, {}) for table in directions
        ]
        coordinates = set().union(*(set(vector) for vector in vectors))
        for coordinate in coordinates:
            equations.append(
                [
                    direction.get(coordinate, Q(0))
                    for direction in vectors[1:]
                ]
                + [-vectors[0].get(coordinate, Q(0))]
            )
    for colour in range(3):
        equations.append(
            [
                data["grade_data"][grade_index][3][colour]
                for grade_index in grade_indices
            ]
            + [Q(0)]
        )
    variable_count = len(grade_indices)
    pivots = []
    row_index = 0
    for column in range(variable_count):
        pivot = next(
            (
                index
                for index in range(row_index, len(equations))
                if equations[index][column]
            ),
            None,
        )
        if pivot is None:
            continue
        equations[row_index], equations[pivot] = equations[pivot], equations[row_index]
        scale = equations[row_index][column]
        equations[row_index] = [value / scale for value in equations[row_index]]
        for index, row in enumerate(equations):
            if index == row_index or not row[column]:
                continue
            factor = row[column]
            equations[index] = [
                row[j] - factor * equations[row_index][j]
                for j in range(variable_count + 1)
            ]
        pivots.append(column)
        row_index += 1
    consistent = not any(
        not any(row[:variable_count]) and row[-1] for row in equations
    )
    reduced = tuple(
        tuple(row) for row in equations if any(row)
    )
    return consistent, tuple(pivots), reduced, len(q_basis)


def grade_for_coordinates(data, left, right):
    return data["coordinate_pair_to_grade"].get(frozenset((left, right)))


def swap_new_coordinate(coordinate):
    old, new, old_colour, new_colour = coordinate
    require(new in (8, 9), "coordinate is not cross-new")
    return old, 17 - new, old_colour, new_colour


def support_orbit_key(support):
    direct = tuple(sorted(support))
    swapped = tuple(sorted(swap_new_coordinate(coordinate) for coordinate in support))
    return min(direct, swapped)


def actual_cut_record(data, weighted_coordinates):
    provenance = data["provenance"]
    module = data["module"]
    forced_pair = data["forced_pair"]
    cells = provenance.add_weighted_coordinates(
        module, data["lifted_base"], weighted_coordinates
    )
    tensor = module.matching_tensor(provenance.B10, cells)
    residual = forced_pair.tensor_difference(
        tensor, forced_pair.delta_tensor(provenance.B10)
    )
    columns = forced_pair.insertion_columns(module, data["u_set"], cells)
    basis = module.rational_basis(list(columns.values()))
    rows = forced_pair.flatten_rows(
        residual, provenance.B10, (CUT, 6, 7), data["u_set"]
    )
    bad = {
        word: data["two_cell"].quotient_remainder(row, basis)
        for word, row in rows.items()
        if not module.rational_member(row, basis)
    }
    return len(basis), bad


def sparse_combination(*terms):
    answer = {}
    for coefficient, vector in terms:
        if not coefficient:
            continue
        for index, value in vector.items():
            answer[index] = answer.get(index, Q(0)) + coefficient * value
            if not answer[index]:
                answer.pop(index)
    return answer


def support_permanents(data, support, weights):
    coefficients = {}
    for left_index, right_index in combinations(range(len(support)), 2):
        grade_index = grade_for_coordinates(
            data, support[left_index], support[right_index]
        )
        if grade_index is None:
            continue
        coefficients[grade_index] = coefficients.get(grade_index, Q(0)) + (
            weights[left_index] * weights[right_index]
        )
        if not coefficients[grade_index]:
            coefficients.pop(grade_index)
    return coefficients


def fast_actual_cut_record(data, support, weights):
    permanents = support_permanents(data, support, weights)
    anchor_change = tuple(
        sum(
            coefficient * data["grade_data"][grade_index][3][colour]
            for grade_index, coefficient in permanents.items()
        )
        for colour in range(3)
    )
    if any(anchor_change):
        return False, 0, {}, permanents
    columns = {}
    for label, base_column in data["base_columns"].items():
        terms = [(Q(1), base_column)]
        terms.extend(
            (weight, data["linear_directions"][coordinate][label])
            for coordinate, weight in zip(support, weights)
        )
        terms.extend(
            (coefficient, data["grade_data"][grade_index][4][label])
            for grade_index, coefficient in permanents.items()
        )
        columns[label] = sparse_combination(*terms)
    basis = data["module"].rational_basis(list(columns.values()))
    words = set(data["residual_rows"])
    for grade_index in permanents:
        words.update(data["grade_data"][grade_index][5])
    bad = {}
    for word in words:
        terms = [(Q(1), data["residual_rows"].get(word, {}))]
        terms.extend(
            (
                coefficient,
                data["grade_data"][grade_index][5].get(word, {}),
            )
            for grade_index, coefficient in permanents.items()
        )
        row = sparse_combination(*terms)
        if not data["module"].rational_member(row, basis):
            bad[word] = data["two_cell"].quotient_remainder(row, basis)
    return not bad, len(basis), bad, permanents


def evaluated_columns(data, coordinates, weights):
    cells = data["provenance"].add_weighted_coordinates(
        data["module"],
        data["lifted_base"],
        tuple(zip(coordinates, weights)),
    )
    return data["forced_pair"].insertion_columns(
        data["module"], data["u_set"], cells
    )


def independent_column_labels(module, columns):
    labels = []
    basis = {}
    for label in sorted(columns):
        candidate = module.rational_basis(
            list(basis.values()) + [columns[label]]
        )
        if len(candidate) > len(basis):
            labels.append(label)
            basis = candidate
    return tuple(labels), basis


def poly_vector_add(table, monomial, vector):
    for coordinate, coefficient in vector.items():
        polynomial = table.setdefault(coordinate, {})
        polynomial[monomial] = polynomial.get(monomial, Q(0)) + coefficient
        if not polynomial[monomial]:
            polynomial.pop(monomial)
        if not polynomial:
            table.pop(coordinate)


def raw_polynomial_data(data, support):
    """Literal column/residual polynomials in one variable per support cell."""
    variable_count = len(support)
    zero_monomial = (0,) * variable_count
    columns = {
        label: {} for label in data["base_columns"]
    }
    for label, vector in data["base_columns"].items():
        poly_vector_add(columns[label], zero_monomial, vector)
    for index, coordinate in enumerate(support):
        monomial = tuple(1 if j == index else 0 for j in range(variable_count))
        for label, vector in data["linear_directions"][coordinate].items():
            poly_vector_add(columns[label], monomial, vector)

    residual = {word: {} for word in data["residual_rows"]}
    for word, vector in data["residual_rows"].items():
        poly_vector_add(residual[word], zero_monomial, vector)

    raw_grade_cache = {}
    for left_index, right_index in combinations(range(variable_count), 2):
        left = support[left_index]
        right = support[right_index]
        grade_index = grade_for_coordinates(data, left, right)
        if grade_index is None:
            continue
        monomial = tuple(
            1 if j in (left_index, right_index) else 0
            for j in range(variable_count)
        )
        if grade_index not in raw_grade_cache:
            components = data["grade_data"][grade_index][4]
            grade_rows = data["grade_data"][grade_index][5]
            raw_grade_cache[grade_index] = components, grade_rows
        components, grade_rows = raw_grade_cache[grade_index]
        for label, vector in components.items():
            poly_vector_add(columns[label], monomial, vector)
        for word, vector in grade_rows.items():
            residual.setdefault(word, {})
            poly_vector_add(residual[word], monomial, vector)
    return columns, residual


def polynomial_expression(polynomial, variables):
    if not polynomial:
        return "0"
    terms = []
    for monomial, coefficient in sorted(polynomial.items()):
        factors = []
        if coefficient == -1 and any(monomial):
            factors.append("-1")
        elif coefficient != 1 or not any(monomial):
            factors.append(
                str(coefficient.numerator)
                if coefficient.denominator == 1
                else f"({coefficient.numerator}/{coefficient.denominator})"
            )
        factors.extend(
            variable if exponent == 1 else f"{variable}^{exponent}"
            for variable, exponent in zip(variables, monomial)
            if exponent
        )
        terms.append("*".join(factors) if factors else "1")
    return "+".join(terms).replace("+-", "-")


def parse_factorizations(output, names):
    records = {}
    lines = [line.strip() for line in output.splitlines() if line.strip()]
    index = 0
    while index < len(lines):
        if lines[index] not in names:
            index += 1
            continue
        name = lines[index]
        index += 1
        require(lines[index] == "[1]:", f"missing factor block for {name}")
        index += 1
        factors = []
        while index < len(lines) and lines[index] != "[2]:":
            require("=" in lines[index], f"malformed factor at {name}")
            factors.append(lines[index].split("=", 1)[1])
            index += 1
        require(index < len(lines), f"missing exponent block for {name}")
        index += 1
        exponents = tuple(int(value) for value in lines[index].split(","))
        require(len(factors) == len(exponents), f"factor exponent mismatch at {name}")
        records[name] = tuple(zip(factors, exponents))
        index += 1
    require(set(records) == set(names), "determinant factor record incomplete")
    return records


def singular_determinants(data, support, sample_weights):
    columns_at_sample = evaluated_columns(data, support, sample_weights)
    labels, basis = independent_column_labels(data["module"], columns_at_sample)
    polynomial_columns, polynomial_residual = raw_polynomial_data(data, support)
    pivot_rows = tuple(sorted(basis))
    require(len(labels) == len(pivot_rows), "pivot square changed")
    variables = tuple("abcd"[: len(support)])

    residual_cells = data["provenance"].add_weighted_coordinates(
        data["module"], data["lifted_base"], tuple(zip(support, sample_weights))
    )
    residual_tensor = data["module"].matching_tensor(
        data["provenance"].B10, residual_cells
    )
    residual_tensor = data["forced_pair"].tensor_difference(
        residual_tensor,
        data["forced_pair"].delta_tensor(data["provenance"].B10),
    )
    residual_rows = data["forced_pair"].flatten_rows(
        residual_tensor,
        data["provenance"].B10,
        (CUT, 6, 7),
        data["u_set"],
    )
    bad = {
        word: data["two_cell"].quotient_remainder(vector, basis)
        for word, vector in residual_rows.items()
        if not data["module"].rational_member(vector, basis)
    }

    matrices = []
    base_entries = [
        polynomial_expression(
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
                    polynomial_expression(
                        polynomial_columns[label].get(row, {}), variables
                    )
                )
            entries.append(
                polynomial_expression(
                    polynomial_residual.get(word, {}).get(row, {}), variables
                )
            )
        matrices.append((f"aug{number}", len(labels) + 1, entries))

    lines = [f"ring r=0,({','.join(variables)}),dp;"]
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
    return len(labels), pivot_rows, bad, parse_factorizations(process.stdout, names)


def prepare():
    three_cell = load_three_cell_frontier()
    zero_exclusion = three_cell.load_zero_exclusion()
    rank_one = zero_exclusion.load_rank_one_intersection()
    permanent_kernel = rank_one.load_permanent_kernel()
    provenance = permanent_kernel.load_provenance_cancellation()
    graded_guard = provenance.load_graded_guard()
    multitrace = graded_guard.load_multitrace()
    frontier = multitrace.load_frontier()
    one_cross = frontier.load_one_cross_edge()
    forced_pair = one_cross.load_forced_pair_contraction()
    certificate = forced_pair.load_positive_moduli_certificate()
    two_cell = certificate.load_two_cell_audit()
    one_cell = two_cell.load_one_cell_elimination()
    unit_gate = one_cell.load_unit_gate()
    module = unit_gate.load_three_cut_verifier()
    base = unit_gate.build_base(module)
    unit_gate.audit_base(module, base)
    lifted_base = forced_pair.lift_cells(module, base)

    z = CUT
    u_set = tuple(vertex for vertex in module.S if vertex != z) + (8, 9)
    base_columns = forced_pair.insertion_columns(module, u_set, lifted_base)
    coordinates = frontier.cross_coordinates()
    linear_generators = list(base_columns.values())
    linear_directions = {}
    for coordinate in coordinates:
        cells = provenance.add_weighted_coordinates(
            module, lifted_base, ((coordinate, Q(1)),)
        )
        columns = forced_pair.insertion_columns(module, u_set, cells)
        directions = {
            label: one_cell.sparse_difference(columns[label], base_columns[label])
            for label in base_columns
        }
        linear_directions[coordinate] = directions
        linear_generators.extend(directions.values())
    linear_basis = module.rational_basis(linear_generators)
    require(len(linear_basis) == 126, "linear rank changed")

    base_tensor = module.matching_tensor(provenance.B10, lifted_base)
    residual = forced_pair.tensor_difference(
        base_tensor, forced_pair.delta_tensor(provenance.B10)
    )
    residual_rows = forced_pair.flatten_rows(
        residual, provenance.B10, (z, 6, 7), u_set
    )
    residual_q = quotient_table(residual_rows, linear_basis, two_cell)
    representatives = permanent_kernel.permanent_representatives(
        provenance, frontier
    )
    representative_index = {pair: index for index, pair in enumerate(representatives)}
    coordinate_pair_to_grade = {}
    oriented_pair_to_grade = {}
    grade_data = []
    pure_words = tuple((colour,) * 10 for colour in range(3))
    for index, pair in enumerate(representatives):
        for orientation in (pair, provenance.swap_pair(pair)):
            coordinate_pair_to_grade[frozenset(orientation)] = index
            oriented_pair_to_grade[orientation] = index
        full_grade = provenance.ordered_pair_grade(
            module, base, pair, provenance.B8, (8, 9)
        )
        anchor = tuple(full_grade.get(word, Q(0)) for word in pure_words)
        components = provenance.mixed_column_components(
            frontier, forced_pair, one_cell, module, lifted_base, pair, u_set
        )
        q_basis = module.rational_basis(
            [
                two_cell.quotient_remainder(vector, linear_basis)
                for vector in components.values()
            ]
        )
        full_rows = forced_pair.flatten_rows(
            full_grade, provenance.B10, (z, 6, 7), u_set
        )
        d_rows = quotient_table(full_rows, linear_basis, two_cell)
        grade_data.append(
            (pair, q_basis, d_rows, anchor, components, full_rows)
        )
    require(len(coordinate_pair_to_grade) == 4_536, "oriented pair map changed")

    return {
        "three_cell": three_cell,
        "provenance": provenance,
        "frontier": frontier,
        "forced_pair": forced_pair,
        "two_cell": two_cell,
        "one_cell": one_cell,
        "module": module,
        "base": base,
        "lifted_base": lifted_base,
        "u_set": u_set,
        "base_columns": base_columns,
        "coordinates": coordinates,
        "linear_directions": linear_directions,
        "linear_basis": linear_basis,
        "residual_rows": residual_rows,
        "residual_q": residual_q,
        "representatives": representatives,
        "representative_index": representative_index,
        "coordinate_pair_to_grade": coordinate_pair_to_grade,
        "oriented_pair_to_grade": oriented_pair_to_grade,
        "grade_data": grade_data,
    }


def main() -> None:
    data = prepare()
    grade_data = data["grade_data"]
    signatures = defaultdict(list)
    for index, record in enumerate(grade_data):
        _pair, q_basis, d_rows, anchor = record[:4]
        signatures[(basis_key(q_basis), table_key(d_rows), anchor)].append(index)
    require(len(signatures) == 1805, "individual grade-data signature count changed")
    signature_multiplicities = Counter(map(len, signatures.values()))
    require(
        signature_multiplicities
        == Counter({1: 1770, 9: 25, 8: 4, 54: 2, 27: 2, 53: 1, 26: 1}),
        "individual grade-data signature multiplicities changed",
    )

    by_new = {
        new: tuple(
            coordinate
            for coordinate in data["coordinates"]
            if coordinate[1] == new
        )
        for new in (8, 9)
    }
    left_pairs = tuple(combinations(by_new[8], 2))
    right_pairs = tuple(combinations(by_new[9], 2))
    rectangle_incidence = Counter()
    oriented_map = data["oriented_pair_to_grade"]
    for left_pair in left_pairs:
        for right_pair in right_pairs:
            grades = {
                oriented_map[(left, right)]
                for left in left_pair
                for right in right_pair
                if (left, right) in oriented_map
            }
            rectangle_incidence[len(grades)] += 1
    expected_rectangle_incidence = Counter(
        {4: 3_807_972, 3: 2_204_496, 2: 508_032, 0: 10_368, 1: 2_268}
    )
    require(
        rectangle_incidence == expected_rectangle_incidence,
        "all-rectangle permanent incidence census changed",
    )

    # Forced-pair swap is the only symmetry used here.  It exchanges the
    # 1+3 and 3+1 strata and acts within the 2+2 stratum.
    one_side = len(by_new[8])
    star_supports = one_side * len(tuple(combinations(by_new[9], 3)))
    rectangle_supports = len(left_pairs) * len(right_pairs)
    rectangle_fixed_by_swap = len(left_pairs)
    rectangle_orbits = (rectangle_supports + rectangle_fixed_by_swap) // 2
    zero_grade_orbits = len(tuple(combinations(by_new[8], 4)))
    require(
        (star_supports, rectangle_supports, rectangle_fixed_by_swap, rectangle_orbits)
        == (4_294_080, 6_533_136, 2_556, 3_267_846),
        "four-cell topology orbit census changed",
    )
    require(zero_grade_orbits == 1_028_790, "one-side orbit census changed")
    star_incidence = Counter(
        {
            grade_count: one_side
            * len(tuple(combinations(range(63), grade_count)))
            * len(tuple(combinations(range(9), 3 - grade_count)))
            for grade_count in range(4)
        }
    )
    require(
        star_incidence
        == Counter({3: 2_859_192, 2: 1_265_544, 1: 163_296, 0: 6_048}),
        "star permanent incidence census changed",
    )

    old_nodes = tuple((vertex, colour) for vertex in range(8) for colour in range(3))
    new_colour_pairs = tuple(combinations(range(3), 2))
    structured_rectangles = []
    structured_systems = Counter()
    for left_node in old_nodes:
        for right_node in old_nodes:
            if left_node[0] == right_node[0]:
                continue
            for left_colours in new_colour_pairs:
                for right_colours in new_colour_pairs:
                    support = tuple(
                        (left_node[0], 8, left_node[1], colour)
                        for colour in left_colours
                    ) + tuple(
                        (right_node[0], 9, right_node[1], colour)
                        for colour in right_colours
                    )
                    permanents = support_permanents(
                        data, support, (Q(1),) * 4
                    )
                    require(len(permanents) == 4, "structured rectangle collapsed")
                    system = exact_affine_system(data, tuple(permanents))
                    structured_systems[(system[0], len(system[1]), system[3])] += 1
                    if system[0]:
                        structured_rectangles.append((support, permanents, system))
    structured_orbits = {
        support_orbit_key(support)
        for support, _permanents, _system in structured_rectangles
    }
    expected_structured_systems = Counter(
        {
            (False, 4, 0): 1938,
            (False, 0, 0): 960,
            (False, 0, 20): 396,
            (False, 0, 24): 392,
            (False, 0, 12): 182,
            (False, 0, 8): 154,
            (False, 0, 16): 108,
            (False, 4, 8): 72,
            (False, 4, 12): 70,
            (False, 0, 36): 70,
            (False, 0, 32): 54,
            (False, 1, 0): 48,
            (False, 4, 4): 18,
            (False, 0, 4): 18,
            (False, 0, 28): 18,
            (False, 1, 12): 16,
            (False, 1, 8): 8,
            (True, 4, 0): 6,
            (True, 0, 24): 4,
            (True, 4, 12): 2,
            (True, 0, 36): 2,
        }
    )
    require(
        structured_systems == expected_structured_systems,
        "structured rectangle affine census changed",
    )
    require(len(structured_rectangles) == 14, "affine survivor count changed")
    expected_orbits = (
        ((0, 8, 1, 0), (0, 8, 1, 2), (2, 9, 1, 0), (2, 9, 1, 2)),
        ((0, 8, 1, 0), (0, 8, 1, 2), (3, 9, 1, 0), (3, 9, 1, 2)),
        ((0, 8, 1, 0), (0, 8, 1, 2), (5, 9, 1, 0), (5, 9, 1, 2)),
        ((1, 8, 1, 0), (1, 8, 1, 2), (4, 9, 1, 0), (4, 9, 1, 2)),
        ((3, 8, 1, 0), (3, 8, 1, 2), (5, 9, 1, 0), (5, 9, 1, 2)),
        ((3, 8, 1, 0), (3, 8, 1, 2), (6, 9, 1, 0), (6, 9, 1, 2)),
        ((5, 8, 1, 0), (5, 8, 1, 2), (7, 9, 1, 0), (7, 9, 1, 2)),
    )
    require(tuple(sorted(structured_orbits)) == expected_orbits, "orbit reps changed")

    # Each representative has a square cofactor minor and an augmented
    # residual minor which are the same nonzero torus monomial.  The fourth
    # representative uses the pivot selected on ac=-1; that pivot is in fact
    # monomial on the whole torus, closing the only generic rank-drop divisor.
    expected_aug0 = (
        (("-1", 1), ("a", 3)),
        (("-1", 1), ("a", 9), ("c", 8), ("d", 1)),
        (("-1", 1), ("a", 4), ("c", 3), ("d", 1)),
        (("-1", 1), ("a", 6), ("c", 2), ("d", 4)),
        (("1", 1), ("a", 4), ("c", 3), ("d", 1)),
        (("1", 1), ("a", 3)),
        (("-1", 1), ("a", 3)),
    )
    determinant_records = []
    for orbit_index, support in enumerate(expected_orbits):
        sample = (
            (Q(1), Q(1), Q(-1), Q(1))
            if orbit_index == 3
            else (Q(1), Q(2), Q(3), Q(5))
        )
        rank, _pivots, _bad, factors = singular_determinants(data, support, sample)
        require(rank in (17, 20, 21), "structured orbit rank changed")
        require(factors["base"] == expected_aug0[orbit_index], "base minor changed")
        require(factors["aug0"] == expected_aug0[orbit_index], "augmented minor changed")
        determinant_records.append((rank, factors["aug0"]))
    structured_stars = []
    structured_star_systems = Counter()
    for centre_node in old_nodes:
        for leaf_node in old_nodes:
            if centre_node[0] == leaf_node[0]:
                continue
            for centre_colour in range(3):
                support = ((centre_node[0], 8, centre_node[1], centre_colour),) + tuple(
                    (leaf_node[0], 9, leaf_node[1], colour)
                    for colour in range(3)
                )
                permanents = support_permanents(data, support, (Q(1),) * 4)
                require(len(permanents) == 3, "structured star collapsed")
                system = exact_affine_system(data, tuple(permanents))
                structured_star_systems[(system[0], len(system[1]), system[3])] += 1
                if system[0]:
                    structured_stars.append((support, permanents, system))
    expected_star_systems = Counter(
        {
            (False, 3, 0): 648,
            (False, 0, 0): 324,
            (False, 0, 15): 132,
            (False, 0, 18): 132,
            (False, 0, 9): 62,
            (False, 0, 6): 52,
            (False, 0, 12): 36,
            (False, 3, 6): 24,
            (False, 3, 9): 24,
            (False, 0, 27): 24,
            (False, 0, 24): 18,
            (False, 1, 0): 12,
            (False, 3, 3): 6,
            (False, 0, 3): 6,
            (False, 0, 21): 6,
            (False, 1, 9): 4,
            (False, 1, 6): 2,
        }
    )
    require(structured_star_systems == expected_star_systems, "star census changed")
    require(not structured_stars, "a structured star affine survivor appeared")

    print("N=10 minimal four-cross bounded frontier: exact PASS")
    print("topology orbits: 1+3=4294080; 2+2=3267846; one-side=1028790")
    print(f"rectangle permanent-class incidence: {rectangle_incidence}")
    print(f"star permanent-class incidence: {star_incidence}")
    print("old-node structured stars: 1512 tested; affine survivors: 0")
    print("old-node structured rectangles: 4536 tested; affine survivors: 14")
    print("affine rectangle survivors: 7 forced-pair-swap orbits")
    print(f"literal cut-2 monomial determinant records: {determinant_records}")
    print("literal evaluated-span survivors in the seven orbits: 0")
    print("scope: remaining unstructured four-cell orbits are not exhausted")


if __name__ == "__main__":
    main()
