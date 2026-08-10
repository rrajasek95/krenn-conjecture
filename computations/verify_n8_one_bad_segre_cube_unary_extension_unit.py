#!/usr/bin/env python3
"""Close the Segre-K4 counterguard against every pure unary extension.

Let H be the exact 14-cell top-null quadratic from commit 772290e.  Add an
arbitrary all-zero-colour scalar quadratic d on all 15 physical edges.  Every
H-cell has exactly one nonzero-coloured endpoint, so the coefficients of
(H+d)^[3] split by defect count into d^[3], d^[2]H, dH^[2], H^[3].

This checker reconstructs every coefficient as a sparse integral polynomial
and verifies a six-row ordinary source identity expressing haf(d) in the
mixed coefficient ideal.  Therefore (H+d)^[3] can never equal X_0.
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
    "computations/verify_n8_one_bad_segre_cube_k4_closure_counterguard.py"
)
DEPENDENCY_SHA256 = (
    "44e2ca27001ef82ed77f73d5c956963b13507f98b4c9a1fd7b6f71b6434e700b"
)
EXPECTED_DIGEST = "83dbae8c546b324cba8132f88e50523a215ff45313b64386f9d4258a1711d667"
SITES = tuple(range(6))
EDGES = tuple(itertools.combinations(SITES, 2))
ZERO_EXPONENT = (0,) * len(EDGES)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load_dependency():
    path = ROOT / DEPENDENCY
    actual = sha256(path.read_bytes()).hexdigest()
    require(actual == DEPENDENCY_SHA256,
            f"dependency changed: {DEPENDENCY}: {actual}")
    spec = spec_from_file_location("segre_k4", path)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def poly_constant(value):
    value = Fraction(value)
    return {} if value == 0 else {ZERO_EXPONENT: value}


def poly_variable(index):
    exponent = [0] * len(EDGES)
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


def poly_serial(value):
    return sorted((list(monomial), str(coefficient))
                  for monomial, coefficient in value.items())


def build_top_null_H(module):
    base_support, base_weights, _rows, exported = module.audit_plucker_square()
    cells = {
        ((2, 5), (0, 1)): Fraction(1),
        ((2, 5), (2, 0)): Fraction(-1),
        ((3, 4), (0, 2)): Fraction(1),
        ((3, 4), (1, 0)): Fraction(-1),
    }
    support = set(base_support)
    support.update(cells)
    weights = dict(base_weights)
    weights.update(cells)
    require(len(support) == 14,
            "the pinned Segre-K4 top-null support changed")
    require(all(sum(colour != 0 for colour in colours) == 1
                for _edge, colours in support),
            "an H-cell stopped carrying exactly one colour defect")
    completion = module.audit_cross_completion(
        base_support, base_weights, exported
    )
    require(completion["full_top_tensor"] == 0,
            "the pinned H quadratic stopped being top-null")
    return frozenset(support), weights


def coefficient_polynomials(module, H_support, H_weights):
    cell_polynomial = {
        cell: poly_constant(H_weights[cell]) for cell in H_support
    }
    for edge_index, edge in enumerate(EDGES):
        cell_polynomial[(edge, (0, 0))] = poly_variable(edge_index)
    support = frozenset(cell_polynomial)

    coefficients = {}
    matching_counts = {}
    for word in itertools.product(range(3), repeat=6):
        terms = []
        for matching in module.MATCHINGS:
            cells = tuple((edge, (word[edge[0]], word[edge[1]]))
                          for edge in matching)
            if all(cell in support for cell in cells):
                terms.append(poly_product(cell_polynomial[cell]
                                          for cell in cells))
        coefficient = poly_add(*terms)
        if coefficient:
            coefficients[word] = coefficient
            matching_counts[word] = len(terms)
    return coefficients, matching_counts


def verify_identity(module):
    H_support, H_weights = build_top_null_H(module)
    coefficients, matching_counts = coefficient_polynomials(
        module, H_support, H_weights
    )

    by_defect = Counter(sum(colour != 0 for colour in word)
                        for word in coefficients)
    require(by_defect == Counter({2: 8, 1: 6, 0: 1}),
            f"the pure-extension defect ledger changed: {by_defect}")
    require(all(sum(exponent) == 3 - sum(colour != 0 for colour in word)
                for word, polynomial in coefficients.items()
                for exponent in polynomial),
            "the colour-defect/pure-degree grading changed")

    pure = coefficients[(0, 0, 0, 0, 0, 0)]
    rows = {
        label: coefficients[tuple(map(int, label))]
        for label in (
            "000020", "000100", "002000",
            "100020", "100100", "102000",
        )
    }
    variables = tuple(poly_variable(index) for index in range(len(EDGES)))

    # Edge order:
    # d11=25, d13=35, d14=45, d4=05, d7=14, d3=04,
    # d8=15, d6=13, d2=03, d5=12, d1=02.
    certificate_terms = (
        poly_mul(variables[14], rows["000020"]),
        poly_mul(variables[13], rows["000100"]),
        poly_scale(poly_mul(variables[11], rows["002000"]), -1),
        poly_mul(poly_add(poly_mul(variables[4], variables[7]),
                          poly_mul(variables[3], variables[8])),
                 rows["100020"]),
        poly_mul(poly_add(poly_mul(variables[4], variables[6]),
                          poly_mul(variables[2], variables[8])),
                 rows["100100"]),
        poly_scale(
            poly_mul(poly_add(poly_mul(variables[4], variables[5]),
                              poly_mul(variables[1], variables[8])),
                     rows["102000"]),
            -1,
        ),
    )
    reconstructed = poly_add(*certificate_terms)
    require(reconstructed == pure,
            "the six-row pure-hafnian certificate changed")

    return {
        "H_decorated_cells": len(H_support),
        "H_cells_have_one_nonzero_endpoint": True,
        "arbitrary_pure_variables": len(EDGES),
        "nonzero_coefficient_rows_by_defect": {
            str(defect): count for defect, count in sorted(by_defect.items())
        },
        "mixed_rows_used": list(rows),
        "pure_hafnian_terms": len(pure),
        "certificate_terms": len(certificate_terms),
        "certificate": (
            "haf(d)=d14*g000020+d13*g000100-d11*g002000"
            "+(d4*d7+d3*d8)*g100020"
            "+(d4*d6+d2*d8)*g100100"
            "-(d4*d5+d1*d8)*g102000"
        ),
        "pure_polynomial": poly_serial(pure),
        "row_matching_count_digest": sha256(json.dumps(
            {"".join(map(str, word)): matching_counts[word]
             for word in sorted(matching_counts)},
            sort_keys=True,
        ).encode()).hexdigest(),
        "verdict": (
            "all mixed coefficients of (H+d)^[3] force haf(d)=0, so no "
            "arbitrary all-zero quadratic d can restore the unary X0 row"
        ),
    }


def main():
    module = load_dependency()
    ledger = {
        "dependency": {"path": DEPENDENCY, "sha256": DEPENDENCY_SHA256},
        "pure_unary_extension": verify_identity(module),
        "scope": (
            "all 15 pure-0 cells over the exact 14-cell Segre-K4 mixed "
            "quadratic H; arbitrary new mixed-colour cells and deformations "
            "of H are not included"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_DIGEST != "TO_BE_FILLED":
        require(digest == EXPECTED_DIGEST,
                f"unary-extension ledger changed: {digest}")
    print("N=8 Segre-K4 pure-unary extension unit: PASS")
    print("arbitrary pure d: 15 cells; mixed rows imply haf(d)=0")
    print("certificate: 6 literal mixed coefficients")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
