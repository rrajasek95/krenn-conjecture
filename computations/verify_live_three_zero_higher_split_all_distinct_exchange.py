#!/usr/bin/env python3
"""Exact audits for the uniform higher-split exchange closure.

This script checks the algebraic identities and every numerical inequality
used in the proof.  All stress instances are over ``QQ``; there is no
floating-point or random computation.
"""

from __future__ import annotations

import sympy as sp


def check_split_bookkeeping() -> None:
    """Audit all degree and cardinality formulas on a broad exact range."""
    for original_r in range(9, 51):
        for h in range(7, original_r - 1):
            p = original_r - 1
            k = p - h
            exceptional_size = p + h + 2
            complement_size = p + 2
            denominator_degree = (k + 1) + 2 * h
            numerator_degree_cap = denominator_degree - 2
            residual_degree_cap = numerator_degree_cap - complement_size

            assert k >= 1
            assert exceptional_size == p + h + 2
            assert denominator_degree == p + h + 1
            assert numerator_degree_cap == p + h - 1
            assert residual_degree_cap == h - 3


def check_cubic_gauge_and_lift() -> None:
    """Verify the logarithmic gauge and the lifted Robin row exactly."""
    z, a, b, old_y, q_value = sp.symbols("z a b old_y q_value")

    def gauge(anchor: sp.Expr) -> sp.Expr:
        return (z - anchor) * (z + anchor) ** 2

    def psi(anchor: sp.Expr, added: sp.Expr) -> sp.Expr:
        return 1 / (anchor + added) - 2 / (added - anchor)

    g_b = gauge(b)
    g_value = g_b.subs(z, -a)
    g_derivative = sp.diff(g_b, z).subs(z, -a)
    assert sp.factor(g_derivative / g_value + psi(a, b)) == 0

    # Substitute q'(-a)=-old_y*q(-a) into the lifted Robin expression.
    lifted_row = (
        g_derivative * q_value
        + g_value * (-old_y * q_value)
        + (old_y + psi(a, b)) * g_value * q_value
    )
    assert sp.factor(lifted_row) == 0
    assert sp.expand(g_b.subs(z, -b)) == 0
    assert sp.expand(sp.diff(g_b, z).subs(z, -b)) == 0

    # The pairwise-coprime assertion also includes the possible zero anchor.
    sample_anchors = [0, 1, 3, 7, -2]
    sample_gauges = [sp.Poly(gauge(value), z, domain=sp.QQ) for value in sample_anchors]
    for i, left in enumerate(sample_gauges):
        for right in sample_gauges[i + 1 :]:
            assert sp.gcd(left, right).degree() == 0


def check_gcd_and_ramification_inequalities() -> None:
    """Check the sharp gcd, zero-node, cross-root, and RH counts."""
    n, epsilon, rho, sigma, e0 = sp.symbols(
        "n epsilon rho sigma e0", integer=True, nonnegative=True
    )
    minimum_gcd_degree = rho + 2 * sigma + e0
    maximum_delta = n + epsilon - 1 - minimum_gcd_degree
    guaranteed_cross_anchors = n - rho - sigma

    assert sp.expand(
        guaranteed_cross_anchors
        - maximum_delta
        - (1 - epsilon + sigma + e0)
    ) == 0
    assert sp.expand(
        n
        - sigma
        - (maximum_delta - 1)
        - (2 - epsilon + rho + sigma + e0)
    ) == 0

    # Enumerate every small combinatorial edge that can still allow a
    # nonconstant pencil (maximum_delta >= 1).  e0=0 is the no-common-zero
    # case at the zero anchor; a positive e0 must be at least two.
    for n_value in range(1, 14):
        for epsilon_value in (0, 1):
            e0_values = (0,) if epsilon_value == 0 else (0, 2, 3, 4)
            for e0_value in e0_values:
                for rho_value in range(n_value + 1):
                    for sigma_value in range(n_value + 1):
                        delta_cap = (
                            n_value
                            + epsilon_value
                            - 1
                            - rho_value
                            - 2 * sigma_value
                            - e0_value
                        )
                        if delta_cap < 1:
                            continue
                        u_value = n_value - rho_value - sigma_value
                        assert u_value >= delta_cap
                        assert n_value - sigma_value >= delta_cap
                        assert (
                            n_value - sigma_value - (delta_cap - 1)
                            == 2
                            - epsilon_value
                            + rho_value
                            + sigma_value
                            + e0_value
                        )
                        assert n_value - sigma_value - (delta_cap - 1) > 0

    # A double zero of one base-point-free pencil member forces the
    # Wronskian to vanish.  These identities cover either nonzero
    # coefficient of the member, including the alpha=0 or beta=0 edges.
    alpha, beta, p0, p1, q0, q1 = sp.symbols(
        "alpha beta p0 p1 q0 q1"
    )
    member = alpha * p0 + beta * q0
    member_derivative = alpha * p1 + beta * q1
    wronskian = p0 * q1 - p1 * q0
    assert sp.expand(
        p0 * member_derivative - p1 * member - beta * wronskian
    ) == 0
    assert sp.expand(
        q0 * member_derivative - q1 * member + alpha * wronskian
    ) == 0


def check_odd_cross_polynomial() -> None:
    """Check oddness and the cancellation of the degree-2delta term."""
    z = sp.symbols("z")
    for delta in range(1, 8):
        p_coefficients = sp.symbols(f"p0:{delta + 1}")
        q_coefficients = sp.symbols(f"q0:{delta + 1}")
        p = sum(value * z**degree for degree, value in enumerate(p_coefficients))
        q = sum(value * z**degree for degree, value in enumerate(q_coefficients))
        cross = sp.expand(p * q.subs(z, -z) - p.subs(z, -z) * q)
        assert sp.expand(cross.subs(z, -z) + cross) == 0
        assert sp.Poly(cross, z).degree() <= 2 * delta - 1
        assert sp.expand(cross).coeff(z, 2 * delta) == 0


def check_full_core_logarithmic_derivative() -> None:
    """Verify the full-core Robin coefficient and local Laurent terms."""
    z = sp.symbols("z")
    nodes = sp.symbols("x0:5")
    root_polynomial = sp.prod(z - node for node in nodes)
    first = sp.diff(root_polynomial, z)
    second = sp.diff(root_polynomial, z, 2)
    for i, node in enumerate(nodes):
        logarithmic_derivative = second.subs(z, node) / first.subs(z, node)
        expected = 2 * sum(
            1 / (node - other)
            for j, other in enumerate(nodes)
            if j != i
        )
        assert sp.factor(logarithmic_derivative - expected) == 0

    # Write P=(z-x)R locally.  The coefficient of (z-x)^(-1) is the
    # displayed Robin expression divided by the nonzero double-pole scale.
    w, x, mu, K = sp.symbols("w x mu K")
    q_value, q_derivative, r_value, r_derivative = sp.symbols(
        "q_value q_derivative r_value r_derivative", nonzero=True
    )
    local_numerator = q_value + q_derivative * w
    local_cofactor = r_value + r_derivative * w
    regular_factor = local_numerator / (
        (x + mu + w) ** (K + 1) * local_cofactor**2
    )
    double_coefficient = regular_factor.subs(w, 0)
    simple_coefficient = sp.diff(regular_factor, w).subs(w, 0)
    robin_numerator = q_derivative - (
        (K + 1) / (x + mu) + 2 * r_derivative / r_value
    ) * q_value
    scale = (x + mu) ** (K + 1) * r_value**2
    assert sp.factor(double_coefficient - q_value / scale) == 0
    assert sp.factor(simple_coefficient - robin_numerator / scale) == 0


def check_multiplier_surjectivity() -> None:
    """Audit the shifted Euler operator and its evaluation map."""
    z, mu, K = sp.symbols("z mu K")
    for degree in range(8):
        basis_element = (z + mu) ** degree
        image = (z + mu) * sp.diff(basis_element, z) + (K + 1) * basis_element
        assert sp.expand(image - (degree + K + 1) * basis_element) == 0

    # The derivative evaluation matrix is a diagonally and column-scaled
    # Vandermonde matrix.  Verify its determinant formula symbolically.
    size = 4
    shifted_nodes = sp.symbols(f"v0:{size}")
    row_scales = sp.symbols(f"d0:{size}")
    matrix = sp.Matrix(
        [
            [
                row_scales[i] * (j + K + 1) * shifted_nodes[i] ** j
                for j in range(size)
            ]
            for i in range(size)
        ]
    )
    vandermonde = sp.prod(
        shifted_nodes[j] - shifted_nodes[i]
        for i in range(size)
        for j in range(i + 1, size)
    )
    expected = (
        sp.prod(row_scales)
        * sp.prod(j + K + 1 for j in range(size))
        * vandermonde
    )
    assert sp.factor(matrix.det() - expected) == 0


def terminal_robin_matrix(nodes: list[int], mu: int, k: int) -> sp.Matrix:
    """Robin map on polynomials of degree at most M-3, over QQ."""
    size = len(nodes)
    rows: list[list[sp.Expr]] = []
    for i, node in enumerate(nodes):
        robin_value = -sp.Rational(k + 1, node + mu) - 2 * sum(
            sp.Rational(1, node - other)
            for j, other in enumerate(nodes)
            if j != i
        )
        row = []
        for degree in range(size - 2):
            derivative = 0 if degree == 0 else degree * node ** (degree - 1)
            row.append(derivative + robin_value * node**degree)
        rows.append(row)
    return sp.Matrix(rows)


def check_terminal_robin_stress_instances() -> None:
    """Check exact full column rank, including a zero-node instance."""
    instances = [
        ([0, 1, 2, 3, 4], 7, 1),
        ([-2, 1, 3, 4, 6, 8], 11, 2),
        ([0, 2, 5, 7, 9, 12, 13], 17, 3),
        ([-4, -1, 2, 3, 7, 9, 12, 15], 20, 4),
    ]
    for nodes, mu, k in instances:
        assert len(nodes) == len(set(nodes))
        assert all(-node not in nodes for node in nodes if node != 0)
        assert all(node + mu != 0 for node in nodes)
        matrix = terminal_robin_matrix(nodes, mu, k)
        assert matrix.rank() == len(nodes) - 2

        # The M by M submatrix from s=(z+mu)^j, 0<=j<M, is visibly a
        # scaled Vandermonde and directly confirms evaluation surjectivity.
        evaluation = sp.Matrix(
            [
                [
                    (j + k + 1) * (node + mu) ** (j + k)
                    for j in range(len(nodes))
                ]
                for node in nodes
            ]
        )
        assert evaluation.det() != 0


def main() -> None:
    check_split_bookkeeping()
    check_cubic_gauge_and_lift()
    check_gcd_and_ramification_inequalities()
    check_odd_cross_polynomial()
    check_full_core_logarithmic_derivative()
    check_multiplier_surjectivity()
    check_terminal_robin_stress_instances()
    print("higher-split exchange lift and full-core closure: PASS")
    print("three-lift gcd/zero inequalities and RH count: exact")
    print("full-core residue-multiplier surjectivity: exact")


if __name__ == "__main__":
    main()
