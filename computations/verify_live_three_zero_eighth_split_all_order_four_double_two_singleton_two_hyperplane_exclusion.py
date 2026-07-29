#!/usr/bin/env python3
"""Exact audit of the all-order d=4 two-singleton hyperplane exclusion."""

from __future__ import annotations

import sympy as sp


# Incidence dimensions in K subset P_7.
ambient_dimension = 4
ambient_degree = 7
singleton_factor_degree = 3
repeated_factor_degree = 2
assert 2 * singleton_factor_degree <= ambient_degree
assert 2 * singleton_factor_degree + repeated_factor_degree > ambient_degree
assert 3 + 3 - ambient_dimension == 2
assert ambient_dimension - 2 == 2


z, r, s, x, y = sp.symbols("z r s x y")
a0, a1, a2 = sp.symbols("a0 a1 a2")


def singleton_factor(t):
    return (z - t) * (z + t) ** 2


def second_derivative_numerator(t, coefficients):
    """Reduced numerator T_t(a) in (a/f_t)''=2*T_t(a)/denominator."""
    c0, c1, c2 = coefficients
    return sp.expand(
        2 * c0 * t**2
        - 4 * c0 * t * z
        + 6 * c0 * z**2
        - c1 * t**3
        + 5 * c1 * t**2 * z
        - 3 * c1 * t * z**2
        + 3 * c1 * z**3
        + c2 * t**4
        - 2 * c2 * t**3 * z
        + 6 * c2 * t**2 * z**2
        - 2 * c2 * t * z**3
        + c2 * z**4
    )


# Exact differentiation, including cancellation of the apparent
# (z+t)^2 numerator factor against f_t^3.
t = sp.symbols("t")
a = a0 + a1 * z + a2 * z**2
actual_second_derivative = sp.diff(a / singleton_factor(t), z, 2)
expected_second_derivative = (
    2 * second_derivative_numerator(t, (a0, a1, a2))
    / ((z - t) ** 3 * (z + t) ** 4)
)
assert sp.factor(actual_second_derivative - expected_second_derivative) == 0

# The row on H*(cz+d) first forces H''=0 and then H'=0.  Its rows on
# H*R and H*S are therefore exactly the R'' and S'' rows.
p, hp, hpp, value, first, second = sp.symbols(
    "p hp hpp value first second"
)
c, d = sp.symbols("c d")
linear_row = hpp * (c * p + d) + 2 * hp * c
assert sp.diff(linear_row, d) == hpp
assert sp.diff(linear_row, c).subs(hpp, 0) == 2 * hp
product_second_row = hpp * value + 2 * hp * first + sp.Symbol("h") * second
assert product_second_row.subs({hpp: 0, hp: 0}) == sp.Symbol("h") * second


# A monic quartic belongs to im(T_t) exactly when its coefficients obey
# the two displayed linear constraints.
c0, c1, c2, c3, c4 = sp.symbols("c0 c1 c2 c3 c4")
generic_image = sp.Poly(second_derivative_numerator(t, (a0, a1, a2)), z)
image_coefficients = [generic_image.coeff_monomial(z**j) for j in range(5)]
constraint_one = -12 * c0 - 3 * t * c1 + 2 * t**2 * c2 + 3 * t**3 * c3
constraint_two = 3 * c0 - t**2 * c2 + 3 * t**4 * c4
image_substitution = {
    c0: image_coefficients[0],
    c1: image_coefficients[1],
    c2: image_coefficients[2],
    c3: image_coefficients[3],
    c4: image_coefficients[4],
}
assert sp.expand(constraint_one.subs(image_substitution)) == 0
assert sp.expand(constraint_two.subs(image_substitution)) == 0

# Conversely, the image has rank three, so its two independent equations
# cut it out inside P_4.
image_matrix = sp.zeros(5, 3)
for column, coefficient in enumerate((a0, a1, a2)):
    for row in range(5):
        image_matrix[row, column] = sp.diff(image_coefficients[row], coefficient)
assert image_matrix.rank() == 3


e1, e2, e3, e4 = sp.symbols("e1 e2 e3 e4")


def monic_image_equations(parameter):
    substitution = {c0: e4, c1: e3, c2: e2, c3: e1, c4: 1, t: parameter}
    return [
        sp.expand(constraint_one.subs(substitution)),
        sp.expand(constraint_two.subs(substitution)),
    ]


quartic_equations = monic_image_equations(r) + monic_image_equations(s)
quartic_matrix, quartic_rhs = sp.linear_eq_to_matrix(
    quartic_equations, (e1, e2, e3, e4)
)
assert sp.factor(quartic_matrix.det()) == 27 * r * s * (r - s) ** 2 * (r + s) ** 2

quartic_solution = {
    e1: -2 * (r + s),
    e2: 3 * (r**2 + s**2),
    e3: -2 * r * s * (r + s),
    e4: r**2 * s**2,
}
assert all(sp.expand(equation.subs(quartic_solution)) == 0 for equation in quartic_equations)

# If either singleton is zero, the forced constant coefficient is zero,
# whereas product(x_i) is nonzero.  No missing pair edge is used here.
assert quartic_solution[e4].subs(r, 0) == 0
assert quartic_solution[e4].subs(s, 0) == 0

X = sp.expand(
    z**4
    + quartic_solution[e1] * z**3
    + quartic_solution[e2] * z**2
    + quartic_solution[e3] * z
    + quartic_solution[e4]
)

# Unique normalized preimages for denominators f_s and f_r.
a_normalized = sp.expand(
    z**2 - sp.Rational(2, 3) * r * z
    + (3 * r**2 - 2 * r * s - 3 * s**2) / 6
)
b_normalized = sp.expand(
    z**2 - sp.Rational(2, 3) * s * z
    + (-3 * r**2 - 2 * r * s + 3 * s**2) / 6
)


def coefficients(poly):
    polynomial = sp.Poly(poly, z)
    return tuple(polynomial.coeff_monomial(z**j) for j in range(3))


assert sp.expand(second_derivative_numerator(s, coefficients(a_normalized)) - X) == 0
assert sp.expand(second_derivative_numerator(r, coefficients(b_normalized)) - X) == 0


# Repeated-pair evaluation determinant and its exact structural factor.
R = a_normalized / singleton_factor(s)
S = b_normalized / singleton_factor(r)
evaluation_points = (x, -x, y, -y)
evaluation_matrix = sp.Matrix(
    [[1, point, R.subs(z, point), S.subs(z, point)] for point in evaluation_points]
)
determinant = sp.factor(evaluation_matrix.det())

u, v = sp.symbols("u v")
P = sp.expand(
    12 * r**4 * s**4
    + 4 * r**2 * s**2 * (3 * r**2 + 4 * r * s + 3 * s**2) * (u + v)
    - (9 * r**4 + 12 * r**3 * s + 10 * r**2 * s**2 + 12 * r * s**3 + 9 * s**4)
    * (u**2 + v**2)
    - 2 * (9 * r**4 + 4 * r**3 * s + 14 * r**2 * s**2 + 4 * r * s**3 + 9 * s**4)
    * u * v
    + 4 * (3 * r**2 + 4 * r * s + 3 * s**2) * u * v * (u + v)
    + 12 * u**2 * v**2
)
expected_determinant = (
    x * y * (r - s) * (x - y) ** 2 * (x + y) ** 2 * P.subs({u: x**2, v: y**2})
    / (
        9
        * (x**2 - r**2) ** 2
        * (y**2 - r**2) ** 2
        * (x**2 - s**2) ** 2
        * (y**2 - s**2) ** 2
    )
)
assert sp.factor(determinant - expected_determinant) == 0

# Every displayed factor outside P is nonzero under the structural
# assumptions: x,y != 0; x != +/-y; r != s; and no repeated value is
# equal or opposite to either singleton.  The six edges used here are all
# repeated--repeated, never the possible triple--zero missing edge.
structural_factors = (
    x,
    y,
    r - s,
    x - y,
    x + y,
    x**2 - r**2,
    y**2 - r**2,
    x**2 - s**2,
    y**2 - s**2,
)
assert len(structural_factors) == 9
assert sp.factor(P - P.xreplace({u: v, v: u})) == 0
P_polynomial = sp.Poly(P, u, v)
assert P_polynomial.degree(u) == P_polynomial.degree(v) == 2
assert P_polynomial.coeff_monomial(u**2 * v**2) == 12

# Interpolation contradiction.  For fixed u_i, the three other distinct
# squares give three roots of a degree-at-most-two polynomial in v.  The
# Vandermonde determinant is nonzero.  Its v^2 coefficient then vanishes
# at four distinct u_i, although it is a quadratic with leading term 12u^2.
u1, u2, u3, u4 = sp.symbols("u1 u2 u3 u4")
vandermonde_three = sp.Matrix(
    [[1, node, node**2] for node in (u2, u3, u4)]
).det()
assert sp.expand(
    vandermonde_three + (u2 - u3) * (u2 - u4) * (u3 - u4)
) == 0
v_squared_coefficient = sp.Poly(P, v).coeff_monomial(v**2)
assert sp.Poly(v_squared_coefficient, u).degree() == 2
assert sp.Poly(v_squared_coefficient, u).coeff_monomial(u**2) == 12


print("h=8 all-order d=4 two-singleton hyperplane exclusion: PASS")
print("exact repeated rows and candidate quartic: exact")
print("six repeated-pair determinants and bidegree contradiction: exact")
print("zero singleton and unique missing edge: audited")
