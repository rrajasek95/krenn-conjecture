#!/usr/bin/env python3
"""Exact audit for ``notes/polarized-three-cap-reconstruction-obstruction.md``.

For three independent arbitrary bilinear caps on pair 13 of the rational
binary Delta_(8,2) source, this script constructs the three linear
degree-two boundary families B_a=s_a*x+r_a and directly enumerates their
trilinear six-site hafnian.  It verifies

    [B_1 B_2 B_3]_U = tau_0 e0^6 + tau_1(e1^6-e101111),

where tau_i is the complete polarization of s^2*kappa_i.  It also checks
the explicit nondegenerate product caps giving (tau_0,tau_1)=(22,72).
"""

from __future__ import annotations

import itertools
import sys
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from verify_n8_pair_cap_obstruction import (  # noqa: E402
    VERTICES,
    edge_entry,
    matching_tensor,
    perfect_matchings,
    source,
)


P, Q = 1, 3
BOUNDARY = tuple(vertex for vertex in VERTICES if vertex not in (P, Q))


def cap_family(edges, cap):
    scalar = sp.factor(
        sum(
            cap[i, j] * edge_entry(edges, P, Q, i, j)
            for i, j in itertools.product(range(2), repeat=2)
        )
    )
    degree_two = {}
    for a, b in itertools.combinations(BOUNDARY, 2):
        matrix = {}
        for color_a, color_b in itertools.product(range(2), repeat=2):
            value = scalar * edge_entry(edges, a, b, color_a, color_b)
            value += sum(
                cap[i, j]
                * (
                    edge_entry(edges, P, a, i, color_a)
                    * edge_entry(edges, Q, b, j, color_b)
                    + edge_entry(edges, P, b, i, color_b)
                    * edge_entry(edges, Q, a, j, color_a)
                )
                for i, j in itertools.product(range(2), repeat=2)
            )
            value = sp.factor(value)
            if value != 0:
                matrix[color_a, color_b] = value
        if matrix:
            degree_two[a, b] = matrix
    return scalar, degree_two


def trilinear_hafnian(families):
    """Return the coefficient dictionary of [B_1 B_2 B_3]_BOUNDARY."""

    answer = {}
    matchings = tuple(perfect_matchings(BOUNDARY))
    for coloring in itertools.product(range(2), repeat=6):
        local = dict(zip(BOUNDARY, coloring, strict=True))
        value = sp.S.Zero
        for matching in matchings:
            for assignment in itertools.permutations(range(3)):
                term = sp.S.One
                for edge, family_index in zip(matching, assignment, strict=True):
                    u, v = edge
                    term *= edge_entry(
                        families[family_index], u, v, local[u], local[v]
                    )
                value += term
        value = sp.factor(value)
        if value != 0:
            answer[coloring] = value
    return answer


def main() -> None:
    edges = source()
    assert matching_tensor(VERTICES, edges) == {
        (0,) * 8: sp.S.One,
        (1,) * 8: sp.S.One,
    }
    assert BOUNDARY == (2, 4, 5, 6, 7, 8)

    scalars = []
    kappas = []
    families = []
    caps = []
    for cap_index in range(3):
        cap = {
            (i, j): sp.symbols(f"k{cap_index}_{i}{j}")
            for i, j in itertools.product(range(2), repeat=2)
        }
        scalar, family = cap_family(edges, cap)
        assert scalar == -cap[1, 0]
        caps.append(cap)
        scalars.append(scalar)
        kappas.append((cap[0, 0], cap[1, 1]))
        families.append(family)

    actual = trilinear_hafnian(families)
    tau = []
    for color in range(2):
        tau.append(
            sp.factor(
                2
                * (
                    scalars[0] * scalars[1] * kappas[2][color]
                    + scalars[0] * scalars[2] * kappas[1][color]
                    + scalars[1] * scalars[2] * kappas[0][color]
                )
            )
        )

    expected = {
        (0,) * 6: tau[0],
        (1,) * 6: tau[1],
        (1, 0, 1, 1, 1, 1): -tau[1],
    }
    assert actual == expected
    print("arbitrary three-cap polarization identity: PASS")

    # Three genuinely different nondegenerate product caps from equation
    # (19).  K_ij = left_i * right_j.
    product_parameters = ((1, 1), (2, 3), (3, 2))
    substitution = {}
    for cap_index, (a, b) in enumerate(product_parameters):
        cap = caps[cap_index]
        substitution.update(
            {
                cap[0, 0]: 1,
                cap[0, 1]: b,
                cap[1, 0]: a,
                cap[1, 1]: a * b,
            }
        )
    specialized_tau = tuple(sp.factor(value.subs(substitution)) for value in tau)
    assert specialized_tau == (22, 72)
    specialized = {
        coloring: sp.factor(value.subs(substitution))
        for coloring, value in actual.items()
    }
    assert specialized == {
        (0,) * 6: 22,
        (1,) * 6: 72,
        (1, 0, 1, 1, 1, 1): -72,
    }
    print("nondegenerate product-cap instance (22,72,-72): PASS")


if __name__ == "__main__":
    main()
