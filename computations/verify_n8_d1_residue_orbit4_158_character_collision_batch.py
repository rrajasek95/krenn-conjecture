#!/usr/bin/env python3
"""Checked quotient-character collision on a later 158-cell O4 face."""

from __future__ import annotations

import hashlib
import importlib
import os
import sys
from collections import Counter
from fractions import Fraction
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
                "a pinned character-collision source changed: " + filename)

B = importlib.import_module("verify_n8_d1_residue_orbit4_158_direct_batch")
X = importlib.import_module(
    "verify_n8_d1_residue_orbit4_158_second_layer_collision"
)
E, Q, C, D = B.E, B.Q, B.C, B.D

MISSING = (
    (0, 1, 0, 1), (0, 1, 1, 0), (0, 2, 1, 0), (0, 3, 0, 1),
    (0, 4, 0, 1), (0, 4, 1, 0),
    (0, 5, 0, 1), (0, 5, 1, 0),
    (0, 6, 0, 1), (0, 6, 1, 0),
    (0, 7, 0, 0), (0, 7, 0, 1), (0, 7, 1, 0), (0, 7, 1, 1),
    (1, 2, 0, 1), (1, 3, 1, 0),
    (1, 6, 0, 0), (1, 6, 0, 1), (1, 6, 1, 0), (1, 6, 1, 1),
    (1, 7, 1, 0),
    (2, 7, 0, 0), (2, 7, 0, 1), (2, 7, 1, 0), (2, 7, 1, 1),
    (2, 7, 2, 0), (2, 7, 2, 1),
    (3, 6, 0, 0), (3, 6, 0, 1), (3, 6, 1, 0), (3, 6, 1, 1),
    (3, 6, 2, 0), (3, 6, 2, 1),
    (3, 7, 0, 1), (3, 7, 2, 1),
)
GENERATOR_SHA256 = (
    "acae4d2eafa8dcaa93a9c226d002ba8b787e7f454259662a10117dcf334f5d33"
)
COLLISION_RECORDS = (1260, 1269)
EXPECTED_LEDGER_SHA256 = (
    "06a02e65dba6fe21ef874cf10d7fd03e80d523deb47b7a9dfbe11bfc63f09d6b"
)


def certificate_input():
    support = Q.allowed_support() - set(MISSING)
    records = C.coefficient_generators(support)
    require(len(support) == 158 and len(records) == 4321
            and D.content_hash(records) == GENERATOR_SHA256,
            "the later collision face changed")
    rows = B.initial_rows(records)
    basis, dependencies = E.L.integer_laurent_basis(rows)
    require(len(rows) == 72 and len(basis) == 25 and len(dependencies) == 47
            and all(E.row_character(dependency, rows) == 1
                    for dependency in dependencies),
            "the later collision first character changed")
    basis_characters = {
        pivot: E.row_character(representation, rows)
        for pivot, (_basis_row, representation) in basis.items()
    }
    one_class = []
    two_class = []
    selected = []
    for record_index, record in enumerate(records):
        reduced, traces, parents = E.reduce_record(
            record, basis, basis_characters
        )
        if len(reduced) == 1:
            one_class.append(record_index)
        if len(reduced) == 2:
            two_class.append(record_index)
        if record_index in COLLISION_RECORDS:
            selected.append((record_index, reduced, traces, parents))
    require(not one_class and len(two_class) == 256,
            "the later collision reduced-class census changed")
    require([row[0] for row in selected] == list(COLLISION_RECORDS),
            "the selected collision records changed")

    relations = X.base_relations(records, rows)
    certificates = [
        X.reduced_certificate(
            records, rows, basis, relations,
            record_index, reduced, traces,
        )
        for record_index, reduced, traces, _parents in selected
    ]
    first = selected[0][1]
    second = selected[1][1]
    require([str(value) for _monomial, value in sorted(first.items())]
            == ["1", "1"]
            and [str(value) for _monomial, value in sorted(second.items())]
            == ["-1", "1"],
            "the later opposite characters changed")
    first_lead = sorted(first)[0]
    second_lead = sorted(second)[0]
    scale = E.exponent_add(
        second_lead, E.exponent_scale(first_lead, -1)
    )
    combined = E.certificate_add(
        E.certificate_mul(certificates[0], E.laurent_monomial(scale)),
        certificates[1],
    )
    target = E.laurent_add(
        E.laurent_mul(first, E.laurent_monomial(scale)), second
    )
    require(len(target) == 1
            and next(iter(target.values())) == Fraction(2),
            "the later collision did not isolate twice a monomial")
    require(E.evaluate_certificate(combined, records) == target,
            "the expanded later collision identity failed")
    ordinary = X.clear_to_saturation(
        combined, target, support, records
    )
    require(ordinary == {
        "source_records": [
            1260, 1269, 1272, 3037, 3038, 3039, 3040,
            3041, 3042, 3046, 3166, 3169, 3172,
        ],
        "laurent_cofactor_terms": 39,
        "clearing_monomial": [
            ["x_02_00", 1], ["x_02_22", 1], ["x_04_00", 1],
            ["x_13_22", 1], ["x_37_20", 1], ["x_46_00", 1],
            ["x_47_02", 2], ["x_56_00", 1], ["x_56_01", 1],
            ["x_56_10", 1], ["x_56_11", 1], ["x_57_12", 1],
            ["x_57_22", 2],
        ],
        "ordinary_saturation_power": 2,
        "ordinary_cofactor_terms": 39,
        "ordinary_certificate_sha256":
            "65256e5c40aa73b2568f6937815f8fefb2505f835b56f2a9d84335d9328370b8",
        "integral_coefficients": False,
    }, "the later ordinary collision certificate changed")
    witnesses = E.source_witnesses(
        records, tuple(ordinary["source_records"])
    )
    require(len(witnesses) == 28 and set(witnesses) <= support,
            "a later collision source witness changed")
    return support, records, rows, first, second, scale, ordinary, witnesses


def transported_clause_audit():
    *_, witnesses = certificate_input()
    return E.transform_clauses(set(MISSING), set(witnesses))


def audit():
    started = monotonic()
    support, records, rows, first, second, scale, ordinary, witnesses = (
        certificate_input()
    )
    transported = E.transform_clauses(set(MISSING), set(witnesses))
    require(len(transported) == 8,
            "the later collision transport orbit changed")
    ledger = {
        "pinned_sources": PINNED,
        "localized_cells": len(support),
        "complete_shadow": C.support_shadow_audit(support),
        "coefficient_generators": len(records),
        "generator_sha256": D.content_hash(records),
        "first_character_profile": [len(rows), 25, 47],
        "one_class_generators": 0,
        "two_class_generators": 256,
        "collision_records": list(COLLISION_RECORDS),
        "first_normal_form": E.polynomial_trace(first),
        "second_normal_form": E.polynomial_trace(second),
        "aligning_laurent_monomial": [[name, exponent]
                                      for name, exponent in scale],
        "ordinary_saturation_certificate": ordinary,
        "localized_source_witnesses": [list(cell) for cell in witnesses],
        "distinct_transported_clauses": transported,
        "characteristic_scope": "every characteristic except two",
        "status": "later 158-cell face is empty by quotient-edge collision",
    }
    return ledger, D.content_hash(ledger), monotonic() - started


def main():
    ledger, digest, elapsed = audit()
    if EXPECTED_LEDGER_SHA256 == "TO_BE_FROZEN":
        print("ledger sha256:", digest)
    else:
        require(digest == EXPECTED_LEDGER_SHA256,
                "the later 158-cell collision ledger changed")
        print("ledger sha256 (frozen):", digest)
    print("collision records:", ledger["collision_records"])
    print("ordinary saturation: U^%d" % ledger[
        "ordinary_saturation_certificate"
    ]["ordinary_saturation_power"])
    print("elapsed: %.2fs" % elapsed)


if __name__ == "__main__":
    main()
