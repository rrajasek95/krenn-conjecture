#!/usr/bin/env python3
"""Exact countermodel to all 504 pairwise one-hole identities."""

from __future__ import annotations

from collections import defaultdict
from itertools import combinations, product

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


def build_edges():
    e = [sp.eye(3)[:, i] for i in range(3)]
    outer = lambda x, y: x * y.T
    edges = {(i, j): sp.zeros(3, 3) for i in range(8) for j in range(i + 1, 8)}

    def put(i, j, matrix):
        edges[tuple(sorted((i, j)))] = matrix if i < j else matrix.T

    put(6, 7, sp.eye(3))
    for i, u in enumerate(range(3)):
        put(6, u, outer(e[i], e[i]))
        put(7, u, sp.eye(3))
    for i, v in enumerate(range(3, 6)):
        put(6, v, sp.eye(3))
        put(7, v, outer(e[i], e[i]))

    explicit = {
        (0, 1): outer(e[2], e[0]),
        (0, 2): outer(e[1], e[0]),
        (3, 5): outer(e[1], e[0]),
        (4, 5): outer(e[0], e[1]),
        (2, 3): -outer(e[1], e[2]),
        (2, 4): -outer(e[1], e[2]),
        (1, 3): -outer(e[2], e[2]),
        (1, 4): -outer(e[2], e[2]),
    }
    edges.update(explicit)
    return edges


EDGES = build_edges()


def oriented(u: int, v: int):
    return EDGES[(u, v)] if u < v else EDGES[(v, u)].T


def cross(a: sp.Matrix, b: sp.Matrix):
    return sp.Matrix(
        [
            a[1] * b[2] - a[2] * b[1],
            a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0],
        ]
    )


def scalar_hafnian(vertices, covectors):
    total = sp.Integer(0)
    for matching in perfect_matchings(tuple(vertices)):
        term = sp.Integer(1)
        for u, v in matching:
            term *= (covectors[u].T * oriented(u, v) * covectors[v])[0]
        total += term
    return sp.expand(total)


def one_site_partial(vertices, hole, covectors):
    out = sp.zeros(3, 1)
    for matching in perfect_matchings(tuple(vertices)):
        term = sp.Integer(1)
        vector = None
        for u, v in matching:
            matrix = oriented(u, v)
            if u == hole:
                vector = matrix * covectors[v]
            elif v == hole:
                vector = matrix.T * covectors[u]
            else:
                term *= (covectors[u].T * matrix * covectors[v])[0]
        out += term * vector
    return out.applyfunc(sp.expand)


def two_site_partial(vertices, w, z, covectors):
    out = sp.zeros(3, 3)
    for matching in perfect_matchings(tuple(vertices)):
        term = sp.Integer(1)
        vector_w = None
        vector_z = None
        direct = None
        for u, v in matching:
            matrix = oriented(u, v)
            if {u, v} == {w, z}:
                direct = matrix if (u, v) == (w, z) else matrix.T
            elif u == w:
                vector_w = matrix * covectors[v]
            elif v == w:
                vector_w = matrix.T * covectors[u]
            elif u == z:
                vector_z = matrix * covectors[v]
            elif v == z:
                vector_z = matrix.T * covectors[u]
            else:
                term *= (covectors[u].T * matrix * covectors[v])[0]
        out += term * (direct if direct is not None else vector_w * vector_z.T)
    return out.applyfunc(sp.expand)


def full_matching_tensor():
    tensor = defaultdict(int)
    for matching in perfect_matchings(tuple(range(8))):
        entries = []
        for u, v in matching:
            matrix = oriented(u, v)
            entries.append(
                [(i, j, int(matrix[i, j])) for i in range(3) for j in range(3) if matrix[i, j]]
            )
        if any(not edge_entries for edge_entries in entries):
            continue
        for choices in product(*entries):
            coloring = [None] * 8
            value = 1
            for (u, v), (i, j, coefficient) in zip(matching, choices):
                coloring[u] = i
                coloring[v] = j
                value *= coefficient
            tensor[tuple(coloring)] += value
    return {coloring: value for coloring, value in tensor.items() if value}


def main():
    alpha = sp.Matrix(sp.symbols("alpha0:3"))
    beta = sp.Matrix(sp.symbols("beta0:3"))
    variables = tuple(alpha) + tuple(beta)

    one_hole_count = 0
    two_hole_passes = []
    two_hole_failures = []
    central_residual = None

    for p, q in combinations(range(8), 2):
        remainder = [u for u in range(8) if u not in (p, q)]
        gammas = {
            u: cross(oriented(p, u).T * alpha, oriented(q, u).T * beta)
            for u in remainder
        }
        g = (alpha.T * oriented(p, q) * beta)[0]

        for hole in remainder:
            covectors = {u: gammas[u] for u in remainder if u != hole}
            partial = one_site_partial(remainder, hole, covectors)
            for r in range(3):
                lhs = alpha[r] * beta[r] * sp.prod(
                    gammas[u][r] for u in remainder if u != hole
                )
                residual = sp.Poly(sp.expand(lhs - g * partial[r]), *variables)
                assert residual.is_zero
                one_hole_count += 1

        for w, z in combinations(remainder, 2):
            contracted = [u for u in remainder if u not in (w, z)]
            covectors = {u: gammas[u] for u in contracted}
            lhs = sp.diag(
                *[
                    alpha[r]
                    * beta[r]
                    * sp.prod(gammas[u][r] for u in contracted)
                    for r in range(3)
                ]
            )
            quotient = two_site_partial(remainder, w, z, covectors)
            residual_hafnian = scalar_hafnian(contracted, covectors)
            xw = oriented(p, w).T * alpha
            xz = oriented(p, z).T * alpha
            yw = oriented(q, w).T * beta
            yz = oriented(q, z).T * beta
            correction = xw * yz.T + yw * xz.T
            residual = (lhs - g * quotient - residual_hafnian * correction).applyfunc(
                sp.expand
            )
            if residual == sp.zeros(3, 3):
                two_hole_passes.append((p, q, w, z))
            else:
                two_hole_failures.append((p, q, w, z))
            if (p, q, w, z) == (6, 7, 0, 3):
                central_residual = residual

    assert one_hole_count == 504

    tensor = full_matching_tensor()
    assert len(tensor) == 103
    assert tensor[(1, 0, 0, 0, 0, 1, 0, 0)] == 1
    assert tensor != {(r,) * 8: 1 for r in range(3)}

    assert len(two_hole_passes) == 404
    assert len(two_hole_failures) == 16
    assert all(
        (p, q, w, z) in two_hole_passes
        for p, q in combinations(range(6), 2)
        for w, z in combinations([u for u in range(8) if u not in (p, q)], 2)
    )
    expected_monomial = (
        alpha[0] * alpha[1] ** 2 * alpha[2] ** 2
        * beta[0] * beta[1] ** 2 * beta[2] ** 2
    )
    assert central_residual is not None
    assert sp.expand(central_residual[0, 0] - expected_monomial) == 0

    # Exact minimum-witness instance of Theorem 6.2 in the companion note.
    skew = (
        sp.Matrix([[0, 0, 0], [0, 0, 1], [0, -1, 0]]),
        sp.Matrix([[0, 0, -1], [0, 0, 0], [1, 0, 0]]),
        sp.Matrix([[0, 1, 0], [-1, 0, 0], [0, 0, 0]]),
    )
    for r in range(3):
        witnesses = {
            u
            for u in range(6)
            if oriented(6, u) * skew[r] * oriented(7, u).T == sp.zeros(3, 3)
        }
        assert witnesses == {r, 3 + r}
        # The opposite star blocks are transverse identities, rather than
        # zero blocks or the anchor-rectangle completion forced by a target.
        assert oriented(7, r) == sp.eye(3)
        assert oriented(6, 3 + r) == sp.eye(3)

    print("verified all 504 one-hole polynomial identities")
    print("verified non-target matching tensor with 103 nonzero coefficients")
    print("verified 404 passing and 16 failing full two-hole identities")
    print("two-hole failures:", two_hole_failures)


if __name__ == "__main__":
    main()
