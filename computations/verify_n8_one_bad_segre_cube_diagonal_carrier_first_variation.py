#!/usr/bin/env python3
"""Compute the exact first variation of the diagonal-carrier unit.

The base chart is the fixed fourteen-cell Segre--K4 quadratic together with
arbitrary 00, 11, and 22 cells.  The pinned six-row functional vanishes on
that entire 45-variable chart.  This checker adjoins each of the remaining
76 decorated cells separately and computes its exact linear transgression.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEPENDENCY = (
    "computations/verify_n8_one_bad_segre_cube_diagonal_carrier_unit.py"
)
DEPENDENCY_SHA256 = (
    "39d63c7e206e683fd948d2fc4b77b81d3014a2f3847eb320ed46d68249120e87"
)
EXPECTED_DIGEST = "5b6889b29f5a26a1cd09aa2171d2210472e90a7f44d80c8c948383ba444c24ee"
VARIABLE_COUNT = 46
ZERO_EXPONENT = (0,) * VARIABLE_COUNT


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load_dependency():
    path = ROOT / DEPENDENCY
    actual = sha256(path.read_bytes()).hexdigest()
    require(actual == DEPENDENCY_SHA256,
            f"dependency changed: {DEPENDENCY}: {actual}")
    spec = spec_from_file_location("diagonal_unit", path)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def poly_constant(value):
    value = Fraction(value)
    return {} if value == 0 else {ZERO_EXPONENT: value}


def poly_variable(index):
    exponent = [0] * VARIABLE_COUNT
    exponent[index] = 1
    return {tuple(exponent): Fraction(1)}


def poly_add(*values):
    result = Counter()
    for value in values:
        result.update(value)
    return {monomial: coefficient
            for monomial, coefficient in result.items() if coefficient}


def poly_scale(value, scalar):
    scalar = Fraction(scalar)
    return {monomial: scalar * coefficient
            for monomial, coefficient in value.items()
            if scalar * coefficient}


def poly_mul(left, right):
    result = Counter()
    for left_monomial, left_coefficient in left.items():
        for right_monomial, right_coefficient in right.items():
            monomial = tuple(a + b for a, b in
                             zip(left_monomial, right_monomial, strict=True))
            result[monomial] += left_coefficient * right_coefficient
    return {monomial: coefficient
            for monomial, coefficient in result.items() if coefficient}


def poly_product(values):
    result = poly_constant(1)
    for value in values:
        result = poly_mul(result, value)
    return result


def quadratic(variables, pairs):
    return poly_add(*(poly_mul(variables[left], variables[right])
                      for left, right in pairs))


def setup(dependency):
    pure_unary = dependency.load_dependency()
    source = pure_unary.load_dependency()
    support_H, weights_H = pure_unary.build_top_null_H(source)
    edges = pure_unary.EDGES
    edge_index = {edge: index for index, edge in enumerate(edges)}
    variables = tuple(poly_variable(index)
                      for index in range(VARIABLE_COUNT))

    base = {cell: poly_constant(weights_H[cell]) for cell in support_H}
    for edge in edges:
        index = edge_index[edge]
        base[(edge, (0, 0))] = variables[index]
        base[(edge, (1, 1))] = variables[15 + index]
        base[(edge, (2, 2))] = variables[30 + index]
    require(len(base) == 59, "the diagonal-carrier base support changed")

    multipliers = {
        "000001": variables[11],
        "000020": poly_scale(variables[10], -1),
        "000100": variables[9],
        "100020": poly_scale(quadratic(variables, (
            (1, 6), (1, 7), (2, 5), (3, 5),
        )), -1),
        "102000": quadratic(variables, ((1, 6), (2, 5))),
        "200001": quadratic(variables, (
            (1, 6), (1, 8), (2, 5), (4, 5),
        )),
    }
    return source, edges, variables, base, multipliers


def coefficient(source, support, word):
    terms = []
    for matching in source.MATCHINGS:
        cells = tuple((edge, (word[edge[0]], word[edge[1]]))
                      for edge in matching)
        if all(cell in support for cell in cells):
            terms.append(poly_product(support[cell] for cell in cells))
    return poly_add(*terms)


def functional(source, support, multipliers):
    pure = coefficient(source, support, (0,) * 6)
    reconstruction = poly_add(*(
        poly_mul(multiplier,
                 coefficient(source, support, tuple(map(int, label))))
        for label, multiplier in multipliers.items()
    ))
    return poly_add(pure, poly_scale(reconstruction, -1))


def cell_label(cell):
    edge, colours = cell
    return f"{edge[0]}{edge[1]}:{colours[0]}{colours[1]}"


def audit_first_variation(dependency):
    source, edges, variables, base, multipliers = setup(dependency)
    require(not functional(source, base, multipliers),
            "the base diagonal-carrier unit stopped vanishing identically")

    universe = {
        (edge, colours)
        for edge in edges
        for colours in itertools.product(range(3), repeat=2)
    }
    missing = tuple(sorted(universe - set(base)))
    require(len(missing) == 76,
            "the missing decorated-cell universe changed")

    term_histogram = Counter()
    decoration_histogram = Counter()
    dangerous = []
    for cell in missing:
        support = dict(base)
        support[cell] = variables[45]
        remainder = functional(source, support, multipliers)
        term_count = len(remainder)
        term_histogram[term_count] += 1
        decoration_histogram[(cell[1], term_count)] += 1
        require(all(exponent[45] == 1 for exponent in remainder),
                f"the first variation at {cell_label(cell)} stopped linear")
        if remainder:
            dangerous.append((cell_label(cell), term_count))

    expected_dangerous = (
        ("02:10", 8), ("02:12", 6), ("02:20", 8),
        ("03:01", 3), ("03:10", 8), ("03:20", 8),
        ("04:02", 3), ("04:10", 4), ("04:12", 12), ("04:20", 8),
        ("05:01", 3), ("05:10", 7), ("05:21", 12),
        ("13:01", 3), ("14:02", 3), ("15:01", 3),
    )
    require(tuple(dangerous) == expected_dangerous,
            f"the dangerous first-variation list changed: {dangerous}")
    require(term_histogram == Counter({
        0: 60, 3: 6, 4: 1, 6: 1, 7: 1, 8: 5, 12: 2,
    }), f"the first-variation term histogram changed: {term_histogram}")

    return {
        "base_cells": len(base),
        "missing_cells_tested": len(missing),
        "invisible_first_variations": term_histogram[0],
        "dangerous_first_variations": len(dangerous),
        "dangerous_cells_and_term_counts": dangerous,
        "term_histogram": {
            str(key): value for key, value in sorted(term_histogram.items())
        },
        "decoration_histogram": {
            f"{colours[0]}{colours[1]}/{terms}": count
            for (colours, terms), count in sorted(decoration_histogram.items())
        },
        "verdict": (
            "the diagonal-carrier unit is first-order invariant in 60 of "
            "the 76 missing cell directions; every nonzero transgression "
            "is supported on one of 16 cells incident to site 0 or site 1"
        ),
    }


def main():
    dependency = load_dependency()
    ledger = {
        "dependency": {"path": DEPENDENCY, "sha256": DEPENDENCY_SHA256},
        "first_variation": audit_first_variation(dependency),
        "scope": (
            "one added decorated coordinate at a time around the exact "
            "45-variable diagonal-carrier chart; simultaneous second-order "
            "interactions among individually invisible directions are not "
            "excluded"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_DIGEST != "TO_BE_FILLED":
        require(digest == EXPECTED_DIGEST,
                f"first-variation ledger changed: {digest}")
    print("N=8 Segre-K4 diagonal-carrier first variation: PASS")
    print("missing directions: 76 = 60 invisible + 16 nonzero")
    print("all nonzero transgressions are incident to site 0 or site 1")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
