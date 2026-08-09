#!/usr/bin/env python3
"""Integral direct Laurent unit on the third 158-cell O4 frontier."""

from __future__ import annotations

import hashlib
import importlib
import os
import sys
from collections import Counter
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
    "verify_n8_d1_residue_orbit4_second_incidence_frontier_iterated_laurent.py":
        "290195e979282bee0029a4cf02012b79ecba2212bf87daacb2710ff9cf6edf63",
}
for filename, expected in PINNED.items():
    with open(os.path.join(HERE, filename), "rb") as handle:
        require(hashlib.sha256(handle.read()).hexdigest() == expected,
                "a pinned direct-Laurent source changed: " + filename)

B = importlib.import_module("verify_n8_d1_residue_orbit4_158_direct_batch")
E = importlib.import_module(
    "verify_n8_d1_residue_orbit4_second_incidence_frontier_iterated_laurent"
)
Q, C, D = B.Q, B.C, B.D

MISSING = (
    (0, 1, 0, 1), (0, 1, 1, 0), (0, 3, 0, 1),
    (0, 6, 0, 0), (0, 6, 0, 1), (0, 6, 1, 0), (0, 6, 1, 1),
    (0, 7, 0, 1), (0, 7, 1, 0),
    (1, 2, 0, 1), (1, 2, 1, 0), (1, 3, 1, 0),
    (1, 4, 0, 1), (1, 5, 1, 0),
    (1, 6, 0, 1), (1, 6, 1, 0),
    (1, 7, 0, 0), (1, 7, 0, 1), (1, 7, 1, 0), (1, 7, 1, 1),
    (2, 6, 0, 0), (2, 6, 0, 1), (2, 6, 1, 0), (2, 6, 1, 1),
    (2, 6, 2, 0), (2, 6, 2, 1),
    (3, 7, 0, 0), (3, 7, 0, 1), (3, 7, 1, 0), (3, 7, 1, 1),
    (3, 7, 2, 0), (3, 7, 2, 1),
    (4, 5, 0, 1), (4, 5, 0, 2), (4, 5, 2, 1),
)
GENERATOR_SHA256 = (
    "46147d08740aa57b20c76ee2995d712f1e4615c81714f9679751ede9547b26f4"
)
TERMINAL_RECORD = 3306
EXPECTED_LEDGER_SHA256 = (
    "afd3745f077ef6d0bb08b476cb71e0374096f972c754ad91cf72005bff4fe93f"
)


def certificate_input():
    support = Q.allowed_support() - set(MISSING)
    records = C.coefficient_generators(support)
    require(len(support) == 158 and len(records) == 4321
            and D.content_hash(records) == GENERATOR_SHA256,
            "the third 158-cell coefficient input changed")
    rows = B.initial_rows(records)
    basis, dependencies = E.L.integer_laurent_basis(rows)
    require(len(rows) == 64 and len(basis) == 24 and len(dependencies) == 40
            and all(E.row_character(dependency, rows) == 1
                    for dependency in dependencies),
            "the third 158-cell signed Laurent lattice changed")
    basis_characters = {
        pivot: E.row_character(representation, rows)
        for pivot, (_basis_row, representation) in basis.items()
    }
    histogram = Counter()
    one_class = []
    terminal = None
    for record_index, record in enumerate(records):
        reduced, traces, parents = E.reduce_record(
            record, basis, basis_characters
        )
        histogram[len(reduced)] += 1
        if len(reduced) == 1:
            one_class.append(record_index)
        if record_index == TERMINAL_RECORD:
            terminal = {
                "iteration": 0,
                "source_record": record_index,
                "normal_form": E.polynomial_trace(reduced),
                "parents": sorted(parents),
                "traces": traces,
            }
    require(len(one_class) == 39 and one_class[18] == TERMINAL_RECORD,
            "the direct one-class census changed")
    require(terminal["normal_form"] == [[
        [["x_05_02", 1], ["x_14_10", 1], ["x_27_01", 1],
         ["x_36_10", 1], ["x_57_02", 1], ["x_57_22", -1]],
        "1",
    ]], "the selected integral Laurent monomial changed")
    ordinary = E.ordinary_saturation_certificate(
        records, rows, terminal, support
    )
    require(ordinary == {
        "source_records": [2413, 2415, 3306, 3360, 3366],
        "laurent_cofactor_terms": 12,
        "clearing_monomial": [
            ["x_02_22", 1], ["x_13_22", 1], ["x_46_00", 1],
            ["x_47_02", 1], ["x_56_00", 1], ["x_57_22", 2],
        ],
        "ordinary_saturation_power": 1,
        "ordinary_cofactor_terms": 12,
        "ordinary_certificate_sha256":
            "ca3febeb761d7400130b6952ecd616337f97c82eea0c4441de0aef4cbc1efcb2",
    }, "the third 158-cell ordinary certificate changed")
    witnesses = E.source_witnesses(
        records, tuple(ordinary["source_records"])
    )
    require(len(witnesses) == 15 and set(witnesses) <= support,
            "a third-face source witness is not localized")
    return support, records, rows, histogram, one_class, terminal, ordinary, witnesses


def transported_clause_audit():
    _support, _records, _rows, _histogram, _one_class, _terminal, _ordinary, witnesses = (
        certificate_input()
    )
    return E.transform_clauses(set(MISSING), set(witnesses))


def audit():
    started = monotonic()
    support, records, rows, histogram, one_class, terminal, ordinary, witnesses = (
        certificate_input()
    )
    transported = E.transform_clauses(set(MISSING), set(witnesses))
    require(len(transported) == 8,
            "the third-face transport orbit changed")
    ledger = {
        "pinned_sources": PINNED,
        "localized_cells": len(support),
        "complete_shadow": C.support_shadow_audit(support),
        "coefficient_generators": len(records),
        "generator_sha256": D.content_hash(records),
        "unique_plus_rows": len(rows),
        "laurent_rank": 24,
        "dependencies": 40,
        "odd_dependencies": 0,
        "reduced_histogram": {
            str(classes): count for classes, count in sorted(histogram.items())
        },
        "one_class_generators": one_class,
        "selected_terminal": {
            "source_record": terminal["source_record"],
            "normal_form": terminal["normal_form"],
        },
        "ordinary_saturation_certificate": ordinary,
        "localized_source_witnesses": [list(cell) for cell in witnesses],
        "distinct_transported_clauses": transported,
        "characteristic_scope": "every characteristic",
        "status": "third 158-cell O4 face is empty by integral direct U^1",
    }
    return ledger, D.content_hash(ledger), monotonic() - started


def main():
    ledger, digest, elapsed = audit()
    if EXPECTED_LEDGER_SHA256 == "TO_BE_FROZEN":
        print("ledger sha256:", digest)
    else:
        require(digest == EXPECTED_LEDGER_SHA256,
                "the third 158-cell direct-unit ledger changed")
        print("ledger sha256 (frozen):", digest)
    print("terminal record:", ledger["selected_terminal"]["source_record"])
    print("one-class generators:", len(ledger["one_class_generators"]))
    print("ordinary saturation: U^%d" % ledger[
        "ordinary_saturation_certificate"
    ]["ordinary_saturation_power"])
    print("elapsed: %.2fs" % elapsed)


if __name__ == "__main__":
    main()
