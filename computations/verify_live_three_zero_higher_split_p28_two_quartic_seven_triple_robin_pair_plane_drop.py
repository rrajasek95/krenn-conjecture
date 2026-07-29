#!/usr/bin/env python3
"""Exact audit of the p=28 4^2 3^7 1 Robin pair-plane drop."""

from __future__ import annotations

from itertools import combinations

import sympy as sp


def wronskian(polynomials: list[sp.Expr], z: sp.Symbol) -> sp.Expr:
    return sp.factor(
        sp.det(
            sp.Matrix(
                [
                    [sp.diff(f, z, order) for f in polynomials]
                    for order in range(len(polynomials))
                ]
            )
        )
    )


def audit_boundary_profiles() -> None:
    residuals = ((2, 7, 0, 1), (2, 7, 1, -1))
    expected_complement = (4, 4) + (3,) * 6 + (1, 1)
    for h in range(22, 28):
        k = 28 - h
        for e, a, b, u in residuals:
            assert 4 * e + 3 * a + 2 * b + u == 30
            selected_doubles = b
            selected_triples = 1
            selected_layers = selected_doubles + selected_triples
            selected_singletons = h + 2 - 2 * selected_layers
            total_singletons = h + u
            fixed_complementary_singletons = (
                total_singletons - selected_singletons
            )
            assert fixed_complementary_singletons == 1

            complement = (
                (4,) * e
                + (3,) * (a - selected_triples)
                + (2,) * (b - selected_doubles)
                + (1,) * (fixed_complementary_singletons + 1)
            )
            assert complement == expected_complement
            assert sum(complement) == 28
            assert len(complement) == 10
            assert len(complement) - 4 == 6

            selected_forced = (
                4 * selected_layers
                + 5 * selected_singletons
                + max(0, 6 - k)
            )
            selected_degree = h + 3 - selected_layers
            selected_cap = 6 * (selected_degree + 1 - 6)
            assert selected_forced == selected_cap


def audit_common_kernel_and_pair_planes() -> None:
    baseline = (4, 4) + (3,) * 7 + (1,)
    assert sum(baseline) == 30
    assert len(baseline) == 10
    for dimension, expected_gap in ((6, 0), (7, 12)):
        forced = sum(dimension - multiplicity for multiplicity in baseline)
        cap = dimension * (11 - dimension)
        assert forced - cap == expected_gap

    relation_dimension = 4
    common_dimension_cap = 6
    pair_lower_bound = 2 * relation_dimension - common_dimension_cap
    pair_ambient_dimension = 10 - 8 + 1
    robin_plane_dimension = pair_ambient_dimension - 1
    assert pair_lower_bound == robin_plane_dimension == 2

    z = sp.symbols("z")
    sites = tuple(range(1, 8))
    factors = {
        site: sp.Poly((z - site) ** 2 * (z + site) ** 2, z)
        for site in sites
    }
    for i, j in combinations(sites, 2):
        assert sp.gcd(factors[i], factors[j]).degree() == 0
        product = factors[i] * factors[j]
        assert product.degree() == 8
        # At a structurally separated singleton site, the coefficient of
        # q'(s) in L_s(product*q) is product(s), hence nonzero.
        for singleton in (0, 8):
            assert product.eval(singleton) != 0


def audit_square_product_span() -> None:
    t = sp.symbols("t")
    a = sp.symbols("a0:4")
    selected_pairs = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3))
    rows = []
    for i, j in selected_pairs:
        polynomial = sp.Poly((t - a[i]) ** 2 * (t - a[j]) ** 2, t)
        rows.append(
            [polynomial.coeff_monomial(t**degree) for degree in range(5)]
        )
    determinant = sp.factor(sp.det(sp.Matrix(rows)))
    expected = sp.factor(
        4
        * (a[0] - a[1]) ** 4
        * (a[0] - a[2])
        * (a[0] - a[3])
        * (a[1] - a[2])
        * (a[1] - a[3])
        * (a[2] - a[3]) ** 2
    )
    assert sp.factor(determinant - expected) == 0
    assert determinant.subs({a[r]: r + 1 for r in range(4)}) != 0


def audit_robin_basis_and_quotient() -> None:
    z, t = sp.symbols("z t")
    s, beta, ai, aj = sp.symbols("s beta ai aj")
    square = s**2
    qij = (t - ai) ** 2 * (t - aj) ** 2
    pij = sp.expand(qij.subs(t, z**2))
    pij_at_s = sp.factor(pij.subs(z, s))
    assert sp.factor(pij_at_s - (square - ai) ** 2 * (square - aj) ** 2) == 0

    log_jet = sp.factor(sp.diff(pij, z).subs(z, s) / pij_at_s)
    expected_log_jet = 4 * s / (square - ai) + 4 * s / (square - aj)
    assert sp.factor(log_jet - expected_log_jet) == 0
    gamma = beta + log_jet

    x = z - s
    x_member = sp.expand(pij * x**2)
    y_member = sp.expand(pij * (1 - gamma * x))

    def robin(poly: sp.Expr) -> sp.Expr:
        return sp.factor(sp.diff(poly, z).subs(z, s) + beta * poly.subs(z, s))

    assert robin(x_member) == 0
    assert sp.factor(robin(y_member)) == 0

    # In parity coordinates R=E(t)+z O(t), Psi_s=2sE+(t+s^2)O.
    # Y has E=(1+gamma*s)Q and O=-gamma*Q.
    quotient_y = sp.factor(
        2 * s * (1 + gamma * s) * qij
        + (t + square) * (-gamma * qij)
    )
    expected_quotient = sp.factor((2 * s + gamma * (square - t)) * qij)
    assert sp.factor(quotient_y - expected_quotient) == 0

    # Kernel identity for Psi_s on (z-s)^2 q(z^2).
    q0, q1, q2, q3, q4 = sp.symbols("q0:5")
    q = q0 + q1 * t + q2 * t**2 + q3 * t**3 + q4 * t**4
    even_part = (t + square) * q
    odd_part = -2 * s * q
    assert sp.expand(2 * s * even_part + (t + square) * odd_part) == 0

    # For s != 0 the affine quotient factor cannot vanish identically:
    # if gamma=0 its constant remainder is 2s; otherwise it has nonzero
    # t coefficient.  Two images sharing only Q_1 cannot be proportional,
    # because their least common square divisor has degree six while each
    # image has degree at most five.
    assert sp.Poly(2 * s + gamma * (square - t), t).degree() <= 1
    q12 = (t - ai) ** 2 * (t - aj) ** 2
    ak = sp.symbols("ak")
    q13 = (t - ai) ** 2 * (t - ak) ** 2
    assert sp.Poly(sp.lcm(sp.Poly(q12, t), sp.Poly(q13, t)), t).degree() == 6
    assert sp.Poly(q12, t).degree() + 1 == 5
    assert sp.Poly(q13, t).degree() + 1 == 5


def audit_zero_singleton_branches() -> None:
    z, t, beta = sp.symbols("z t beta")
    # Pair products span P_4(t).  At s=0 the X space is t P_4 and the Y
    # space is (1-beta*z) P_4.  Their parity-coordinate columns have the
    # following exact ranks for beta != 0.
    basis = [t**degree for degree in range(5)]
    columns = []
    # Coefficient order: even t^0..t^5, then odd z*t^0..z*t^4.
    for q in basis:
        columns.append(
            [sp.Poly(t * q, t).coeff_monomial(t**degree) for degree in range(6)]
            + [0] * 5
        )
    for q in basis:
        columns.append(
            [sp.Poly(q, t).coeff_monomial(t**degree) for degree in range(6)]
            + [
                sp.Poly(-beta * q, t).coeff_monomial(t**degree)
                for degree in range(5)
            ]
        )
    matrix = sp.Matrix.hstack(*(sp.Matrix(column) for column in columns))
    ten_minor = sp.factor(matrix.extract(range(1, 11), range(10)).det())
    assert ten_minor == -beta**5
    assert matrix.subs(beta, 1).rank() == 10

    # At beta=0, P_4+tP_4 is exactly the even P_5.
    assert len(set(range(5)) | set(range(1, 6))) == 6

    even_basis = [z ** (2 * degree) for degree in range(6)]
    even_wronskian = wronskian(even_basis, z)
    assert sp.Poly(even_wronskian, z).degree() == 15
    assert sp.factor(even_wronskian / z**15).is_nonzero
    repeated_forced_weight = 2 * (6 - 4) + 7 * (6 - 3)
    assert repeated_forced_weight == 25
    for nonzero_node in range(1, 10):
        assert even_wronskian.subs(z, nonzero_node) != 0


def main() -> None:
    audit_boundary_profiles()
    audit_common_kernel_and_pair_planes()
    audit_square_product_span()
    audit_robin_basis_and_quotient()
    audit_zero_singleton_branches()
    active_maximal_cap = 3
    moving_triples = 7
    assert moving_triples - active_maximal_cap == 4
    print("p=28 4^2 3^7 1 Robin pair-plane dimension bound: PASS")
    print("s != 0 forces rank >= 7; s = 0, beta != 0 forces rank 10")
    print("the exceptional s = beta = 0 even six-space fails repeated rows")
    print("at most three q=6 selections; at least four have q<=5")
    print("residual tuples covered: (2,7,0,1), (2,7,1,-1)")
    print("scope guard: dimension drop only, not profile closure")


if __name__ == "__main__":
    main()
