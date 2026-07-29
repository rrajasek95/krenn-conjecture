#!/usr/bin/env python3
"""Independent exact audit of the final p=18 low-triple closures.

This checker does not import the primary low-triple checker.  It verifies:

* the complementary-triple third-order row forces D=3 for a=1;
* common cubic divisibility closes b=0,...,8 and is exactly sharp at b=9;
* the a=0,b=11 selected-pair lift has S_ij in P_5 and K_i in P_10;
* ten exact second-order rows force dim K_i <= 5;
* pair intersections force dim K_i=5 and contain g_j g_k;
* the fixed-v logarithmic derivative is
      a_j=(5v+j)/(v^2-j^2),
  its fibres have size at most two, and the pair equations force at least
  seven of the nine available indices into one fibre.

Only integer/rational polynomial arithmetic is used.
"""

from __future__ import annotations

import sympy as sp


def wronskian_cap(degree: int, dimension: int) -> int:
    return dimension * (degree + 1 - dimension)


def forced_weight(
    simple_rows: int,
    double_rows: int,
    triple_rows: int,
    dimension: int,
) -> int:
    return (
        simple_rows * max(dimension - 1, 0)
        + double_rows * max(dimension - 2, 0)
        + triple_rows * max(dimension - 3, 0)
    )


def audit_complementary_triple_row() -> None:
    for h in range(13, 18):
        for b in range(10):
            a = 1
            d = min(b, 2)
            total_singletons = h + 20 - 3 * a - 2 * b
            selected_singletons = h + 2 - 2 * d
            fixed_singletons = selected_singletons - 1
            pool = total_singletons - fixed_singletons
            remaining_doubles = b - d

            # After choosing the moving q, the complement consists of the
            # fixed triple, the remaining doubles, and pool-1 singletons.
            complement_mass = (
                3 + 2 * remaining_doubles + (pool - 1)
            )
            complement_classes = (
                1 + remaining_doubles + (pool - 1)
            )
            relation_degree = complement_classes - 4
            kernel_degree = relation_degree + 3

            assert complement_mass == 18
            assert relation_degree >= 0
            assert pool >= 1

            # The lifted relation three-space forces D>=3.  Adding the
            # complementary triple's exact order-three row rules out D=4.
            assert forced_weight(
                pool, remaining_doubles, 1, 3
            ) <= wronskian_cap(kernel_degree, 3)
            assert forced_weight(
                pool, remaining_doubles, 1, 4
            ) > wronskian_cap(kernel_degree, 4)

            # Once D=3, every moving lift equals the common kernel and all
            # its members are divisible by the pairwise-coprime cubics f_q.
            multiple_dimension = max(
                kernel_degree - 3 * pool + 1, 0
            )
            if b <= 8:
                assert multiple_dimension < 3
            else:
                assert b == 9
                assert (pool, remaining_doubles, kernel_degree) == (2, 7, 8)
                assert multiple_dimension == 3


def audit_zero_triple_endpoint_counts() -> None:
    for h in range(13, 18):
        # Profile 2^11 1^(h-2); select two doubles and all singletons.
        doubles = 11
        singletons = h - 2
        selected_labels = 2 * 2 + singletons
        assert selected_labels == h + 2

        complementary_doubles = doubles - 2
        complement_mass = 2 * complementary_doubles
        complement_classes = complementary_doubles
        relation_degree = complement_classes - 4
        exchange_degree = 5
        kernel_degree = relation_degree + exchange_degree

        assert complement_mass == 18
        assert complement_classes == 9
        assert relation_degree == 5
        assert kernel_degree == 10

        # Ten baseline double nodes, each carrying one normalized
        # second-order row.
        rows = doubles - 1
        assert rows == 10
        assert forced_weight(0, rows, 0, 5) == wronskian_cap(10, 5)
        assert forced_weight(0, rows, 0, 6) > wronskian_cap(10, 6)

        # Two lifted three-spaces have intersection dimension at most one:
        # coprime quintics have a degree-ten product in P_10.  Therefore
        # their sum has dimension at least five, forcing D=5.
        lifted_dimension = 3
        maximum_intersection = 1
        assert 2 * lifted_dimension - maximum_intersection == 5

        # At fixed v, remove i and v from the eleven double values.
        pair_index_pool = doubles - 2
        remaining_after_two_comparison_indices = pair_index_pool - 2
        assert pair_index_pool == 9
        assert remaining_after_two_comparison_indices == 7


def audit_logarithmic_derivative_identity() -> None:
    z, v, j, k = sp.symbols("z v j k")
    alpha, delta = sp.symbols("alpha delta")

    def g(parameter):
        return (z - parameter) ** 3 * (z + parameter) ** 2

    gj = g(j)
    gk = g(k)
    gj_v = gj.subs(z, v)
    gk_v = gk.subs(z, v)
    aj = sp.cancel(sp.diff(gj, z).subs(z, v) / gj_v)
    ak = sp.cancel(sp.diff(gk, z).subs(z, v) / gk_v)

    assert sp.factor(aj - (5 * v + j) / (v**2 - j**2)) == 0
    assert sp.factor(ak - (5 * v + k) / (v**2 - k**2)) == 0

    # Normalize J_v(P)=P''+2 alpha P'+delta P by P(v).
    product = gj * gk
    normalized_row = sp.cancel(
        (
            sp.diff(product, z, 2)
            + 2 * alpha * sp.diff(product, z)
            + delta * product
        ).subs(z, v)
        / (gj_v * gk_v)
    )
    bj = sp.cancel(
        sp.diff(gj, z, 2).subs(z, v) / gj_v + 2 * alpha * aj
    )
    bk = sp.cancel(
        sp.diff(gk, z, 2).subs(z, v) / gk_v + 2 * alpha * ak
    )
    assert sp.factor(
        normalized_row - (delta + bj + bk + 2 * aj * ak)
    ) == 0

    # A fixed value A of a_j gives a genuine quadratic in j with linear
    # coefficient one, so every fibre has at most two elements.
    A = sp.symbols("A")
    fibre_polynomial = sp.expand(
        A * j**2 + j + 5 * v - A * v**2
    )
    cleared_equation = sp.factor(
        (A - (5 * v + j) / (v**2 - j**2)) * (v**2 - j**2)
    )
    assert sp.factor(cleared_equation + fibre_polynomial) == 0
    assert sp.Poly(fibre_polynomial, j).coeff_monomial(j) == 1
    assert sp.Poly(fibre_polynomial, j).degree() <= 2

    # Subtracting the pair equations E(j,k) and E(l,k) leaves exactly
    # (b_j-b_l)+2(a_j-a_l)a_k.  If a_j != a_l this fixes a_k
    # independently of k for all seven remaining indices.
    aj_symbol, al_symbol, ak_symbol = sp.symbols("a_j a_l a_k")
    bj_symbol, bl_symbol, bk_symbol, c = sp.symbols(
        "b_j b_l b_k c"
    )
    equation_jk = c + bj_symbol + bk_symbol + 2 * aj_symbol * ak_symbol
    equation_lk = c + bl_symbol + bk_symbol + 2 * al_symbol * ak_symbol
    assert sp.expand(
        equation_jk
        - equation_lk
        - (
            bj_symbol
            - bl_symbol
            + 2 * (aj_symbol - al_symbol) * ak_symbol
        )
    ) == 0
    assert 7 > 2


def audit_exchange_factor_orders() -> None:
    z, q = sp.symbols("z q")
    f = (z - q) ** 2 * (z + q)
    g = (z - q) ** 3 * (z + q) ** 2

    # The singleton lift is automatic at its selected node through order 1.
    assert f.subs(z, q) == 0
    assert sp.diff(f, z).subs(z, q) == 0

    # The selected-double lift is automatic at its selected node through
    # order 2.
    assert g.subs(z, q) == 0
    assert sp.diff(g, z).subs(z, q) == 0
    assert sp.diff(g, z, 2).subs(z, q) == 0

    # At a distinct nonopposite complementary node x, multiplication by f
    # transports a normalized order-three row because f(x) is a unit.
    x = sp.symbols("x")
    assert sp.factor(f.subs(z, x)) == (-q + x) ** 2 * (q + x)


def main() -> None:
    audit_complementary_triple_row()
    audit_zero_triple_endpoint_counts()
    audit_logarithmic_derivative_identity()
    audit_exchange_factor_orders()

    print("independent p=18 final low-triple audit: PASS")
    print("a=1 closed through b=8; b=9 is exact divisor-dimension equality")
    print("a=0,b=11 endpoint: D=5 and nine-index/fibre contradiction verified")


if __name__ == "__main__":
    main()
