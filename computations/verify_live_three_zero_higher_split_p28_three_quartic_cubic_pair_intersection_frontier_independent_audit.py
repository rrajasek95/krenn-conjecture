#!/usr/bin/env python3
"""Independent exact audit of the p=28 cubic-pair frontier.

The construction starts only from the two displayed cubic rows.  It solves
the degree-four syzygy problem afresh and imports no primary checker.
"""

from itertools import combinations

import sympy as sp


t, z, sigma = sp.symbols("t z sigma")


def polynomial_gcd(polynomials: list[sp.Poly]) -> sp.Poly:
    result = polynomials[0]
    for polynomial in polynomials[1:]:
        result = sp.gcd(result, polynomial)
    return result.monic()


def coefficient_column(vector: sp.Matrix, variable: sp.Symbol, degree: int) -> sp.Matrix:
    return sp.Matrix(
        [sp.Poly(entry, variable).coeff_monomial(variable**degree) for entry in vector]
    )


def polynomial_column(polynomial: sp.Expr, variable: sp.Symbol, cap: int) -> sp.Matrix:
    poly = sp.Poly(sp.expand(polynomial), variable)
    return sp.Matrix([poly.coeff_monomial(variable**j) for j in range(cap + 1)])


def row_coefficients(row: list[sp.Expr]) -> list[sp.Matrix]:
    return [
        sp.Matrix([[sp.Poly(entry, t).coeff_monomial(t**degree) for entry in row]])
        for degree in range(4)
    ]


lambda_row = [
    -t**2 - t - 1,
    t**2 + t - 1,
    t**3 - t**2 + t,
    -t**3 + t**2 + t - 1,
    t**3 + t,
    t**2 + 1,
]
mu_row = [
    -t**3 - t**2 + 1,
    0,
    t**3 - t**2 + t,
    -t**3 - t**2 - t - 1,
    -t**3 - t**2 - 1,
    t**3 + t + 1,
]


# The coefficient covectors have the claimed 4+4 -> 6 incidence.
lambda_coeff = row_coefficients(lambda_row)
mu_coeff = row_coefficients(mu_row)
lambda_coefficient_span = sp.Matrix.vstack(*lambda_coeff)
mu_coefficient_span = sp.Matrix.vstack(*mu_coeff)

assert lambda_coefficient_span.rank() == 4
assert mu_coefficient_span.rank() == 4
assert sp.Matrix.vstack(lambda_coefficient_span, mu_coefficient_span).rank() == 6


# Solve ker(lambda,mu,lambda',mu') among six-vector polynomials of degree <=4.
four_rows = [
    lambda_row,
    mu_row,
    [sp.diff(entry, t) for entry in lambda_row],
    [sp.diff(entry, t) for entry in mu_row],
]
unknowns = sp.symbols("x0:30")
candidate = [
    sum((unknowns[5 * coordinate + degree] * t**degree for degree in range(5)), sp.Integer(0))
    for coordinate in range(6)
]
equations = []
for row in four_rows:
    expression = sp.Poly(
        sp.expand(sum((row[j] * candidate[j] for j in range(6)), sp.Integer(0))), t
    )
    equations.extend(expression.coeff_monomial(t**degree) for degree in range(8))

syzygy_matrix, _ = sp.linear_eq_to_matrix(equations, unknowns)
syzygy_nullspace = syzygy_matrix.nullspace()

assert syzygy_matrix.shape == (32, 30)
assert syzygy_matrix.rank() == 28
assert len(syzygy_nullspace) == 2

E, O = [
    sp.Matrix(
        [
            sp.factor(
                sum(
                    (solution[5 * coordinate + degree] * t**degree for degree in range(5)),
                    sp.Integer(0),
                )
            )
            for coordinate in range(6)
        ]
    )
    for solution in syzygy_nullspace
]

for row in four_rows:
    assert sp.expand(sum((row[j] * E[j] for j in range(6)), sp.Integer(0))) == 0
    assert sp.expand(sum((row[j] * O[j] for j in range(6)), sp.Integer(0))) == 0


# Both the finite line subbundle and its value at infinity are primitive.
EO_matrix = sp.Matrix.hstack(E, O)
EO_minors = []
for rows in combinations(range(6), 2):
    minor = sp.factor(EO_matrix[list(rows), :].det())
    if minor != 0:
        EO_minors.append(sp.Poly(minor, t, domain=sp.QQ))
assert sp.expand(polynomial_gcd(EO_minors).as_expr() - 1) == 0
assert sp.Matrix.hstack(coefficient_column(E, t, 4), coefficient_column(O, t, 4)).rank() == 2


# Low and high coefficient projections prove no cover-branch defect and give
# echelon degrees 4,5,6,7,8,9.
low_projection = sp.Matrix.hstack(
    coefficient_column(E, t, 0),
    coefficient_column(O, t, 0),
    coefficient_column(E, t, 1),
    coefficient_column(O, t, 1),
    coefficient_column(E, t, 2),
    coefficient_column(O, t, 2),
)
high_projection = sp.Matrix.hstack(
    coefficient_column(O, t, 4),
    coefficient_column(E, t, 4),
    coefficient_column(O, t, 3),
    coefficient_column(E, t, 3),
    coefficient_column(O, t, 2),
    coefficient_column(E, t, 2),
)

assert low_projection.det() != 0
assert high_projection.det() != 0

F = sp.Matrix([sp.expand(E[j].subs(t, z**2) + z * O[j].subs(t, z**2)) for j in range(6)])
F_coefficients = sp.Matrix.hstack(*(polynomial_column(entry, z, 9) for entry in F))
assert F_coefficients.rank() == 6
assert max(sp.degree(entry, z) for entry in F) <= 9


# Reconstruct U(C,D) directly from coefficient comparison in sigma.
def row_dot_F(row: sp.Matrix) -> sp.Expr:
    return sp.expand((row * F)[0])


C = row_dot_F(lambda_coeff[3])
D = sp.expand(row_dot_F(lambda_coeff[2]) + 2 * z**2 * C)
P = row_dot_F(mu_coeff[3])
Q = sp.expand(row_dot_F(mu_coeff[2]) + 2 * z**2 * P)


def audit_cubic_identity(
    coefficient_rows: list[sp.Matrix], first: sp.Expr, second: sp.Expr
) -> sp.Matrix:
    expected = [
        first,
        second - 2 * z**2 * first,
        z**4 * first - 2 * z**2 * second,
        z**4 * second,
    ]
    for degree in range(4):
        assert sp.expand(row_dot_F(coefficient_rows[degree]) - expected[3 - degree]) == 0

    row_at_sigma = sum(
        (sigma**degree * coefficient_rows[degree] for degree in range(4)),
        sp.zeros(1, 6),
    )
    identity = sp.expand(
        row_dot_F(row_at_sigma) - (sigma - z**2) ** 2 * (first * sigma + second)
    )
    assert identity == 0
    return sp.Matrix.hstack(*(polynomial_column(polynomial, z, 9) for polynomial in expected))


U_lambda = audit_cubic_identity(lambda_coeff, C, D)
U_mu = audit_cubic_identity(mu_coeff, P, Q)

assert U_lambda.rank() == 4
assert U_mu.rank() == 4
assert sp.Matrix.hstack(U_lambda, U_mu).rank() == 6
assert U_lambda.rank() + U_mu.rank() - sp.Matrix.hstack(U_lambda, U_mu).rank() == 2


# The cubic frame is primitive and row-reduced.  These two exact checks give
# Forney/splitting degrees (3,3), rather than merely two rows of degree <=3.
annihilator_frame = sp.Matrix([lambda_row, mu_row])
frame_minors = []
for columns in combinations(range(6), 2):
    minor = sp.factor(annihilator_frame[:, list(columns)].det())
    if minor != 0:
        frame_minors.append(sp.Poly(minor, t, domain=sp.QQ))
leading_frame = sp.Matrix(
    [
        [sp.Poly(entry, t).coeff_monomial(t**3) for entry in lambda_row],
        [sp.Poly(entry, t).coeff_monomial(t**3) for entry in mu_row],
    ]
)

assert sp.expand(polynomial_gcd(frame_minors).as_expr() - 1) == 0
assert leading_frame.rank() == 2
assert max(sp.degree(entry, t) for entry in lambda_row) == 3
assert max(sp.degree(entry, t) for entry in mu_row) == 3


# Split a(z^2)+z b(z^2), and independently derive the determinant of eta from
# differentiating lambda'(t)E(t)=lambda'(t)O(t)=0.
def even_odd_parts(polynomial: sp.Expr) -> tuple[sp.Expr, sp.Expr]:
    poly = sp.Poly(sp.expand(polynomial), z)
    cap = poly.degree()
    even = sum(
        (poly.coeff_monomial(z ** (2 * degree)) * t**degree for degree in range(cap // 2 + 1)),
        sp.Integer(0),
    )
    odd = sum(
        (
            poly.coeff_monomial(z ** (2 * degree + 1)) * t**degree
            for degree in range((cap - 1) // 2 + 1)
        ),
        sp.Integer(0),
    )
    return sp.expand(even), sp.expand(odd)


R_lambda = sp.expand(z**2 * C + D)
R_mu = sp.expand(z**2 * P + Q)
a, b = even_odd_parts(R_lambda)
c, d = even_odd_parts(R_mu)
kappa = sp.factor(a * d - b * c)
kappa_target = 2 * t**6 + 6 * t**5 - 249 * t**4 - 56 * t**3 + 81 * t**2 + 15 * t + 3

lambda_prime = sp.Matrix([[sp.diff(entry, t) for entry in lambda_row]])
mu_prime = sp.Matrix([[sp.diff(entry, t) for entry in mu_row]])
eta_matrix = sp.Matrix(
    [
        [(lambda_prime * E.diff(t))[0], (lambda_prime * O.diff(t))[0]],
        [(mu_prime * E.diff(t))[0], (mu_prime * O.diff(t))[0]],
    ]
)
R_matrix = sp.Matrix([[a, b], [c, d]])

assert eta_matrix.applyfunc(sp.expand) == (-2 * R_matrix).applyfunc(sp.expand)
assert sp.expand(eta_matrix.det() - 4 * kappa) == 0
assert sp.degree(kappa, t) == 6
assert sp.rem(sp.Poly(kappa, t), sp.Poly(kappa_target, t)) == 0
assert sp.gcd(sp.Poly(kappa_target, t), sp.Poly(sp.diff(kappa_target, t), t)).degree() == 0


# Its zero divisor is also exactly the scalar gcd of E^O^E'^O'.
derivative_wedge_matrix = sp.Matrix.hstack(E, O, E.diff(t), O.diff(t))
wedge_minors = []
for rows in combinations(range(6), 4):
    minor = sp.factor(derivative_wedge_matrix[list(rows), :].det())
    if minor != 0:
        wedge_minors.append(sp.Poly(minor, t, domain=sp.QQ))
wedge_gcd = polynomial_gcd(wedge_minors)
assert sp.expand(wedge_gcd.as_expr() - sp.Poly(kappa_target, t).monic().as_expr()) == 0


# The ordinary Wronskian has full cap degree, no zero at 0 or infinity, and no
# repeated finite root.  In particular it cannot have the desired 3/2 profile.
ordinary_wronskian = sp.expand(
    sp.Matrix([[sp.diff(entry, z, derivative) for entry in F] for derivative in range(6)]).det()
)
ordinary_wronskian_poly = sp.Poly(ordinary_wronskian, z, domain=sp.QQ)

assert ordinary_wronskian_poly.degree() == 24
assert ordinary_wronskian_poly.coeff_monomial(1) != 0
assert ordinary_wronskian_poly.LC() != 0
assert sp.gcd(ordinary_wronskian_poly, ordinary_wronskian_poly.diff()).degree() == 0


# The separated shift is an abstract six-dimensional calculation.  Coordinates
# are ordered C,tC,t^2C,D,tD,t^2D.
c_shift = sp.symbols("c_shift", nonzero=True)
standard = [sp.eye(6)[:, j] for j in range(6)]
U_shift_0 = sp.Matrix.hstack(
    standard[0],
    standard[3] - 2 * standard[1],
    standard[2] - 2 * standard[4],
    standard[5],
)
U_shift_c = sp.Matrix.hstack(
    standard[0],
    standard[3] + c_shift * standard[0] - 2 * standard[1],
    standard[2] - 2 * standard[4] - 2 * c_shift * standard[1],
    standard[5] + c_shift * standard[2],
)
claimed_intersection = sp.Matrix.hstack(standard[0], standard[3] - 2 * standard[1])

assert U_shift_0.rank() == 4
assert U_shift_c.rank() == 4
assert sp.Matrix.hstack(U_shift_0, U_shift_c).rank() == 6
assert U_shift_0.rank() + U_shift_c.rank() - sp.Matrix.hstack(U_shift_0, U_shift_c).rank() == 2
assert sp.Matrix.hstack(U_shift_0, claimed_intersection).rank() == 4
assert sp.Matrix.hstack(U_shift_c, claimed_intersection).rank() == 4


# Its primitive four-plane has the two quadratic block annihilators.
u = sp.Matrix([1, t, t**2])
u_prime = u.diff(t)
block_u_1 = sp.Matrix.vstack(u, sp.zeros(3, 1))
block_u_2 = sp.Matrix.vstack(sp.zeros(3, 1), u)
block_du_1 = sp.Matrix.vstack(u_prime, sp.zeros(3, 1))
block_du_2 = sp.Matrix.vstack(sp.zeros(3, 1), u_prime)
quadratic_frame = sp.Matrix(
    [[t**2, -2 * t, 1, 0, 0, 0], [0, 0, 0, t**2, -2 * t, 1]]
)

for vector in (block_u_1, block_u_2, block_du_1, block_du_2):
    assert quadratic_frame * vector == sp.zeros(2, 1)
assert sp.Matrix(
    [[sp.Poly(entry, t).coeff_monomial(t**2) for entry in quadratic_frame.row(row)] for row in range(2)]
).rank() == 2


# Verify the Delta^2 scalar exactly with formal first jets of p,q,r,s.
p, q, r, ss, p1, q1, r1, s1 = sp.symbols("p q r ss p1 q1 r1 s1")
E_sep = p * block_u_1 + r * block_u_2
O_sep = q * block_u_1 + ss * block_u_2
E_sep_prime = p1 * block_u_1 + r1 * block_u_2 + p * block_du_1 + r * block_du_2
O_sep_prime = q1 * block_u_1 + s1 * block_u_2 + q * block_du_1 + ss * block_du_2
separated_wedge = sp.Matrix.hstack(E_sep, O_sep, E_sep_prime, O_sep_prime)
primitive_wedge = sp.Matrix.hstack(block_u_1, block_u_2, block_du_1, block_du_2)
Delta = p * ss - q * r

for rows in combinations(range(6), 4):
    assert sp.expand(
        separated_wedge[list(rows), :].det() - Delta**2 * primitive_wedge[list(rows), :].det()
    ) == 0


# Re-derive the Crum invariant and its constant in differential algebra.  Here
# rho_j denotes D^j rho for D=(2z)^(-1)d/dz.
rho = sp.symbols("rho0:7")


def D_operator(expression: sp.Expr) -> sp.Expr:
    return sp.expand(
        sp.diff(expression, t)
        + sp.diff(expression, z) / (2 * z)
        + sum((sp.diff(expression, rho[j]) * rho[j + 1] for j in range(6)), sp.Integer(0))
    )


def ordinary_derivative(expression: sp.Expr) -> sp.Expr:
    return sp.expand(2 * z * D_operator(expression))


transformed = [
    8 * z**3 * rho[3],
    8 * z**3 * (t * rho[3] + 3 * rho[2]),
    8 * z**3 * (t**2 * rho[3] + 6 * t * rho[2] + 6 * rho[1]),
]
transformed_wronskian = sp.Matrix(
    [
        transformed,
        [ordinary_derivative(entry) for entry in transformed],
        [ordinary_derivative(ordinary_derivative(entry)) for entry in transformed],
    ]
).det()
Crum_invariant = (
    -12 * rho[1] * rho[3] * rho[5]
    + 15 * rho[1] * rho[4] ** 2
    + 18 * rho[2] ** 2 * rho[5]
    - 60 * rho[2] * rho[3] * rho[4]
    + 40 * rho[3] ** 3
)
assert sp.factor(16 * z**3 * transformed_wronskian - 2**17 * z**15 * Crum_invariant) == 0


# The norm screen is a necessary sign-free identity.  A generic exact sample
# checks all exponents and signs; the accompanying audit gives the factor proof.
triple_values = [1, 2, 3, 4, 5, 6]
quartic_values = [7, 8, 9]
T = sp.prod(z - value for value in triple_values)
R = sp.prod(z - value for value in quartic_values)
K = sp.prod(t - value**2 for value in triple_values)
H = -sp.prod(t - value**2 for value in quartic_values)
target_wronskian = sp.expand(T**3 * R**2)
assert sp.expand(T * T.subs(z, -z) - K.subs(t, z**2)) == 0
assert sp.expand(R * R.subs(z, -z) - H.subs(t, z**2)) == 0
assert sp.expand(
    target_wronskian * target_wronskian.subs(z, -z)
    - K.subs(t, z**2) ** 3 * H.subs(t, z**2) ** 2
) == 0


# Finally reconstruct the local jet-minor partitions.  Multiplication by a
# regular unit is lower triangular on jets and hence does not change ranks.
def local_partition_audit(orders: list[int], jet_cut: int, expected_weight: int) -> None:
    functions = [z**order for order in orders]
    jet_matrix = sp.Matrix(
        [[sp.diff(function, z, derivative).subs(z, 0) for derivative in range(jet_cut + 1)] for function in functions]
    )
    preceding_matrix = jet_matrix[:, :jet_cut]
    W = sp.factor(
        sp.Matrix(
            [[sp.diff(function, z, derivative) for function in functions] for derivative in range(6)]
        ).det()
    )
    W_poly = sp.Poly(W, z)
    valuation = min(monomial[0] for monomial, coefficient in W_poly.terms() if coefficient != 0)
    assert preceding_matrix.rank() == jet_cut
    assert jet_matrix.rank() == jet_cut
    assert valuation == expected_weight
    assert sum(order - index for index, order in enumerate(orders)) == expected_weight


local_partition_audit([0, 1, 2, 4, 5, 6], jet_cut=3, expected_weight=3)
local_partition_audit([0, 1, 2, 3, 5, 6], jet_cut=4, expected_weight=2)


print("p=28 cubic-pair intersection frontier independent audit: PASS")
print("cubic coefficient ranks=4,4, joint=6; U-space intersection dimension=2")
print("shift branch=(2,2) with Delta^2 scalar; transverse branch primitive=(3,3)")
print(f"kappa={kappa_target}; squarefree degree=6; derivative-wedge gcd=kappa")
print("echelon degrees=4..9; Wronskian degree=24, squarefree, nonzero at 0 and infinity")
print("norm exponents and triple/quartic jet-minor partitions reconstructed")
