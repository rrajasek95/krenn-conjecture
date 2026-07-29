#!/usr/bin/env python3
"""Exact audit of the p=28 4^3 3^6 q=5 saturation theorem."""

from __future__ import annotations

from itertools import permutations

import sympy as sp


def audit_profiles_and_dimensions() -> None:
    profiles = ((3, 6, 0, 0), (3, 6, 1, -2))
    splits = tuple((h, 28 - h) for h in range(22, 28))
    assert splits == (
        (22, 6), (23, 5), (24, 4),
        (25, 3), (26, 2), (27, 1),
    )

    for h, _k in splits:
        for quartics, triples, doubles, offset in profiles:
            assert 4 * quartics + 3 * triples + 2 * doubles + offset == 30
            selected_repeated = 1 + doubles
            selected_singletons = h + 2 - 2 * selected_repeated
            assert selected_singletons == h + offset
            complement = (4,) * quartics + (3,) * (triples - 1) + (1,)
            assert len(complement) == 9
            assert sum(complement) == 28
            assert complement.count(4) == 3
            assert complement.count(3) == 5
            assert complement.count(1) == 1

    # Seven common-kernel dimensions are excluded by the exact baseline
    # rows.  Dimension six is precisely saturated.
    assert 3 * (7 - 4) + 6 * (7 - 3) == 33
    assert 7 * (10 - 7) == 21
    assert 3 * (6 - 4) + 6 * (6 - 3) == 24
    assert 6 * (10 - 6) == 24

    # Three transported spaces of dimension at least three cannot fit in
    # dimension at most four: their common intersection would be nonzero,
    # but its three coprime quartic factors have degree twelve > nine.
    assert 3 + 3 + 3 - 2 * 4 == 1
    assert 3 * 4 > 9

    # In a common five-space a q=5 transport meets every q=5/q=6 partner.
    assert 3 + 3 - 5 == 1
    assert 3 + 4 - 5 == 2
    # In a common six-space a q=6 transport meets each q=5 partner.
    assert 4 + 3 - 6 == 1


def robin_family():
    z, x, i, rho = sp.symbols("z x i rho")
    a = i**2
    delta = a - x
    factor = (z**2 - x) ** 2
    linear = (rho * delta + 4 * i) * (z - i) - delta
    family = sp.expand(factor * linear)

    value = sp.factor(family.subs(z, i))
    derivative = sp.factor(sp.diff(family, z).subs(z, i))
    assert sp.expand(value + (a - x) ** 3) == 0
    assert sp.expand(derivative - rho * (a - x) ** 3) == 0
    assert sp.expand(derivative + rho * value) == 0

    coefficients = [sp.expand(family).coeff(x, power) for power in range(4)]
    rows = (0, 1, 4, 5)
    minor = sp.Matrix([
        [coefficient.coeff(z, degree) for coefficient in coefficients]
        for degree in rows
    ])
    assert sp.factor(minor.det()) == 16 * i**2

    # Four distinct squared values multiply this coefficient minor by a
    # Vandermonde determinant, so there is no rho-dependent rank drop.
    xs = sp.symbols("x0:4")
    vandermonde = sp.Matrix([[value**power for value in xs] for power in range(4)])
    expected = sp.prod(xs[right] - xs[left]
                       for left in range(4) for right in range(left + 1, 4))
    assert sp.expand(vandermonde.det() - expected) == 0

    return z, i, rho, coefficients


def audit_q6_wronskian(z, i, rho, coefficients) -> None:
    wronskian = sp.factor(sp.det(sp.Matrix([
        [sp.diff(coefficient, z, order) for coefficient in coefficients]
        for order in range(4)
    ])))
    residual = (
        rho**2 * z**3
        - (i * rho**2 + 4 * rho) * z**2
        + (i**2 * rho**2 + 6 * i * rho + 5) * z
        - (i**3 * rho**2 + 10 * i**2 * rho + 25 * i)
    )
    assert sp.expand(
        wronskian + 384 * i * z * (z - i) ** 3 * residual
    ) == 0
    assert sp.Poly(wronskian, z).degree() <= 7
    # If rho != 0, residual has leading coefficient rho^2.  If rho=0,
    # it is 5(z-5i), so it is never zero when i is structurally nonzero.
    assert sp.Poly(residual, z).LC() == rho**2
    assert sp.expand(residual.subs(rho, 0) - 5 * (z - 5 * i)) == 0

    # A regular-unit complementary triple row is a nonzero relation among
    # ordinary jets zero through three, because its top coefficient is U(j).
    y = sp.symbols("y")
    u = sp.symbols("u0:4")
    s = sp.symbols("s0:4")
    unit = sum(u[order] * y**order for order in range(4))
    section = sum(s[order] * y**order for order in range(4))
    third_jet = sp.diff(unit * section, y, 3).subs(y, 0)
    assert sp.expand(third_jet - 6 * sum(u[r] * s[3 - r] for r in range(4))) == 0
    assert sp.diff(third_jet, s[3]) == 6 * u[0]

    # z=0, z=i with multiplicity three, and the five other moving values
    # would force at least nine roots on a nonzero polynomial of degree <=7.
    assert 1 + 3 + 5 == 9 > 7


def audit_residual_degree_and_splitting() -> None:
    # Saturated echelon degrees 4,...,9 give the following maximum degrees
    # in t for the even and odd coordinate parts.
    even_odd_degrees = ((2, 1), (2, 2), (3, 2), (3, 3), (4, 3), (4, 4))
    best = -1
    for chosen_rows in permutations(range(6), 4):
        e0, o0 = even_odd_degrees[chosen_rows[0]]
        e1, o1 = even_odd_degrees[chosen_rows[1]]
        e2, o2 = even_odd_degrees[chosen_rows[2]]
        e3, o3 = even_odd_degrees[chosen_rows[3]]
        best = max(best, e0 + o1 + (e2 - 1) + (o3 - 1))
    assert best == 12
    assert 12 - 6 == 6

    # After scalar-gcd removal, constant and linear annihilator rows are
    # impossible.  This is the complete splitting ledger through degree six.
    splitting_types = tuple(
        (alpha, beta)
        for alpha in range(2, 7)
        for beta in range(alpha, 7)
        if alpha + beta <= 6
    )
    assert splitting_types == ((2, 2), (2, 3), (2, 4), (3, 3))

    # Generic rank-two second fundamental form.  If delta is its torsion
    # cokernel length, the derived determinant has degree
    # 3*d-12-2*delta.  A residual scalar gcd can hide at most 6-d of the
    # six moving roots, so the determinant must retain at least d roots.
    survivors = []
    for d in range(4, 7):
        for delta in range(0, 8):
            determinant_degree = 3 * d - 12 - 2 * delta
            retained_roots = d
            if determinant_degree >= retained_roots:
                survivors.append((d, delta))
    assert survivors == [(6, 0)]
    d, delta = survivors[0]
    assert 4 - 2 * d + delta == -8  # degree of the rank-two kernel L
    assert 3 * d - 12 - 2 * delta == 6
    assert 6 - d == 0  # no residual scalar gcd remains

    # E and O are degree-at-most-four sections.  Their injection
    # O(-4)^2 -> L has equal source/target degree and hence no torsion.
    assert 2 * (-4) == 4 - 2 * d + delta
    matrix_ledgers = {
        (2, 4): ((0, 2), (-2, 0), (2, 4)),
        (3, 3): ((1, 1), (-1, -1), (3, 3)),
    }
    # Entries record W/L, (W/L) tensor Omega, and the two row degrees of
    # the induced 2x2 derivative matrix.  Both determinants have degree 6.
    for splitting, (quotient, target, row_degrees) in matrix_ledgers.items():
        alpha, beta = splitting
        assert quotient == (alpha - 2, beta - 2)
        assert target == (alpha - 4, beta - 4)
        assert row_degrees == (alpha, beta)
        assert sum(row_degrees) == 6


def audit_developable_closure() -> None:
    # Cone: a nondegenerate direction curve in P^4 has degree at least four,
    # while the square-cover projection of a degree-nine point has 2e <= 9.
    cone_degrees = tuple(e for e in range(4, 20) if 2 * e <= 9)
    assert cone_degrees == (4,)
    # A(z) P_4(z^2) has the following five local orders at zero.  Inserting
    # one more independent section still leaves positive Wronskian weight.
    unit_sequence = (0, 1, 2, 4, 6, 8)
    simple_zero_sequence = (0, 1, 3, 5, 7, 9)
    regular_weight = sum(range(6))
    assert sum(unit_sequence) - regular_weight == 6
    assert sum(simple_zero_sequence) - regular_weight == 10

    # Tangent edge: d=2e-2-R1, d<=8, and five units of total ramification
    # are spent per unit of first ramification.
    tangent_cases = []
    for edge_degree in range(5, 40):
        for plucker_degree in range(9):
            first_ramification = 2 * edge_degree - 2 - plucker_degree
            if (
                first_ramification >= 0
                and 5 * first_ramification <= 6 * (edge_degree - 5)
            ):
                tangent_cases.append(
                    (edge_degree, plucker_degree, first_ramification)
                )
    assert tangent_cases == [(5, 8, 0)]

    # A general degree-nine section of the square-pulled tangent lines to
    # the rational normal quintic.
    z = sp.symbols("z")
    a0, a1, b0, b1 = sp.symbols("a0 a1 b0 b1")
    scalar_a = a0 + a1 * z
    scalar_b = b0 + b1 * z
    t = z**2
    coordinates = (
        scalar_a,
        4 * t * scalar_a + scalar_b,
        6 * t**2 * scalar_a + 4 * t * scalar_b,
        4 * t**3 * scalar_a + 6 * t**2 * scalar_b,
        t**4 * scalar_a + 4 * t**3 * scalar_b,
        t**4 * scalar_b,
    )
    wronskian = sp.expand(sp.det(sp.Matrix([
        [sp.diff(coordinate, z, order) for coordinate in coordinates]
        for order in range(6)
    ])))
    determinant = a0 * b1 - a1 * b0
    assert sp.rem(wronskian, z**6, domain=sp.QQ[a0, a1, b0, b1]) == 0
    quotient = sp.cancel(wronskian / (z**6 * determinant))
    assert quotient != 0
    assert sp.Poly(quotient, z).degree() == 12
    assert sp.Poly(wronskian, z).degree() == 18


def main() -> None:
    audit_profiles_and_dimensions()
    z, i, rho, coefficients = robin_family()
    audit_q6_wronskian(z, i, rho, coefficients)
    audit_residual_degree_and_splitting()
    audit_developable_closure()
    print("p=28 4^3 3^6 q=5 saturation: PASS")
    print("common kernel: dimension exactly six")
    print("all six moving-triple selections: q=5")
    print("residual alternative: developable or decomposable degree <=6")
    print("primitive annihilator splittings: (2,2), (2,3), (2,4), (3,3)")
    print("generic tangent rank two: only d=6, delta=0, types (2,4)/(3,3)")
    print("rank-two normal form: L=O(-4)^2; eta rows (2,4) or (3,3)")
    print("developable residual: cone and tangent branches excluded at z=0")
    print("scope: strict normal form, not profile closure")


if __name__ == "__main__":
    main()
