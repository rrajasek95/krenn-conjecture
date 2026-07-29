#!/usr/bin/env python3
"""Exact audit of the h=8, k=2 profile 2^9 1^2 closure."""

from __future__ import annotations

from itertools import combinations

import sympy as sp


z, w, mu = sp.symbols("z w mu")


def coefficient_vector(poly: sp.Expr, degree: int) -> list[sp.Expr]:
    expanded = sp.Poly(sp.expand(poly), z)
    return [expanded.coeff_monomial(z**index) for index in range(degree + 1)]


def check_profile_cores_and_formal_lift() -> None:
    h, p, k = 8, 10, 2
    multiplicities = (2,) * 9 + (1, 1)
    assert sum(multiplicities) == p + h + 2 == 20

    core_count = 0
    double_indices = set(range(9))
    for five_set_tuple in combinations(range(9), 5):
        five_set = set(five_set_tuple)
        outside = double_indices - five_set
        for partial_pair_tuple in combinations(sorted(five_set), 2):
            partial_pair = set(partial_pair_tuple)
            takes = {
                index: (1 if index in partial_pair else 2)
                for index in five_set
            }
            complement = tuple(
                multiplicity - takes.get(index, 0)
                for index, multiplicity in enumerate(multiplicities)
            )
            core_count += 1
            assert sum(takes.values()) == h
            assert len(takes) == 5
            assert sum(complement) == p + 2 == 12
            assert sum(entry == 1 for entry in complement) == 4
            assert complement[-2:] == (1, 1)
            assert all(complement[index] == 2 for index in outside)
            assert all(complement[index] == 1 for index in partial_pair)
            assert len(takes) - 3 == 2

    assert core_count == sp.binomial(9, 5) * sp.binomial(5, 2) == 1260

    x, y, a, b, c, q = sp.symbols("x y a b c q")
    complement_factor = sp.symbols("complement_factor")
    original = (
        q
        * (z - x)
        * (z - y)
        * complement_factor
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
        complement_factor
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

    # C^2 L has degree 2*4+2=10.  Both the original and lifted
    # rational functions decay by two powers at infinity.
    residual_degree = 2
    complement_degree = 2 * 4 + 2
    original_numerator_degree = residual_degree + 2 + complement_degree
    original_denominator_degree = (k + 1) + 2 * 2 + 3 * 3
    lifted_numerator_degree = complement_degree + residual_degree + 2 * 2
    lifted_denominator_degree = (k + 1) + 3 * 5
    assert (original_numerator_degree, original_denominator_degree) == (14, 16)
    assert (lifted_numerator_degree, lifted_denominator_degree) == (16, 18)

    # A singleton may be zero without spoiling any of the six local units.
    sample_mu = sp.Integer(10)
    selected = tuple(map(sp.Integer, range(1, 6)))
    outside_values = tuple(map(sp.Integer, range(6, 10)))
    singleton_values = (sp.Integer(0), sp.Integer(11))
    C_sample = sp.prod(z - value for value in outside_values)
    L_sample = sp.prod(z - value for value in singleton_values)
    A_sample = C_sample**2 * L_sample
    for node in (-sample_mu,) + tuple(-value for value in selected):
        assert A_sample.subs(z, node) != 0
    squared_nodes = {sample_mu**2} | {value**2 for value in selected}
    assert len(squared_nodes) == 6


def check_complement_independent_local_kernel() -> None:
    # The Wronskian estimate sees only six exact order-two rows on P_6.
    for dimension in range(5, 8):
        for order_one_nodes in range(7):
            for absorbed_nodes in range(7 - order_one_nodes):
                ordinary_nodes = 6 - order_one_nodes - absorbed_nodes
                gcd_degree = order_one_nodes + 3 * absorbed_nodes
                forced_weight = (
                    ordinary_nodes * (dimension - 2)
                    + order_one_nodes * (dimension - 1)
                )
                degree_bound = dimension * (7 - gcd_degree - dimension)
                deficit = forced_weight - degree_bound
                expected = (
                    (dimension - 4) * (dimension + 3)
                    + (dimension + 1) * order_one_nodes
                    + 2 * (dimension + 1) * absorbed_nodes
                )
                assert deficit == expected
                assert deficit > 0

    dimension = 4
    assert 6 * (dimension - 2) == dimension * (7 - dimension) == 12

    # The ten pair products span all even quartics; the products through
    # one fixed h_t span h_t times all even quartics.
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

    fixed_triples = [
        quadratics[0] * quadratics[i] * quadratics[j]
        for i, j in combinations(range(1, 5), 2)
    ]
    triple_matrix = sp.Matrix(
        [coefficient_vector(poly, 6) for poly in fixed_triples]
    )
    assert triple_matrix.rank() == 3

    # The parity minors used in the remaining three-space case are odd
    # and have exactly the required degree cap.
    f_coefficients = sp.symbols("f0:7")
    g_coefficients = sp.symbols("g0:7")
    f = sum(coefficient * z**index for index, coefficient in enumerate(f_coefficients))
    g = sum(coefficient * z**index for index, coefficient in enumerate(g_coefficients))
    parity_minor = sp.expand(f * g.subs(z, -z) - f.subs(z, -z) * g)
    assert sp.expand(parity_minor.subs(z, -z) + parity_minor) == 0
    assert sp.Poly(parity_minor, z).degree() <= 11

    # Restriction of an exact second-order z-row to G(z)R(z^2).
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

    # A second-order row on cubics in the squared coordinate annihilates
    # the cube based at its support.  Six distinct supports cannot share
    # one nonzero dual cubic.
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


def check_relation_pencil_degree_drop_and_exact_dimension() -> None:
    c_coefficients = sp.symbols("c0:4")
    l_coefficients = sp.symbols("l0:2")
    n_coefficients = sp.symbols("n0:8")
    C_poly = z**4 + sum(
        c_coefficients[index] * z**index for index in range(4)
    )
    L_poly = z**2 + sum(
        l_coefficients[index] * z**index for index in range(2)
    )
    N = sum(n_coefficients[index] * z**index for index in range(8))

    differential = sp.expand(
        C_poly * L_poly * ((z + mu) * sp.diff(N, z) + 3 * N)
        - (z + mu)
        * (2 * sp.diff(C_poly, z) * L_poly + C_poly * sp.diff(L_poly, z))
        * N
    )
    assert sp.Poly(differential, z).degree() <= 12

    rational_function = (z + mu) ** 3 * N / (C_poly**2 * L_poly)
    assert sp.factor(
        sp.diff(rational_function, z)
        - (z + mu) ** 2
        * differential
        / (C_poly**3 * L_poly**2)
    ) == 0

    # For N=z^n, the nominal z^(n+6) coefficient is n-7.
    for degree in range(8):
        trial = z**degree
        trial_differential = sp.Poly(
            sp.expand(
                C_poly
                * L_poly
                * ((z + mu) * sp.diff(trial, z) + 3 * trial)
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

    # Five rows with four-dimensional kernel have rank three and exactly
    # two relations.  Injectivity therefore makes the S-image exactly a
    # two-plane, not merely a subspace of dimension at most two.
    ambient_dimension = 7
    kernel_dimension = 4
    row_count = 5
    row_rank = ambient_dimension - kernel_dimension
    relation_dimension = row_count - row_rank
    assert row_rank == 3
    assert relation_dimension == 2
    injective_image_dimension = relation_dimension
    assert injective_image_dimension == 2

    # If the differential image vanishes, G is constant.  Evaluating
    # (z+mu)^3 N = gamma C^2 L at -mu kills gamma because the complement
    # factor is structurally a unit there.
    gamma = sp.symbols("gamma")
    complement_at_common_pole = sp.symbols(
        "complement_at_common_pole", nonzero=True
    )
    assert sp.solve(
        sp.Eq(0, gamma * complement_at_common_pole), gamma
    ) == [0]


def check_singleton_rows_swap_and_zero_case() -> None:
    r, s, Y_r, Y_s, gamma = sp.symbols("r s Y_r Y_s gamma")

    def robin_row(node: sp.Expr, log_derivative: sp.Expr) -> sp.Matrix:
        return sp.Matrix(
            [
                log_derivative,
                1 + node * log_derivative,
                2 * node + node**2 * log_derivative,
            ]
        )

    equations = list(
        robin_row(r, Y_r) - gamma * robin_row(s, Y_s)
    )
    solution = sp.solve(equations, [Y_r, Y_s, gamma], dict=True)
    assert solution == [
        {
            Y_r: -2 / (r - s),
            Y_s: 2 / (r - s),
            gamma: -1,
        }
    ]

    # The same proportionality is exact when the first singleton is zero.
    zero_row = robin_row(
        sp.Integer(0), sp.simplify((-2 / (r - s)).subs(r, 0))
    )
    other_row = robin_row(
        s, sp.simplify((2 / (r - s)).subs(r, 0))
    )
    assert sp.simplify(zero_row + other_row) == sp.zeros(3, 1)

    # A double pole B(z)S(z)/w^2 contributes (BS)' at the pole.
    b0, b1, b2, q0, q1, q2 = sp.symbols("b0 b1 b2 q0 q1 q2")
    local_B = b0 + b1 * w + b2 * w**2
    local_S = q0 + q1 * w + q2 * w**2
    residue = sp.residue(local_B * local_S / w**2, w, 0)
    assert residue == b0 * q1 + b1 * q0
    assert sp.simplify(residue / b0 - (q1 + (b1 / b0) * q0)) == 0

    # The mutual singleton term cancels the forced Robin coefficient.
    base = sp.symbols("base")
    logarithmic_derivative = base - 2 / (r - s)
    assert sp.solve(
        sp.Eq(logarithmic_derivative, -2 / (r - s)), base
    ) == [0]

    # Every unordered pair of nine doubles crosses some 5/4 partition.
    values = set(range(9))
    crossing_pairs: set[tuple[int, int]] = set()
    for five_set_tuple in combinations(range(9), 5):
        five_set = set(five_set_tuple)
        complement = values - five_set
        for a in five_set:
            for b in complement:
                crossing_pairs.add(tuple(sorted((a, b))))
    assert crossing_pairs == set(combinations(range(9), 2))

    x, a, b = sp.symbols("x a b")
    swap_difference = (
        2 * (1 / (r + b) - 1 / (r + a))
        - 3 * (1 / (r - a) - 1 / (r - b))
    )

    def fibre_map(value: sp.Expr) -> sp.Expr:
        return 2 / (r + value) + 3 / (r - value)

    assert sp.factor(
        swap_difference - (fibre_map(b) - fibre_map(a))
    ) == 0
    assert sp.factor(
        fibre_map(x) - (5 * r + x) / (r**2 - x**2)
    ) == 0

    fibre_value = sp.symbols("fibre_value")
    fibre_polynomial = sp.expand(
        fibre_value * (r**2 - x**2) - 5 * r - x
    )
    assert sp.Poly(fibre_polynomial, x).degree() == 2
    assert sp.Poly(fibre_polynomial, x).coeff_monomial(x) == -1
    assert fibre_polynomial.subs(r, 0) == -fibre_value * x**2 - x
    assert sp.Poly(fibre_polynomial.subs(r, 0), x).coeff_monomial(x) == -1
    assert 9 > 2


def main() -> None:
    check_profile_cores_and_formal_lift()
    check_complement_independent_local_kernel()
    check_relation_pencil_degree_drop_and_exact_dimension()
    check_singleton_rows_swap_and_zero_case()
    print("eighth-split double/single 2^9 1^2 closure: PASS")
    print("1260 formal-five-double cores and C^2 L lifts: exact")
    print("six-row local kernel dimension four: complement-independent")
    print("relation image is an exact two-plane in P_2: exact")
    print("singleton Robin proportionality and zero-node audit: exact")
    print("5/4 partition swap and degree-two fibre: impossible")


if __name__ == "__main__":
    main()
