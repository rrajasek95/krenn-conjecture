#!/usr/bin/env python3
"""Independent exact audit of the higher-split exchange closure.

The checks here deliberately do not import the main checker.  They cover
the Hermite degree bookkeeping, the zero-anchor cubic gauge, the numerical
inequalities in the two-dimensional-pencil contradiction, exact small-m
searches for a counterexample to the three-lift lemma, the terminal residue
multiplier, and the graph-layer cardinalities.
"""

from __future__ import annotations

from itertools import product

import sympy as sp


def poly_vector(poly: sp.Expr, z: sp.Symbol, degree: int) -> list[sp.Expr]:
    expanded = sp.Poly(sp.expand(poly), z)
    return [expanded.nth(j) for j in range(degree + 1)]


def check_hermite_context() -> None:
    """Reconstruct every cardinality and numerator-degree bound."""
    for r in range(9, 45):
        p = r - 1
        for h in range(7, r - 1):
            k = p - h
            size_e = p + h + 2
            size_r = h
            size_n = size_e - size_r
            size_l = size_n - 2
            size_active = k + 1
            degree_d = (k + 1) + 2 * h
            degree_q_cap = degree_d - 2
            degree_residual_cap = degree_q_cap - size_n
            assert k >= 1
            assert size_n == p + 2
            assert size_l == p
            assert size_r + k == p
            assert size_active >= 2
            assert degree_d == p + h + 1
            assert degree_q_cap == p + h - 1
            assert degree_residual_cap == h - 3

    # Exact partial-fraction stress, with a zero exceptional anchor and
    # several common-column jets.  The numerator columns are independent
    # and each has degree at most deg(D)-2.
    z = sp.symbols("z")
    anchors = [0, 1, 3, 7, 12, 18, 25]
    mu = sp.Integer(31)
    k = 3
    denominator = (z + mu) ** (k + 1) * sp.prod(
        (z + anchor) ** 2 for anchor in anchors
    )
    fractions = [1 / (z + anchor) ** 2 for anchor in anchors]
    fractions += [1 / (z + mu) ** (j + 2) for j in range(k)]
    numerator_columns = [sp.cancel(denominator * value) for value in fractions]
    degree_d = sp.Poly(denominator, z).degree()
    assert all(sp.denom(value) == 1 for value in numerator_columns)
    assert all(sp.Poly(value, z).degree() <= degree_d - 2 for value in numerator_columns)
    coefficient_matrix = sp.Matrix.hstack(
        *[
            sp.Matrix(poly_vector(value, z, degree_d - 2))
            for value in numerator_columns
        ]
    )
    assert coefficient_matrix.rank() == len(fractions)


def check_robin_extraction_and_zero_gauge() -> None:
    """Check the residue sign and cubic gauge, also at the zero anchor."""
    z, a, b, mu = sp.symbols("z a b mu")
    k = sp.Integer(4)
    g = (z - b) * (z + b) ** 2
    psi = 1 / (a + b) - 2 / (b - a)
    assert sp.factor(sp.diff(g, z).subs(z, -a) / g.subs(z, -a) + psi) == 0

    g0 = z**3
    psi_a0 = 1 / a - 2 / (-a)
    assert sp.factor(sp.diff(g0, z).subs(z, -a) / g0.subs(z, -a) + psi_a0) == 0
    assert g0.subs(z, 0) == 0
    assert sp.diff(g0, z).subs(z, 0) == 0

    # Independently derive Y from P_N / D_tilde at z=-a.
    rows = sp.symbols("x0:4")
    other_anchors = sp.symbols("c0:3")
    p_n = sp.prod(z - value for value in rows)
    d_tilde = (z + mu) ** (k + 1) * sp.prod(
        (z + value) ** 2 for value in other_anchors
    )
    derived = sp.diff(p_n, z).subs(z, -a) / p_n.subs(z, -a)
    derived -= sp.diff(d_tilde, z).subs(z, -a) / d_tilde.subs(z, -a)
    expected = -sum(1 / (a + value) for value in rows)
    expected -= (k + 1) / (mu - a)
    expected -= 2 * sum(1 / (value - a) for value in other_anchors)
    assert sp.factor(derived - expected) == 0


def check_pencil_counts() -> None:
    """Exhaust every small admissible gcd/pole-count edge."""
    for epsilon in (0, 1):
        for n in range(1, 15):
            m = n + epsilon - 1
            for rho in range(n + 1):
                for sigma in range(n + 1):
                    for e0 in ((0,) if epsilon == 0 else (0, 2, 3, 4, 5)):
                        minimum_e = rho + 2 * sigma + e0
                        if minimum_e > m:
                            continue
                        for e in range(minimum_e, m + 1):
                            delta_cap = m - e
                            for delta in range(1, delta_cap + 1):
                                u = n - rho - sigma
                                assert u >= delta
                                assert n - sigma >= delta
                                ramification_points = 2 * (n - sigma)
                                assert ramification_points > 2 * delta - 2

    z = sp.symbols("z")
    for delta in range(1, 8):
        p_coeff = [sp.Integer((j + 1) * (j + 2) + 1) for j in range(delta + 1)]
        q_coeff = [sp.Integer((j + 2) * (j + 4) - 1) for j in range(delta + 1)]
        p = sum(p_coeff[j] * z**j for j in range(delta + 1))
        q = sum(q_coeff[j] * z**j for j in range(delta + 1))
        cross = sp.expand(p * q.subs(z, -z) - p.subs(z, -z) * q)
        assert sp.expand(cross.subs(z, -z) + cross) == 0
        assert sp.Poly(cross, z).degree() <= 2 * delta - 1


def robin_matrix(
    anchors: tuple[int, ...], y_values: tuple[int, ...], degree: int
) -> sp.Matrix:
    """Rows P'(-a)+Y_a P(-a) on polynomials of bounded degree."""
    rows: list[list[sp.Expr]] = []
    for anchor, y_value in zip(anchors, y_values, strict=True):
        node = -anchor
        rows.append(
            [
                (0 if j == 0 else j * node ** (j - 1)) + y_value * node**j
                for j in range(degree + 1)
            ]
        )
    return sp.Matrix(rows)


def small_m_counterexample_search() -> tuple[int, int]:
    """Search exact rational Robin grids for a span of dimension below 3.

    For each Robin kernel and each anchor b, we compute the whole subspace
    of kernel members divisible by g_b.  A candidate counterexample would
    make every such intersection nonzero while their combined span had
    dimension at most two.
    """
    z = sp.symbols("z")
    tested = 0
    qualifying = 0
    anchor_sets = {
        3: ((0, 1, 3, 7), (1, 2, 4, 7)),
        4: ((0, 1, 3, 7, 12), (1, 2, 4, 7, 11)),
        5: ((0, 1, 3, 7, 12, 18),),
        6: ((0, 1, 3, 7, 12, 18, 25),),
        7: ((0, 1, 3, 7, 12, 18, 25, 33),),
    }
    for m, sets in anchor_sets.items():
        q_degree = m - 3
        for anchors in sets:
            assert len(anchors) == m + 1
            assert len(set(anchors)) == len(anchors)
            assert all(-a not in anchors for a in anchors if a != 0)
            # The larger grids at m=3,4 and smaller grids through the first
            # proof-relevant value m=7 keep this exact search quick while
            # including zero and nonzero cases.
            y_grid = (-2, -1, 0, 1, 2) if m <= 4 else (-1, 0, 1)
            for y_values in product(y_grid, repeat=m + 1):
                tested += 1
                common_robin = robin_matrix(anchors, y_values, m)
                lifted_columns: list[sp.Matrix] = []
                all_nonzero = True
                for b in anchors:
                    gauge = sp.expand((z - b) * (z + b) ** 2)
                    multiplier = sp.Matrix.hstack(
                        *[
                            sp.Matrix(poly_vector(gauge * z**j, z, m))
                            for j in range(q_degree + 1)
                        ]
                    )
                    restricted = common_robin * multiplier
                    nullspace = restricted.nullspace()
                    if not nullspace:
                        all_nonzero = False
                        break
                    lifted_columns.extend(multiplier * vector for vector in nullspace)
                if not all_nonzero:
                    continue
                qualifying += 1
                span_rank = sp.Matrix.hstack(*lifted_columns).rank()
                assert span_rank >= 3
    return tested, qualifying


def check_full_core_multiplier() -> None:
    """Verify terminal signs, infinity degree, and evaluation surjectivity."""
    z = sp.symbols("z")
    anchors = [0, 1, 3, 7, 12, 18, 25]
    mu = 31
    k = 4
    nodes = [-value for value in anchors]
    root_poly = sp.prod(z - value for value in nodes)
    m_size = len(nodes)

    for node in nodes:
        others = [value for value in nodes if value != node]
        assert sp.factor(
            sp.diff(root_poly, z, 2).subs(z, node)
            / sp.diff(root_poly, z).subs(z, node)
            - 2 * sum(sp.Rational(1, node - other) for other in others)
        ) == 0

    # On the shifted monomial basis, the multiplier operator is diagonal.
    for j in range(m_size + 2):
        s = (z + mu) ** j
        image = (z + mu) * sp.diff(s, z) + (k + 1) * s
        assert sp.expand(image - (j + k + 1) * s) == 0

    # G_s' evaluations for s=1,(z+mu),...,(z+mu)^(M-1) already form
    # an invertible M by M matrix; this is stronger than merely checking
    # the stated degree-(M+1) evaluation map is onto.
    evaluation = sp.Matrix(
        [
            [
                (j + k + 1) * (node + mu) ** (j + k)
                for j in range(m_size)
            ]
            for node in nodes
        ]
    )
    assert evaluation.det() != 0

    # The maximal allowed product s*q/P^2 has degree at most -2 at
    # infinity, exactly the residue-free threshold used in the note.
    assert (m_size + 1) + (m_size - 3) - 2 * m_size == -2

    # Exact terminal Robin matrices have full column rank in rational
    # instances, including zero and nonzero-only anchor sets.
    instances = [
        ([0, 1, 3, 7, 12], 19, 1),
        ([1, 2, 4, 7, 11, 16], 23, 3),
        ([0, 2, 5, 9, 14, 20, 27], 37, 5),
    ]
    for anchor_values, mu_value, k_value in instances:
        node_values = [-value for value in anchor_values]
        p_root = sp.prod(z - value for value in node_values)
        rows: list[list[sp.Expr]] = []
        for node in node_values:
            y_value = -sp.Rational(k_value + 1, node + mu_value)
            y_value -= sp.diff(p_root, z, 2).subs(z, node) / sp.diff(
                p_root, z
            ).subs(z, node)
            rows.append(
                [
                    (0 if j == 0 else j * node ** (j - 1)) + y_value * node**j
                    for j in range(len(node_values) - 2)
                ]
            )
        matrix = sp.Matrix(rows)
        assert matrix.rank() == len(node_values) - 2


def check_graph_cleanup_counts() -> None:
    """Audit the inherited isolated-star shore sizes at every split."""
    for r in range(9, 45):
        p = r - 1
        for h in range(7, r - 1):
            k = p - h
            exceptional = p + h + 2
            active = k + 1
            fixed_r = h
            complement_n = exceptional - fixed_r
            marked_b = 2
            l_size = complement_n - marked_b
            # Removing the target star leaves h exceptional columns and k
            # common columns, against the p labels in L.
            assert fixed_r + (active - 1) == p
            assert l_size == p
            # A nontarget active star leaves one extra row-zero and one
            # fewer row-one site, hence no balanced matching cofactor.
            assert (l_size + 1, fixed_r + active - 2) == (p + 1, p - 1)


def main() -> None:
    check_hermite_context()
    check_robin_extraction_and_zero_gauge()
    check_pencil_counts()
    tested, qualifying = small_m_counterexample_search()
    check_full_core_multiplier()
    check_graph_cleanup_counts()
    print("independent higher-split exchange audit: PASS")
    print(f"small-m exact Robin grids tested: {tested}")
    print(f"grids satisfying every cubic intersection: {qualifying}")
    print("no span-one or span-two three-lift counterexample found")
    print("Hermite, zero-gauge, full-core residue, and cleanup counts: exact")


if __name__ == "__main__":
    main()
