#!/usr/bin/env python3
"""Exact audits for ``notes/one-crossing-kernel-collapse.md``.

The checker has three independent parts.

1.  On the rational eight-site binary GHZ source from
    ``verify_n8_pair_cap_obstruction.py`` it tests

        ker(F_1) <= ker(D)

    on all 56 three-versus-five cuts.  Exactly 12 cuts pass and 44 fail.
2.  On the passing cut C={1,2,5}, it constructs an exact factor map Phi,
    builds the collapsed six-site edge tensors, and checks that their
    matching tensor is binary GHZ.  The old high-sector separation fails
    on this same cut, so this also audits strictness of the new criterion.
3.  On the ternary active-anchor model from
    ``verify_total_sector_six_reduction.py`` it checks over Q that all 56
    cuts fail the kernel inclusion, even though all three constant fibres
    and all coordinate anchors have the target values.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations, product

import sympy as sp

import verify_n8_pair_cap_obstruction as binary
import verify_total_sector_six_reduction as ternary


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(rest):
            yield ((first, second),) + tail


def target_right_rows(q: int) -> sp.Matrix:
    """Rows e_r^(tensor 5), in lexicographic right-word order."""
    rows = sp.zeros(q, q**5)
    for color in range(q):
        index = sum(color * q ** (4 - position) for position in range(5))
        rows[color, index] = 1
    return rows


def binary_sector(C, crossing_number: int) -> tuple[tuple[int, ...], sp.Matrix]:
    """Flattening rows for the indicated crossing sector."""
    vertices = binary.VERTICES
    edges = binary.source()
    C = tuple(C)
    C_set = set(C)
    U = tuple(vertex for vertex in vertices if vertex not in C_set)
    matchings = tuple(perfect_matchings(vertices))
    rows = []
    for left_colors in product(range(2), repeat=3):
        row = []
        for right_colors in product(range(2), repeat=5):
            coloring = dict(zip(C, left_colors, strict=True))
            coloring.update(zip(U, right_colors, strict=True))
            value = sp.S.Zero
            for matching in matchings:
                crossing = sum(
                    (left in C_set) != (right in C_set)
                    for left, right in matching
                )
                if crossing != crossing_number:
                    continue
                term = sp.S.One
                for left, right in matching:
                    term *= binary.edge_entry(
                        edges,
                        left,
                        right,
                        coloring[left],
                        coloring[right],
                    )
                value += term
            row.append(sp.factor(value))
        rows.append(row)
    return U, sp.Matrix(rows)


def inclusion_defect(flattening: sp.Matrix, q: int) -> int:
    """Dimension added to the row space by the q target rows."""
    target_rows = target_right_rows(q)
    return flattening.col_join(target_rows).rank() - flattening.rank()


def factor_map(flattening: sp.Matrix, desired: sp.Matrix) -> sp.Matrix:
    """Choose Phi with Phi*flattening=desired, setting extension freedoms to 0."""
    rows = []
    for row_index in range(desired.rows):
        solutions = sp.linsolve(
            (flattening.T, desired.row(row_index).T)
        )
        solution = next(iter(solutions))
        parameters = set().union(
            *(entry.free_symbols for entry in solution)
        )
        rows.append(
            [sp.simplify(entry.subs({p: 0 for p in parameters}))
             for entry in solution]
        )
    answer = sp.Matrix(rows)
    assert answer * flattening == desired
    return answer


def binary_edge_matrix(edges, left, right) -> sp.Matrix:
    return sp.Matrix(
        2,
        2,
        lambda a, b: binary.edge_entry(edges, left, right, a, b),
    )


def collapsed_binary_source(C, U, phi):
    """Construct (Phi tensor id)K_u and retain the internal U edges."""
    edges = binary.source()
    C = tuple(C)
    left_words = tuple(product(range(2), repeat=3))
    collapsed = {}

    for exposed in U:
        boundary = sp.zeros(8, 2)
        for left_index, left_word in enumerate(left_words):
            colors = dict(zip(C, left_word, strict=True))
            for exposed_color in range(2):
                value = sp.S.Zero
                for crossing_vertex in C:
                    remaining = tuple(
                        vertex for vertex in C if vertex != crossing_vertex
                    )
                    value += binary.edge_entry(
                        edges,
                        remaining[0],
                        remaining[1],
                        colors[remaining[0]],
                        colors[remaining[1]],
                    ) * binary.edge_entry(
                        edges,
                        crossing_vertex,
                        exposed,
                        colors[crossing_vertex],
                        exposed_color,
                    )
                boundary[left_index, exposed_color] = sp.factor(value)
        collapsed[("star", exposed)] = phi * boundary

    for left, right in combinations(U, 2):
        collapsed[(left, right)] = binary_edge_matrix(edges, left, right)
    return collapsed


def collapsed_coefficient(collapsed, labels, coloring):
    local = dict(zip(labels, coloring, strict=True))
    value = sp.S.Zero
    for matching in perfect_matchings(labels):
        term = sp.S.One
        for left, right in matching:
            if left == "star":
                matrix = collapsed[("star", right)]
                term *= matrix[local[left], local[right]]
            elif right == "star":
                matrix = collapsed[("star", left)]
                term *= matrix[local[right], local[left]]
            else:
                edge = tuple(sorted((left, right)))
                matrix = collapsed[edge]
                if edge == (left, right):
                    term *= matrix[local[left], local[right]]
                else:
                    term *= matrix[local[right], local[left]]
        value += term
    return sp.factor(value)


def audit_binary_exact_source():
    edges = binary.source()
    assert binary.matching_tensor(binary.VERTICES, edges) == {
        (0,) * 8: sp.S.One,
        (1,) * 8: sp.S.One,
    }

    histogram = Counter()
    passing = []
    for C in combinations(binary.VERTICES, 3):
        _U, one_crossing = binary_sector(C, 1)
        rank = one_crossing.rank()
        defect = inclusion_defect(one_crossing, 2)
        histogram[rank, defect] += 1
        if defect == 0:
            passing.append(C)

    assert histogram == Counter(
        {
            (2, 0): 12,
            (1, 1): 28,
            (0, 2): 8,
            (2, 1): 4,
            (1, 2): 4,
        }
    )
    assert len(passing) == 12

    # This cut passes the new kernel test but fails the old requirement
    # G_C intersect LS_C(T_3)=0.
    C = (1, 2, 5)
    U, one_crossing = binary_sector(C, 1)
    _same_U, high = binary_sector(C, 3)
    desired = target_right_rows(2)
    phi = factor_map(one_crossing, desired)
    assert phi == sp.Matrix(
        [[1, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 4]]
    )

    diagonal_left = sp.zeros(8, 2)
    diagonal_left[0, 0] = 1
    diagonal_left[7, 1] = 1
    intersection_dimension = (
        high.rank() + 2 - high.row_join(diagonal_left).rank()
    )
    assert high.rank() == 2
    assert intersection_dimension == 1
    # The actual surviving diagonal contamination is g_(C,1).
    assert high.row_join(sp.eye(8)[:, 7]).rank() == high.rank()

    collapsed = collapsed_binary_source(C, U, phi)
    labels = ("star",) + U
    output = {
        coloring: coefficient
        for coloring in product(range(2), repeat=6)
        if (coefficient := collapsed_coefficient(
            collapsed, labels, coloring
        )) != 0
    }
    assert output == {(0,) * 6: sp.S.One, (1,) * 6: sp.S.One}
    assert collapsed[("star", 3)] == sp.Matrix([[0, 0], [0, 2]])
    assert collapsed[("star", 7)] == sp.Matrix([[1, 0], [0, 0]])
    assert all(
        collapsed[("star", vertex)] == sp.zeros(2)
        for vertex in (4, 6, 8)
    )
    return histogram


def ternary_entry(left, right, left_color, right_color):
    if left < right:
        return ternary.MATRICES.get((left, right), ternary.ZERO)[
            left_color
        ][right_color]
    return ternary.MATRICES.get((right, left), ternary.ZERO)[
        right_color
    ][left_color]


def ternary_one_crossing(C) -> sp.Matrix:
    vertices = tuple(range(8))
    C = tuple(C)
    C_set = set(C)
    U = tuple(vertex for vertex in vertices if vertex not in C_set)
    rows = []
    for left_colors in product(range(3), repeat=3):
        row = []
        for right_colors in product(range(3), repeat=5):
            coloring = dict(zip(C, left_colors, strict=True))
            coloring.update(zip(U, right_colors, strict=True))
            value = 0
            for matching in ternary.MATCHINGS:
                crossing = sum(
                    (left in C_set) != (right in C_set)
                    for left, right in matching
                )
                if crossing != 1:
                    continue
                term = 1
                for left, right in matching:
                    term *= ternary_entry(
                        left,
                        right,
                        coloring[left],
                        coloring[right],
                    )
                value += term
            row.append(value)
        rows.append(row)
    return sp.Matrix(rows)


def audit_ternary_anchor_near_target():
    # Reuse the independent checks of active coordinate anchors, exact
    # constant fibres, and the explicitly surviving mixed coefficient.
    ternary.verify_factorization_and_anchors()
    ternary.verify_constant_fibres_and_nonexample()

    histogram = Counter()
    for C in combinations(range(8), 3):
        one_crossing = ternary_one_crossing(C)
        rank = one_crossing.rank()
        defect = inclusion_defect(one_crossing, 3)
        histogram[rank, defect] += 1
        assert defect > 0

    assert histogram == Counter(
        {(6, 3): 32, (9, 3): 15, (3, 3): 8, (8, 3): 1}
    )
    return histogram


def main():
    binary_histogram = audit_binary_exact_source()
    ternary_histogram = audit_ternary_anchor_near_target()
    print("exact binary GHZ: 12 passing and 44 failing five-set cuts")
    print("binary (rank F1, inclusion defect):", dict(binary_histogram))
    print("constructed exact collapsed six-site binary GHZ")
    print("same cut has one-dimensional total high-sector contamination")
    print("ternary anchor model: all 56 cuts fail the kernel inclusion")
    print("ternary (rank F1, inclusion defect):", dict(ternary_histogram))


if __name__ == "__main__":
    main()
