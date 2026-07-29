#!/usr/bin/env python3
"""Exact audit of the p=28 cubic-pair intersection frontier.

This checks:
  * the separated shift family has primitive splitting (2,2), not (3,3);
  * the Crum formula for its ordinary Wronskian;
  * an exact transverse pair of cubic annihilator rows whose induced
    four-spaces meet in dimension two inside a saturated-boundary
    six-space with genuine primitive splitting (3,3);
  * the transverse example has a squarefree sextic residual determinant
    but a generic squarefree degree-24 ordinary Wronskian, so intersection
    alone does not impose the target 4^3 3^6 ramification.
"""

from itertools import combinations
from math import gcd

import sympy as sp


t, z, s = sp.symbols("t z s")


def coefficient_vector(row: list[sp.Expr], degree: int) -> sp.Matrix:
    return sp.Matrix([sp.Poly(entry, t).coeff_monomial(t**degree) for entry in row])


def polynomial_coefficient_matrix(polynomials: list[sp.Expr], max_degree: int = 9) -> sp.Matrix:
    return sp.Matrix(
        [
            [sp.Poly(poly, z).coeff_monomial(z**degree) for poly in polynomials]
            for degree in range(max_degree + 1)
        ]
    )


def primitive_integer_syzygies(
    lam: list[sp.Expr], mu: list[sp.Expr]
) -> tuple[sp.Matrix, sp.Matrix]:
    """Degree-at-most-four kernel of lam,mu,lam',mu' over Q[t]."""

    variables = sp.symbols("x0:30")
    vector = [
        sum(variables[5 * j + degree] * t**degree for degree in range(5))
        for j in range(6)
    ]
    equations: list[sp.Expr] = []
    for row in (lam, mu, [sp.diff(x, t) for x in lam], [sp.diff(x, t) for x in mu]):
        identity = sp.Poly(sum(row[j] * vector[j] for j in range(6)), t)
        equations.extend(identity.coeff_monomial(t**degree) for degree in range(8))
    matrix, _ = sp.linear_eq_to_matrix(equations, variables)
    nullspace = matrix.nullspace()
    assert len(nullspace) == 2

    answer = []
    for basis_vector in nullspace:
        denominator = sp.ilcm(*[int(sp.denom(entry)) for entry in basis_vector])
        integers = [int(entry * denominator) for entry in basis_vector]
        content = gcd(*[abs(entry) for entry in integers if entry])
        integers = [entry // content for entry in integers]
        answer.append(
            sp.Matrix(
                [
                    sum(integers[5 * j + degree] * t**degree for degree in range(5))
                    for j in range(6)
                ]
            )
        )
    return answer[0], answer[1]


def monic(poly: sp.Expr, variable: sp.Symbol) -> sp.Expr:
    return sp.Poly(poly, variable).monic().as_expr()


def parity_rows(poly: sp.Expr) -> tuple[sp.Expr, sp.Expr]:
    """Return a(t),b(t) with poly(z)=a(z^2)+z b(z^2)."""

    source = sp.Poly(sp.expand(poly), z)
    even = sum(source.coeff_monomial(z ** (2 * degree)) * t**degree for degree in range(5))
    odd = sum(source.coeff_monomial(z ** (2 * degree + 1)) * t**degree for degree in range(5))
    return sp.expand(even), sp.expand(odd)


def induced_pair(row: list[sp.Expr], F: sp.Matrix) -> tuple[sp.Expr, sp.Expr]:
    coefficients = [coefficient_vector(row, degree) for degree in range(4)]
    C = sp.expand(coefficients[3].dot(F))
    D = sp.expand(coefficients[2].dot(F) + 2 * z**2 * C)
    return C, D


def U(C: sp.Expr, D: sp.Expr) -> list[sp.Expr]:
    square = z**2
    return [
        C,
        D - 2 * square * C,
        square**2 * C - 2 * square * D,
        square**2 * D,
    ]


# ---------------------------------------------------------------------------
# 1. The separated shift family.
# ---------------------------------------------------------------------------

C0 = 1 + 2 * z + z**4
D0 = 1 - z + z**2 + z**5
c = sp.Integer(3)
first = U(C0, D0)
shifted = U(C0, D0 + c * C0)
first_matrix = polynomial_coefficient_matrix(first)
shifted_matrix = polynomial_coefficient_matrix(shifted)
assert first_matrix.rank() == 4
assert shifted_matrix.rank() == 4
assert first_matrix.row_join(shifted_matrix).rank() == 6
assert first_matrix.rank() + shifted_matrix.rank() - first_matrix.row_join(shifted_matrix).rank() == 2

# The sum is C<P_2(z^2)> direct-sum D<P_2(z^2)>.
separated_basis = [
    C0,
    z**2 * C0,
    z**4 * C0,
    D0,
    z**2 * D0,
    z**4 * D0,
]
assert polynomial_coefficient_matrix(separated_basis).rank() == 6
shift_sum = polynomial_coefficient_matrix(first + shifted)
separated_matrix = polynomial_coefficient_matrix(separated_basis)
assert shift_sum.row_join(separated_matrix).rank() == 6

# Its primitive annihilator has two quadratic block rows.
u = sp.Matrix([1, t, t**2])
v = sp.Matrix([t**2, -2 * t, 1])
p, q = parity_rows(C0)
r, w = parity_rows(D0)
E_sep = sp.Matrix.vstack(p * u, r * u)
O_sep = sp.Matrix.vstack(q * u, w * u)
ann1 = sp.Matrix([[t**2, -2 * t, 1, 0, 0, 0]])
ann2 = sp.Matrix([[0, 0, 0, t**2, -2 * t, 1]])
for ann in (ann1, ann2):
    for section in (E_sep, O_sep, E_sep.diff(t), O_sep.diff(t)):
        assert sp.expand((ann * section)[0]) == 0

# The derivative four-wedge has the square scalar (p*w-q*r)^2.
delta = sp.expand(p * w - q * r)
moving_sep = sp.Matrix.hstack(E_sep, O_sep, E_sep.diff(t), O_sep.diff(t))
sep_minors = [
    sp.expand(moving_sep[list(rows), :].det())
    for rows in combinations(range(6), 4)
]
sep_gcd = sp.factor(sp.gcd_list([minor for minor in sep_minors if minor]))
assert monic(sep_gcd, t) == monic(delta**2, t)
assert sp.degree(delta, t) <= 4

# Exact Crum formula for the ordinary Wronskian of C<P_2(t)>+D<P_2(t)>.
wronskian_sep = sp.factor(
    sp.det(
        sp.Matrix(
            [[sp.diff(poly, z, order) for poly in separated_basis] for order in range(6)]
        )
    )
)
Dt = lambda expression: sp.cancel(sp.diff(expression, z) / (2 * z))
ratio = sp.cancel(D0 / C0)
derivatives = [ratio]
for _ in range(5):
    derivatives.append(Dt(derivatives[-1]))
r1, r2, r3, r4, r5 = derivatives[1:]
invariant = (
    -12 * r1 * r3 * r5
    + 15 * r1 * r4**2
    + 18 * r2**2 * r5
    - 60 * r2 * r3 * r4
    + 40 * r3**3
)
assert sp.cancel(wronskian_sep - 2**17 * z**15 * C0**6 * invariant) == 0


# ---------------------------------------------------------------------------
# 2. A genuine transverse (3,3) pair.
# ---------------------------------------------------------------------------

lam = [
    -t**2 - t - 1,
    t**2 + t - 1,
    t**3 - t**2 + t,
    -t**3 + t**2 + t - 1,
    t**3 + t,
    t**2 + 1,
]
mu = [
    -t**3 - t**2 + 1,
    0,
    t**3 - t**2 + t,
    -t**3 - t**2 - t - 1,
    -t**3 - t**2 - 1,
    t**3 + t + 1,
]

lam_coefficients = sp.Matrix.hstack(*(coefficient_vector(lam, degree) for degree in range(4)))
mu_coefficients = sp.Matrix.hstack(*(coefficient_vector(mu, degree) for degree in range(4)))
assert lam_coefficients.rank() == 4
assert mu_coefficients.rank() == 4
assert lam_coefficients.row_join(mu_coefficients).rank() == 6

E, O = primitive_integer_syzygies(lam, mu)
for row in (sp.Matrix([lam]), sp.Matrix([mu])):
    for section in (E, O, E.diff(t), O.diff(t)):
        assert sp.expand((row * section)[0]) == 0
assert max(sp.degree(entry, t) for entry in E) <= 4
assert max(sp.degree(entry, t) for entry in O) <= 4

F = E.subs(t, z**2) + z * O.subs(t, z**2)
K_matrix = polynomial_coefficient_matrix(list(F))
assert K_matrix.rank() == 6
low = sp.Matrix.hstack(
    *(section.applyfunc(lambda entry: sp.Poly(entry, t).coeff_monomial(t**degree))
      for degree in range(3) for section in (E, O))
)
high = sp.Matrix.hstack(
    O.applyfunc(lambda entry: sp.Poly(entry, t).coeff_monomial(t**4)),
    E.applyfunc(lambda entry: sp.Poly(entry, t).coeff_monomial(t**4)),
    O.applyfunc(lambda entry: sp.Poly(entry, t).coeff_monomial(t**3)),
    E.applyfunc(lambda entry: sp.Poly(entry, t).coeff_monomial(t**3)),
    O.applyfunc(lambda entry: sp.Poly(entry, t).coeff_monomial(t**2)),
    E.applyfunc(lambda entry: sp.Poly(entry, t).coeff_monomial(t**2)),
)
assert low.det() != 0
assert high.det() != 0

C1, D1 = induced_pair(lam, F)
C2, D2 = induced_pair(mu, F)
for row, Cj, Dj in ((lam, C1, D1), (mu, C2, D2)):
    row_at_s = sp.Matrix(
        [[sum(coefficient_vector(row, degree)[coordinate] * s**degree for degree in range(4))
          for coordinate in range(6)]]
    )
    identity = sp.expand((row_at_s * F)[0] - (s - z**2) ** 2 * (Cj * s + Dj))
    assert identity == 0

U1 = polynomial_coefficient_matrix(U(C1, D1))
U2 = polynomial_coefficient_matrix(U(C2, D2))
assert U1.rank() == 4
assert U2.rank() == 4
assert U1.row_join(U2).rank() == 6
assert U1.rank() + U2.rank() - U1.row_join(U2).rank() == 2
assert U1.row_join(U2).row_join(K_matrix).rank() == 6

# The annihilator frame is primitive of splitting (3,3).
annihilator = sp.Matrix.vstack(sp.Matrix([lam]), sp.Matrix([mu]))
annihilator_minors = [
    sp.expand(annihilator[:, list(columns)].det())
    for columns in combinations(range(6), 2)
]
assert sp.gcd_list([minor for minor in annihilator_minors if minor]) == 1
assert sp.Matrix.vstack(coefficient_vector(lam, 3).T, coefficient_vector(mu, 3).T).rank() == 2

# Recover the two cubic eta rows from R_j=t C_j+D_j.
R1 = sp.expand(z**2 * C1 + D1)
R2 = sp.expand(z**2 * C2 + D2)
a, b = parity_rows(R1)
c_eta, d = parity_rows(R2)
assert max(sp.degree(entry, t) for entry in (a, b, c_eta, d)) <= 3
kappa = sp.factor(a * d - b * c_eta)
assert sp.degree(kappa, t) == 6
assert sp.degree(sp.gcd(kappa, sp.diff(kappa, t)), t) == 0

moving = sp.Matrix.hstack(E, O, E.diff(t), O.diff(t))
pluecker = [
    sp.expand(moving[list(rows), :].det())
    for rows in combinations(range(6), 4)
]
pluecker_gcd = sp.factor(sp.gcd_list([minor for minor in pluecker if minor]))
assert monic(pluecker_gcd, t) == monic(kappa, t)

# Intersection plus all degree guards still leaves a generic Wronskian,
# rather than the target cube-square factorization.
wronskian = sp.factor(
    sp.det(sp.Matrix([[sp.diff(F[j], z, order) for j in range(6)] for order in range(6)]))
)
assert sp.degree(wronskian, z) == 24
assert sp.Poly(wronskian, z).coeff_monomial(1) != 0
assert sp.LC(sp.Poly(wronskian, z)) != 0
assert sp.degree(sp.gcd(wronskian, sp.diff(wronskian, z)), z) == 0

print("p=28 cubic-pair intersection frontier: PASS")
print("shift family: intersection 2, primitive splitting (2,2), square scalar")
print("transverse family: intersection 2, primitive splitting (3,3)")
print("transverse residual determinant: squarefree sextic")
print("transverse ordinary Wronskian: squarefree degree 24")
print("scope: intersection/echelon data alone do not force 4^3 3^6")
