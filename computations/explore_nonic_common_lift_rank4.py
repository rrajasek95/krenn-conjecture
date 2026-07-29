#!/usr/bin/env python3
"""Symbolic reconnaissance for the rank-four odd projection at 2^13.

On the chart ell(w^4) != 0, write the odd hyperplane as the span of
    p_j(w) = w^j - l_j w^4,  j=0,...,3.
This script solves linearly for every cubic vector F satisfying
    rank(F(w), O(w), O'(w)) <= 2 identically.
It is discovery code; a proof checker should replace it once the normal
form is understood.
"""

from __future__ import annotations

import itertools

import sympy as sp


def main() -> None:
    w = sp.symbols("w")
    ls = sp.symbols("l0:4")
    xs = sp.symbols("x0:16")

    O = sp.Matrix([[w**j - ls[j] * w**4 for j in range(4)]])
    Op = O.diff(w)
    F = sp.Matrix(
        [[sum(xs[4 * j + k] * w**k for k in range(4)) for j in range(4)]]
    )

    equations = []
    for cols in itertools.combinations(range(4), 3):
        minor = sp.expand(sp.Matrix.vstack(F, O, Op)[:, cols].det())
        poly = sp.Poly(minor, w)
        equations.extend(poly.coeff_monomial(w**k) for k in range(10))

    matrix, rhs = sp.linear_eq_to_matrix(equations, xs)
    assert rhs == sp.zeros(rhs.rows, 1)
    print("matrix shape:", matrix.shape)

    # Generic rational-function rank/nullspace over Q(l0,l1,l2,l3).
    null = matrix.nullspace()
    print("generic nullity:", len(null))
    for index, vector in enumerate(null):
        nonzero = [(xs[i], sp.factor(value)) for i, value in enumerate(vector) if value]
        print("basis", index)
        for name, value in nonzero:
            print(" ", name, "=", value)

    if len(null) == 2:
        a, b = sp.symbols("A B")
        vector = a * null[0] + b * null[1]
        Fs = [sp.expand(sum(vector[4 * j + k] * w**k for k in range(4))) for j in range(4)]
        denominator = sp.expand(Op[0, 1] * O[0, 0] - Op[0, 0] * O[0, 1])
        beta = sp.factor((Fs[1] * O[0, 0] - Fs[0] * O[0, 1]) / denominator)
        alpha = sp.factor((Fs[0] - beta * Op[0, 0]) / O[0, 0])
        print("beta =", beta)
        print("alpha =", alpha)
        print("tangent residuals:")
        for j in range(4):
            print(j, sp.factor(Fs[j] - alpha * O[0, j] - beta * Op[0, j]))

    histogram = {}
    exceptional = []
    for values in itertools.product((-1, 0, 1), repeat=4):
        rank = matrix.subs(dict(zip(ls, values))).rank()
        nullity = 16 - rank
        histogram[nullity] = histogram.get(nullity, 0) + 1
        if nullity != 2:
            exceptional.append((values, nullity))
    print("sample nullity histogram:", histogram)
    print("sample exceptional charts:", exceptional)

    _rref, pivots = matrix.rref()
    print("generic pivots:", pivots)
    print("generic free columns:", tuple(i for i in range(16) if i not in pivots))
    _, row_pivots = matrix.T.rref()
    square = matrix[list(row_pivots[:14]), list(pivots[:14])]
    print("one rank-14 minor:", sp.factor(square.det()))
    for values in [(-3, 0, 1, t) for t in (-2, -1, 0, 1, 2)]:
        print("discriminant sample", values, "nullity", 16 - matrix.subs(dict(zip(ls, values))).rank())


if __name__ == "__main__":
    main()
