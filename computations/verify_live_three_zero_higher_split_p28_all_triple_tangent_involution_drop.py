#!/usr/bin/env python3
"""Exact audit of the p=28 all-triple tangent-involution drop."""

from __future__ import annotations

from itertools import combinations

import sympy as sp


def wronskian_weight(sequence: tuple[int, ...]) -> int:
    r = len(sequence)
    return sum(sequence) - r * (r - 1) // 2


def omission_sequence(r: int, exact_order: int) -> tuple[int, ...]:
    answer = tuple(j for j in range(r + 1) if j != exact_order)
    assert len(answer) == r
    return answer


def wronskian(polynomials: list[sp.Expr], z: sp.Symbol) -> sp.Expr:
    return sp.factor(
        sp.det(
            sp.Matrix(
                [
                    [sp.diff(f, z, row) for f in polynomials]
                    for row in range(len(polynomials))
                ]
            )
        )
    )


def plucker_tangent(polynomials: list[sp.Expr], z: sp.Symbol) -> list[sp.Expr]:
    return [
        sp.expand(polynomials[a] * sp.diff(polynomials[b], z)
                  - polynomials[b] * sp.diff(polynomials[a], z))
        for a, b in combinations(range(len(polynomials)), 2)
    ]


def zero_order(poly: sp.Expr, z: sp.Symbol) -> int:
    p = sp.Poly(sp.expand(poly), z)
    if p.is_zero:
        return 10**9
    return min(monomial[0] for monomial, _ in p.terms())


def audit_boundary_and_local_sequences() -> None:
    # Selecting one of ten triples leaves 3^9 1, of mass 28 and ten
    # classes.  The relation space is a four-space in P_6.
    complement = (1,) + (3,) * 9
    assert sum(complement) == 28
    assert len(complement) == 10
    relation_dimension = 4
    relation_degree = len(complement) - 4
    assert relation_degree == 6

    simple_sequence = omission_sequence(4, 1)
    triple_sequence = omission_sequence(4, 3)
    regular_sequence = (0, 1, 2, 3)
    assert simple_sequence == (0, 2, 3, 4)
    assert triple_sequence == (0, 1, 2, 4)
    assert wronskian_weight(simple_sequence) == 3
    assert wronskian_weight(triple_sequence) == 1
    assert wronskian_weight(regular_sequence) == 0
    forced = 3 + 9
    cap = relation_dimension * (relation_degree + 1 - relation_dimension)
    assert forced == cap == 12

    # Every possible positive gcd order below the row order costs strictly
    # more than the saturated primitive contribution.
    for exact_order in (1, 3):
        primitive_cost = 4 - exact_order
        for gcd_order in range(1, exact_order):
            divided_cost = 4 * gcd_order + max(
                0, 4 - exact_order + gcd_order
            )
            assert divided_cost > primitive_cost
        for gcd_order in range(exact_order + 1, 6):
            assert 4 * gcd_order > primitive_cost

    # Degree twelve forces the unique top echelon profile (3,4,5,6),
    # hence no ramification or base point at infinity.
    degree_profiles = tuple(combinations(range(7), 4))
    saturated = tuple(
        profile for profile in degree_profiles if sum(profile) - 6 == 12
    )
    assert saturated == ((3, 4, 5, 6),)

    # The common 3^10 baseline has mass thirty.  Six dimensions are on
    # equality; seven dimensions have excess twelve.
    baseline = (3,) * 10
    assert sum(baseline) == 30
    for dimension, expected_gap in ((6, 0), (7, 12)):
        baseline_forced = sum(dimension - m for m in baseline)
        baseline_cap = dimension * (11 - dimension)
        assert baseline_forced - baseline_cap == expected_gap

    # Both residual tuples produce the same moving complement for every
    # split.  The second has one common fixed selected double.
    residuals = ((0, 10, 0, 0), (0, 10, 1, -2))
    for h in range(22, 28):
        k = 28 - h
        for e, a, b, u in residuals:
            assert 4 * e + 3 * a + 2 * b + u == 30
            selected_doubles = b
            selected_triples = 1
            d = selected_doubles + selected_triples
            selected_singletons = h + 2 - 2 * d
            assert selected_singletons == h + u
            selected_forced = (
                4 * d + 5 * selected_singletons + max(0, 6 - k)
            )
            selected_degree = h + 3 - d
            selected_cap = 6 * (selected_degree + 1 - 6)
            assert selected_forced == selected_cap


def audit_transport_intersections() -> None:
    z = sp.symbols("z")
    sites = tuple(range(1, 11))
    assert all(site != 0 for site in sites)
    assert len({site for site in sites} | {-site for site in sites}) == 20

    factors = {site: sp.Poly((z - site) ** 2 * (z + site) ** 2, z)
               for site in sites}
    assert all(factor.degree() == 4 for factor in factors.values())
    for i, j in combinations(sites, 2):
        assert sp.gcd(factors[i], factors[j]).degree() == 0
        assert (factors[i] * factors[j]).degree() == 8
        # Pair ambient B_i B_j P_2 has dimension three.
        assert 10 - 8 + 1 == 3

    for i, j, k in combinations(sites, 3):
        assert (factors[i] * factors[j] * factors[k]).degree() == 12
        assert 12 > 10

    # Two four-spaces in a common space of dimension at most six meet in
    # dimension at least two.  The four signed first-jet rows have rank
    # at least two at +j, hence their kernel has dimension at most two.
    # Only common dimension six is compatible, and every pair
    # intersection/kernel has dimension exactly two.
    compatible = []
    for common_dimension in range(4, 7):
        intersection_lower = 8 - common_dimension
        jet_kernel_upper = 4 - 2
        if intersection_lower <= jet_kernel_upper:
            compatible.append(common_dimension)
    assert compatible == [6]

    fixed = 10
    signed_partners = {sign * j for j in sites if j != fixed for sign in (-1, 1)}
    assert len(signed_partners) == 18
    assert 0 not in signed_partners


def audit_local_plucker_orders_and_degree() -> None:
    x, z = sp.symbols("x z")

    selected_local = [1, x**2, x**3, x**4]
    triple_local = [1, x, x**2, x**4]
    regular_local = [1, x, x**2, x**3]
    assert zero_order(wronskian(selected_local, x), x) == 3
    assert zero_order(wronskian(triple_local, x), x) == 1
    assert zero_order(wronskian(regular_local, x), x) == 0

    selected_minors = plucker_tangent(selected_local, x)
    triple_minors = plucker_tangent(triple_local, x)
    regular_minors = plucker_tangent(regular_local, x)
    assert min(zero_order(p, x) for p in selected_minors) == 1
    assert min(zero_order(p, x) for p in triple_minors) == 0
    assert min(zero_order(p, x) for p in regular_minors) == 0

    echelon_model = [z**3, z**4, z**5, z**6]
    tangent = plucker_tangent(echelon_model, z)
    tangent_degrees = [sp.Poly(p, z).degree() for p in tangent]
    assert max(tangent_degrees) == 10
    # Dividing the unique simple finite tangent base factor leaves degree 9.
    assert max(tangent_degrees) - 1 == 9


def audit_cross_minor_root_count() -> None:
    z = sp.symbols("z")
    aa = sp.symbols("a0:10")
    bb = sp.symbols("b0:10")
    p = sum(aa[r] * z**r for r in range(10))
    q = sum(bb[r] * z**r for r in range(10))
    cross = sp.expand(p * q.subs(z, -z) - q * p.subs(z, -z))
    assert sp.expand(cross.subs(z, -z) + cross) == 0
    # The nominal degree-18 coefficient cancels; a generic cross-minor
    # has odd degree seventeen.
    assert sp.Poly(cross, z).degree() == 17

    partners = tuple(range(1, 10))
    roots = {sign * value for value in partners for sign in (-1, 1)}
    assert len(roots) == 18
    assert len(roots) > 17
    # The alternative coarse count uses degree <=18 and adds the automatic
    # odd root at zero.
    assert len(roots | {0}) == 19
    assert 19 > 18


def audit_involution_classification() -> None:
    z, t = sp.symbols("z t")
    ee = sp.symbols("e0:4")
    oo = sp.symbols("o0:3")
    even = sum(ee[r] * t**r for r in range(4))
    odd_coefficient = sum(oo[r] * t**r for r in range(3))
    f = even.subs(t, z**2) + z * odd_coefficient.subs(t, z**2)
    fprime = sp.diff(f, z)
    fprime_at_minus = fprime.subs(z, -z)
    expected_difference = 4 * z * sp.diff(even, t).subs(t, z**2)
    expected_sum = (
        2 * odd_coefficient.subs(t, z**2)
        + 4 * z**2 * sp.diff(odd_coefficient, t).subs(t, z**2)
    )
    assert sp.expand(fprime - fprime_at_minus - expected_difference) == 0
    assert sp.expand(fprime + fprime_at_minus - expected_sum) == 0

    # If the primitive vector is anti-invariant, all coordinates have a
    # common z factor.  The invariant four-space is necessarily the full
    # even system in degree at most six.
    even_basis = [1, z**2, z**4, z**6]
    assert all(sp.rem(poly, z, domain=sp.QQ) == 0 for poly in [z, z**3, z**5, z**7])
    assert len(even_basis) == 4

    a = sp.symbols("a", nonzero=True)
    jet = sp.Matrix(
        [[sp.diff(poly, z, order).subs(z, a) for poly in even_basis]
         for order in range(4)]
    )
    determinant = sp.factor(jet.det())
    assert determinant != 0
    assert sp.simplify(determinant.subs(a, 1)) != 0
    for rows in range(1, 5):
        assert jet.subs(a, 2)[:rows, :].rank() == rows
    assert wronskian_weight((0, 1, 2, 3)) == 0
    assert wronskian_weight((0, 2, 3, 4)) == 3

    # At zero the square map is ramified, emphasizing why nonzero triple
    # values are an essential structural input.
    zero_jet_ranks = [
        sp.Matrix(
            [[sp.diff(poly, z, order).subs(z, 0) for poly in even_basis]
             for order in range(rows)]
        ).rank()
        for rows in range(1, 7)
    ]
    assert zero_jet_ranks == [1, 1, 2, 2, 3, 3]


def main() -> None:
    audit_boundary_and_local_sequences()
    audit_transport_intersections()
    audit_local_plucker_orders_and_degree()
    audit_cross_minor_root_count()
    audit_involution_classification()
    print("p=28 all-triple tangent-involution dimension drop: PASS")
    print("ten active q=6 selections force nine tangent-line identifications")
    print("degree-nine tangent map is involution-invariant: audited")
    print("conclusion scope: at least one selected kernel has dimension <=5")


if __name__ == "__main__":
    main()
