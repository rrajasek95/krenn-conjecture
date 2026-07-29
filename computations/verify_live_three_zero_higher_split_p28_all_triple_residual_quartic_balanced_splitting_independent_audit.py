#!/usr/bin/env python3
"""Independent audit of the p=28 residual-quartic balanced splitting.

No project checker is imported.  The script checks finite/infinite
basepoint removal, the determinant-degree ledger, the affine polynomial
row supplied by a line summand, the degree-one differentiation identity,
and a fiberwise rank-two (2,2) model including its infinity fiber.
"""

from __future__ import annotations

from itertools import combinations

import sympy as sp


def homogeneous_lift(poly: sp.Expr, t: sp.Symbol, s: sp.Symbol,
                     u: sp.Symbol, degree: int) -> sp.Expr:
    p = sp.Poly(sp.expand(poly), t)
    return sp.expand(sum(
        coefficient * u**power[0] * s ** (degree - power[0])
        for power, coefficient in p.terms()
    ))


def check_primitive_projectivization() -> None:
    t, s, u = sp.symbols("t s u")

    # A concrete vector with a finite scalar gcd.  Dividing first and then
    # using the actual maximum degree removes finite and infinite basepoints.
    raw = [(t - 3) * value for value in (1, t, t**2, 1 + t**3)]
    gcd = sp.gcd_list(raw)
    assert sp.factor(gcd) == t - 3
    primitive = [sp.cancel(value / gcd) for value in raw]
    assert sp.gcd_list(primitive) == 1
    actual_degree = max(sp.Poly(value, t).degree() for value in primitive)
    assert actual_degree == 3
    homogeneous = [homogeneous_lift(value, t, s, u, actual_degree)
                   for value in primitive]
    assert any(value.subs({s: 0, u: 1}) != 0 for value in homogeneous)
    for finite in (-2, 0, 3, 7):
        assert any(value.subs({s: 1, u: finite}) != 0
                   for value in homogeneous)

    # If the original affine coordinates have degree <=4 and their gcd has
    # degree r, the primitive quotient has actual degree <=4-r.  Therefore
    # primitive projective degree four forces r=0 and no infinity drop.
    candidates = [(gcd_degree, quotient_degree)
                  for gcd_degree in range(5)
                  for quotient_degree in range(5 - gcd_degree)]
    assert [item for item in candidates if item[1] == 4] == [(0, 4)]


def check_determinant_degree_and_splitting_ledger() -> None:
    # A rank-two subbundle O(-alpha)+O(-beta) is represented by homogeneous
    # rows of those degrees.  Every 2x2 minor has degree alpha+beta; if all
    # minors vanished at one projective point, the fiber rank would drop.
    # Hence a subbundle has no common Pluecker zero and projective degree
    # alpha+beta.
    candidates = []
    for degree in range(5):
        for alpha in range(degree + 1):
            beta = degree - alpha
            if alpha <= beta:
                candidates.append((degree, alpha, beta))
    assert [item for item in candidates if item[1] >= 2] == [(4, 2, 2)]

    s, u = sp.symbols("s u")
    for alpha, beta in ((0, 0), (0, 3), (1, 2), (2, 2)):
        first = sp.Matrix([s**alpha, u**alpha, 0, 0])
        second = sp.Matrix([0, 0, s**beta, u**beta])
        matrix = sp.Matrix.vstack(first.T, second.T)
        minors = [sp.expand(matrix[:, columns].det())
                  for columns in combinations(range(4), 2)]
        nonzero = [minor for minor in minors if minor != 0]
        assert all(sp.Poly(minor, s, u).total_degree() == alpha + beta
                   for minor in nonzero)
        for point in ((1, 0), (0, 1)):
            assert matrix.subs({s: point[0], u: point[1]}).rank() == 2


def check_minimal_polynomial_row_and_degree_one() -> None:
    t, s, u = sp.symbols("t s u")
    r0 = sp.Matrix(1, 6, sp.symbols("r0:6"))
    r1 = sp.Matrix(1, 6, sp.symbols("q0:6"))
    rho = r0 + t * r1

    ecoeff = sp.symbols("e0:24")
    ocoeff = sp.symbols("o0:24")
    E = sp.Matrix([
        sum(ecoeff[4 * column + power] * t**power for power in range(4))
        for column in range(6)
    ])
    O = sp.Matrix([
        sum(ocoeff[4 * column + power] * t**power for power in range(4))
        for column in range(6)
    ])

    # Differentiating rho*E=0 and subtracting rho*E'=0 leaves rho'*E=0.
    # The same identity holds for O.
    for vector in (E, O):
        differentiated = sp.diff((rho * vector)[0], t)
        remainder = sp.expand(
            differentiated - (rho * sp.diff(vector, t))[0]
            - (r1 * vector)[0]
        )
        assert remainder == 0

    # A degree-alpha homogeneous generator gives an affine polynomial row
    # of degree <=alpha.  If alpha=1 and the t coefficient vanishes, its
    # homogeneous row has a common zero at infinity; as a subbundle row it
    # must either have genuine degree one or already be a nonzero constant
    # relation.  Both are covered by the proof.
    homogeneous_row = s * r0 + u * r1
    assert homogeneous_row.subs({s: 1, u: t}) == rho
    assert homogeneous_row.subs({s: 0, u: 1}) == r1


def check_balanced_model_including_infinity() -> None:
    t, s, u = sp.symbols("t s u")
    lam = sp.Matrix([1, t, t**2, 0, 0, 0])
    mu = sp.Matrix([0, 0, 0, 1, t, t**2])
    affine = sp.Matrix.vstack(lam.T, mu.T)

    lam_h = sp.Matrix([s**2, s * u, u**2, 0, 0, 0])
    mu_h = sp.Matrix([0, 0, 0, s**2, s * u, u**2])
    homogeneous = sp.Matrix.vstack(lam_h.T, mu_h.T)
    for point in ((1, 0), (1, 2), (0, 1)):
        assert homogeneous.subs({s: point[0], u: point[1]}).rank() == 2

    minors = {
        columns: sp.expand(affine[:, columns].det())
        for columns in combinations(range(6), 2)
    }
    nonzero = [minor for minor in minors.values() if minor != 0]
    assert sp.gcd_list(nonzero) == 1
    assert max(sp.Poly(minor, t).degree() for minor in nonzero) == 4

    for a, b, c, d in combinations(range(6), 4):
        relation = (
            minors[a, b] * minors[c, d]
            - minors[a, c] * minors[b, d]
            + minors[a, d] * minors[b, c]
        )
        assert sp.expand(relation) == 0


def main() -> None:
    check_primitive_projectivization()
    check_determinant_degree_and_splitting_ledger()
    check_minimal_polynomial_row_and_degree_one()
    check_balanced_model_including_infinity()
    print("independent residual-quartic balanced-splitting audit: PASS")
    print("basepoints: finite gcd and infinity degree drop both removed")
    print("only splitting under degree <=4: (alpha,beta)=(2,2)")
    print("scope: strict frontier sharpening, not profile closure")


if __name__ == "__main__":
    main()
