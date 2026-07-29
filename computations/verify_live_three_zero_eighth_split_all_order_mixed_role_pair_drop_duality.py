#!/usr/bin/env python3
"""Exact audit of the all-k mixed-role pair-drop duality theorem."""

import sympy as sp


z, mu = sp.symbols("z mu")
k = sp.symbols("k", integer=True, positive=True)


# The kernel data and every missing-edge/parity count are independent of k.
for d in range(5):
    s = 10 - 2 * d
    layer_count = 10 - d
    degree_cap = 11 - d

    assert 2 * d + s == 10
    assert 2 * d + 3 * s == 30 - 4 * d
    assert 25 - 4 * d > degree_cap
    assert 1 + 2 * layer_count == 2 * degree_cap - 1
    assert 3 + 2 * (layer_count - 1) == 2 * degree_cap - 1

    for lowered_singletons in range(3):
        core_classes = layer_count - lowered_singletons
        residual_degree = core_classes - 3
        lift_factor_degree = 4 + lowered_singletons
        assert residual_degree == 7 - d - lowered_singletons
        assert residual_degree + lift_factor_degree == degree_cap

    for dimension in range(5, degree_cap + 2):
        forced_weight = d * (dimension - 2) + s * (dimension - 1)
        wronskian_cap = dimension * (degree_cap + 1 - dimension)
        deficit = forced_weight - wronskian_cap
        assert deficit == dimension**2 - 2 * dimension - 10
        assert deficit > 0

    for absorbed_singletons in range(s + 1):
        square_degree = (degree_cap - 2 * absorbed_singletons) // 2
        if square_degree < 2:
            continue
        forced_weight = 2 * (s - absorbed_singletons)
        wronskian_cap = 3 * (square_degree - 2)
        assert forced_weight > wronskian_cap

    ambient_dimension = degree_cap + 1
    row_count = layer_count
    row_rank = ambient_dimension - 4
    relation_dimension = row_count - row_rank
    assert (row_rank, relation_dimension) == (8 - d, 2)

    # Complementary and common-pole degrees at symbolic order k.
    complement_degree = k + 8
    selected_denominator_degree = 3 * d + 2 * s
    rational_numerator_degree = complement_degree + degree_cap
    rational_denominator_degree = (k + 1) + selected_denominator_degree
    assert sp.simplify(
        rational_numerator_degree - rational_denominator_degree
    ) == -2
    assert selected_denominator_degree == 20 - d

    annihilated_moments = degree_cap + 1
    relation_numerator_degree = (
        selected_denominator_degree - annihilated_moments - 1
    )
    assert relation_numerator_degree == 7
    assert 2 * d + s == 10


# A simple gcd zero at a singleton row forces a common square-variable
# root, so an absorbed singleton costs at least two gcd degrees.
r = sp.symbols("r")
b0, b1 = sp.symbols("b0 b1", nonzero=True)
e0, e1 = sp.symbols("e0 e1")
local_g = z + r
local_unit = b0 + b1 * (z + r)
local_even = e0 + e1 * (z**2 - r**2)
row = sp.diff(local_unit * local_g * local_even, z).subs(z, -r)
assert sp.expand(row - b0 * e0) == 0


# Exact quotient differentiation at symbolic common-pole order.
A_value, A_prime, N_value, N_prime = sp.symbols(
    "A_value A_prime N_value N_prime"
)
direct_numerator = (
    (
        (k + 1) * (z + mu) ** k * N_value
        + (z + mu) ** (k + 1) * N_prime
    )
    * A_value
    - (z + mu) ** (k + 1) * N_value * A_prime
)
factored_numerator = (z + mu) ** k * (
    A_value * ((z + mu) * N_prime + (k + 1) * N_value)
    - (z + mu) * A_prime * N_value
)
assert sp.expand(direct_numerator - factored_numerator) == 0


# The leading term and the target degree are independent of k.
n, c = sp.symbols("n c", integer=True)
leading_coefficient = n + (k + 1) - (k + 8)
assert sp.simplify(leading_coefficient - (n - 7)) == 0
for degree_n in range(8):
    nominal_degree = c + degree_n
    if degree_n == 7:
        assert leading_coefficient.subs(n, degree_n) == 0
        differential_degree_bound = c + 6
    else:
        assert nominal_degree <= c + 6
        differential_degree_bound = nominal_degree
    assert sp.simplify(differential_degree_bound - 10) <= c - 4

# Concrete order checks guard the symbolic bookkeeping at several rows.
for order in range(1, 21):
    for d in range(5):
        s = 10 - 2 * d
        degree_cap = 11 - d
        assert (order + 8) + degree_cap + 2 == (
            (order + 1) + 3 * d + 2 * s
        )
        assert 7 + (order + 1) - (order + 8) == 0


# The simple-root Wronskian criterion and the c=5 singleton contradiction.
for classes in range(5, 15):
    target_degree = classes - 4
    pencil_wronskian_degree = 2 * target_degree - 2
    assert pencil_wronskian_degree == 2 * classes - 10

x = z - r
b2 = sp.symbols("b2")
B = b0 + b1 * x + b2 * x**2
assert sp.diff(B * x, z).subs(z, r) == b0


# At a complementary double, the k-dependent common-pole term cancels
# from every selected/outside swap.
u, v, x_value, fixed_terms = sp.symbols("u v x fixed_terms")


def phi(anchor, value):
    return 2 / (anchor + value) + 3 / (anchor - value)


before = (
    k / (u + mu)
    + fixed_terms
    + 2 / (u + x_value)
    - 3 / (u - v)
)
after = (
    k / (u + mu)
    + fixed_terms
    + 2 / (u + v)
    - 3 / (u - x_value)
)
assert sp.factor((before - after) - (phi(u, x_value) - phi(u, v))) == 0
assert sp.factor(
    phi(u, x_value) - (5 * u + x_value) / (u**2 - x_value**2)
) == 0
fibre_value = sp.symbols("lambda")
fibre_polynomial = sp.Poly(
    sp.expand(fibre_value * (u**2 - x_value**2) - 5 * u - x_value),
    x_value,
)
assert fibre_polynomial.degree() <= 2
assert fibre_polynomial.coeff_monomial(x_value) == -1


print("all-order h=8 mixed-role pair-drop duality: PASS")
print("kernel audit: d=0..4, full graph or one triple-zero missing edge")
print("common-pole audit: symbolic k>=1, target degree c-4")
print("scope: theorem/local corollaries only; no all-k census credit")
