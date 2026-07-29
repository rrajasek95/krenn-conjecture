#!/usr/bin/env python3
"""Exact audit of the arbitrary-row five-hole decomposition.

This is a combinatorial identity checker, not a putative GHZ realization.
All arithmetic is rational and all 105 perfect matchings are enumerated.
"""

from fractions import Fraction as Q
from itertools import combinations, permutations, product

import sympy as sp


P, QV, K = 0, 1, 2
U = tuple(range(3, 8))
VERTICES = tuple(range(8))
COLORS = tuple(range(3))
WORDS = tuple(product(COLORS, repeat=5))


def zero_matrix():
    return [[Q(0) for _ in COLORS] for _ in COLORS]


def transpose(matrix):
    return [list(row) for row in zip(*matrix)]


def matvec_transpose(matrix, vector):
    return [sum(matrix[i][j] * vector[i] for i in COLORS)
            for j in COLORS]


def dot(left, right):
    return sum(a * b for a, b in zip(left, right))


def cross(left, right):
    return [
        left[1] * right[2] - left[2] * right[1],
        left[2] * right[0] - left[0] * right[2],
        left[0] * right[1] - left[1] * right[0],
    ]


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1:]
        for matching in perfect_matchings(rest):
            yield ((first, second),) + matching


MATCHINGS = tuple(perfect_matchings(VERTICES))
assert len(MATCHINGS) == 105


def matrices():
    answer = {}
    for u, v in combinations(VERTICES, 2):
        answer[u, v] = [
            [Q(((u + 2) * (i + 1) + (v + 3) * (j + 2)
                 + 2 * i * j + 1) % 11 - 5)
             for j in COLORS]
            for i in COLORS
        ]
    # Make the incidence equation transparent and choose alpha,beta below
    # with alpha^T beta=0.
    answer[P, QV] = [[Q(int(i == j)) for j in COLORS] for i in COLORS]
    return answer


A = matrices()


def edge_matrix(u, v):
    return A[u, v] if u < v else transpose(A[v, u])


ALPHA = [Q(1), Q(2), Q(1)]
BETA = [Q(3), Q(4), Q(-11)]
assert dot(ALPHA, BETA) == 0


def star(capped_vertex, outside_vertex, covector):
    return matvec_transpose(edge_matrix(capped_vertex, outside_vertex),
                            covector)


X = {i: star(P, i, ALPHA) for i in (K,) + U}
Y = {i: star(QV, i, BETA) for i in (K,) + U}


def edge_value(u, v, color_u, color_v):
    return edge_matrix(u, v)[color_u][color_v]


def h4_value(vertices, coloring):
    total = Q(0)
    for matching in perfect_matchings(vertices):
        value = Q(1)
        for u, v in matching:
            value *= edge_value(u, v, coloring[u], coloring[v])
        total += value
    return total


def one_cross_response(star_rows, word):
    coloring = dict(zip(U, word))
    total = Q(0)
    for i in U:
        rest = tuple(u for u in U if u != i)
        total += star_rows[i][coloring[i]] * h4_value(rest, coloring)
    return total


def d_rows(z):
    return {i: star(K, i, z) for i in U}


def three_cross_by_internal_edge(z, word):
    coloring = dict(zip(U, word))
    d = d_rows(z)
    total = Q(0)
    for a, b in combinations(U, 2):
        complement = tuple(i for i in U if i not in (a, b))
        internal = edge_value(a, b, coloring[a], coloring[b])
        permanent = Q(0)
        for assignment in permutations(complement):
            u, v, w = assignment
            permanent += (X[u][coloring[u]] * Y[v][coloring[v]]
                          * d[w][coloring[w]])
        total += internal * permanent
    return total


def three_cross_by_star_pair(z, word):
    coloring = dict(zip(U, word))
    d = d_rows(z)
    total = Q(0)
    for u, v in combinations(U, 2):
        correction = (X[u][coloring[u]] * Y[v][coloring[v]]
                      + Y[u][coloring[u]] * X[v][coloring[v]])
        rest = tuple(i for i in U if i not in (u, v))
        residual = Q(0)
        for w in rest:
            a, b = tuple(i for i in rest if i != w)
            residual += (d[w][coloring[w]]
                         * edge_value(a, b, coloring[a], coloring[b]))
        total += correction * residual
    return total


def direct_contraction(z, word):
    coloring = dict(zip(U, word))
    caps = {P: ALPHA, QV: BETA, K: z}
    total = Q(0)
    for matching in MATCHINGS:
        value = Q(1)
        for u, v in matching:
            u_capped = u in caps
            v_capped = v in caps
            matrix = edge_matrix(u, v)
            if u_capped and v_capped:
                value *= sum(caps[u][i] * matrix[i][j] * caps[v][j]
                             for i in COLORS for j in COLORS)
            elif u_capped:
                value *= sum(caps[u][i] * matrix[i][coloring[v]]
                             for i in COLORS)
            elif v_capped:
                value *= sum(matrix[coloring[u]][j] * caps[v][j]
                             for j in COLORS)
            else:
                value *= matrix[coloring[u]][coloring[v]]
        total += value
    return total


def rhs(z, word):
    return (
        dot(X[K], z) * one_cross_response(Y, word)
        + dot(Y[K], z) * one_cross_response(X, word)
        + three_cross_by_internal_edge(z, word)
    )


def main():
    rows = ([Q(1), Q(0), Q(0)], [Q(0), Q(1), Q(0)],
            [Q(0), Q(0), Q(1)], [Q(2), Q(-3), Q(5)])
    for z in rows:
        for word in WORDS:
            direct = direct_contraction(z, word)
            assert direct == rhs(z, word)
            assert (three_cross_by_internal_edge(z, word)
                    == three_cross_by_star_pair(z, word))

    gamma = cross(X[K], Y[K])
    assert gamma != [Q(0), Q(0), Q(0)]
    assert dot(X[K], gamma) == dot(Y[K], gamma) == 0
    for word in WORDS:
        assert direct_contraction(gamma, word) == three_cross_by_internal_edge(
            gamma, word
        )

    # Symbolic audit of the triangle-response equations (14).
    sx = sp.symbols("s1:4")
    tx = sp.symbols("t1:4")
    lx, ly = sp.symbols("Lx Ly")
    equations_s = sp.Matrix([
        sx[0] + sx[1],
        sx[0] + sx[2] - lx,
        sx[1] + sx[2],
    ])
    equations_t = sp.Matrix([
        tx[1] + tx[2] - ly,
        tx[0] + tx[2],
        tx[0] + tx[1],
    ])
    solution_s = sp.solve(tuple(equations_s), sx, dict=True)
    solution_t = sp.solve(tuple(equations_t), tx, dict=True)
    assert solution_s == [{sx[0]: lx / 2, sx[1]: -lx / 2,
                           sx[2]: lx / 2}]
    assert solution_t == [{tx[0]: -ly / 2, tx[1]: ly / 2,
                           tx[2]: ly / 2}]

    print("verified arbitrary-row one-cross plus shared three-cross decomposition")
    print("verified internal-edge/permanent and star-pair regroupings")
    print("verified common-annihilator specialization kills both fixed responses")
    print("verified the unique three-hole triangle-response normal form")


if __name__ == "__main__":
    main()
