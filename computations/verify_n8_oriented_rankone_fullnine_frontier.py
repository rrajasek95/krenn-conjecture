#!/usr/bin/env python3
"""Audit the oriented N=8 rank-one/full-nine and reciprocal frontier."""

from __future__ import annotations

from fractions import Fraction
from math import factorial


N = 8


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def component_decompositions():
    types = sorted(
        [("P", size) for size in range(1, N + 1)]
        + [("C", size) for size in range(3, N + 1)]
    )
    result = []

    def visit(start, left, chosen):
        if left == 0:
            result.append(tuple(chosen))
            return
        for index in range(start, len(types)):
            if types[index][1] <= left:
                visit(index, left - types[index][1], chosen + [types[index]])

    visit(0, N, [])
    return result


def component_invariants(component):
    kind, size = component
    edges = size - 1 if kind == "P" else size
    if kind == "C" and size == 3:
        return edges, None, size
    if kind == "C":
        return edges, 2 if size == 4 else size, size
    chords = max(size - 2, 0)
    covered = 0 if size <= 2 else 2 if size == 3 else size
    return edges, chords, covered


def minimum_edges_for_degree_four_vertices(t):
    """Minimum edges allowing t specified vertices to have degree >=4."""

    if t <= 5:
        return t * (t - 1) // 2 + t * (5 - t)
    return 2 * t


def reciprocal_flat_census():
    decompositions = component_decompositions()
    minimum_degree_edges = [minimum_edges_for_degree_four_vertices(t)
                            for t in range(N + 1)]
    require(minimum_degree_edges == [0, 4, 7, 9, 10, 10, 12, 14, 16],
            "degree-four complement extremal ledger changed")
    survivors = {}

    for reciprocal_pairs in range(4):
        witness_edges = 24 - reciprocal_pairs
        complement_budget = 4 + reciprocal_pairs
        max_three_essential = max(
            t for t, edge_minimum in enumerate(minimum_degree_edges)
            if edge_minimum <= complement_budget
        )
        initial_good_lower = witness_edges - (16 + max_three_essential)
        candidates = []
        for decomposition in decompositions:
            data = [component_invariants(component)
                    for component in decomposition]
            if any(chords is None for _edges, chords, _covered in data):
                continue
            good_edges = sum(edges for edges, _chords, _covered in data)
            chords = sum(chord for _edges, chord, _covered in data)
            covered = sum(cover for _edges, _chord, cover in data)
            if good_edges > N or chords > complement_budget:
                continue

            remaining_triple_sites = min(max_three_essential, N - covered)
            selected_bad_budget = (
                covered + 2 * (N - covered) + remaining_triple_sites
            )
            refined_good_lower = witness_edges - selected_bad_budget
            required_good = max(initial_good_lower, refined_good_lower)
            if good_edges >= required_good:
                candidates.append(
                    (tuple(sorted(decomposition)), good_edges,
                     chords, covered, required_good)
                )
        survivors[reciprocal_pairs] = candidates

    require(not survivors[0] and not survivors[1] and not survivors[2],
            "an all-flat rank-one witness graph survived for r<=2")
    expected_r3 = {
        ((('P', 1), ('P', 1), ('P', 2), ('P', 2), ('P', 2)), 3, 0, 0, 3),
        ((('P', 2), ('P', 2), ('P', 2), ('P', 2)), 4, 0, 0, 3),
    }
    require(set(survivors[3]) == expected_r3,
            f"first reciprocal frontier changed: {survivors[3]}")
    return survivors


def orientation_and_eligibility_table():
    table = {
        ("O", "O"): ("R", "R"),
        ("I", "I"): ("L", "L"),
        ("O", "I"): ("R", "L"),
        ("I", "O"): ("L", "R"),
    }
    require(set(table.values()) == {("R", "R"), ("L", "L"),
                                    ("R", "L"), ("L", "R")},
            "orientation/ruling table changed")
    colors = {0, 1, 2}
    for head in colors:
        eligible = colors - {head}
        require(len(eligible) == 2 and head not in eligible,
                "coordinate-head ruling eligibility changed")
    return table


def reciprocal_selector_accessibility():
    colors = {0, 1, 2}
    access = {}
    for left_axis in colors:
        for right_axis in colors:
            accessible = set()
            for target in colors:
                if left_axis != target or right_axis != target:
                    accessible.add(target)
            access[(left_axis, right_axis)] = accessible
            expected = colors if left_axis != right_axis else colors - {left_axis}
            require(accessible == expected,
                    "reciprocal coordinate selector accessibility changed")
    return access


def uniform_overlap_ledger():
    rows = []
    for order in range(8, 34, 2):
        for triple_sites in range(order + 1):
            good_lower = order - triple_sites
            if 2 * triple_sites < order:
                require(2 * good_lower > order,
                        "uniform overlap matching threshold failed")
            rows.append((order, triple_sites, good_lower))
    return rows


def cubic_cross_only_permanent_ledger():
    # For a three-regular bipartite multigraph with shore size m, the
    # van-der-Waerden bound is per(A) >= 3^m m!/m^m.  At m=4 it already
    # exceeds three and the bound is strictly increasing thereafter.
    bounds = []
    for shore_size in range(4, 33):
        bound = Fraction(3 ** shore_size * factorial(shore_size),
                         shore_size ** shore_size)
        require(bound > 3,
                "three-regular bipartite permanent bound fell to three")
        if shore_size > 4:
            require(bound > bounds[-1][1],
                    "permanent lower bound stopped increasing")
        bounds.append((shore_size, bound))
    return bounds


def main():
    survivors = reciprocal_flat_census()
    orientations = orientation_and_eligibility_table()
    access = reciprocal_selector_accessibility()
    uniform_rows = uniform_overlap_ledger()
    permanent_bounds = cubic_cross_only_permanent_ledger()
    print("all-flat survivors for reciprocal counts 0,1,2:",
          [len(survivors[r]) for r in range(3)])
    print("first reciprocal frontier r=3:", survivors[3])
    print("shared-site orientation/ruling table:", orientations)
    print("off-diagonal reciprocal targets accessible:", access[(0, 1)])
    print("diagonal reciprocal inaccessible target:",
          sorted({0, 1, 2} - access[(0, 0)]))
    print("uniform no-reciprocal overlap ledgers:", len(uniform_rows))
    print("3-regular bipartite permanent lower bound at shore 4:",
          permanent_bounds[0][1])
    print("oriented rank-one/full-nine frontier: PASS")


if __name__ == "__main__":
    main()
