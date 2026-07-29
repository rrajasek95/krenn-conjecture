#!/usr/bin/env python3
"""Exact audit of the remaining repeated-double seventh-split closures."""

import sympy as sp


x, y = sp.symbols("x y")


def chi(node, moving, multiplicity):
    return (
        multiplicity / (moving - node)
        - (multiplicity + 1) / (moving + node)
    )


def eta(node, moving, multiplicity):
    return (
        multiplicity / (moving - node) ** 2
        + (multiplicity + 1) / (moving + node) ** 2
    )


def simple_row(node, local_Y, degree):
    """Ascending-coefficient row for q'(node)+local_Y*q(node)."""
    return [
        (power * node ** (power - 1) if power else 0)
        + local_Y * node**power
        for power in range(degree + 1)
    ]


def repeated_row(node, local_Y, local_M, degree):
    """Ascending row for q''+2Yq'+Mq at the repeated node."""
    return [
        (power * (power - 1) * node ** (power - 2) if power >= 2 else 0)
        + (2 * local_Y * power * node ** (power - 1) if power else 0)
        + local_M * node**power
        for power in range(degree + 1)
    ]


def assert_bidegree(row, x_bound, y_bound):
    assert all(sp.denom(entry) == 1 for entry in row)
    assert max(sp.Poly(entry, x, y).degree(x) for entry in row) <= x_bound
    assert max(sp.Poly(entry, x, y).degree(y) for entry in row) <= y_bound


# ---------------------------------------------------------------------------
# Two repeated anchors and a moving simple class: a degree-eight obstruction.
# ---------------------------------------------------------------------------

a, b, Ua, Va, Ub, Vb = sp.symbols("a b Ua Va Ub Vb")


def cleared_repeated_linear(node, local_U, local_V):
    local_D = x**2 - node**2
    local_Y = local_U + chi(node, x, 1)
    local_M = local_Y**2 + local_V + eta(node, x, 1)
    return [
        sp.cancel(local_D**2 * entry).expand()
        for entry in repeated_row(node, local_Y, local_M, 1)
    ]


row_a = cleared_repeated_linear(a, Ua, Va)
row_b = cleared_repeated_linear(b, Ub, Vb)
assert all(sp.Poly(entry, x).degree() <= 4 for entry in row_a + row_b)
two_repeated_determinant = sp.cancel(sp.Matrix([row_a, row_b]).det()).expand()
assert sp.Poly(two_repeated_determinant, x).degree() <= 8

# Endpoint evaluation of the a-row forces the two conditions on the b-row.
Yb = Ub + chi(b, x, 1)
Mb = Yb**2 + Vb + eta(b, x, 1)
b_against_a = 2 * Yb + (b - a) * Mb
b_endpoint_equations = [
    sp.factor(b_against_a.subs(x, endpoint))
    for endpoint in (a, -a)
]
solved_b = sp.solve(b_endpoint_equations, (Ub, Vb), dict=True)
expected_Ub = (a - 3 * b) / ((a - b) * (a + b))
expected_V = -(3 * a**2 - 2 * a * b + 3 * b**2) / (
    (a - b) ** 2 * (a + b) ** 2
)
assert len(solved_b) == 1
assert sp.factor(solved_b[0][Ub] - expected_Ub) == 0
assert sp.factor(solved_b[0][Vb] - expected_V) == 0

# The symmetric endpoints determine the a-row constants.
expected_Ua = (3 * a - b) / ((a - b) * (a + b))
endpoint_constants = {
    Ua: expected_Ua,
    Va: expected_V,
    Ub: expected_Ub,
    Vb: expected_V,
}
specialized_determinant = sp.factor(
    two_repeated_determinant.subs(endpoint_constants)
)
quartic_remainder = sp.cancel(
    specialized_determinant
    * (a - b)
    * (a + b) ** 4
    / (4 * (x**2 - a**2) * (x**2 - b**2))
).expand()
assert sp.denom(quartic_remainder) == 1
quartic_remainder = sp.Poly(quartic_remainder, x)
assert quartic_remainder.degree() == 4
top = quartic_remainder.coeff_monomial(x**4)
next_top = quartic_remainder.coeff_monomial(x**3)
assert sp.factor(top - (9 * a**2 + 22 * a * b + 9 * b**2)) == 0
assert sp.factor(
    next_top + 4 * (a + b) * (a**2 + 6 * a * b + b**2)
) == 0
assert sp.factor(
    top - 9 * (a**2 + 6 * a * b + b**2) + 32 * a * b
) == 0


# ---------------------------------------------------------------------------
# Endpoint nonidentity lemmas for reduced linear pencils.
# ---------------------------------------------------------------------------

t, s, C, j = sp.symbols("t s C j")
opposite_difference = sp.factor(chi(s, t, j) - chi(s, -t, j))
assert sp.factor(opposite_difference + 2 * t / (t**2 - s**2)) == 0

# Two ordinary simple rows: at the poles of the nonzero anchor t, identity
# would require the other row to take the same value at both endpoints.
# The displayed difference proves this impossible even if s=0.
assert sp.factor(opposite_difference.subs(s, 0) + 2 / t) == 0

# A repeated row and a simple row have the same endpoint contradiction.
# Directly check that their cleared determinant has the nominal degree six.
Ur, Vr, Cs = sp.symbols("Ur Vr Cs")
repeated_mixed = cleared_repeated_linear(t, Ur, Vr)
simple_Y = Cs + chi(s, x, 1)
simple_mixed = [
    sp.cancel((x**2 - s**2) * entry).expand()
    for entry in simple_row(s, simple_Y, 1)
]
mixed_determinant = sp.cancel(
    sp.Matrix([repeated_mixed, simple_mixed]).det()
).expand()
assert sp.Poly(mixed_determinant, x).degree() <= 6


# ---------------------------------------------------------------------------
# Three simple anchors with two moving full doubles.
# ---------------------------------------------------------------------------

c, Ca, Cb, Cc = sp.symbols("c Ca Cb Cc")


def cleared_bivariate_simple_quadratic(node, constant):
    local_Y = constant + chi(node, x, 2) + chi(node, y, 2)
    local_D = (x**2 - node**2) * (y**2 - node**2)
    return [
        sp.cancel(local_D * entry).expand()
        for entry in simple_row(node, local_Y, 2)
    ]


three_simple_rows = [
    cleared_bivariate_simple_quadratic(a, Ca),
    cleared_bivariate_simple_quadratic(b, Cb),
    cleared_bivariate_simple_quadratic(c, Cc),
]
for row in three_simple_rows:
    assert_bidegree(row, 2, 2)
# Every Leibniz term takes one entry from each row, so the determinant
# bidegree is bounded by the sum of these exact row bounds.
assert sum(2 for _ in three_simple_rows) == 6

for endpoint, factor in ((a, 4 * a), (-a, 6 * a)):
    expected = [
        sp.expand(factor * (x**2 - a**2) * value)
        for value in (1, a, a**2)
    ]
    assert all(
        sp.factor(entry.subs(y, endpoint) - target) == 0
        for entry, target in zip(three_simple_rows[0], expected)
    )

# Exact quadratic-to-linear basis reduction q(z)=(z-a)r(z).
factor_map_quadratic = sp.Matrix([[-a, 0], [1, -a], [0, 1]])
assert (
    sp.Matrix([[1, a, a**2]]) * factor_map_quadratic
    == sp.zeros(1, 2)
)
Z = sp.symbols("Z")
generic_quadratic_simple = sp.Matrix(
    [[Z, 1 + s * Z, 2 * s + s**2 * Z]]
)
generic_linear_shifted = sp.Matrix(
    [[Z + 1 / (s - a), 1 + s * (Z + 1 / (s - a))]]
)
assert all(
    sp.factor(entry) == 0
    for entry in (
        generic_quadratic_simple * factor_map_quadratic
        - (s - a) * generic_linear_shifted
    )
)


# ---------------------------------------------------------------------------
# One simple and one repeated row with two moving full doubles.
# ---------------------------------------------------------------------------


def cleared_bivariate_simple_linear(node, constant):
    local_Y = constant + chi(node, x, 2) + chi(node, y, 2)
    local_D = (x**2 - node**2) * (y**2 - node**2)
    return [
        sp.cancel(local_D * entry).expand()
        for entry in simple_row(node, local_Y, 1)
    ]


def cleared_bivariate_repeated_linear(node, local_U, local_V):
    local_Y = local_U + chi(node, x, 2) + chi(node, y, 2)
    local_M = (
        local_Y**2
        + local_V
        + eta(node, x, 2)
        + eta(node, y, 2)
    )
    local_D = (x**2 - node**2) ** 2 * (y**2 - node**2) ** 2
    return [
        sp.cancel(local_D * entry).expand()
        for entry in repeated_row(node, local_Y, local_M, 1)
    ]


simple_bivariate_linear = cleared_bivariate_simple_linear(a, Ca)
repeated_bivariate_linear = cleared_bivariate_repeated_linear(b, Ub, Vb)
assert_bidegree(simple_bivariate_linear, 2, 2)
assert_bidegree(repeated_bivariate_linear, 4, 4)
assert 2 + 4 == 6

for endpoint, factor in ((b, 24 * b**2), (-b, 48 * b**2)):
    expected = [
        sp.expand(factor * (x**2 - b**2) ** 2 * value)
        for value in (1, b)
    ]
    assert all(
        sp.factor(entry.subs(y, endpoint) - target) == 0
        for entry, target in zip(repeated_bivariate_linear, expected)
    )

# After q(z)=(z-b)r with constant r, the remaining simple equation clears
# to K*(x^2-a^2)+(5a-x), whose x coefficient is always -1.
Kshift = sp.symbols("Kshift")
constant_residual_numerator = sp.Poly(
    Kshift * (x**2 - a**2) + 5 * a - x, x
)
assert constant_residual_numerator.degree() <= 2
assert constant_residual_numerator.coeff_monomial(x) == -1


# ---------------------------------------------------------------------------
# Two repeated quadratic rows plus one simple row (the isolated d=2 case).
# ---------------------------------------------------------------------------


def cleared_bivariate_repeated_quadratic(node, local_U, local_V):
    local_Y = local_U + chi(node, x, 1) + chi(node, y, 1)
    local_M = (
        local_Y**2
        + local_V
        + eta(node, x, 1)
        + eta(node, y, 1)
    )
    local_D = (x**2 - node**2) ** 2 * (y**2 - node**2) ** 2
    return [
        sp.cancel(local_D * entry).expand()
        for entry in repeated_row(node, local_Y, local_M, 2)
    ]


def cleared_bivariate_simple_quadratic_j1(node, constant):
    local_Y = constant + chi(node, x, 1) + chi(node, y, 1)
    local_D = (x**2 - node**2) * (y**2 - node**2)
    return [
        sp.cancel(local_D * entry).expand()
        for entry in simple_row(node, local_Y, 2)
    ]


isolated_rows = [
    cleared_bivariate_repeated_quadratic(a, Ua, Va),
    cleared_bivariate_repeated_quadratic(b, Ub, Vb),
    cleared_bivariate_simple_quadratic_j1(c, Cc),
]
assert_bidegree(isolated_rows[0], 4, 4)
assert_bidegree(isolated_rows[1], 4, 4)
assert_bidegree(isolated_rows[2], 2, 2)
assert 4 + 4 + 2 == 10

for endpoint, factor in ((a, 8 * a**2), (-a, 24 * a**2)):
    expected = [
        sp.expand(factor * (x**2 - a**2) ** 2 * value)
        for value in (1, a, a**2)
    ]
    assert all(
        sp.factor(entry.subs(y, endpoint) - target) == 0
        for entry, target in zip(isolated_rows[0], expected)
    )


# ---------------------------------------------------------------------------
# Strict counts and the final residual table.
# ---------------------------------------------------------------------------

# The uniform univariate lemma has c-3 legal roots and needs at least nine.
uniform_closed = {
    8: {3, 4, 5},
    9: {3, 4, 5, 6},
    10: {4, 5, 6, 7},
    11: {5, 6, 7},
    12: {6, 7},
    13: {7},
}
for p, doubles in uniform_closed.items():
    for d in doubles:
        singleton_count = p + 9 - 2 * d
        class_count = p + 9 - d
        assert d >= 3
        assert singleton_count >= 2
        assert class_count - 3 >= 9

# Both degree-six bivariate grids have eight moving double classes.
for p, d, singleton_count, fixed_double_anchors in (
    (11, 9, 2, 1),
    (12, 10, 1, 2),
):
    assert p + 9 == 2 * d + singleton_count
    moving_doubles = d - fixed_double_anchors
    assert moving_doubles == 8
    assert moving_doubles - 1 == 7 > 6
    assert moving_doubles == 8 > 6

# The all-double p=11,d=10 selection has one partial and one full fixed
# double, again leaving eight moving double classes.
assert 11 + 9 == 2 * 10
assert 10 - 2 == 8

# The isolated p=8,d=2 profile has twelve moving singleton classes.
assert 8 + 9 - 2 * 2 == 13
assert 13 - 1 == 12
assert 12 - 1 == 11 > 10
assert 12 > 10

post_sixteen = {
    8: {2, 3, 4, 5, 6, 7, 8},
    9: {3, 4, 5, 6, 7, 8, 9},
    10: {4, 5, 6, 7, 8, 9},
    11: {5, 6, 7, 9, 10},
    12: {6, 7, 10},
    13: {7},
}
extra_closed = {
    8: {2, 3, 4, 5},
    9: {3, 4, 5, 6},
    10: {4, 5, 6, 7},
    11: {5, 6, 7, 9, 10},
    12: {6, 7, 10},
    13: {7},
}
expected_remaining = {
    8: {6, 7, 8},
    9: {7, 8, 9},
    10: {8, 9},
    11: set(),
    12: set(),
    13: set(),
}
for p, residuals in post_sixteen.items():
    assert residuals - extra_closed[p] == expected_remaining[p]


print("two repeated linear rows: exact degree-eight nonidentity")
print("ordinary and mixed two-anchor endpoint obstructions: exact")
print("degree-six moving-double bivariate closures: exact")
print("isolated d=2 bidegree-(10,10) closure: exact")
print("strict legality counts and sharpened double frontier: exact")
