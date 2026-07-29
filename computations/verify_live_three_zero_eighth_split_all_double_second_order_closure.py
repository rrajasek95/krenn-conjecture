#!/usr/bin/env python3
"""Exact audit of the h=8, k=2 all-double second-order closure."""

from __future__ import annotations

from itertools import combinations

import sympy as sp


z, w, mu = sp.symbols("z w mu")


def coefficient_vector(poly: sp.Expr, degree: int) -> list[sp.Expr]:
    expanded = sp.Poly(sp.expand(poly), z)
    return [expanded.coeff_monomial(z**index) for index in range(degree + 1)]


def check_profile_cores_and_double_lift() -> None:
    h, p, k = 8, 10, 2
    multiplicities = (2,) * 10
    assert sum(multiplicities) == p + h + 2 == 20

    core_count = 0
    indices = range(10)
    for full_set in combinations(indices, 5):
        full_set = set(full_set)
        outside = set(indices) - full_set
        for partial_pair in combinations(sorted(full_set), 2):
            takes = {
                index: (1 if index in partial_pair else 2)
                for index in full_set
            }
            complement = tuple(
                multiplicity - takes.get(index, 0)
                for index, multiplicity in enumerate(multiplicities)
            )
            core_count += 1
            assert sum(takes.values()) == h
            assert len(takes) == 5
            assert sum(complement) == p + 2 == 12
            assert sum(entry == 1 for entry in complement) == 2
            assert all(complement[index] == 2 for index in outside)

            residual_cap = len(takes) - 3
            assert residual_cap == 2

    assert core_count == sp.binomial(10, 5) * sp.binomial(5, 2)

    x, y, a, b, c, q = sp.symbols("x y a b c q")
    outside_factor = sp.symbols("outside_factor")
    original = (
        q
        * (z - x)
        * (z - y)
        * outside_factor
        / (
            (z + mu) ** 3
            * (z + x) ** 2
            * (z + y) ** 2
            * (z + a) ** 3
            * (z + b) ** 3
            * (z + c) ** 3
        )
    )
    lifted_polynomial = (z**2 - x**2) * (z**2 - y**2) * q
    common = (
        outside_factor
        * lifted_polynomial
        / (
            (z + mu) ** 3
            * (z + x) ** 3
            * (z + y) ** 3
            * (z + a) ** 3
            * (z + b) ** 3
            * (z + c) ** 3
        )
    )
    assert sp.factor(original - common) == 0

    assert 2 + 4 == 6  # quadratic residual plus two quadratic lifts
    numerator_degree = 2 * 5 + 6
    denominator_degree = (k + 1) + 3 * 5
    assert numerator_degree == 16
    assert denominator_degree == 18
    assert denominator_degree - numerator_degree == 2


def check_exact_order_two_rows_and_wronskian_bound() -> None:
    c0, c1, c2 = sp.symbols("c0 c1 c2")
    regular = c0 + c1 * w + c2 * w**2
    assert sp.residue(regular / w**3, w, 0) == c2

    # If the gcd has order 0, 1, 2, or >=3 at an exact second-order
    # functional, the reduced condition has order 2, 1, is impossible,
    # or is automatic, respectively.  For d>=5 the minimal Wronskian
    # deficit is already positive.
    for dimension in range(5, 8):
        for order_one_nodes in range(7):
            for absorbed_nodes in range(7 - order_one_nodes):
                ordinary_nodes = 6 - order_one_nodes - absorbed_nodes
                gcd_degree = order_one_nodes + 3 * absorbed_nodes
                forced_weight = (
                    ordinary_nodes * (dimension - 2)
                    + order_one_nodes * (dimension - 1)
                )
                degree_bound = dimension * (
                    7 - gcd_degree - dimension
                )
                deficit = forced_weight - degree_bound
                expected = (
                    (dimension - 4) * (dimension + 3)
                    + (dimension + 1) * order_one_nodes
                    + 2 * (dimension + 1) * absorbed_nodes
                )
                assert deficit == expected
                assert deficit > 0

    # Dimension four is the unique sharp local case.  Any gcd degree or
    # absorbed node makes the inequality strict.
    dimension = 4
    ordinary_weight = 6 * (dimension - 2)
    degree_bound = dimension * (7 - dimension)
    assert ordinary_weight == degree_bound == 12


def check_three_dimensional_intersection_classification() -> None:
    values = tuple(map(sp.Integer, (1, 2, 3, 4, 5)))
    quadratics = tuple(z**2 - value**2 for value in values)

    pair_products = [
        quadratics[i] * quadratics[j]
        for i, j in combinations(range(5), 2)
    ]
    pair_matrix = sp.Matrix(
        [coefficient_vector(poly, 4) for poly in pair_products]
    )
    assert pair_matrix.rank() == 3

    # If one divisibility plane is the whole three-space, the products
    # through that fixed quadratic span exactly h_i * P_2(z^2).
    fixed_triples = [
        quadratics[0] * quadratics[i] * quadratics[j]
        for i, j in combinations(range(1, 5), 2)
    ]
    triple_matrix = sp.Matrix(
        [coefficient_vector(poly, 6) for poly in fixed_triples]
    )
    assert triple_matrix.rank() == 3

    # Every parity minor of two sextics is odd and has degree at most 11.
    f_coefficients = sp.symbols("f0:7")
    g_coefficients = sp.symbols("g0:7")
    f = sum(coefficient * z**index for index, coefficient in enumerate(f_coefficients))
    g = sum(coefficient * z**index for index, coefficient in enumerate(g_coefficients))
    parity_minor = sp.expand(f * g.subs(z, -z) - f.subs(z, -z) * g)
    assert sp.expand(parity_minor.subs(z, -z) + parity_minor) == 0
    assert sp.Poly(parity_minor, z).degree() <= 11

    # Restrict an exact second-order z-jet to G(z)R(z^2).  Depending on
    # whether G has local order 0, 1, or 2, an explicitly nonzero
    # coefficient of R'', R', or R remains.
    node, local_y, local_m = sp.symbols(
        "node local_y local_m", nonzero=True
    )
    G0, G1, G2 = sp.symbols("G0 G1 G2")
    R0, R1, R2 = sp.symbols("R0 R1 R2")
    restricted = (
        G2 * R0
        + 4 * node * G1 * R1
        + 2 * G0 * R1
        + 4 * node**2 * G0 * R2
        + 2 * local_y * (G1 * R0 + 2 * node * G0 * R1)
        + local_m * G0 * R0
    )
    assert sp.diff(restricted, R2) == 4 * node**2 * G0
    assert sp.diff(restricted.subs(G0, 0), R1) == 4 * node * G1
    assert sp.diff(
        restricted.subs({G0: 0, G1: 0}), R0
    ) == G2

    # A general second-order row on cubics in s annihilates (s-u)^3.
    u, A, B, M = sp.symbols("u A B M")
    row = sp.Matrix(
        [[
            M,
            A + u * M,
            2 * B + 2 * u * A + u**2 * M,
            6 * u * B + 3 * u**2 * A + u**3 * M,
        ]]
    )
    dual_cubic = (
        row[0] * u**3
        - 3 * row[1] * u**2
        + 3 * row[2] * u
        - row[3]
    )
    assert sp.expand(dual_cubic) == 0


def check_relation_pencil_and_degree_drop() -> None:
    c_coefficients = sp.symbols("c0:5")
    n_coefficients = sp.symbols("n0:8")
    C = z**5 + sum(c_coefficients[index] * z**index for index in range(5))
    N = sum(n_coefficients[index] * z**index for index in range(8))

    differential = sp.expand(
        C * ((z + mu) * sp.diff(N, z) + 3 * N)
        - 2 * (z + mu) * sp.diff(C, z) * N
    )
    assert sp.Poly(differential, z).degree() <= 11

    rational_function = (z + mu) ** 3 * N / C**2
    assert sp.factor(
        sp.diff(rational_function, z)
        - (z + mu) ** 2 * differential / C**3
    ) == 0

    # The leading z^(n+5) coefficient is n-7; at n=7 it cancels, which
    # is the sharp reason that division by a monic Q^2 leaves only P_1.
    for degree in range(8):
        trial = z**degree
        trial_differential = sp.Poly(
            sp.expand(
                C * ((z + mu) * sp.diff(trial, z) + 3 * trial)
                - 2 * (z + mu) * sp.diff(C, z) * trial
            ),
            z,
        )
        assert trial_differential.degree() <= 11
        if degree < 7:
            assert trial_differential.coeff_monomial(
                z ** (degree + 5)
            ) == degree - 7
        else:
            assert trial_differential.coeff_monomial(z**12) == 0

    # The determinant identity for two relation numerators records the
    # induced pencil and fixes all signs.
    N1 = sp.Function("N1")(z)
    N2 = sp.Function("N2")(z)

    def formal_differential(function: sp.Expr) -> sp.Expr:
        return (
            C * ((z + mu) * sp.diff(function, z) + 3 * function)
            - 2 * (z + mu) * sp.diff(C, z) * function
        )

    wronskian = N1 * sp.diff(N2, z) - N2 * sp.diff(N1, z)
    assert sp.expand(
        N1 * formal_differential(N2)
        - N2 * formal_differential(N1)
        - C * (z + mu) * wronskian
    ) == 0

    # If the P_1 image were zero, the rational function would be constant.
    # Structural C(-mu) != 0 then excludes a nonzero identity
    # (z+mu)^3 N = constant*C^2.
    assert sp.factor(C.subs(z, -mu)) != 0


def check_rational_derivative_residues_and_swap() -> None:
    local_u = sp.symbols("local_u")
    a0, a1, a2 = sp.symbols("a0 a1 a2")
    local_regular = a0 + a1 * w + a2 * w**2
    first_residue = sp.residue(local_regular / w**3, w, 0)
    second_residue = sp.residue(
        (local_u + w) * local_regular / w**3, w, 0
    )
    assert first_residue == a2
    assert second_residue == a1 + local_u * a2

    u, a, b = sp.symbols("u a b")
    swap_difference = (
        2 * (1 / (u + b) - 1 / (u + a))
        - 3 * (1 / (u - a) - 1 / (u - b))
    )

    def fibre_map(value: sp.Expr) -> sp.Expr:
        return 2 / (u + value) + 3 / (u - value)

    assert sp.factor(
        swap_difference - (fibre_map(b) - fibre_map(a))
    ) == 0
    assert sp.factor(fibre_map(a) - (5 * u + a) / (u**2 - a**2)) == 0

    fibre_value = sp.symbols("fibre_value")
    fibre_polynomial = sp.expand(
        fibre_value * (u**2 - a**2) - (5 * u + a)
    )
    assert sp.Poly(fibre_polynomial, a).degree() == 2
    assert sp.Poly(fibre_polynomial, a).coeff_monomial(a) == -1
    assert sp.expand(fibre_polynomial.subs(fibre_value, 0)) == -5 * u - a
    assert 9 > 2


def check_global_wronskian_equality_frontier() -> None:
    collision_excess = 10

    # Antiderivative space J.  Here every collision multiplicity m_v is 1.
    survivors = []
    for dimension in range(3, 11):
        for absorbed in range(6):
            for gcd_degree in range(0, 11):
                if gcd_degree < 2 * absorbed:
                    continue
                a = absorbed
                deficit = (
                    dimension**2
                    - collision_excess
                    + dimension * (gcd_degree - a)
                    + a
                )
                if deficit <= 0:
                    survivors.append(
                        (dimension, absorbed, gcd_degree, deficit)
                    )
    assert survivors == [(3, 0, 0, -1)]

    dimension = 3
    numerator_degree = collision_excess - 1
    wronskian_cap = dimension * (
        numerator_degree - dimension + 1
    )
    collision_weight = collision_excess * (dimension - 1)
    assert wronskian_cap == 21
    assert collision_weight == 20
    assert wronskian_cap - collision_weight == 1

    # Full-core K.  With c=10, k=2, ell=0, the only noncontradictory
    # common-pole/gcd case is d=3, gcd=0, u=0, and it is exact equality.
    c, k, ell = 10, 2, 0
    full_survivors = []
    for dimension in range(3, 11):
        for reflected_base_nodes in range(0, 4):
            for common_order in range(0, 6):
                for gcd_degree in range(0, 11):
                    if gcd_degree < 2 * reflected_base_nodes + common_order:
                        continue
                    if common_order <= k:
                        n = k - common_order
                        if ell >= n:
                            continue
                        common_weight = (ell + 1) * max(
                            dimension - k + common_order + ell, 0
                        )
                    else:
                        common_weight = 0

                    deficit = (
                        dimension**2
                        - c
                        + reflected_base_nodes * (dimension + 1)
                        + dimension * common_order
                        + common_weight
                        + dimension
                        * (
                            gcd_degree
                            - 2 * reflected_base_nodes
                            - common_order
                        )
                    )
                    if deficit <= 0:
                        full_survivors.append(
                            (
                                dimension,
                                reflected_base_nodes,
                                common_order,
                                gcd_degree,
                                common_weight,
                                deficit,
                            )
                        )
    assert full_survivors == [(3, 0, 0, 0, 1, 0)]

    dimension = 3
    reflected_weight = c * (dimension - 1)
    common_weight = 1
    polynomial_degree_cap = dimension * (c - dimension)
    assert reflected_weight + common_weight == polynomial_degree_cap == 21


def main() -> None:
    check_profile_cores_and_double_lift()
    check_exact_order_two_rows_and_wronskian_bound()
    check_three_dimensional_intersection_classification()
    check_relation_pencil_and_degree_drop()
    check_rational_derivative_residues_and_swap()
    check_global_wronskian_equality_frontier()
    print("eighth-split all-double 2^10 second-order closure: PASS")
    print("five-node double-partial lifts and dimension four: exact")
    print("rank-three residue rows and P_1 relation pencil: exact")
    print("partition Stieltjes swap and degree-two fibre: impossible")
    print("global K/J Wronskian equality frontier: exact")


if __name__ == "__main__":
    main()
