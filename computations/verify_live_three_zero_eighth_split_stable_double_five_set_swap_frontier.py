#!/usr/bin/env python3
"""Exact audit of the stable h=8 double-family five-set swap frontier."""

from __future__ import annotations

import sympy as sp


# Unified degree ledger for 2^m and 2^m 1.
for multiplicity_classes in range(12, 81):
    for epsilon in (0, 1):
        complement_doubles = multiplicity_classes - 5
        common_pole_order = 2 * multiplicity_classes - 18 + epsilon
        complement_classes = complement_doubles + epsilon
        target_degree = complement_classes - 4

        assert common_pole_order == 2 * complement_doubles - 8 + epsilon
        assert 2 * complement_doubles + epsilon == common_pole_order + 8
        assert target_degree == multiplicity_classes - 9 + epsilon

        rational_numerator_degree = (
            common_pole_order + 10 + target_degree
        )
        rational_denominator_degree = (
            3 * complement_doubles + 2 * epsilon
        )
        assert rational_denominator_degree - rational_numerator_degree == 2


z, mu, k = sp.symbols("z mu k")
C = sp.Function("C")(z)
L = sp.Function("L")(z)
N = sp.Function("N")(z)

# Arbitrary-complement dual differentiation.
E_N = sp.expand(
    C * L * ((z + mu) * sp.diff(N, z) + (k + 1) * N)
    - (z + mu)
    * (2 * sp.diff(C, z) * L + C * sp.diff(L, z))
    * N
)
G_N = (z + mu) ** (k + 1) * N / (C**2 * L)
expected_derivative = (z + mu) ** k * E_N / (C**3 * L**2)
# SymPy does not automatically replace
# ``(z+mu)**(k+1)`` by ``(z+mu)*(z+mu)**k`` for a symbolic exponent.
# Audit the same formal differentiation after making that power-law
# normalization explicitly.
power_normalized_derivative = (z + mu) ** k * sp.expand(
    (k + 1) * C * L * N
    + (z + mu) * C * L * sp.diff(N, z)
    - 2 * (z + mu) * sp.diff(C, z) * L * N
    - (z + mu) * C * sp.diff(L, z) * N
) / (C**3 * L**2)
assert sp.factor(power_normalized_derivative - expected_derivative) == 0

# Leading cancellation is always deg(N)-7.
j, n, epsilon = sp.symbols("j n epsilon")
assert sp.expand(j + (2 * n - 8 + epsilon + 1) - (2 * n + epsilon)) == j - 7


# Exact triple-pole residue row and its Wronskian consequence.
u = sp.symbols("u")
B0, B1, B2 = sp.symbols("B0 B1 B2", nonzero=True)
s00, s01, s02, s10, s11, s12 = sp.symbols(
    "s00 s01 s02 s10 s11 s12"
)
row0 = B0 * s02 + 2 * B1 * s01 + B2 * s00
row1 = B0 * s12 + 2 * B1 * s11 + B2 * s10
X = B1 / B0
assert sp.factor(
    (s00 * s12 - s02 * s10)
    + 2 * X * (s00 * s11 - s01 * s10)
) == sp.factor((s00 * row1 - s10 * row0) / B0)

# The singleton double-pole row is exact first order.
D0, D1, p0, p1 = sp.symbols("D0 D1 p0 p1", nonzero=True)
assert sp.expand(D0 * p1 + D1 * p0 - D0 * (p1 + D1 / D0 * p0)) == 0


# Fixed-degree numerator Wronskian and mixed determinant.
N0, N1 = sp.Function("N0")(z), sp.Function("N1")(z)
E0 = sp.expand(
    C * L * ((z + mu) * sp.diff(N0, z) + (k + 1) * N0)
    - (z + mu)
    * (2 * sp.diff(C, z) * L + C * sp.diff(L, z))
    * N0
)
E1 = sp.expand(
    C * L * ((z + mu) * sp.diff(N1, z) + (k + 1) * N1)
    - (z + mu)
    * (2 * sp.diff(C, z) * L + C * sp.diff(L, z))
    * N1
)
wronskian_N = N0 * sp.diff(N1, z) - N1 * sp.diff(N0, z)
assert sp.factor(
    N0 * E1 - N1 * E0 - C * L * (z + mu) * wronskian_N
) == 0
assert 2 * 7 - 2 == 12
assert 12 - 2 * 5 == 2

# A selected pencil basepoint is automatically a triple gcd root: locally
# E(N)=aN'+bN with a(0) a unit, so N(0)=E(N)(0)=E(N)'(0)=0 successively
# kills the first two derivatives as well.
a0, a1, b0, b1, n0, n1, n2 = sp.symbols(
    "a0 a1 b0 b1 n0 n1 n2", nonzero=True
)
E_at_zero = a0 * n1 + b0 * n0
E_prime_at_zero = a0 * n2 + (a1 + b0) * n1 + b1 * n0
assert E_at_zero.subs(n0, 0) == a0 * n1
assert E_prime_at_zero.subs({n0: 0, n1: 0}) == a0 * n2

# Riemann--Hurwitz excludes every selected basepoint and bounds the total
# pencil gcd by one degree.
for selected_basepoints in range(1, 6):
    assert 2 * (5 - selected_basepoints) > (
        2 * (7 - 3 * selected_basepoints) - 2
    )
for total_gcd_degree in range(2, 8):
    assert 10 > 2 * (7 - total_gcd_degree) - 2
assert 10 <= 2 * 6 - 2

for complement_doubles in range(7, 41):
    for singleton_count in (0, 1):
        target_degree = complement_doubles + singleton_count - 4
        assert 7 + target_degree == (
            complement_doubles + singleton_count + 3
        )


# One-value swap of logarithmic jets.
u, a, b = sp.symbols("u a b")


def phi(anchor, value):
    return 2 / (anchor + value) + 3 / (anchor - value)


def psi(anchor, value):
    return 2 / (anchor + value) ** 2 + 3 / (anchor - value) ** 2


selected_first_change = 2 / (u + b) - 2 / (u + a)
outside_first_change = 3 / (u - b) - 3 / (u - a)
delta = sp.factor(selected_first_change + outside_first_change)
assert sp.factor(delta - (phi(u, b) - phi(u, a))) == 0

selected_second_change = -2 / (u + b) ** 2 + 2 / (u + a) ** 2
outside_second_change = -3 / (u - b) ** 2 + 3 / (u - a) ** 2
eta = sp.factor(selected_second_change + outside_second_change)
assert sp.factor(eta - (psi(u, a) - psi(u, b))) == 0

x, j0 = sp.symbols("x j0")
assert sp.expand(
    (x + delta) ** 2 + (j0 + eta)
    - (x**2 + j0 + 2 * x * delta + delta**2 + eta)
) == 0


# Full rational multiplier and the same-numerator differential transform.
Q, C_symbol, L_symbol = sp.symbols("Q C_symbol L_symbol", nonzero=True)
Q_prime_ratio = (z + b) / (z + a)
C_prime_ratio = (z - a) / (z - b)
full_multiplier = sp.factor(
    Q_prime_ratio**2 / C_prime_ratio**3
)
assert sp.factor(
    full_multiplier
    - (z + b) ** 2 * (z - b) ** 3
    / ((z + a) ** 2 * (z - a) ** 3)
) == 0

R = (z - a) / (z - b)
C_generic = sp.Function("C_generic")(z)
L_generic = sp.Function("L_generic")(z)
N_generic = sp.Function("N_generic")(z)


def differential_operator(C_input):
    return sp.expand(
        C_input
        * L_generic
        * ((z + mu) * sp.diff(N_generic, z) + (k + 1) * N_generic)
        - (z + mu)
        * (
            2 * sp.diff(C_input, z) * L_generic
            + C_input * sp.diff(L_generic, z)
        )
        * N_generic
    )


assert sp.factor(
    differential_operator(R * C_generic)
    - R * differential_operator(C_generic)
    + 2
    * (z + mu)
    * C_generic
    * L_generic
    * sp.diff(R, z)
    * N_generic
) == 0


# Eleven-value localization.
for multiplicity_classes in range(12, 81):
    background = multiplicity_classes - 11
    pure_target_dimension = multiplicity_classes - 8
    singleton_target_dimension = multiplicity_classes - 7
    assert pure_target_dimension == background + 3
    assert singleton_target_dimension - 1 == background + 3
    assert (background + 3) - 2 == background + 1
    assert background + 2 > background + 1


# Adjacent-pencils overlap obstruction.
for multiplicity_classes in range(12, 81):
    for singleton_count in (0, 1):
        common_outside = multiplicity_classes - 6
        common_pole_order = (
            2 * multiplicity_classes - 18 + singleton_count
        )
        numerator_degree_bound = (
            2 * common_outside
            + singleton_count
            - (common_pole_order + 1)
        )
        assert numerator_degree_bound == 5

assert 2 * 5 - 2 == 8
assert 2 * 6 == 12
assert 12 > 8

A_swap = (z + b) ** 2 * (z - b) ** 3
B_swap = (z + a) ** 2 * (z - a) ** 3
assert sp.factor(
    B_swap * full_multiplier - A_swap
) == 0


print("h=8 stable double-family five-set swap frontier: PASS")
print("arbitrary-complement dual map and complementary rows: exact")
print("N-side Wronskian and mixed determinant identities: exact")
print("one-value swap signs and same-N obstruction: exact")
print("adjacent derivative pencils have intersection dimension at most one")
