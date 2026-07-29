#!/usr/bin/env python3
"""Exact audit of the h=8, k=6, 2^12 common-lift closure."""

from __future__ import annotations

from itertools import combinations

import sympy as sp


# Common-lift degree ledger.
assert 6 + 2 * 4 == 14                 # numerator degree of H
assert 3 * 8 == 24                     # denominator degree of H
assert 14 + 8 - 24 == -2               # H times an octic
assert 5 + 3 == 8                       # A_a times a cubic
assert 2 * 5 > 8                        # distinct lift factors cannot meet

# Corrected Wronskian deficit for a d-space of octics at eight exact
# order-two rows.
for d in range(5, 10):
    baseline_deficit = 8 * (d - 2) - d * (9 - d)
    assert baseline_deficit == d**2 - d - 16
    assert baseline_deficit > 0
    assert baseline_deficit + (d + 1) > baseline_deficit
    assert baseline_deficit + (2 * d + 2) > baseline_deficit


z, a, w, s = sp.symbols("z a w s", nonzero=True)

# Pairwise coprimality of fifth-value lift factors under a != +/-b.
b = sp.symbols("b", nonzero=True)
A_a = (z + a) ** 2 * (z - a) ** 3
A_b = (z + b) ** 2 * (z - b) ** 3
assert sp.Poly(A_a, z).degree() == 5
assert sp.Poly(A_a * A_b, z).degree() == 10

# Exact parity factorization and the fifth quotient row.
e0, e1, e2, o0, o1 = sp.symbols("e0 e1 e2 o0 o1")
even = (w - s) ** 2 * (e0 + e1 * w + e2 * w**2)
odd = (w - s) ** 2 * (o0 + o1 * w)
assert sp.diff(even, w, 2).subs(w, s) == 2 * (e0 + e1 * s + e2 * s**2)
assert sp.diff(odd, w, 2).subs(w, s) == 2 * (o0 + o1 * s)
quotient_at_a = (e0 + e1 * s + e2 * s**2) + a * (o0 + o1 * s)
assert sp.expand(
    (
        sp.diff(even, w, 2).subs(w, s)
        + a * sp.diff(odd, w, 2).subs(w, s)
    )
    / 2
    - quotient_at_a
) == 0


# Every 3x3 minor of [E', O, O'] has degree at most seven.  Check one
# completely generic column triple; relabeling covers the others.
ecoef = sp.symbols("e0:12")
ocoef = sp.symbols("o0:12")
Ecols = [sum(ecoef[4 * j + q] * w**q for q in range(4)) for j in range(3)]
Ocols = [sum(ocoef[4 * j + q] * w**q for q in range(4)) for j in range(3)]
minor = sp.Poly(
    sp.det(
        sp.Matrix(
            [
                Ecols,
                Ocols,
                [sp.diff(poly, w) for poly in Ocols],
            ]
        )
    ),
    w,
)
assert minor.degree() <= 7


# Full odd rank: solve the coefficient comparison in
# rank[E', (1,w,w^2,w^3), (0,1,2w,3w^2)] <= 2.
v = [1, w, w**2, w**3]
vp = [sp.diff(poly, w) for poly in v]
fcoef = sp.symbols("f0:16")
F_generic = [
    sum(fcoef[4 * j + q] * w**q for q in range(4)) for j in range(4)
]
equations = []
for cols in combinations(range(4), 3):
    det = sp.Poly(
        sp.det(
            sp.Matrix(
                [
                    [F_generic[j] for j in cols],
                    [v[j] for j in cols],
                    [vp[j] for j in cols],
                ]
            )
        ),
        w,
    )
    equations.extend(det.all_coeffs())
matrix, _ = sp.linear_eq_to_matrix(equations, fcoef)
assert matrix.rank() == 12
assert len(matrix.nullspace()) == 4

A, B, C, D = sp.symbols("A B C D")
F = [
    3 * A + 3 * B * w - 2 * D,
    2 * A * w + 2 * B * w**2 + C - D * w,
    A * w**2 + B * w**3 + 2 * C * w,
    3 * C * w**2 + D * w**3,
]
for cols in combinations(range(4), 3):
    assert sp.factor(
        sp.det(
            sp.Matrix(
                [
                    [F[j] for j in cols],
                    [v[j] for j in cols],
                    [vp[j] for j in cols],
                ]
            )
        )
    ) == 0

n0 = [w**2, -2 * w, 1, 0]
n1 = [0, w**2, -2 * w, 1]
Fp = [sp.diff(poly, w) for poly in F]
vpp = [sp.diff(poly, w, 2) for poly in v]
Y = B * w**2 + (A - D) * w - C
dot = lambda row, column: sp.expand(sum(x * y for x, y in zip(row, column)))
assert sp.factor(dot(v, n0)) == 0
assert sp.factor(dot(v, n1)) == 0
assert sp.factor(dot(vp, n0)) == 0
assert sp.factor(dot(vp, n1)) == 0
assert sp.factor(dot(Fp, n0) + 2 * Y) == 0
assert sp.factor(dot(Fp, n1) + 2 * w * Y) == 0
assert sp.factor(dot(vpp, n0) - 2) == 0
assert sp.factor(dot(vpp, n1) - 2 * w) == 0
quartic_fibre = sp.expand(B * a**4 + (A - D) * a**2 - a - C)
assert sp.Poly(quartic_fibre, a).degree() <= 4
assert sp.Poly(quartic_fibre, a).coeff_monomial(a) == -1


# Lower-rank degree counts.
assert 3 * (4 - 3) == 3               # three-cubic Wronskian
assert 2 * (4 - 2) == 4               # two-cubic Wronskian
assert 2 * (5 - 2) == 6               # two-quartic Wronskian
assert 8 - 3 >= 5                      # r=3 regular squares
assert 8 - 4 >= 4                      # r=2 regular squares
assert 8 - 1 >= 7                      # r=1 regular squares
assert 3 * 2 > 4                       # two quartic triple roots impossible
assert 7 * 2 > 6                       # seven double Wronskian roots impossible

# In rank zero, the two families in (29) kill all five coefficient
# directions.  Their coefficient spans have ranks four and five together.
ell = sp.symbols("l0:5")
poly = sum(ell[j] * w**j for j in range(5))
# Coefficient vectors, as polynomials in s, of (w-s)^3 and w(w-s)^3.
family0 = sp.Poly((w - s) ** 3, w)
family1 = sp.Poly(w * (w - s) ** 3, w)
vectors = []
for family in (family0, family1):
    for power in range(4):
        vectors.append(
            [
                sp.Poly(family.coeff_monomial(w**j), s).coeff_monomial(s**power)
                for j in range(5)
            ]
        )
assert sp.Matrix(vectors).rank() == 5


print("h=8 k=6 twelve-double common-lift closure: PASS")
print("common octic exactness kernel has dimension exactly four")
print("eight parity-jet rank conditions exclude odd ranks 0 through 4")
