#!/usr/bin/env python3
"""Exact fixed-old-source frontier for arbitrary N=10 cross additions.

The anchored N=8 source is lifted by the forced diagonal pair (8,9), and
all 144 old--new coloured cross coordinates are allowed.  This checker
combines the permanent-image and permanent-zero audits at the ordinary
coefficient-cylinder level.  On fixed cut 2 it proves:

* zero symmetrized permanent data cannot complete the cylinder;
* one nonzero permanent class cannot complete it, even after all 144 linear
  cofactor directions are allowed independently; and
* two nonzero classes sharing a cross coordinate cannot complete it, even
  in the same universal linear superspace.

Consequently every cross addition supported on at most three cells is
excluded.  The checker also shows why this finite calculation does not close
arbitrary support: allowing all 2,268 quadratic cofactor directions makes
the cut-2 residual lie in the resulting superspace.  The remaining problem
is therefore a coupled nonlinear permanent-image/cylinder-span implication,
not another linear separation.
"""

from __future__ import annotations

import importlib.util
from collections import Counter
from fractions import Fraction
from pathlib import Path


Q = Fraction
CUT = 2


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def load_zero_exclusion():
    path = Path(__file__).with_name(
        "verify_n10_permanent_zero_cross_linear_superspace_exclusion.py"
    )
    spec = importlib.util.spec_from_file_location("zero_exclusion", path)
    require(spec is not None and spec.loader is not None, "cannot load zero audit")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def quotient_coordinates(vector, basis, two_cell):
    return two_cell.quotient_remainder(vector, basis)


def row_quotients(rows, basis, two_cell):
    return {
        word: quotient_coordinates(row, basis, two_cell)
        for word, row in rows.items()
    }


def scalar_system_has_solution(constant_rows, direction_rows):
    """Solve q0 + p*q1 = 0 exactly; return (feasible, forced p or None)."""
    forced = None
    for word in set(constant_rows) | set(direction_rows):
        constant = constant_rows.get(word, {})
        direction = direction_rows.get(word, {})
        coordinates = set(constant) | set(direction)
        for coordinate in coordinates:
            a = constant.get(coordinate, Q(0))
            b = direction.get(coordinate, Q(0))
            if not b:
                if a:
                    return False, None
                continue
            value = -a / b
            if forced is None:
                forced = value
            elif forced != value:
                return False, None
    return True, forced


def two_scalar_system(constant_rows, left_rows, right_rows, extra_equations=()):
    """Solve q0 + a*q1 + b*q2 = 0 by exact rational row reduction.

    Return consistency, rank, one solution, and whether both variables can
    be nonzero.  A free solution entry is ``None``.
    """
    equations = []
    for word in set(constant_rows) | set(left_rows) | set(right_rows):
        constant = constant_rows.get(word, {})
        left = left_rows.get(word, {})
        right = right_rows.get(word, {})
        for coordinate in set(constant) | set(left) | set(right):
            equations.append(
                [
                    left.get(coordinate, Q(0)),
                    right.get(coordinate, Q(0)),
                    -constant.get(coordinate, Q(0)),
                ]
            )
    equations.extend(
        [Q(left), Q(right), Q(value)]
        for left, right, value in extra_equations
    )
    pivots = []
    row_index = 0
    for column in range(2):
        pivot = next(
            (index for index in range(row_index, len(equations)) if equations[index][column]),
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
                row[j] - factor * equations[row_index][j] for j in range(3)
            ]
        pivots.append(column)
        row_index += 1
    if any(not row[0] and not row[1] and row[2] for row in equations):
        return False, len(pivots), None, False
    solution = [None, None]
    for index, column in enumerate(pivots):
        # This value is a particular solution with all free variables zero.
        solution[column] = equations[index][2]
    if len(pivots) == 2:
        both_nonzero = bool(solution[0] and solution[1])
    elif len(pivots) == 1:
        pivot = pivots[0]
        free = 1 - pivot
        pivot_row = equations[0]
        # x_pivot = rhs - alpha*x_free.  Both variables can be nonzero
        # unless this row literally forces x_pivot=0.
        both_nonzero = bool(pivot_row[2] or pivot_row[free])
    else:
        both_nonzero = True
    return True, len(pivots), tuple(solution), both_nonzero


def orientations(provenance, representative):
    return representative, provenance.swap_pair(representative)


def sharing_grade_pairs(provenance, representatives):
    """All permanent-class pairs realizable by a three-cell cross support."""
    coordinate_to_grades = {}
    for grade_index, representative in enumerate(representatives):
        coordinates = {
            coordinate
            for pair in orientations(provenance, representative)
            for coordinate in pair
        }
        for coordinate in coordinates:
            coordinate_to_grades.setdefault(coordinate, []).append(grade_index)
    pairs = set()
    for grade_indices in coordinate_to_grades.values():
        for left_index, left in enumerate(grade_indices):
            for right in grade_indices[left_index + 1 :]:
                if left != right:
                    pairs.add(tuple(sorted((left, right))))
    return tuple(sorted(pairs))


def main() -> None:
    zero_exclusion = load_zero_exclusion()
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

    base_tensor = module.matching_tensor(provenance.B10, lifted_base)
    residual = forced_pair.tensor_difference(
        base_tensor, forced_pair.delta_tensor(provenance.B10)
    )
    z = CUT
    u_set = tuple(vertex for vertex in module.S if vertex != z) + (8, 9)
    base_columns = forced_pair.insertion_columns(module, u_set, lifted_base)
    universal_linear_generators = list(base_columns.values())
    coordinates = frontier.cross_coordinates()
    require(len(coordinates) == 144, "cross-coordinate census changed")
    for coordinate in coordinates:
        cells = provenance.add_weighted_coordinates(
            module, lifted_base, ((coordinate, Q(1)),)
        )
        columns = forced_pair.insertion_columns(module, u_set, cells)
        universal_linear_generators.extend(
            one_cell.sparse_difference(columns[label], base_columns[label])
            for label in base_columns
        )
    linear_basis = module.rational_basis(universal_linear_generators)
    require(len(linear_basis) == 126, "cut-2 universal linear rank changed")

    residual_rows = forced_pair.flatten_rows(
        residual, provenance.B10, (z, 6, 7), u_set
    )
    residual_quotients = row_quotients(residual_rows, linear_basis, two_cell)
    bad_residual = {
        word: remainder for word, remainder in residual_quotients.items() if remainder
    }
    require(
        bad_residual == {(1, 1, 1): {1089: Q(1), 1097: Q(1)}},
        "cut-2 universal linear residual changed",
    )

    representatives = permanent_kernel.permanent_representatives(
        provenance, frontier
    )
    require(len(representatives) == 2_268, "permanent class census changed")
    pure_words = tuple((colour,) * 10 for colour in range(3))
    grade_data = []
    anchor_changing = []
    for pair in representatives:
        full_grade = provenance.ordered_pair_grade(
            module, base, pair, provenance.B8, (8, 9)
        )
        anchor_change = tuple(full_grade.get(word, Q(0)) for word in pure_words)
        if any(anchor_change):
            anchor_changing.append((pair, anchor_change))
        components = provenance.mixed_column_components(
            frontier, forced_pair, one_cell, module, lifted_base, pair, u_set
        )
        quadratic_quotients = [
            quotient_coordinates(component, linear_basis, two_cell)
            for component in components.values()
        ]
        quadratic_basis = module.rational_basis(quadratic_quotients)
        full_rows = forced_pair.flatten_rows(
            full_grade, provenance.B10, (z, 6, 7), u_set
        )
        full_quotient_rows = row_quotients(full_rows, linear_basis, two_cell)
        grade_data.append(
            (pair, quadratic_basis, full_quotient_rows, anchor_change)
        )
    require(len(anchor_changing) == 13, "anchor-changing class count changed")
    require(len(grade_data) == 2_268, "full permanent class data count changed")
    preserving_grade_data = tuple(
        record for record in grade_data if not any(record[3])
    )
    require(
        len(preserving_grade_data) == 2_255,
        "anchor-preserving class count changed",
    )

    # A single nonzero permanent class cannot absorb the residual, even when
    # every possible linear cross direction is granted independently.
    one_class_ranks = Counter()
    one_class_survivors = []
    for pair, quadratic_basis, full_rows, _anchor_change in preserving_grade_data:
        basis = quadratic_basis
        one_class_ranks[len(linear_basis) + len(basis)] += 1
        constant_rows = row_quotients(residual_quotients, basis, two_cell)
        direction_rows = row_quotients(full_rows, basis, two_cell)
        feasible, coefficient = scalar_system_has_solution(
            constant_rows, direction_rows
        )
        # ``None`` means the quotient equation is identically zero, so every
        # nonzero coefficient is a necessary survivor.
        if feasible and (coefficient is None or coefficient != Q(0)):
            one_class_survivors.append((pair, coefficient))
    require(not one_class_survivors, "a one-class nonzero source survived cut 2")
    require(
        one_class_ranks
        == Counter(
            {
                126: 1467,
                131: 198,
                132: 198,
                129: 132,
                128: 116,
                130: 54,
                135: 36,
                134: 27,
                127: 18,
                133: 9,
            }
        ),
        "one-class enlarged-rank histogram changed",
    )

    # Every genuine three-cell source with two nonzero grades produces two
    # swap-symmetrized permanent classes sharing one literal coordinate.
    all_representatives = tuple(record[0] for record in grade_data)
    grade_index = {pair: index for index, pair in enumerate(all_representatives)}
    sharing_pairs = sharing_grade_pairs(provenance, all_representatives)
    require(len(sharing_pairs) == 231_336, "sharing class-pair census changed")
    three_cell_survivors = []
    two_class_ranks = Counter()
    for left_index, right_index in sharing_pairs:
        left_pair, left_quadratic, left_full_rows, left_anchor = grade_data[
            left_index
        ]
        right_pair, right_quadratic, right_full_rows, right_anchor = grade_data[
            right_index
        ]
        # The index dictionary is an internal consistency guard: grade_data
        # and all_representatives must have identical order.
        require(
            grade_index[left_pair] == left_index
            and grade_index[right_pair] == right_index,
            "permanent grade index changed",
        )
        basis = module.rational_basis(
            list(left_quadratic.values()) + list(right_quadratic.values())
        )
        two_class_ranks[len(linear_basis) + len(basis)] += 1
        constant_rows = row_quotients(residual_quotients, basis, two_cell)
        left_rows = row_quotients(left_full_rows, basis, two_cell)
        right_rows = row_quotients(right_full_rows, basis, two_cell)
        feasible, rank, solution, both_nonzero = two_scalar_system(
            constant_rows,
            left_rows,
            right_rows,
            tuple(
                (left_anchor[index], right_anchor[index], Q(0))
                for index in range(3)
            ),
        )
        if feasible and both_nonzero:
            three_cell_survivors.append(
                (left_pair, right_pair, rank, solution)
            )
    require(
        not three_cell_survivors,
        "a sharing two-class/three-cell necessary survivor appeared",
    )
    require(
        two_class_ranks
        == Counter(
            {
                126: 113922,
                131: 21825,
                132: 21348,
                129: 12834,
                128: 10836,
                135: 8568,
                134: 8568,
                130: 6768,
                137: 6300,
                136: 5256,
                133: 4851,
                138: 4248,
                127: 1710,
                140: 1566,
                141: 1143,
                139: 972,
                143: 270,
                144: 252,
                142: 99,
            }
        ),
        "sharing two-class enlarged-rank histogram changed",
    )

    # Linear separation genuinely stops at larger support.  Grant all
    # permanent quadratic cofactor directions independently and verify that
    # the old residual is absorbed already on cut 2.
    all_quadratic_generators = []
    for _pair, quadratic_basis, _full_rows, _anchor_change in grade_data:
        all_quadratic_generators.extend(quadratic_basis.values())
    all_quadratic_basis = module.rational_basis(all_quadratic_generators)
    require(
        len(linear_basis) + len(all_quadratic_basis) == 1224,
        "full quadratic cut-2 rank changed",
    )
    require(
        all(
            module.rational_member(row, all_quadratic_basis)
            for row in residual_quotients.values()
        ),
        "full quadratic superspace did not absorb the cut-2 residual",
    )

    print("N=10 fixed-old arbitrary-cross frontier: exact PASS")
    print("fixed cut audited: 2")
    print("cross coordinates: 144; permanent classes: 2268")
    print("anchor-changing classes: 13; anchor-preserving classes: 2255")
    print("universal all-linear rank: 126")
    print(f"one-class enlarged-rank histogram: {one_class_ranks}")
    print("one nonzero permanent class survivors: 0")
    print(f"sharing two-class systems tested: {len(sharing_pairs)}")
    print(f"sharing two-class rank histogram: {two_class_ranks}")
    print("sharing two-class/three-cell survivors: 0")
    print(
        "source-level corollary: every support of at most three cross cells is excluded"
    )
    print(
        f"all-quadratic universal rank: {len(linear_basis) + len(all_quadratic_basis)}"
    )
    print("all-quadratic superspace absorbs every cut-2 residual row")
    print(
        "stopping rule: arbitrary support requires coupled nonlinear rank conditions"
    )
    print("scope: fixed anchored old source; this is not a Krenn counterexample")


if __name__ == "__main__":
    main()
