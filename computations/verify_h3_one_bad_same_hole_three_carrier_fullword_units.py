#!/usr/bin/env python3
"""Three-packet full-word verdict for the same-hole carrier calibrations.

Extend 1906206's literal full-word audit from the shared C/A packet to the
middle A/T right packet and the forced-secondary middle-left packet.  In all
three supports, words 00000000 and 00000001 share one unique matching and
differ only by the fixed R_a/R_c cell on edge 27.  The same determinant-
cleared and fixed-normalization two-row units therefore close all packets.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import importlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_one_bad_same_hole_shared_carrier_fullword_unit.py":
        "191336312c54249a719def2e3cce12162321c9a7a9dc869b095adf3f2d16f1d9",
}
EXPECTED_LEDGER_SHA256 = (
    "d3a36002485d27be89a6f9d7a76d404b5976d19ef85e0ec463ff0f096791914b"
)

PURE = (0,) * 8
MIXED = tuple(map(int, "00000001"))
TARGET_WORDS = {(colour,) * 8 for colour in range(3)}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, f"dependency changed: {relative}: {actual}")


def packet_audit(base, repair, fullword, name, expected, expected_matching):
    common = repair.common_packets(base.cell)[name]
    source = Counter(common)
    source.update(repair.outer_source(base.cell))
    rows, live = fullword.full_word_rows(base, source)

    histogram = Counter(map(len, rows.values()))
    summary = (len(source), len(rows), sum(map(len, rows.values())), histogram)
    require(summary == expected, f"{name} full-word summary changed: {summary}")
    unique_mixed = tuple(sorted(
        word for word, polynomial in rows.items()
        if word not in TARGET_WORDS and len(polynomial) == 1
    ))
    require(len(unique_mixed) == histogram[1] - 3,
            f"{name} unique mixed count changed")

    require(live[PURE] == live[MIXED] == (expected_matching,),
            f"{name} private matching changed: {live[PURE]}, {live[MIXED]}")
    pure_monomial = next(iter(rows[PURE]))
    mixed_monomial = next(iter(rows[MIXED]))
    common_tail = set(pure_monomial).intersection(mixed_monomial)
    require(len(common_tail) == 3,
            f"{name} pure/mixed common tail changed: {common_tail}")

    ra = fullword.variable_name(base.cell(2, 7, 0, 0))
    rc = fullword.variable_name(base.cell(2, 7, 0, 1))
    require(set(pure_monomial) - common_tail == {ra}
            and set(mixed_monomial) - common_tail == {rc},
            f"{name} private factor changed")
    pure_generator = fullword.add(
        (rows[PURE], 1), (Counter({(): Fraction(1)}), -1))
    mixed_generator = rows[MIXED]
    localized = fullword.add(
        (fullword.multiply_variable(mixed_generator, ra), 1),
        (fullword.multiply_variable(pure_generator, rc), -1),
    )
    require(localized == Counter({(rc,): 1}),
            f"{name} determinant-cleared unit changed: {localized}")

    fixed_values = {
        fullword.variable_name(cell): Fraction(value)
        for cell, value in repair.outer_source(base.cell).items()
    }
    fixed_pure = fullword.specialize(pure_generator, fixed_values)
    fixed_mixed = fullword.specialize(mixed_generator, fixed_values)
    ordinary = fullword.add((fixed_mixed, Fraction(-1, 2)),
                            (fixed_pure, -1))
    require(ordinary == Counter({(): 1}),
            f"{name} ordinary unit changed: {ordinary}")

    return {
        "support_cells": len(source),
        "nonzero_physical_rows": len(rows),
        "physical_monomials": sum(map(len, rows.values())),
        "row_size_histogram": dict(sorted(histogram.items())),
        "unique_mixed_monomial_rows": len(unique_mixed),
        "private_matching": expected_matching,
        "pure_word": "00000000",
        "mixed_word": "00000001",
        "common_tail": tuple(sorted(common_tail)),
        "localized_identity": "ra*Gmixed-rc*Gpure=rc",
        "fixed_identity": "1=(-1/2)*Gmixed-Gpure",
    }


def main():
    pin_dependencies()
    base = importlib.import_module(
        "verify_h3_one_bad_common_q_cap_extraction_boundary")
    repair = importlib.import_module(
        "verify_h3_one_bad_same_hole_internal_repair_reselection")
    fullword = importlib.import_module(
        "verify_h3_one_bad_same_hole_shared_carrier_fullword_unit")

    expected = {
        "shared_CA": (17, 29, 31, Counter({1: 27, 2: 2})),
        "middle_AT_right": (17, 21, 23, Counter({1: 19, 2: 2})),
        "middle_AT_left_secondary": (19, 34, 38,
                                      Counter({1: 30, 2: 4})),
    }
    expected_matchings = {
        "shared_CA": ((0, 1), (2, 7), (3, 4), (5, 6)),
        "middle_AT_right": ((0, 3), (1, 4), (2, 7), (5, 6)),
        "middle_AT_left_secondary": ((0, 3), (1, 4), (2, 7), (5, 6)),
    }
    packets = {
        name: packet_audit(base, repair, fullword, name, summary,
                           expected_matchings[name])
        for name, summary in expected.items()
    }

    require(packets["middle_AT_right"]["private_matching"]
            == packets["middle_AT_left_secondary"]["private_matching"]
            != packets["shared_CA"]["private_matching"],
            "the shared/middle private-matching split changed")
    require(all(packet["localized_identity"]
                == "ra*Gmixed-rc*Gpure=rc"
                for packet in packets.values()),
            "the three determinant-cleared identities separated")

    ledger = {
        "dependencies": PINS,
        "packets": packets,
        "verdict": (
            "all three exact same-hole carrier-only packets are empty; the "
            "middle-right and forced middle-left packets have the same "
            "literal private-row unit as the shared C/A packet"
        ),
        "scope": (
            "exact 17/17/19-cell carrier supports with fixed endpoint stars "
            "and directs; no extra residue cells, no arbitrary support "
            "completion, and no general curved-OO transport claim"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"the three-packet full-word ledger changed: {digest}")

    print("h=3 same-hole three-carrier full-word units: PASS")
    print("supports: shared/right/left+secondary = 17/17/19 cells")
    print("private matchings: shared=01|27|34|56; middle=03|14|27|56")
    print("all have ordinary unit 1=(-1/2)G_00000001-G_00000000")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
