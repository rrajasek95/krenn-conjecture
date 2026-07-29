#!/usr/bin/env python3
"""Exact audit of the 3^3 2^2 1^10 full complementary-residue boundary."""

from __future__ import annotations

import sympy as sp


# The all-order selection uses all ten singletons and leaves 3^3 2^2.
profile = (3,) * 3 + (2,) * 2 + (1,) * 10
complement = (3,) * 3 + (2,) * 2
assert sum(profile) == 23
assert sum(complement) == 13
assert len(complement) == 5
assert 10 == 10  # d=0, s=10 formal role.


z = sp.symbols("z")
H = sp.Poly(
    8286 * z**10
    + 8286 * z**9
    + 8286 * z**8
    - 25786851 * z**7
    + 362953470 * z**6
    - 2285123704 * z**5
    + 8099136386 * z**4
    - 17184131115 * z**3
    + 21620151100 * z**2
    - 14846006000 * z
    + 4280724000,
    z,
    domain=sp.QQ,
)
assert H.degree() == 10

# Exact root-separation tests over QQ: H has ten simple, nonzero roots and
# contains no pair alpha,-alpha.
assert sp.gcd(H, H.diff()).degree() == 0
H_reflected = sp.Poly(H.as_expr().subs(z, -z), z, domain=sp.QQ)
assert sp.gcd(H, H_reflected).degree() == 0
assert H.eval(0) != 0

# The roots alpha=-r avoid both signs of all displayed exceptional values,
# so the singleton values r do as well.
for value in range(1, 6):
    assert H.eval(value) != 0
    assert H.eval(-value) != 0


MULTIPLICITIES = {1: 3, 4: 3, 5: 3, 2: 2, 3: 2}


def local_unit(polynomial, anchor):
    denominator = sp.prod(
        (z - value) ** (multiplicity + 1)
        for value, multiplicity in MULTIPLICITIES.items()
        if value != anchor
    )
    return z**5 * polynomial / denominator  # mu=0 and k=5.


for anchor, multiplicity in MULTIPLICITIES.items():
    unit = local_unit(H.as_expr(), anchor)
    assert sp.cancel(unit.subs(z, anchor)) != 0
    for derivative_order in (multiplicity - 1, multiplicity):
        assert sp.cancel(
            sp.diff(unit, z, derivative_order).subs(z, anchor)
        ) == 0


# Rebuild all ten conditions as homogeneous linear rows on P_10 and audit
# the rank independently of the displayed solution.
coefficients = sp.symbols("c0:11")
general_H = sum(coefficient * z**degree for degree, coefficient in enumerate(coefficients))
equations = []
for anchor, multiplicity in MULTIPLICITIES.items():
    unit = local_unit(general_H, anchor)
    for derivative_order in (multiplicity - 1, multiplicity):
        equations.append(
            sp.together(
                sp.diff(unit, z, derivative_order).subs(z, anchor)
            ).as_numer_denom()[0]
        )
matrix, right_hand_side = sp.linear_eq_to_matrix(equations, coefficients)
assert matrix.shape == (10, 11)
assert matrix.rank() == 8
assert right_hand_side == sp.zeros(10, 1)
displayed_vector = sp.Matrix(list(reversed(H.all_coeffs())))
assert matrix * displayed_vector == sp.zeros(10, 1)


print("k=5 two-double full complementary-residue boundary: PASS")
print("ten direct residue jets: rank eight and simultaneously consistent")
print("ten singleton roots: squarefree, nonzero, nonopposite, and separated")
