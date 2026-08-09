#!/usr/bin/env python3
"""Quotient-character oracle on the fourth 158-cell O4 frontier."""

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
                "a pinned quotient-character source changed: " + filename)

B = importlib.import_module("verify_n8_d1_residue_orbit4_158_direct_batch")
E = importlib.import_module(
    "verify_n8_d1_residue_orbit4_second_incidence_frontier_iterated_laurent"
)
Q, C, D = B.Q, B.C, B.D

MISSING = (
    (0, 1, 0, 1), (0, 1, 1, 0),
    (0, 3, 0, 1), (0, 3, 1, 0),
    (0, 4, 0, 1), (0, 4, 1, 0),
    (0, 5, 0, 1), (0, 5, 1, 0), (0, 6, 1, 0),
    (0, 7, 0, 0), (0, 7, 0, 1), (0, 7, 1, 0), (0, 7, 1, 1),
    (1, 2, 0, 1),
    (1, 6, 0, 0), (1, 6, 0, 1), (1, 6, 1, 0), (1, 6, 1, 1),
    (1, 7, 0, 1), (1, 7, 1, 0),
    (2, 6, 0, 1), (2, 6, 0, 2), (2, 6, 2, 1),
    (2, 7, 0, 0), (2, 7, 0, 1), (2, 7, 1, 0), (2, 7, 1, 1),
    (2, 7, 2, 0), (2, 7, 2, 1),
    (3, 6, 0, 0), (3, 6, 0, 1), (3, 6, 1, 0), (3, 6, 1, 1),
    (3, 6, 2, 0), (3, 6, 2, 1),
)
GENERATOR_SHA256 = (
    "345cb777174369a09e5de06d019d5b7ce6363fc132943b5aa1d5ef5c41aa0aa8"
)
TERMINAL_RECORD = 2771
EXPECTED_LEDGER_SHA256 = (
    "8998b5d90e122b8cec710200f72adc916f35155915e5e6fc2bb8fd1b100fd7a9"
)


def certificate_input():
    support = Q.allowed_support() - set(MISSING)
    records = C.coefficient_generators(support)
    require(len(support) == 158 and len(records) == 4321
            and D.content_hash(records) == GENERATOR_SHA256,
            "the fourth 158-cell coefficient input changed")
    rows = B.initial_rows(records)
    basis, dependencies = E.L.integer_laurent_basis(rows)
    require(len(rows) == 54 and len(basis) == 20 and len(dependencies) == 34
            and all(E.row_character(dependency, rows) == 1
                    for dependency in dependencies),
            "the fourth 158-cell first character changed")
    basis_characters = {
        pivot: E.row_character(representation, rows)
        for pivot, (_basis_row, representation) in basis.items()
    }
    histogram = Counter()
    one_class = []
    graph_edges = []
    terminal = None
    for record_index, record in enumerate(records):
        reduced, traces, parents = E.reduce_record(
            record, basis, basis_characters
        )
        histogram[len(reduced)] += 1
        if len(reduced) == 1:
            one_class.append(record_index)
        if len(reduced) == 2:
            (first, first_coefficient), (second, second_coefficient) = sorted(
                reduced.items()
            )
            difference, constant = E.canonical_row(
                E.exponent_difference(first, second),
                -second_coefficient / first_coefficient,
            )
            graph_edges.append((record_index, difference, constant))
        if record_index == TERMINAL_RECORD:
            terminal = {
                "iteration": 0,
                "source_record": record_index,
                "normal_form": E.polynomial_trace(reduced),
                "parents": sorted(parents),
                "traces": traces,
            }
    require(len(one_class) == 12 and one_class[0] == TERMINAL_RECORD,
            "the fourth-face one-class census changed")
    require(terminal["normal_form"] == [[
        [["x_05_11", 1], ["x_15_02", 1], ["x_26_10", 1],
         ["x_37_01", 1], ["x_47_02", 1], ["x_57_22", -1]],
        "1",
    ]], "the fourth-face terminal monomial changed")

    by_difference = {}
    parallel_collisions = []
    for record_index, difference, constant in graph_edges:
        if (difference in by_difference
                and by_difference[difference][1] != constant):
            parallel_collisions.append([
                by_difference[difference][0], record_index,
                str(by_difference[difference][1]), str(constant),
            ])
        else:
            by_difference[difference] = (record_index, constant)
    require(len(graph_edges) == 475 and len(by_difference) == 35
            and len(parallel_collisions) == 12,
            "the quotient-character multigraph changed")

    ordinary = E.ordinary_saturation_certificate(
        records, rows, terminal, support
    )
    require(ordinary == {
        "source_records": [2771, 3416, 3417, 3445, 3448],
        "laurent_cofactor_terms": 10,
        "clearing_monomial": [
            ["x_02_22", 1], ["x_13_22", 1], ["x_46_00", 1],
            ["x_47_02", 1], ["x_56_10", 1], ["x_57_22", 2],
        ],
        "ordinary_saturation_power": 2,
        "ordinary_cofactor_terms": 10,
        "ordinary_certificate_sha256":
            "9610d372b848e6c1cab957f02f22d3e62f1a2dcd08bac4a4d4a794ba9a7e43df",
    }, "the fourth-face ordinary U^2 certificate changed")
    witnesses = E.source_witnesses(
        records, tuple(ordinary["source_records"])
    )
    require(len(witnesses) == 15 and set(witnesses) <= support,
            "a fourth-face source witness is not localized")
    return (support, records, rows, histogram, one_class, graph_edges,
            parallel_collisions, terminal, ordinary, witnesses)


def transported_clause_audit():
    *_, witnesses = certificate_input()
    return E.transform_clauses(set(MISSING), set(witnesses))


def audit():
    started = monotonic()
    (support, records, rows, histogram, one_class, graph_edges,
     collisions, terminal, ordinary, witnesses) = certificate_input()
    transported = E.transform_clauses(set(MISSING), set(witnesses))
    require(len(transported) == 8, "the fourth-face transport orbit changed")
    ledger = {
        "pinned_sources": PINNED,
        "localized_cells": len(support),
        "complete_shadow": C.support_shadow_audit(support),
        "coefficient_generators": len(records),
        "generator_sha256": D.content_hash(records),
        "first_character": {
            "plus_rows": len(rows), "rank": 20,
            "dependencies": 34, "inconsistent_dependencies": 0,
        },
        "reduced_histogram_sha256": D.content_hash({
            str(classes): count for classes, count in sorted(histogram.items())
        }),
        "one_class_generators": one_class,
        "quotient_character_graph": {
            "two_class_edges": len(graph_edges),
            "distinct_displacements": 35,
            "opposite_character_parallel_edges": collisions,
        },
        "selected_terminal": {
            "source_record": terminal["source_record"],
            "normal_form": terminal["normal_form"],
        },
        "ordinary_saturation_certificate": ordinary,
        "localized_source_witnesses": [list(cell) for cell in witnesses],
        "distinct_transported_clauses": transported,
        "characteristic_scope": "every characteristic",
        "status": "fourth 158-cell face is empty by direct U^2",
    }
    return ledger, D.content_hash(ledger), monotonic() - started


def main():
    ledger, digest, elapsed = audit()
    if EXPECTED_LEDGER_SHA256 == "TO_BE_FROZEN":
        print("ledger sha256:", digest)
    else:
        require(digest == EXPECTED_LEDGER_SHA256,
                "the fourth-face quotient-character ledger changed")
        print("ledger sha256 (frozen):", digest)
    print("one-class generators:", len(ledger["one_class_generators"]))
    print("parallel collisions:", len(ledger[
        "quotient_character_graph"
    ]["opposite_character_parallel_edges"]))
    print("ordinary saturation: U^%d" % ledger[
        "ordinary_saturation_certificate"
    ]["ordinary_saturation_power"])
    print("elapsed: %.2fs" % elapsed)


if __name__ == "__main__":
    main()
