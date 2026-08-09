#!/usr/bin/env python3
"""Exact source-graded four-point guard for the explicit two-cross witness.

The ordinary output tensor forgets whether a coefficient came from the
forced-pair lift or from the ordered cross pair

    (0,8;00), (1,9;00).

Retain the latter source provenance before output summation as the six-site
cofactor K = H_{2,3,4,5,6,7}.  Inserting colours zero at old endpoints 0,1
recovers the mixed ``ts`` output coefficient exactly.  Its boundary-012 row
is -e_00000 on every adjacent cut.  Exact old-cylinder normal forms show
that this row belongs to the fixed cuts 2,3,4 and to none of 0,1,5.  Thus
each fixed-three-plus-candidate graded four-cut system forces ts=0.

The checker also verifies forced-pair stability: after adjoining another
diagonal old pair, the eight-site provenance cofactor contracts exactly to
K, its guarded row contracts to the same row, and the ordinary summand and
Delta contract through N=12 -> N=10 -> N=8.
"""

from __future__ import annotations

import importlib.util
from fractions import Fraction
from pathlib import Path


Q = Fraction
B8 = tuple(range(8))
B10 = tuple(range(10))
B12 = tuple(range(12))
ENDPOINTS = (0, 1)
GRADE_VERTICES8 = tuple(range(2, 8))
GRADE_VERTICES10 = tuple(range(2, 10))
FIXED_CUTS = (2, 3, 4)
CANDIDATE_CUTS = (0, 1, 5)
BOUNDARY_WORD = (0, 1, 2)
GUARD_ROW = {0: Q(-1)}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def load_multitrace():
    path = Path(__file__).with_name(
        "verify_n10_two_cross_edge_multitrace_repair.py"
    )
    spec = importlib.util.spec_from_file_location("multitrace", path)
    require(spec is not None and spec.loader is not None, "cannot load multitrace audit")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def insert_endpoint_colours(grade, vertices, endpoints=ENDPOINTS):
    remaining = tuple(vertex for vertex in vertices if vertex not in endpoints)
    answer = {}
    for grade_word, coefficient in grade.items():
        assignment = {endpoints[0]: 0, endpoints[1]: 0}
        assignment.update(zip(remaining, grade_word))
        word = tuple(assignment[vertex] for vertex in vertices)
        answer[word] = answer.get(word, Q(0)) + coefficient
        if not answer[word]:
            answer.pop(word)
    return answer


def tensor_diagonal_pair(grade):
    return {
        word + (colour, colour): coefficient
        for word, coefficient in grade.items()
        for colour in range(3)
    }


def controlled_last_pair_contraction(tensor, controller_position):
    answer = {}
    for word, coefficient in tensor.items():
        if word[-2] != word[-1] or word[-1] != word[controller_position]:
            continue
        old_word = word[:-2]
        answer[old_word] = answer.get(old_word, Q(0)) + coefficient
        if not answer[old_word]:
            answer.pop(old_word)
    return answer


def add_diagonal_pair(module, cells, left, right):
    answer = {edge: list(entries) for edge, entries in cells.items()}
    module.add_sources(
        answer,
        tuple((left, right, colour, colour, Q(1)) for colour in range(3)),
    )
    return answer


def cut_guard_data(
    forced_pair, two_cell, module, base, inserted_grade, z
):
    old_u_set = tuple(vertex for vertex in module.S if vertex != z)
    c_set = (z, 6, 7)
    rows = forced_pair.flatten_rows(inserted_grade, B8, c_set, old_u_set)
    guard_row = rows.get(BOUNDARY_WORD, {})
    require(guard_row == GUARD_ROW, f"source-grade guard row changed at cut {z}")
    old_columns = forced_pair.insertion_columns(module, old_u_set, base)
    old_basis = module.rational_basis(list(old_columns.values()))
    remainder = two_cell.quotient_remainder(guard_row, old_basis)
    return old_u_set, old_columns, old_basis, remainder


def main() -> None:
    multitrace = load_multitrace()
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

    # The ordered-pair source grade is retained before inserting the two old
    # endpoint colours and before summing it into the ordinary output tensor.
    grade6 = module.matching_tensor(GRADE_VERTICES8, base)
    require(
        grade6
        == {
            (2, 1, 0, 0, 0, 0): Q(1),
            (0, 0, 0, 0, 1, 2): Q(-1),
            (0, 0, 0, 0, 0, 0): Q(1),
        },
        "six-site ordered-pair provenance cofactor changed",
    )
    inserted_grade8 = insert_endpoint_colours(grade6, B8)

    lifted_base = forced_pair.lift_cells(module, base)
    corners = tuple(
        frontier.add_pair(module, lifted_base, left_weight, right_weight)
        for left_weight, right_weight in ((0, 0), (1, 0), (0, 1), (1, 1))
    )
    tensor_components = frontier.bilinear_components(
        one_cell, *(module.matching_tensor(B10, cells) for cells in corners)
    )
    require(not tensor_components[1] and not tensor_components[2], "linear full grade appeared")
    require(
        {word[:-2]: coefficient for word, coefficient in tensor_components[3].items()}
        == inserted_grade8,
        "six-site source grade did not reconstruct the mixed output coefficient",
    )

    # The ordinary component retains the exact target under every controlled
    # trace.  The tagged source grade carries no target component.
    tensor8 = module.matching_tensor(B8, base)
    tensor10 = module.matching_tensor(B10, lifted_base)
    for controller in B8:
        require(
            one_cross.controlled_tensor_contraction(tensor10, controller) == tensor8,
            f"ordinary forced lift did not reconstruct at controller {controller}",
        )
        require(
            one_cross.controlled_tensor_contraction(
                forced_pair.delta_tensor(B10), controller
            )
            == forced_pair.delta_tensor(B8),
            f"Delta did not reconstruct at controller {controller}",
        )

    expected_remainders = {
        0: {63: Q(1)},
        1: {63: Q(1)},
        2: {},
        3: {},
        4: {},
        5: {21: Q(1), 150: Q(1)},
    }
    guard_records = {}
    graded_module_records = {}
    cut_data = {}
    for z in module.S:
        old_u_set, old_columns, old_basis, remainder = cut_guard_data(
            forced_pair, two_cell, module, base, inserted_grade8, z
        )
        require(
            remainder == expected_remainders[z],
            f"source-grade quotient guard changed at cut {z}",
        )
        guard_records[z] = remainder
        cut_data[z] = (old_u_set, old_columns, old_basis)

        # Use the largest natural coefficientwise coupled cylinder: every
        # 1,t,s,ts coefficient of every literal N=10 cofactor column.  A
        # mixed residual coefficient outside even this superspace cannot be
        # absorbed by a source-graded cofactor identity.
        new_u_set = old_u_set + frontier.NEW_VERTICES
        coefficient_columns = frontier.coefficient_columns(
            forced_pair, one_cell, module, new_u_set, corners
        )
        coefficient_rows = frontier.coefficient_rows(
            forced_pair, one_cell, module, z, new_u_set, corners
        )
        coupled_basis = module.rational_basis(
            [
                component
                for components in coefficient_columns.values()
                for component in components
            ]
        )
        bad_mixed_rows = {
            word: two_cell.quotient_remainder(components[3], coupled_basis)
            for word, components in coefficient_rows.items()
            if components[3]
            and not module.rational_member(components[3], coupled_basis)
        }
        graded_module_records[z] = (len(coupled_basis), bad_mixed_rows)

    expected_graded_modules = {
        0: (17, {BOUNDARY_WORD: {567: Q(1)}}),
        1: (17, {BOUNDARY_WORD: {567: Q(1)}}),
        2: (25, {}),
        3: (25, {}),
        4: (27, {}),
        5: (24, {BOUNDARY_WORD: {189: Q(1)}}),
    }
    require(
        graded_module_records == expected_graded_modules,
        "coupled source-graded coefficient-cylinder audit changed",
    )

    for candidate in CANDIDATE_CUTS:
        four_cuts = FIXED_CUTS + (candidate,)
        require(
            all(not guard_records[z] for z in FIXED_CUTS)
            and guard_records[candidate],
            f"graded four-cut guard failed at candidate {candidate}",
        )

    # N-stability on the forced-pair tower.  The next old source is A8 tensor
    # g_89, so its ordered-pair cofactor is K6 tensor g_89 and contracts to K6.
    grade8 = module.matching_tensor(GRADE_VERTICES10, lifted_base)
    require(grade8 == tensor_diagonal_pair(grade6), "eight-site grade is not K tensor g")
    require(
        controlled_last_pair_contraction(grade8, 0) == grade6,
        "eight-site source grade did not contract to the six-site grade",
    )
    inserted_grade10 = insert_endpoint_colours(grade8, B10)
    require(
        controlled_last_pair_contraction(inserted_grade10, 0) == inserted_grade8,
        "inserted source grade did not commute with contraction",
    )

    for z in module.S:
        old_u_set, old_columns, old_basis = cut_data[z]
        lifted_u_set = old_u_set + (8, 9)
        rows10 = forced_pair.flatten_rows(
            inserted_grade10, B10, (z, 6, 7), lifted_u_set
        )
        controller = old_u_set[0]
        contracted_guard = one_cross.controlled_row_contraction(
            forced_pair,
            rows10.get(BOUNDARY_WORD, {}),
            old_u_set,
            controller,
        )
        require(
            contracted_guard == GUARD_ROW,
            f"lifted guard row did not contract at cut {z}",
        )
        require(
            two_cell.quotient_remainder(contracted_guard, old_basis)
            == expected_remainders[z],
            f"lifted quotient guard changed at cut {z}",
        )

    # The ordinary target and output also contract exactly through one more
    # forced-pair lift, giving an explicit N=12 -> N=10 -> N=8 tower check.
    base12 = add_diagonal_pair(module, lifted_base, 10, 11)
    tensor12 = module.matching_tensor(B12, base12)
    require(
        controlled_last_pair_contraction(tensor12, 0) == tensor10,
        "ordinary N=12 tensor did not contract to N=10",
    )
    require(
        controlled_last_pair_contraction(forced_pair.delta_tensor(B12), 0)
        == forced_pair.delta_tensor(B10),
        "Delta12 did not contract to Delta10",
    )

    print("N=10 source-graded ordered-pair four-point guard: exact PASS")
    print(f"six-site provenance support: {len(grade6)}")
    print(f"guard row at boundary {BOUNDARY_WORD}: {GUARD_ROW}")
    print(f"cut quotient normal forms: {guard_records}")
    print(f"coupled graded-cylinder records: {graded_module_records}")
    print("fixed cuts 2,3,4: ordered-pair grade is admitted")
    print("candidate cuts 0,1,5: ordered-pair grade is eliminated")
    print("ordinary component: Delta reconstructs exactly")
    print("forced-pair stability: N=12 -> N=10 -> N=8 exact")
    print("verdict: exact source-graded counterguard; ungraded implication not claimed")


if __name__ == "__main__":
    main()
