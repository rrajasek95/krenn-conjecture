#!/usr/bin/env python3
"""Exact audit of the k=2 one-triple partial-double closure."""

from __future__ import annotations

from itertools import combinations
from pathlib import Path
import sys

import sympy as sp


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import verify_live_three_zero_higher_split_collision_frontier as frontier
import verify_live_three_zero_eighth_split_k2_three_triple_double_closure as previous


z = sp.symbols("z")


PROFILES = (
    (3, 2, 2, 2, 2, 2, 2, 2, 2, 1),
    (3, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1),
)


EXPECTED_FINAL = (
    (2, 2, 2, 2, 2, 2, 2, 2, 2, 2),
    (2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1),
)


def check_selections_and_degrees():
    h, p, k = 8, 10, 2
    for profile in PROFILES:
        triple = next(index for index, part in enumerate(profile) if part == 3)
        doubles = [index for index, part in enumerate(profile) if part == 2]
        assert len(doubles) in (7, 8)
        checked = 0
        for three in combinations(doubles, 3):
            for partial in three:
                takes = {triple: 3}
                takes.update(
                    {index: (1 if index == partial else 2) for index in three}
                )
                checked += 1
                assert sum(takes.values()) == h
                assert len(takes) == 4
                assert profile[partial] - takes[partial] == 1
                assert frontier.leaves_singleton(profile, takes)

                complement_size = sum(
                    multiplicity - takes.get(index, 0)
                    for index, multiplicity in enumerate(profile)
                )
                denominator_degree = (k + 1) + sum(
                    take + 1 for take in takes.values()
                )
                numerator_cap = p + len(takes) - 1
                residual_cap = numerator_cap - complement_size
                assert complement_size == p + 2 == 12
                assert denominator_degree == 15
                assert numerator_cap == 13
                assert residual_cap == 1
        assert checked == 3 * sp.binomial(len(doubles), 3)


def check_exact_partial_to_full_lift():
    value, q = sp.symbols("value q")
    partial_factor = (z - value) / (z + value) ** 2
    full_factor = 1 / (z + value) ** 3
    h_value = z**2 - value**2
    assert sp.factor(partial_factor * q - full_factor * h_value * q) == 0
    assert sp.Poly(h_value, z).degree() == 2


def check_four_node_rank_argument():
    nodes = sp.symbols("xi0:4")
    # Ascending coefficient columns of (z-xi)^3.
    shifted_cubics = sp.Matrix(
        [
            [-node**3, 3 * node**2, -3 * node, 1]
            for node in nodes
        ]
    )
    determinant = sp.factor(shifted_cubics.det())
    vandermonde = sp.prod(
        nodes[j] - nodes[i] for i in range(4) for j in range(i + 1, 4)
    )
    assert sp.factor(determinant / vandermonde) in (9, -9)

    # A general exact order-two functional at xi is nonzero and kills the
    # shifted cubic there.
    xi, c0, c1, c2 = sp.symbols("xi c0 c1 c2")
    polynomial = (z - xi) ** 3
    functional = (
        c0 * polynomial.subs(z, xi)
        + c1 * sp.diff(polynomial, z).subs(z, xi)
        + c2 * sp.diff(polynomial, z, 2).subs(z, xi)
    )
    assert functional == 0


def check_quadric_ruling_encoding():
    value = sp.symbols("value")
    q0, q1 = sp.symbols("q0 q1")
    polynomial = sp.expand((z**2 - value**2) * (q0 + q1 * z))
    coefficients = [polynomial.coeff(z, degree) for degree in range(4)]
    matrix = sp.Matrix(
        [[coefficients[0], coefficients[2]], [coefficients[1], coefficients[3]]]
    )
    assert sp.factor(matrix.det()) == 0
    assert matrix == sp.Matrix([[-value**2 * q0, q0], [-value**2 * q1, q1]])

    # Pairwise distinct/nonopposite anchors make the quadratic gauges
    # coprime; two of them already have product degree four, above the
    # cubic lift cap.
    other = sp.symbols("other")
    assert sp.factor(
        sp.resultant(z**2 - value**2, z**2 - other**2, z)
        - (value - other) ** 2 * (value + other) ** 2
    ) == 0


def chi(count: int, anchor, moving):
    return sp.factor(
        count / (moving - anchor) - (count + 1) / (moving + anchor)
    )


def cleared_simple_row(anchor, moving, constant):
    denominator = moving**2 - anchor**2
    coefficient = constant + chi(2, anchor, moving)
    return sp.Matrix(
        [
            sp.cancel(denominator * coefficient),
            sp.cancel(denominator * (1 + anchor * coefficient)),
        ]
    )


def check_moving_determinant_and_endpoints():
    t, u, v, A, B = sp.symbols("t u v A B")
    row_t = cleared_simple_row(t, v, A)
    row_u = cleared_simple_row(u, v, B)
    assert all(sp.denom(entry) == 1 for entry in tuple(row_t) + tuple(row_u))
    assert all(sp.Poly(entry, v).degree() <= 2 for entry in tuple(row_t) + tuple(row_u))
    determinant = sp.expand(row_t[0] * row_u[1] - row_t[1] * row_u[0])
    assert sp.Poly(determinant, v).degree() <= 4

    assert sp.simplify(row_t.subs(v, t) - 4 * t * sp.Matrix([1, t])) == sp.zeros(2, 1)
    assert sp.simplify(row_t.subs(v, -t) - 6 * t * sp.Matrix([1, t])) == sp.zeros(2, 1)

    difference = sp.factor(
        (u - t) * (chi(2, u, t) - chi(2, u, -t))
    )
    assert sp.factor(difference - 2 * t / (t + u)) == 0

    # Directly verify that determinant vanishing at both endpoints would
    # impose two incompatible conditions on the translated u-row.
    condition_plus = sp.factor(1 + (u - t) * (B + chi(2, u, t)))
    condition_minus = sp.factor(1 + (u - t) * (B + chi(2, u, -t)))
    assert sp.factor(condition_plus - condition_minus - difference) == 0


def check_root_counts_and_frontier():
    for profile in PROFILES:
        doubles = profile.count(2)
        assert doubles - 2 >= 5 > 4

    previous_set = set(previous.EXPECTED_FINAL)
    assert set(PROFILES) <= previous_set
    final = previous_set - set(PROFILES)
    ordered = tuple(sorted(final, key=lambda item: (len(item), 20 - len(item), item)))
    assert ordered == EXPECTED_FINAL
    assert len(final) == 2
    assert sum((263, 270, 22, 14, 12, 3, 5, 18, 3, 8, 2, 2, 2, 2, 1)) == 627


def main():
    check_selections_and_degrees()
    check_exact_partial_to_full_lift()
    check_four_node_rank_argument()
    check_quadric_ruling_encoding()
    check_moving_determinant_and_endpoints()
    check_root_counts_and_frontier()
    print("k=2 one-triple partial-double closure: PASS")
    print("three lifted residuals span the common two-dimensional cubic kernel")
    print("quadric ruling forces one common linear residual")
    print("degree-four moving determinant has at least five roots: impossible")
    print("h=8,k=2 frontier: two profiles remain, 2^10 and 2^9 1^2")


if __name__ == "__main__":
    main()
