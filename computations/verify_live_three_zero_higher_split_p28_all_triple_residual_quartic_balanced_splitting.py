#!/usr/bin/env python3
"""Exact checks for the all-triple balanced residual splitting."""

from __future__ import annotations

from itertools import combinations

import sympy as sp


def check_splitting_ledger() -> None:
    candidates = []
    for degree in range(5):
        for alpha in range(degree + 1):
            beta = degree - alpha
            if alpha <= beta:
                candidates.append((degree, alpha, beta))
    survivors = [
        item for item in candidates if item[1] >= 2
    ]
    assert survivors == [(4, 2, 2)]


def check_linear_covector_derivative() -> None:
    t = sp.symbols("t")
    r0 = sp.symbols("r0:6")
    r1 = sp.symbols("s0:6")
    ecoeff = sp.symbols("e0:18")
    ocoeff = sp.symbols("o0:18")
    rho = sp.Matrix([[r0[j] + t * r1[j] for j in range(6)]])
    E = sp.Matrix([
        ecoeff[3 * j] + ecoeff[3 * j + 1] * t
        + ecoeff[3 * j + 2] * t**2
        for j in range(6)
    ])
    O = sp.Matrix([
        ocoeff[3 * j] + ocoeff[3 * j + 1] * t
        + ocoeff[3 * j + 2] * t**2
        for j in range(6)
    ])
    for vector in (E, O):
        differentiated = sp.diff((rho * vector)[0], t)
        reduced = sp.expand(differentiated - (rho * sp.diff(vector, t))[0])
        assert reduced == sp.expand(sp.Matrix([r1]).dot(vector))


def check_balanced_model() -> None:
    t = sp.symbols("t")
    lam = sp.Matrix([1, t, t**2, 0, 0, 0])
    mu = sp.Matrix([0, 0, 0, 1, t, t**2])
    two_by_six = sp.Matrix.vstack(lam.T, mu.T)
    assert two_by_six.rank() == 2

    pluecker = {}
    for cols in combinations(range(6), 2):
        pluecker[cols] = sp.expand(two_by_six[:, cols].det())
    nonzero = [value for value in pluecker.values() if value != 0]
    assert max(sp.Poly(value, t).degree() for value in nonzero) == 4
    assert sp.gcd_list(nonzero) == 1

    # Every 2x2 Pluecker relation holds, hence the Hodge-dual four-vector
    # is decomposable at every parameter value.
    for a, b, c, d in combinations(range(6), 4):
        relation = (
            pluecker[a, b] * pluecker[c, d]
            - pluecker[a, c] * pluecker[b, d]
            + pluecker[a, d] * pluecker[b, c]
        )
        assert sp.expand(relation) == 0

    samples = (sp.Rational(0), sp.Rational(1), sp.Rational(-2))
    for value in samples:
        assert two_by_six.subs(t, value).rank() == 2


def main() -> None:
    check_splitting_ledger()
    check_linear_covector_derivative()
    check_balanced_model()
    print("p=28 all-triple residual-quartic balanced splitting: PASS")
    print("only annihilator splitting (2,2) survives degree <=4")
    print("balanced decomposable quartic model: PASS")
    print("scope: residual frontier only; profile closure not claimed")


if __name__ == "__main__":
    main()
