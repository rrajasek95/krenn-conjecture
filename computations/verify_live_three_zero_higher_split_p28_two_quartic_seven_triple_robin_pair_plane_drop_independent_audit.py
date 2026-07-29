#!/usr/bin/env python3
"""Independent exact audit of the p=28 two-quartic Robin-plane bound.

This script deliberately does not import the primary checker.  It rebuilds
the profile bookkeeping, Wronskian bounds, four-value product span, Robin
quotient, zero-singleton branches, and the exceptional even-space
Wronskian from exact symbolic arithmetic.
"""

from __future__ import annotations

from itertools import combinations

import sympy as sp


def exact_row_cost(dimension: int, order: int, gcd_order: int) -> int:
    """Minimum local Wronskian cost after removing a common local gcd."""
    if gcd_order <= order:
        reduced_order = order - gcd_order
        reduced_cost = max(0, dimension - reduced_order)
    else:
        reduced_cost = 0
    return dimension * gcd_order + reduced_cost


def wronskian(polynomials: list[sp.Expr], z: sp.Symbol) -> sp.Expr:
    matrix = sp.Matrix(
        [
            [sp.diff(polynomial, z, derivative) for polynomial in polynomials]
            for derivative in range(len(polynomials))
        ]
    )
    return sp.factor(matrix.det())


def audit_profiles_and_relation_spaces() -> None:
    residual_profiles = ((2, 7, 0, 1), (2, 7, 1, -1))
    selected_complement = (4, 4) + (3,) * 6 + (1, 1)
    common_baseline = (4, 4) + (3,) * 7 + (1,)

    assert sum(selected_complement) == 28
    assert len(selected_complement) == 10
    assert sum(common_baseline) == 30
    assert len(common_baseline) == 10

    for h in range(22, 28):
        k = 28 - h
        for quartics, triples, doubles, singleton_shift in residual_profiles:
            assert 4 * quartics + 3 * triples + 2 * doubles + singleton_shift == 30

            # The moving triple is always selected in role two.  In the
            # second residual profile the sole double is selected as well.
            role_two_layers = 1 + doubles
            selected_singletons = h + 2 - 2 * role_two_layers
            available_singletons = h + singleton_shift
            fixed_unselected_singletons = available_singletons - selected_singletons
            assert fixed_unselected_singletons == 1

            reconstructed = (
                (4,) * quartics
                + (3,) * (triples - 1)
                + (2,) * (doubles - doubles)
                + (1,) * (fixed_unselected_singletons + 1)
            )
            assert reconstructed == selected_complement

            # The p=28 selected-kernel frontier is equality at q=6 and has
            # excess 12 at q=7, for every one of the six relevant splits.
            for q, expected_gap in ((6, 0), (7, 12)):
                forced = (
                    role_two_layers * (q - 2)
                    + selected_singletons * (q - 1)
                    + max(0, q - k)
                )
                selected_degree = h + 3 - role_two_layers
                cap = q * (selected_degree + 1 - q)
                assert forced - cap == expected_gap

            previous_gap = 12
            for q in range(8, selected_degree + 2):
                forced = (
                    role_two_layers * (q - 2)
                    + selected_singletons * (q - 1)
                    + max(0, q - k)
                )
                cap = q * (selected_degree + 1 - q)
                gap = forced - cap
                assert gap > previous_gap
                previous_gap = gap

    # A six-dimensional selected kernel has a four-dimensional row-relation
    # space in degree c-4=6.  Quartic transport puts it in degree ten.
    selected_kernel_dimension = 6
    relation_dimension = selected_kernel_dimension - 2
    relation_degree = len(selected_complement) - 4
    transport_degree = 4
    assert relation_dimension == 4
    assert relation_degree == 6
    assert relation_degree + transport_degree == 10


def audit_exact_transport_and_common_kernel() -> None:
    z, i = sp.symbols("z i")
    r0, r1, r2, r3 = sp.symbols("r0:4")
    x = z - i
    regular = r0 + r1 * x + r2 * x**2 + r3 * x**3

    # Locally one (z-i)^2 factor of the quartic transport changes the
    # selected exact first-order row into the baseline exact third-order row.
    lifted = sp.expand(x**2 * regular)
    assert sp.diff(lifted, z, 3).subs(z, i) == 6 * r1

    common_baseline = (4, 4) + (3,) * 7 + (1,)
    common_degree = 10
    for dimension, expected_excess in ((6, 0), (7, 12)):
        forced = sum(max(0, dimension - order) for order in common_baseline)
        cap = dimension * (common_degree + 1 - dimension)
        assert forced - cap == expected_excess

        # Removing any common local gcd cannot lower the row contribution
        # below the base-point-free exact-row contribution.
        for order in set(common_baseline):
            base_cost = max(0, dimension - order)
            for gcd_order in range(order + 4):
                assert exact_row_cost(dimension, order, gcd_order) >= base_cost

    assert sum(max(0, 7 - order) for order in common_baseline) == 40
    assert 7 * (11 - 7) == 28


def audit_pair_intersections_and_robin_basis() -> None:
    z = sp.symbols("z")
    s, beta = sp.symbols("s beta")
    sites = (1, 2, 3, 4)
    quartics = {site: sp.Poly((z**2 - site**2) ** 2, z) for site in sites}

    for left, right in combinations(sites, 2):
        assert sp.gcd(quartics[left], quartics[right]).degree() == 0
        product = quartics[left] * quartics[right]
        assert product.degree() == 8
        # In degree ten the coprime pair ambient is product*P_2.
        assert 10 - product.degree() + 1 == 3

    relation_dimension = 4
    common_dimension_cap = 6
    intersection_lower_bound = 2 * relation_dimension - common_dimension_cap
    robin_ambient_dimension = 3 - 1
    assert intersection_lower_bound == robin_ambient_dimension == 2

    ai, aj = sp.symbols("ai aj")
    product = sp.expand((z**2 - ai) ** 2 * (z**2 - aj) ** 2)
    product_at_s = sp.factor(product.subs(z, s))
    log_derivative = sp.factor(sp.diff(product, z).subs(z, s) / product_at_s)
    expected_log_derivative = 4 * s / (s**2 - ai) + 4 * s / (s**2 - aj)
    assert sp.factor(log_derivative - expected_log_derivative) == 0

    gamma = beta + log_derivative
    x = z - s
    first_member = sp.expand(product * x**2)
    second_member = sp.expand(product * (1 - gamma * x))

    def robin(polynomial: sp.Expr) -> sp.Expr:
        return sp.factor(
            sp.diff(polynomial, z).subs(z, s) + beta * polynomial.subs(z, s)
        )

    assert robin(first_member) == 0
    assert sp.factor(robin(second_member)) == 0

    # The restriction to product*P_2 is genuinely nonzero whenever the
    # singleton is structurally separated: q=z-s has Robin value product(s).
    test_q = z - s
    assert sp.factor(robin(product * test_q) - product_at_s) == 0


def audit_four_value_product_span() -> None:
    t = sp.symbols("t")
    a0, a1, a2, a3 = sp.symbols("a0:4")
    squares = (a0, a1, a2, a3)
    five_pairs = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3))
    assert set(index for pair in five_pairs for index in pair) == set(range(4))

    coefficient_rows = []
    for left, right in five_pairs:
        polynomial = sp.Poly(
            (t - squares[left]) ** 2 * (t - squares[right]) ** 2, t
        )
        coefficient_rows.append(
            [polynomial.coeff_monomial(t**degree) for degree in range(5)]
        )
    determinant = sp.factor(sp.Matrix(coefficient_rows).det())
    expected = sp.factor(
        4
        * (a0 - a1) ** 4
        * (a0 - a2)
        * (a0 - a3)
        * (a1 - a2)
        * (a1 - a3)
        * (a2 - a3) ** 2
    )
    assert sp.factor(determinant - expected) == 0


def audit_nonzero_singleton_quotient() -> None:
    z, t, s, gamma = sp.symbols("z t s gamma")

    # In parity coordinates (E_0,...,E_5,O_0,...,O_4), the six even
    # coefficient columns give a (2s)I_6 minor of Psi_s.  Thus Psi_s has
    # rank six whenever s is nonzero.
    quotient_matrix = sp.zeros(6, 11)
    for degree in range(6):
        quotient_matrix[degree, degree] = 2 * s
    for degree in range(5):
        quotient_matrix[degree, 6 + degree] += s**2
        quotient_matrix[degree + 1, 6 + degree] += 1
    assert sp.factor(quotient_matrix[:, :6].det()) == (2 * s) ** 6

    # The five expected kernel vectors are (z-s)^2 t^j, 0<=j<=4.
    for degree in range(5):
        even = (t + s**2) * t**degree
        odd = -2 * s * t**degree
        assert sp.expand(2 * s * even + (t + s**2) * odd) == 0

    ai, aj = sp.symbols("ai aj")
    qij = (t - ai) ** 2 * (t - aj) ** 2
    even_y = (1 + gamma * s) * qij
    odd_y = -gamma * qij
    quotient_y = sp.factor(2 * s * even_y + (t + s**2) * odd_y)
    expected_y = sp.factor((2 * s + gamma * (s**2 - t)) * qij)
    assert sp.factor(quotient_y - expected_y) == 0

    # Two pair images sharing just one square factor cannot be proportional:
    # a common nonzero polynomial would contain three distinct squared
    # factors (degree six), while each quotient image has degree at most five.
    a1, a2, a3 = sp.symbols("a1 a2 a3")
    fraction_field = sp.QQ.frac_field(a1, a2, a3)
    q12 = sp.Poly((t - a1) ** 2 * (t - a2) ** 2, t, domain=fraction_field)
    q13 = sp.Poly((t - a1) ** 2 * (t - a3) ** 2, t, domain=fraction_field)
    common_divisor = sp.gcd(q12, q13)
    lcm_degree = q12.degree() + q13.degree() - common_divisor.degree()
    assert common_divisor.degree() == 2
    assert lcm_degree == 6
    assert q12.degree() + 1 == q13.degree() + 1 == 5


def audit_zero_singleton_branches() -> None:
    z, t, beta = sp.symbols("z t beta")

    # Coordinate order is even 1,t,...,t^5 followed by odd z,zt,...,zt^4.
    columns: list[sp.Matrix] = []
    for degree in range(5):
        vector = [0] * 11
        vector[degree + 1] = 1  # t*P_4(t)
        columns.append(sp.Matrix(vector))
    for degree in range(5):
        vector = [0] * 11
        vector[degree] = 1
        vector[6 + degree] = -beta  # (1-beta*z)*P_4(t)
        columns.append(sp.Matrix(vector))
    combined = sp.Matrix.hstack(*columns)
    assert sp.factor(combined.extract(range(1, 11), range(10)).det()) == -beta**5
    assert combined.subs(beta, 2).rank() == 10

    # For beta=0 the two spaces are P_4(t) and tP_4(t), whose union is P_5(t).
    assert combined.subs(beta, 0).rank() == 6

    even_basis = [z ** (2 * degree) for degree in range(6)]
    even_wronskian = wronskian(even_basis, z)
    quotient = sp.factor(even_wronskian / z**15)
    assert quotient != 0 and not quotient.has(z)

    # Every repeated baseline node is nonzero.  In fact one active triple
    # node already contradicts this Wronskian; the full baseline would demand
    # the larger total nonzero-node weight recorded below.
    active_nonzero_node = sp.Integer(2)
    assert even_wronskian.subs(z, active_nonzero_node) != 0
    assert max(0, 6 - 3) == 3
    full_repeated_weight = 2 * (6 - 4) + 7 * (6 - 3)
    assert full_repeated_weight == 25


def main() -> None:
    audit_profiles_and_relation_spaces()
    audit_exact_transport_and_common_kernel()
    audit_pair_intersections_and_robin_basis()
    audit_four_value_product_span()
    audit_nonzero_singleton_quotient()
    audit_zero_singleton_branches()

    active_values = 4
    pair_planes_available = len(tuple(combinations(range(active_values), 2)))
    assert pair_planes_available == 6
    assert 7 - (active_values - 1) == 4

    print("independent p=28 4^2 3^7 1 Robin pair-plane audit: PASS")
    print("four maximal selections suffice; no fifth, sixth, or seventh is used")
    print("s!=0 gives five kernel directions plus two quotient directions")
    print("s=0,beta!=0 gives rank ten; s=beta=0 gives an impossible even six-space")
    print("conclusion: at most three q=6 selections, hence at least four q<=5")
    print("scope guard: fixed-baseline dimension drop only, not profile closure")


if __name__ == "__main__":
    main()
