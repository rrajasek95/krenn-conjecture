#!/usr/bin/env python3
"""Exact unit-minor certificates on 17 noncentral boundary cells.

For one extra plane, C denotes the central p_01 != 0 chart, B the affine
part of p_01 = 0, and E the remaining endpoint of that projective boundary.
This checker closes the six cell orbits

    EEE, BEE, CEE, BBE, CBE, BBB,

including every permutation of the letters.  All selected response rows are
direct-free (source pair 01 is excluded).
"""

from __future__ import annotations

from itertools import permutations

import sympy as sp

import explore_live_three_zero_minimal_three_extra_response as response


DEFAULT_PRIME = 1_000_003
KINDS = {"C": "01", "B": "12", "E": "02"}
PARAMETER_NAMES = ("a", "b", "c", "d", "e", "f")
PARAMETER_PAIRS = (("a", "b"), ("c", "d"), ("e", "f"))
SYMBOLS = sp.symbols("a b c d e f")
SYMBOL_BY_NAME = dict(zip(PARAMETER_NAMES, SYMBOLS))
R = sp.Rational


def distinct_permutations(word):
    return tuple(sorted(set(map("".join, permutations(word)))))


def cell_data(cell):
    charts = tuple(KINDS[letter] for letter in cell)
    substitutions = {}
    for letter, (first, second) in zip(cell, PARAMETER_PAIRS):
        if letter == "B":
            substitutions[second] = 0
        elif letter == "E":
            substitutions[first] = 0
            substitutions[second] = 0

    if cell.count("C") == 1 and cell.count("B") == 1:
        central = cell.index("C")
        boundary = cell.index("B")
        ordered_indices = (2*central, 2*central + 1, 2*boundary)
    else:
        ordered_indices = tuple(
            index
            for index, name in enumerate(PARAMETER_NAMES)
            if name not in substitutions
        )
    variables = tuple(SYMBOLS[index] for index in ordered_indices)
    return charts, substitutions, ordered_indices, variables


def modular_value(value, prime):
    value = R(value)
    return int(value.p) * pow(int(value.q), prime - 2, prime) % prime


def squarefree_support(value, variables):
    if isinstance(value, sp.Integer):
        assert value != 0
        return sp.S.One
    local_map = {str(symbol): symbol for symbol in SYMBOLS}
    product = sp.S.One
    for factor, _multiplicity in value.factor()[1]:
        product *= sp.sympify(
            str(factor).replace("^", "**"), locals=local_map
        )
    return sp.Poly(
        product, *variables, domain=sp.QQ
    ).sqf_part().monic().as_expr()


def selected_support(cell, point, prime=DEFAULT_PRIME, raw_modular=False):
    charts, substitutions, ordered_indices, variables = cell_data(cell)
    response.PRIME = prime
    values = [0] * 6
    for index, value in zip(ordered_indices, point):
        values[index] = int(value) % prime if raw_modular else modular_value(
            value, prime
        )
    selected = response.select_labels(
        charts,
        tuple(values),
        excluded_sources=((0, 1),),
    )
    assert len(selected) == 19
    labels = tuple(label for _support, label in selected)
    assert all(label[1:] != (0, 1) for label in labels)
    determinant = response.flint_restricted_determinant(
        charts, labels, substitutions
    )
    return squarefree_support(determinant, variables)


def assert_unit(cell, points, modular_points=()):
    _charts, _substitutions, _indices, variables = cell_data(cell)
    supports = [selected_support(cell, point) for point in points]
    supports.extend(
        selected_support(cell, point, prime=prime, raw_modular=True)
        for prime, point in modular_points
    )
    if not variables:
        assert supports == [sp.S.One]
        return
    basis = sp.groebner(
        supports, *variables, order="grevlex", domain=sp.QQ
    )
    assert basis.reduce(sp.S.One)[1] == 0, cell


ONE_VARIABLE_POINTS = ((0,), (R(-1, 2),))

CENTRAL_ENDPOINT_POINTS = (
    (0, 0),
    (-2, 0),
    (0, -3),
    (0, -1),
)

TWO_BOUNDARY_POINTS = (
    (0, 0),
    (0, R(-1, 2)),
    (R(-3, 4), 0),
    (R(-1, 2), 0),
    (R(-1, 2), R(-1, 2)),
)

MIXED_POINTS = (
    (0, 0, 0),
    (-3, -1, -3),
    (-3, -2, -3),
    (-3, -3, -3),
    (-3, -3, R(-1, 2)),
    (R(2, 5), -3, -3),
    (2, -3, -3),
    (1, -1, 0),
    (1, -2, 0),
    (1, -3, 0),
    (-2, 0, 0),
    (0, -1, 1),
    (-2, -1, 1),
    (0, -2, 1),
    (-2, -2, 1),
    (0, -3, 1),
    (-2, -3, 1),
    (0, 0, R(-1, 2)),
    (-2, 0, R(-1, 2)),
    (-2, -3, 0),
    (-3, -3, 0),
    (0, -1, 0),
    (0, -1, R(-1, 2)),
    (0, -2, 0),
    (0, -2, R(-1, 2)),
    (0, -3, 0),
    (0, -3, R(-1, 2)),
)

BBB_POINTS = (
    (0, 0, 0),
    (R(-1, 2), 0, 0),
    (0, R(-1, 2), 0),
    (0, 0, R(-1, 2)),
    (R(-1, 2), R(-1, 2), 0),
    (R(-1, 2), 0, R(-1, 2)),
    (0, R(-1, 2), R(-1, 2)),
    (R(-1, 2), R(-1, 2), R(-1, 2)),
    (R(1, 2), R(-1, 2), 0),
    (R(-1, 2), 0, R(1, 2)),
    (R(1, 2), 0, R(-1, 2)),
    (R(-1, 2), R(1, 4), R(1, 4)),
    (R(-1, 2), R(-1, 2), 1),
    (0, R(-1, 2), R(1, 2)),
    (1, R(-1, 2), R(-1, 2)),
    (R(-1, 2), 1, R(-1, 2)),
)


def main():
    try:
        assert_unit("EEE", ((0, 0, 0, 0, 0, 0),))
        for cell in distinct_permutations("BEE"):
            assert_unit(cell, ONE_VARIABLE_POINTS)
        for cell in distinct_permutations("CEE"):
            assert_unit(cell, CENTRAL_ENDPOINT_POINTS)
        for cell in distinct_permutations("BBE"):
            assert_unit(cell, TWO_BOUNDARY_POINTS)
        for cell in distinct_permutations("CBE"):
            assert_unit(cell, MIXED_POINTS)
        assert_unit(
            "BBB",
            BBB_POINTS,
            modular_points=((101, (86, 51, 65)),),
        )
    finally:
        response.PRIME = DEFAULT_PRIME

    print("minimal three-extra reduced boundary cells: PASS")
    print("six noncentral cell orbits / seventeen cells: exact unit ideals")
    print("EEE, BEE, CEE, BBE, CBE, BBB: uniformly rank 19")
    print("all selected rows direct-free; arbitrary B_01 scale allowed")


if __name__ == "__main__":
    main()
