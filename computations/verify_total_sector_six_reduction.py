#!/usr/bin/env python3
"""Exact audit for the total-sector six-site reduction note.

The source used here is deliberately *not* an exact GHZ source.  It is an
exact countermodel to the claim that active coordinate anchors, normalized
constant fibres, and freedom to choose the five exposed vertices force the
total-sector separation condition.

All matrices have integer entries.  Full row rank modulo PRIME certifies
full row rank over Q.  The six non-full cuts are then checked by exact
rational row reduction in SymPy.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations, product

from sympy import Matrix


N = 8
Q = 3
PRIME = 1_000_003
ZERO = ((0, 0, 0), (0, 0, 0), (0, 0, 0))
S = ((0, 1, 0), (0, 0, 1), (1, 0, 0))
S2 = ((0, 0, 1), (1, 0, 0), (0, 1, 0))


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for pos in range(1, len(vertices)):
        second = vertices[pos]
        rest = vertices[1:pos] + vertices[pos + 1 :]
        for matching in perfect_matchings(rest):
            yield ((first, second),) + matching


def round_robin_factors(n):
    """The standard one-factorization on infinity union Z/(n-1)."""
    infinity = n - 1
    modulus = n - 1
    factors = []
    for r in range(modulus):
        factor = [tuple(sorted((infinity, r)))]
        for k in range(1, n // 2):
            factor.append(tuple(sorted(((r + k) % modulus, (r - k) % modulus))))
        factors.append(tuple(sorted(factor)))
    return tuple(factors)


FACTORS = round_robin_factors(N)
MATCHINGS = tuple(perfect_matchings(range(N)))
COLORINGS_3 = tuple(product(range(Q), repeat=3))
COLORINGS_5 = tuple(product(range(Q), repeat=5))


def coordinate_matrix(color):
    return tuple(
        tuple(int(i == color and j == color) for j in range(Q))
        for i in range(Q)
    )


def build_source():
    matrices = {}
    for edge in FACTORS[0]:
        matrices[edge] = S
    for edge in FACTORS[1]:
        matrices[edge] = S2
    for color, factor in enumerate(FACTORS[2:5]):
        for edge in factor:
            matrices[edge] = coordinate_matrix(color)
    return matrices


MATRICES = build_source()


def coefficient(coloring, vertices=tuple(range(N))):
    value = 0
    for matching in perfect_matchings(vertices):
        term = 1
        for u, v in matching:
            term *= MATRICES.get(tuple(sorted((u, v))), ZERO)[coloring[u]][coloring[v]]
            if term == 0:
                break
        value += term
    return value


def total_high_sector_flattening(C):
    """Rows are C-colors, columns are U-colors, for T_3+T_5."""
    C = tuple(C)
    C_set = set(C)
    U = tuple(v for v in range(N) if v not in C_set)
    rows = []
    for c_colors in COLORINGS_3:
        fixed = dict(zip(C, c_colors))
        row = []
        for u_colors in COLORINGS_5:
            coloring = fixed | dict(zip(U, u_colors))
            value = 0
            for matching in MATCHINGS:
                crossing = sum((u in C_set) != (v in C_set) for u, v in matching)
                if crossing < 3:
                    continue
                term = 1
                for u, v in matching:
                    term *= MATRICES.get((u, v), ZERO)[coloring[u]][coloring[v]]
                    if term == 0:
                        break
                value += term
            row.append(value)
        rows.append(row)
    return rows


def rank_mod_prime(rows, prime=PRIME):
    matrix = [[entry % prime for entry in row] for row in rows]
    nrows = len(matrix)
    ncols = len(matrix[0])
    pivot_row = 0
    for column in range(ncols):
        pivot = next(
            (row for row in range(pivot_row, nrows) if matrix[row][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        inverse = pow(matrix[pivot_row][column], prime - 2, prime)
        matrix[pivot_row] = [entry * inverse % prime for entry in matrix[pivot_row]]
        for row in range(nrows):
            if row == pivot_row or matrix[row][column] == 0:
                continue
            multiple = matrix[row][column]
            matrix[row] = [
                (entry - multiple * pivot_entry) % prime
                for entry, pivot_entry in zip(matrix[row], matrix[pivot_row])
            ]
        pivot_row += 1
        if pivot_row == nrows:
            break
    return pivot_row


def diagonal_columns():
    # Lexicographic color order puts 000,111,222 at rows 0,13,26.
    return Matrix(27, 3, lambda row, col: int(row == (0, 13, 26)[col]))


def verify_factorization_and_anchors():
    first_five_edges = [edge for factor in FACTORS[:5] for edge in factor]
    assert len(first_five_edges) == 20
    assert len(set(first_five_edges)) == 20
    for factor in FACTORS[:5]:
        assert sorted(v for edge in factor for v in edge) == list(range(N))

    # Every vertex has one E_ii edge for every i, and every such edge is
    # active: after deleting it, the remaining support still has a perfect
    # matching.  Nonnegative entries then prevent cancellation of the
    # corresponding complementary coefficient.
    support = set(MATRICES)
    for color, factor in enumerate(FACTORS[2:5]):
        expected = coordinate_matrix(color)
        for vertex in range(N):
            incident = [edge for edge in factor if vertex in edge]
            assert len(incident) == 1
            assert MATRICES[incident[0]] == expected
        for edge in factor:
            complement = tuple(v for v in range(N) if v not in edge)
            assert any(
                all(tuple(sorted(pair)) in support for pair in matching)
                for matching in perfect_matchings(complement)
            )


def verify_constant_fibres_and_nonexample():
    for color in range(Q):
        assert coefficient((color,) * N) == 1

    # State explicitly in executable form that this source has not solved
    # the conjecture: a mixed coefficient survives.
    mixed = (0, 0, 0, 0, 0, 1, 2, 2)
    assert coefficient(mixed) == 1


def verify_all_five_sets():
    rank_intersection_histogram = Counter()
    exceptional = {}
    diagonal = diagonal_columns()

    for C in combinations(range(N), 3):
        rows = total_high_sector_flattening(C)
        modular_rank = rank_mod_prime(rows)
        if modular_rank == 27:
            # A nonzero 27-minor modulo PRIME is a nonzero integer minor,
            # hence the left Schmidt space is all of Q^27.
            rational_rank = 27
            intersection_dimension = 3
        else:
            matrix = Matrix(rows)
            rational_rank = matrix.rank()
            augmented_rank = matrix.row_join(diagonal).rank()
            intersection_dimension = 3 + rational_rank - augmented_rank
            exceptional[C] = (rational_rank, intersection_dimension)

        assert intersection_dimension > 0, C
        rank_intersection_histogram[(rational_rank, intersection_dimension)] += 1

    assert rank_intersection_histogram == Counter(
        {
            (27, 3): 50,
            (23, 3): 3,
            (24, 3): 1,
            (25, 3): 1,
            (21, 2): 1,
        }
    )
    assert exceptional == {
        (0, 1, 7): (23, 3),
        (0, 2, 7): (23, 3),
        (1, 3, 6): (24, 3),
        (1, 6, 7): (25, 3),
        (2, 4, 5): (21, 2),
        (3, 4, 5): (23, 3),
    }

    # On the sole two-dimensional intersection, the two displayed diagonal
    # basis vectors themselves lie in the total high-sector column space.
    C = (2, 4, 5)
    matrix = Matrix(total_high_sector_flattening(C))
    rank = matrix.rank()
    for row_index in (0, 26):
        assert matrix.row_join(Matrix.eye(27)[:, row_index]).rank() == rank
    assert matrix.row_join(Matrix.eye(27)[:, 13]).rank() == rank + 1

    return rank_intersection_histogram


def main():
    verify_factorization_and_anchors()
    verify_constant_fibres_and_nonexample()
    histogram = verify_all_five_sets()
    print("verified active E_ii anchors and three normalized constant fibres")
    print("verified nonzero total-sector contamination for all 56 five-sets")
    print("(left rank, intersection dimension): count =", dict(histogram))


if __name__ == "__main__":
    main()
