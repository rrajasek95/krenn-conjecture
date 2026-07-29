#!/usr/bin/env python3
"""Exact local countermodel to the proposed moving-root kernel orientation.

The model has E,O in C^6[tau] of degree at most four.  At tau=0 (so
t=z^2=1), the residual first-derivative four-plane has a simple rank drop.
The + square-root sheet has vanishing sequence (0,1,2,4,5,6), while the -
sheet is unramified.  Nevertheless the right kernel of the derivative map
is [0:1], not the sheet vector [1:1].
"""

from itertools import combinations

import sympy as sp


tau = sp.symbols("tau")
q = sp.Rational
eye = sp.eye(6)
e = [eye[:, j] for j in range(6)]
zero = sp.zeros(6, 1)

# Coefficients of E(tau) and O(tau), in ascending powers of tau.
E = [zero.copy() for _ in range(5)]
O = [zero.copy() for _ in range(5)]
E[0], O[0] = e[0], e[1]
E[1], O[1] = e[2], zero.copy()
E[2], O[2] = zero.copy(), e[3]
E[3] = e[4]
O[3] = -e[4] - q(1, 2) * e[3] - q(1, 16) * e[1]
E[4] = e[0]
O[4] = -e[0] + q(9, 128) * e[1] + q(3, 8) * e[3] + q(1, 2) * e[4] + e[5]

Epoly = sum((E[j] * tau**j for j in range(5)), zero.copy())
Opoly = sum((O[j] * tau**j for j in range(5)), zero.copy())

# On the two local sheets z=+/-sqrt(1+tau), F=E+zO.  The square root is
# only used as a formal power series, so every assertion is over Q.
root = sp.sqrt(1 + tau)
Gplus = (Epoly + root * Opoly).applyfunc(
    lambda x: sp.series(x, tau, 0, 7).removeO().expand()
)
Gminus = (Epoly - root * Opoly).applyfunc(
    lambda x: sp.series(x, tau, 0, 7).removeO().expand()
)


def coefficient_vector(series_vector: sp.Matrix, order: int) -> sp.Matrix:
    return series_vector.applyfunc(lambda x: sp.expand(x).coeff(tau, order))


plus = [coefficient_vector(Gplus, j) for j in range(7)]
minus = [coefficient_vector(Gminus, j) for j in range(6)]
plus_ranks = [sp.Matrix.hstack(*plus[: j + 1]).rank() for j in range(7)]
minus_ranks = [sp.Matrix.hstack(*minus[: j + 1]).rank() for j in range(6)]

assert plus_ranks == [1, 2, 3, 3, 4, 5, 6]
assert minus_ranks == [1, 2, 3, 4, 5, 6]

# The four-plane span(E,O,E_t,O_t) has rank three at tau=0.  Modulo
# L_0=span(E(0),O(0)), its two derivative columns are e_2 and 0, so the
# right kernel is [0:1].
fiber = sp.Matrix.hstack(
    Epoly.subs(tau, 0),
    Opoly.subs(tau, 0),
    Epoly.diff(tau).subs(tau, 0),
    Opoly.diff(tau).subs(tau, 0),
)
assert fiber.rank() == 3
assert Epoly.diff(tau).subs(tau, 0) == e[2]
assert Opoly.diff(tau).subs(tau, 0) == zero
assert sp.Matrix([0, 1]) != sp.Matrix([1, 1])

# The rank drop is simple: the gcd of all nonzero Pluecker coordinates of
# E wedge O wedge E_t wedge O_t is exactly tau, up to a rational unit.
moving = sp.Matrix.hstack(Epoly, Opoly, Epoly.diff(tau), Opoly.diff(tau))
pluecker = [
    sp.expand(moving[list(rows), :].det())
    for rows in combinations(range(6), 4)
    if moving[list(rows), :].det() != 0
]
gcd = sp.factor(sp.gcd_list(pluecker))
assert sp.Poly(gcd, tau).monic().as_expr() == tau

# Degree guard: F(z)=E(z^2-1)+zO(z^2-1) has six independent coordinate
# polynomials of degree at most nine.
z = sp.symbols("z")
F = Epoly.subs(tau, z**2 - 1) + z * Opoly.subs(tau, z**2 - 1)
assert max(sp.degree(entry, z) for entry in F) <= 9
coefficient_matrix = sp.Matrix(
    [[sp.expand(entry).coeff(z, j) for entry in F] for j in range(10)]
)
assert coefficient_matrix.rank() == 6

print("p=28 residual kernel-orientation countermodel: PASS")
print("+ sheet sequence: (0,1,2,4,5,6)")
print("- sheet sequence: (0,1,2,3,4,5)")
print("simple residual rank drop: yes")
print("actual eta right kernel: [0:1], not [1:1]")

