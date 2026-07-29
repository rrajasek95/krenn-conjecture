#!/usr/bin/env python3
"""Exact audit of the transverse one-hole cofactor kernel."""

from __future__ import annotations

from itertools import product

import sympy as sp


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for j in range(1, len(vertices)):
        second = vertices[j]
        rest = vertices[1:j] + vertices[j + 1 :]
        for matching in perfect_matchings(rest):
            yield ((first, second),) + matching


# A linear form is represented by the index of a coordinate variable.
# These ordered bases make the two all-equal bit strings have the same xyz
# product, so kappa=000-111.
PLANE_BASES = ((1, 2), (2, 0), (0, 1))


def exponent(indices):
    return tuple(indices.count(i) for i in range(3))


def multiplication_matrix(number_of_planes: int):
    bases = PLANE_BASES[:number_of_planes]
    columns = list(product((0, 1), repeat=number_of_planes))
    row_keys = sorted(
        {exponent([bases[u][bits[u]] for u in range(number_of_planes)]) for bits in columns}
    )
    row_index = {key: i for i, key in enumerate(row_keys)}
    matrix = sp.zeros(len(row_keys), len(columns))
    for j, bits in enumerate(columns):
        key = exponent([bases[u][bits[u]] for u in range(number_of_planes)])
        matrix[row_index[key], j] = 1
    return matrix, columns


def combined_one_hole_matrix():
    columns = list(product((0, 1), repeat=6))
    row_keys = set()
    column_rows = []
    for bits in columns:
        entries = []
        for hole in range(6):
            if hole < 3:
                beta_indices = [PLANE_BASES[u][bits[u]] for u in range(3) if u != hole]
                alpha_indices = [PLANE_BASES[v - 3][bits[v]] for v in range(3, 6)]
            else:
                beta_indices = [PLANE_BASES[u][bits[u]] for u in range(3)]
                alpha_indices = [
                    PLANE_BASES[v - 3][bits[v]] for v in range(3, 6) if v != hole
                ]
            key = (hole, bits[hole], exponent(alpha_indices), exponent(beta_indices))
            row_keys.add(key)
            entries.append(key)
        column_rows.append(entries)
    row_keys = sorted(row_keys)
    row_index = {key: i for i, key in enumerate(row_keys)}
    matrix = sp.zeros(len(row_keys), len(columns))
    for j, entries in enumerate(column_rows):
        for key in entries:
            matrix[row_index[key], j] = 1
    return matrix, columns


def matching_tensor(edges: dict[tuple[int, int], sp.Matrix]):
    tensor = {}
    supported = []
    for matching in perfect_matchings(tuple(range(6))):
        nonzero_term = False
        for coloring in product((0, 1), repeat=6):
            value = sp.Integer(1)
            for u, v in matching:
                value *= edges.get((u, v), sp.zeros(2, 2))[coloring[u], coloring[v]]
            if value:
                nonzero_term = True
                tensor[coloring] = tensor.get(coloring, 0) + value
        if nonzero_term:
            supported.append(matching)
    return {key: value for key, value in tensor.items() if value}, supported


def main():
    pair_map, _ = multiplication_matrix(2)
    assert pair_map.rank() == 4

    triple_map, triple_columns = multiplication_matrix(3)
    assert triple_map.rank() == 7
    kappa3 = sp.zeros(8, 1)
    kappa3[triple_columns.index((0, 0, 0))] = 1
    kappa3[triple_columns.index((1, 1, 1))] = -1
    assert triple_map * kappa3 == sp.zeros(triple_map.rows, 1)
    triple_kernel = triple_map.nullspace()
    assert len(triple_kernel) == 1
    assert sp.Matrix.hstack(triple_kernel[0], kappa3).rank() == 1

    combined, columns = combined_one_hole_matrix()
    assert combined.rank() == 63
    web = sp.zeros(64, 1)
    for bits, coefficient in {
        (0, 0, 0, 0, 0, 0): 1,
        (0, 0, 0, 1, 1, 1): -1,
        (1, 1, 1, 0, 0, 0): -1,
        (1, 1, 1, 1, 1, 1): 1,
    }.items():
        web[columns.index(bits)] = coefficient
    assert combined * web == sp.zeros(combined.rows, 1)
    combined_kernel = combined.nullspace()
    assert len(combined_kernel) == 1
    assert sp.Matrix.hstack(combined_kernel[0], web).rank() == 1

    e00 = sp.Matrix([[1, 0], [0, 0]])
    e11 = sp.Matrix([[0, 0], [0, 1]])
    e01 = sp.Matrix([[0, 1], [0, 0]])
    e10 = sp.Matrix([[0, 0], [1, 0]])
    edges = {
        (0, 1): e00,
        (0, 2): e11,
        (4, 5): e00,
        (3, 5): e11,
        (2, 3): e00,
        (2, 4): -e01,
        (1, 3): -e10,
        (1, 4): e11,
    }
    tensor, supported = matching_tensor(edges)
    expected_matchings = {
        ((0, 1), (2, 3), (4, 5)),
        ((0, 1), (2, 4), (3, 5)),
        ((0, 2), (1, 3), (4, 5)),
        ((0, 2), (1, 4), (3, 5)),
    }
    assert set(supported) == expected_matchings
    expected_tensor = {
        (0, 0, 0, 0, 0, 0): 1,
        (0, 0, 0, 1, 1, 1): -1,
        (1, 1, 1, 0, 0, 0): -1,
        (1, 1, 1, 1, 1, 1): 1,
    }
    assert tensor == expected_tensor
    print("verified transverse one-hole kernel and exact matching web")


if __name__ == "__main__":
    main()
