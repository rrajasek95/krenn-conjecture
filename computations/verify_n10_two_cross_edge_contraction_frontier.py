#!/usr/bin/env python3
"""Exact two-cross-edge frontier for the N=8 -> N=10 contraction lane.

The 144 cross coordinates join one old vertex to vertex 8 or 9.  This
checker first classifies all 10,296 unordered coordinate pairs.  A quadratic
full-matching term is possible exactly when the two coordinates use opposite
new vertices and distinct old vertices (4,536 pairs).

It then treats the smallest compatible pair

    t E_(08;00) + s E_(19;00)

symbolically, by recovering its four coefficient corners over Q.  On the
three old complete cuts, at least one controlled pair trace sends every
cofactor and residual coefficient into the old N=8 insertion cylinder.  On
each candidate fourth cut, the mixed ``ts`` residual coefficient remains
outside that cylinder for every possible old controller.  Thus the one-edge
contraction theorem does not extend to two arbitrary cross edges.  This is a
counterexample to that induction mechanism, not a counterexample to Krenn.
"""

from __future__ import annotations

import importlib.util
from collections import Counter
from fractions import Fraction
from itertools import combinations
from pathlib import Path


Q = Fraction
B8 = tuple(range(8))
B10 = tuple(range(10))
S = tuple(range(6))
NEW_VERTICES = (8, 9)
LEFT = (0, 8, 0, 0)
RIGHT = (1, 9, 0, 0)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def load_one_cross_edge():
    path = Path(__file__).with_name(
        "verify_n10_one_cross_edge_coefficient_cylinder_contraction.py"
    )
    spec = importlib.util.spec_from_file_location("one_cross", path)
    require(spec is not None and spec.loader is not None, "cannot load one-cross audit")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def cross_coordinates():
    return tuple(
        (old, new, old_colour, new_colour)
        for new in NEW_VERTICES
        for old in B8
        for old_colour in range(3)
        for new_colour in range(3)
    )


def topology(left, right):
    old_l, new_l, _, _ = left
    old_r, new_r, _, _ = right
    return (
        "same_new" if new_l == new_r else "opposite_new",
        "shared_old" if old_l == old_r else "distinct_old",
    )


def colour_type(left, right):
    _, _, old_l, new_l = left
    _, _, old_r, new_r = right
    if new_l != new_r:
        return "new_colours_distinct"
    matches = int(old_l == new_l) + int(old_r == new_l)
    return f"new_colours_equal_{matches}_old_matches"


def classify_pairs():
    coordinates = cross_coordinates()
    require(len(coordinates) == 144, "cross-coordinate count changed")
    topology_counts = Counter()
    colour_counts = Counter()
    joint_counts = Counter()
    quadratic_count = 0
    for left, right in combinations(coordinates, 2):
        pair_topology = topology(left, right)
        pair_colour = colour_type(left, right)
        topology_counts[pair_topology] += 1
        colour_counts[pair_colour] += 1
        joint_counts[pair_topology + (pair_colour,)] += 1
        if pair_topology == ("opposite_new", "distinct_old"):
            quadratic_count += 1

    require(sum(topology_counts.values()) == 10_296, "pair count changed")
    require(
        topology_counts
        == Counter(
            {
                ("same_new", "shared_old"): 576,
                ("same_new", "distinct_old"): 4_536,
                ("opposite_new", "shared_old"): 648,
                ("opposite_new", "distinct_old"): 4_536,
            }
        ),
        "topology census changed",
    )
    require(quadratic_count == 4_536, "quadratic-capable count changed")
    require(
        colour_counts
        == Counter(
            {
                "new_colours_distinct": 6_912,
                "new_colours_equal_0_old_matches": 1_488,
                "new_colours_equal_1_old_matches": 1_536,
                "new_colours_equal_2_old_matches": 360,
            }
        ),
        "colour census changed",
    )
    require(
        joint_counts[("opposite_new", "distinct_old", "new_colours_distinct")]
        == 3_024,
        "quadratic new-colour mismatch count changed",
    )
    require(
        joint_counts[("opposite_new", "distinct_old", "new_colours_equal_2_old_matches")]
        == 168,
        "fully compatible quadratic count changed",
    )
    return topology_counts, colour_counts, joint_counts


def add_pair(module, lifted_base, left_weight, right_weight):
    cells = {edge: list(entries) for edge, entries in lifted_base.items()}
    sources = []
    if left_weight:
        sources.append((*LEFT, Q(left_weight)))
    if right_weight:
        sources.append((*RIGHT, Q(right_weight)))
    module.add_sources(cells, sources)
    return cells


def bilinear_components(one_cell, value00, value10, value01, value11):
    return (
        value00,
        one_cell.sparse_difference(value10, value00),
        one_cell.sparse_difference(value01, value00),
        one_cell.sparse_linear_combination(
            (1, value11), (-1, value10), (-1, value01), (1, value00)
        ),
    )


def coefficient_columns(forced_pair, one_cell, module, u_set, corners):
    tables = tuple(forced_pair.insertion_columns(module, u_set, cells) for cells in corners)
    labels = tuple(tables[0])
    require(all(tuple(table) == labels for table in tables), "column labels changed")
    return {
        label: bilinear_components(
            one_cell,
            tables[0][label],
            tables[1][label],
            tables[2][label],
            tables[3][label],
        )
        for label in labels
    }


def coefficient_rows(forced_pair, one_cell, module, z, u_set, corners):
    c_set = (z, 6, 7)
    tables = tuple(
        forced_pair.flatten_rows(
            forced_pair.tensor_difference(
                module.matching_tensor(B10, cells), forced_pair.delta_tensor(B10)
            ),
            B10,
            c_set,
            u_set,
        )
        for cells in corners
    )
    words = tuple(sorted(set().union(*(table.keys() for table in tables))))
    return {
        word: bilinear_components(
            one_cell,
            tables[0].get(word, {}),
            tables[1].get(word, {}),
            tables[2].get(word, {}),
            tables[3].get(word, {}),
        )
        for word in words
    }


def coefficient_failures(
    one_cross, forced_pair, module, old_basis, old_u_set, controller, columns, rows
):
    column_failures = []
    residual_failures = []
    degree_names = ("1", "t", "s", "ts")
    for label, components in columns.items():
        for component_index, component in enumerate(components[1:], 1):
            contracted = one_cross.controlled_row_contraction(
                forced_pair,
                component,
                old_u_set,
                controller,
            )
            if not module.rational_member(contracted, old_basis):
                column_failures.append((label, degree_names[component_index], contracted))
    for word, components in rows.items():
        for component_index, component in enumerate(components[1:], 1):
            contracted = one_cross.controlled_row_contraction(
                forced_pair,
                component,
                old_u_set,
                controller,
            )
            if not module.rational_member(contracted, old_basis):
                residual_failures.append((word, degree_names[component_index], contracted))
    return column_failures, residual_failures


def audit_countermodel(one_cross, forced_pair, certificate, one_cell, module, base):
    lifted_base = forced_pair.lift_cells(module, base)
    corners = tuple(
        add_pair(module, lifted_base, left_weight, right_weight)
        for left_weight, right_weight in ((0, 0), (1, 0), (0, 1), (1, 1))
    )

    tensors = tuple(module.matching_tensor(B10, cells) for cells in corners)
    tensor_components = bilinear_components(one_cell, *tensors)
    require(not tensor_components[1], "left cross edge entered a full matching alone")
    require(not tensor_components[2], "right cross edge entered a full matching alone")
    require(tensor_components[3], "two-cross mixed full tensor vanished")
    require(
        all(word[8] == word[9] == word[0] == word[1] == 0 for word in tensor_components[3]),
        "mixed full tensor has an unexpected endpoint colour",
    )

    passing_controllers = {}
    column_controllers = {}
    failure_census = Counter()
    witnesses = {}
    for z in S:
        old_u_set = tuple(vertex for vertex in S if vertex != z)
        new_u_set = old_u_set + NEW_VERTICES
        old_columns = forced_pair.insertion_columns(module, old_u_set, base)
        old_basis = module.rational_basis(list(old_columns.values()))
        columns = coefficient_columns(forced_pair, one_cell, module, new_u_set, corners)
        rows = coefficient_rows(forced_pair, one_cell, module, z, new_u_set, corners)

        passes = []
        clean_columns = []
        for controller in old_u_set:
            column_failures, residual_failures = coefficient_failures(
                one_cross,
                forced_pair,
                module,
                old_basis,
                old_u_set,
                controller,
                columns,
                rows,
            )
            if not column_failures and not residual_failures:
                passes.append(controller)
            if not column_failures:
                clean_columns.append(controller)
            failure_census[(z, controller, "column")] = len(column_failures)
            failure_census[(z, controller, "residual")] = len(residual_failures)
            if residual_failures:
                word, degree, contracted = residual_failures[0]
                remainder = certificate.load_two_cell_audit().quotient_remainder(
                    contracted, old_basis
                )
                require(remainder, "reported residual failure has zero quotient remainder")
                witnesses[(z, controller)] = (word, degree, remainder)

        passing_controllers[z] = tuple(passes)
        column_controllers[z] = tuple(clean_columns)

    require(
        all(passing_controllers[z] for z in (2, 3, 4)),
        "two-cross pair no longer descends on every fixed cut",
    )
    require(
        all(not passing_controllers[z] for z in (0, 1, 5)),
        "candidate cut unexpectedly admits a controlled descent",
    )
    require(
        column_controllers[0] == (1, 4, 5)
        and column_controllers[1] == (0, 4, 5)
        and not column_controllers[5],
        "candidate-cut cofactor-controller pattern changed",
    )
    for z in (0, 1, 5):
        old_u_set = tuple(vertex for vertex in S if vertex != z)
        for controller in old_u_set:
            require((z, controller) in witnesses, f"missing residual witness at {(z, controller)}")
            require(
                witnesses[(z, controller)][1] == "ts",
                f"candidate obstruction is not quadratic at {(z, controller)}",
            )
    return (
        tensor_components[3],
        passing_controllers,
        column_controllers,
        failure_census,
        witnesses,
    )


def main() -> None:
    topology_counts, colour_counts, joint_counts = classify_pairs()
    one_cross = load_one_cross_edge()
    forced_pair = one_cross.load_forced_pair_contraction()
    certificate = forced_pair.load_positive_moduli_certificate()
    two_cell = certificate.load_two_cell_audit()
    one_cell = two_cell.load_one_cell_elimination()
    unit_gate = one_cell.load_unit_gate()
    module = unit_gate.load_three_cut_verifier()
    base = unit_gate.build_base(module)
    unit_gate.audit_base(module, base)

    mixed_tensor, passing, column_controllers, failures, witnesses = audit_countermodel(
        one_cross, forced_pair, certificate, one_cell, module, base
    )
    print("N=10 two-cross-edge controlled-contraction frontier: exact PASS")
    print("unordered cross-coordinate pairs: 10296")
    print(f"topology census: {dict(topology_counts)}")
    print(f"colour census: {dict(colour_counts)}")
    print("quadratic-capable opposite-new/distinct-old pairs: 4536")
    print("fully endpoint-compatible quadratic pairs: 168")
    print(f"explicit symbolic pair: {LEFT}, {RIGHT}")
    print(f"mixed full-tensor support: {len(mixed_tensor)}")
    print(f"passing controllers by cut: {passing}")
    print(f"cofactor-contained controllers by cut: {column_controllers}")
    print("candidate cuts 0,1,5: mixed-ts residual obstruction for every controller")
    print("verdict: the arbitrary two-cross-edge contraction theorem is false")


if __name__ == "__main__":
    main()
