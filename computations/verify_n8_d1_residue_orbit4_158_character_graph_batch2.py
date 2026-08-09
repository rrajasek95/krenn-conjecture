#!/usr/bin/env python3
"""Checked quotient-character certificates for later 158-cell O4 faces."""

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
                "a pinned character-graph source changed: " + filename)

B = importlib.import_module("verify_n8_d1_residue_orbit4_158_direct_batch")
E = importlib.import_module(
    "verify_n8_d1_residue_orbit4_second_incidence_frontier_iterated_laurent"
)
Q, C, D = B.Q, B.C, B.D

FACES = ({
    "label": "face5",
    "missing": (
        (0, 1, 0, 1), (0, 1, 1, 0), (0, 3, 1, 0),
        (0, 6, 0, 0), (0, 6, 0, 1), (0, 6, 1, 0), (0, 6, 1, 1),
        (0, 7, 0, 1), (0, 7, 1, 0),
        (1, 2, 0, 1), (1, 2, 1, 0),
        (1, 4, 0, 1), (1, 4, 1, 0),
        (1, 5, 0, 1), (1, 5, 1, 0),
        (1, 6, 0, 1), (1, 6, 1, 0),
        (1, 7, 0, 0), (1, 7, 0, 1), (1, 7, 1, 0), (1, 7, 1, 1),
        (2, 3, 0, 1), (2, 3, 2, 1),
        (2, 6, 0, 0), (2, 6, 0, 1), (2, 6, 1, 0), (2, 6, 1, 1),
        (2, 6, 2, 0), (2, 6, 2, 1),
        (3, 7, 0, 0), (3, 7, 0, 1), (3, 7, 1, 0), (3, 7, 1, 1),
        (3, 7, 2, 0), (3, 7, 2, 1),
    ),
    "generator_sha256":
        "2f4349a736e0f3d2061b21d2635e1da5f52d3da586f9052b658bd25aad828ba1",
    "first_profile": [54, 20, 34],
    "one_class_count": 12,
    "two_class_edges": 514,
    "distinct_displacements": 38,
    "parallel_collisions": 30,
    "terminal_record": 3613,
    "terminal_normal_form": [[
        [["x_05_12", 1], ["x_14_00", 1], ["x_27_00", 1],
         ["x_36_01", 1], ["x_57_12", 1], ["x_57_22", -1]],
        "1",
    ]],
    "ordinary": {
        "source_records": [2444, 2445, 2447, 2448, 3613, 3666, 3669],
        "laurent_cofactor_terms": 12,
        "clearing_monomial": [
            ["x_02_22", 1], ["x_13_22", 1], ["x_46_00", 1],
            ["x_47_02", 1], ["x_56_10", 1], ["x_57_22", 2],
        ],
        "ordinary_saturation_power": 1,
        "ordinary_cofactor_terms": 12,
        "ordinary_certificate_sha256":
            "1591128a2837beb136645280987ea1e7846a2b0e79c763a8ca9861c3fc5aa2e7",
    },
    "witness_count": 18,
}, {
    "label": "face6",
    "missing": (
        (0, 1, 0, 1), (0, 1, 1, 0),
        (0, 3, 0, 1), (0, 3, 1, 0),
        (0, 4, 0, 1), (0, 4, 1, 0),
        (0, 5, 0, 1), (0, 5, 1, 0),
        (0, 6, 0, 1), (0, 6, 1, 0),
        (0, 7, 0, 0), (0, 7, 0, 1), (0, 7, 1, 0), (0, 7, 1, 1),
        (1, 2, 1, 0),
        (1, 6, 0, 0), (1, 6, 0, 1), (1, 6, 1, 0), (1, 6, 1, 1),
        (1, 7, 0, 1), (1, 7, 1, 0),
        (2, 6, 1, 0), (2, 6, 1, 2),
        (2, 7, 0, 0), (2, 7, 0, 1), (2, 7, 1, 0), (2, 7, 1, 1),
        (2, 7, 2, 0), (2, 7, 2, 1),
        (3, 6, 0, 0), (3, 6, 0, 1), (3, 6, 1, 0), (3, 6, 1, 1),
        (3, 6, 2, 0), (3, 6, 2, 1),
    ),
    "generator_sha256":
        "f6cb693620994bf53a1b4e5bd53f61ba0ebbd1f560ef21b06b0e787c92d86ada",
    "first_profile": [54, 20, 34],
    "one_class_count": 24,
    "two_class_edges": 519,
    "distinct_displacements": 42,
    "parallel_collisions": 24,
    "terminal_record": 1575,
    "terminal_normal_form": [[
        [["x_04_00", 1], ["x_15_12", 1], ["x_26_01", 1],
         ["x_37_00", 1], ["x_57_12", 1], ["x_57_22", -1]],
        "1",
    ]],
    "ordinary": {
        "source_records": [1575, 3416, 3417, 3419, 3420, 3598, 3601],
        "laurent_cofactor_terms": 12,
        "clearing_monomial": [
            ["x_02_22", 1], ["x_13_22", 1], ["x_46_00", 1],
            ["x_47_02", 1], ["x_56_10", 1], ["x_57_22", 2],
        ],
        "ordinary_saturation_power": 1,
        "ordinary_cofactor_terms": 12,
        "ordinary_certificate_sha256":
            "5113cd490e452525c4d32251fa2b806e1f77d795bba42187ac2719e8892558b6",
    },
    "witness_count": 18,
}, {
    "label": "face8",
    "missing": (
        (0, 1, 0, 1), (0, 1, 1, 0),
        (0, 3, 0, 1), (0, 3, 1, 0),
        (0, 6, 0, 0), (0, 6, 0, 1), (0, 6, 1, 0), (0, 6, 1, 1),
        (0, 7, 0, 1),
        (1, 2, 0, 1), (1, 2, 1, 0),
        (1, 4, 0, 1), (1, 4, 1, 0),
        (1, 5, 0, 1), (1, 5, 1, 0),
        (1, 6, 0, 1), (1, 6, 1, 0),
        (1, 7, 0, 0), (1, 7, 0, 1), (1, 7, 1, 0), (1, 7, 1, 1),
        (2, 6, 0, 0), (2, 6, 0, 1), (2, 6, 1, 0), (2, 6, 1, 1),
        (2, 6, 2, 0), (2, 6, 2, 1),
        (2, 7, 1, 0), (2, 7, 2, 0),
        (3, 7, 0, 0), (3, 7, 0, 1), (3, 7, 1, 0), (3, 7, 1, 1),
        (3, 7, 2, 0), (3, 7, 2, 1),
    ),
    "generator_sha256":
        "6fa6f7147fae1d4caeac187693e5869e4b0a5571bdda5a957a6cfabe31681e4b",
    "first_profile": [72, 25, 47],
    "one_class_count": 12,
    "two_class_edges": 286,
    "distinct_displacements": 29,
    "parallel_collisions": 24,
    "terminal_record": 2595,
    "terminal_normal_form": [[
        [["x_05_02", 1], ["x_15_11", 1], ["x_27_01", 1],
         ["x_36_10", 1], ["x_47_02", 1], ["x_57_22", -1]],
        "1",
    ]],
    "ordinary": {
        "source_records": [2120, 2121, 2595, 2635, 2638],
        "laurent_cofactor_terms": 10,
        "clearing_monomial": [
            ["x_02_22", 1], ["x_13_22", 1], ["x_46_00", 1],
            ["x_47_02", 1], ["x_56_10", 1], ["x_57_22", 2],
        ],
        "ordinary_saturation_power": 2,
        "ordinary_cofactor_terms": 10,
        "ordinary_certificate_sha256":
            "a180d32e8160e2c5b220e08d9ec9493aaba3c018b40efa8b334df3cb96fefc74",
    },
    "witness_count": 15,
},)

EXPECTED_LEDGER_SHA256 = (
    "8a26763324cdf2619f723da804b95d17054621eeaf9ad1e9289740fa1c30e528"
)


def face_audit(frozen):
    support = Q.allowed_support() - set(frozen["missing"])
    records = C.coefficient_generators(support)
    require(len(support) == 158 and len(records) == 4321
            and D.content_hash(records) == frozen["generator_sha256"],
            frozen["label"] + " coefficient input changed")
    rows = B.initial_rows(records)
    basis, dependencies = E.L.integer_laurent_basis(rows)
    require([len(rows), len(basis), len(dependencies)]
            == frozen["first_profile"]
            and all(E.row_character(dependency, rows) == 1
                    for dependency in dependencies),
            frozen["label"] + " first character changed")
    basis_characters = {
        pivot: E.row_character(representation, rows)
        for pivot, (_basis_row, representation) in basis.items()
    }
    one_class = []
    graph_edges = []
    terminal = None
    for record_index, record in enumerate(records):
        reduced, traces, parents = E.reduce_record(
            record, basis, basis_characters
        )
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
        if record_index == frozen["terminal_record"]:
            terminal = {
                "iteration": 0,
                "source_record": record_index,
                "normal_form": E.polynomial_trace(reduced),
                "parents": sorted(parents),
                "traces": traces,
            }
    require(len(one_class) == frozen["one_class_count"]
            and terminal["normal_form"] == frozen["terminal_normal_form"],
            frozen["label"] + " direct-unit census changed")
    by_difference = {}
    collisions = []
    for record_index, difference, constant in graph_edges:
        if (difference in by_difference
                and by_difference[difference][1] != constant):
            collisions.append([
                by_difference[difference][0], record_index,
                str(by_difference[difference][1]), str(constant),
            ])
        else:
            by_difference[difference] = (record_index, constant)
    require(len(graph_edges) == frozen["two_class_edges"]
            and len(by_difference) == frozen["distinct_displacements"]
            and len(collisions) == frozen["parallel_collisions"],
            frozen["label"] + " quotient graph changed")
    ordinary = E.ordinary_saturation_certificate(
        records, rows, terminal, support
    )
    require(ordinary == frozen["ordinary"],
            frozen["label"] + " ordinary certificate changed")
    witnesses = E.source_witnesses(
        records, tuple(ordinary["source_records"])
    )
    require(len(witnesses) == frozen["witness_count"]
            and set(witnesses) <= support,
            frozen["label"] + " source witness changed")
    return {
        "label": frozen["label"],
        "missing_cells": [list(cell) for cell in frozen["missing"]],
        "complete_shadow": C.support_shadow_audit(support),
        "generator_sha256": D.content_hash(records),
        "first_character_profile": frozen["first_profile"],
        "one_class_generators": one_class,
        "quotient_character_graph": {
            "two_class_edges": len(graph_edges),
            "distinct_displacements": len(by_difference),
            "opposite_character_parallel_edges": collisions,
        },
        "terminal_record": terminal["source_record"],
        "terminal_normal_form": terminal["normal_form"],
        "ordinary_saturation_certificate": ordinary,
        "localized_source_witnesses": [list(cell) for cell in witnesses],
    }


def transported_clause_audit():
    clauses = {}
    for frozen in FACES:
        row = face_audit(frozen)
        for clause in E.transform_clauses(
                {tuple(cell) for cell in row["missing_cells"]},
                {tuple(cell) for cell in row["localized_source_witnesses"]}):
            key = (
                tuple(tuple(cell) for cell in clause["positive_cells"]),
                tuple(tuple(cell) for cell in clause["negative_cells"]),
            )
            clauses[key] = clause
    return [clauses[key] for key in sorted(clauses)]


def audit():
    started = monotonic()
    faces = [face_audit(frozen) for frozen in FACES]
    transported = transported_clause_audit()
    require(len(transported) == 8 * len(FACES),
            "the later-face transport census changed")
    ledger = {
        "pinned_sources": PINNED,
        "faces": faces,
        "distinct_transported_clauses": transported,
        "characteristic_scope": "every characteristic",
        "status": "later 158-cell faces are empty by direct character units",
    }
    return ledger, D.content_hash(ledger), monotonic() - started


def main():
    ledger, digest, elapsed = audit()
    if EXPECTED_LEDGER_SHA256 == "TO_BE_FROZEN":
        print("ledger sha256:", digest)
    else:
        require(digest == EXPECTED_LEDGER_SHA256,
                "the later 158-cell character-graph ledger changed")
        print("ledger sha256 (frozen):", digest)
    print("faces:", len(ledger["faces"]))
    print("transported clauses:", len(ledger["distinct_transported_clauses"]))
    print("elapsed: %.2fs" % elapsed)


if __name__ == "__main__":
    main()
