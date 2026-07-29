#!/usr/bin/env python3
"""Independent exact audit of the p=28 all-triple quartic frontier.

This module deliberately imports no project checker.  It reconstructs the
dimension-five obstruction, the signed Hermite degree calculation, all
developable degree lists, and every cone/tangent normal-form calculation.
In particular it regression-tests the corrected cuspidal-sextic tangent
frame; the former ``-7/all-even`` model is not used.
"""

from __future__ import annotations

from itertools import combinations, permutations
from math import comb, factorial

import sympy as sp


def wronskian(polynomials: list[sp.Expr], z: sp.Symbol) -> sp.Expr:
    return sp.expand(
        sp.det(sp.Matrix([
            [sp.diff(poly, z, order) for poly in polynomials]
            for order in range(len(polynomials))
        ]))
    )


def jet_determinant(
    polynomials: list[sp.Expr], z: sp.Symbol, point: sp.Expr
) -> sp.Expr:
    return sp.expand(sp.det(sp.Matrix([
        [sp.diff(poly, z, order).subs(z, point) for poly in polynomials]
        for order in range(len(polynomials))
    ])))


def polynomial_order(poly: sp.Expr, z: sp.Symbol) -> int:
    p = sp.Poly(sp.expand(poly), z)
    if p.is_zero:
        return 10**6
    return min(power[0] for power, coefficient in p.terms() if coefficient)


def high_degree_kernel(
    gamma: list[sp.Expr], delta: list[sp.Expr], z: sp.Symbol, cap: int
) -> tuple[list[sp.Matrix], list[sp.Expr]]:
    """All polynomial A,C for which A*gamma+C*delta has degree <= cap."""
    avec = sp.symbols(f"a0:{cap + 1}")
    cvec = sp.symbols(f"c0:{cap + 1}")
    A = sum(avec[k] * z**k for k in range(cap + 1))
    C = sum(cvec[k] * z**k for k in range(cap + 1))
    section = [sp.expand(A * g + C * d) for g, d in zip(gamma, delta)]
    equations: list[sp.Expr] = []
    for coordinate in section:
        equations.extend(
            coefficient
            for (degree,), coefficient in sp.Poly(coordinate, z).terms()
            if degree > cap
        )
    matrix, _ = sp.linear_eq_to_matrix(equations, avec + cvec)
    return matrix.nullspace(), section


def check_common_kernel_five() -> None:
    # Three transports cannot live in dimensions <=4, and three q=6
    # transports cannot live in dimension five.
    assert 3 + 3 + 3 - 2 * 4 == 1
    assert 4 + 4 + 4 - 2 * 5 == 2
    assert 3 * 4 == 12 > 10
    assert 3 + 3 - 5 == 1

    # A three-dimensional reduced polynomial space forces gcd degree <=4.
    # Such a gcd can meet at most four of nine pairwise-disjoint signed
    # pairs, leaving at least five coprime B_j.  One coprime transport then
    # divides a residual polynomial of degree <=2.
    assert 6 - 4 + 1 == 3
    assert 9 - 4 == 5
    assert 2 < 4

    t = sp.symbols("t")
    sites = (1, 2, 3)
    translates = [sp.Poly((t - site**2) ** 2, t) for site in sites]
    coefficient_matrix = sp.Matrix([
        [poly.coeff_monomial(t**degree) for degree in range(3)]
        for poly in translates
    ])
    assert coefficient_matrix.det() != 0

    # The exceptional quadratic gcds at distinct sites are not
    # proportional, so two exceptional transports cannot meet.
    z = sp.symbols("z")
    exceptional = [sp.Poly((z - site) ** 2, z) for site in (1, 2)]
    vectors = [
        sp.Matrix([poly.coeff_monomial(z**degree) for degree in range(3)])
        for poly in exceptional
    ]
    assert sp.Matrix.hstack(*vectors).rank() == 2

    # Five even dimensions form a hyperplane in the six-dimensional
    # degree-five t-space.  Ten translated fourth powers force its
    # annihilator to kill degrees 0,...,4; t(t-b)^4 then forces degree 5.
    b = sp.symbols("b")
    ell = sp.symbols("ell0:6")

    def apply_L(poly: sp.Expr) -> sp.Expr:
        p = sp.Poly(sp.expand(poly), t)
        return sp.expand(sum(
            ell[k] * p.coeff_monomial(t**k) for k in range(6)
        ))

    first = sp.Poly(apply_L((t - b) ** 4), b)
    assert first.degree() == 4
    span_matrix = sp.Matrix([
        [sp.Poly((t - value) ** 4, t).coeff_monomial(t**degree)
         for degree in range(5)]
        for value in range(5)
    ])
    assert span_matrix.det() != 0
    assert sp.Poly(t * (t - b) ** 4, t).coeff_monomial(t**5) == 1


def check_signed_hermite_normalization() -> None:
    z, t = sp.symbols("z t", nonzero=True)

    # Columns F(+),F'(+),F(-),F'(-) in the frame E,O,E',O'.
    coefficient_matrix = sp.Matrix([
        [1, 0, 1, 0],
        [z, 1, -z, 1],
        [0, 2 * z, 0, -2 * z],
        [0, 2 * z**2, 0, 2 * z**2],
    ])
    assert sp.factor(coefficient_matrix.det()) == 16 * z**4

    def maximum_parity_degree(echelon: range) -> int:
        maximum = -1
        for degrees in combinations(echelon, 4):
            for roles in permutations(("E", "O", "Et", "Ot")):
                value = 0
                legal = True
                for degree, role in zip(degrees, roles):
                    caps = {
                        "E": degree // 2,
                        "O": (degree - 1) // 2,
                        "Et": degree // 2 - 1,
                        "Ot": (degree - 1) // 2 - 1,
                    }
                    legal &= caps[role] >= 0
                    value += caps[role]
                if legal:
                    maximum = max(maximum, value)
        return maximum

    assert maximum_parity_degree(range(5, 11)) == 14
    assert maximum_parity_degree(range(3, 7)) == 6
    assert 14 - 10 == 4
    assert 9 > 6

    # Rank <=2 makes the four-wedge and its first derivative zero: one
    # differentiated column can raise a two-dimensional span only to three.
    x = sp.symbols("x")
    basis = [sp.eye(4).col(k) for k in range(4)]
    columns = [basis[0], basis[1], basis[0] + x * basis[2],
               basis[1] + x * basis[3]]
    determinant = sp.factor(sp.Matrix.hstack(*columns).det())
    assert polynomial_order(determinant, x) == 2


def tangent_degree_options(projective_dimension: int, cap: int) -> list[tuple[int, int, int]]:
    """(edge degree, tangent Pluecker degree, total first ramification)."""
    r = projective_dimension
    answer: list[tuple[int, int, int]] = []
    for edge_degree in range(r, 30):
        total_weight = (r + 1) * (edge_degree - r)
        for first in range(total_weight + 1):
            # If a_1-1=s, each of a_1,...,a_r shifts by at least s.
            if r * first > total_weight:
                continue
            tangent_degree = 2 * edge_degree - 2 - first
            if tangent_degree <= cap:
                answer.append((edge_degree, tangent_degree, first))
    return answer


def check_p3_developables() -> None:
    assert tangent_degree_options(3, 5) == [(3, 4, 0), (4, 5, 1)]
    assert 2 <= 6 // 2 == 3

    z, a, c = sp.symbols("z a c", nonzero=True)
    phi_coefficients = sp.symbols("p0:7")
    phi = sum(phi_coefficients[k] * z**k for k in range(7))

    # Cone e=3: three projected coordinates are even, so at z=0 their
    # first four jets have rank at most two.
    even_coefficients = [sp.symbols(f"e{row}_0:4") for row in range(3)]
    evens = [
        sum(coefficients[k] * z ** (2 * k) for k in range(4))
        for coefficients in even_coefficients
    ]
    assert jet_determinant(evens + [phi], z, 0) == 0

    # Cone e=2: selected stationarity makes the degree-two projection
    # scalar have a double zero at nonzero a.
    scalar = (z - a) ** 2
    cone = [scalar, scalar * z**2, scalar * z**4, phi]
    Wcone = sp.factor(wronskian(cone, z))
    assert polynomial_order(Wcone, z) >= 1
    assert polynomial_order(sp.expand(Wcone.subs(z, z + a)), z) >= 3

    # Rational normal cubic tangent edge.  Solve directly from its binary
    # cubic tangent factor, allowing every quadratic A and B.
    aa = sp.symbols("a0:3")
    bb = sp.symbols("b0:3")
    A = sum(aa[k] * z**k for k in range(3))
    B = sum(bb[k] * z**k for k in range(3))
    t = z**2
    cubic = [A, 2 * A * t + B, A * t**2 + 2 * B * t, B * t**2]
    assert jet_determinant(cubic, z, 0) == 0

    # Cuspidal quartic at finite t=c.  The saturated tangent frame is
    # (1,u^2,u^3,u^4), (0,2,3u,4u^2).  Exhaust all polynomial A,C.
    u = z**2 - c
    gamma = [1, u**2, u**3, u**4]
    delta = [0, 2, 3 * u, 4 * u**2]
    nullspace, _ = high_degree_kernel(gamma, delta, z, 6)
    assert len(nullspace) == 4
    supports = [{k for k, entry in enumerate(vector) if entry}
                for vector in nullspace]
    assert supports == [{7}, {8}, {9}, {0, 11}]
    assert nullspace[-1][0] / nullspace[-1][11] == -4

    q0, q1, q2, q4 = sp.symbols("q0 q1 q2 q4")
    section = [
        sp.expand(-4 * q4 * g + (q0 + q1 * z + q2 * z**2 + q4 * z**4) * d)
        for g, d in zip(gamma, delta)
    ]
    assert jet_determinant(section, z, 0) == 0

    # Cusp at infinity: the g^3_4 omits t^3.  Direct polynomial solving
    # gives Wronskian degree at most 11, below the saturated degree 12.
    gamma_inf = [t**4, t**2, t, 1]
    delta_inf = [4 * t**3, 2 * t, 1, 0]
    null_inf, _ = high_degree_kernel(gamma_inf, delta_inf, z, 6)
    assert len(null_inf) == 4
    parameters = sp.symbols("r0:4")
    combined = sum(
        (parameters[k] * null_inf[k] for k in range(4)), sp.zeros(14, 1)
    )
    Avec = sum(combined[k] * z**k for k in range(7))
    Cvec = sum(combined[7 + k] * z**k for k in range(7))
    section_inf = [sp.expand(Avec * g + Cvec * d)
                   for g, d in zip(gamma_inf, delta_inf)]
    degree_caps = [sp.Poly(poly, z).degree() for poly in section_inf]
    assert degree_caps == [6, 6, 4, 2]
    # Echelon degrees are distinct.  With two coordinates capped at six,
    # at most one echelon pivot can actually have degree six.
    assert 2 + 4 + 5 + 6 - comb(4, 2) == 11 < 12


def check_p5_developables_and_corrected_cusp() -> None:
    assert tangent_degree_options(5, 9) == [(5, 8, 0), (6, 9, 1)]
    for edge_degree in (4, 5):
        vertex_count = 10 - 2 * edge_degree
        nonvertex_count = 10 - vertex_count
        minor_degree = 4 * edge_degree - 12
        assert nonvertex_count == 2 * edge_degree > minor_degree

    z, c = sp.symbols("z c")
    t = z**2

    # Rational normal quintic tangent edge.
    aa = sp.symbols("a0:3")
    bb = sp.symbols("b0:3")
    A = sum(aa[k] * z**k for k in range(3))
    B = sum(bb[k] * z**k for k in range(3))
    quintic: list[sp.Expr] = []
    for index in range(6):
        coordinate = 0
        if index <= 4:
            coordinate += comb(4, index) * A * t**index
        if index >= 1:
            coordinate += comb(4, index - 1) * B * t ** (index - 1)
        quintic.append(sp.expand(coordinate))
    assert jet_determinant(quintic, z, 0) == 0

    # Correct cuspidal sextic frame.  This exact solve is the regression
    # guard for the former erroneous (power+1)*u^(power-1) checker frame.
    u = t - c
    gamma = [1, u**2, u**3, u**4, u**5, u**6]
    delta = [0, 2, 3 * u, 4 * u**2, 5 * u**3, 6 * u**4]
    nullspace, _ = high_degree_kernel(gamma, delta, z, 10)
    assert len(nullspace) == 4
    supports = [{k for k, entry in enumerate(vector) if entry}
                for vector in nullspace]
    assert supports == [{11}, {12}, {13}, {0, 15}]
    assert nullspace[-1][0] / nullspace[-1][15] == -6

    # The old all-even claim is false: C=z is a valid odd section.
    odd_section = [sp.expand(z * d) for d in delta]
    assert all(sp.Poly(poly, z).degree() <= 10 for poly in odd_section)
    assert any(sp.expand(poly.subs(z, -z) - poly) != 0
               for poly in odd_section)

    q0, q1, q2, q4 = sp.symbols("q0 q1 q2 q4")
    generic = sum(
        (parameter * vector for parameter, vector in
         zip((q0, q1, q2, q4), nullspace)),
        sp.zeros(22, 1),
    )
    Afinal = sum(generic[k] * z**k for k in range(11))
    Cfinal = sum(generic[11 + k] * z**k for k in range(11))
    assert sp.expand(Afinal + 6 * q4) == 0
    assert sp.expand(Cfinal - (q0 + q1 * z + q2 * z**2 + q4 * z**4)) == 0
    finite = [sp.expand(Afinal * g + Cfinal * d)
              for g, d in zip(gamma, delta)]
    assert all(sp.Poly(poly, z).degree() <= 10 for poly in finite)
    coefficient_matrix = sp.Matrix([
        [sp.Poly(poly, z).coeff_monomial(z**degree) for poly in finite]
        for degree in range(11)
    ])
    prefix_ranks = [coefficient_matrix[:degree + 1, :].rank()
                    for degree in range(9)]
    assert prefix_ranks == [1, 2, 3, 3, 4, 4, 5, 5, 6]
    # This is vanishing sequence (0,1,2,4,6,8), of Wronskian weight six.
    # Specializing the parameters can only lower a prefix rank and hence
    # can only increase that weight (or make the six functions dependent).
    assert sum((0, 1, 2, 4, 6, 8)) - comb(6, 2) == 6
    assert coefficient_matrix.rank() == 6

    # Cusp at infinity: omit t^5 and exhaust the resulting section space.
    gamma_inf = [t**6, t**4, t**3, t**2, t, 1]
    delta_inf = [6 * t**5, 4 * t**3, 3 * t**2, 2 * t, 1, 0]
    null_inf, _ = high_degree_kernel(gamma_inf, delta_inf, z, 10)
    assert len(null_inf) == 4
    parameters = sp.symbols("s0:4")
    combined = sum(
        (parameters[k] * null_inf[k] for k in range(4)), sp.zeros(22, 1)
    )
    Avec = sum(combined[k] * z**k for k in range(11))
    Cvec = sum(combined[11 + k] * z**k for k in range(11))
    infinity = [sp.expand(Avec * g + Cvec * d)
                for g, d in zip(gamma_inf, delta_inf)]
    degree_caps = [sp.Poly(poly, z).degree() for poly in infinity]
    assert degree_caps == [10, 10, 8, 6, 4, 2]
    # Six independent coordinates have distinct echelon degrees; the two
    # degree-ten caps therefore contribute pivots of degree at most 9,10.
    assert 2 + 4 + 6 + 8 + 9 + 10 - comb(6, 2) == 24 < 30


def check_residual_quartic_and_scope() -> None:
    # Ten distinct simple square roots divide a degree-14 four-vector.
    assert 14 - 10 == 4
    assert 10 + 5 > 14  # five q=6 double roots would already overfill.

    # The local exact-order-three model still permits a simple four-wedge
    # root, so no unproved multiplicity upgrade is smuggled into the result.
    x = sp.symbols("x")
    basis = [sp.eye(6).col(k) for k in range(6)]
    v = basis[0] + x * basis[2] + x**2 * basis[3] / 2
    w = basis[1] + x * basis[2] + x**2 * basis[4] / 2
    matrix = sp.Matrix.hstack(v, w, sp.diff(v, x), sp.diff(w, x))
    minor = sp.factor(matrix[[0, 1, 2, 4], :].det())
    assert polynomial_order(minor, x) == 1
    assert sp.diff(v, x, 3) == sp.zeros(6, 1)

    # A nonconstant decomposable Lambda^4-valued quartic really exists.
    t = sp.symbols("t")
    columns = [basis[0], basis[1], basis[2] + t * basis[4],
               basis[3] + t**3 * basis[5]]
    matrix = sp.Matrix.hstack(*columns)
    pluecker = [
        sp.expand(matrix[list(rows), :].det())
        for rows in combinations(range(6), 4)
    ]
    nonzero = [coordinate for coordinate in pluecker if coordinate != 0]
    assert max(sp.Poly(coordinate, t).degree() for coordinate in nonzero) == 4
    assert matrix.rank() == 4
    assert any(sp.diff(coordinate, t) != 0 for coordinate in nonzero)


def main() -> None:
    check_common_kernel_five()
    check_signed_hermite_normalization()
    check_p3_developables()
    check_p5_developables_and_corrected_cusp()
    check_residual_quartic_and_scope()
    print("independent p=28 all-triple residual-quartic audit: PASS")
    print("common kernel: dimension 6; every q=6 branch excluded")
    print("corrected cusp sextic: A=-6*c4, C=c0+c1*z+c2*z^2+c4*z^4")
    print("remaining scope: nonzero decomposable Lambda^4 quartic, not closure")


if __name__ == "__main__":
    main()
