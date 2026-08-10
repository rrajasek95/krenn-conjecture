#!/usr/bin/env python3
"""Exclude every diagonal-carrier extension of the Segre--K4 quadratic.

Let H be the exact fourteen-cell top-null quadratic from commit 772290e.
Add arbitrary cells d_ij:00, a_ij:11, and b_ij:22 on all fifteen physical
edges.  This checker expands the six displayed mixed coefficients of q^[3]
and verifies an integral identity expressing the pure-zero hafnian in their
ideal.  Thus even the diagonal carriers forced by the response anchors cannot
restore q^[3]=X0 while H remains fixed.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEPENDENCY = (
    "computations/verify_n8_one_bad_segre_cube_unary_extension_unit.py"
)
DEPENDENCY_SHA256 = (
    "9d2261e098872aa5dd7bf512065d3fd322eb07a19eb5e94c28a6cb7bcf6926ed"
)
EXPECTED_DIGEST = "ad4c3729e0519853e4f7ef0c1e169abdb6d8f326474083fb5866279a4bff8d4d"
VARIABLE_COUNT = 45
ZERO_EXPONENT = (0,) * VARIABLE_COUNT


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load_dependency():
    path = ROOT / DEPENDENCY
    actual = sha256(path.read_bytes()).hexdigest()
    require(actual == DEPENDENCY_SHA256,
            f"dependency changed: {DEPENDENCY}: {actual}")
    spec = spec_from_file_location("pure_unary", path)
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


def build_coefficients(dependency):
    source = dependency.load_dependency()
    support_H, weights_H = dependency.build_top_null_H(source)
    edges = dependency.EDGES
    edge_index = {edge: index for index, edge in enumerate(edges)}
    variables = tuple(poly_variable(index)
                      for index in range(VARIABLE_COUNT))

    cell_polynomial = {
        cell: poly_constant(weights_H[cell]) for cell in support_H
    }
    for edge in edges:
        index = edge_index[edge]
        cell_polynomial[(edge, (0, 0))] = variables[index]
        cell_polynomial[(edge, (1, 1))] = variables[15 + index]
        cell_polynomial[(edge, (2, 2))] = variables[30 + index]

    require(len(cell_polynomial) == 59,
            "the H plus diagonal-carrier support changed")
    coefficients = {}
    words = tuple(tuple(map(int, label)) for label in (
        "000000", "000001", "000020", "000100",
        "100020", "102000", "200001",
    ))
    for word in words:
        terms = []
        for matching in source.MATCHINGS:
            cells = tuple((edge, (word[edge[0]], word[edge[1]]))
                          for edge in matching)
            if all(cell in cell_polynomial for cell in cells):
                terms.append(poly_product(cell_polynomial[cell]
                                          for cell in cells))
        coefficients[word] = poly_add(*terms)
    return source, variables, coefficients


def verify_identity(dependency):
    source, variables, coefficients = build_coefficients(dependency)
    coefficient = lambda label: coefficients[tuple(map(int, label))]

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
    reconstructed = poly_add(*(
        poly_mul(multiplier, coefficient(label))
        for label, multiplier in multipliers.items()
    ))
    pure = coefficient("000000")
    require(reconstructed == pure,
            "the diagonal-carrier six-row certificate changed")
    require(len(pure) == 15,
            "the pure-zero hafnian term count changed")
    require(all(all(exponent[index] == 0 for index in range(15, 45))
                for exponent in pure),
            "a nonzero-colour carrier entered the pure-zero coefficient")

    row_terms = {
        label: len(coefficient(label)) for label in multipliers
    }
    require(row_terms == {
        "000001": 9,
        "000020": 9,
        "000100": 9,
        "100020": 3,
        "102000": 3,
        "200001": 3,
    }, f"the mixed-row term ledger changed: {row_terms}")

    return {
        "fixed_H_cells": 14,
        "arbitrary_cells": {"00": 15, "11": 15, "22": 15},
        "total_support_cells": 59,
        "pure_hafnian_terms": len(pure),
        "mixed_row_terms": row_terms,
        "certificate": (
            "haf(d)=d11*g000001-d10*g000020+d9*g000100"
            "-(d1*d6+d1*d7+d2*d5+d3*d5)*g100020"
            "+(d1*d6+d2*d5)*g102000"
            "+(d1*d6+d1*d8+d2*d5+d4*d5)*g200001"
        ),
        "verdict": (
            "all six mixed coefficients zero force haf(d)=0 even with "
            "arbitrary 11 and 22 cells, contradicting q^[3]=X0"
        ),
        "matching_count": len(source.MATCHINGS),
    }


def main():
    dependency = load_dependency()
    ledger = {
        "dependency": {"path": DEPENDENCY, "sha256": DEPENDENCY_SHA256},
        "diagonal_carrier_unit": verify_identity(dependency),
        "scope": (
            "the exact fixed fourteen-cell Segre-K4 H plus arbitrary 00, "
            "11, and 22 cells on all residual edges; arbitrary deformation "
            "of H or added 12/21 and other mixed cells is not included"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_DIGEST != "TO_BE_FILLED":
        require(digest == EXPECTED_DIGEST,
                f"diagonal-carrier ledger changed: {digest}")
    print("N=8 Segre-K4 diagonal-carrier unit: PASS")
    print("arbitrary cells: 15 pure 00 + 15 diagonal 11 + 15 diagonal 22")
    print("certificate: 6 literal mixed top coefficients")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
