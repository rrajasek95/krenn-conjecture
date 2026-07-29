#!/usr/bin/env python3
"""Exact audit of the k=5 profile 3^3 2^3 1^8 second-jet closure."""

from __future__ import annotations

import sympy as sp


# Formal selection and complement.
profile = (3,) * 3 + (2,) * 3 + (1,) * 8
assert sum(profile) == 23
selected_role = 2 + 8
assert selected_role == 10
complement = tuple(sorted((3,) * 3 + (2,) * 2, reverse=True))
assert complement == (3, 3, 3, 2, 2)
assert len(complement) == 5


z, u = sp.symbols("z u", nonzero=True)
b0, b1, b2, b3 = sp.symbols("b0 b1 b2 b3", nonzero=True)
local = z - u
B = b0 + b1 * local + b2 * local**2 + b3 * local**3

# The residue at an order-three pole is half the second derivative.
assert sp.diff(B * local, z, 2).subs(z, u) == 2 * b1
assert sp.diff(B, z, 2).subs(z, u) == 2 * b2


v, x = sp.symbols("v x")


def phi(anchor, value):
    return 2 / (anchor + value) + 3 / (anchor - value)


def psi(anchor, value):
    return 2 / (anchor + value) ** 2 + 3 / (anchor - value) ** 2


phi_numerator = sp.factor(
    sp.together(phi(u, x) - phi(u, v)).as_numer_denom()[0]
)
assert sp.factor(
    phi_numerator
    - (v - x) * (-u**2 - 5 * u * v - 5 * u * x - v * x)
) == 0

fibre_relation = u**2 + 5 * u * (x + v) + x * v
solved_v = -(u**2 + 5 * u * x) / (5 * u + x)
assert sp.factor(fibre_relation.subs(v, solved_v)) == 0
assert sp.factor(
    (v - x).subs(v, solved_v)
    + (u**2 + 10 * u * x + x**2) / (5 * u + x)
) == 0

psi_substitution = sp.factor((psi(u, x) - psi(u, v)).subs(v, solved_v))
expected = -(
    (u**2 + 10 * u * x + x**2)
    * (5 * u**2 + 2 * u * x + 5 * x**2)
) / (24 * u**2 * (u - x) ** 2 * (u + x) ** 2)
assert sp.factor(psi_substitution - expected) == 0


# The three pairwise quadrics give incompatible linear sums.
q_uv = 5 * u**2 + 2 * u * v + 5 * v**2
q_ux = 5 * u**2 + 2 * u * x + 5 * x**2
first_difference = sp.factor(q_ux - q_uv)
assert sp.factor(
    first_difference + (v - x) * (2 * u + 5 * v + 5 * x)
) == 0

q_xu = 5 * x**2 + 2 * x * u + 5 * u**2
q_xv = 5 * x**2 + 2 * x * v + 5 * v**2
second_difference = sp.factor(q_xu - q_xv)
assert sp.factor(
    second_difference - (u - v) * (5 * u + 2 * x + 5 * v)
) == 0

linear_one = 2 * u + 5 * x + 5 * v
linear_two = 5 * u + 2 * x + 5 * v
assert sp.factor(linear_one - linear_two - 3 * (x - u)) == 0


print("k=5 three-double second-jet closure: PASS")
print("profile and full linear relation plane: exact")
print("first/second swap jets and paired quadratic: exact")
print("three distinct double values: impossible")
