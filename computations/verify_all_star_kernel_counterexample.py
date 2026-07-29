#!/usr/bin/env python3
"""Exact counterexample to an all-star-kernel diagonal-rigidity lemma.

The six-site binary source is a signed two-matching cancellation gadget
together with an all-y matching.  It realizes ``2 X + Y`` and every
nonzero scalar cell is tensor-active.  For every site i this script forms
the complete
monomer map

    F_i : direct_sum_(j != i) V_j -> tensor_(j != i) V_j,
    e_c^(j) |-> e_c^(j) tensor H_(B minus {i,j})(q),

over Q and reports its rank and a sparse exact kernel basis.
"""

from __future__ import annotations

import itertools
from fractions import Fraction


N = 6
VERTICES = tuple(range(N))
X, Y = range(2)
ZERO = ((0, 0), (0, 0))

# H(q)=2 X+Y.  The yx term from 01|23|45 is cancelled by the yx term from
# 02|13|45, while 05|12|34 supplies Y.
MATRICES = {
    (0, 1): ((1, 0), (1, 0)),
    (2, 3): ((1, 0), (0, 0)),
    (4, 5): ((2, 0), (0, 0)),
    (0, 2): ((0, 0), (-1, 0)),
    (1, 3): ((1, 0), (0, 0)),
    (0, 5): ((0, 0), (0, 1)),
    (1, 2): ((0, 0), (0, 1)),
    (3, 4): ((0, 0), (0, 1)),
}


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position, partner in enumerate(vertices[1:], 1):
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(rest):
            yield ((first, partner),) + tail


def tensor(vertices):
    vertices = tuple(vertices)
    answer = {}
    for colors in itertools.product((X, Y), repeat=len(vertices)):
        coloring = dict(zip(vertices, colors))
        value = 0
        for matching in perfect_matchings(vertices):
            term = 1
            for u, v in matching:
                term *= MATRICES.get((u, v), ZERO)[coloring[u]][coloring[v]]
            value += term
        answer[colors] = Fraction(value)
    return answer


def monomer_matrix(site):
    output_vertices = tuple(v for v in VERTICES if v != site)
    output_colorings = tuple(itertools.product((X, Y), repeat=N - 1))
    columns = tuple(
        (neighbor, color)
        for neighbor in output_vertices
        for color in (X, Y)
    )
    cofactors = {
        neighbor: tensor(v for v in output_vertices if v != neighbor)
        for neighbor in output_vertices
    }
    matrix = []
    for colors in output_colorings:
        coloring = dict(zip(output_vertices, colors))
        row = []
        for neighbor, color in columns:
            complement = tuple(v for v in output_vertices if v != neighbor)
            row.append(
                cofactors[neighbor][tuple(coloring[v] for v in complement)]
                if coloring[neighbor] == color
                else Fraction(0)
            )
        matrix.append(row)
    return columns, matrix


def rref_kernel(matrix):
    rows = [row[:] for row in matrix]
    column_count = len(rows[0])
    pivots = []
    cursor = 0
    for column in range(column_count):
        pivot = next(
            (row for row in range(cursor, len(rows)) if rows[row][column]),
            None,
        )
        if pivot is None:
            continue
        rows[cursor], rows[pivot] = rows[pivot], rows[cursor]
        scale = rows[cursor][column]
        rows[cursor] = [entry / scale for entry in rows[cursor]]
        for row in range(len(rows)):
            if row == cursor or not rows[row][column]:
                continue
            scale = rows[row][column]
            rows[row] = [
                left - scale * right
                for left, right in zip(rows[row], rows[cursor])
            ]
        pivots.append(column)
        cursor += 1
    free = tuple(column for column in range(column_count) if column not in pivots)
    kernel = []
    for free_column in free:
        vector = [Fraction(0)] * column_count
        vector[free_column] = 1
        for row, pivot in enumerate(pivots):
            vector[pivot] = -rows[row][free_column]
        kernel.append(tuple(vector))
    return tuple(pivots), tuple(kernel)


def sparse_vector(columns, vector):
    return {
        f"{neighbor}{'x' if color == X else 'y'}": value
        for (neighbor, color), value in zip(columns, vector)
        if value
    }


def main():
    full = tensor(VERTICES)
    for coloring, value in full.items():
        target = 2 if all(color == X for color in coloring) else 1 if all(color == Y for color in coloring) else 0
        assert value == target, (coloring, value)

    supported = tuple(
        matching
        for matching in perfect_matchings(VERTICES)
        if all(edge in MATRICES for edge in matching)
    )
    assert supported == (
        ((0, 1), (2, 3), (4, 5)),
        ((0, 2), (1, 3), (4, 5)),
        ((0, 5), (1, 2), (3, 4)),
    )
    for edge, matrix in MATRICES.items():
        complement = tuple(vertex for vertex in VERTICES if vertex not in edge)
        cofactor = tensor(complement)
        assert any(cofactor.values()), edge
        assert any(value for row in matrix for value in row), edge

    reports = {}
    for site in VERTICES:
        columns, matrix = monomer_matrix(site)
        pivots, kernel = rref_kernel(matrix)
        for vector in kernel:
            assert all(
                sum(entry * coefficient for entry, coefficient in zip(row, vector)) == 0
                for row in matrix
            )
        reports[site] = (len(pivots), len(kernel))
        print(
            f"site={site} rank={len(pivots)} nullity={len(kernel)} "
            f"kernel={[sparse_vector(columns, vector) for vector in kernel]}"
        )

    assert reports == {
        0: (7, 3),
        1: (8, 2),
        2: (9, 1),
        3: (8, 2),
        4: (7, 3),
        5: (8, 2),
    }
    # A target-preserving monomial gauge uses one common permutation of
    # x,y at every site.  Hence an xy cell remains off diagonal.  The two
    # displayed nonzero xy cells certify that this source is not gauge
    # equivalent to a diagonal one.
    assert MATRICES[(0, 1)][Y][X] and MATRICES[(0, 2)][Y][X]
    print("verified H(q)=2X+Y and nontrivial kernel at all six monomer maps")
    print("verified every nonzero scalar cell has a nonzero derivative tensor")
    print("the nonzero yx cells on 01 and 02 survive every allowed monomial gauge")


if __name__ == "__main__":
    main()
