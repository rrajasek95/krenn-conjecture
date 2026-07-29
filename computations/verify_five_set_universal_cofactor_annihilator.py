#!/usr/bin/env python3
"""Exact audit for ``notes/five-set-universal-cofactor-annihilator.md``.

This script checks three finite linear-algebra statements over Q.

1. For a dense deterministic integral family on five ternary sites it
   builds the cofactor insertion matrix S_U and verifies

       dim delta_U(ker B_U)
           = 3 - dim(G_U intersect im S_U) > 0.

   It constructs an explicit sparsely supported beta with B_U beta = 0
   and delta_U beta != 0.
2. After adjoining a three-site shore with deterministic integral edge
   matrices, it verifies the exact factorization F_1 = Gamma B_U.
3. It independently enumerates all 45 perfect matchings having one edge
   across the 3|5 cut and verifies that their summed flattening is F_1.  The
   beta from part 1 kills every exposed-U cofactor separately.  Cancellation
   among the three internal matchings inside one four-site cofactor remains
   allowed, as it must over arbitrary complex weights.

The universal existence theorem is not inferred from this sample.  It is
the formal dual consequence of the arbitrary-complex six-site theorem
proved in the accompanying note.
"""

from __future__ import annotations

from itertools import combinations, product
from random import Random

import sympy as sp


Q = 3
U = tuple(range(5))
C = tuple(range(5, 8))
B = C + U


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


def words(vertices):
    return tuple(product(range(Q), repeat=len(vertices)))


def dense_integral_edges(vertices, seed):
    """Small deterministic dense matrices, with no genericity claim."""
    rng = Random(seed)
    return {
        (left, right): sp.Matrix(
            Q, Q, [rng.randrange(-2, 3) for _ in range(Q * Q)]
        )
        for left, right in combinations(vertices, 2)
    }


def edge_entry(edges, left, right, left_color, right_color):
    if left < right:
        return edges[(left, right)][left_color, right_color]
    return edges[(right, left)][right_color, left_color]


def matching_tensor(vertices, edges):
    """Column vector for H_vertices in lexicographic word order."""
    vertices = tuple(vertices)
    matchings = tuple(perfect_matchings(vertices))
    entries = []
    for coloring in words(vertices):
        local = dict(zip(vertices, coloring, strict=True))
        value = sp.S.Zero
        for matching in matchings:
            term = sp.S.One
            for left, right in matching:
                term *= edge_entry(
                    edges, left, right, local[left], local[right]
                )
            value += term
        entries.append(sp.expand(value))
    return sp.Matrix(entries)


def insert_one_site(site, site_color, other_vertices, other_tensor):
    """Insert e_site_color tensor other_tensor into the ordered U slots."""
    other_vertices = tuple(other_vertices)
    other_index = {word: index for index, word in enumerate(words(other_vertices))}
    result = sp.zeros(Q ** len(U), 1)
    for index, word in enumerate(words(U)):
        local = dict(zip(U, word, strict=True))
        if local[site] != site_color:
            continue
        other_word = tuple(local[vertex] for vertex in other_vertices)
        result[index] = other_tensor[other_index[other_word]]
    return result


def cofactor_insertion_matrix(internal_edges):
    """Columns are e_a^(u) tensor H_(U-u); B_U is its transpose."""
    columns = []
    cofactors = {}
    for site in U:
        other = tuple(vertex for vertex in U if vertex != site)
        cofactors[site] = matching_tensor(other, internal_edges)
        for color in range(Q):
            columns.append(
                insert_one_site(site, color, other, cofactors[site])
            )
    return sp.Matrix.hstack(*columns), cofactors


def target_matrix():
    """Columns g_(U,r)=e_r^tensor5."""
    result = sp.zeros(Q ** len(U), Q)
    all_words = words(U)
    positions = {word: index for index, word in enumerate(all_words)}
    for color in range(Q):
        result[positions[(color,) * len(U)], color] = 1
    return result


def sparse_separating_functional(slice_matrix, target_column):
    """Return beta with S^T beta=0 and target_column^T beta=1.

    The support is a nonsingular row minor of [S | target], so no large
    parametrized nullspace computation is needed.
    """
    augmented = slice_matrix.row_join(target_column)
    if augmented.rank() != slice_matrix.rank() + 1:
        raise ValueError("the chosen target column already lies in the slice space")
    _rref, pivot_rows = augmented.T.rref()
    rank = augmented.rank()
    pivot_rows = pivot_rows[:rank]
    square = augmented.extract(pivot_rows, range(augmented.cols))
    assert square.rows == square.cols == rank
    values = square.T.inv()[:, -1]
    beta = sp.zeros(augmented.rows, 1)
    for row, value in zip(pivot_rows, values, strict=True):
        beta[row] = value
    assert slice_matrix.T * beta == sp.zeros(slice_matrix.cols, 1)
    assert (target_column.T * beta)[0] == 1
    return beta


def target_defect_dimension(slice_matrix, target):
    intersection = (
        slice_matrix.rank()
        + target.rank()
        - slice_matrix.row_join(target).rank()
    )
    image_dimension = target.rank() - intersection

    # Independently compute rank(delta restricted to ker B) without forming
    # a 228-vector nullspace: it is the rank gained by the target rows over B.
    b_map = slice_matrix.T
    delta = target.T
    restriction_rank = b_map.col_join(delta).rank() - b_map.rank()
    assert image_dimension == restriction_rank
    return image_dimension, intersection


def boundary_response_columns(all_edges, cofactors):
    """Gamma columns K_u[:,a] in lexicographic C-word order."""
    c_words = words(C)
    columns = []
    for exposed in U:
        for exposed_color in range(Q):
            column = []
            for c_word in c_words:
                local = dict(zip(C, c_word, strict=True))
                value = sp.S.Zero
                for crossing_vertex in C:
                    remaining = tuple(
                        vertex for vertex in C if vertex != crossing_vertex
                    )
                    value += edge_entry(
                        all_edges,
                        remaining[0],
                        remaining[1],
                        local[remaining[0]],
                        local[remaining[1]],
                    ) * edge_entry(
                        all_edges,
                        crossing_vertex,
                        exposed,
                        local[crossing_vertex],
                        exposed_color,
                    )
                column.append(sp.expand(value))
            columns.append(sp.Matrix(column))
    assert len(columns) == len(U) * Q
    return sp.Matrix.hstack(*columns)


def direct_one_crossing_flattening(all_edges):
    """Enumerate the 45 one-cross matchings independently."""
    c_set = set(C)
    crossing_matchings = tuple(
        matching
        for matching in perfect_matchings(B)
        if sum(
            (left in c_set) != (right in c_set)
            for left, right in matching
        )
        == 1
    )
    assert len(crossing_matchings) == 45

    result = sp.zeros(Q ** len(C), Q ** len(U))
    for row, c_word in enumerate(words(C)):
        for column, u_word in enumerate(words(U)):
            local = dict(zip(C, c_word, strict=True))
            local.update(zip(U, u_word, strict=True))
            value = sp.S.Zero
            for matching in crossing_matchings:
                term = sp.S.One
                for left, right in matching:
                    term *= edge_entry(
                        all_edges, left, right, local[left], local[right]
                    )
                value += term
            result[row, column] = sp.expand(value)
    return result


def main():
    internal_edges = dense_integral_edges(U, seed=20260726)
    slice_matrix, cofactors = cofactor_insertion_matrix(internal_edges)
    target = target_matrix()

    slice_rank = slice_matrix.rank()
    defect_dimension, intersection_dimension = target_defect_dimension(
        slice_matrix, target
    )
    assert slice_rank == 15
    assert defect_dimension > 0

    chosen_color = next(
        color
        for color in range(Q)
        if slice_matrix.row_join(target[:, color]).rank() > slice_rank
    )
    beta = sparse_separating_functional(
        slice_matrix, target[:, chosen_color]
    )
    delta_beta = target.T * beta
    assert delta_beta != sp.zeros(Q, 1)

    all_edges = dict(internal_edges)
    all_edges.update(dense_integral_edges(C, seed=20260727))
    cross_rng = Random(20260728)
    for left in U:
        for right in C:
            edge = tuple(sorted((left, right)))
            all_edges[edge] = sp.Matrix(
                Q,
                Q,
                [cross_rng.randrange(-2, 3) for _ in range(Q * Q)],
            )

    gamma = boundary_response_columns(all_edges, cofactors)
    b_map = slice_matrix.T
    factored = gamma * b_map
    direct = direct_one_crossing_flattening(all_edges)
    assert factored == direct
    assert b_map * beta == sp.zeros(len(U) * Q, 1)
    assert factored * beta == sp.zeros(Q ** len(C), 1)

    print("exact universal-cofactor audit: PASS")
    print(f"rank S_U = {slice_rank} of {len(U) * Q}")
    print(
        "dim(G_U intersection S_U) =",
        intersection_dimension,
        "; dim delta_U(ker B_U) =",
        defect_dimension,
    )
    print(
        f"constructed beta with {sum(value != 0 for value in beta)} nonzero "
        f"coordinates and delta(beta)={tuple(delta_beta)}"
    )
    print("verified F_1 = Gamma B_U against the sum of all 45 one-cross matchings")


if __name__ == "__main__":
    main()
