#!/usr/bin/env python3
"""Discover exact direct-free certificates on two-extra boundary cells."""

from __future__ import annotations

import argparse

import sympy as sp

import explore_live_three_zero_minimal_two_extra_response as response
from explore_live_three_zero_minimal_three_extra_ccb import (
    modular_finish,
    singular_status,
)
from verify_live_three_zero_minimal_three_extra_boundary_low_cells import (
    MIXED_POINTS,
)


KINDS = {"C": "01", "B": "12", "E": "02"}
PARAMETER_NAMES = ("a", "b", "c", "d")
SYMBOLS = sp.symbols("a b c d")
SYMBOL_BY_NAME = dict(zip(PARAMETER_NAMES, SYMBOLS))
LOCAL_MAP = dict(zip(PARAMETER_NAMES, SYMBOLS))
R = sp.Rational
DEFAULT_PRIME = 1_000_003

ONE_POINTS = (
    (0,), (-1,), (-2,), (-3,), (1,), (R(-1, 2),)
)
TWO_POINTS = (
    (0, 0),
    (-1, -1),
    (-2, -2),
    (-3, -3),
    (1, 1),
    (R(-1, 2), R(-1, 2)),
    (0, -1),
    (-1, 0),
    (0, -2),
    (-2, 0),
    (1, -1),
    (-1, 1),
)
ZERO_POINTS = ((),)


def cell_data(cell):
    assert len(cell) == 2 and all(letter in KINDS for letter in cell)
    charts = tuple(KINDS[letter] for letter in cell)
    substitutions = {}
    for letter, (first, second) in zip(
        cell, (("a", "b"), ("c", "d"))
    ):
        if letter == "B":
            substitutions[second] = 0
        elif letter == "E":
            substitutions[first] = 0
            substitutions[second] = 0
    free_names = tuple(
        name for name in PARAMETER_NAMES if name not in substitutions
    )
    variables = tuple(SYMBOL_BY_NAME[name] for name in free_names)
    return charts, substitutions, free_names, variables


def points_for_dimension(dimension):
    if dimension == 0:
        return ZERO_POINTS
    if dimension == 1:
        return ONE_POINTS
    if dimension == 2:
        return TWO_POINTS
    if dimension == 3:
        return MIXED_POINTS
    raise ValueError(dimension)


def modular_value(value, prime):
    value = R(value)
    return int(value.p)*pow(int(value.q), prime-2, prime) % prime


def full_point(cell, point):
    _charts, substitutions, free_names, _variables = cell_data(cell)
    values = {name: R(value) for name, value in substitutions.items()}
    values.update(dict(zip(free_names, point)))
    return tuple(values[name] for name in PARAMETER_NAMES)


def modular_full_point(cell, point, prime):
    _charts, substitutions, free_names, _variables = cell_data(cell)
    values = {
        name: int(value) % prime
        for name, value in substitutions.items()
    }
    values.update(
        {
            name: int(value) % prime
            for name, value in zip(free_names, point)
        }
    )
    return tuple(values[name] for name in PARAMETER_NAMES)


def labels_at(cell, point, prime=DEFAULT_PRIME, raw_modular=False):
    charts, _substitutions, _free_names, _variables = cell_data(cell)
    response.PRIME = prime
    values = (
        tuple(int(value) % prime for value in point)
        if raw_modular
        else tuple(modular_value(value, prime) for value in point)
    )
    selected = response.select_labels(charts, values)
    assert len(selected) == 20, (cell, len(selected), point)
    labels = tuple(label for _support, label in selected)
    assert all(label[1:] != (0, 1) for label in labels)
    return labels


def exact_support(cell, labels):
    charts, substitutions, _free_names, variables = cell_data(cell)
    determinant = response.flint_determinant(charts, labels)
    product = sp.S.One
    for factor, _multiplicity in determinant.factor_squarefree()[1]:
        product *= sp.sympify(
            str(factor).replace("^", "**"), locals=LOCAL_MAP
        )
    restricted = sp.expand(
        product.subs(
            {SYMBOL_BY_NAME[name]: value
             for name, value in substitutions.items()}
        )
    )
    assert restricted != 0
    if not variables:
        return sp.S.One
    return sp.Poly(
        restricted, *variables, domain=sp.QQ
    ).sqf_part().monic().as_expr()


def base_supports(cell, show=False):
    _charts, _substitutions, _free_names, variables = cell_data(cell)
    polynomials = []
    label_sets = set()
    for point in points_for_dimension(len(variables)):
        labels = labels_at(cell, full_point(cell, point))
        if labels in label_sets:
            continue
        label_sets.add(labels)
        polynomial = exact_support(cell, labels)
        if polynomial not in polynomials:
            polynomials.append(polynomial)
            if show:
                print(point, sp.factor(polynomial), flush=True)
    return tuple(polynomials)


def discover(cell):
    _charts, _substitutions, _free_names, variables = cell_data(cell)
    polynomials = list(base_supports(cell))
    if not variables:
        assert polynomials == [sp.S.One]
        print("MODULAR_POINTS", (), flush=True)
        return

    def add_at(point, prime):
        full = modular_full_point(cell, point, prime)
        labels = labels_at(
            cell, full, prime=prime, raw_modular=True
        )
        return exact_support(cell, labels)

    modular_finish(polynomials, variables, add_at)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--cell",
        choices=tuple(
            left+right
            for left in ("C", "B", "E")
            for right in ("C", "B", "E")
            if left+right != "CC"
        ),
        required=True,
    )
    parser.add_argument("--discover", action="store_true")
    parser.add_argument("--show", action="store_true")
    args = parser.parse_args()
    _charts, _substitutions, _free_names, variables = cell_data(args.cell)
    try:
        if args.discover:
            discover(args.cell)
        else:
            polynomials = base_supports(args.cell, show=args.show)
            status = (
                "UNIT"
                if not variables and polynomials == (sp.S.One,)
                else singular_status(polynomials, variables)
            )
            print(
                args.cell,
                "supports", len(polynomials),
                "status", status.replace("\n", " "),
            )
    finally:
        response.PRIME = DEFAULT_PRIME


if __name__ == "__main__":
    main()
