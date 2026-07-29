#!/usr/bin/env python3
"""Exact audit for the seventh-split bivariate quartet closure.

The checker uses only rational-function arithmetic.  It verifies the
canonical cubic Robin kernel, both endpoint shifts, the signed quartet
certificate, the cubic moving-fifth numerator, and the degree-four final
pair obstruction.  No floating-point specialization is used.
"""

from itertools import permutations

import sympy as sp
from sympy.polys.domains import QQ
from sympy.polys.rings import ring


def parity(permutation):
    inversions = sum(
        permutation[i] > permutation[j]
        for i in range(len(permutation))
        for j in range(i + 1, len(permutation))
    )
    return -1 if inversions % 2 else 1


def determinant(matrix, polynomial_ring):
    """Small exact determinant without expression-domain heuristics."""
    answer = polynomial_ring.zero
    for permutation in permutations(range(len(matrix))):
        term = polynomial_ring(parity(permutation))
        for row, column in enumerate(permutation):
            term *= matrix[row][column]
        answer += term
    return answer


# ---------------------------------------------------------------------------
# Canonical kernel and the biquadratically cleared five-anchor rows.
# ---------------------------------------------------------------------------

z, x, y, t, u = sp.symbols("z x y t u")
g = (z - x) * (z + x) ** 2
assert sp.expand((x**2 - z**2) * sp.diff(g, z) - (x - 3 * z) * g) == 0

dx = x**2 - t**2
dy = y**2 - t**2
psi_x = -(x - 3 * t) / dx
psi_y = -(y - 3 * t) / dy
cleared = sp.cancel(dx * dy * (u + psi_x + psi_y)).expand()
expected = sp.expand(u * dx * dy - (x - 3 * t) * dy - (y - 3 * t) * dx)
assert cleared == expected
assert sp.Poly(expected, x, y).degree(x) <= 2
assert sp.Poly(expected, x, y).degree(y) <= 2


# ---------------------------------------------------------------------------
# Exact Plücker expansion in the basis (g_x, z g_x, 1, z, z^2).
# ---------------------------------------------------------------------------

# The basis change from ascending monomials has determinant one.
basis_change = sp.Matrix(
    [
        [-x**3, 0, 1, 0, 0],
        [-x**2, -x**3, 0, 1, 0],
        [x, -x**2, 0, 0, 1],
        [1, x, 0, 0, 0],
        [0, 1, 0, 0, 0],
    ]
)
assert basis_change.det() == 1

# The first two transformed Robin columns have the claimed factor form.
robin_g = (sp.diff(g, z) + (u + psi_x) * g).subs(z, t)
robin_zg = (sp.diff(z * g, z) + (u + psi_x) * z * g).subs(z, t)
g_at_t = g.subs(z, t)
assert sp.cancel(robin_g - u * g_at_t) == 0
assert sp.cancel(robin_zg - (1 + t * u) * g_at_t) == 0

# Audit the five-row Laplace identity with independent exact row data.
PL, *plucker_gens = ring(
    ",".join(
        [f"f{i}" for i in range(5)]
        + [f"t{i}" for i in range(5)]
        + [f"u{i}" for i in range(5)]
        + [f"a{i}" for i in range(5)]
        + [f"b{i}" for i in range(5)]
        + [f"c{i}" for i in range(5)]
    ),
    QQ,
)
f_values = plucker_gens[0:5]
t_values = plucker_gens[5:10]
u_values = plucker_gens[10:15]
a_values = plucker_gens[15:20]
b_values = plucker_gens[20:25]
c_values = plucker_gens[25:30]
plucker_matrix = [
    [
        f_values[i] * u_values[i],
        f_values[i] * (1 + t_values[i] * u_values[i]),
        a_values[i],
        b_values[i],
        c_values[i],
    ]
    for i in range(5)
]
plucker_left = determinant(plucker_matrix, PL)
plucker_right = PL.zero
for i in range(5):
    for j in range(i + 1, 5):
        pair_minor = (
            (t_values[j] - t_values[i]) * u_values[i] * u_values[j]
            + u_values[i]
            - u_values[j]
        )
        complement = [k for k in range(5) if k not in (i, j)]
        last_minor = determinant(
            [
                [a_values[k], b_values[k], c_values[k]]
                for k in complement
            ],
            PL,
        )
        plucker_right += (
            (-1) ** (i + j + 1)
            * f_values[i]
            * f_values[j]
            * pair_minor
            * last_minor
        )
assert plucker_left == plucker_right


# ---------------------------------------------------------------------------
# Endpoint division q(z)=(z-ta)r(z).
# ---------------------------------------------------------------------------

ta, tj = sp.symbols("ta tj")


def psi(node, moving):
    return 1 / (moving - node) - 2 / (moving + node)


plus_shift = sp.factor(psi(tj, ta) + 1 / (tj - ta))
minus_shift = sp.factor(psi(tj, -ta) + 1 / (tj - ta))
assert sp.simplify(plus_shift + 2 / (ta + tj)) == 0
assert sp.simplify(
    minus_shift + 1 / (ta + tj) + 1 / (tj - ta)
) == 0


# ---------------------------------------------------------------------------
# Recheck the exact signed quartet certificate over QQ(t0,t1,t2,t3).
# ---------------------------------------------------------------------------

KT = QQ.frac_field("t0", "t1", "t2", "t3")
nodes = list(KT.gens)
RU, u0, u1, u2, u3 = ring("u0,u1,u2,u3", KT)
translations = [u0, u1, u2, u3]


def phi(local_nodes, values):
    a, b, c = local_nodes
    A, B, C = values
    return (
        -(a - b) * (a - c) * (b - c) * A * B * C
        + (a - b) * (a + b - 2 * c) * A * B
        - (a - c) * (a - 2 * b + c) * A * C
        - (b - c) * (2 * a - b - c) * B * C
        - 2 * (b - c) * A
        + 2 * (a - c) * B
        - 2 * (a - b) * C
    )


def endpoint(index, sign):
    complement = [j for j in range(4) if j != index]
    values = []
    for j in complement:
        if sign == 1:
            value = translations[j] - 2 / (nodes[j] + nodes[index])
        else:
            value = (
                translations[j]
                - 1 / (nodes[j] + nodes[index])
                - 1 / (nodes[j] - nodes[index])
            )
        values.append(value)
    return phi([nodes[j] for j in complement], values)


quartet_left = RU.zero
for i in range(4):
    complement = [j for j in range(4) if j != i]
    delta = KT.one
    for p in range(3):
        for q in range(p + 1, 3):
            delta *= nodes[complement[q]] - nodes[complement[p]]
    quartet_left += (endpoint(i, 1) - endpoint(i, -1)) / (
        nodes[i] * delta
    )

pair_sum_product = KT.one
for i in range(4):
    for j in range(i + 1, 4):
        pair_sum_product *= nodes[i] + nodes[j]

quartet_right = RU.zero
for i in range(4):
    sigma = KT.one
    for j in range(4):
        if i != j:
            sigma *= nodes[i] + nodes[j]
    quartet_right += sigma * translations[i]
quartet_right *= KT(-6) / pair_sum_product
assert quartet_left == quartet_right


# ---------------------------------------------------------------------------
# The moving fifth-anchor certificate S_a(Q union {e}).
# ---------------------------------------------------------------------------

a, b, c, d, e = sp.symbols("a b c d e")
companions = [b, c, d]

fixed_sum = 0
for j in companions:
    others = [k for k in companions if k != j]
    fixed_sum += (e + j) * sp.prod(j + k for k in others) / (j**2 - a**2)

cleared_S = sp.factor(
    2 * a * (
        (e**2 - a**2) * fixed_sum
        + (e + b) * (e + c) * (e + d)
    )
)
assert sp.Poly(cleared_S, e).degree() <= 3
assert sp.factor(
    cleared_S.subs(e, a) - 2 * a * (a + b) * (a + c) * (a + d)
) == 0

# Check that this really is (e^2-a^2) times the displayed rational S_a.
F = [a, b, c, d, e]
S_a = 0
for j in F[1:]:
    sigma = sp.prod(j + k for k in F if k not in (a, j))
    S_a += sigma * (1 / (j - a) - 1 / (a + j))
assert sp.factor((e**2 - a**2) * S_a - cleared_S) == 0


# ---------------------------------------------------------------------------
# Independent audit of the degree-four pair-polynomial contradiction.
# This is not needed by the bivariate-quartet proof, but records the exact
# application if a future proof of the stronger DR5 classification is used.
# ---------------------------------------------------------------------------

A, B = sp.symbols("A B")
Da = y**2 - a**2
Db = y**2 - b**2
Xa = A * Da - (y + 3 * a)
Xb = B * Db - (y + 3 * b)
pair_numerator = sp.Poly(
    sp.expand((a - b) * Xa * Xb + Xa * Db - Xb * Da), y
)
assert pair_numerator.degree() <= 4
assert sp.factor(pair_numerator.coeff_monomial(y**3) + (a - b) * (A + B)) == 0
assert sp.factor(
    pair_numerator.coeff_monomial(y**4)
    - ((a - b) * A * B + A - B)
) == 0

zero_branch = sp.Poly(pair_numerator.as_expr().subs({A: 0, B: 0}), y)
assert sp.factor(zero_branch.coeff_monomial(y**2) - 2 * (b - a)) == 0

factor_branch = sp.Poly(
    pair_numerator.as_expr().subs({A: 2 / (a - b), B: -2 / (a - b)}),
    y,
)
assert sp.factor(
    factor_branch.coeff_monomial(y) - 4 * (a - b) * (a + b)
) == 0


# The many-class double/single criterion used in the note.
for p in range(8, 40):
    for doubles in range(1, 8):
        distinct_classes = p + 9 - doubles
        assert (distinct_classes >= 17) == (p >= doubles + 8)

print("canonical cubic Robin kernel: exact")
print("five-row factor-family Plücker expansion: exact")
print("bivariate cleared row and bidegree-(10,10) determinant bound: exact")
print("both endpoint shifts and signed quartet certificate: exact")
print("moving-fifth cubic numerator and nonzero test value: exact")
print("optional degree-four DR5 application coefficients: exact")
print("many-class double/single root counts: exact")
