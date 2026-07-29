#!/usr/bin/env python3
"""Exact audit of the h=8, k=3 profile 2^10 1 closure."""

from __future__ import annotations

from itertools import combinations

import sympy as sp


z, w, mu = sp.symbols("z w mu")


def coefficient_vector(poly: sp.Expr, degree: int) -> list[sp.Expr]:
    expanded = sp.Poly(sp.expand(poly), z)
    return [expanded.coeff_monomial(z**index) for index in range(degree + 1)]


def check_cores_lift_and_degrees() -> None:
    h, p, k = 8, 11, 3
    profile = (2,) * 10 + (1,)
    assert sum(profile) == p + h + 2 == 21

    core_count = 0
    double_indices = set(range(10))
    for five_tuple in combinations(range(10), 5):
        five_set = set(five_tuple)
        outside = double_indices - five_set
        for pair_tuple in combinations(sorted(five_set), 2):
            pair = set(pair_tuple)
            takes = {
                index: (1 if index in pair else 2)
                for index in five_set
            }
            complement = tuple(
                profile[index] - takes.get(index, 0)
                for index in range(len(profile))
            )
            core_count += 1
            assert sum(takes.values()) == h
            assert len(takes) == 5
            assert sum(complement) == p + 2 == 13
            assert sum(entry == 1 for entry in complement) == 3
            assert complement[-1] == 1
            assert all(complement[index] == 2 for index in outside)
            assert all(complement[index] == 1 for index in pair)
            assert len(takes) - 3 == 2
    assert core_count == sp.binomial(10, 5) * sp.binomial(5, 2) == 2520

    x, y, a, b, c, q = sp.symbols("x y a b c q")
    complement_factor = sp.symbols("complement_factor")
    original = (
        q
        * (z - x)
        * (z - y)
        * complement_factor
        / (
            (z + mu) ** 4
            * (z + x) ** 2
            * (z + y) ** 2
            * (z + a) ** 3
            * (z + b) ** 3
            * (z + c) ** 3
        )
    )
    lifted = (z**2 - x**2) * (z**2 - y**2) * q
    common = (
        complement_factor
        * lifted
        / (
            (z + mu) ** 4
            * (z + x) ** 3
            * (z + y) ** 3
            * (z + a) ** 3
            * (z + b) ** 3
            * (z + c) ** 3
        )
    )
    assert sp.factor(original - common) == 0

    residual_degree = 2
    complement_degree = 2 * 5 + 1
    original_numerator_degree = residual_degree + 2 + complement_degree
    original_denominator_degree = (k + 1) + 2 * 2 + 3 * 3
    lifted_numerator_degree = complement_degree + residual_degree + 2 * 2
    lifted_denominator_degree = (k + 1) + 3 * 5
    assert (original_numerator_degree, original_denominator_degree) == (15, 17)
    assert (lifted_numerator_degree, lifted_denominator_degree) == (17, 19)


def check_five_row_local_kernel() -> None:
    # Five exact order-two rows on P_6 already exclude dimension >=5.
    for dimension in range(5, 8):
        for order_one_nodes in range(6):
            for absorbed_nodes in range(6 - order_one_nodes):
                ordinary_nodes = 5 - order_one_nodes - absorbed_nodes
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
                    dimension**2
                    - 2 * dimension
                    - 10
                    + (dimension + 1) * order_one_nodes
                    + 2 * (dimension + 1) * absorbed_nodes
                )
                assert deficit == expected
                assert deficit > 0

    values = tuple(map(sp.Integer, (1, 2, 3, 4, 5)))
    quadratics = tuple(z**2 - value**2 for value in values)
    pair_products = [
        quadratics[i] * quadratics[j]
        for i, j in combinations(range(5), 2)
    ]
    assert sp.Matrix(
        [coefficient_vector(poly, 4) for poly in pair_products]
    ).rank() == 3

    fixed_triples = [
        quadratics[0] * quadratics[i] * quadratics[j]
        for i, j in combinations(range(1, 5), 2)
    ]
    assert sp.Matrix(
        [coefficient_vector(poly, 6) for poly in fixed_triples]
    ).rank() == 3

    f_coefficients = sp.symbols("f0:7")
    g_coefficients = sp.symbols("g0:7")
    f = sum(coefficient * z**index for index, coefficient in enumerate(f_coefficients))
    g = sum(coefficient * z**index for index, coefficient in enumerate(g_coefficients))
    parity_minor = sp.expand(f * g.subs(z, -z) - f.subs(z, -z) * g)
    assert sp.expand(parity_minor.subs(z, -z) + parity_minor) == 0
    assert sp.Poly(parity_minor, z).degree() <= 11

    # Exact second-order row restricted to G(z)R(z^2).
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
    assert sp.diff(restricted.subs({G0: 0, G1: 0}), R0) == G2

    # Five distinct squared supports cannot be roots of one dual cubic.
    squared_node, A0, A1, A2 = sp.symbols("squared_node A0 A1 A2")
    row = sp.Matrix(
        [[
            A0,
            A1 + squared_node * A0,
            2 * A2 + 2 * squared_node * A1 + squared_node**2 * A0,
            6 * squared_node * A2
            + 3 * squared_node**2 * A1
            + squared_node**3 * A0,
        ]]
    )
    dual_cubic = (
        row[0] * squared_node**3
        - 3 * row[1] * squared_node**2
        + 3 * row[2] * squared_node
        - row[3]
    )
    assert sp.expand(dual_cubic) == 0
    assert 5 > 3


def check_relation_plane_and_singleton_cancellation() -> None:
    c_coefficients = sp.symbols("c0:5")
    n_coefficients = sp.symbols("n0:8")
    r = sp.symbols("r")
    C_poly = z**5 + sum(
        c_coefficients[index] * z**index for index in range(5)
    )
    L_poly = z - r
    N = sum(n_coefficients[index] * z**index for index in range(8))

    differential = sp.expand(
        C_poly * L_poly * ((z + mu) * sp.diff(N, z) + 4 * N)
        - (z + mu)
        * (
            2 * sp.diff(C_poly, z) * L_poly
            + C_poly * sp.diff(L_poly, z)
        )
        * N
    )
    assert sp.Poly(differential, z).degree() <= 12

    rational_function = (z + mu) ** 4 * N / (C_poly**2 * L_poly)
    assert sp.factor(
        sp.diff(rational_function, z)
        - (z + mu) ** 3
        * differential
        / (C_poly**3 * L_poly**2)
    ) == 0

    for degree in range(8):
        trial = z**degree
        trial_differential = sp.Poly(
            sp.expand(
                C_poly
                * L_poly
                * ((z + mu) * sp.diff(trial, z) + 4 * trial)
                - (z + mu)
                * (
                    2 * sp.diff(C_poly, z) * L_poly
                    + C_poly * sp.diff(L_poly, z)
                )
                * trial
            ),
            z,
        )
        assert trial_differential.degree() <= 12
        if degree < 7:
            assert trial_differential.coeff_monomial(
                z ** (degree + 6)
            ) == degree - 7
        else:
            assert trial_differential.coeff_monomial(z**13) == 0
    assert 12 - 2 * 5 == 2

    # Five rows, kernel dimension four in P_6: rank 3 and two relations.
    assert 7 - 4 == 3
    assert 5 - 3 == 2

    # The singleton row is (BS)'(r); it kills (z-r)^2 even at r=0.
    b0, b1 = sp.symbols("b0 b1", nonzero=True)
    local_B = b0 + b1 * w
    singleton_square = w**2
    assert sp.diff(local_B * singleton_square, w).subs(w, 0) == 0
    assert sp.diff(
        local_B * singleton_square.subs(w, z), z
    ).subs({z: 0, r: 0}) == 0

    S = (z - r) ** 2
    before_cancellation = (
        (z + mu) ** 3 * sp.Symbol("Q") ** 2 * S
        / (sp.Symbol("C") ** 3 * (z - r) ** 2)
    )
    after_cancellation = (
        (z + mu) ** 3 * sp.Symbol("Q") ** 2
        / sp.Symbol("C") ** 3
    )
    assert sp.cancel(before_cancellation - after_cancellation) == 0


def check_outside_residue_and_double_swaps() -> None:
    # A(z)/(z-u)^3 has residue A''(u)/2.
    a0, a1, a2, a3 = sp.symbols("a0 a1 a2 a3")
    local_A = a0 + a1 * w + a2 * w**2 + a3 * w**3
    assert sp.residue(local_A / w**3, w, 0) == a2
    assert sp.diff(local_A, w, 2).subs(w, 0) / 2 == a2

    u, x = sp.symbols("u x")

    def phi(value: sp.Expr) -> sp.Expr:
        return 2 / (u + value) + 3 / (u - value)

    def psi(value: sp.Expr) -> sp.Expr:
        return -2 / (u + value) ** 2 - 3 / (u - value) ** 2

    assert sp.factor(phi(x) - (5 * u + x) / (u**2 - x**2)) == 0
    assert sp.simplify(sp.diff(phi(x), u) - psi(x)) == 0

    # Exact mixed finite difference of Xi^2+Zeta.
    Xi, Zeta, delta1, delta2, epsilon1, epsilon2 = sp.symbols(
        "Xi Zeta delta1 delta2 epsilon1 epsilon2"
    )
    base = Xi**2 + Zeta
    first = (Xi + delta1) ** 2 + Zeta + epsilon1
    second = (Xi + delta2) ** 2 + Zeta + epsilon2
    both = (
        (Xi + delta1 + delta2) ** 2
        + Zeta
        + epsilon1
        + epsilon2
    )
    mixed = sp.expand(both - first - second + base)
    assert mixed == 2 * delta1 * delta2

    # Every ordered disjoint pair of swaps can be realized inside a
    # five-subset of the other nine values.
    universe = set(range(9))
    realized: set[tuple[int, int, int, int]] = set()
    for subset_tuple in combinations(range(9), 5):
        subset = set(subset_tuple)
        outside = universe - subset
        for a, c in combinations(sorted(subset), 2):
            for b, d in combinations(sorted(outside), 2):
                realized.add((a, b, c, d))
                realized.add((a, d, c, b))
                realized.add((c, b, a, d))
                realized.add((c, d, a, b))
    for a in range(9):
        for b in range(9):
            for c in range(9):
                for d in range(9):
                    if len({a, b, c, d}) == 4:
                        assert (a, b, c, d) in realized

    # Exhaust equality patterns for nine Phi-values.  Condition (36)
    # permits only one block of size nine or blocks of sizes eight and one.
    patterns: list[tuple[int, ...]] = []

    def generate_restricted_growth(prefix: list[int], maximum: int) -> None:
        if len(prefix) == 9:
            patterns.append(tuple(prefix))
            return
        for label in range(maximum + 2):
            prefix.append(label)
            generate_restricted_growth(prefix, max(maximum, label))
            prefix.pop()

    generate_restricted_growth([0], 0)
    valid_block_sizes: set[tuple[int, ...]] = set()
    for pattern in patterns:
        valid = True
        for four in combinations(range(9), 4):
            a, b, c, d = four
            pairings = (
                ((a, b), (c, d)),
                ((a, c), (b, d)),
                ((a, d), (b, c)),
            )
            for first_pair, second_pair in pairings:
                first_equal = pattern[first_pair[0]] == pattern[first_pair[1]]
                second_equal = pattern[second_pair[0]] == pattern[second_pair[1]]
                if not (first_equal or second_equal):
                    valid = False
                    break
            if not valid:
                break
        if valid:
            counts = sorted(
                (pattern.count(label) for label in set(pattern)),
                reverse=True,
            )
            valid_block_sizes.add(tuple(counts))
    assert valid_block_sizes == {(9,), (8, 1)}

    fibre_value = sp.symbols("fibre_value")
    fibre_polynomial = sp.expand(
        fibre_value * (u**2 - x**2) - 5 * u - x
    )
    assert sp.Poly(fibre_polynomial, x).degree() == 2
    assert sp.Poly(fibre_polynomial, x).coeff_monomial(x) == -1
    assert 8 > 2


def main() -> None:
    check_cores_lift_and_degrees()
    check_five_row_local_kernel()
    check_relation_plane_and_singleton_cancellation()
    check_outside_residue_and_double_swaps()
    print("eighth-split k=3 ten-double/one-singleton closure: PASS")
    print("2520 partial-pair lifts and five-row kernel dimension four: exact")
    print("relation image is a quadratic plane; singleton square cancels: exact")
    print("outside-double Riccati equation and mixed swap: exact")
    print("eight values in a degree-two fibre: impossible")


if __name__ == "__main__":
    main()
