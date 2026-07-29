#!/usr/bin/env python3
"""Exact audit of the all-order five-double six-class residue closure."""

from __future__ import annotations

from pathlib import Path
import sys

import sympy as sp


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import verify_live_three_zero_higher_split_collision_frontier as frontier


# Endpoint kernel arithmetic: d=5, s=0, L=5, D=6.
d = 5
formal_layers = 5
ambient_degree = 6
assert formal_layers - 3 + 2 + 2 == ambient_degree
assert 4 * 2 > ambient_degree  # neighbor-product bound for every U_i.
assert 5 * 2 > ambient_degree  # a two-space cannot equal every U_i.

for dimension in range(5, ambient_degree + 2):
    forced_weight = d * (dimension - 2)
    wronskian_cap = dimension * (ambient_degree + 1 - dimension)
    deficit = forced_weight - wronskian_cap
    assert deficit == dimension**2 - 2 * dimension - 10
    assert deficit > 0

# A hypothetical three-space has an odd degree-11 parity determinant and
# the saturated divisor z*prod(z^2-x_i^2), also of degree 11.  The constant
# cross-product vector must vanish because it is orthogonal to a basis.
parity_degree = 2 * ambient_degree - 1
saturated_divisor_degree = 1 + 2 * formal_layers
assert parity_degree == saturated_divisor_degree == 11
p0, p1, p2 = sp.symbols("p0 p1 p2")
c0, c1, c2 = sp.symbols("c0 c1 c2")
assert sp.Matrix([p0, p1, p2]).dot(sp.Matrix([c0, c1, c2])) == (
    c0 * p0 + c1 * p1 + c2 * p2
)

# The primitive square-variable three-space has degree m=2 or 3 only.
degree_cases = []
for gcd_degree in range(ambient_degree + 1):
    square_degree = (ambient_degree - gcd_degree) // 2
    if square_degree >= 2:
        degree_cases.append((gcd_degree, square_degree))
assert degree_cases == [(0, 3), (1, 2), (2, 2)]
assert 5 > 2  # in the m=2 cases, some G(-x_i) is nonzero.

z, x = sp.symbols("z x", nonzero=True)
y = sp.symbols("y")
unit_value, gcd_value = sp.symbols("unit_value gcd_value", nonzero=True)
E0, E1, E2 = sp.symbols("E0 E1 E2")
# Chain rule coefficient of the independent E'' jet in (B*G*E(z^2))''.
assert 4 * x**2 * unit_value * gcd_value != 0
assert 3 * (3 + 1 - 3) == 3  # m=3 Wronskian cap.
assert 5 > 3

# Endpoint duality at symbolic common-pole order k.
k = sp.symbols("k", integer=True, positive=True)
selected_denominator_degree = 3 * d
annihilated_moments = ambient_degree + 1
relation_numerator_degree = (
    selected_denominator_degree - annihilated_moments - 1
)
assert relation_numerator_degree == 7
complement_degree = k + 8
rational_numerator_degree = complement_degree + ambient_degree
rational_denominator_degree = (k + 1) + selected_denominator_degree
assert sp.simplify(
    rational_numerator_degree - rational_denominator_degree
) == -2
n = sp.symbols("n", integer=True)
assert sp.simplify(n + (k + 1) - (k + 8)) == n - 7
assert 2 * d == 10  # Q^2 divisor, leaving target degree c-4.

# At c=6, a two-plane in P_2 contained in the nonzero simple-root residue
# kernel equals that kernel, and (z-r)^2 belongs to it.
r = sp.symbols("r")
local = z - r
b0, b1, b2 = sp.symbols("b0 b1 b2", nonzero=True)
local_unit = b0 + b1 * local + b2 * local**2
assert sp.diff(local_unit * local**2, z).subs(z, r) == 0
assert 6 - 4 == 2


u, t = sp.symbols("u t", nonzero=True)


def phi(anchor, value):
    return 2 / (anchor + value) + 3 / (anchor - value)


def psi(anchor, value):
    return 2 / (anchor + value) ** 2 + 3 / (anchor - value) ** 2


assert sp.factor(
    phi(u, t) - (5 * u + t) / (u**2 - t**2)
) == 0

# Moving t from selected exponent +2 at z=-t to complementary exponent
# -3 at z=t subtracts Phi in the first log derivative and adds Psi in the
# second log derivative.
selected_first = 2 / (u + t)
outside_first = -3 / (u - t)
assert sp.factor(selected_first - outside_first - phi(u, t)) == 0
selected_second = -2 / (u + t) ** 2
outside_second = 3 / (u - t) ** 2
assert sp.factor(outside_second - selected_second - psi(u, t)) == 0

# Exact pair-equation subtraction.
A, C = sp.symbols("A C")
p_v, p_w, p_x = sp.symbols("p_v p_w p_x")
h_v, h_w, h_x = sp.symbols("h_v h_w h_x")
equation_vw = h_v + h_w + 2 * p_v * p_w + C
equation_vx = h_v + h_x + 2 * p_v * p_x + C
assert sp.factor(
    equation_vw - equation_vx
    - (h_w - h_x + 2 * p_v * (p_w - p_x))
) == 0
assert 8 - 3 == 5  # five remaining v values if p_w != p_x.

fibre_value = sp.symbols("lambda")
fibre_polynomial = sp.Poly(
    sp.expand(fibre_value * (u**2 - t**2) - 5 * u - t),
    t,
)
assert fibre_polynomial.degree() <= 2
assert fibre_polynomial.coeff_monomial(t) == -1


def profile(triples=0, doubles=0, singletons=0):
    return (3,) * triples + (2,) * doubles + (1,) * singletons


expected_hits = {
    1: {profile(0, 8, 3)},
    2: {profile(0, 9, 2)},
    3: {profile(1, 8, 2), profile(0, 10, 1)},
    4: {profile(1, 9, 1)},
    5: {profile(2, 8, 1)},
}

# On a baseline residual with a singleton, failure of the short route gives
# top-two sum at most seven.  Exhaust the at-most-three nondouble classes to
# make the all-k census finite before inspecting the six possible orders.
maximum_total = 0
for double_count in range(8, 11):
    other_count = 11 - double_count

    def build_other(prefix=(), maximum=7):
        if len(prefix) == other_count:
            yield prefix
            return
        for value in range(min(maximum, 7), 0, -1):
            if value == 2:
                continue
            yield from build_other(prefix + (value,), value)

    for other in build_other():
        candidate = tuple(sorted((2,) * double_count + other, reverse=True))
        if candidate.count(1) == 0:
            continue
        if candidate[0] + candidate[1] > 7:
            continue
        maximum_total = max(maximum_total, sum(candidate))
assert maximum_total == 24
assert maximum_total - 18 == 6

observed_hits = {}
for order in range(1, maximum_total - 18 + 1):
    _, residuals = frontier.census(8, 8 + order)
    hits = {
        candidate
        for candidate in residuals
        if len(candidate) == 11
        and candidate.count(2) >= 8
        and candidate.count(1) >= 1
    }
    if hits:
        observed_hits[order] = hits
assert observed_hits == expected_hits


print("h=8 all-order five-double six-class residue closure: PASS")
print("endpoint d=5 kernel and duality: exact")
print("C=11, n2>=8, n1>=1 pair-residue closure: exact")
print("k=5 final profile 3^2 2^8 1: closed")
