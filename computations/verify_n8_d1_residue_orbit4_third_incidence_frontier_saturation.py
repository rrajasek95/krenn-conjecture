#!/usr/bin/env python3
"""Exact ordinary saturation of the third 159-cell O4 incidence face."""

from __future__ import annotations

import hashlib
import importlib
import os
import sys
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

EXPECTED_GENERATOR_SHA256 = (
    "c1ea0da1c979832b96862523c5c67361c48e1387109dd24aa82526f513cc3bcb"
)
EXPECTED_LEDGER_SHA256 = (
    "51dc48d36f3e9a58fa5472763822e4ed5cd15e4fd88f12f0f9d5d354be1d2514"
)

FRONTIER_MISSING = (
    (0, 1, 0, 1), (0, 1, 1, 0), (0, 3, 0, 1), (0, 3, 1, 0),
    (0, 6, 0, 0), (0, 6, 0, 1), (0, 6, 1, 0), (0, 6, 1, 1),
    (0, 7, 0, 1), (0, 7, 1, 0),
    (1, 2, 0, 1), (1, 2, 1, 0),
    (1, 4, 0, 1), (1, 4, 1, 0), (1, 5, 0, 1), (1, 5, 1, 0),
    (1, 6, 0, 1), (1, 6, 1, 0),
    (1, 7, 0, 0), (1, 7, 0, 1), (1, 7, 1, 0), (1, 7, 1, 1),
    (2, 6, 0, 0), (2, 6, 0, 1), (2, 6, 1, 0), (2, 6, 1, 1),
    (2, 6, 2, 0), (2, 6, 2, 1),
    (3, 7, 0, 0), (3, 7, 0, 1), (3, 7, 1, 0), (3, 7, 1, 1),
    (3, 7, 2, 0), (3, 7, 2, 1),
)


def certificate_input():
    support = Q.allowed_support() - set(FRONTIER_MISSING)
    require(len(support) == 159,
            "the third incidence frontier changed size")
    records = C.coefficient_generators(support)
    require(len(records) == 4321
            and D.content_hash(records) == EXPECTED_GENERATOR_SHA256,
            "the third incidence coefficient input changed")
    rows, iterations, final = E.closure(records, frozen=False)
    require(len(rows) == 54
            and [(row["input_rows"], row["lattice_rank"], row["new_rows"])
                 for row in iterations] == [(54, 20, 37)],
            "the third incidence Laurent profile changed")
    require(final["iteration"] == 0 and final["source_record"] == 3129,
            "the third incidence terminal generator changed")
    require(final["normal_form"] == [[
        [["x_05_02", 1], ["x_15_11", 1], ["x_27_01", 1],
         ["x_36_10", 1], ["x_47_02", 1], ["x_57_22", -1]],
        "1",
    ]], "the third incidence Laurent unit changed")
    ordinary = E.ordinary_saturation_certificate(
        records, rows, final, support
    )
    require(ordinary == {
        "source_records": [2444, 2445, 3129, 3189, 3192],
        "laurent_cofactor_terms": 10,
        "clearing_monomial": [
            ["x_02_22", 1], ["x_13_22", 1], ["x_46_00", 1],
            ["x_47_02", 1], ["x_56_10", 1], ["x_57_22", 2],
        ],
        "ordinary_saturation_power": 2,
        "ordinary_cofactor_terms": 10,
        "ordinary_certificate_sha256":
            "35ebdb7ea7098a057e4553d7aed8d4b761d1235658ce3c64f6a665f56f08e500",
    }, "the third incidence ordinary U^2 certificate changed")
    witnesses = E.source_witnesses(
        records, tuple(ordinary["source_records"])
    )
    require(len(witnesses) == 15 and set(witnesses) <= support,
            "the third incidence source witnesses changed")
    return support, records, rows, iterations, final, ordinary, witnesses


def clause_audit():
    _support, _records, _rows, _iterations, _final, ordinary, witnesses = (
        certificate_input()
    )
    return {
        "positive_cells": [list(cell) for cell in FRONTIER_MISSING],
        "negative_cells": [list(cell) for cell in witnesses],
        "source_records": ordinary["source_records"],
    }


def transported_clause_audit():
    base = clause_audit()
    return E.transform_clauses(
        set(FRONTIER_MISSING),
        {tuple(cell) for cell in base["negative_cells"]},
    )


def audit():
    started = monotonic()
    support, records, _rows, iterations, final, ordinary, witnesses = (
        certificate_input()
    )
    shadow = C.support_shadow_audit(support)
    transported = E.transform_clauses(set(FRONTIER_MISSING), set(witnesses))
    ledger = {
        "pinned_engine_sha256": source_digest,
        "localized_cells": len(support),
        "complete_shadow": shadow,
        "coefficient_generators": len(records),
        "generator_sha256": D.content_hash(records),
        "initial_unique_plus_rows": 54,
        "laurent_rank": iterations[0]["lattice_rank"],
        "terminal_record": final["source_record"],
        "terminal_normal_form": final["normal_form"],
        "ordinary_saturation_certificate": ordinary,
        "localized_source_witnesses": [list(cell) for cell in witnesses],
        "distinct_transported_clauses": transported,
        "characteristic_scope": "every characteristic; coefficients are integral",
        "status": "third 159-cell O4 incidence frontier is coefficient-empty",
    }
    return ledger, D.content_hash(ledger), monotonic() - started


def main():
    ledger, digest, elapsed = audit()
    if EXPECTED_LEDGER_SHA256 == "TO_BE_FROZEN":
        print("ledger sha256:", digest)
    else:
        require(digest == EXPECTED_LEDGER_SHA256,
                "the third-incidence saturation ledger changed")
        print("ledger sha256 (frozen):", digest)
    print("terminal record:", ledger["terminal_record"])
    print("ordinary saturation: U^%d" % ledger[
        "ordinary_saturation_certificate"
    ]["ordinary_saturation_power"])
    print("source records:", len(ledger[
        "ordinary_saturation_certificate"
    ]["source_records"]))
    print("elapsed: %.2fs" % elapsed)


if __name__ == "__main__":
    main()
