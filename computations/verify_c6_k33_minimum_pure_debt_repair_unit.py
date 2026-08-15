#!/usr/bin/env python3
"""Minimum simultaneous repair of the first K3,3 pure-completion debts.

The 15-cell K3,3 guard has 66 minimum pure-witness completions with the
smallest possible mixed-singleton count, ten.  Choose the lexicographically
canonical 23-cell completion.  This checker solves the exact minimum-union
problem for mating all ten singleton rows.  The minimum is seven cells and
there are twelve packets.  Every packet creates the same new private mixed
row 000011 with fine 01|23|45, hence a literal source unit.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
from itertools import product
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_c6_thirteen_exit_k33_shared_star_guard.py":
        "04b631cee46de29d8b4228aad777a414ae75aa021444bbc9ffc39852442592e2",
    "notes/2026-08-15-c6-thirteen-exit-k33-shared-star-guard.md":
        "6cbafc38ad54f8100170188765acbe2750c776f4b484f4f5c7330c0247094993",
}


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load_guard():
    relative = "computations/verify_c6_thirteen_exit_k33_shared_star_guard.py"
    specification = importlib.util.spec_from_file_location(
        "c6_k33_guard_dependency", ROOT / relative
    )
    require(specification is not None and specification.loader is not None,
            specification)
    module = importlib.util.module_from_spec(specification)
    sys.modules[specification.name] = module
    specification.loader.exec_module(module)
    return module


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned K3,3 guard changed", relative, actual, expected))


def base_guard_support(guard):
    record = guard.k33_guard()
    weights = record.pop("weights")
    require(len(weights) == 15, len(weights))
    return frozenset(weights)


def minimum_pure_completions(guard, base):
    _, mixed_occurrences, pure = guard.support_mask_inventory()

    def cell_index(cell):
        left, right, alpha, beta = cell
        return 9 * guard.EDGES.index((left, right)) + 3 * alpha + beta

    base_mask = sum(1 << cell_index(cell) for cell in base)
    records = []
    for witness_indices in product(range(15), repeat=3):
        support_mask = base_mask
        for colour, matching_index in enumerate(witness_indices):
            support_mask |= pure[colour][matching_index]
        singleton_count = 0
        for occurrence_masks in mixed_occurrences.values():
            multiplicity = sum((mask & support_mask) == mask
                               for mask in occurrence_masks)
            singleton_count += int(multiplicity == 1)
        if singleton_count != 10:
            continue
        support = set(base)
        for colour, matching_index in enumerate(witness_indices):
            support.update(guard.occurrence_cells(
                guard.MATCHINGS[matching_index], (colour,) * guard.N
            ))
        require(len(support) == support_mask.bit_count() == 23,
                (witness_indices, len(support), support_mask.bit_count()))
        records.append((tuple(sorted(support)), witness_indices))

    require(len(records) == 66 and len({support for support, _ in records}) == 66,
            (len(records), len({support for support, _ in records})))
    canonical_support, canonical_witnesses = min(records)
    require(canonical_witnesses == (1, 6, 2), canonical_witnesses)
    require(tuple(guard.matching_name(guard.MATCHINGS[index])
                  for index in canonical_witnesses) ==
            ("01|24|35", "03|12|45", "01|25|34"),
            canonical_witnesses)
    return {
        "minimum_singleton_completions": len(records),
        "all_support_sizes": (23,),
        "canonical_witness_indices": canonical_witnesses,
        "canonical_witness_fines": tuple(
            guard.matching_name(guard.MATCHINGS[index])
            for index in canonical_witnesses
        ),
        "canonical_support": frozenset(canonical_support),
    }


def singleton_rows(guard, support):
    rows = guard.complete_rows({cell: Q(1) for cell in support})
    answer = []
    for word, occurrences in rows.items():
        if len(set(word)) > 1 and len(occurrences) == 1:
            answer.append((word, occurrences[0][0]))
    return tuple(answer)


def mate_candidates(guard, support, singletons):
    all_candidates = []
    records = []
    for word, old_matching in singletons:
        candidate_by_missing = {}
        for matching in guard.MATCHINGS:
            if matching == old_matching:
                continue
            missing = frozenset(
                cell for cell in guard.occurrence_cells(matching, word)
                if cell not in support
            )
            require(missing, (word, old_matching, matching))
            candidate_by_missing.setdefault(missing, matching)
        minimal = tuple(sorted(
            ((missing, matching)
             for missing, matching in candidate_by_missing.items()
             if not any(other < missing for other in candidate_by_missing)),
            key=lambda item: (len(item[0]), tuple(sorted(item[0])), item[1]),
        ))
        all_candidates.append(minimal)
        records.append({
            "word": guard.word_name(word),
            "old_fine": guard.matching_name(old_matching),
            "minimal_candidate_count": len(minimal),
            "missing_cell_sizes": tuple(sorted({len(missing)
                                                 for missing, _ in minimal})),
        })
    return tuple(all_candidates), tuple(records)


def minimum_union_solutions(candidates, budget):
    solutions = set()

    def recurse(packet):
        uncovered = tuple(
            row for row, row_candidates in enumerate(candidates)
            if not any(missing <= packet for missing, _ in row_candidates)
        )
        if not uncovered:
            solutions.add(frozenset(packet))
            return
        row = min(
            uncovered,
            key=lambda index: sum(
                len(packet | missing) <= budget
                for missing, _ in candidates[index]
            ),
        )
        children = set()
        for missing, _ in candidates[row]:
            child = frozenset(packet | missing)
            if len(child) <= budget:
                children.add(child)
        for child in sorted(children, key=lambda item: tuple(sorted(item))):
            recurse(child)

    recurse(frozenset())
    return frozenset(solutions)


def repair_census(guard, support, singletons, candidates):
    budget_counts = {}
    solutions = frozenset()
    for budget in range(1, 8):
        solutions = minimum_union_solutions(candidates, budget)
        budget_counts[budget] = len(solutions)
        if solutions:
            break
    require(budget_counts == {1: 0, 2: 0, 3: 0, 4: 0,
                              5: 0, 6: 0, 7: 12}, budget_counts)
    require(all(len(packet) == 7 for packet in solutions), solutions)

    new_singleton_histogram = Counter()
    first_new_histogram = Counter()
    packet_records = []
    intersection = set.intersection(*(set(packet) for packet in solutions))
    expected_intersection = {
        (1, 3, 1, 1),
        (2, 3, 0, 0),
        (2, 3, 0, 2),
        (4, 5, 0, 0),
    }
    require(intersection == expected_intersection, intersection)

    old_words = {word for word, _ in singletons}
    for packet in sorted(solutions, key=lambda item: tuple(sorted(item))):
        enlarged = frozenset(set(support) | set(packet))
        rows = guard.complete_rows({cell: Q(1) for cell in enlarged})
        for word in old_words:
            require(len(rows[word]) >= 2, (packet, word, rows[word]))
        new_singletons = tuple(
            (word, occurrences[0][0])
            for word, occurrences in rows.items()
            if len(set(word)) > 1 and len(occurrences) == 1
        )
        require(new_singletons, packet)
        first_word, first_fine = new_singletons[0]
        require(first_word == (0, 0, 0, 0, 1, 1)
                and first_fine == ((0, 1), (2, 3), (4, 5)),
                (packet, first_word, first_fine))
        first_cells = guard.occurrence_cells(first_fine, first_word)
        require(first_cells == (
            (0, 1, 0, 0),
            (2, 3, 0, 0),
            (4, 5, 1, 1),
        ), first_cells)
        require(all(cell in enlarged for cell in first_cells),
                (packet, first_cells))
        new_singleton_histogram[len(new_singletons)] += 1
        first_new_histogram[guard.word_name(first_word)] += 1
        packet_records.append({
            "new_cells": tuple(guard.cell_name(cell)
                               for cell in sorted(packet)),
            "new_mixed_singletons": len(new_singletons),
            "first_new_unit": {
                "word": guard.word_name(first_word),
                "fine": guard.matching_name(first_fine),
                "cells": tuple(guard.cell_name(cell) for cell in first_cells),
                "equation": "nonzero monomial = 0",
            },
        })

    require(new_singleton_histogram == Counter({
        23: 2, 24: 2, 25: 2, 26: 1, 27: 2, 28: 2, 30: 1,
    }), new_singleton_histogram)
    require(first_new_histogram == Counter({"000011": 12}),
            first_new_histogram)
    return {
        "minimum_added_cells": 7,
        "budget_solution_counts": budget_counts,
        "minimum_packets": len(solutions),
        "common_forced_cells": tuple(guard.cell_name(cell)
                                     for cell in sorted(intersection)),
        "new_singleton_histogram":
            dict(sorted(new_singleton_histogram.items())),
        "universal_new_unit": {
            "word": "000011",
            "fine": "01|23|45",
            "cells": ("01;00", "23;00", "45;11"),
            "reason": (
                "01;00 and 45;11 are in the canonical pure completion; "
                "every minimum repair packet contains 23;00"
            ),
        },
        "all_packet_records": tuple(packet_records),
    }


def build_ledger():
    pin_dependencies()
    guard = load_guard()
    base = base_guard_support(guard)
    completion = minimum_pure_completions(guard, base)
    support = completion.pop("canonical_support")
    singletons = singleton_rows(guard, support)
    require(len(singletons) == 10, singletons)
    candidates, candidate_records = mate_candidates(guard, support, singletons)
    repair = repair_census(guard, support, singletons, candidates)
    return {
        "theorem": "minimum K3,3 pure-debt repair creates a source unit",
        "pins": PINS,
        "minimum_pure_completion": completion,
        "canonical_support_cells": tuple(guard.cell_name(cell)
                                         for cell in sorted(support)),
        "ten_singleton_debts": tuple({
            "word": guard.word_name(word),
            "fine": guard.matching_name(matching),
            "cells": tuple(guard.cell_name(cell) for cell in
                           guard.occurrence_cells(matching, word)),
        } for word, matching in singletons),
        "mate_candidate_records": candidate_records,
        "minimum_simultaneous_repair": repair,
        "verdict": (
            "every cardinality-minimum simultaneous mate packet for the "
            "canonical minimum pure completion creates the literal mixed "
            "unit 000011/01|23|45.  Larger/nonminimum mate packets remain "
            "outside this finite layer."
        ),
    }


EXPECTED_LEDGER_SHA256 = (
    "e436369afb5a94268ce65f4189ba5562746ee150c90134c789bb8a1c5bb822af"
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("structural", "full", "exhaustive"),
                        default="structural")
    parser.add_argument("--dump-ledger", action="store_true")
    arguments = parser.parse_args()
    ledger = build_ledger()
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256:
        require(digest == EXPECTED_LEDGER_SHA256,
                ("minimum repair ledger changed", digest,
                 EXPECTED_LEDGER_SHA256))
    if arguments.dump_ledger:
        print(json.dumps(ledger, indent=2, sort_keys=True))
    print("C6 K3,3 minimum pure-debt repair: PASS")
    print("mode", arguments.mode)
    print("ledger_sha256", digest)
    print("canonical debts: 10; minimum repair: 7 cells / 12 packets")
    print("all minimum packets create unit 000011 / 01|23|45")


if __name__ == "__main__":
    main()
