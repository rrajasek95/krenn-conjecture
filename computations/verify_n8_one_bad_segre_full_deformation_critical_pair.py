#!/usr/bin/env python3
"""Exact simultaneous-deformation boundary of the Segre--K4 unit.

Expand the six-row diagonal-carrier functional on the full decorated K6
quadratic: the fixed fourteen-cell H, all 45 diagonal cells, and all 76
remaining endpoint-colour cells with independent variables.  The remainder
has 129 terms: 99 linear and 30 quadratic in the missing-cell variables.
Only 17 missing cells occur.  Sixteen are the known first-order directions;
the seventeenth, 12:02, is tangent-invisible and appears only in three exact
Hessian pairs.

The smallest hidden pair is x=03:10, y=12:02.  Its coefficient is

    -x*y*d45*(d02*d13+d03*d12).

It is the literal matching 03|12|45 in the mixed word 102000, multiplied by
the pinned diagonal coefficient.  Hence common-q Hessian/third-cofactor
provenance does not remove the simultaneous obstruction: it certifies it.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction
from functools import reduce
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIRST_PATH = (
    "computations/verify_n8_one_bad_segre_cube_"
    "diagonal_carrier_first_variation.py"
)
FIRST_NOTE = "notes/n8-one-bad-segre-cube-diagonal-carrier-first-variation.md"
FULL_ONE_CELL_PATH = (
    "computations/verify_n8_one_bad_segre_cube_four_residual_units.py"
)
FULL_ONE_CELL_NOTE = "notes/n8-one-bad-segre-cube-four-residual-units.md"
PINS = {
    FIRST_PATH:
        "477c6a05e2cc95662bea9f3909e532de2d17c88614de16795d0be6e757c130c9",
    FIRST_NOTE:
        "9aa213b0a3cb7861916f71649c1619f4953f14b3ba6c3cf2e69134628dc03a29",
    FULL_ONE_CELL_PATH:
        "a09d41c4bed6b774026395b953bc5d51e19d74f3b41ae2d513a6c6b263a4a1d0",
    FULL_ONE_CELL_NOTE:
        "376625ec69096460560b1e793087e66486c3f6a3d95271a14cec796ed248eb4d",
}
EXPECTED_DIGEST = "2cf786dacfd789f88e036fe35f76fe3d6c94d864c063eec93f169db444ebcbe9"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load_pinned(name, relative):
    path = ROOT / relative
    actual = sha256(path.read_bytes()).hexdigest()
    require(actual == PINS[relative],
            f"pinned dependency changed: {relative}: {actual}")
    spec = spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None,
            f"cannot load {relative}")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# Sparse polynomials use sorted tuples of variable indices as monomials.
# Repeated indices are retained, so multipliers may contain ordinary powers.
def convert_polynomial(polynomial):
    return {
        tuple(index for index, power in enumerate(exponent)
              for _ in range(power)): coefficient
        for exponent, coefficient in polynomial.items()
    }


def poly_add(*polynomials):
    answer = defaultdict(Fraction)
    for polynomial in polynomials:
        for monomial, coefficient in polynomial.items():
            answer[monomial] += coefficient
    return {monomial: coefficient for monomial, coefficient in answer.items()
            if coefficient}


def poly_scale(polynomial, scalar):
    scalar = Fraction(scalar)
    return {monomial: scalar * coefficient
            for monomial, coefficient in polynomial.items()
            if scalar * coefficient}


def poly_multiply(left, right):
    answer = defaultdict(Fraction)
    for left_monomial, left_coefficient in left.items():
        for right_monomial, right_coefficient in right.items():
            answer[tuple(sorted(left_monomial + right_monomial))] += (
                left_coefficient * right_coefficient
            )
    return {monomial: coefficient for monomial, coefficient in answer.items()
            if coefficient}


def cell_label(first_variation, cell):
    return first_variation.cell_label(cell)


def full_functional(first_variation):
    diagonal_unit = first_variation.load_dependency()
    source, edges, _variables, base, multipliers = first_variation.setup(
        diagonal_unit
    )
    cell_polynomials = {
        cell: convert_polynomial(polynomial)
        for cell, polynomial in base.items()
    }
    universe = {
        (edge, colours)
        for edge in edges
        for colours in itertools.product(range(3), repeat=2)
    }
    missing = tuple(sorted(universe - set(base)))
    require(len(missing) == 76, "full decorated deformation count changed")
    for index, cell in enumerate(missing, 45):
        cell_polynomials[cell] = {(index,): Fraction(1)}
    require(len(cell_polynomials) == 135,
            "full decorated K6 cell count changed")

    def coefficient(word):
        terms = []
        for matching in source.MATCHINGS:
            factors = (
                cell_polynomials[(edge, (word[edge[0]], word[edge[1]]))]
                for edge in matching
            )
            terms.append(reduce(poly_multiply, factors,
                                {(): Fraction(1)}))
        return poly_add(*terms)

    pure = coefficient((0,) * 6)
    reconstruction = []
    for word_label, multiplier in multipliers.items():
        reconstruction.append(poly_multiply(
            convert_polynomial(multiplier),
            coefficient(tuple(map(int, word_label))),
        ))
    functional = poly_add(
        pure, *(poly_scale(term, -1) for term in reconstruction)
    )
    return source, edges, missing, functional


def audit_full_remainder(first_variation):
    source, edges, missing, functional = full_functional(first_variation)
    labels = {
        45 + index: cell_label(first_variation, cell)
        for index, cell in enumerate(missing)
    }
    missing_degree = Counter()
    used_cells = Counter()
    pair_groups = Counter()
    for monomial in functional:
        missing_variables = tuple(index for index in monomial if index >= 45)
        missing_degree[len(missing_variables)] += 1
        cell_names = tuple(labels[index] for index in missing_variables)
        used_cells.update(cell_names)
        if len(cell_names) == 2:
            pair_groups[cell_names] += 1

    require(len(functional) == 129
            and missing_degree == Counter({1: 99, 2: 30}),
            f"full transgression degree ledger changed: {missing_degree}")
    require(len(used_cells) == 17,
            f"full transgression cell count changed: {len(used_cells)}")

    expected_pairs = {
        ("02:10", "14:02"): 4,
        ("02:20", "15:01"): 4,
        ("03:10", "12:02"): 2,
        ("03:10", "14:02"): 4,
        ("03:20", "15:01"): 4,
        ("04:10", "12:02"): 2,
        ("04:20", "15:01"): 4,
        ("05:10", "12:02"): 2,
        ("05:10", "14:02"): 4,
    }
    require(dict(pair_groups) == expected_pairs,
            f"quadratic critical-pair graph changed: {pair_groups}")

    inherited = first_variation.audit_first_variation(
        first_variation.load_dependency()
    )
    first_order = {
        label for label, _count in
        inherited["dangerous_cells_and_term_counts"]
    }
    require(len(first_order) == 16
            and set(used_cells) - first_order == {"12:02"},
            "the unique tangent-invisible quadratic cell changed")

    # Isolate x=03:10, y=12:02.  The two monomials are exactly
    # -x*y*d45*d02*d13 and -x*y*d45*d03*d12.
    index_by_label = {label: index for index, label in labels.items()}
    x_index = index_by_label["03:10"]
    y_index = index_by_label["12:02"]
    selected = {
        monomial: coefficient for monomial, coefficient in functional.items()
        if tuple(index for index in monomial if index >= 45)
        == (x_index, y_index)
    }
    expected_selected = {
        tuple(sorted((1, 6, 14, x_index, y_index))): Fraction(-1),
        tuple(sorted((2, 5, 14, x_index, y_index))): Fraction(-1),
    }
    require(selected == expected_selected,
            f"hidden Hessian-pair coefficient changed: {selected}")

    matching = ((0, 3), (1, 2), (4, 5))
    require(matching in source.MATCHINGS,
            "hidden pair stopped completing the literal perfect matching")

    return {
        "full_source_cells": 135,
        "fixed_H_cells": 14,
        "diagonal_variables": 45,
        "remaining_deformation_variables": 76,
        "functional_terms": len(functional),
        "deformation_degree_histogram": {
            str(degree): count for degree, count in sorted(missing_degree.items())
        },
        "first_order_cells": len(first_order),
        "all_order_cells_in_functional": len(used_cells),
        "unique_first_order_invisible_cell": "12:02",
        "quadratic_pair_groups": {
            "*".join(pair): count for pair, count in expected_pairs.items()
        },
        "smallest_hidden_pair": {
            "cells": ["03:10", "12:02"],
            "mixed_word": "102000",
            "physical_matching": ["03", "12", "45"],
            "third_cofactor": "J_{03,12,45}=1",
            "coefficient": (
                "-x_03:10*x_12:02*d45*(d02*d13+d03*d12)"
            ),
        },
    }


def main():
    first_variation = load_pinned("segre_first_variation", FIRST_PATH)
    require(sha256((ROOT / FIRST_NOTE).read_bytes()).hexdigest()
            == PINS[FIRST_NOTE], "first-variation note changed")
    # Pin the complete one-coordinate theorem as the scope boundary.  It is
    # not imported because this checker expands the full decorated source at
    # once rather than replaying any one-cell chart.
    require(sha256((ROOT / FULL_ONE_CELL_PATH).read_bytes()).hexdigest()
            == PINS[FULL_ONE_CELL_PATH], "one-cell unit checker changed")
    require(sha256((ROOT / FULL_ONE_CELL_NOTE).read_bytes()).hexdigest()
            == PINS[FULL_ONE_CELL_NOTE], "one-cell unit note changed")
    audit = audit_full_remainder(first_variation)
    ledger = {
        "pins": PINS,
        "full_deformation_transgression": audit,
        "verdict": (
            "one-cell Segre closure does not globalize by an independent-"
            "direction initial order: common-q provenance creates nine "
            "quadratic critical-pair classes, including one direction that "
            "is completely invisible at first order"
        ),
        "exact_next_stratification": (
            "separate the permanent factor d02*d13+d03*d12; off its zero "
            "locus the 03:10/12:02 Hessian pair is active, while on its zero "
            "locus a permanent-null matching exchange is required"
        ),
        "scope": (
            "exact full-source six-row transgression and structural initial-"
            "form counterguard; not a two-cell feasibility enumeration and "
            "not a one-bad source or conjecture counterexample"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    require(EXPECTED_DIGEST != "TO_BE_FILLED", "pin EXPECTED_DIGEST")
    require(digest == EXPECTED_DIGEST,
            ("full-deformation critical-pair ledger changed", digest))
    print("N=8 Segre full-deformation critical pair: PASS")
    print("six-row remainder: 99 linear + 30 quadratic terms")
    print("hidden direction 12:02 enters only through common-q Hessian pairs")
    print("smallest pair: 03:10*12:02 with permanent factor")
    print("ledger sha256:", digest)


if __name__ == "__main__":
    main()
