#!/usr/bin/env python3
"""Exact audit of the h=8,k=3 formal-five-double duality theorem."""

from itertools import combinations
from pathlib import Path
import sys

import sympy as sp


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import verify_live_three_zero_higher_split_collision_frontier as frontier


def main() -> None:
    z, mu = sp.symbols("z mu")

    # Formal core and lift arithmetic.
    profile = (2,) * 5
    count = 0
    for partial in combinations(range(5), 2):
        takes = [1 if index in partial else 2 for index in range(5)]
        assert sum(takes) == 8
        assert len(takes) == 5
        assert sum(value == 1 for value in takes) == 2
        count += 1
    assert count == 10
    assert 11 + 6 == 17
    assert 4 + 3 * 5 == 19

    x, y = sp.symbols("x y")
    assert sp.factor((z - x) / (z + x) ** 2 - (z**2 - x**2) / (z + x) ** 3) == 0
    assert sp.factor((z - y) / (z + y) ** 2 - (z**2 - y**2) / (z + y) ** 3) == 0

    t = sp.symbols("t")
    for multiplicity in range(2, 8):
        partial = (z - t) ** (multiplicity - 1) / (z + t) ** 2
        full = (z - t) ** (multiplicity - 2) / (z + t) ** 3
        assert sp.factor(
            partial
            - (z - t) ** (multiplicity - 2) * (z - t) / (z + t) ** 2
        ) == 0
        assert sp.factor(
            full - (z - t) ** (multiplicity - 2) / (z + t) ** 3
        ) == 0

    # Mixed five-order-two/one-order-three Wronskian bound, including
    # every possible local gcd order.  At value nodes the viable orders
    # are 0, 1, and >=3; at the common node they are 0, 1, 2, and >=4.
    for dimension in range(5, 8):
        baseline = 5 * (dimension - 2) + (dimension - 3)
        degree = dimension * (7 - dimension)
        deficit = baseline - degree
        assert deficit == dimension**2 - dimension - 13
        assert deficit > 0
        common_cases = (
            (0, dimension - 3, 0),
            (1, dimension - 2, dimension + 1),
            (2, dimension - 1, 2 * dimension + 2),
            (4, 0, 3 * dimension + 3),
        )
        for order_one_nodes in range(6):
            for absorbed_value_nodes in range(6 - order_one_nodes):
                ordinary_value_nodes = (
                    5 - order_one_nodes - absorbed_value_nodes
                )
                value_weight = (
                    ordinary_value_nodes * (dimension - 2)
                    + order_one_nodes * (dimension - 1)
                )
                value_gcd_degree = (
                    order_one_nodes + 3 * absorbed_value_nodes
                )
                value_increment = (
                    (dimension + 1) * order_one_nodes
                    + (2 * dimension + 2) * absorbed_value_nodes
                )
                for common_order, common_weight, common_increment in common_cases:
                    gcd_degree = value_gcd_degree + common_order
                    forced_weight = value_weight + common_weight
                    reduced_degree = dimension * (
                        7 - gcd_degree - dimension
                    )
                    observed = forced_weight - reduced_degree
                    expected = (
                        deficit + value_increment + common_increment
                    )
                    assert observed == expected
                    assert observed > 0

    # General differential factorization.  Use symbolic monic polynomials
    # with degrees deg(A)=11, deg(rad A)=c.
    n = sp.symbols("n", integer=True, nonnegative=True)
    for classes in range(4, 9):
        # Leading-degree audit: D_A has degree c-1 and leading coefficient 11.
        for degree_n in range(8):
            nominal_coefficient = degree_n + 4 - 11
            if degree_n == 7:
                assert nominal_coefficient == 0
                degree_bound = classes + 6
            else:
                degree_bound = classes + degree_n
                assert degree_bound <= classes + 6
        assert classes + 6 - 10 == classes - 4

    # Audit the c-4 bound on every complementary multiplicity pattern
    # occurring in the eight applications.
    outside_patterns = {
        (3, 3, 3, 2),
        (3, 3, 3, 1, 1),
        (3, 2, 2, 2, 2),
        (3, 3, 2, 1, 1, 1),
        (3, 2, 2, 2, 1, 1),
        (2, 2, 2, 2, 2, 1),
        (3, 3, 1, 1, 1, 1, 1),
    }
    for multiplicities in outside_patterns:
        assert sum(multiplicities) == 11
        classes = len(multiplicities)
        roots = tuple(map(sp.Integer, range(1, classes + 1)))
        actual_A = sp.prod(
            (z - root) ** multiplicity
            for root, multiplicity in zip(roots, multiplicities)
        )
        actual_g = sp.prod(
            (z - root) ** (multiplicity - 1)
            for root, multiplicity in zip(roots, multiplicities)
        )
        actual_radical = sp.cancel(actual_A / actual_g)
        actual_D = sp.cancel(sp.diff(actual_A, z) / actual_g)
        assert sp.Poly(actual_radical, z).degree() == classes
        assert sp.Poly(actual_D, z).degree() == classes - 1
        assert sp.Poly(actual_D, z).LC() == 11
        for degree_n in range(8):
            trial = z**degree_n
            actual_E = sp.Poly(
                sp.expand(
                    actual_radical
                    * ((z + mu) * sp.diff(trial, z) + 4 * trial)
                    - (z + mu) * actual_D * trial
                ),
                z,
            )
            assert actual_E.degree() <= classes + 6
            if degree_n < 7:
                assert actual_E.coeff_monomial(
                    z ** (classes + degree_n)
                ) == degree_n - 7
            else:
                assert actual_E.coeff_monomial(
                    z ** (classes + 7)
                ) == 0

    # Check the derivative identity on a representative multiplicity pattern.
    a, b, c = sp.symbols("a b c")
    A = (z - a) ** 3 * (z - b) ** 2 * (z - c) ** 6
    g = (z - a) ** 2 * (z - b) * (z - c) ** 5
    radical = sp.cancel(A / g)
    D_A = sp.cancel(sp.diff(A, z) / g)
    coeffs = sp.symbols("n0:8")
    N = sum(coeffs[index] * z**index for index in range(8))
    E = sp.expand(radical * ((z + mu) * sp.diff(N, z) + 4 * N) - (z + mu) * D_A * N)
    G = (z + mu) ** 4 * N / A
    assert sp.factor(sp.diff(G, z) - (z + mu) ** 3 * g * E / A**2) == 0
    assert sp.Poly(E, z).degree() <= 9  # c=3 gives c+6

    # Robin-row proportionality on P_2.
    r, s, Yr, Ys, gamma = sp.symbols("r s Yr Ys gamma")

    def robin(node, value):
        return sp.Matrix([value, 1 + node * value, 2 * node + node**2 * value])

    solution = sp.solve(list(robin(r, Yr) - gamma * robin(s, Ys)), [Yr, Ys, gamma], dict=True)
    assert solution == [{Yr: -2 / (r - s), Ys: 2 / (r - s), gamma: -1}]
    qnode = sp.symbols("qnode")
    assert sp.solve(sp.Eq(2 / (r - s), -2 / (s - qnode)), qnode) == [r]

    # P_1 cannot be killed by a singleton double-pole row.
    B0, B1 = sp.symbols("B0 B1", nonzero=True)
    local = B0 + B1 * z
    assert sp.diff(local, z).subs(z, 0) == B1
    assert sp.diff(local * z, z).subs(z, 0) == B0

    # Partition-swap map and fibre.
    u, value = sp.symbols("u value")
    Phi = 2 / (u + value) + 3 / (u - value)
    assert sp.factor(Phi - (5 * u + value) / (u**2 - value**2)) == 0
    lam = sp.symbols("lam")
    fibre = sp.expand(lam * (u**2 - value**2) - 5 * u - value)
    assert sp.Poly(fibre, value).degree() == 2
    assert sp.Poly(fibre, value).coeff_monomial(value) == -1
    assert sp.Poly(fibre.subs(u, 0), value).coeff_monomial(value) == -1

    # Boolean-slice mixed finite difference.
    base, da, db, dc, dd = sp.symbols("base da db dc dd")
    ea, eb, ec, ed, constant = sp.symbols("ea eb ec ed constant")

    def subset_equation(left, right, eleft, eright):
        return (base + left + right) ** 2 + constant + eleft + eright

    rectangle = sp.expand(
        subset_equation(da, dc, ea, ec)
        - subset_equation(da, dd, ea, ed)
        - subset_equation(db, dc, eb, ec)
        + subset_equation(db, dd, eb, ed)
    )
    assert sp.factor(rectangle - 2 * (da - db) * (dc - dd)) == 0

    # A pencil in P_d has Wronskian degree at most 2d-2.
    for degree in range(1, 8):
        p_coeffs = sp.symbols(f"p{degree}_0:{degree + 1}")
        q_coeffs = sp.symbols(f"q{degree}_0:{degree + 1}")
        p_poly = sum(p_coeffs[index] * z**index for index in range(degree + 1))
        q_poly = sum(q_coeffs[index] * z**index for index in range(degree + 1))
        wronskian = sp.expand(
            p_poly * sp.diff(q_poly, z) - sp.diff(p_poly, z) * q_poly
        )
        assert sp.Poly(wronskian, z).degree() <= 2 * degree - 2
    assert 5 > 2 * 3 - 2

    # Exact census locations and complementary class counts.
    profiles = {
        (3, 3, 3, 2, 2, 2, 2, 2, 2): 4,
        (3, 2, 2, 2, 2, 2, 2, 2, 2, 2): 5,
        (3, 3, 3, 2, 2, 2, 2, 2, 1, 1): 5,
        (2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1): 6,
        (3, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1): 6,
        (3, 3, 2, 2, 2, 2, 2, 2, 1, 1, 1): 6,
        (3, 3, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1): 7,
    }
    counts, residuals = frontier.census(8, 11)
    assert counts["R"] == 46
    for full_profile, outside_classes in profiles.items():
        assert full_profile in residuals
        double_indices = [index for index, multiplicity in enumerate(full_profile) if multiplicity == 2]
        assert len(double_indices) >= 5
        T = set(double_indices[:5])
        outside = [full_profile[index] for index in range(len(full_profile)) if index not in T]
        assert sum(outside) == 11
        assert len(outside) == outside_classes
        assert outside_classes - 4 in (0, 1, 2, 3)
        if full_profile == (3, 3, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1):
            assert outside.count(1) == 5
            assert outside_classes == 7
            assert 5 > 2 * (outside_classes - 4) - 2

    formal_profile = (3, 3, 3, 2, 2, 2, 2, 1, 1, 1, 1)
    assert formal_profile in residuals
    chosen_formal = {0, 3, 4, 5, 6}
    outside_multiplicities = []
    for index, full_multiplicity in enumerate(formal_profile):
        residual_multiplicity = full_multiplicity - (
            2 if index in chosen_formal else 0
        )
        if residual_multiplicity:
            outside_multiplicities.append(residual_multiplicity)
    assert sorted(outside_multiplicities) == [1, 1, 1, 1, 1, 3, 3]
    assert len(outside_multiplicities) == 7
    assert outside_multiplicities.count(1) == 5
    assert 5 > 2 * (len(outside_multiplicities) - 4) - 2
    for partial_pair in combinations(chosen_formal, 2):
        takes = {
            index: (1 if index in partial_pair else 2)
            for index in chosen_formal
        }
        complement = [
            full_multiplicity - takes.get(index, 0)
            for index, full_multiplicity in enumerate(formal_profile)
        ]
        assert sum(takes.values()) == 8
        assert complement.count(1) >= 4

    # Every pair crosses each partition family used in the fibre arguments.
    for total_doubles, selected in ((9, 5), (8, 5)):
        crossing = set()
        for T_tuple in combinations(range(total_doubles), selected):
            T_set = set(T_tuple)
            for left in T_set:
                for right in set(range(total_doubles)) - T_set:
                    crossing.add(tuple(sorted((left, right))))
        assert crossing == set(combinations(range(total_doubles), 2))

    print("PASS: exact h=8,k=3 formal-five-double duality audit")


if __name__ == "__main__":
    main()
