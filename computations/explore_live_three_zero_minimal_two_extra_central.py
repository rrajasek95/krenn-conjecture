#!/usr/bin/env python3
"""Discover exact branch minors on the central two-extra chart."""

from __future__ import annotations

import argparse

import sympy as sp

import explore_live_three_zero_minimal_two_extra_response as response
from explore_live_three_zero_minimal_three_extra_ccb import (
    modular_finish,
    singular_status,
)


a, b, c, d = sp.symbols("a b c d")
SYMBOLS = (a, b, c, d)
LOCAL_MAP = {str(symbol): symbol for symbol in SYMBOLS}
R = sp.Rational
DEFAULT_PRIME = 1_000_003

THREE_POINTS = (
    (0, 0, 0),
    (-1, -1, -1),
    (-2, -2, -2),
    (1, 1, 1),
    (0, -1, -2),
    (-2, -1, 0),
    (1, -1, 1),
    (-1, 1, -1),
) + tuple(
    tuple(value if index == axis else 0 for index in range(3))
    for axis in range(3)
    for value in (-1, -2, -3, 1)
)


def modular_value(value, prime=DEFAULT_PRIME):
    value = R(value)
    return (
        int(value.p)
        * pow(int(value.q), prime-2, prime)
        % prime
    )


def labels_at(point, prime=DEFAULT_PRIME, raw_modular=False):
    response.PRIME = prime
    values = tuple(
        int(value) % prime
        if raw_modular
        else modular_value(value, prime)
        for value in point
    )
    selected = response.select_labels(("01", "01"), values)
    assert len(selected) == 20
    labels = tuple(label for _support, label in selected)
    assert all(label[1:] != (0, 1) for label in labels)
    return labels


def full_squarefree_support(labels):
    determinant = response.flint_determinant(("01", "01"), labels)
    product = sp.S.One
    for factor, _multiplicity in determinant.factor_squarefree()[1]:
        product *= sp.sympify(
            str(factor).replace("^", "**"), locals=LOCAL_MAP
        )
    return sp.expand(product)


def branch_data(branch):
    if branch == "a0":
        return (
            (b, c, d),
            {a: 0},
            lambda point: (0, point[0], point[1], point[2]),
            None,
        )
    if branch == "c0":
        return (
            (a, b, d),
            {c: 0},
            lambda point: (point[0], point[1], 0, point[2]),
            None,
        )
    if branch == "bd":
        return (
            (a, b, c),
            {d: b},
            lambda point: (point[0], point[1], point[2], point[1]),
            None,
        )
    if branch == "Q":
        denominator = a+3

        def full(point):
            avalue, bvalue, dvalue = point
            if avalue == -3:
                return None
            cvalue = -3*R(avalue+2, avalue+3)
            return (avalue, bvalue, cvalue, dvalue)

        return (
            (a, b, d),
            {c: -3*(a+2)/denominator},
            full,
            denominator,
        )
    raise ValueError(branch)


def restricted_support(labels, branch):
    variables, substitutions, _full, _localizer = branch_data(branch)
    restricted = sp.cancel(
        full_squarefree_support(labels).subs(substitutions)
    )
    numerator = restricted.as_numer_denom()[0]
    assert numerator != 0
    return sp.Poly(
        numerator, *variables, domain=sp.QQ
    ).sqf_part().monic().as_expr()


def branch_supports(branch, show=False):
    _variables, _substitutions, full, _localizer = branch_data(branch)
    polynomials = []
    label_sets = set()
    for point in THREE_POINTS:
        full_point = full(point)
        if full_point is None:
            continue
        labels = labels_at(full_point)
        if labels in label_sets:
            continue
        label_sets.add(labels)
        polynomial = restricted_support(labels, branch)
        if polynomial not in polynomials:
            polynomials.append(polynomial)
            if show:
                print(point, sp.factor(polynomial), flush=True)
    return tuple(polynomials)


def modular_full_point(branch, point, prime):
    if branch == "a0":
        return (0, point[0], point[1], point[2])
    if branch == "c0":
        return (point[0], point[1], 0, point[2])
    if branch == "bd":
        return (point[0], point[1], point[2], point[1])
    if branch == "Q":
        avalue, bvalue, dvalue = point
        denominator = (avalue+3) % prime
        assert denominator
        cvalue = (
            -3*(avalue+2)*pow(denominator, prime-2, prime)
        ) % prime
        return (avalue, bvalue, cvalue, dvalue)
    raise ValueError(branch)


def discover_branch(branch):
    variables, _substitutions, _full, localizer = branch_data(branch)
    polynomials = list(branch_supports(branch))

    def add_at(point, prime):
        full_point = modular_full_point(branch, point, prime)
        labels = labels_at(
            full_point, prime=prime, raw_modular=True
        )
        return restricted_support(labels, branch)

    modular_finish(
        polynomials, variables, add_at, localizer=localizer
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--branch", choices=("a0", "c0", "bd", "Q"), required=True
    )
    parser.add_argument("--show", action="store_true")
    parser.add_argument("--discover", action="store_true")
    args = parser.parse_args()
    variables, _substitutions, _full, localizer = branch_data(
        args.branch
    )
    try:
        if args.discover:
            discover_branch(args.branch)
        else:
            polynomials = branch_supports(
                args.branch, show=args.show
            )
            status = singular_status(
                polynomials, variables, localizer=localizer
            )
            print(
                args.branch,
                "supports", len(polynomials),
                "status", status.replace("\n", " "),
            )
    finally:
        response.PRIME = DEFAULT_PRIME


if __name__ == "__main__":
    main()
