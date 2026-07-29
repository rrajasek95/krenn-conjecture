#!/usr/bin/env python3
"""Exact audit of the repeated-anchor seventh-split bivariate closure."""

import sympy as sp
# ---------------------------------------------------------------------------
# The repeated-pole row.
# ---------------------------------------------------------------------------

z, x, y, t, A, K = sp.symbols("z x y t A K")
q0, q1, q2, q3 = sp.symbols("q0 q1 q2 q3")


def psi(node, moving):
    return 1 / (moving - node) - 2 / (moving + node)


def eta(node, moving):
    return 1 / (moving - node) ** 2 + 2 / (moving + node) ** 2


# eta is the nodal derivative of psi, as required by a logarithmic
# second derivative.
tau = sp.symbols("tau")
assert sp.factor(sp.diff(psi(tau, x), tau).subs(tau, t) - eta(t, x)) == 0

dx = x**2 - t**2
dy = y**2 - t**2
psi_x_numerator = 3 * t - x
eta_x_numerator = 3 * x**2 - 2 * t * x + 3 * t**2
assert sp.factor(psi(t, x) - psi_x_numerator / dx) == 0
assert sp.factor(eta(t, x) - eta_x_numerator / dx**2) == 0

Y = A + psi(t, x) + psi(t, y)
M = Y**2 + K + eta(t, x) + eta(t, y)

# On ascending cubic coefficients, q''+2Yq'+Mq is this row.
repeated_row = [
    M,
    2 * Y + t * M,
    2 + 4 * t * Y + t**2 * M,
    6 * t + 6 * t**2 * Y + t**3 * M,
]

# Check the coefficient row directly on a symbolic cubic.
q = q0 + q1 * z + q2 * z**2 + q3 * z**3
assert sp.factor(
    sum(entry * coefficient for entry, coefficient in zip(
        repeated_row, (q0, q1, q2, q3)
    ))
    - (sp.diff(q, z, 2) + 2 * Y * sp.diff(q, z) + M * q).subs(z, t)
) == 0

repeated_cleared = [
    sp.cancel(dx**2 * dy**2 * entry).expand()
    for entry in repeated_row
]
assert all(sp.denom(entry) == 1 for entry in repeated_cleared)
assert max(sp.Poly(entry, x, y).degree(x) for entry in repeated_cleared) <= 4
assert max(sp.Poly(entry, x, y).degree(y) for entry in repeated_cleared) <= 4

# The double clearing is genuinely necessary.  At the two opposite poles,
# the minimally cleared row becomes a nonzero evaluation row.
evaluation = [1, t, t**2, t**3]
for entry, value in zip(repeated_cleared, evaluation):
    assert sp.factor(entry.subs(y, t) - 8 * t**2 * dx**2 * value) == 0
    assert sp.factor(entry.subs(y, -t) - 24 * t**2 * dx**2 * value) == 0


# Verify the product-rule derivation without dividing by the residual q.
H0, H1, H2 = sp.symbols("H0 H1 H2")
q_value = q0
q_prime = q1
q_second = q2
product_second = H2 * q_value + 2 * H1 * q_prime + H0 * q_second
derived = H0 * (
    q_second
    + 2 * (H1 / H0) * q_prime
    + (H2 / H0) * q_value
)
assert sp.cancel(product_second - derived) == 0


# ---------------------------------------------------------------------------
# Three simple rows and the sharp bidegree of the mixed determinant.
# ---------------------------------------------------------------------------


def simple_cleared_row(node, constant):
    local_y = constant + psi(node, x) + psi(node, y)
    denominator = (x**2 - node**2) * (y**2 - node**2)
    row = [
        local_y,
        1 + node * local_y,
        2 * node + node**2 * local_y,
        3 * node**2 + node**3 * local_y,
    ]
    answer = [sp.cancel(denominator * entry).expand() for entry in row]
    assert all(sp.denom(entry) == 1 for entry in answer)
    assert max(sp.Poly(entry, x, y).degree(x) for entry in answer) <= 2
    assert max(sp.Poly(entry, x, y).degree(y) for entry in answer) <= 2
    return answer


# A rational specialization proves that the nominal (10,10) bound is sharp;
# in particular, the hoped-for (8,8) bound is false.
numeric_nodes = [sp.Rational(1), sp.Rational(2), sp.Rational(3), sp.Rational(4)]
numeric_repeated = [
    entry.subs({t: numeric_nodes[0], A: sp.Rational(2, 3), K: sp.Rational(5, 7)})
    for entry in repeated_cleared
]
numeric_simple = [
    simple_cleared_row(numeric_nodes[i], sp.Rational(i + 2, i + 3))
    for i in range(1, 4)
]
numeric_determinant = sp.Poly(
    sp.Matrix([numeric_repeated] + numeric_simple).det(method="domain-ge"),
    x,
    y,
)
assert numeric_determinant.degree(x) == 10
assert numeric_determinant.degree(y) == 10
assert numeric_determinant.coeff_monomial(x**10 * y**10) == sp.Rational(
    19133, 630
)


# ---------------------------------------------------------------------------
# Endpoint division and the inherited three-anchor contradiction.
# ---------------------------------------------------------------------------

s = sp.symbols("s")
plus_shift = sp.factor(psi(s, t) + 1 / (s - t))
minus_shift = sp.factor(psi(s, -t) + 1 / (s - t))
assert sp.factor(plus_shift + 2 / (s + t)) == 0
assert sp.factor(minus_shift + 1 / (s + t) + 1 / (s - t)) == 0

# Multiplication q(z)=(z-t)r(z) is an exact basis map from quadratic
# coefficients to the cubic hyperplane q(t)=0.  The simple cubic Robin
# row restricts to (s-t) times the shifted quadratic Robin row.
Z = sp.symbols("Z")
factor_map = sp.Matrix(
    [
        [-t, 0, 0],
        [1, -t, 0],
        [0, 1, -t],
        [0, 0, 1],
    ]
)
assert sp.Matrix([[1, t, t**2, t**3]]) * factor_map == sp.zeros(1, 3)
cubic_simple = sp.Matrix(
    [[Z, 1 + s * Z, 2 * s + s**2 * Z, 3 * s**2 + s**3 * Z]]
)
quadratic_shifted = sp.Matrix(
    [[
        Z + 1 / (s - t),
        1 + s * (Z + 1 / (s - t)),
        2 * s + s**2 * (Z + 1 / (s - t)),
    ]]
)
assert all(
    sp.factor(entry) == 0
    for entry in cubic_simple * factor_map - (s - t) * quadratic_shifted
)

# With the evaluation row first, the corresponding four-by-four
# determinant is exactly the reduced three-by-three determinant times the
# three nonzero factors s_i-t.
s0, s1, s2, Z0, Z1, Z2 = sp.symbols("s0 s1 s2 Z0 Z1 Z2")
cubic_rows = []
quadratic_rows = []
for node, local_Z in ((s0, Z0), (s1, Z1), (s2, Z2)):
    cubic_rows.append(
        [
            local_Z,
            1 + node * local_Z,
            2 * node + node**2 * local_Z,
            3 * node**2 + node**3 * local_Z,
        ]
    )
    shifted = local_Z + 1 / (node - t)
    quadratic_rows.append(
        [shifted, 1 + node * shifted, 2 * node + node**2 * shifted]
    )
endpoint_determinant = sp.Matrix([[1, t, t**2, t**3]] + cubic_rows).det()
reduced_determinant = sp.Matrix(quadratic_rows).det()
assert sp.factor(
    endpoint_determinant
    - (s0 - t) * (s1 - t) * (s2 - t) * reduced_determinant
) == 0

# Recheck the final incompatible linear combination from the three-anchor
# quadratic Robin certificate.
a, b, c, U, V, W = sp.symbols("a b c U V W")
L_a = (a**2 - b**2) * V + (a**2 - c**2) * W + 2 * a - b - c
L_b = (a**2 - b**2) * U + (c**2 - b**2) * W + a - 2 * b + c
L_c = (a**2 - c**2) * U + (b**2 - c**2) * V + a + b - 2 * c
certificate = (
    -(b**2 - c**2) * L_a
    - (a**2 - c**2) * L_b
    + (a**2 - b**2) * L_c
)
assert sp.factor(certificate - 3 * (a - b) * (a - c) * (b - c)) == 0


# ---------------------------------------------------------------------------
# Strict value counts and the sharpened residual table.
# ---------------------------------------------------------------------------

for classes in range(16, 40):
    outside_fixed = classes - 4
    assert outside_fixed - 1 >= 11
    assert outside_fixed >= 12

# Residual double/single lists from the seventh-split frontier, followed by
# the removal of every d with c=p+9-d >= 16.
old_residuals = {
    8: list(range(1, 9)),
    9: list(range(1, 10)),
    10: list(range(1, 10)),
    11: [1, 2, 3, 4, 5, 6, 7, 9, 10],
    12: [1, 2, 3, 4, 5, 6, 7, 10],
    13: list(range(1, 8)),
}
expected_remaining = {
    8: list(range(2, 9)),
    9: list(range(3, 10)),
    10: list(range(4, 10)),
    11: [5, 6, 7, 9, 10],
    12: [6, 7, 10],
    13: [7],
}
for p, residuals in old_residuals.items():
    remaining = [d for d in residuals if p + 9 - d < 16]
    assert remaining == expected_remaining[p]

for p in range(14, 40):
    stable_residuals = range(1, 8)
    assert all(p + 9 - d >= 16 for d in stable_residuals)


print("repeated pole gives one second-order row: exact")
print("minimal repeated-row clearing and endpoint factors 8,24: exact")
print("mixed determinant bidegree (10,10), sharply not (8,8): exact")
print("endpoint reduction to the three-anchor nonidentity certificate: exact")
print("c>=16 grid counts and sharpened residual table: exact")
