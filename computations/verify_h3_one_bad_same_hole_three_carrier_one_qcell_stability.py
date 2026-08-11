#!/usr/bin/env python3
"""One-q-cell stability of the three same-hole private-row units.

For each exact carrier support in 9a81c82, add every unused decorated cell
on the ten common physical edges, one at a time.  Neither private word
00000000 nor 00000001 acquires a new matching.  The first possible
contamination needs two pure-00 q cells and is listed exactly for each packet.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import importlib
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_one_bad_same_hole_three_carrier_fullword_units.py":
        "ee1d078ba90e9cde71b53570ec439c773eb7b66f59a32a261dda05fee51867ea",
}
EXPECTED_LEDGER_SHA256 = (
    "d7072c110f3eb6af34566dab811617691ac96b147f3317c63a1886465556f342"
)

VERTICES = tuple(range(8))
COMMON = tuple(range(5))
COLORS = tuple(range(3))
PURE = (0,) * 8
MIXED = tuple(map(int, "00000001"))


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, f"dependency changed: {relative}: {actual}")


def q_name(cell):
    u, v, a, b = cell
    return f"q{u}{v}:{a}{b}"


def word_polynomial(base, support, word):
    polynomial = Counter()
    live = []
    for matching in base.perfect_matchings(VERTICES):
        cells = tuple(base.cell(u, v, word[u], word[v])
                      for u, v in matching)
        if not all(cell in support for cell in cells):
            continue
        polynomial[tuple(sorted(q_name(cell) for cell in cells))] += 1
        live.append(matching)
    return polynomial, tuple(live)


def viable_q_missing_sets(base, support, q_universe, word):
    answer = []
    for matching in base.perfect_matchings(VERTICES):
        cells = {base.cell(u, v, word[u], word[v]) for u, v in matching}
        missing = cells - support
        if missing and missing <= q_universe:
            answer.append((matching, frozenset(missing)))
    return tuple(answer)


def serial_missing(entries):
    return tuple({
        "matching": matching,
        "missing_q_cells": tuple(sorted(q_name(cell) for cell in missing)),
    } for matching, missing in entries)


def main():
    pin_dependencies()
    base = importlib.import_module(
        "verify_h3_one_bad_common_q_cap_extraction_boundary")
    repair = importlib.import_module(
        "verify_h3_one_bad_same_hole_internal_repair_reselection")

    q_universe = {
        base.cell(u, v, a, b)
        for u, v in itertools.combinations(COMMON, 2)
        for a, b in itertools.product(COLORS, repeat=2)
    }
    require(len(q_universe) == 90, "the common-q universe changed")

    packet_names = (
        "shared_CA", "middle_AT_right", "middle_AT_left_secondary")
    expected_counts = {
        "shared_CA": (83, 8, 75),
        "middle_AT_right": (83, 8, 75),
        "middle_AT_left_secondary": (81, 8, 73),
    }
    expected_two_cell_frontier = {
        "shared_CA": {
            ("q03:00", "q14:00"),
            ("q04:00", "q13:00"),
        },
        "middle_AT_right": {
            ("q01:00", "q34:00"),
            ("q04:00", "q13:00"),
        },
        "middle_AT_left_secondary": {
            ("q01:00", "q34:00"),
            ("q04:00", "q13:00"),
        },
    }

    ledgers = {}
    for name in packet_names:
        common = repair.common_packets(base.cell)[name]
        source = Counter(common)
        source.update(repair.outer_source(base.cell))
        support = set(source)
        unused = tuple(sorted(q_universe - support))
        unused_00 = tuple(cell for cell in unused if cell[2:] == (0, 0))
        unused_other = tuple(cell for cell in unused if cell[2:] != (0, 0))
        require((len(unused), len(unused_00), len(unused_other))
                == expected_counts[name],
                f"{name} unused-q census changed")

        pure0, pure_live0 = word_polynomial(base, support, PURE)
        mixed0, mixed_live0 = word_polynomial(base, support, MIXED)
        require(len(pure0) == len(mixed0) == 1
                and len(pure_live0) == len(mixed_live0) == 1,
                f"{name} baseline private rows changed")

        classifications = Counter()
        contaminators = []
        for cell in unused:
            enlarged = support | {cell}
            pure, pure_live = word_polynomial(base, enlarged, PURE)
            mixed, mixed_live = word_polynomial(base, enlarged, MIXED)
            if pure == pure0 and mixed == mixed0:
                classifications["original_two_row_unit_survives"] += 1
            else:
                contaminators.append((cell, pure_live, mixed_live))
        require(not contaminators,
                f"{name} acquired a one-cell contaminator: {contaminators}")
        require(classifications
                == Counter({"original_two_row_unit_survives": len(unused)}),
                f"{name} one-cell classification changed: {classifications}")

        pure_frontier = viable_q_missing_sets(
            base, support, q_universe, PURE)
        mixed_frontier = viable_q_missing_sets(
            base, support, q_universe, MIXED)
        require(pure_frontier == mixed_frontier,
                f"{name} pure/mixed contamination frontiers separated")
        require(len(pure_frontier) == 2
                and {len(missing) for _, missing in pure_frontier} == {2},
                f"{name} first contamination depth changed: {pure_frontier}")
        actual_frontier = {
            tuple(sorted(q_name(cell) for cell in missing))
            for _, missing in pure_frontier
        }
        require(actual_frontier == expected_two_cell_frontier[name],
                f"{name} two-cell frontier changed: {actual_frontier}")

        ledgers[name] = {
            "unused_q_cells": len(unused),
            "unused_00_cells": len(unused_00),
            "unused_other_decorations": len(unused_other),
            "one_cell_classification": dict(classifications),
            "one_cell_contaminators": 0,
            "first_possible_contamination_depth": 2,
            "two_cell_frontier": serial_missing(pure_frontier),
        }

    ledger = {
        "dependencies": PINS,
        "q_universe_cells": len(q_universe),
        "packets": ledgers,
        "verdict": (
            "all 247 single unused decorated-q additions preserve the "
            "original private-row unit; there is no replacement-unit case "
            "and no one-cell residue packet"
        ),
        "scope": (
            "one additional common-q cell on each of the three exact carrier "
            "supports; the explicitly listed two-cell frontiers are not "
            "analyzed"
        ),
    }
    require(sum(packet["unused_q_cells"] for packet in ledgers.values()) == 247,
            "the total one-cell census changed")
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"the one-q-cell stability ledger changed: {digest}")

    print("h=3 same-hole three-carrier one-q-cell stability: PASS")
    print("unused q cells: shared/right/left+secondary = 83/83/81")
    print("one-cell contaminators: 0/0/0; original units survive all 247")
    print("first possible private-row contamination depth: two q cells")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
