#!/usr/bin/env python3
"""Two direct U^1 closures and the first open 158-cell O4 frontier."""

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


PINNED_ENGINE_SHA256 = (
    "290195e979282bee0029a4cf02012b79ecba2212bf87daacb2710ff9cf6edf63"
)
SOURCE = os.path.join(
    HERE,
    "verify_n8_d1_residue_orbit4_second_incidence_frontier_iterated_laurent.py",
)
with open(SOURCE, "rb") as handle:
    source_digest = hashlib.sha256(handle.read()).hexdigest()
require(source_digest == PINNED_ENGINE_SHA256,
        "the pinned ordinary Laurent-saturation engine changed")
E = importlib.import_module(
    "verify_n8_d1_residue_orbit4_second_incidence_frontier_iterated_laurent"
)
Q, C, D = E.Q, E.C, E.D

EXPECTED_LEDGER_SHA256 = (
    "f04e232f035737df78cc6e3d5b51c126719d0d58e6b33b662cb265c307f897f9"
)

CLOSED_FACES = (
    {
        "missing": (
            (0, 1, 0, 1), (0, 1, 1, 0), (0, 2, 1, 0), (0, 3, 1, 0),
            (0, 6, 0, 0), (0, 6, 0, 1), (0, 6, 1, 0), (0, 6, 1, 1),
            (0, 7, 0, 1), (0, 7, 1, 0),
            (1, 2, 0, 1), (1, 4, 0, 1), (1, 5, 0, 1), (1, 5, 1, 0),
            (1, 6, 0, 1), (1, 6, 1, 0),
            (1, 7, 0, 0), (1, 7, 0, 1), (1, 7, 1, 0), (1, 7, 1, 1),
            (2, 6, 0, 0), (2, 6, 0, 1), (2, 6, 1, 0), (2, 6, 1, 1),
            (2, 6, 2, 0), (2, 6, 2, 1),
            (3, 4, 1, 0), (3, 4, 1, 2), (3, 4, 2, 0),
            (3, 7, 0, 0), (3, 7, 0, 1), (3, 7, 1, 0), (3, 7, 1, 1),
            (3, 7, 2, 0), (3, 7, 2, 1),
        ),
        "generator_sha256":
            "3c448cdec98be6c8967fb37fafc040151d09e8fbab255adda2090b87828f8b25",
        "terminal_record": 3541,
        "source_records": [2309, 2310, 2312, 2313, 3541, 3597, 3600],
        "certificate_sha256":
            "0550d8d5257fcf5a90adae3bb0497fa8fcfbf4faf389f10e2efb4ebaca3a243a",
    },
    {
        "missing": (
            (0, 1, 0, 1), (0, 1, 1, 0), (0, 3, 1, 0),
            (0, 6, 0, 0), (0, 6, 0, 1), (0, 6, 1, 0), (0, 6, 1, 1),
            (0, 7, 0, 1), (0, 7, 1, 0),
            (1, 2, 0, 1), (1, 2, 1, 0), (1, 4, 0, 1),
            (1, 5, 0, 1), (1, 5, 1, 0), (1, 6, 0, 1), (1, 6, 1, 0),
            (1, 7, 0, 0), (1, 7, 0, 1), (1, 7, 1, 0), (1, 7, 1, 1),
            (2, 6, 0, 0), (2, 6, 0, 1), (2, 6, 1, 0), (2, 6, 1, 1),
            (2, 6, 2, 0), (2, 6, 2, 1),
            (3, 4, 1, 0), (3, 4, 1, 2), (3, 4, 2, 0),
            (3, 7, 0, 0), (3, 7, 0, 1), (3, 7, 1, 0), (3, 7, 1, 1),
            (3, 7, 2, 0), (3, 7, 2, 1),
        ),
        "generator_sha256":
            "398a4b70c3472479c6e25fbab62bd3e31924f6cb9e692640cd35a7530516a5f9",
        "terminal_record": 3613,
        "source_records": [2444, 2445, 2447, 2448, 3613, 3666, 3669],
        "certificate_sha256":
            "447a5e6277b9734f397a8a74f48bd4a2c11640f2f1657fdb2e13c0dd91242a08",
    },
)

OPEN_MISSING = (
    (0, 1, 0, 1), (0, 1, 1, 0), (0, 2, 1, 0), (0, 3, 0, 1),
    (0, 4, 0, 1), (0, 4, 1, 0), (0, 5, 0, 1), (0, 5, 1, 0),
    (0, 6, 0, 1),
    (0, 7, 0, 0), (0, 7, 0, 1), (0, 7, 1, 0), (0, 7, 1, 1),
    (1, 2, 0, 1), (1, 3, 1, 0),
    (1, 6, 0, 0), (1, 6, 0, 1), (1, 6, 1, 0), (1, 6, 1, 1),
    (1, 7, 0, 1), (1, 7, 1, 0),
    (2, 6, 1, 0), (2, 6, 2, 0),
    (2, 7, 0, 0), (2, 7, 0, 1), (2, 7, 1, 0), (2, 7, 1, 1),
    (2, 7, 2, 0), (2, 7, 2, 1),
    (3, 6, 0, 0), (3, 6, 0, 1), (3, 6, 1, 0), (3, 6, 1, 1),
    (3, 6, 2, 0), (3, 6, 2, 1),
)
OPEN_GENERATOR_SHA256 = (
    "7097b288a7a41be1fe4abb42ee8de20f49c5e69a2a1f720268ac7568b02aa9ce"
)


def initial_rows(records):
    rows, seen = [], set()
    for record_index, record in enumerate(records):
        if len(record["terms"]) != 2:
            continue
        parsed = [(tuple(monomial), Fraction(coefficient))
                  for monomial, coefficient in record["terms"]]
        if {coefficient for _monomial, coefficient in parsed} != {Fraction(1)}:
            continue
        difference = E.L.exponent_difference(parsed[0][0], parsed[1][0])
        key = E.canonical_row(difference, Fraction(-1))
        if key in seen:
            continue
        seen.add(key)
        rows.append({
            "difference": difference,
            "constant": Fraction(-1),
            "source_record": record_index,
            "parents": (),
            "iteration": 0,
            "divisor": tuple(parsed[1][0]),
        })
    return rows


def closed_face_audit(frozen):
    support = Q.allowed_support() - set(frozen["missing"])
    records = C.coefficient_generators(support)
    require(len(support) == 158 and len(records) == 4321
            and D.content_hash(records) == frozen["generator_sha256"],
            "a closed 158-cell face changed")
    rows, iterations, final = E.closure(records, frozen=False)
    require([(row["input_rows"], row["lattice_rank"], row["new_rows"])
             for row in iterations] == [(54, 20, 36)]
            and final["source_record"] == frozen["terminal_record"],
            "a closed 158-cell Laurent profile changed")
    ordinary = E.ordinary_saturation_certificate(
        records, rows, final, support
    )
    require(ordinary["source_records"] == frozen["source_records"]
            and ordinary["ordinary_saturation_power"] == 1
            and ordinary["ordinary_certificate_sha256"]
            == frozen["certificate_sha256"],
            "a closed 158-cell ordinary certificate changed")
    witnesses = E.source_witnesses(records, tuple(ordinary["source_records"]))
    require(len(witnesses) == 18 and set(witnesses) <= support,
            "a closed 158-cell witness set changed")
    return {
        "missing_cells": [list(cell) for cell in frozen["missing"]],
        "generator_sha256": frozen["generator_sha256"],
        "terminal_record": final["source_record"],
        "terminal_normal_form": final["normal_form"],
        "ordinary_certificate": ordinary,
        "localized_witnesses": [list(cell) for cell in witnesses],
    }


def open_face_audit():
    support = Q.allowed_support() - set(OPEN_MISSING)
    records = C.coefficient_generators(support)
    require(len(support) == 158 and len(records) == 4321
            and D.content_hash(records) == OPEN_GENERATOR_SHA256,
            "the first direct-Laurent-open 158-cell face changed")
    shadow = C.support_shadow_audit(support)
    rows = initial_rows(records)
    basis, dependencies = E.L.integer_laurent_basis(rows)
    require(len(rows) == 54 and len(basis) == 20 and len(dependencies) == 34
            and all(E.row_character(dependency, rows) == 1
                    for dependency in dependencies),
            "the open face signed-Laurent lattice changed")
    basis_characters = {
        pivot: E.row_character(representation, rows)
        for pivot, (_basis_row, representation) in basis.items()
    }
    histogram = Counter()
    one_class = []
    for record_index, record in enumerate(records):
        reduced, _traces, _parents = E.reduce_record(
            record, basis, basis_characters
        )
        histogram[len(reduced)] += 1
        if len(reduced) == 1:
            one_class.append(record_index)
    histogram_digest = D.content_hash({
        str(classes): count for classes, count in sorted(histogram.items())
    })
    require(not one_class
            and histogram_digest
            == "4f3ea6a53dc54f8c89e9ed8862e8592428bec07077359d888f53f974f5588c9c",
            "the open face direct-normal-form census changed")
    return {
        "missing_cells": [list(cell) for cell in OPEN_MISSING],
        "complete_shadow": shadow,
        "coefficient_generators": len(records),
        "generator_sha256": D.content_hash(records),
        "unique_plus_rows": len(rows),
        "laurent_rank": len(basis),
        "dependencies": len(dependencies),
        "odd_dependencies": 0,
        "one_class_generators": one_class,
        "reduced_histogram_sha256": histogram_digest,
        "status": "first 158-cell face not closed by direct Laurent oracle",
    }


def transported_clause_audit():
    clauses = {}
    for frozen in CLOSED_FACES:
        row = closed_face_audit(frozen)
        for clause in E.transform_clauses(
                {tuple(cell) for cell in row["missing_cells"]},
                {tuple(cell) for cell in row["localized_witnesses"]}):
            key = (tuple(tuple(cell) for cell in clause["positive_cells"]),
                   tuple(tuple(cell) for cell in clause["negative_cells"]))
            clauses[key] = clause
    require(len(clauses) == 16,
            "the two-face 158-cell clause orbit changed")
    return [clauses[key] for key in sorted(clauses)]


def audit():
    started = monotonic()
    closed = [closed_face_audit(frozen) for frozen in CLOSED_FACES]
    open_frontier = open_face_audit()
    transported = {}
    for row in closed:
        for clause in E.transform_clauses(
                {tuple(cell) for cell in row["missing_cells"]},
                {tuple(cell) for cell in row["localized_witnesses"]}):
            key = (tuple(tuple(cell) for cell in clause["positive_cells"]),
                   tuple(tuple(cell) for cell in clause["negative_cells"]))
            transported[key] = clause
    require(len(transported) == 16,
            "the two-face 158-cell clause orbit changed")
    ledger = {
        "pinned_engine_sha256": source_digest,
        "closed_direct_faces": closed,
        "distinct_transported_clauses": [
            transported[key] for key in sorted(transported)
        ],
        "first_direct_oracle_open_frontier": open_frontier,
        "characteristic_scope": "closed faces: every characteristic",
        "status": (
            "two 158-cell faces closed by integral U^1; next exact 158-cell "
            "frontier frozen after direct signed-Laurent oracle returned open"
        ),
    }
    return ledger, D.content_hash(ledger), monotonic() - started


def main():
    ledger, digest, elapsed = audit()
    if EXPECTED_LEDGER_SHA256 == "TO_BE_FROZEN":
        print("ledger sha256:", digest)
    else:
        require(digest == EXPECTED_LEDGER_SHA256,
                "the 158-cell direct-batch ledger changed")
        print("ledger sha256 (frozen):", digest)
    print("closed faces:", len(ledger["closed_direct_faces"]))
    print("transported clauses:", len(ledger["distinct_transported_clauses"]))
    print("open generator sha256:", ledger[
        "first_direct_oracle_open_frontier"
    ]["generator_sha256"])
    print("elapsed: %.2fs" % elapsed)


if __name__ == "__main__":
    main()
