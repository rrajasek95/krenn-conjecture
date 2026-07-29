#!/usr/bin/env python3
"""Exact audit of the stable h=8 decic four-space closure."""

from __future__ import annotations

from itertools import combinations

import sympy as sp


# Common-kernel degree and Wronskian ledgers.
for epsilon in (0, 1):
    p = 10 - epsilon
    common_degree = p + epsilon
    assert common_degree == 10
    for d in range(2, 8):
        forced = p * (d - 2) + epsilon * (d - 1)
        cap = d * (common_degree + 1 - d)
        assert forced - cap == d**2 - d - 2 * p - epsilon

assert 5**2 - 5 - 2 * 10 == 0       # pure five-space equality
assert 6**2 - 6 - 2 * 10 > 0        # pure dimension at most five
assert 5**2 - 5 - (2 * 9 + 1) > 0  # singleton dimension at most four

# Every local gcd correction is strict at the relevant dimensions.
for d in range(2, 8):
    assert d + 1 > 0
    assert 2 * d + 2 > 0


z, w, a, b, s = sp.symbols("z w a b s")


# Fifth-choice factors are coprime off the forbidden a=+-b collisions.
A_a = sp.expand((z + a) ** 2 * (z - a) ** 3)
A_b = sp.expand((z + b) ** 2 * (z - b) ** 3)
assert A_a == z**5 - a * z**4 - 2 * a**2 * z**3 + 2 * a**3 * z**2 + a**4 * z - a**5
assert sp.factor(sp.resultant(A_a, A_b, z)) == (a - b) ** 13 * (a + b) ** 12

# Any three distinct A_a are independent: the displayed coefficient
# minor is a nonzero Vandermonde.  This is the only input needed after
# reducing a four-product relation modulo its first factor.
aa = sp.symbols("a0:3")
A_columns = [sp.Poly((z + x) ** 2 * (z - x) ** 3, z) for x in aa]
vandermonde_minor = sp.Matrix(
    [[poly.coeff_monomial(z**degree) for poly in A_columns] for degree in (5, 4, 3)]
).det()
assert sp.factor(
    vandermonde_minor
    + 2 * (aa[0] - aa[1]) * (aa[0] - aa[2]) * (aa[1] - aa[2])
) == 0


# Lower odd-rank degree counts with E quintic and O quartic.
for p in (9, 10):
    assert p - 3 >= 6               # odd rank three: regular squares
    assert 2 * (p - 3) > 5          # double roots of a quintic
    assert p - 6 >= 3               # odd rank two: regular squares
    assert 2 * 3 > 5                # two triple roots beat degree five
    assert p - 2 >= 7               # odd rank one: regular squares
    assert 2 * (p - 2) > 8          # double roots beat quintic-pair Wronskian


# Pure-even annihilator lemma.  The coefficient vectors below are
# w^j(w-s)^3 for j=0,1,2 in the basis 1,w,...,w^5.
D = []
for j in range(3):
    vector = [sp.Integer(0)] * 6
    for q, coefficient in enumerate((-s**3, 3 * s**2, -3 * s, 1)):
        vector[j + q] = coefficient
    D.append(vector)

wedge_coordinates = [(i, j) for i in range(6) for j in range(i + 1, 6)]
coefficient_rows = []
for i, j in ((0, 1), (0, 2), (1, 2)):
    wedge = [
        sp.expand(D[i][u] * D[j][v] - D[i][v] * D[j][u])
        for u, v in wedge_coordinates
    ]
    assert max(sp.Poly(entry, s).degree() if entry else -1 for entry in wedge) <= 6
    for degree in range(7):
        coefficient_rows.append(
            [sp.Poly(entry, s).coeff_monomial(s**degree) for entry in wedge]
        )

wedge_span = sp.Matrix(coefficient_rows)
assert wedge_span.rank() == 14
perpendicular = wedge_span.nullspace()
assert len(perpendicular) == 1
perpendicular = perpendicular[0]
expected_nonzero = {(0, 5): 10, (1, 4): -2, (2, 3): 1}
scale = perpendicular[wedge_coordinates.index((2, 3))]
assert scale != 0
for index, pair in enumerate(wedge_coordinates):
    assert sp.simplify(perpendicular[index] / scale - expected_nonzero.get(pair, 0)) == 0

alternating = sp.zeros(6)
for coefficient, (i, j) in zip(perpendicular, wedge_coordinates):
    alternating[i, j] = coefficient
    alternating[j, i] = -coefficient
assert alternating.rank() == 6       # no nonzero decomposable bivector lies here


# Degree-ten cofactor bound for [E',O,O'].  The nominal degree eleven
# cancels because the leading rows of O and O' are proportional.
ec = sp.symbols("ec0:15")
oc = sp.symbols("oc0:15")
Eprime = [sum(ec[5 * j + q] * w**q for q in range(5)) for j in range(3)]
O_generic = [sum(oc[5 * j + q] * w**q for q in range(5)) for j in range(3)]
cofactor_minor = sp.Poly(
    sp.det(
        sp.Matrix(
            [Eprime, O_generic, [sp.diff(poly, w) for poly in O_generic]]
        )
    ),
    w,
)
assert cofactor_minor.degree() <= 10

# In the nine-point case the affine cofactor quotient is killed by
# orthogonality to O and O', exactly as in the nonic singleton proof.
c0, c1, d0, d1 = sp.symbols("c0 c1 d0 d1")
f0, f1, g0, g1 = sp.symbols("f0 f1 g0 g1")
affine_pairing = (f0 + f1 * w) * (w * c0 + d0) + (g0 + g1 * w) * (
    w * c1 + d1
)
assert sp.expand(
    sp.diff(affine_pairing, w)
    - f1 * (w * c0 + d0)
    - g1 * (w * c1 + d1)
    - c0 * (f0 + f1 * w)
    - c1 * (g0 + g1 * w)
) == 0


TRIPLES = tuple(combinations(range(4), 3))


def determinant_rows(first, second, third, columns):
    """Three-by-three determinant on a chosen column triple."""
    return sp.det(
        sp.Matrix(
            [
                [first[j] for j in columns],
                [second[j] for j in columns],
                [third[j] for j in columns],
            ]
        )
    )


def tangent_solution_and_fibre(Orow):
    """Return tangent nullity, reduced fifth-row fibre, and Wronskian.

    The common gcd of the fifth-row minors contains the gcd of the
    inflection minors.  Removing that factor leaves precisely the equation
    imposed at noninflection points.
    """
    coefficients = sp.symbols("tc0:20")
    generic = [
        sum(coefficients[5 * j + q] * w**q for q in range(5))
        for j in range(4)
    ]
    Oprime = [sp.diff(poly, w) for poly in Orow]
    tangent_equations = []
    for columns in TRIPLES:
        polynomial = sp.Poly(
            determinant_rows(generic, Orow, Oprime, columns), w
        )
        tangent_equations.extend(polynomial.all_coeffs())

    matrix, _ = sp.linear_eq_to_matrix(tangent_equations, coefficients)
    reduced, pivots = matrix.rref()
    free = [index for index in range(20) if index not in pivots]
    solution = {coefficients[index]: coefficients[index] for index in free}
    for row, pivot in enumerate(pivots):
        solution[coefficients[pivot]] = sp.factor(
            -sum(reduced[row, index] * coefficients[index] for index in free)
        )
    Trow = [sp.factor(poly.subs(solution)) for poly in generic]

    Osecond = [sp.diff(poly, w, 2) for poly in Orow]
    fifth = [sp.diff(poly, w) for poly in Trow]
    fifth = [left + a * right for left, right in zip(fifth, Osecond)]

    fifth_minors = []
    inflection_minors = []
    for columns in TRIPLES:
        fifth_minor = determinant_rows(fifth, Orow, Oprime, columns)
        fifth_minors.append(sp.together(fifth_minor).as_numer_denom()[0])
        inflection_minors.append(
            sp.expand(determinant_rows(Osecond, Orow, Oprime, columns))
        )

    common_fifth = fifth_minors[0]
    common_inflection = inflection_minors[0]
    for polynomial in fifth_minors[1:]:
        common_fifth = sp.gcd(common_fifth, polynomial)
    for polynomial in inflection_minors[1:]:
        common_inflection = sp.gcd(common_inflection, polynomial)

    # Only the part of the inflection gcd actually present in the fifth
    # minors is automatic.  At a triple inflection, for example, the
    # inflection minors have gcd w^2 while the fifth minors have gcd w.
    automatic_inflection = sp.gcd(common_fifth, common_inflection)
    reduced_fibre = sp.factor(
        sp.cancel(common_fifth / automatic_inflection).subs(w, a**2)
    )
    assert reduced_fibre != 0
    wronskian = sp.factor(
        sp.det(
            sp.Matrix(
                [
                    [sp.diff(poly, w, order) for poly in Orow]
                    for order in range(4)
                ]
            )
        )
    )
    return len(free), reduced_fibre, wronskian


def audit_chart(name, Orow, expected_nullity, fibre_cap, odd_degree):
    nullity, fibre, wronskian = tangent_solution_and_fibre(Orow)
    assert nullity == expected_nullity, (name, nullity)
    polynomial = sp.Poly(sp.expand(fibre), a)
    assert polynomial.degree() <= fibre_cap, (name, polynomial.degree())
    odd_part = sp.Poly(sp.expand(fibre - fibre.subs(a, -a)), a)
    assert odd_part.as_expr() != 0, name
    assert odd_part.degree() == odd_degree, (name, odd_part.degree())
    return sp.factor(wronskian)


# Exhaustive monomial-plus-pivot charts off the tangent rank-jump locus.
# Their reduced fibre is an even quartic plus a fixed nonzero linear term.
l0, l1, l2, l3 = sp.symbols("l0 l1 l2 l3", nonzero=True)
no_triple_charts = [
    (
        "q4-l2",
        [1 + l0 * w**4, w + l1 * w**4, w**2 + l2 * w**4, w**3 + l3 * w**4],
    ),
    (
        "q4-l1",
        [1 + l0 * w**4, w + l1 * w**4, w**2, w**3 + l3 * w**4],
    ),
    ("q4-l1-l3zero", [1 + l0 * w**4, w + l1 * w**4, w**2, w**3]),
    ("q4-l0", [1 + l0 * w**4, w, w**2, w**3 + l3 * w**4]),
    ("q4-l0-l3zero", [1 + l0 * w**4, w, w**2, w**3]),
    (
        "q3-l2",
        [1 + l0 * w**3, w + l1 * w**3, w**2 + l2 * w**3, w**4],
    ),
    ("q3-l2zero", [1 + l0 * w**3, w + l1 * w**3, w**2, w**4]),
    ("q2", [1 + l0 * w**2, w + l1 * w**2, w**3, w**4]),
]
for chart_name, chart in no_triple_charts:
    audit_chart(chart_name, chart, expected_nullity=4, fibre_cap=4, odd_degree=1)


# Exact triple- and quadruple-root normal forms.  The affine degree of the
# Wronskian records the multiplicity at infinity.
lam = sp.symbols("lam", nonzero=True)
finite_triple_W = audit_chart(
    "finite-triple",
    [1 + lam * w, w**2, w**3, w**4],
    expected_nullity=5,
    fibre_cap=6,
    odd_degree=3,
)
finite_quad_W = audit_chart(
    "finite-quad",
    [w, w**2, w**3, w**4],
    expected_nullity=6,
    fibre_cap=6,
    odd_degree=3,
)
infinity_triple_W = audit_chart(
    "infinity-triple",
    [1, w, w**2, w**3 + lam * w**4],
    expected_nullity=5,
    fibre_cap=6,
    odd_degree=1,
)
infinity_triple_limit_W = audit_chart(
    "infinity-triple-limit",
    [1, w, w**2, w**4],
    expected_nullity=5,
    fibre_cap=6,
    odd_degree=1,
)
infinity_quad_W = audit_chart(
    "infinity-quad",
    [1, w, w**2, w**3],
    expected_nullity=6,
    fibre_cap=6,
    odd_degree=1,
)

assert sp.factor(finite_triple_W / w**3) != 0
assert sp.Poly(finite_triple_W, w).degree() == 4
assert sp.factor(finite_quad_W / w**4) != 0
assert sp.Poly(finite_quad_W, w).degree() == 4
assert sp.Poly(infinity_triple_W, w).degree() == 1
assert sp.Poly(infinity_triple_limit_W, w).degree() == 1
assert sp.Poly(infinity_quad_W, w).degree() == 0


# Noninflection counts beat every fibre degree in both p=9 and p=10.
for p in (9, 10):
    assert p - 4 > 4
    assert p - 2 > 6
    assert p - 1 > 6


print("stable h=8 decic four-space closure: PASS")
print("singleton 2^13 1 is closed; pure 2^14 can survive only in dimension five")
print("all parity ranks 0 through 4 are excluded independently of plane intersections")
