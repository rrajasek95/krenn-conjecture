#!/usr/bin/env python3
"""Exact audit of the p=8, (d,s)=(8,1) role-swap closure."""

import sympy as sp


z, t, x, y = sp.symbols("z t x y")


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


def second_operator(poly, node, local_y, local_v):
    local_m = local_y**2 + local_v
    return sp.expand(
        sp.diff(poly, z, 2).subs(z, node)
        + 2 * local_y * sp.diff(poly, z).subs(z, node)
        + local_m * poly.subs(z, node)
    )


# ---------------------------------------------------------------------------
# Partial-to-full lift, away from and at the promoted anchor.
# ---------------------------------------------------------------------------

Y, V = sp.symbols("Y V")
h = z**2 - x**2
ell = sp.diff(h, z).subs(z, t) / h.subs(z, t)
ell_prime = sp.diff(2 * z / (z**2 - x**2), z).subs(z, t)

assert sp.factor(chi(t, x, 2) - chi(t, x, 1) + ell) == 0
assert sp.factor(eta(t, x, 2) - eta(t, x, 1) + ell_prime) == 0

q0, q1 = sp.symbols("q0 q1")
q = q0 + q1 * z
lifted_away = second_operator(h * q, t, Y - ell, V - ell_prime)
old_away = h.subs(z, t) * second_operator(q, t, Y, V)
assert sp.factor(lifted_away - old_away) == 0

# At the promoted anchor the old partial coefficient is Y_T+1/(2x).
YT, VT = sp.symbols("YT VT")
lifted_self = second_operator(h * q, x, YT, VT)
old_self = 4 * x * (
    sp.diff(q, z).subs(z, x) + (YT + 1 / (2 * x)) * q.subs(z, x)
)
assert sp.factor(lifted_self - old_self) == 0


# ---------------------------------------------------------------------------
# Four second-order rows cannot have rank one on cubic coefficients.
# ---------------------------------------------------------------------------

M = sp.symbols("M")
row = sp.Matrix(
    [[M, 2 * Y + t * M, 2 + 4 * t * Y + t**2 * M,
      6 * t + 6 * t**2 * Y + t**3 * M]]
)
dual_cubic = (
    row[0] * t**3 - 3 * row[1] * t**2 + 3 * row[2] * t - row[3]
)
assert sp.expand(dual_cubic) == 0

# The divisibility spaces S_u are precisely matrices with low column
# equal to -u times the high column, and lie on the rank-one quadric.
u, alpha, beta = sp.symbols("u alpha beta")
divisible = sp.expand((z**2 - u) * (alpha + beta * z))
coeffs = [sp.Poly(divisible, z).coeff_monomial(z**j) for j in range(4)]
matrix_encoding = sp.Matrix([[coeffs[0], coeffs[2]],
                             [coeffs[1], coeffs[3]]])
assert sp.factor(matrix_encoding.det()) == 0
assert matrix_encoding == sp.Matrix([[-u * alpha, alpha],
                                     [-u * beta, beta]])

# Restriction of the quadric to a projective line is quadratic.  If it
# vanishes identically, the standard 2x2 rank-one lemma gives either a
# common left factor or a common right factor.  The mixed coefficient is
# recorded explicitly here.
p0, p1, p2, p3, r0, r1, r2, r3, lam = sp.symbols(
    "p0 p1 p2 p3 r0 r1 r2 r3 lam"
)
line_quadric = sp.Poly(
    (p0 + lam * r0) * (p3 + lam * r3)
    - (p1 + lam * r1) * (p2 + lam * r2),
    lam,
)
assert line_quadric.degree() == 2
assert line_quadric.coeff_monomial(lam) == (
    p0 * r3 + r0 * p3 - p1 * r2 - r1 * p2
)


# ---------------------------------------------------------------------------
# Strict bidegree-(4,4) determinant and endpoint contradiction.
# ---------------------------------------------------------------------------

a, b, U, V = sp.symbols("a b U V")


def cleared_simple_linear(node, constant):
    local_y = constant + chi(node, x, 2) + chi(node, y, 2)
    local_d = (x**2 - node**2) * (y**2 - node**2)
    return [
        sp.cancel(local_d * local_y).expand(),
        sp.cancel(local_d * (1 + node * local_y)).expand(),
    ]


row_a = cleared_simple_linear(a, U)
row_b = cleared_simple_linear(b, V)
for entry in row_a + row_b:
    assert sp.denom(entry) == 1
    assert sp.Poly(entry, x, y).degree(x) <= 2
    assert sp.Poly(entry, x, y).degree(y) <= 2

determinant = sp.cancel(sp.Matrix([row_a, row_b]).det()).expand()
assert sp.Poly(determinant, x, y).degree(x) <= 4
assert sp.Poly(determinant, x, y).degree(y) <= 4

expected_endpoint_a = [
    4 * a * (x**2 - a**2),
    4 * a**2 * (x**2 - a**2),
]
expected_endpoint_minus_a = [
    6 * a * (x**2 - a**2),
    6 * a**2 * (x**2 - a**2),
]
assert all(
    sp.factor(entry.subs(y, a) - expected) == 0
    for entry, expected in zip(row_a, expected_endpoint_a)
)
assert all(
    sp.factor(entry.subs(y, -a) - expected) == 0
    for entry, expected in zip(row_a, expected_endpoint_minus_a)
)

K = sp.symbols("K")
endpoint_numerator = sp.Poly(
    (1 + (b - a) * K) * (x**2 - b**2) + (b - a) * (5 * b - x),
    x,
)
assert endpoint_numerator.degree() <= 2
assert endpoint_numerator.coeff_monomial(x) == -(b - a)

# Exact profile and grid counts.  Four-role selections are legal because
# the partial double leaves its mate; the final fixed pair has six moving
# doubles, hence five off-diagonal roots in the first variable.
p, doubles, singles = 8, 8, 1
assert 2 * doubles + singles == p + 9 == 17
assert doubles - 4 == 4  # outside a chosen four-role core
moving_pool = doubles - 2
assert moving_pool == 6
assert moving_pool - 1 == 5 > 4
assert moving_pool == 6 > 4


print("partial-to-full second-order lift: exact")
print("four-role cubic kernel and ruling reduction: exact")
print("strict bidegree-(4,4) six-double grid: exact")
print("endpoint linear coefficient and profile legality: exact")
