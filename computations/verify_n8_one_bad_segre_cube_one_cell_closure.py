#!/usr/bin/env python3
"""Close 72 of 76 one-cell deformations of the diagonal-carrier chart.

Sixty missing decorated cells leave the pinned six-row certificate unchanged.
For twelve of the sixteen nonzero first variations, this checker verifies one
of six alternative integral coefficient identities.  Exactly four endpoint
star directions remain outside this exact one-cell closure.
"""

from __future__ import annotations

from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEPENDENCY = (
    "computations/"
    "verify_n8_one_bad_segre_cube_diagonal_carrier_first_variation.py"
)
DEPENDENCY_SHA256 = (
    "477c6a05e2cc95662bea9f3909e532de2d17c88614de16795d0be6e757c130c9"
)
EXPECTED_DIGEST = "34739364d22a61e3ccb31100cf6c82523fab51a89316a354d1af3607779f897b"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load_dependency():
    path = ROOT / DEPENDENCY
    actual = sha256(path.read_bytes()).hexdigest()
    require(actual == DEPENDENCY_SHA256,
            f"dependency changed: {DEPENDENCY}: {actual}")
    spec = spec_from_file_location("first_variation", path)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def parse_cell(label):
    return ((int(label[0]), int(label[1])),
            (int(label[3]), int(label[4])))


R1 = (
    (1, "000001", (11,)), (-1, "000020", (10,)),
    (1, "000100", (9,)),
    (-1, "102000", (1, 7)), (-1, "102000", (3, 5)),
    (-1, "200001", (1, 7)), (1, "200001", (1, 8)),
    (-1, "200001", (3, 5)), (1, "200001", (4, 5)),
    (1, "200100", (1, 6)), (1, "200100", (1, 7)),
    (1, "200100", (2, 5)), (1, "200100", (3, 5)),
)
R2 = (
    (1, "000001", (11,)), (-1, "000020", (10,)),
    (1, "000100", (9,)),
    (-1, "100020", (1, 7)), (-1, "100020", (3, 5)),
    (1, "200001", (1, 8)), (1, "200001", (4, 5)),
    (1, "200100", (1, 6)), (1, "200100", (2, 5)),
)
R3 = (
    (1, "000001", (9,)), (1, "000001", (11,)),
    (-1, "000020", (9,)), (-1, "000020", (10,)),
    (1, "002000", (9,)),
    (-1, "100020", (1, 6)), (-1, "100020", (1, 7)),
    (-1, "100020", (2, 5)), (-1, "100020", (3, 5)),
    (1, "102000", (1, 6)), (1, "102000", (2, 5)),
    (1, "200001", (1, 6)), (1, "200001", (1, 8)),
    (1, "200001", (2, 5)), (1, "200001", (4, 5)),
)
R4 = (
    (1, "000001", (11,)), (-1, "000020", (10,)),
    (1, "000100", (9,)),
    (-1, "100020", (1, 7)), (1, "100020", (1, 8)),
    (-1, "100020", (3, 5)), (1, "100020", (4, 5)),
    (-1, "102000", (1, 8)), (-1, "102000", (4, 5)),
    (1, "200100", (1, 6)), (1, "200100", (1, 8)),
    (1, "200100", (2, 5)), (1, "200100", (4, 5)),
)
R5 = (
    (-1, "000001", (10,)), (1, "000001", (11,)),
    (1, "000100", (9,)), (1, "000100", (10,)),
    (-1, "002000", (10,)),
    (-1, "100020", (1, 6)), (-1, "100020", (1, 7)),
    (-1, "100020", (2, 5)), (-1, "100020", (3, 5)),
    (1, "102000", (1, 6)), (1, "102000", (2, 5)),
    (1, "200001", (1, 6)), (1, "200001", (1, 8)),
    (1, "200001", (2, 5)), (1, "200001", (4, 5)),
)
R6 = (
    (-1, "000020", (10,)), (1, "000020", (11,)),
    (1, "000100", (9,)), (1, "000100", (11,)),
    (-1, "002000", (11,)),
    (-1, "100020", (1, 6)), (-1, "100020", (1, 7)),
    (-1, "100020", (2, 5)), (-1, "100020", (3, 5)),
    (1, "102000", (1, 6)), (1, "102000", (2, 5)),
    (1, "200001", (1, 6)), (1, "200001", (1, 8)),
    (1, "200001", (2, 5)), (1, "200001", (4, 5)),
)

RECIPE_GROUPS = {
    "R1": (("02:10", "04:12"), R1),
    "R2": (("02:12", "04:10"), R2),
    "R3": (("03:01", "13:01"), R3),
    "R4": (("03:20", "05:21"), R4),
    "R5": (("04:02", "14:02"), R5),
    "R6": (("05:01", "15:01"), R6),
}
REMAINING = ("02:20", "03:10", "04:20", "05:10")


def verify_recipe(first_variation, source, variables, base,
                  cell_label, recipe):
    support = dict(base)
    support[parse_cell(cell_label)] = variables[45]
    coefficients = {}
    for _sign, word_label, _multiplier in recipe:
        if word_label not in coefficients:
            coefficients[word_label] = first_variation.coefficient(
                source, support, tuple(map(int, word_label))
            )
    terms = []
    for sign, word_label, multiplier in recipe:
        factor = first_variation.poly_product(
            variables[index] for index in multiplier
        )
        terms.append(first_variation.poly_scale(
            first_variation.poly_mul(factor, coefficients[word_label]), sign
        ))
    reconstructed = first_variation.poly_add(*terms)
    pure = first_variation.coefficient(source, support, (0,) * 6)
    require(reconstructed == pure,
            f"the alternative unit for {cell_label} changed")
    return {
        "recipe_terms": len(recipe),
        "mixed_words": len(coefficients),
    }


def audit_one_cell_closure(first_variation):
    diagonal_unit = first_variation.load_dependency()
    source, _edges, variables, base, _multipliers = first_variation.setup(
        diagonal_unit
    )
    first_ledger = first_variation.audit_first_variation(diagonal_unit)
    require(first_ledger["invisible_first_variations"] == 60,
            "the inherited invisible-direction count changed")

    certificates = {}
    closed = []
    for group, (cells, recipe) in RECIPE_GROUPS.items():
        certificates[group] = {
            "cells": list(cells),
            "audits": {
                cell: verify_recipe(first_variation, source, variables, base,
                                    cell, recipe)
                for cell in cells
            },
        }
        closed.extend(cells)
    require(len(closed) == 12 and len(set(closed)) == 12,
            "the alternative-certificate coverage changed")

    inherited_dangerous = {
        cell for cell, _terms in
        first_ledger["dangerous_cells_and_term_counts"]
    }
    require(inherited_dangerous - set(closed) == set(REMAINING),
            "the four residual endpoint directions changed")
    return {
        "missing_cell_directions": 76,
        "closed_by_original_certificate": 60,
        "closed_by_alternative_certificates": len(closed),
        "total_exactly_closed": 60 + len(closed),
        "alternative_recipe_groups": certificates,
        "remaining_directions": list(REMAINING),
        "verdict": (
            "72 of 76 one-cell deformations of the diagonal-carrier chart "
            "are top-empty by explicit integral mixed-row certificates; "
            "only four site-0 outgoing one-zero-endpoint directions remain"
        ),
    }


def main():
    first_variation = load_dependency()
    ledger = {
        "dependency": {"path": DEPENDENCY, "sha256": DEPENDENCY_SHA256},
        "one_cell_closure": audit_one_cell_closure(first_variation),
        "scope": (
            "one added decorated coordinate at a time around the full "
            "diagonal-carrier chart; the four listed directions and all "
            "simultaneous multi-coordinate deformations remain open"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_DIGEST != "TO_BE_FILLED":
        require(digest == EXPECTED_DIGEST,
                f"one-cell closure ledger changed: {digest}")
    print("N=8 Segre-K4 one-cell closure: PASS")
    print("one-cell directions: 76 = 72 closed + 4 residual")
    print("residual: 02:20, 03:10, 04:20, 05:10")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
