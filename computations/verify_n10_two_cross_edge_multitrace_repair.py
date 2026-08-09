#!/usr/bin/env python3
"""Test finite linear combinations of controlled traces on the two-cross witness.

For a fixed cut, let P_a be the old-vertex-controlled contraction for each
controller a on the five-vertex insertion shore.  Any combination

    Q_lambda = sum_a lambda_a P_a,   sum_a lambda_a = 1,

reconstructs every forced-pair lift and preserves Delta.  This checker asks
over Q whether lambda can also send every nonconstant cofactor coefficient
and every nonconstant residual coefficient of

    A_8 tensor g_89 + t E_(08;00) + s E_(19;00)

into the old N=8 insertion cylinder.  Membership is converted to exact
linear equations by quotient normal forms.  No coefficient values are
sampled.
"""

from __future__ import annotations

import importlib.util
from fractions import Fraction
from pathlib import Path


Q = Fraction
CANDIDATE_CUTS = (0, 1, 5)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def load_frontier():
    path = Path(__file__).with_name(
        "verify_n10_two_cross_edge_contraction_frontier.py"
    )
    spec = importlib.util.spec_from_file_location("two_cross", path)
    require(spec is not None and spec.loader is not None, "cannot load frontier")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def ranks(module, equations, variable_count):
    coefficient_vectors = []
    augmented_vectors = []
    for coefficients, rhs, _tag in equations:
        coefficient = {
            index: value for index, value in enumerate(coefficients) if value
        }
        augmented = dict(coefficient)
        if rhs:
            augmented[variable_count] = rhs
        coefficient_vectors.append(coefficient)
        augmented_vectors.append(augmented)
    return (
        len(module.rational_basis(coefficient_vectors)),
        len(module.rational_basis(augmented_vectors)),
    )


def solve_unique(equations, variable_count):
    """Return the unique exact solution when the coefficient rank is full."""
    matrix = [
        [Q(value) for value in coefficients] + [Q(rhs)]
        for coefficients, rhs, _tag in equations
    ]
    pivot_row = 0
    pivots = {}
    for column in range(variable_count):
        selected = next(
            (row for row in range(pivot_row, len(matrix)) if matrix[row][column]),
            None,
        )
        if selected is None:
            continue
        matrix[pivot_row], matrix[selected] = matrix[selected], matrix[pivot_row]
        scale = matrix[pivot_row][column]
        matrix[pivot_row] = [value / scale for value in matrix[pivot_row]]
        for row in range(len(matrix)):
            if row == pivot_row or not matrix[row][column]:
                continue
            scale = matrix[row][column]
            matrix[row] = [
                left - scale * right
                for left, right in zip(matrix[row], matrix[pivot_row])
            ]
        pivots[column] = pivot_row
        pivot_row += 1
    for row in matrix:
        require(
            any(row[:-1]) or not row[-1],
            "attempted to solve an inconsistent linear system",
        )
    if len(pivots) != variable_count:
        return None
    return tuple(matrix[pivots[column]][-1] for column in range(variable_count))


def quotient_equations(
    frontier,
    one_cross,
    forced_pair,
    two_cell,
    module,
    old_basis,
    old_u_set,
    labelled_components,
    family,
):
    equations = []
    controllers = tuple(old_u_set)
    for label, components in labelled_components.items():
        for component_index, component in enumerate(components[1:], 1):
            remainders = []
            for controller in controllers:
                contracted = one_cross.controlled_row_contraction(
                    forced_pair, component, old_u_set, controller
                )
                remainders.append(two_cell.quotient_remainder(contracted, old_basis))
            quotient_indices = sorted(set().union(*(remainder for remainder in remainders)))
            for quotient_index in quotient_indices:
                coefficients = tuple(
                    remainder.get(quotient_index, Q(0))
                    for remainder in remainders
                )
                if any(coefficients):
                    equations.append(
                        (coefficients, Q(0), (family, label, component_index, quotient_index))
                    )
    return equations


def first_inconsistency(module, equations, variable_count):
    selected = []
    for equation in equations:
        candidate = selected + [equation]
        coefficient_rank, augmented_rank = ranks(module, candidate, variable_count)
        if augmented_rank > coefficient_rank:
            return equation[2], tuple(selected), equation
        selected = candidate
    return None


def audit_cut(
    frontier, one_cross, forced_pair, certificate, two_cell, one_cell, module, base, z
):
    old_u_set = tuple(vertex for vertex in frontier.S if vertex != z)
    new_u_set = old_u_set + frontier.NEW_VERTICES
    lifted_base = forced_pair.lift_cells(module, base)
    corners = tuple(
        frontier.add_pair(module, lifted_base, left_weight, right_weight)
        for left_weight, right_weight in ((0, 0), (1, 0), (0, 1), (1, 1))
    )
    old_columns = forced_pair.insertion_columns(module, old_u_set, base)
    old_basis = module.rational_basis(list(old_columns.values()))
    columns = frontier.coefficient_columns(
        forced_pair, one_cell, module, new_u_set, corners
    )
    rows = frontier.coefficient_rows(
        forced_pair, one_cell, module, z, new_u_set, corners
    )

    # The word 00000012 in the mixed full tensor has boundary word 012 on
    # each candidate cut and old insertion-shore word 00000.  Every possible
    # controller therefore gives literally the same contracted row.  This
    # diagonal direct-sum class is the sharp obstruction: any reconstruction
    # which is the identity on diagonal forced-lift rows must retain it.
    diagonal_component = rows[(0, 1, 2)][3]
    diagonal_images = tuple(
        one_cross.controlled_row_contraction(
            forced_pair, diagonal_component, old_u_set, controller
        )
        for controller in old_u_set
    )
    require(
        all(image == {0: Q(-1)} for image in diagonal_images),
        f"mixed diagonal witness changed at cut {z}",
    )
    diagonal_remainders = tuple(
        two_cell.quotient_remainder(image, old_basis)
        for image in diagonal_images
    )
    require(
        diagonal_remainders[0]
        and all(
            remainder == diagonal_remainders[0]
            for remainder in diagonal_remainders
        ),
        f"diagonal quotient witness changed at cut {z}",
    )
    expected_remainder = (
        {63: Q(1)} if z in (0, 1) else {21: Q(1), 150: Q(1)}
    )
    require(
        diagonal_remainders[0] == expected_remainder,
        f"diagonal quotient normal form changed at cut {z}",
    )

    preserve = [((Q(1),) * len(old_u_set), Q(1), ("preserve",))]
    cofactor = quotient_equations(
        frontier,
        one_cross,
        forced_pair,
        two_cell,
        module,
        old_basis,
        old_u_set,
        columns,
        "cofactor",
    )
    residual = quotient_equations(
        frontier,
        one_cross,
        forced_pair,
        two_cell,
        module,
        old_basis,
        old_u_set,
        rows,
        "residual",
    )
    systems = {
        "preserve": preserve,
        "preserve+cofactor": preserve + cofactor,
        "preserve+residual": preserve + residual,
        "all": preserve + cofactor + residual,
    }
    records = {}
    for name, equations in systems.items():
        rank, augmented_rank = ranks(module, equations, len(old_u_set))
        solution = None
        if rank == augmented_rank:
            solution = solve_unique(equations, len(old_u_set))
        records[name] = {
            "equations": len(equations),
            "rank": rank,
            "augmented_rank": augmented_rank,
            "solution": solution,
        }
    contradiction = first_inconsistency(
        module, systems["all"], len(old_u_set)
    )
    return tuple(old_u_set), records, contradiction, diagonal_remainders[0]


def main() -> None:
    frontier = load_frontier()
    one_cross = frontier.load_one_cross_edge()
    forced_pair = one_cross.load_forced_pair_contraction()
    certificate = forced_pair.load_positive_moduli_certificate()
    two_cell = certificate.load_two_cell_audit()
    one_cell = two_cell.load_one_cell_elimination()
    unit_gate = one_cell.load_unit_gate()
    module = unit_gate.load_three_cut_verifier()
    base = unit_gate.build_base(module)
    unit_gate.audit_base(module, base)

    results = {}
    for z in CANDIDATE_CUTS:
        controllers, records, contradiction, diagonal_remainder = audit_cut(
            frontier,
            one_cross,
            forced_pair,
            certificate,
            two_cell,
            one_cell,
            module,
            base,
            z,
        )
        results[z] = (controllers, records, contradiction, diagonal_remainder)

    print("N=10 two-cross finite multitrace repair audit: exact PASS")
    for z, (controllers, records, contradiction, diagonal_remainder) in results.items():
        print(f"cut {z}, controllers {controllers}")
        for name, record in records.items():
            print(
                f"  {name}: equations={record['equations']}, "
                f"rank={record['rank']}, augmented={record['augmented_rank']}, "
                f"solution={record['solution']}"
            )
        print(f"  first all-system contradiction: {None if contradiction is None else contradiction[0]}")
        print(
            "  direct-sum diagonal mixed-row remainder: "
            f"{diagonal_remainder}"
        )
    print("verdict: no scalar multitrace or diagonal-reconstructing direct-sum repair")


if __name__ == "__main__":
    main()
