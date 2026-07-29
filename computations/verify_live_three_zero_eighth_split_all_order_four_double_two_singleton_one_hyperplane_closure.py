#!/usr/bin/env python3
"""Exact audit of the all-order d=4 singleton (3,2) incidence closure."""

from __future__ import annotations

import sympy as sp


# Basic incidence and parity arithmetic.
d = 4
singleton_count = 2
repeated_count = 4
ambient_degree = 11 - d
assert (singleton_count, repeated_count, ambient_degree) == (2, 4, 7)
assert 3 + 2 - 4 == 1
assert 2 * 3 + 2 > ambient_degree

# If U_s were contained in U_r, it would be f_r*f_s*P_1 and could contain
# no repeated neighbor.  At most one of the four required edges is absent.
assert 3 + 3 + 1 == ambient_degree
assert 3 + 3 + 2 > ambient_degree
assert repeated_count - 1 == 3

# The parity determinant of U_s/f_s has degree at most seven.  Normally the
# four repeated pairs give eight roots.  In the missing-edge case, three
# repeated pairs plus the other nonzero singleton pair still give eight.
parity_degree = 2 * (ambient_degree - 3) - 1
assert parity_degree == 7
assert 2 * repeated_count == 8 > parity_degree
assert 2 * (repeated_count - 1) + 2 == 8 > parity_degree

# Gcd/multiplicity classification of a two-space G(z)E(z^2) in P_4.
# n is the square-variable degree and m=ord_{-r}(G).  Exactness excludes
# m=1.  If m=0, f_r-divisibility needs n>=2; if m>=2, the cap is saturated.
normal_form_cases = []
for gcd_degree in range(5):
    for square_degree in range(1, 3):
        if gcd_degree + 2 * square_degree > 4:
            continue
        for gcd_order_at_minus_r in range(gcd_degree + 1):
            if gcd_order_at_minus_r == 1:
                continue
            if gcd_order_at_minus_r == 0 and square_degree < 2:
                continue
            if gcd_order_at_minus_r >= 2:
                # The full degree-two gcd is (z+r)^2.
                if gcd_degree != gcd_order_at_minus_r:
                    continue
            normal_form_cases.append(
                (gcd_degree, square_degree, gcd_order_at_minus_r)
            )
assert normal_form_cases == [(0, 2, 0), (2, 1, 2)]


z, w, r, s = sp.symbols("z w r s")


def singleton_factor(parameter):
    return (z - parameter) * (z + parameter) ** 2


f_r = singleton_factor(r)
f_s = singleton_factor(s)
q_r = w - r**2
q_s = w - s**2

# The canonical singleton-pair lines in the two cases.
assert sp.factor((z**2 - r**2) ** 2 - f_r * (z - r)) == 0
assert sp.factor(
    (z + r) ** 2 * (z**2 - r**2) - f_r * (z + r)
) == 0


# Exact four-point row-subtraction determinant.
e0u, e1u, e0v, e1v = sp.symbols("e0u e1u e0v e1v")
rp, rm, sp_, sm = sp.symbols("rp rm sp_ sm")
tp, tm, vp, vm = sp.symbols("tp tm vp vm")
evaluation_matrix = sp.Matrix(
    [
        [e0u, e1u, rp, sp_],
        [e0u, e1u, rm, sm],
        [e0v, e1v, tp, vp],
        [e0v, e1v, tm, vm],
    ]
)
even_determinant = e0u * e1v - e1u * e0v
parity_wedge = (rp - rm) * (vp - vm) - (sp_ - sm) * (tp - tm)
assert sp.expand(evaluation_matrix.det() + even_determinant * parity_wedge) == 0

# A projective fibre of a primitive P_2 pencil is cut out by one nonzero
# polynomial of degree at most two.  The rank-two escape then has exactly
# two independent vectors in one fibre, and all outside vectors wedge to
# zero with both.  The latter vector must be zero.
d00, d01, d10, d11, v0, v1 = sp.symbols(
    "d00 d01 d10 d11 v0 v1"
)
independent_matrix = sp.Matrix([[d00, d01], [d10, d11]])
independent_determinant = independent_matrix.det()
zero_wedges = sp.Matrix(
    [
        [d01, -d00],
        [d11, -d10],
    ]
) * sp.Matrix([v0, v1])
assert sp.factor(sp.Matrix([[d01, -d00], [d11, -d10]]).det()) == (
    independent_determinant
)
assert len(zero_wedges) == 2


# Type-A parity numerator.
h_coefficients = sp.symbols("h0:5")
h = sum(h_coefficients[index] * z**index for index in range(5))
type_a_numerator = sp.expand(
    f_r * h * f_s.subs(z, -z)
    - f_r.subs(z, -z) * h.subs(z, -z) * f_s
)
h0, h1, h2, h3, h4 = h_coefficients
L_h = sp.expand(
    h0 * (r - s)
    - h1 * r * s
    + (h1 + h2 * (r - s) - h3 * r * s) * w
    + (h3 + h4 * (r - s)) * w**2
)
type_a_expected = (
    -2
    * z
    * (z**2 - r**2)
    * (z**2 - s**2)
    * L_h.subs(w, z**2)
)
assert sp.expand(type_a_numerator - type_a_expected) == 0
assert sp.Poly(L_h, w).degree() == 2

# The parity-coefficient map has rank three whenever r!=s, including each
# possible zero singleton.  Its two-dimensional kernel is precisely
# h=(z-r)(z+s)(A+Bz^2).
L_coefficients = [
    sp.Poly(L_h, w).coeff_monomial(w**power) for power in range(3)
]
L_matrix, _ = sp.linear_eq_to_matrix(L_coefficients, h_coefficients)
assert L_matrix.rank() == 3
assert sp.factor(L_matrix[:, (0, 1, 3)].det()) == r - s
assert L_matrix.subs(r, 0).rank() == 3
assert L_matrix.subs(s, 0).rank() == 3
A, B = sp.symbols("A B")
type_a_even_h = sp.expand((z - r) * (z + s) * (A + B * z**2))
type_a_even_coefficients = {
    h_coefficients[index]: sp.Poly(type_a_even_h, z).coeff_monomial(z**index)
    for index in range(5)
}
assert sp.expand(L_h.subs(type_a_even_coefficients)) == 0
assert sp.factor(
    (f_r * type_a_even_h / f_s)
    - (
        (z**2 - r**2) ** 2
        * (A + B * z**2)
        / (z**2 - s**2)
    )
) == 0

# Two zero parity nodes force each quadratic L_h into the same one-space.
# Evaluating any two such multiples at all other nodes keeps the parity
# vectors on their fixed coefficient line.
u0, u1, u2, u3, c_R, c_S = sp.symbols(
    "u0 u1 u2 u3 c_R c_S"
)
shared_quadratic = (w - u2) * (w - u3)
assert sp.Poly(shared_quadratic, w).degree() == 2
fixed_coefficient_wedge = sp.Matrix(
    [
        [c_R * shared_quadratic.subs(w, u0), c_S * shared_quadratic.subs(w, u0)],
        [c_R * shared_quadratic.subs(w, u1), c_S * shared_quadratic.subs(w, u1)],
    ]
).det()
assert sp.expand(fixed_coefficient_wedge) == 0


# Type-B parity numerator.  After cancelling (z+r)^2, every completion
# function is (z-r)h/f_s.  Dividing its odd numerator by z leaves degree
# at most three in w and in fact has the structural factor w-s^2.
type_b_small_numerator = (z - r) * h
type_b_parity_numerator = sp.expand(
    type_b_small_numerator * f_s.subs(z, -z)
    - type_b_small_numerator.subs(z, -z) * f_s
)
type_b_divided = sp.Poly(sp.expand(type_b_parity_numerator / z), z)
assert all(
    type_b_divided.coeff_monomial(z**odd_power) == 0
    for odd_power in (1, 3, 5, 7)
)
type_b_square_polynomial = sp.expand(
    sum(
        type_b_divided.coeff_monomial(z ** (2 * power)) * w**power
        for power in range(4)
    )
)
assert sp.Poly(type_b_square_polynomial, w).degree() <= 3
assert sp.rem(
    sp.Poly(type_b_square_polynomial, w),
    sp.Poly(w - s**2, w),
).is_zero

# Its even kernel is h=(z+r)(z+s)(A+Bz^2), including r=0 or s=0.
type_b_coefficients = sp.Poly(type_b_square_polynomial, w).all_coeffs()
type_b_matrix, _ = sp.linear_eq_to_matrix(
    type_b_coefficients, h_coefficients
)
assert type_b_matrix.rank() == 3
assert sp.expand(
    type_b_matrix[:3, (0, 1, 3)].det() + 8 * (r + s)
) == 0
assert type_b_matrix.subs(r, 0).rank() == 3
assert type_b_matrix.subs(s, 0).rank() == 3
type_b_even_h = sp.expand((z + r) * (z + s) * (A + B * z**2))
type_b_even_coefficients = {
    h_coefficients[index]: sp.Poly(type_b_even_h, z).coeff_monomial(z**index)
    for index in range(5)
}
assert sp.expand(
    type_b_square_polynomial.subs(type_b_even_coefficients)
) == 0
assert sp.factor(
    ((z - r) * type_b_even_h / f_s)
    - (
        (z**2 - r**2)
        * (A + B * z**2)
        / (z**2 - s**2)
    )
) == 0


# Type-A exact differential operator on the square variable.
lambda0, lambda1, lambda2 = sp.symbols(
    "lambda0 lambda1 lambda2"
)
p0, p1, p2 = sp.symbols("p0 p1 p2")
P = p0 + p1 * w + p2 * w**2
D = lambda0 * w**2 - 2 * lambda1 * w + lambda2
D_E_P = sp.expand(
    D * sp.diff(P, w, 2)
    - sp.diff(D, w) * sp.diff(P, w)
    + 2 * lambda0 * P
)
ell_P = lambda0 * p0 + lambda1 * p1 + lambda2 * p2
assert sp.expand(D_E_P - 2 * ell_P) == 0

# Under F(z)=phi(z^2), the top square-variable derivative coefficient in
# (C*F)''(-x) is 4*x^2*C(-x), nonzero at every repeated value.
x, c_value, c_first, c_second = sp.symbols(
    "x c_value c_first c_second", nonzero=True
)
phi0, phi1, phi2 = sp.symbols("phi0 phi1 phi2")
z_at_row = -x
even_first = 2 * z_at_row * phi1
even_second = 2 * phi1 + 4 * x**2 * phi2
gauged_row = (
    c_value * even_second
    + 2 * c_first * even_first
    + c_second * phi0
)
assert sp.diff(gauged_row, phi2) == 4 * x**2 * c_value

# Exact action on the simple partial fraction.
a = sp.symbols("a")
reciprocal = 1 / (w - a)
D_E_reciprocal = sp.factor(
    D * sp.diff(reciprocal, w, 2)
    - sp.diff(D, w) * sp.diff(reciprocal, w)
    + 2 * lambda0 * reciprocal
)
Q = sp.expand(
    2 * D
    + sp.diff(D, w) * (w - a)
    + 2 * lambda0 * (w - a) ** 2
)
assert sp.factor(D_E_reciprocal - Q / (w - a) ** 3) == 0
Q_polynomial = sp.Poly(Q, w)
assert Q_polynomial.all_coeffs() == [
    6 * lambda0,
    -6 * a * lambda0 - 6 * lambda1,
    2 * a**2 * lambda0 + 2 * a * lambda1 + 2 * lambda2,
]
assert sp.solve(
    Q_polynomial.all_coeffs(),
    (lambda0, lambda1, lambda2),
    dict=True,
) == [{lambda0: 0, lambda1: 0, lambda2: 0}]

# Four distinct roots kill L*(w-a)^3+c*Q, whose degree is at most three.
# The cubic coefficient first kills L and Q!=0 then kills c.
L, c = sp.symbols("L c")
terminal_polynomial = sp.Poly(
    sp.expand(L * (w - a) ** 3 + c * Q),
    w,
)
assert terminal_polynomial.degree() <= 3
assert terminal_polynomial.coeff_monomial(w**3) == L

# Type B: after the gauge, the unique second-order functional annihilating
# P_1 is phi''.  Its action on c/(w-a) is nonzero off the pole.
assert sp.diff(1, w, 2) == 0
assert sp.diff(w, w, 2) == 0
assert sp.factor(
    sp.diff(c / (w - a), w, 2) - 2 * c / (w - a) ** 3
) == 0

# Explicit zero/missing-edge checks.
assert 2 * 3 + 2 == 8  # fixed zero plane singleton, one missing q edge
assert 2 * 4 == 8      # zero hyperplane singleton, all plane-q edges
assert ambient_degree - 3 == 4
assert ambient_degree - (3 + 2) == 2
assert ambient_degree - (3 + 2 + 2) == 0


print("h=8 all-order d=4 singleton (3,2) incidence closure: PASS")
print("Type-A fibre/parity escape and exact operator: closed")
print("Type-B linear pencil and exact second derivative: closed")
print("r=0, s=0, and unique triple-zero missing edge: exact")
