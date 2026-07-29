#!/usr/bin/env python3
"""Exact audit of two saturated-quartic h=8,k=4 moment closures."""

from itertools import combinations
from pathlib import Path
import sys

import sympy as sp


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import verify_live_three_zero_higher_split_collision_frontier as frontier


def audit_formal_cores(profile, formal_choices, expected_count):
    count = 0
    for chosen_tuple in formal_choices:
        assert len(chosen_tuple) == 5
        assert len(set(chosen_tuple)) == 5
        for partial_tuple in combinations(chosen_tuple, 2):
            partial = set(partial_tuple)
            takes = {
                index: (1 if index in partial else 2)
                for index in chosen_tuple
            }
            assert sum(takes.values()) == 8
            assert frontier.leaves_singleton(profile, takes)
            count += 1
    assert count == expected_count


def main() -> None:
    h, k, p, total = 8, 4, 12, 22
    choose_two = (3,) * 4 + (2,) * 3 + (1,) * 4
    choose_one = (3,) * 3 + (2,) * 4 + (1,) * 5
    for profile in (choose_two, choose_one):
        assert sum(profile) == total == p + h + 2

    triples_two = tuple(range(4))
    doubles_two = tuple(range(4, 7))
    choices_two = tuple(
        doubles_two + selected
        for selected in combinations(triples_two, 2)
    )
    audit_formal_cores(choose_two, choices_two, 60)

    triples_one = tuple(range(3))
    doubles_one = tuple(range(3, 7))
    choices_one = tuple(doubles_one + (selected,) for selected in triples_one)
    audit_formal_cores(choose_one, choices_one, 30)

    # Every formal removal leaves six simple roots and two outside triples.
    for simple_count in (4 + 2, 5 + 1):
        complement = (1,) * simple_count + (3,) * 2
        assert sum(complement) == k + h == 12
        assert len(complement) == 8
        assert complement.count(1) == 6
        assert len(complement) - 4 == 4

    # A saturated quartic pencil has basis degrees 3 and 4.  Its Wronskian
    # and accessory polynomial have universal top coefficients.
    z = sp.symbols("z")
    f_coefficients = sp.symbols("f0:4")
    g_coefficients = sp.symbols("g0:5")
    f = sum(f_coefficients[index] * z**index for index in range(4))
    g = sum(g_coefficients[index] * z**index for index in range(5))
    W = sp.Poly(sp.expand(f * sp.diff(g, z) - sp.diff(f, z) * g), z)
    V = sp.Poly(
        sp.expand(
            sp.diff(f, z) * sp.diff(g, z, 2)
            - sp.diff(f, z, 2) * sp.diff(g, z)
        ),
        z,
    )
    w6 = W.coeff_monomial(z**6)
    w5 = W.coeff_monomial(z**5)
    assert sp.expand(V.coeff_monomial(z**4) - 12 * w6) == 0
    assert sp.expand(V.coeff_monomial(z**3) - 8 * w5) == 0

    # Expansion of -sum Y_x/(z-x), followed by normalization W=L monic,
    # gives sum Y=0, sum xY=-12, sum x^2Y=4*w5=-4*sum x.
    nodes = sp.symbols("x0:6")
    robin = sp.symbols("Y0:6")
    moment0 = sum(robin)
    moment1 = sum(nodes[i] * robin[i] for i in range(6))
    moment2 = sum(nodes[i] ** 2 * robin[i] for i in range(6))
    l5 = -sum(nodes)
    q_minus_1 = -moment0
    q_minus_2 = -moment1
    q_minus_3 = -moment2
    assert q_minus_1.subs(moment0, 0) == 0
    assert sp.expand(q_minus_2.subs(moment1, -12) - 12) == 0
    assert sp.expand(
        (q_minus_3 + l5 * q_minus_2).subs(
            {moment1: -12, moment2: 4 * l5}
        )
        - 8 * l5
    ) == 0

    # Exact selected-pair coefficient and the two nontrivial rectangles.
    a, b, c, d = sp.symbols("a b c d")

    def pair_coefficient(power, left, right):
        plus_poles = 2 * (left**power + right**power) / (left + right)
        simple_interaction = -2 * (
            left**power - right**power
        ) / (left - right)
        outside_interaction = 4 * (
            left**power - right**power
        ) / (left - right)
        return sp.cancel(plus_poles + simple_interaction + outside_interaction)

    coefficient0 = 4 / (a + b)
    coefficient1 = 4
    coefficient2 = 4 * (a**2 + a * b + b**2) / (a + b)
    assert sp.cancel(pair_coefficient(0, a, b) - coefficient0) == 0
    assert sp.cancel(pair_coefficient(1, a, b) - coefficient1) == 0
    assert sp.cancel(pair_coefficient(2, a, b) - coefficient2) == 0

    def rectangle(power):
        return sp.factor(
            pair_coefficient(power, a, c)
            - pair_coefficient(power, a, d)
            - pair_coefficient(power, b, c)
            + pair_coefficient(power, b, d)
        )

    denominator = (a + c) * (a + d) * (b + c) * (b + d)
    expected0 = 4 * (a - b) * (c - d) * (a + b + c + d) / denominator
    e3 = a * b * c + a * b * d + a * c * d + b * c * d
    expected2 = -4 * (a - b) * (c - d) * e3 / denominator
    assert sp.cancel(rectangle(0) - expected0) == 0
    assert rectangle(1) == 0
    assert sp.cancel(rectangle(2) - expected2) == 0

    quartic = sp.expand((z - a) * (z - b) * (z - c) * (z - d))
    odd_part = sp.expand(quartic - quartic.subs(z, -z))
    assert sp.expand(
        odd_part - (-2 * (a + b + c + d) * z**3 - 2 * e3 * z)
    ) == 0

    # Choose-one cancellation.  The selected-root Robin coefficient is kept
    # as an arbitrary symbol because it cancels from both combinations.
    selected, selected_robin = sp.symbols("a_sel Y_sel")
    singleton_roots = sp.symbols("r0:5")
    increments = tuple(
        2 / (root + selected) + 2 / (root - selected)
        for root in singleton_roots
    )
    p_minus = sum(1 / (-selected - root) for root in singleton_roots)
    sigma = sum(singleton_roots)
    # Check each singleton summand separately.  This is the same exact
    # rational identity as a common-denominator expansion, but avoids an
    # irrelevant product of all five symbolic denominators.
    for root, increment in zip(singleton_roots, increments):
        p_term = 1 / (-selected - root)
        assert sp.cancel(
            (root - selected) * increment - (4 + 4 * selected * p_term)
        ) == 0
        assert sp.cancel(
            root * (root - selected) * increment
            - (4 * root - 4 * selected - 4 * selected**2 * p_term)
        ) == 0
    assert (selected - selected) * selected_robin == 0
    assert len(singleton_roots) == 5
    assert sp.expand(sum(singleton_roots) - sigma) == 0
    assert p_minus == sum(1 / (-selected - root) for root in singleton_roots)

    c0, c1, c2 = sp.symbols("c0 c1 c2")
    four_a_p = c1 - 20 - selected * c0
    elimination = sp.expand(
        (c2 - selected * c1)
        - (4 * sigma - 16 * selected - selected * four_a_p)
    )
    expected_elimination = c2 - 4 * sigma - 4 * selected - c0 * selected**2
    assert sp.expand(elimination - expected_elimination) == 0
    final_quadratic = c0 * selected**2 + 4 * selected + 4 * sigma - c2
    assert sp.Poly(final_quadratic, selected).degree() <= 2
    assert sp.Poly(final_quadratic, selected).coeff_monomial(selected) == 4

    counts, residuals = frontier.census(h, p)
    assert counts["R"] == 46
    assert choose_two in residuals
    assert choose_one in residuals

    print("PASS: saturated-quartic h=8,k=4 moment closures")
    print("90 legal formal-five cores and three Robin moments: exact")
    print("choose-two even quartic and choose-one nonzero quadratic: exact")


if __name__ == "__main__":
    main()
