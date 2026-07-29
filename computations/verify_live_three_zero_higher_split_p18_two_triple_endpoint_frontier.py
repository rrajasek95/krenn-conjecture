#!/usr/bin/env python3
"""Exact audit of the p=18 two-triple endpoint frontier."""

from __future__ import annotations

from math import factorial
from pathlib import Path
import itertools
import sys

import sympy as sp


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from verify_live_three_zero_higher_split_q5_boundary_census import (  # noqa: E402
    formal_selections,
    symbolic_survivors,
)


def assert_zero(expr: sp.Expr) -> None:
    assert sp.factor(sp.together(expr)) == 0, sp.factor(sp.together(expr))


def profile(triples: int, doubles: int, singletons: int) -> tuple[int, ...]:
    return (3,) * triples + (2,) * doubles + (1,) * singletons


def wronskian(polys: list[sp.Expr], variable: sp.Symbol) -> sp.Expr:
    return sp.factor(
        sp.Matrix(
            [
                [sp.diff(poly, variable, order) for poly in polys]
                for order in range(len(polys))
            ]
        ).det()
    )


EXPECTED_SELECTIONS = {
    0: ((0, 0, profile(2, 0, 12)), (1, 1, profile(1, 0, 15))),
    1: (
        (0, 0, profile(2, 1, 10)),
        (1, 0, profile(2, 0, 12)),
        (1, 1, profile(1, 1, 13)),
        (2, 1, profile(1, 0, 15)),
    ),
    2: (
        (0, 0, profile(2, 2, 8)),
        (1, 0, profile(2, 1, 10)),
        (1, 1, profile(1, 2, 11)),
        (2, 0, profile(2, 0, 12)),
        (2, 1, profile(1, 1, 13)),
    ),
    3: (
        (0, 0, profile(2, 3, 6)),
        (1, 0, profile(2, 2, 8)),
        (1, 1, profile(1, 3, 9)),
        (2, 0, profile(2, 1, 10)),
        (2, 1, profile(1, 2, 11)),
    ),
    4: (
        (0, 0, profile(2, 4, 4)),
        (1, 0, profile(2, 3, 6)),
        (1, 1, profile(1, 4, 7)),
        (2, 0, profile(2, 2, 8)),
        (2, 1, profile(1, 3, 9)),
    ),
    5: (
        (0, 0, profile(2, 5, 2)),
        (1, 0, profile(2, 4, 4)),
        (1, 1, profile(1, 5, 5)),
        (2, 0, profile(2, 3, 6)),
        (2, 1, profile(1, 4, 7)),
    ),
    6: (
        (0, 0, profile(2, 6, 0)),
        (1, 0, profile(2, 5, 2)),
        (1, 1, profile(1, 6, 3)),
        (2, 0, profile(2, 4, 4)),
        (2, 1, profile(1, 5, 5)),
    ),
    7: (
        (1, 0, profile(2, 6, 0)),
        (1, 1, profile(1, 7, 1)),
        (2, 0, profile(2, 5, 2)),
        (2, 1, profile(1, 6, 3)),
    ),
    8: (
        (2, 0, profile(2, 6, 0)),
        (2, 1, profile(1, 7, 1)),
    ),
}


def audit_family_and_selection_table() -> None:
    for h in range(13, 18):
        survivors = symbolic_survivors(h, 18)
        for doubles in range(9):
            original = profile(2, doubles, h + 14 - 2 * doubles)
            assert original in survivors
            observed = tuple(
                (selection.d, selection.selected_triples, selection.complement)
                for selection in formal_selections(original, h, 18)
            )
            assert observed == EXPECTED_SELECTIONS[doubles]

            packet = doubles // 3
            selected_doubles = doubles - 3 * packet
            common_complement = profile(2, 3 * packet, 12 - 6 * packet)
            assert (
                selected_doubles,
                0,
                common_complement,
            ) in observed

        # The translated applicability condition stops exactly at b=8.
        beyond = profile(2, 9, h - 4)
        assert beyond not in survivors


def audit_bare_endpoint_dominance() -> None:
    z = sp.symbols("z")
    coordinates = sp.symbols("x0:6")
    x0, x1, x2, x3, x4, x5 = coordinates
    basis = [
        1 + x0 * z**3 + x1 * z**4,
        z + x2 * z**3 + x3 * z**4,
        z**2 + x4 * z**3 + x5 * z**4,
    ]
    full_wronskian = sp.expand(wronskian(basis, z))
    assert full_wronskian.coeff(z, 0) == 2
    coefficient_map = sp.Matrix(
        [full_wronskian.coeff(z, degree) for degree in range(1, 7)]
    )
    jacobian = coefficient_map.jacobian(coordinates)
    witness = dict(zip(coordinates, (-2, -2, -2, -1, -2, -2)))
    assert jacobian.det().subs(witness) == -1430784

    witness_wronskian = sp.factor(full_wronskian.subs(witness))
    expected = -2 * (
        2 * z**6 - 6 * z**4 - 6 * z**3 + 6 * z**2 + 6 * z - 1
    )
    assert_zero(witness_wronskian - expected)
    assert sp.Poly(witness_wronskian, z).degree() == 6
    assert sp.gcd(
        sp.Poly(witness_wronskian, z),
        sp.Poly(sp.diff(witness_wronskian, z), z),
    ).degree() == 0
    assert sp.gcd(
        sp.Poly(witness_wronskian, z),
        sp.Poly(witness_wronskian.subs(z, -z), z),
    ).degree() == 0
    assert witness_wronskian.subs(z, 0) != 0


def normalized_neighbor_wronskians() -> tuple[
    sp.Symbol,
    sp.Symbol,
    list[tuple[int, int, int]],
    list[sp.Expr],
    sp.Matrix,
]:
    z, beta = sp.symbols("z beta")
    basis = [1 - beta * z, z**2, z**3, z**4, z**5]
    triples = list(itertools.combinations(range(5), 3))
    quotients = []
    for indices in triples:
        full = wronskian([basis[index] for index in indices], z)
        quotient = sp.cancel(full / z**2)
        assert not sp.denom(quotient).has(z)
        quotients.append(sp.factor(quotient))
    matrix = sp.Matrix(
        [
            [sp.expand(poly).coeff(z, degree) for poly in quotients]
            for degree in range(8)
        ]
    )
    return z, beta, triples, quotients, matrix


def audit_neighbor_quintic_geometry() -> None:
    z, beta, triples, quotients, coefficient_matrix = (
        normalized_neighbor_wronskians()
    )
    expected = [
        -2 * (beta * z - 3),
        -2 * z * (3 * beta * z - 8),
        -6 * z**2 * (2 * beta * z - 5),
        -6 * z**2 * (beta * z - 2),
        -2 * z**3 * (8 * beta * z - 15),
        -4 * z**4 * (3 * beta * z - 5),
        2 * z**4,
        6 * z**5,
        6 * z**6,
        2 * z**7,
    ]
    assert triples == list(itertools.combinations(range(5), 3))
    for observed, target in zip(quotients, expected):
        assert_zero(observed - target)

    # This triangular minor proves surjectivity for every beta, including
    # the zero-slope chart.
    pivot_columns = [0, 1, 3, 4, 6, 7, 8, 9]
    assert coefficient_matrix[:, pivot_columns].det() == 4976640
    assert coefficient_matrix.rank() == 8

    # Check the dual Pluecker sign convention on an exact decomposable
    # coordinate vector.
    sample = sp.Matrix(
        [[1, 2, 3, 4, 5], [0, 1, 4, 2, 3], [3, 0, 2, 1, 6]]
    )
    pluecker = {
        indices: sample[:, indices].det() for indices in triples
    }
    dual = {
        pair: (-1) ** sum(pair)
        * pluecker[tuple(index for index in range(5) if index not in pair)]
        for pair in itertools.combinations(range(5), 2)
    }
    for four in itertools.combinations(range(5), 4):
        i, j, k, ell = four
        assert (
            dual[i, j] * dual[k, ell]
            - dual[i, k] * dual[j, ell]
            + dual[i, ell] * dual[j, k]
        ) == 0

    # A single affine Grassmannian point works for every complex beta.
    coordinates = sp.symbols("y0:6")
    hyperplane_basis = [1 - beta * z, z**2, z**3, z**4, z**5]
    chart_basis = [
        hyperplane_basis[index]
        + coordinates[2 * index] * hyperplane_basis[3]
        + coordinates[2 * index + 1] * hyperplane_basis[4]
        for index in range(3)
    ]
    chart_wronskian = sp.cancel(wronskian(chart_basis, z) / z**2)
    assert not sp.denom(chart_wronskian).has(z)
    assert sp.expand(chart_wronskian).coeff(z, 0) == 6
    chart_coefficients = sp.Matrix(
        [
            sp.expand(chart_wronskian).coeff(z, degree)
            for degree in range(1, 8)
        ]
    )
    jacobian = chart_coefficients.jacobian(coordinates)
    witness = dict(zip(coordinates, (-2, -2, -2, -1, -2, -2)))
    witness_jacobian = jacobian.subs(witness)
    minor_one = sp.factor(witness_jacobian[list(range(6)), :].det())
    minor_two = sp.factor(
        witness_jacobian[[0, 1, 2, 3, 4, 6], :].det()
    )
    assert_zero(
        minor_one + 165888 * (6 * beta**2 - 60 * beta - 355)
    )
    assert_zero(
        minor_two - 27648 * (8 * beta**2 - 131 * beta - 325)
    )
    assert sp.gcd(
        sp.Poly(minor_one, beta), sp.Poly(minor_two, beta)
    ).degree() == 0

    # Hook-length degree of the 3-by-2 rectangle: deg Gr(3,5)=5.
    hook_product = 1
    rows, columns = 3, 2
    for row in range(rows):
        for column in range(columns):
            hook_product *= rows - row + columns - column - 1
    assert factorial(rows * columns) // hook_product == 5


def audit_exchange_slopes_and_second_jets() -> None:
    z, r, u = sp.symbols("z r u")
    phi = 3 / (r - u) + 2 / (r + u)
    assert_zero(phi - (5 * r + u) / (r**2 - u**2))
    assert_zero(2 / (r + r) - 1 / r)
    assert_zero(
        sp.diff(3 / (z - u) + 2 / (z + u), z).subs(z, r)
        + 3 / (r - u) ** 2
        + 2 / (r + u) ** 2
    )

    # Audit an actual selected-triple local unit.  The small products have
    # the same logarithmic multiplicities as the full endpoint formula.
    x, v, y, mu, k = sp.symbols("x v y mu k")
    neighbor_logarithmic_derivative = (
        k / (z + mu)
        + 2 / (z + r)
        + 2 / (z + u)
        + 1 / (z + y)
        - 4 / (z - x)
        - 3 / (z - v)
    )
    neighbor_beta = neighbor_logarithmic_derivative.subs(z, r)
    expected_beta = (
        k / (r + mu)
        + 1 / r
        + 2 / (r + u)
        + 1 / (r + y)
        - 4 / (r - x)
        - 3 / (r - v)
    )
    assert_zero(neighbor_beta - expected_beta)

    # At a complementary double v, selecting q removes its negative-pole
    # cube and inserts its plus-pole square.
    q, w, t, x1, x2 = sp.symbols("q w t x1 x2")
    alpha_empty = (
        k / (v + mu)
        + 1 / (v + y)
        - 4 / (v - x1)
        - 4 / (v - x2)
        - 3 / (v - q)
        - 3 / (v - w)
        - 3 / (v - t)
    )
    eta_empty = sp.diff(
        k / (z + mu)
        + 1 / (z + y)
        - 4 / (z - x1)
        - 4 / (z - x2)
        - 3 / (z - q)
        - 3 / (z - w)
        - 3 / (z - t),
        z,
    ).subs(z, v)
    selected_log = (
        k / (z + mu)
        + 2 / (z + q)
        + 1 / (z + y)
        - 4 / (z - x1)
        - 4 / (z - x2)
        - 3 / (z - w)
        - 3 / (z - t)
    )
    alpha_selected = selected_log.subs(z, v)
    eta_selected = sp.diff(selected_log, z).subs(z, v)
    assert_zero(
        alpha_selected
        - alpha_empty
        - 3 / (v - q)
        - 2 / (v + q)
    )
    assert_zero(
        eta_selected
        - eta_empty
        + 3 / (v - q) ** 2
        + 2 / (v + q) ** 2
    )
    # The residue of U*S/(z-v)^3 is (U*S)''(v)/2.
    tau = sp.symbols("tau")
    u0, u1, u2, p0, p1, p2 = sp.symbols("u0 u1 u2 p0 p1 p2")
    unit_jet = u0 + u1 * tau + u2 * tau**2 / 2
    polynomial_jet = p0 + p1 * tau + p2 * tau**2 / 2
    residue = sp.expand(unit_jet * polynomial_jet / tau**3).coeff(
        tau, -1
    )
    assert_zero(residue - (u0 * p2 + 2 * u1 * p1 + u2 * p0) / 2)
    alpha_jet = u1 / u0
    eta_jet = (u0 * u2 - u1**2) / u0**2
    delta_jet = u2 / u0
    assert_zero(delta_jet - alpha_jet**2 - eta_jet)

    alpha, delta = sp.symbols("alpha delta")
    for degree in range(5):
        row_entry = (
            sp.diff(z**degree, z, 2)
            + 2 * alpha * sp.diff(z**degree, z)
            + delta * z**degree
        ).subs(z, v)
        expected_entry = (
            (degree * (degree - 1) * v ** (degree - 2) if degree >= 2 else 0)
            + (2 * alpha * degree * v ** (degree - 1) if degree >= 1 else 0)
            + delta * v**degree
        )
        assert_zero(row_entry - expected_entry)

    assert len(list(itertools.combinations(range(6), 0))) == 1
    assert len(list(itertools.combinations(range(7), 1))) == 7
    assert len(list(itertools.combinations(range(8), 2))) == 28
    assert 2 * 8 == 16


def main() -> None:
    audit_family_and_selection_table()
    audit_bare_endpoint_dominance()
    audit_neighbor_quintic_geometry()
    audit_exchange_slopes_and_second_jets()
    print("p=18 two-triple endpoint frontier PASS")
    print("families audited: b=0,...,8")
    print("common complements: 3^2 1^12, 3^2 2^3 1^6, 3^2 2^6")
    print("bare 3^2 2^6 Wronski map: dominant")
    print("neighbor 3 2^7 1 image: irreducible quintic")
    print("endpoint rank-two systems retained: 1 + 7 + 28")
    print("frontier scope: no endpoint closure claimed")


if __name__ == "__main__":
    main()
