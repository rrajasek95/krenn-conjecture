#!/usr/bin/env python3
"""Exact torus collision and two-grade cancellation at the N=10 frontier.

For opposite-new, distinct-old cross pairs, swapping the two old endpoints
between new vertices 8 and 9 leaves the full matching grade and every
quadratic cofactor grade unchanged.  The two source monomials are distinct
but have the same torus character even before quotienting by the anchored
base and target characters.

The checker classifies all 4,536 quadratic-capable pairs into 2,268 such
two-element output-grade classes.  It then verifies the smallest explicit
cancellation: the four-cell cross block

  E_(08;00) + E_(19;00) + E_(18;00) - E_(09;00)

has permanent 1 - 1 = 0.  Its full quadratic output and all quadratic
cofactor contributions cancel exactly, although both ordered-pair source
grades are nonzero.  The remaining source differs from the forced lift only
through linear one-cross cofactor directions.  This disproves formal
provenance separation, not Krenn's conjecture.
"""

from __future__ import annotations

import importlib.util
from collections import Counter, defaultdict
from fractions import Fraction
from itertools import combinations
from pathlib import Path


Q = Fraction
B8 = tuple(range(8))
B10 = tuple(range(10))
B12 = tuple(range(12))
PAIR_A = ((0, 8, 0, 0), (1, 9, 0, 0))
PAIR_B = ((1, 8, 0, 0), (0, 9, 0, 0))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def load_graded_guard():
    path = Path(__file__).with_name(
        "verify_n10_two_cross_source_graded_four_point_guard.py"
    )
    spec = importlib.util.spec_from_file_location("graded_guard", path)
    require(spec is not None and spec.loader is not None, "cannot load graded guard")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def coordinate_character(coordinate):
    old, new, old_colour, new_colour = coordinate
    return {3 * old + old_colour: Q(1), 3 * new + new_colour: Q(1)}


def sparse_sum(*vectors):
    answer = {}
    for vector in vectors:
        for index, value in vector.items():
            answer[index] = answer.get(index, Q(0)) + value
            if not answer[index]:
                answer.pop(index)
    return answer


def pair_character(pair):
    return sparse_sum(*(coordinate_character(coordinate) for coordinate in pair))


def exact_key(vector):
    return tuple(sorted(vector.items()))


def projective_tensor_key(tensor):
    if not tensor:
        return ()
    pivot = min(tensor)
    scale = tensor[pivot]
    return tuple(sorted((word, value / scale) for word, value in tensor.items()))


def swap_pair(pair):
    left, right = pair
    require(left[1] == 8 and right[1] == 9, "pair is not new-endpoint ordered")
    old_l, _, old_colour_l, new_colour_l = left
    old_r, _, old_colour_r, new_colour_r = right
    return (
        (old_r, 8, old_colour_r, new_colour_l),
        (old_l, 9, old_colour_l, new_colour_r),
    )


def ordered_pair_grade(module, base, pair, old_vertices, new_vertices):
    left, right = pair
    require(
        left[1] == new_vertices[0] and right[1] == new_vertices[1],
        "pair does not use the declared new vertices",
    )
    old_l, _, old_colour_l, new_colour_l = left
    old_r, _, old_colour_r, new_colour_r = right
    require(old_l != old_r, "quadratic grade repeats an old endpoint")
    remaining = tuple(vertex for vertex in old_vertices if vertex not in (old_l, old_r))
    cofactor = module.matching_tensor(remaining, base)
    answer = {}
    for word, coefficient in cofactor.items():
        assignment = {old_l: old_colour_l, old_r: old_colour_r}
        assignment.update(zip(remaining, word))
        output_word = (
            tuple(assignment[vertex] for vertex in old_vertices)
            + (new_colour_l, new_colour_r)
        )
        answer[output_word] = coefficient
    return answer


def pair_cells(module, base, pair, left_weight, right_weight):
    cells = {edge: list(entries) for edge, entries in base.items()}
    sources = []
    if left_weight:
        sources.append((*pair[0], Q(left_weight)))
    if right_weight:
        sources.append((*pair[1], Q(right_weight)))
    module.add_sources(cells, sources)
    return cells


def mixed_column_components(
    frontier, forced_pair, one_cell, module, base, pair, u_set
):
    corners = tuple(
        pair_cells(module, base, pair, left_weight, right_weight)
        for left_weight, right_weight in ((0, 0), (1, 0), (0, 1), (1, 1))
    )
    tables = tuple(
        forced_pair.insertion_columns(module, u_set, cells) for cells in corners
    )
    return {
        label: frontier.bilinear_components(
            one_cell,
            tables[0][label],
            tables[1][label],
            tables[2][label],
            tables[3][label],
        )[3]
        for label in tables[0]
    }


def add_weighted_coordinates(module, base, weighted_coordinates):
    cells = {edge: list(entries) for edge, entries in base.items()}
    module.add_sources(
        cells,
        tuple((*coordinate, Q(weight)) for coordinate, weight in weighted_coordinates),
    )
    return cells


def affine_column_superposition(
    forced_pair, one_cell, module, base, weighted_coordinates, u_set
):
    base_columns = forced_pair.insertion_columns(module, u_set, base)
    expected = {label: dict(column) for label, column in base_columns.items()}
    for coordinate, weight in weighted_coordinates:
        single = add_weighted_coordinates(module, base, ((coordinate, weight),))
        single_columns = forced_pair.insertion_columns(module, u_set, single)
        for label in expected:
            expected[label] = one_cell.sparse_linear_combination(
                (1, expected[label]),
                (1, single_columns[label]),
                (-1, base_columns[label]),
            )
    return expected


def main() -> None:
    graded_guard = load_graded_guard()
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

    # Target-stabilizing anchored torus quotient.
    support = tuple(
        (left, right, colour_l, colour_r)
        for (left, right), entries in lifted_base.items()
        for colour_l, colour_r, weight in entries
        if weight
    )
    require(len(support) == 19, "lifted anchored support count changed")
    target_characters = tuple(
        {3 * vertex + colour: Q(1) for vertex in B10}
        for colour in range(3)
    )
    constraint_basis = module.rational_basis(
        [coordinate_character(coordinate) for coordinate in support]
        + list(target_characters)
    )
    require(len(constraint_basis) == 18, "N=10 torus constraint rank changed")
    left_remainder = two_cell.quotient_remainder(
        coordinate_character(PAIR_A[0]), constraint_basis
    )
    right_remainder = two_cell.quotient_remainder(
        coordinate_character(PAIR_A[1]), constraint_basis
    )
    require(
        left_remainder == {3: Q(-1), 27: Q(-1)}
        and right_remainder == {3: Q(1), 27: Q(1)},
        "witness cross characters changed",
    )
    require(
        not two_cell.quotient_remainder(pair_character(PAIR_A), constraint_basis),
        "witness pair unexpectedly has a separating torus character",
    )
    require(
        pair_character(PAIR_A) == pair_character(PAIR_B),
        "endpoint-swap pair characters are not literally equal",
    )

    # Exact character and output-grade census for all quadratic-capable pairs.
    coordinates = frontier.cross_coordinates()
    pairs = tuple(
        (left, right)
        for left, right in combinations(coordinates, 2)
        if frontier.topology(left, right) == ("opposite_new", "distinct_old")
    )
    require(len(pairs) == 4_536, "quadratic-capable pair count changed")
    character_classes = defaultdict(list)
    grade_classes = defaultdict(list)
    grade_cache = {
        (old_l, old_r): module.matching_tensor(
            tuple(vertex for vertex in B8 if vertex not in (old_l, old_r)), base
        )
        for old_l in B8
        for old_r in B8
        if old_l != old_r
    }

    def cached_grade(pair):
        left, right = pair
        old_l, _, old_colour_l, new_colour_l = left
        old_r, _, old_colour_r, new_colour_r = right
        remaining = tuple(vertex for vertex in B8 if vertex not in (old_l, old_r))
        answer = {}
        for word, coefficient in grade_cache[(old_l, old_r)].items():
            assignment = {old_l: old_colour_l, old_r: old_colour_r}
            assignment.update(zip(remaining, word))
            output_word = (
                tuple(assignment[vertex] for vertex in B8)
                + (new_colour_l, new_colour_r)
            )
            answer[output_word] = coefficient
        return answer

    for pair in pairs:
        remainder = two_cell.quotient_remainder(
            pair_character(pair), constraint_basis
        )
        character_classes[exact_key(remainder)].append(pair)
        grade_classes[projective_tensor_key(cached_grade(pair))].append(pair)

    require(len(character_classes) == 959, "pair-character class count changed")
    require(len(character_classes[()]) == 132, "zero pair-character class changed")
    require(
        Counter(len(records) for records in character_classes.values())
        == Counter({2: 612, 6: 174, 8: 120, 24: 20, 12: 12, 18: 12, 44: 6, 36: 2, 132: 1}),
        "exact pair-character histogram changed",
    )
    require(() not in grade_classes, "a quadratic-capable grade vanished")
    require(
        len(grade_classes) == 2_268
        and all(len(records) == 2 for records in grade_classes.values()),
        "endpoint-swap output-grade pairing changed",
    )
    for records in grade_classes.values():
        left_pair, right_pair = records
        require(
            right_pair == swap_pair(left_pair) or left_pair == swap_pair(right_pair),
            "an output-grade collision is not the endpoint swap",
        )
        require(
            cached_grade(left_pair) == cached_grade(right_pair),
            "endpoint-swap grades are only projectively, not exactly, equal",
        )
        require(
            len(set(left_pair) | set(right_pair)) == 4,
            "two colliding grades use fewer than four cross coordinates",
        )

    # The explicit swapped grades agree in the full tensor and every
    # quadratic cofactor column.
    grade_a = ordered_pair_grade(module, base, PAIR_A, B8, (8, 9))
    grade_b = ordered_pair_grade(module, base, PAIR_B, B8, (8, 9))
    require(grade_a == grade_b and grade_a, "explicit swapped full grades differ")
    for z in module.S:
        u_set = tuple(vertex for vertex in module.S if vertex != z) + (8, 9)
        require(
            mixed_column_components(
                frontier, forced_pair, one_cell, module, lifted_base, PAIR_A, u_set
            )
            == mixed_column_components(
                frontier, forced_pair, one_cell, module, lifted_base, PAIR_B, u_set
            ),
            f"swapped quadratic cofactor grades differ at cut {z}",
        )

    weighted_coordinates = (
        (PAIR_A[0], Q(1)),
        (PAIR_A[1], Q(1)),
        (PAIR_B[0], Q(1)),
        (PAIR_B[1], Q(-1)),
    )
    cancelled = add_weighted_coordinates(module, lifted_base, weighted_coordinates)
    base_tensor10 = module.matching_tensor(B10, lifted_base)
    cancelled_tensor10 = module.matching_tensor(B10, cancelled)
    require(
        cancelled_tensor10 == base_tensor10,
        "permanent-zero cross block did not cancel in the full tensor",
    )

    cut_ranks = {}
    for z in module.S:
        u_set = tuple(vertex for vertex in module.S if vertex != z) + (8, 9)
        actual_columns = forced_pair.insertion_columns(module, u_set, cancelled)
        expected_columns = affine_column_superposition(
            forced_pair,
            one_cell,
            module,
            lifted_base,
            weighted_coordinates,
            u_set,
        )
        require(
            actual_columns == expected_columns,
            f"quadratic cofactor cancellation failed at cut {z}",
        )
        basis = module.rational_basis(list(actual_columns.values()))
        rows = forced_pair.flatten_rows(
            forced_pair.tensor_difference(
                cancelled_tensor10, forced_pair.delta_tensor(B10)
            ),
            B10,
            (z, 6, 7),
            u_set,
        )
        full = all(module.rational_member(row, basis) for row in rows.values())
        cut_ranks[z] = (len(basis), full)
    require(
        cut_ranks
        == {
            0: (19, False),
            1: (19, False),
            2: (20, False),
            3: (20, False),
            4: (20, False),
            5: (21, False),
        },
        "cancelled-source cut census changed",
    )

    # The collision is local and survives one more forced-pair lift.
    base12 = graded_guard.add_diagonal_pair(module, lifted_base, 10, 11)
    pair_a12 = ((0, 10, 0, 0), (1, 11, 0, 0))
    pair_b12 = ((1, 10, 0, 0), (0, 11, 0, 0))
    require(
        ordered_pair_grade(module, lifted_base, pair_a12, B10, (10, 11))
        == ordered_pair_grade(module, lifted_base, pair_b12, B10, (10, 11)),
        "endpoint-swap grade collision failed at N=12",
    )
    cancelled12 = add_weighted_coordinates(
        module,
        base12,
        (
            (pair_a12[0], Q(1)),
            (pair_a12[1], Q(1)),
            (pair_b12[0], Q(1)),
            (pair_b12[1], Q(-1)),
        ),
    )
    require(
        module.matching_tensor(B12, cancelled12)
        == module.matching_tensor(B12, base12),
        "permanent-zero cancellation failed at N=12",
    )

    print("N=10 cross-pair provenance separation audit: exact PASS")
    print("anchored target-stabilizing constraint rank: 18")
    print("witness ordered-pair quotient character: zero")
    print("quadratic pair character classes: 959; zero class: 132")
    print("output-grade classes: 2268 classes of size two")
    print("each collision is the disjoint four-cell endpoint swap")
    print("explicit permanent-zero block: full and quadratic cofactors cancel")
    print(f"cancelled-source cut census: {cut_ranks}")
    print("local endpoint-swap identity persists at N=12")
    print("verdict: torus and free multidegree do not imply ungraded separation")


if __name__ == "__main__":
    main()
