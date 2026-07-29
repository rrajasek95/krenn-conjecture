#!/usr/bin/env python3
"""Exact audits for the six-site hafnian norm bound and slack family.

The script uses only rational arithmetic and Gaussian elimination over F_19.
It certifies the finite incidence counts in the weighted-AM--GM proof, the
symbolic constant/mixed coefficients of the algebraic family, its isotropy,
and maximal star/triangle/full derivative ranks at a point of the family.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from itertools import combinations, product


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    u = vertices[0]
    for position, v in enumerate(vertices[1:], 1):
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(rest):
            yield ((u, v),) + tail


def audit_amgm_incidence_counts():
    vertices = tuple(range(6))
    edges = tuple(combinations(vertices, 2))
    cycles = []
    for omitted_edge in edges:
        remaining = tuple(v for v in vertices if v not in omitted_edge)
        pairings = tuple(perfect_matchings(remaining))
        assert len(pairings) == 3
        for left, right in combinations(pairings, 2):
            cycle_edges = frozenset(left + right)
            assert len(cycle_edges) == 4
            cycles.append((omitted_edge, cycle_edges))
    assert len(cycles) == 45

    edge_counts = Counter()
    adjacent_counts = Counter()
    disjoint_counts = Counter()
    for _, cycle_edges in cycles:
        for edge in cycle_edges:
            edge_counts[edge] += 1
        for left, right in combinations(sorted(cycle_edges), 2):
            key = (left, right)
            if set(left) & set(right):
                adjacent_counts[key] += 1
            else:
                disjoint_counts[key] += 1

    all_adjacent = {
        pair for pair in combinations(edges, 2) if set(pair[0]) & set(pair[1])
    }
    all_disjoint = {
        pair for pair in combinations(edges, 2) if not set(pair[0]) & set(pair[1])
    }
    assert len(all_adjacent) == 60
    assert len(all_disjoint) == 45
    assert set(adjacent_counts) == all_adjacent
    assert set(disjoint_counts) == all_disjoint
    assert set(edge_counts.values()) == {12}
    assert set(adjacent_counts.values()) == {3}
    assert set(disjoint_counts.values()) == {2}


# Sparse Q[a,b] polynomials, enough to audit the displayed fibers.
def pconst(value):
    value = Fraction(value)
    return {} if value == 0 else {(0, 0): value}


def pmono(a_power, b_power, coefficient=1):
    coefficient = Fraction(coefficient)
    return {} if coefficient == 0 else {(a_power, b_power): coefficient}


def padd(left, right):
    answer = dict(left)
    for monomial, coefficient in right.items():
        answer[monomial] = answer.get(monomial, Fraction(0)) + coefficient
        if answer[monomial] == 0:
            del answer[monomial]
    return answer


def pmul(left, right):
    answer = {}
    for (ai, bi), x in left.items():
        for (aj, bj), y in right.items():
            monomial = (ai + aj, bi + bj)
            answer[monomial] = answer.get(monomial, Fraction(0)) + x * y
    return {key: value for key, value in answer.items() if value}


FACTORS = (
    ((0, 1), (2, 3), (4, 5)),
    ((0, 5), (1, 2), (3, 4)),
    ((0, 2), (1, 4), (3, 5)),
    ((0, 3), (1, 5), (2, 4)),
    ((0, 4), (1, 3), (2, 5)),
)
NEGATIVE_EDGES = {(0, 1), (1, 2), (2, 3)}
N_MATRIX = (
    (Fraction(1), Fraction(-2, 3), Fraction(2)),
    (Fraction(2), Fraction(1), Fraction(-2, 3)),
    (Fraction(-2, 3), Fraction(2), Fraction(1)),
)


def family_matrices_polynomial():
    matrices = {}
    for edge in FACTORS[0] + FACTORS[1]:
        sign = -1 if edge in NEGATIVE_EDGES else 1
        matrices[edge] = tuple(
            tuple(pmono(1, 0, sign * entry) for entry in row)
            for row in N_MATRIX
        )
    for color, factor in enumerate(FACTORS[2:]):
        matrix = tuple(
            tuple(pmono(0, 1) if i == color == j else {} for j in range(3))
            for i in range(3)
        )
        for edge in factor:
            matrices[edge] = matrix
    return matrices


def coefficient_polynomial(matrices, coloring):
    answer = {}
    for matching in perfect_matchings(range(6)):
        term = pconst(1)
        for u, v in matching:
            term = pmul(term, matrices[(u, v)][coloring[u]][coloring[v]])
        answer = padd(answer, term)
    return answer


def transpose(matrix):
    return tuple(tuple(matrix[i][j] for i in range(3)) for j in range(3))


def rational_matmul(left, right):
    return tuple(
        tuple(sum(left[i][k] * right[k][j] for k in range(3)) for j in range(3))
        for i in range(3)
    )


def audit_family_symbolics():
    # N is (7/3) times an orthogonal matrix and has diagonal one.
    gram = rational_matmul(N_MATRIX, transpose(N_MATRIX))
    target_gram = tuple(
        tuple(Fraction(49, 9) if i == j else Fraction(0) for j in range(3))
        for i in range(3)
    )
    assert gram == target_gram
    assert rational_matmul(transpose(N_MATRIX), N_MATRIX) == target_gram
    assert tuple(N_MATRIX[i][i] for i in range(3)) == (1, 1, 1)

    matrices = family_matrices_polynomial()
    pure_value = padd(pmono(0, 3), pmono(2, 1, -1))
    for color in range(3):
        assert coefficient_polynomial(matrices, (color,) * 6) == pure_value

    # One mixed fiber cancels identically, while another is visibly nonzero.
    assert coefficient_polynomial(matrices, (0, 0, 0, 1, 1, 1)) == {}
    assert coefficient_polynomial(matrices, (0, 0, 0, 0, 0, 1)) == pmono(
        2, 1, Fraction(2, 3)
    )

    # The signs give products +,-,+,+,+ on the five factors and - on each
    # fourth matching in P union P' union Q_i.
    def sign_product(matching):
        answer = 1
        for edge in matching:
            if edge in NEGATIVE_EDGES:
                answer *= -1
        return answer

    assert tuple(sign_product(factor) for factor in FACTORS) == (1, -1, 1, 1, 1)
    fourth = (
        ((0, 5), (1, 4), (2, 3)),
        ((0, 3), (1, 2), (4, 5)),
        ((0, 1), (2, 5), (3, 4)),
    )
    assert tuple(sign_product(matching) for matching in fourth) == (-1, -1, -1)


def rank_mod_prime(matrix, prime):
    rows = [[entry % prime for entry in row] for row in matrix]
    pivot_row = 0
    for column in range(len(rows[0])):
        pivot = next(
            (row for row in range(pivot_row, len(rows)) if rows[row][column]),
            None,
        )
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        inverse = pow(rows[pivot_row][column], -1, prime)
        rows[pivot_row] = [value * inverse % prime for value in rows[pivot_row]]
        for row in range(len(rows)):
            if row != pivot_row and rows[row][column]:
                multiplier = rows[row][column]
                rows[row] = [
                    (x - multiplier * y) % prime
                    for x, y in zip(rows[row], rows[pivot_row])
                ]
        pivot_row += 1
        if pivot_row == len(rows):
            break
    return pivot_row


def audit_block_ranks_mod19():
    # The specialization a=1, b=6 is on b^3-a^2 b=1 modulo 19.
    prime = 19
    a_value, b_value = 1, 6
    assert (b_value**3 - a_value**2 * b_value) % prime == 1
    inv3 = pow(3, -1, prime)
    n_mod = (
        (1, -2 * inv3 % prime, 2),
        (2, 1, -2 * inv3 % prime),
        (-2 * inv3 % prime, 2, 1),
    )
    matrices = {}
    for edge in FACTORS[0] + FACTORS[1]:
        sign = -1 if edge in NEGATIVE_EDGES else 1
        matrices[edge] = tuple(
            tuple(sign * a_value * entry % prime for entry in row) for row in n_mod
        )
    for color, factor in enumerate(FACTORS[2:]):
        matrix = tuple(
            tuple(b_value if i == color == j else 0 for j in range(3))
            for i in range(3)
        )
        for edge in factor:
            matrices[edge] = matrix

    def subset_tensor(vertices):
        vertices = tuple(vertices)
        answer = {}
        for coloring in product(range(3), repeat=len(vertices)):
            local = dict(zip(vertices, coloring))
            value = 0
            for matching in perfect_matchings(vertices):
                term = 1
                for edge in matching:
                    term *= matrices[edge][local[edge[0]]][local[edge[1]]]
                value += term
            answer[coloring] = value % prime
        return answer

    full = subset_tensor(range(6))
    assert [full[(color,) * 6] for color in range(3)] == [1, 1, 1]

    edges = tuple(combinations(range(6), 2))
    cofactors = {
        edge: subset_tensor(v for v in range(6) if v not in edge) for edge in edges
    }
    full_colorings = tuple(product(range(3), repeat=6))

    def block_matrix(block_edges):
        columns = []
        for edge in block_edges:
            rest = tuple(v for v in range(6) if v not in edge)
            for i in range(3):
                for j in range(3):
                    columns.append(
                        [
                            cofactors[edge][tuple(coloring[v] for v in rest)]
                            if (coloring[edge[0]], coloring[edge[1]]) == (i, j)
                            else 0
                            for coloring in full_colorings
                        ]
                    )
        return [list(row) for row in zip(*columns)]

    star_ranks = []
    for vertex in range(6):
        star = tuple(edge for edge in edges if vertex in edge)
        star_ranks.append(rank_mod_prime(block_matrix(star), prime))
    assert star_ranks == [45] * 6

    triangle_ranks = []
    for triangle in combinations(range(6), 3):
        triangle_ranks.append(
            rank_mod_prime(block_matrix(tuple(combinations(triangle, 2))), prime)
        )
    assert triangle_ranks == [27] * 20

    # Five scalar vertex-gauge directions are always in the kernel.
    assert rank_mod_prime(block_matrix(edges), prime) == 135 - 5


def main():
    audit_amgm_incidence_counts()
    audit_family_symbolics()
    audit_block_ranks_mod19()
    print("PASS: six-site sharp-hafnian incidence certificate")
    print("PASS: exact isotropic pure-normalized slack family")
    print("PASS: star 45, triangle 27, full derivative 130 over F_19")


if __name__ == "__main__":
    main()
