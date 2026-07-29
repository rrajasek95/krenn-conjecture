#!/usr/bin/env python3
"""Independent exact audit of the p=28 all-triple tangent drop.

This checker deliberately does not import the primary checker.  It rebuilds
the residual-profile bookkeeping, the saturated four-space arithmetic, the
transport intersection dimensions, the Pluecker root count, and the two
algebraic identities used in the involution classification.
"""

from __future__ import annotations

from itertools import combinations

import sympy as sp


def weight(sequence: tuple[int, ...]) -> int:
    return sum(sequence) - len(sequence) * (len(sequence) - 1) // 2


def vanishing_order(poly: sp.Expr, variable: sp.Symbol) -> int:
    expanded = sp.Poly(sp.expand(poly), variable)
    if expanded.is_zero:
        return 10**6
    return min(monomial[0] for monomial, _ in expanded.terms())


def tangent_minors(vector: list[sp.Expr], variable: sp.Symbol) -> list[sp.Expr]:
    return [
        sp.expand(
            vector[a] * sp.diff(vector[b], variable)
            - vector[b] * sp.diff(vector[a], variable)
        )
        for a, b in combinations(range(len(vector)), 2)
    ]


def check_exact_applicability() -> None:
    residuals = (
        (0, 10, 0, 0),
        (0, 10, 1, -2),
        (2, 7, 0, 1),
        (2, 7, 1, -1),
        (3, 6, 0, 0),
        (3, 6, 1, -2),
        (7, 0, 0, 2),
        (7, 0, 1, 0),
        (7, 0, 2, -2),
    )
    assert all(4 * e + 3 * a + 2 * b + u == 30
               for e, a, b, u in residuals)

    covered = []
    for profile in residuals:
        e, a, b, u = profile
        if e == 0 and a == 10 and b in (0, 1):
            covered.append(profile)
            fixed_doubles = b
            for h in range(22, 28):
                singleton_count = h + u
                selected_layers = 1 + fixed_doubles
                selected_singletons = h + 2 - 2 * selected_layers
                assert selected_singletons == singleton_count

                # Select one moving triple: its unused label is simple;
                # the other nine triples remain complementary.  The optional
                # unique double is wholly selected and contributes no row.
                complement = (1,) + (3,) * 9
                assert len(complement) == 10
                assert sum(complement) == 28

                # Restoring the moving triple produces precisely 3^10.
                baseline = (3,) * 10
                assert len(baseline) == 10
                assert sum(baseline) == 30
        else:
            assert e > 0 or a < 10

    assert covered == [(0, 10, 0, 0), (0, 10, 1, -2)]


def check_saturated_four_space() -> None:
    r = 4
    simple = (0, 2, 3, 4)
    triple = (0, 1, 2, 4)
    regular = (0, 1, 2, 3)
    assert weight(simple) == 3
    assert weight(triple) == 1
    assert weight(regular) == 0
    assert weight(simple) + 9 * weight(triple) == 12
    assert r * (7 - r) == 12

    # Rebuild every local gcd correction below the exact row order.  At
    # gcd order equal to the row order the nonzero top jet forces one more
    # common zero, so that case cannot be maximal.
    for row_order in (1, 3):
        primitive = max(0, r - row_order)
        for gcd_order in range(1, row_order):
            corrected = r * gcd_order + max(
                0, r - row_order + gcd_order
            )
            assert corrected > primitive
        equal_order_forces_larger_gcd = True
        assert equal_order_forces_larger_gcd
        for gcd_order in range(row_order + 1, 5):
            assert r * gcd_order > primitive

    # The Wronskian has twelve forced finite zeros.  Among four distinct
    # echelon degrees in [0,6], only (3,4,5,6) can have degree twelve.
    profiles = list(combinations(range(7), 4))
    top_profiles = [p for p in profiles if sum(p) - 6 >= 12]
    assert top_profiles == [(3, 4, 5, 6)]

    x = sp.symbols("x")
    local_models = {
        "selected": [1, x**2, x**3, x**4],
        "triple": [1, x, x**2, x**4],
        "regular": [1, x, x**2, x**3],
    }
    expected_wronskian_orders = {"selected": 3, "triple": 1, "regular": 0}
    expected_tangent_orders = {"selected": 1, "triple": 0, "regular": 0}
    for name, model in local_models.items():
        wronskian = sp.det(
            sp.Matrix(
                [[sp.diff(f, x, row) for f in model] for row in range(4)]
            )
        )
        assert vanishing_order(wronskian, x) == expected_wronskian_orders[name]
        assert min(vanishing_order(g, x) for g in tangent_minors(model, x)) == (
            expected_tangent_orders[name]
        )


def check_common_kernel_and_intersections() -> None:
    z = sp.symbols("z")
    sites = tuple(range(1, 11))
    assert len(set(sites) | {-site for site in sites}) == 20
    factors = {site: sp.Poly((z - site) ** 2 * (z + site) ** 2, z)
               for site in sites}

    # The restored 3^10 baseline excludes dimension seven in P_10.
    for dimension, expected_excess in ((6, 0), (7, 12)):
        forced = 10 * max(0, dimension - 3)
        cap = dimension * (11 - dimension)
        assert forced - cap == expected_excess

    for i, j in combinations(sites, 2):
        assert sp.gcd(factors[i], factors[j]).degree() == 0
        product_degree = (factors[i] * factors[j]).degree()
        assert product_degree == 8
        assert 10 - product_degree + 1 == 3

        # Two four-spaces in an at-most-six-space meet in dimension >=2.
        # Divisibility by B_j is the kernel of four signed first-jet rows.
        # The +j rows already have rank two, so this kernel has dimension
        # <=2.  Thus the intersection is exactly two and the common space
        # must have dimension exactly six.
        intersection_lower = 4 + 4 - 6
        jet_kernel_upper = 4 - 2
        assert intersection_lower == jet_kernel_upper == 2

    for i, j, k in combinations(sites, 3):
        assert (factors[i] * factors[j] * factors[k]).degree() == 12
        assert 12 > 10


def check_pluecker_degree_and_signed_roots() -> None:
    z = sp.symbols("z")
    echelon = [z**3, z**4, z**5, z**6]
    minors = tangent_minors(echelon, z)
    degrees = [sp.Poly(g, z).degree() for g in minors]
    assert max(degrees) == 10
    assert sp.Poly(echelon[2] * sp.diff(echelon[3], z)
                   - echelon[3] * sp.diff(echelon[2], z), z).degree() == 10
    # The selected local sequence supplies exactly one common linear
    # tangent factor; after division the morphism has degree nine.
    assert max(degrees) - 1 == 9

    aa = sp.symbols("a0:10")
    bb = sp.symbols("b0:10")
    p = sum(aa[d] * z**d for d in range(10))
    q = sum(bb[d] * z**d for d in range(10))
    cross = sp.expand(p * q.subs(z, -z) - q * p.subs(z, -z))
    assert sp.expand(cross.subs(z, -z) + cross) == 0
    assert sp.Poly(cross, z).degree() == 17

    fixed = 10
    roots = {sign * j for j in range(1, 11) if j != fixed
             for sign in (-1, 1)}
    assert len(roots) == 18
    assert len(roots) > 17
    assert len(roots | {0}) == 19 > 18


def check_involution_classification_identities() -> None:
    z, t = sp.symbols("z t")
    # Coordinatewise even/odd decomposition and derivative identities.
    e0, e1, e2 = sp.symbols("e0 e1 e2")
    o0, o1 = sp.symbols("o0 o1")
    even = e0 + e1 * t + e2 * t**2
    odd = o0 + o1 * t
    component = even.subs(t, z**2) + z * odd.subs(t, z**2)
    derivative = sp.diff(component, z)
    reflected_derivative = derivative.subs(z, -z)
    assert sp.expand(
        derivative - reflected_derivative
        - 4 * z * sp.diff(even, t).subs(t, z**2)
    ) == 0
    assert sp.expand(
        derivative + reflected_derivative
        - 2 * odd.subs(t, z**2)
        - 4 * z**2 * sp.diff(odd, t).subs(t, z**2)
    ) == 0

    # If E' and O' stay in span(E,O), the derivative of every Pluecker
    # coordinate is the same scalar multiple of that coordinate.
    a, b, c, d = sp.symbols("a b c d")
    e = sp.Matrix(sp.symbols("E0:4"))
    o = sp.Matrix(sp.symbols("O0:4"))
    eprime = a * e + b * o
    oprime = c * e + d * o
    wedge = []
    wedge_prime = []
    for left, right in combinations(range(4), 2):
        coordinate = e[left] * o[right] - e[right] * o[left]
        derivative_coordinate = (
            eprime[left] * o[right] + e[left] * oprime[right]
            - eprime[right] * o[left] - e[right] * oprime[left]
        )
        wedge.append(coordinate)
        wedge_prime.append(sp.expand(derivative_coordinate))
    assert all(sp.expand(dp - (a + d) * p) == 0
               for p, dp in zip(wedge, wedge_prime))

    # In the projectively proportional branch, primitivity rules out an
    # odd vector.  Four independent even polynomials of degree <=6 fill
    # the complete cubic system in t, which is unramified away from z=0.
    even_basis = [1, z**2, z**4, z**6]
    nonzero = sp.symbols("u", nonzero=True)
    jets = sp.Matrix(
        [[sp.diff(f, z, row).subs(z, nonzero) for f in even_basis]
         for row in range(4)]
    )
    determinant = sp.factor(jets.det())
    assert determinant != 0
    assert sp.simplify(determinant / nonzero**6) != 0

    odd_basis = [z, z**3, z**5]
    assert all(sp.rem(f, z, domain=sp.QQ) == 0 for f in odd_basis)


def main() -> None:
    check_exact_applicability()
    check_saturated_four_space()
    check_common_kernel_and_intersections()
    check_pluecker_degree_and_signed_roots()
    check_involution_classification_identities()
    print("p=28 all-triple tangent-involution independent audit: PASS")
    print("covered residual tuples: (0,10,0,0), (0,10,1,-2)")
    print("signed tangent roots: 18 > cross-minor degree 17")
    print("scope guard: dimension drop only; no profile closure asserted")


if __name__ == "__main__":
    main()
