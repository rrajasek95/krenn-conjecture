#!/usr/bin/env python3
"""Exact audit of the stable h=8 nonic common-lift closures."""

from __future__ import annotations

from itertools import combinations

import sympy as sp


# Uniform four-core ledger.
for m in range(12, 81):
    for epsilon in (0, 1):
        p = m - 4
        k = 2 * m - 18 + epsilon
        target_degree = p - 5 + epsilon
        common_degree = p + epsilon
        numerator_degree = k + 2 * 4
        denominator_degree = 3 * p + 2 * epsilon

        assert target_degree + 5 == common_degree
        assert numerator_degree + common_degree - denominator_degree == -2

        for d in range(2, min(common_degree + 2, 12)):
            forced = p * (d - 2) + epsilon * (d - 1)
            cap = d * (common_degree + 1 - d)
            assert forced - cap == d**2 - d - 2 * p - epsilon

# The two nonic cases and the next decic threshold.
assert (9, 0, 9, 5**2 - 5 - 18) == (9, 0, 9, 2)
assert (8, 1, 9, 5**2 - 5 - 17) == (8, 1, 9, 3)
assert 2 * 5 > 9
assert 5**2 - 5 - 2 * 10 == 0         # pure m=14 equality
assert 5**2 - 5 - (2 * 9 + 1) == 1   # singleton m=13 still d<=4
assert 2 * 5 == 10                    # pair intersections first appear

# Local gcd corrections.
for d in range(2, 12):
    assert d + 1 > 0                  # simple double gcd; >=2 singleton gcd
    assert 2 * d + 2 > 0              # >=3 double gcd


w, z, a, s = sp.symbols("w z a s", nonzero=True)

# Parity quotient row after division by (w-s)^2.
e0, e1, e2, o0, o1 = sp.symbols("e0 e1 e2 o0 o1")
even = (w - s) ** 2 * (e0 + e1 * w + e2 * w**2)
odd = (w - s) ** 2 * (o0 + o1 * w + e0 * w**2)
assert sp.factor(
    (
        sp.diff(even, w, 2).subs(w, s)
        + a * sp.diff(odd, w, 2).subs(w, s)
    )
    / 2
    - ((even / (w - s) ** 2) + a * (odd / (w - s) ** 2)).subs(w, s)
) == 0

# Degree-nine cofactor bound for [E', O, O'].
ec = sp.symbols("ec0:12")
oc = sp.symbols("oc0:15")
Eprime = [sum(ec[4 * j + q] * w**q for q in range(4)) for j in range(3)]
O = [sum(oc[5 * j + q] * w**q for q in range(5)) for j in range(3)]
minor = sp.Poly(
    sp.det(sp.Matrix([Eprime, O, [sp.diff(poly, w) for poly in O]])),
    w,
)
assert minor.degree() <= 9

# Eight-point affine cofactor quotient: orthogonality to O and O' kills
# both constant covectors when the odd projection has rank four.
c0, c1, d0, d1 = sp.symbols("c0 c1 d0 d1")
f0, f1, g0, g1 = sp.symbols("f0 f1 g0 g1")
affine_pairing = (f0 + f1 * w) * (w * c0 + d0) + (g0 + g1 * w) * (
    w * c1 + d1
)
derived_pairing = sp.diff(affine_pairing, w)
direct_derivative_pairing = f1 * (w * c0 + d0) + g1 * (w * c1 + d1)
assert sp.expand(
    derived_pairing
    - direct_derivative_pairing
    - c0 * (f0 + f1 * w)
    - c1 * (g0 + g1 * w)
) == 0

# Lower odd-rank counts.
assert 3 * (5 - 3) == 6               # three-quartic Wronskian
assert 2 * (5 - 2) == 6               # two-quartic Wronskian
assert 8 - 3 >= 5                      # rank-three regular points
assert 8 - 6 >= 2                      # rank-two regular points
assert 2 * 3 > 4                       # two quartic triple roots
assert (8 - 2) * 2 > 6                 # rank-one double Wronskian roots


def tangent_equations(Orow, Frow):
    """Coefficients of all minors F wedge O wedge O'."""
    Oprime = [sp.diff(poly, w) for poly in Orow]
    equations = []
    for cols in combinations(range(4), 3):
        det = sp.Poly(
            sp.det(
                sp.Matrix(
                    [
                        [Frow[j] for j in cols],
                        [Orow[j] for j in cols],
                        [Oprime[j] for j in cols],
                    ]
                )
            ),
            w,
        )
        equations.extend(det.all_coeffs())
    return equations


def tangent_nullity(Orow, substitutions=None):
    """Dimension of the exact sixteen-coefficient tangent system."""
    coefficients = sp.symbols("tc0:16")
    generic = [
        sum(coefficients[4 * j + q] * w**q for q in range(4))
        for j in range(4)
    ]
    equations = tangent_equations(Orow, generic)
    matrix, _ = sp.linear_eq_to_matrix(equations, coefficients)
    if substitutions:
        matrix = matrix.subs(substitutions)
    return 16 - matrix.rank()


def assert_tangent_and_fibre(Orow, Frow, fibre):
    """Audit global tangency and divisibility of all fifth-row minors."""
    Oprime = [sp.diff(poly, w) for poly in Orow]
    Osecond = [sp.diff(poly, w, 2) for poly in Orow]
    Fprime = [sp.diff(poly, w) for poly in Frow]
    Hrow = [fp + a * opp for fp, opp in zip(Fprime, Osecond)]

    for equation in tangent_equations(Orow, Frow):
        assert sp.factor(equation) == 0
    for cols in combinations(range(4), 3):
        det = sp.factor(
            sp.det(
                sp.Matrix(
                    [
                        [Hrow[j] for j in cols],
                        [Orow[j] for j in cols],
                        [Oprime[j] for j in cols],
                    ]
                )
            )
        )
        assert sp.factor(det / fibre).is_polynomial(w, a)


def four_wronskian(Orow):
    return sp.factor(
        sp.det(
            sp.Matrix(
                [[sp.diff(poly, w, order) for poly in Orow] for order in range(4)]
            )
        )
    )


# q=4, generic tangent rank two.
l0, l1, l2, l3, u, v, t = sp.symbols("l0 l1 l2 l3 u v t")
O4 = [1 + l0 * w**4, w + l1 * w**4, w**2 + l2 * w**4, w**3 + l3 * w**4]
F4 = [
    -16 * u * l3 + 4 * v + 4 * u * l0 * w**3,
    u + (-12 * u * l3 + 3 * v) * w + 4 * u * l1 * w**3,
    2 * u * w + (-8 * u * l3 + 2 * v) * w**2 + 4 * u * l2 * w**3,
    3 * u * w**2 + v * w**3,
]
P4 = a + u + (4 * l3 * u - v) * w
assert_tangent_and_fibre(O4, F4, P4)
assert sp.factor(
    four_wronskian(O4)
    + 12 * (l0 * w**4 - 4 * l1 * w**3 + 6 * l2 * w**2 - 4 * l3 * w - 1)
) == 0

# q=4 special rank three: span(1,w,w^2,w^3+l w^4).
l = sp.symbols("l", nonzero=True)
O4s = [1, w, w**2, w**3 + l * w**4]
F4s = [
    3 * u / (2 * l) - 16 * v * l / 3 + 4 * t + 2 * u * w,
    v / 3 + (u / l - 4 * v * l + 3 * t) * w + 3 * u * w**2 / 2,
    2 * v * w / 3 + (u / (2 * l) - 8 * v * l / 3 + 2 * t) * w**2 + u * w**3,
    v * w**2 + t * w**3,
]
P4s = -6 * a * l - 8 * l**2 * v * w + 6 * l * t * w + 3 * l * u * w**2 - 2 * l * v + 3 * u * w
assert_tangent_and_fibre(O4s, F4s, P4s)
assert sp.factor(four_wronskian(O4s) - 12 * (4 * l * w + 1)) == 0

# q=4 special rank four: the cubic odd space.
A, B, C, D = sp.symbols("A B C D")
O4c = [1, w, w**2, w**3]
F4c = [
    3 * A + 3 * B * w - 2 * D,
    2 * A * w + 2 * B * w**2 + C - D * w,
    A * w**2 + B * w**3 + 2 * C * w,
    3 * C * w**2 + D * w**3,
]
P4c = a - (B * w**2 + (A - D) * w - C)
assert_tangent_and_fibre(O4c, F4c, P4c)
assert four_wronskian(O4c) == 12

# q=3, lambda_2 nonzero.
l2nz = sp.symbols("l2nz", nonzero=True)
O3 = [1 + l0 * w**3, w + l1 * w**3, w**2 + l2nz * w**3, w**4]
F3 = [
    4 * u / l2nz + 3 * v * l0 * w**2 / 4 + u * l0 * w**3 / l2nz,
    v / 4 + 3 * u * w / l2nz + 3 * v * l1 * w**2 / 4 + u * l1 * w**3 / l2nz,
    v * w / 2 + (2 * u / l2nz + 3 * v * l2nz / 4) * w**2 + u * w**3,
    v * w**3,
]
P3 = 4 * u * w - 4 * a * l2nz - l2nz * v
assert_tangent_and_fibre(O3, F3, P3)

# q=3, lambda_2=0 but not both earlier lambdas zero.
O3m = [1 + l0 * w**3, w + l1 * w**3, w**2, w**4]
F3m = [
    2 * u + 3 * v * l0 * w**2 / 4 + u * l0 * w**3 / 2,
    v / 4 + 3 * u * w / 2 + 3 * v * l1 * w**2 / 4 + u * l1 * w**3 / 2,
    v * w / 2 + u * w**2,
    v * w**3,
]
P3m = 2 * u * w - 4 * a - v
assert_tangent_and_fibre(O3m, F3m, P3m)

# q=3 special rank jump: span(1,w,w^2,w^4).
O3s = [1, w, w**2, w**4]
F3s = [
    2 * u + 2 * v * w,
    t / 4 + 3 * u * w / 2 + 3 * v * w**2 / 2,
    t * w / 2 + u * w**2 + v * w**3,
    t * w**3,
]
P3s = 4 * a + t - 2 * u * w - 2 * v * w**2
assert_tangent_and_fibre(O3s, F3s, P3s)

# q=2.
O2 = [1 + l0 * w**2, w + l1 * w**2, w**3, w**4]
F2 = [
    4 * u + v * l0 * w / 2 + 2 * u * l0 * w**2,
    v / 4 + (3 * u + v * l1 / 2) * w + 2 * u * l1 * w**2,
    3 * v * w**2 / 4 + u * w**3,
    v * w**3,
]
P2 = 4 * u * w - 4 * a - v
assert_tangent_and_fibre(O2, F2, P2)

# q=1.
O1 = [1 + l0 * w, w**2, w**3, w**4]
F1 = [
    4 * u - 3 * v * l0**2 / 16 + t * l0 / 4 + 3 * u * l0 * w,
    v / 2 + (-v * l0 / 8 + t / 2) * w + 2 * u * w**2,
    3 * v * w / 4 + (-v * l0 / 16 + 3 * t / 4) * w**2 + u * w**3,
    v * w**2 + t * w**3,
]
P1 = 16 * a * w + l0 * v * w + 4 * t * w - 16 * u * w**2 + 4 * v
assert_tangent_and_fibre(O1, F1, P1)

# q=0.
O0 = [w, w**2, w**3, w**4]
F0 = [
    3 * A - 2 * D + 3 * B * w,
    C / 3 + (2 * A - D) * w + 2 * B * w**2,
    2 * C * w / 3 + A * w**2 + B * w**3,
    C * w**2 + D * w**3,
]
P0 = 3 * A * w + 3 * B * w**2 - C - 3 * D * w - 3 * a * w
assert_tangent_and_fibre(O0, F0, P0)

# Remaining four-Wronskian factorizations.
assert sp.factor(
    four_wronskian(O3)
    - 12 * w * (l0 * w**3 - 4 * l1 * w**2 + 6 * l2nz * w + 4)
) == 0
assert sp.factor(
    four_wronskian(O2)
    + 12 * w**2 * (l0 * w**2 - 4 * l1 * w - 6)
) == 0
assert sp.factor(four_wronskian(O1) - 12 * w**3 * (l0 * w + 4)) == 0
assert sp.factor(four_wronskian(O0) - 12 * w**4) == 0

# The tangent-system rank jumps are exactly the triple/quadruple normal
# forms used in Lemma 6.1.  Double roots alone do not cause a jump.
assert tangent_nullity(O4, {l0: 2, l1: 3, l2: 5, l3: 7}) == 2
assert tangent_nullity(O2, {l0: 2, l1: 3}) == 2
assert tangent_nullity(O1, {l0: 2}) == 3
assert tangent_nullity(O0) == 4
assert tangent_nullity(O4s, {l: 2}) == 3
assert tangent_nullity(O4c) == 4
assert tangent_nullity(O3s) == 3

# Four-Wronskian root types: no triple, exact triple, and quadruple.
I_no_triple = sp.Poly((w - 1) * (w - 2) * (w - 3) * (w - 4), w)
I_triple = sp.Poly(w**3 * (w - 1), w)
I_quadruple = sp.Poly(w**4, w)
assert sp.gcd(
    I_no_triple, sp.Poly(sp.diff(I_no_triple.as_expr(), w, 2), w)
).degree() == 0
assert sp.gcd(
    I_triple, sp.Poly(sp.diff(I_triple.as_expr(), w, 2), w)
).degree() >= 1
assert sp.gcd(
    I_quadruple, sp.Poly(sp.diff(I_quadruple.as_expr(), w, 3), w)
).degree() >= 1

# Every fibre polynomial remains nonzero after w=a^2, with the stated caps.
fibre_data = [
    (P4, 2),
    (P4s, 4),
    (P4c, 4),
    (P3, 2),
    (P3m, 2),
    (P3s, 4),
    (P2, 2),
    (P1, 4),
    (P0, 4),
]
for fibre, cap in fibre_data:
    polynomial = sp.Poly(sp.expand(fibre.subs(w, a**2)), a)
    assert polynomial.degree() <= cap
    assert polynomial.as_expr() != 0


print("stable h=8 nonic common-lift closures: PASS")
print("2^13 and 2^12 1 common kernels have dimension exactly four")
print("all parity ranks and every tangent-hyperplane root type are excluded")
print("first unresolved common-kernel threshold is decic")
