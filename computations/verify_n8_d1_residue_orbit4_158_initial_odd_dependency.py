#!/usr/bin/env python3
"""Three-row initial odd-character dependency on a 158-cell O4 face."""

from __future__ import annotations

import hashlib
import importlib
import itertools
import os
import sys
from time import monotonic

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


PINNED = {
    "verify_n8_d1_residue_orbit4_158_direct_batch.py":
        "8bed466723fe37da34136f4c10f5d49e866984effddcb69b56dbdf0bbde6335e",
    "verify_n8_d1_residue_orbit4_158_second_layer_collision.py":
        "5c47e1e72874afcc70ae7e4646e9f20acb2ba3a51a6b36c9451cc24ed1a0c4fa",
}
for filename, expected in PINNED.items():
    with open(os.path.join(HERE, filename), "rb") as handle:
        require(hashlib.sha256(handle.read()).hexdigest() == expected,
                "a pinned odd-dependency source changed: " + filename)

B = importlib.import_module("verify_n8_d1_residue_orbit4_158_direct_batch")
X = importlib.import_module(
    "verify_n8_d1_residue_orbit4_158_second_layer_collision"
)
E, Q, C, D = B.E, B.Q, B.C, B.D

MISSING = (
    (0, 1, 0, 1), (0, 1, 1, 0), (0, 2, 1, 0),
    (0, 4, 0, 1), (0, 4, 1, 0),
    (0, 5, 0, 1), (0, 5, 1, 0),
    (0, 6, 0, 1), (0, 6, 1, 0),
    (0, 7, 0, 0), (0, 7, 0, 1), (0, 7, 1, 0), (0, 7, 1, 1),
    (1, 2, 0, 1), (1, 3, 1, 0),
    (1, 6, 0, 0), (1, 6, 0, 1), (1, 6, 1, 0), (1, 6, 1, 1),
    (1, 7, 0, 1), (1, 7, 1, 0),
    (2, 7, 0, 0), (2, 7, 0, 1), (2, 7, 1, 0), (2, 7, 1, 1),
    (2, 7, 2, 0), (2, 7, 2, 1),
    (3, 6, 0, 0), (3, 6, 0, 1), (3, 6, 1, 0), (3, 6, 1, 1),
    (3, 6, 2, 0), (3, 6, 2, 1),
    (3, 7, 1, 0), (3, 7, 1, 2),
)
GENERATOR_SHA256 = (
    "0071007004727dd4494b00f05880c257037ddb384c34d5ed367042398cce70c6"
)
EXPECTED_LEDGER_SHA256 = (
    "53671344333efe3a3f4616fc1ff2cbb780060a31d43095fe9a243d0eb4484e0f"
)


def certificate_input():
    support = Q.allowed_support() - set(MISSING)
    records = C.coefficient_generators(support)
    require(len(support) == 158 and len(records) == 4102
            and D.content_hash(records) == GENERATOR_SHA256,
            "the initial-odd 158-cell coefficient input changed")
    rows = B.initial_rows(records)
    basis, dependencies = E.L.integer_laurent_basis(rows)
    bad = [dependency for dependency in dependencies
           if E.row_character(dependency, rows) != 1]
    require(len(rows) == 74 and len(basis) == 26 and len(dependencies) == 48
            and bad == [{73: 1, 72: -1, 1: 1}],
            "the initial odd dependency changed")
    base_relations = X.base_relations(records, rows)
    relation = E.relation_from_representation(bad[0], base_relations)
    require(relation["difference"] == () and relation["constant"] == -1,
            "the odd dependency stopped being a constant relation")
    target = E.laurent_monomial((), 2)
    require(E.evaluate_certificate(relation["certificate"], records) == target,
            "the three-row Laurent constant identity failed")
    ordinary = X.clear_to_saturation(
        relation["certificate"], target, support, records
    )
    require(ordinary == {
        "source_records": [2309, 3459, 3549],
        "laurent_cofactor_terms": 3,
        "clearing_monomial": [
            ["x_02_11", 1], ["x_04_11", 1], ["x_05_11", 1],
            ["x_14_00", 1], ["x_26_00", 1], ["x_37_01", 1],
            ["x_56_00", 1],
        ],
        "ordinary_saturation_power": 1,
        "ordinary_cofactor_terms": 3,
        "ordinary_certificate_sha256":
            "480139f1756c768de2ae4067404656154bb975fab027e058c937510ddc43d406",
        "integral_coefficients": False,
    }, "the initial odd ordinary certificate changed")
    witnesses = E.source_witnesses(
        records, tuple(ordinary["source_records"])
    )
    require(len(witnesses) == 10 and set(witnesses) <= support,
            "an initial-odd source witness changed")
    return support, records, rows, bad[0], ordinary, witnesses


def transported_clause_audit():
    *_, witnesses = certificate_input()
    allowed = Q.allowed_support()
    clauses = {}
    actions = 0
    for site_permutation in itertools.permutations(Q.V.SITES):
        for colour_permutation in itertools.permutations(Q.V.COLORS):
            if {Q.transform_cell(cell, site_permutation, colour_permutation)
                for cell in allowed} != set(allowed):
                continue
            actions += 1
            positive = tuple(sorted(
                Q.transform_cell(cell, site_permutation, colour_permutation)
                for cell in MISSING
            ))
            negative = tuple(sorted(
                Q.transform_cell(cell, site_permutation, colour_permutation)
                for cell in witnesses
            ))
            clauses.setdefault((positive, negative), 0)
            clauses[(positive, negative)] += 1
    require(actions == 8 and len(clauses) == 4
            and set(clauses.values()) == {2},
            "the initial-odd face-clause orbit changed")
    return [{
        "positive_cells": [list(cell) for cell in positive],
        "negative_cells": [list(cell) for cell in negative],
        "transport_multiplicity": multiplicity,
    } for (positive, negative), multiplicity in sorted(clauses.items())]


def audit():
    started = monotonic()
    support, records, rows, dependency, ordinary, witnesses = certificate_input()
    transported = transported_clause_audit()
    ledger = {
        "pinned_sources": PINNED,
        "localized_cells": len(support),
        "complete_shadow": C.support_shadow_audit(support),
        "coefficient_generators": len(records),
        "generator_sha256": D.content_hash(records),
        "first_character_profile": [len(rows), 26, 48],
        "odd_dependency": dict(sorted(dependency.items())),
        "ordinary_saturation_certificate": ordinary,
        "localized_source_witnesses": [list(cell) for cell in witnesses],
        "distinct_transported_clauses": transported,
        "characteristic_scope": "every characteristic except two",
        "status": "158-cell face is empty by an initial three-row odd dependency",
    }
    return ledger, D.content_hash(ledger), monotonic() - started


def main():
    ledger, digest, elapsed = audit()
    if EXPECTED_LEDGER_SHA256 == "TO_BE_FROZEN":
        print("ledger sha256:", digest)
    else:
        require(digest == EXPECTED_LEDGER_SHA256,
                "the initial odd-dependency ledger changed")
        print("ledger sha256 (frozen):", digest)
    print("odd dependency:", ledger["odd_dependency"])
    print("ordinary saturation: U^%d" % ledger[
        "ordinary_saturation_certificate"
    ]["ordinary_saturation_power"])
    print("elapsed: %.2fs" % elapsed)


if __name__ == "__main__":
    main()
