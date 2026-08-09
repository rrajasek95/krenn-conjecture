#!/usr/bin/env python3
"""Exact source-faithful certificate for all positive-moduli two-cell strata.

The two-cell orbit audit leaves 1,858 rank-one and 15 rank-zero character
families.  This checker treats their arbitrary nonzero complex parameters
symbolically.  It uses coefficient-cylinder superspaces of the literal
cofactor maps, exact affine maximal-minor polynomials, and exact bilinear
projection equations.  No coefficient grid or output-only invariant occurs.
"""

from __future__ import annotations

import importlib.util
from collections import Counter
from fractions import Fraction
from pathlib import Path


Q = Fraction


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def load_two_cell_audit():
    path = Path(__file__).with_name(
        "verify_n8_four_cut_two_cell_orbit_feasibility.py"
    )
    spec = importlib.util.spec_from_file_location("two_cell_audit", path)
    require(spec is not None and spec.loader is not None, "cannot load orbit audit")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def copy_cells(base):
    return {edge: list(entries) for edge, entries in base.items()}


def affine_cells(module, base, fixed, variable, parameter):
    cells = copy_cells(base)
    module.add_sources(cells, ((*fixed, Q(1)),))
    if parameter:
        module.add_sources(cells, ((*variable, Q(parameter)),))
    return cells


def bilinear_cells(module, base, left, right, left_weight, right_weight):
    cells = copy_cells(base)
    if left_weight:
        module.add_sources(cells, ((*left, Q(left_weight)),))
    if right_weight:
        module.add_sources(cells, ((*right, Q(right_weight)),))
    return cells


def sparse_evaluate(one_cell, constant, linear, parameter):
    return one_cell.sparse_linear_combination((1, constant), (parameter, linear))


def sparse_bilinear_evaluate(one_cell, components, left, right):
    constant, left_part, right_part, mixed_part = components
    return one_cell.sparse_linear_combination(
        (1, constant),
        (left, left_part),
        (right, right_part),
        (left * right, mixed_part),
    )


def bilinear_components(one_cell, value00, value10, value01, value11):
    return (
        value00,
        one_cell.sparse_difference(value10, value00),
        one_cell.sparse_difference(value01, value00),
        one_cell.sparse_linear_combination(
            (1, value11), (-1, value10), (-1, value01), (1, value00)
        ),
    )


def affine_cut_data(one_cell, module, base, fixed, variable, z):
    u_set = tuple(vertex for vertex in module.S if vertex != z)
    c_set = (z, 6, 7)
    cells0 = affine_cells(module, base, fixed, variable, Q(0))
    cells1 = affine_cells(module, base, fixed, variable, Q(1))
    cells2 = affine_cells(module, base, fixed, variable, Q(2))

    columns0 = one_cell.insertion_columns(module, u_set, cells0)
    columns1 = one_cell.insertion_columns(module, u_set, cells1)
    columns2 = one_cell.insertion_columns(module, u_set, cells2)
    derivatives = tuple(
        one_cell.sparse_difference(column1, column0)
        for column0, column1 in zip(columns0, columns1)
    )
    for column0, derivative, column2 in zip(columns0, derivatives, columns2):
        require(
            sparse_evaluate(one_cell, column0, derivative, Q(2)) == column2,
            f"cofactor column is not affine at {(fixed, variable, z)}",
        )

    row_tables = tuple(
        module.flatten_rows(one_cell.residual_tensor(module, cells), c_set, u_set)
        for cells in (cells0, cells1, cells2)
    )
    words = tuple(sorted(set().union(*(set(rows) for rows in row_tables))))
    rows0 = {word: row_tables[0].get(word, {}) for word in words}
    row_derivatives = {
        word: one_cell.sparse_difference(
            row_tables[1].get(word, {}), row_tables[0].get(word, {})
        )
        for word in words
    }
    for word in words:
        require(
            sparse_evaluate(
                one_cell, rows0[word], row_derivatives[word], Q(2)
            )
            == row_tables[2].get(word, {}),
            f"residual row is not affine at {(fixed, variable, z, word)}",
        )
    return {
        "u_set": u_set,
        "c_set": c_set,
        "columns0": columns0,
        "column_derivatives": derivatives,
        "rows0": rows0,
        "row_derivatives": row_derivatives,
        "words": words,
    }


def impose_affine_vector_equation(one_cell, current, constant, linear):
    """Intersect current with the solutions of constant + t*linear = 0."""
    if current is False:
        return False
    if not linear:
        return current if not constant else False
    pivot = min(linear)
    candidate = -constant.get(pivot, Q(0)) / linear[pivot]
    if one_cell.sparse_linear_combination((1, constant), (candidate, linear)):
        return False
    if current is None:
        return candidate
    return current if current == candidate else False


def affine_universal_constraint(
    one_cell, two_cell, module, base, fixed, variable, cuts
):
    candidate = None
    ranks = []
    for z in cuts:
        data = affine_cut_data(one_cell, module, base, fixed, variable, z)
        universal_basis = module.rational_basis(
            list(data["columns0"]) + list(data["column_derivatives"])
        )
        ranks.append(len(universal_basis))
        for word in data["words"]:
            constant = two_cell.quotient_remainder(
                data["rows0"][word], universal_basis
            )
            linear = two_cell.quotient_remainder(
                data["row_derivatives"][word], universal_basis
            )
            candidate = impose_affine_vector_equation(
                one_cell, candidate, constant, linear
            )
            if candidate is False:
                return False, tuple(ranks)
    return candidate, tuple(ranks)


def independent_column_indices(module, columns):
    selected = []
    basis = {}
    for index, column in enumerate(columns):
        if module.rational_member(column, basis):
            continue
        selected.append(index)
        basis = module.rational_basis([columns[i] for i in selected])
    return tuple(selected), basis


def rational_determinant(matrix):
    matrix = [[Q(value) for value in row] for row in matrix]
    size = len(matrix)
    require(all(len(row) == size for row in matrix), "determinant is not square")
    sign = 1
    determinant = Q(1)
    for column in range(size):
        pivot = next(
            (row for row in range(column, size) if matrix[row][column]), None
        )
        if pivot is None:
            return Q(0)
        if pivot != column:
            matrix[column], matrix[pivot] = matrix[pivot], matrix[column]
            sign = -sign
        pivot_value = matrix[column][column]
        determinant *= pivot_value
        for row in range(column + 1, size):
            if not matrix[row][column]:
                continue
            multiplier = matrix[row][column] / pivot_value
            for index in range(column + 1, size):
                matrix[row][index] -= multiplier * matrix[column][index]
    return sign * determinant


def polynomial_trim(polynomial):
    polynomial = list(polynomial)
    while polynomial and not polynomial[-1]:
        polynomial.pop()
    return tuple(polynomial)


def polynomial_add(left, right):
    answer = [Q(0)] * max(len(left), len(right))
    for index, value in enumerate(left):
        answer[index] += value
    for index, value in enumerate(right):
        answer[index] += value
    return polynomial_trim(answer)


def polynomial_scale(polynomial, scalar):
    if not scalar:
        return ()
    return polynomial_trim(Q(scalar) * value for value in polynomial)


def polynomial_multiply(left, right):
    if not left or not right:
        return ()
    answer = [Q(0)] * (len(left) + len(right) - 1)
    for left_index, left_value in enumerate(left):
        for right_index, right_value in enumerate(right):
            answer[left_index + right_index] += left_value * right_value
    return polynomial_trim(answer)


def polynomial_evaluate(polynomial, value):
    answer = Q(0)
    for coefficient in reversed(polynomial):
        answer = answer * value + coefficient
    return answer


def interpolate_at_consecutive_integers(values):
    answer = ()
    for index, value in enumerate(values):
        basis = (Q(1),)
        denominator = Q(1)
        for other in range(len(values)):
            if other == index:
                continue
            basis = polynomial_multiply(basis, (-Q(other), Q(1)))
            denominator *= index - other
        answer = polynomial_add(answer, polynomial_scale(basis, value / denominator))
    return answer


def polynomial_divmod(dividend, divisor):
    require(bool(divisor), "polynomial division by zero")
    remainder = list(polynomial_trim(dividend))
    quotient = [Q(0)] * max(0, len(remainder) - len(divisor) + 1)
    while remainder and len(remainder) >= len(divisor):
        coefficient = remainder[-1] / divisor[-1]
        shift = len(remainder) - len(divisor)
        quotient[shift] = coefficient
        for index, value in enumerate(divisor):
            remainder[shift + index] -= coefficient * value
        remainder = list(polynomial_trim(remainder))
    return polynomial_trim(quotient), polynomial_trim(remainder)


def polynomial_gcd(left, right):
    while right:
        _quotient, remainder = polynomial_divmod(left, right)
        left, right = right, remainder
    if not left:
        return ()
    return polynomial_scale(left, Q(1) / left[-1])


def determinant_witness_polynomial(one_cell, data, selected, word, pivot_rows):
    matrix_size = len(selected) + 1

    def value_at(parameter):
        vectors = [
            sparse_evaluate(
                one_cell,
                data["columns0"][index],
                data["column_derivatives"][index],
                Q(parameter),
            )
            for index in selected
        ]
        vectors.append(
            sparse_evaluate(
                one_cell,
                data["rows0"][word],
                data["row_derivatives"][word],
                Q(parameter),
            )
        )
        return rational_determinant(
            [
                [vector.get(row, Q(0)) for vector in vectors]
                for row in pivot_rows
            ]
        )

    values = tuple(value_at(parameter) for parameter in range(matrix_size + 1))
    polynomial = interpolate_at_consecutive_integers(values)
    require(polynomial, "selected determinant polynomial vanished")
    require(
        polynomial_evaluate(polynomial, Q(matrix_size + 1))
        == value_at(matrix_size + 1),
        "determinant interpolation failed its extra-point audit",
    )
    return polynomial


EXCEPTIONAL_GCDS = {
    ((2, 3, 0, 1), (2, 3, 2, 0)): None,
    ((2, 3, 0, 1), (2, 5, 2, 0)): (0, 1),
    ((2, 3, 0, 1), (3, 5, 0, 0)): (0, 0, 0, 0, 0, 1),
    ((2, 3, 1, 0), (2, 5, 1, 0)): (0, 1),
    ((2, 3, 2, 0), (2, 5, 2, 0)): (0, 1),
    ((2, 3, 2, 0), (3, 5, 0, 0)): (0, 0, 0, 0, 0, 1),
    ((2, 3, 2, 2), (3, 5, 2, 0)): (0, 0, 1),
    ((2, 5, 2, 0), (3, 5, 0, 0)): (0, 0, 0, 0, 1),
    ((2, 5, 2, 1), (3, 5, 0, 1)): (0, 0, 0, 0, 1, 1),
    ((2, 5, 2, 2), (3, 5, 0, 2)): (0, 0, 0, 0, 1, 1),
    ((6, 7, 0, 2), (6, 7, 1, 0)): None,
}


def exceptional_minor_gcd(one_cell, module, base, fixed, variable):
    gcd = ()
    witnesses = 0
    for z in (2, 3, 4):
        data = affine_cut_data(one_cell, module, base, fixed, variable, z)
        columns_at_one = tuple(
            sparse_evaluate(one_cell, constant, linear, Q(1))
            for constant, linear in zip(
                data["columns0"], data["column_derivatives"]
            )
        )
        selected, basis = independent_column_indices(module, columns_at_one)
        rank = len(selected)
        if rank < 15:
            require(rank == 14, "unexpected exceptional cofactor rank")
            # Every 15-minor has degree at most 15.  Vanishing at these 16
            # exact values proves the symbolic rank ceiling is fourteen.
            for parameter in range(16):
                columns = [
                    sparse_evaluate(one_cell, constant, linear, Q(parameter))
                    for constant, linear in zip(
                        data["columns0"], data["column_derivatives"]
                    )
                ]
                require(
                    len(module.rational_basis(columns)) <= 14,
                    "rank-fourteen ceiling failed",
                )

        for word in data["words"]:
            row_at_one = sparse_evaluate(
                one_cell,
                data["rows0"][word],
                data["row_derivatives"][word],
                Q(1),
            )
            if module.rational_member(row_at_one, basis):
                continue
            augmented = [columns_at_one[index] for index in selected]
            augmented.append(row_at_one)
            augmented_basis = module.rational_basis(augmented)
            require(len(augmented_basis) == rank + 1, "minor witness lost rank")
            pivot_rows = tuple(sorted(augmented_basis))
            polynomial = determinant_witness_polynomial(
                one_cell, data, selected, word, pivot_rows
            )
            require(
                polynomial_evaluate(polynomial, Q(1)),
                "minor witness vanished at its selection point",
            )
            gcd = polynomial_gcd(gcd, polynomial)
            witnesses += 1
    return gcd, witnesses


def exact_four_cut_event(unit_gate, module, cells):
    tensor = module.matching_tensor(module.B, cells)
    if unit_gate.pure_tuple(module, tensor) != (1, 1, 1):
        return False
    if not all(
        unit_gate.active_complete(module.cut_record(z, cells))
        for z in unit_gate.THREE_CUTS
    ):
        return False
    return any(
        unit_gate.active_complete(module.cut_record(z, cells))
        for z in unit_gate.FOURTH_CUT_CANDIDATES
    )


def audit_rank_one_families(one_cell, two_cell, unit_gate, module, base, records):
    support = one_cell.support_coordinates(base)
    constraints = [
        one_cell.coordinate_character(coordinate) for coordinate in sorted(support)
    ]
    constraints.extend(one_cell.target_characters())
    constraint_basis = module.rational_basis(constraints)
    keys = {
        coordinate: two_cell.projective_key(
            two_cell.quotient_remainder(
                one_cell.coordinate_character(coordinate), constraint_basis
            )
        )
        for coordinate in one_cell.all_coordinates()
        if coordinate not in support
    }

    outcomes = Counter()
    exceptional = []
    singleton_checks = []
    for left, right, quotient_rank in records:
        if quotient_rank != 1:
            continue
        fixed, variable = (right, left) if not keys[left] else (left, right)
        candidate, _ranks = affine_universal_constraint(
            one_cell,
            two_cell,
            module,
            base,
            fixed,
            variable,
            unit_gate.THREE_CUTS,
        )
        if candidate is False:
            outcomes["empty"] += 1
        elif candidate is None:
            outcomes["unconstrained"] += 1
            exceptional.append((fixed, variable))
        elif candidate == 0:
            outcomes["zero"] += 1
        else:
            outcomes[("singleton", candidate)] += 1
            singleton_checks.append((fixed, variable, candidate))

    require(
        outcomes
        == Counter(
            {
                "empty": 1737,
                "zero": 108,
                "unconstrained": 11,
                ("singleton", Q(1)): 2,
            }
        ),
        "rank-one universal-cylinder census changed",
    )
    require(
        set(exceptional) == set(EXCEPTIONAL_GCDS),
        "rank-one exceptional family list changed",
    )
    for fixed, variable, candidate in singleton_checks:
        cells = affine_cells(module, base, fixed, variable, candidate)
        require(
            not exact_four_cut_event(unit_gate, module, cells),
            f"rank-one singleton is a four-cut repair at {(fixed, variable, candidate)}",
        )

    minor_counts = Counter()
    direct_checks = 0
    flat_families = 0
    for fixed, variable in exceptional:
        expected = EXCEPTIONAL_GCDS[(fixed, variable)]
        gcd, witnesses = exceptional_minor_gcd(
            one_cell, module, base, fixed, variable
        )
        if expected is None:
            require(not gcd and witnesses == 0, "flat family gained a fixed-cut minor")
            flat_families += 1
            for z in unit_gate.FOURTH_CUT_CANDIDATES:
                candidate, _ranks = affine_universal_constraint(
                    one_cell,
                    two_cell,
                    module,
                    base,
                    fixed,
                    variable,
                    (z,),
                )
                require(
                    candidate is False,
                    f"flat family can enter fourth cylinder {z}: {(fixed, variable)}",
                )
            continue

        require(gcd == tuple(Q(value) for value in expected), "minor gcd changed")
        require(witnesses > 0, "minor certificate has no witnesses")
        minor_counts[gcd] += 1
        if gcd == (Q(0), Q(0), Q(0), Q(0), Q(1), Q(1)):
            cells = affine_cells(module, base, fixed, variable, Q(-1))
            require(
                not exact_four_cut_event(unit_gate, module, cells),
                f"exceptional root is a four-cut repair at {(fixed, variable)}",
            )
            direct_checks += 1

    require(flat_families == 2, "flat-family count changed")
    require(direct_checks == 2, "exceptional-root check count changed")
    require(sum(minor_counts.values()) == 9, "minor-certified family count changed")
    return outcomes, minor_counts, flat_families, len(singleton_checks) + direct_checks


def normalize_bilinear_equation(coefficients):
    coefficients = tuple(Q(value) for value in coefficients)
    pivot = next((value for value in coefficients if value), None)
    if pivot is None:
        return ()
    return tuple(value / pivot for value in coefficients)


def bilinear_universal_equations(
    one_cell, two_cell, module, base, left, right, cuts
):
    corner_cells = {
        (left_value, right_value): bilinear_cells(
            module, base, left, right, left_value, right_value
        )
        for left_value in (0, 1)
        for right_value in (0, 1)
    }
    equations = set()
    ranks = []
    for z in cuts:
        u_set = tuple(vertex for vertex in module.S if vertex != z)
        c_set = (z, 6, 7)
        columns = {
            corner: one_cell.insertion_columns(module, u_set, cells)
            for corner, cells in corner_cells.items()
        }
        column_components = []
        for index in range(15):
            column_components.extend(
                bilinear_components(
                    one_cell,
                    columns[(0, 0)][index],
                    columns[(1, 0)][index],
                    columns[(0, 1)][index],
                    columns[(1, 1)][index],
                )
            )
        universal_basis = module.rational_basis(column_components)
        ranks.append(len(universal_basis))

        rows = {
            corner: module.flatten_rows(
                one_cell.residual_tensor(module, cells), c_set, u_set
            )
            for corner, cells in corner_cells.items()
        }
        words = set().union(*(set(table) for table in rows.values()))
        for word in words:
            components = bilinear_components(
                one_cell,
                rows[(0, 0)].get(word, {}),
                rows[(1, 0)].get(word, {}),
                rows[(0, 1)].get(word, {}),
                rows[(1, 1)].get(word, {}),
            )
            remainders = tuple(
                two_cell.quotient_remainder(component, universal_basis)
                for component in components
            )
            indices = set().union(*(set(remainder) for remainder in remainders))
            for index in indices:
                equation = normalize_bilinear_equation(
                    tuple(remainder.get(index, Q(0)) for remainder in remainders)
                )
                if equation:
                    equations.add(equation)

        cells23 = bilinear_cells(module, base, left, right, Q(2), Q(3))
        columns23 = one_cell.insertion_columns(module, u_set, cells23)
        for index in range(15):
            components = bilinear_components(
                one_cell,
                columns[(0, 0)][index],
                columns[(1, 0)][index],
                columns[(0, 1)][index],
                columns[(1, 1)][index],
            )
            require(
                sparse_bilinear_evaluate(one_cell, components, Q(2), Q(3))
                == columns23[index],
                f"cofactor column is not bilinear at {(left, right, z)}",
            )
        rows23 = module.flatten_rows(
            one_cell.residual_tensor(module, cells23), c_set, u_set
        )
        for word in set(words) | set(rows23):
            components = bilinear_components(
                one_cell,
                rows[(0, 0)].get(word, {}),
                rows[(1, 0)].get(word, {}),
                rows[(0, 1)].get(word, {}),
                rows[(1, 1)].get(word, {}),
            )
            require(
                sparse_bilinear_evaluate(one_cell, components, Q(2), Q(3))
                == rows23.get(word, {}),
                f"residual row is not bilinear at {(left, right, z, word)}",
            )
    return equations, tuple(ranks)


def audit_rank_zero_families(one_cell, two_cell, module, base, records):
    equation_histogram = Counter()
    family_count = 0
    t_equation = (Q(0), Q(1), Q(0), Q(0))
    for left, right, quotient_rank in records:
        if quotient_rank != 0:
            continue
        equations, ranks = bilinear_universal_equations(
            one_cell, two_cell, module, base, left, right, (2, 3, 4)
        )
        require(t_equation in equations, f"rank-zero family lost t=0 equation")
        require(all(14 <= rank <= 16 for rank in ranks), "bilinear rank changed")
        equation_histogram[len(equations)] += 1
        family_count += 1
    require(family_count == 15, "rank-zero family count changed")
    require(
        equation_histogram == Counter({2: 10, 3: 5}),
        "rank-zero equation histogram changed",
    )
    return family_count, equation_histogram


def main() -> None:
    two_cell = load_two_cell_audit()
    one_cell = two_cell.load_one_cell_elimination()
    unit_gate = one_cell.load_unit_gate()
    module = unit_gate.load_three_cut_verifier()
    base = unit_gate.build_base(module)
    unit_gate.audit_base(module, base)
    records, rank_counts, _histogram = two_cell.build_character_census(
        one_cell, module, base
    )
    require(rank_counts[1] == 1858 and rank_counts[0] == 15, "strata changed")

    outcomes, minor_counts, flat_count, direct_checks = audit_rank_one_families(
        one_cell, two_cell, unit_gate, module, base, records
    )
    rank_zero_count, equation_histogram = audit_rank_zero_families(
        one_cell, two_cell, module, base, records
    )

    print("N=8 positive-moduli four-cylinder certificate: PASS")
    print(
        "rank-one universal projection: "
        f"empty={outcomes['empty']}, boundary-only={outcomes['zero']}, "
        f"singleton-one={outcomes[('singleton', Q(1))]}, "
        f"coefficient-invisible={outcomes['unconstrained']}"
    )
    print(
        "rank-one exceptional closure: "
        f"minor-certified={sum(minor_counts.values())}, flat-fourth-obstructed={flat_count}, "
        f"direct exceptional roots checked={direct_checks}"
    )
    print(
        "rank-zero bilinear projection: "
        f"families={rank_zero_count}, equation-count histogram="
        f"{dict(sorted(equation_histogram.items()))}; all force an added weight to zero"
    )
    print(
        "verdict: all 1,873 positive-dimensional two-cell character families "
        "are excluded for nonzero complex weights"
    )


if __name__ == "__main__":
    main()
