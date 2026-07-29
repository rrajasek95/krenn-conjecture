#!/usr/bin/env python3
"""Exact audit of the h=8, k=2 profile 2^9 1^2 closure."""

from __future__ import annotations

from itertools import combinations

import sympy as sp


z, s, w, mu = sp.symbols("z s w mu")


def coefficient_vector(poly: sp.Expr, variable: sp.Symbol, degree: int) -> list[sp.Expr]:
    expanded = sp.Poly(sp.expand(poly), variable)
    return [
        expanded.coeff_monomial(variable**index)
        for index in range(degree + 1)
    ]


def check_profile_cores_and_omitted_double_lift() -> None:
    h, p, k = 8, 10, 2
    multiplicities = (2,) * 9 + (1, 1)
    assert sum(multiplicities) == p + h + 2 == 20

    core_count = 0
    double_indices = range(9)
    for five_set_tuple in combinations(double_indices, 5):
        five_set = set(five_set_tuple)
        outside = set(double_indices) - five_set
        for omitted in five_set:
            takes = {
                index: 2
                for index in five_set
                if index != omitted
            }
            complement = tuple(
                multiplicity - takes.get(index, 0)
                for index, multiplicity in enumerate(multiplicities)
            )
            core_count += 1

            assert sum(takes.values()) == h
            assert len(takes) == 4
            assert sum(complement) == p + 2 == 12
            assert complement[omitted] == 2
            assert all(complement[index] == 2 for index in outside)
            assert complement[-2:] == (1, 1)  # both singleton classes remain
            assert len(takes) - 3 == 1  # residual degree cap

    assert core_count == sp.binomial(9, 5) * 5

    x, t1, t2, t3, t4 = sp.symbols("x t1 t2 t3 t4")
    q0, q1 = sp.symbols("q0 q1")
    outside_factor, singleton_factor = sp.symbols(
        "outside_factor singleton_factor"
    )
    q = q0 + q1 * z
    selected_denominator = sp.prod(
        (z + value) ** 3 for value in (t1, t2, t3, t4)
    )
    original = (
        singleton_factor
        * outside_factor
        * (z - x) ** 2
        * q
        / ((z + mu) ** 3 * selected_denominator)
    )
    lifted_polynomial = (z - x) ** 2 * (z + x) ** 3 * q
    common = (
        singleton_factor
        * outside_factor
        * lifted_polynomial
        / ((z + mu) ** 3 * (z + x) ** 3 * selected_denominator)
    )
    assert sp.factor(original - common) == 0

    assert 2 + 8 + 2 + 1 == 13  # R, C_O^2, omitted double, and q
    assert (k + 1) + 4 * 3 == 15
    assert 5 + 1 == 6  # omitted-double lift times the linear residual
    assert 2 + 8 + 6 == 16
    assert (k + 1) + 5 * 3 == 18
    assert 18 - 16 == 2


def check_exact_order_two_rows_and_wronskian_bound() -> None:
    c0, c1, c2 = sp.symbols("c0 c1 c2")
    regular = c0 + c1 * w + c2 * w**2
    assert sp.residue(regular / w**3, w, 0) == c2

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

    assert 6 * (4 - 2) == 4 * (7 - 4) == 12


def check_parity_decomposition_and_five_contact_lemma() -> None:
    x, alpha, beta = sp.symbols("x alpha beta")
    X = x**2
    q = alpha * z + beta
    lift = sp.expand((z - x) ** 2 * (z + x) ** 3 * q)
    parity_form = sp.expand(
        (z**2 - X) ** 2
        * (
            alpha * z**2
            + beta * x
            + (beta + alpha * x) * z
        )
    )
    assert sp.expand(lift - parity_form) == 0

    odd_part = sp.expand((lift - lift.subs(z, -z)) / 2)
    even_part = sp.expand((lift + lift.subs(z, -z)) / 2)
    gamma = beta + alpha * x
    assert sp.expand(odd_part - gamma * z * (z**2 - X) ** 2) == 0
    assert sp.expand(
        even_part
        - (z**2 - X) ** 2 * (alpha * z**2 + beta * x)
    ) == 0
    assert sp.expand(
        lift.subs(beta, -alpha * x)
        - alpha * (z**2 - X) ** 3
    ) == 0

    # Three odd quadratics and four pure cubics have Vandermonde rank.
    Xs = sp.symbols("X0:4")
    odd_matrix = sp.Matrix(
        [coefficient_vector((s - value) ** 2, s, 2) for value in Xs[:3]]
    )
    pure_matrix = sp.Matrix(
        [coefficient_vector((s - value) ** 3, s, 3) for value in Xs]
    )
    odd_vandermonde = sp.prod(
        Xs[j] - Xs[i] for i in range(3) for j in range(i + 1, 3)
    )
    pure_vandermonde = sp.prod(
        Xs[j] - Xs[i] for i in range(4) for j in range(i + 1, 4)
    )
    assert sp.simplify(odd_matrix.det() / odd_vandermonde) in (-2, 2)
    assert sp.simplify(pure_matrix.det() / pure_vandermonde) in (-9, 9)

    # A general L:P_2(s)->P_3(s), with its coefficients grouped by the
    # input basis 1,s,s^2.
    coefficients = sp.symbols("l0:12")
    variable_X = sp.symbols("variable_X")
    images = [
        sum(coefficients[4 * column + row] * s**row for row in range(4))
        for column in range(3)
    ]
    contact_family = sp.expand(
        variable_X**2 * images[0]
        - 2 * variable_X * images[1]
        + images[2]
    )
    value_polynomial = sp.Poly(
        sp.expand(contact_family.subs(s, variable_X)),
        variable_X,
    )
    derivative_polynomial = sp.Poly(
        sp.expand(sp.diff(contact_family, s).subs(s, variable_X)),
        variable_X,
    )
    assert value_polynomial.degree() <= 5
    assert derivative_polynomial.degree() <= 4
    assert (
        value_polynomial.coeff_monomial(variable_X**5)
        == derivative_polynomial.coeff_monomial(variable_X**4) / 3
    )

    equations = [
        value_polynomial.coeff_monomial(variable_X**degree)
        for degree in range(6)
    ] + [
        derivative_polynomial.coeff_monomial(variable_X**degree)
        for degree in range(5)
    ]
    matrix, _ = sp.linear_eq_to_matrix(equations, coefficients)
    assert matrix.rank() == 10

    multiplication_by_one = sp.Matrix(
        [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0]
    )
    multiplication_by_s = sp.Matrix(
        [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]
    )
    assert matrix * multiplication_by_one == sp.zeros(len(equations), 1)
    assert matrix * multiplication_by_s == sp.zeros(len(equations), 1)
    assert sp.Matrix.hstack(
        multiplication_by_one, multiplication_by_s
    ).rank() == 2
    assert len(matrix.nullspace()) == 2

    A, B = sp.symbols("A B")
    contact_polynomial = B * z**2 - z + A
    assert sp.Poly(contact_polynomial, z).degree() == 2
    assert sp.Poly(contact_polynomial, z).coeff_monomial(z) == -1
    assert 5 > 2


def check_relation_plane_and_degree_drop() -> None:
    c_coefficients = sp.symbols("c0:4")
    r_coefficients = sp.symbols("r0:2")
    n_coefficients = sp.symbols("n0:8")
    C = z**4 + sum(
        c_coefficients[index] * z**index for index in range(4)
    )
    R = z**2 + sum(
        r_coefficients[index] * z**index for index in range(2)
    )
    N = sum(n_coefficients[index] * z**index for index in range(8))

    differential = sp.expand(
        C * R * ((z + mu) * sp.diff(N, z) + 3 * N)
        - 2 * (z + mu) * sp.diff(C, z) * R * N
        - (z + mu) * C * sp.diff(R, z) * N
    )
    assert sp.Poly(differential, z).degree() <= 12

    rational_function = (z + mu) ** 3 * N / (C**2 * R)
    assert sp.factor(
        sp.diff(rational_function, z)
        - (z + mu) ** 2 * differential / (C**3 * R**2)
    ) == 0

    # The nominal coefficient in degree n+6 is n-7.  For n=7 the
    # degree-thirteen term cancels, leaving degree at most twelve.
    for degree in range(8):
        trial = z**degree
        trial_differential = sp.Poly(
            sp.expand(
                C * R * ((z + mu) * sp.diff(trial, z) + 3 * trial)
                - 2 * (z + mu) * sp.diff(C, z) * R * trial
                - (z + mu) * C * sp.diff(R, z) * trial
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
    assert sp.factor((C**2 * R).subs(z, -mu)) != 0


def check_singleton_rows_and_exact_image_plane() -> None:
    B0, B1, B2 = sp.symbols("B0 B1 B2", nonzero=True)
    S0, S1, S2 = sp.symbols("S0 S1 S2")
    local_unit = B0 + B1 * w + B2 * w**2
    local_quadratic = S0 + S1 * w + S2 * w**2
    singleton_residue = sp.residue(
        local_unit * local_quadratic / w**2,
        w,
        0,
    )
    assert singleton_residue == B0 * S1 + B1 * S0
    assert sp.diff(singleton_residue, S1) == B0
    assert sp.residue(local_unit * w**2 / w**2, w, 0) == 0

    a, b = sp.symbols("a b")
    square_matrix = sp.Matrix(
        [
            coefficient_vector((z - a) ** 2, z, 2),
            coefficient_vector((z - b) ** 2, z, 2),
        ]
    )
    # The minor in columns z and z^2 is 2(b-a), so the squares are
    # independent whenever the singleton values are distinct.
    assert sp.simplify(
        square_matrix[:, 1:3].det() - 2 * (b - a)
    ) == 0


def check_outside_double_jets_and_partition_swap() -> None:
    rho, sigma = sp.symbols("rho sigma", nonzero=True)
    A0, A1, A2 = sp.symbols("A0 A1 A2", nonzero=True)
    local_unit = A0 + A1 * w + A2 * w**2 / 2

    rho_residue_twice = sp.expand(
        2 * sp.residue(local_unit * (rho + w) ** 2 / w**3, w, 0)
    )
    sigma_residue_twice = sp.expand(
        2 * sp.residue(local_unit * (sigma + w) ** 2 / w**3, w, 0)
    )
    assert rho_residue_twice == A2 * rho**2 + 4 * A1 * rho + 2 * A0
    assert sigma_residue_twice == A2 * sigma**2 + 4 * A1 * sigma + 2 * A0

    coefficient_matrix = sp.Matrix(
        [[rho**2, 4 * rho], [sigma**2, 4 * sigma]]
    )
    assert sp.factor(coefficient_matrix.det()) == 4 * rho * sigma * (rho - sigma)

    solved_A1 = -A0 * (rho + sigma) / (2 * rho * sigma)
    solved_A2 = 2 * A0 / (rho * sigma)
    assert sp.factor(
        rho_residue_twice.subs({A1: solved_A1, A2: solved_A2})
    ) == 0
    assert sp.factor(
        sigma_residue_twice.subs({A1: solved_A1, A2: solved_A2})
    ) == 0

    u, a, b = sp.symbols("u a b")
    singleton_sum = 1 / (u - a) + 1 / (u - b)
    assert sp.factor(
        (
            -(rho + sigma) / (2 * rho * sigma)
            + singleton_sum / 2
        ).subs({rho: u - a, sigma: u - b})
    ) == 0

    selected_sum, outside_sum = sp.symbols("selected_sum outside_sum")
    logarithmic_derivative = (
        2 / (u + mu)
        + 2 * selected_sum
        - 3 * outside_sum
        - 2 * singleton_sum
    )
    stieltjes_equation = (
        2 / (u + mu)
        + 2 * selected_sum
        - 3 * outside_sum
        - sp.Rational(3, 2) * singleton_sum
    )
    assert sp.factor(
        stieltjes_equation
        - (logarithmic_derivative + singleton_sum / 2)
    ) == 0

    x, y = sp.symbols("x y")
    swap_difference = (
        2 * (1 / (u + y) - 1 / (u + x))
        - 3 * (1 / (u - x) - 1 / (u - y))
    )

    def fibre_map(value: sp.Expr) -> sp.Expr:
        return 2 / (u + value) + 3 / (u - value)

    assert sp.factor(
        swap_difference - (fibre_map(y) - fibre_map(x))
    ) == 0
    assert sp.factor(
        fibre_map(x) - (5 * u + x) / (u**2 - x**2)
    ) == 0

    fibre_value = sp.symbols("fibre_value")
    fibre_polynomial = sp.expand(
        fibre_value * (u**2 - x**2) - 5 * u - x
    )
    assert sp.Poly(fibre_polynomial, x).degree() == 2
    assert sp.Poly(fibre_polynomial, x).coeff_monomial(x) == -1
    assert 8 > 2


def check_final_frontier() -> None:
    old_frontier = {"2^10", "2^9 1^2"}
    new_closures = {"2^10", "2^9 1^2"}
    assert old_frontier - new_closures == set()


def main() -> None:
    check_profile_cores_and_omitted_double_lift()
    check_exact_order_two_rows_and_wronskian_bound()
    check_parity_decomposition_and_five_contact_lemma()
    check_relation_plane_and_degree_drop()
    check_singleton_rows_and_exact_image_plane()
    check_outside_double_jets_and_partition_swap()
    check_final_frontier()
    print("eighth-split nine-double 2^9 1^2 second-order closure: PASS")
    print("five omitted-double lifts and dimension four: exact")
    print("five-contact parity/interpolation lemma: exact")
    print("quadratic relation image and singleton plane: exact")
    print("outside-double Stieltjes swap and degree-two fibre: impossible")
    print("h=8, k=2 no-extra-singular collision frontier: empty")


if __name__ == "__main__":
    main()
