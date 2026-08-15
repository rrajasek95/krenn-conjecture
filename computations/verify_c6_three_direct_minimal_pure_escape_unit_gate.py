#!/usr/bin/env python3
"""Classify minimum pure escapes from the seven-cell three-direct C6 guard.

The base packet has cap 34 in all three colours and the colour-one residual
cycle 05,12,01,25.  Its two mixed rows force the common two-term residual H
to vanish, so pure normalization in colour one requires a cap-avoiding
matching.  Enumerate every support-minimum such repair, retain literal word,
fine, cap, window, tail, and coefficient-operation labels, and then adjoin a
minimum cap-avoiding pure escape in either missing colour.

The first repair is a locally consistent nine-cell guard.  Every next
minimum missing-colour escape creates a literal mixed singleton, hence a
source unit.  The checker also exhausts all minimum three-colour completions.
"""

from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
import importlib.util
from itertools import permutations, product
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_uniform_c6_oriented_complementary_face_naturality.py":
        "7d0fb2cc5d1a722eddfdafaa155f2346fc62c531fe0a33c28abaf8a537b6e980",
    "notes/2026-08-14-c6-oriented-complementary-face-naturality.md":
        "04a1fd8c41c65837d254ca244eed70bb6e585c6099055eed3f023228c278f357",
}
EXPECTED_LEDGER_SHA256 = (
    "c959c3aa2b09e14bc67cba82c5ce3435870f7ecd6bd7bba0b46d1b25a31e236b"
)


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def load(relative: str, name: str):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


def row_inventory(base, support):
    rows = {}
    for word in product(base.COLOURS, repeat=len(base.VERTICES)):
        occurrences = []
        for matching in base.MATCHINGS:
            cells = base.occurrence_cells(matching, word)
            if cells is not None and cells <= support:
                occurrences.append((matching, tuple(sorted(cells))))
        if occurrences:
            rows[word] = tuple(occurrences)
    return rows


def mixed_singleton_records(base, rows):
    records = []
    for word, occurrences in sorted(rows.items()):
        if len(set(word)) == 1 or len(occurrences) != 1:
            continue
        matching, cells = occurrences[0]
        records.append({
            "word": base.word_name(word),
            "operation": f"coefficient:{base.word_name(word)}",
            "fine": f"fine:{base.matching_name(matching)}",
            "matching": matching,
            "decorated_cells": cells,
            "cap": "34",
            "window": "0125",
            "tail": "tail:T",
        })
    return tuple(records)


def transform_matching(matching, vertex):
    return tuple(sorted(tuple(sorted((vertex[left], vertex[right])))
                        for left, right in matching))


def labelled_guard_stabilizer(base, cap, core, mate):
    actions = []
    for vertex in permutations(base.VERTICES):
        if (tuple(sorted((vertex[cap[0]], vertex[cap[1]]))) == cap
                and {tuple(sorted((vertex[left], vertex[right])))
                     for left, right in core} == set(core)
                and {tuple(sorted((vertex[left], vertex[right])))
                     for left, right in mate} == set(mate)):
            actions.append(vertex)
    require(len(actions) == 8, len(actions))
    return tuple(actions)


def orbit_registry(objects, transform, actions):
    universe = set(objects)
    unseen = set(objects)
    representatives = []
    histogram = Counter()
    while unseen:
        representative = min(unseen)
        orbit = {transform(representative, action) for action in actions}
        require(orbit <= universe and orbit <= unseen,
                (representative, orbit - universe, orbit - unseen))
        representatives.append(representative)
        histogram[len(orbit)] += 1
        unseen.difference_update(orbit)
    payload = json.dumps(representatives, separators=(",", ":"))
    return {
        "orbits": len(representatives),
        "orbit_size_histogram": sorted(histogram.items()),
        "representatives": representatives,
        "representative_registry_sha256": sha256(payload.encode()).hexdigest(),
    }


def escape_debt(base, support, cap):
    cap_avoiding = tuple(matching for matching in base.MATCHINGS
                         if cap not in matching)
    answer = 0
    for colour in base.COLOURS:
        if not any(all((endpoints, colour) in support for endpoints in matching)
                   for matching in cap_avoiding):
            answer += 1
    return answer


def audit(base):
    cap = base.edge(3, 4)
    core = (base.edge(0, 5), base.edge(1, 2))
    mate = (base.edge(0, 1), base.edge(2, 5))
    residual = frozenset(core + mate)
    base_support = frozenset((cap, colour) for colour in base.COLOURS) \
        | frozenset((endpoints, 1) for endpoints in residual)
    require(len(base_support) == 7, base_support)

    cap_avoiding = tuple(matching for matching in base.MATCHINGS
                         if cap not in matching)
    first_escapes = tuple(
        matching for matching in cap_avoiding
        if len(set(matching) & residual) == 1
    )
    require(len(cap_avoiding) == 12 and len(first_escapes) == 8,
            (cap_avoiding, first_escapes))
    require(all(len(set(matching) - residual) == 2
                for matching in first_escapes), first_escapes)
    # No cap-avoiding matching contains two residual cells: the only two
    # disjoint residual pairs leave cap 34 as their third edge.
    require(max(len(set(matching) & residual)
                for matching in cap_avoiding) == 1, cap_avoiding)

    actions = labelled_guard_stabilizer(base, cap, core, mate)
    first_orbits = orbit_registry(
        first_escapes,
        lambda matching, action: transform_matching(matching, action),
        actions,
    )

    first_records = []
    for matching in first_escapes:
        support = base_support | frozenset((endpoints, 1)
                                           for endpoints in matching)
        require(len(support) == 9, (matching, support))
        rows = row_inventory(base, support)
        expected_words = {
            tuple(map(int, "111001")),
            tuple(map(int, "111111")),
            tuple(map(int, "111221")),
        }
        require(set(rows) == expected_words, (matching, rows))
        require(len(rows[tuple(map(int, "111001"))]) == 2
                and len(rows[tuple(map(int, "111221"))]) == 2
                and len(rows[tuple(map(int, "111111"))]) == 3,
                (matching, rows))
        require(not mixed_singleton_records(base, rows), (matching, rows))
        require(escape_debt(base, support, cap) == 2, (matching, support))
        first_records.append({
            "escape_fine": f"fine:{base.matching_name(matching)}",
            "escape_matching": matching,
            "new_cells": tuple(sorted(set(matching) - residual)),
            "support_cells": len(support),
            "row_term_counts": {
                base.word_name(word): len(occurrences)
                for word, occurrences in sorted(rows.items())
            },
            "local_equations": (
                "q34[0]*H=0", "q34[2]*H=0", "q34[1]*H+E1=1"
            ),
            "localized_consequence": "H=0, E1=1",
        })

    second_histograms = {}
    second_orbits = {}
    second_first_units = {}
    second_objects = {}
    for colour in (0, 2):
        histogram = Counter()
        objects = []
        first_units = []
        for first in first_escapes:
            first_support = base_support | frozenset(
                (endpoints, 1) for endpoints in first
            )
            for following in cap_avoiding:
                support = first_support | frozenset(
                    (endpoints, colour) for endpoints in following
                )
                require(len(support) == 12, (first, following, colour, support))
                rows = row_inventory(base, support)
                singletons = mixed_singleton_records(base, rows)
                require(singletons,
                        ("minimum next pure escape had no source unit",
                         colour, first, following, rows))
                histogram[len(singletons)] += 1
                objects.append((first, following))
                first_units.append({
                    "first_escape": base.matching_name(first),
                    "next_colour": colour,
                    "next_escape": base.matching_name(following),
                    "unit": singletons[0],
                    "mixed_singleton_count": len(singletons),
                })
        require(len(objects) == 96, (colour, len(objects)))
        second_histograms[colour] = sorted(histogram.items())
        second_objects[colour] = tuple(objects)
        second_first_units[colour] = tuple(first_units)
        second_orbits[colour] = orbit_registry(
            objects,
            lambda obj, action: (
                transform_matching(obj[0], action),
                transform_matching(obj[1], action),
            ),
            actions,
        )

    full_histogram = Counter()
    full_completion_count = 0
    for first in first_escapes:
        first_support = base_support | frozenset(
            (endpoints, 1) for endpoints in first
        )
        for escape_zero in cap_avoiding:
            zero_support = first_support | frozenset(
                (endpoints, 0) for endpoints in escape_zero
            )
            for escape_two in cap_avoiding:
                support = zero_support | frozenset(
                    (endpoints, 2) for endpoints in escape_two
                )
                require(len(support) == 15, support)
                singletons = mixed_singleton_records(
                    base, row_inventory(base, support)
                )
                require(singletons, (first, escape_zero, escape_two))
                full_histogram[len(singletons)] += 1
                full_completion_count += 1
    require(full_completion_count == 1152, full_completion_count)

    return {
        "fixed_labels": {
            "cap": "34",
            "window": "0125",
            "tail": "tail:T",
            "core_fine": f"fine:{base.matching_name(tuple(sorted((cap,) + core)))}",
            "mate_fine": f"fine:{base.matching_name(tuple(sorted((cap,) + mate)))}",
            "mixed_operations": (
                "coefficient:111001", "coefficient:111221"
            ),
            "pure_operation": "coefficient:111111",
        },
        "base_cells": len(base_support),
        "base_escape_debt": escape_debt(base, base_support, cap),
        "cap_avoiding_matchings": len(cap_avoiding),
        "minimum_colour1_escape_new_cells": 2,
        "minimum_colour1_escapes": len(first_escapes),
        "minimum_colour1_escape_orbits": first_orbits,
        "nine_cell_local_guards": first_records,
        "nine_cell_escape_debt": 2,
        "minimum_missing_colour_escape_new_cells": 3,
        "second_escape_realizations_per_colour": 96,
        "second_escape_singleton_histograms": second_histograms,
        "second_escape_orbits": second_orbits,
        "second_escape_first_units": second_first_units,
        "full_minimum_completions": full_completion_count,
        "full_completion_singleton_histogram": sorted(full_histogram.items()),
        "terminal_ear_potential": (
            "mu=#colours without a supported cap-avoiding pure matching; "
            "mu=3 on the seven-cell guard and mu=2 after the unique first "
            "kind of minimum repair; every next minimum decrease emits a "
            "mixed singleton before recurrence"
        ),
        "theorem": (
            "the nine-cell first repair is locally consistent, but every "
            "support-minimum attempt to supply either next pure escape is "
            "an immediate mixed-row source unit"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("structural", "full", "exhaustive"),
                        default="structural")
    arguments = parser.parse_args()
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))
    base = load(
        "computations/verify_uniform_c6_oriented_complementary_face_naturality.py",
        "c6_three_direct_escape_base",
    )
    ledger = {
        "mode_independent": True,
        "dependencies": PINS,
        "audit": audit(base),
        "scope": (
            "support-minimum cap-avoiding pure escapes from the labelled "
            "seven-cell diagonal three-direct guard; nonminimum simultaneous "
            "repairs are not classified"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger changed", digest, EXPECTED_LEDGER_SHA256))

    result = ledger["audit"]
    print("C6 three-direct minimum pure-escape gate: PASS")
    print("mode", arguments.mode)
    print("first escapes / orbits", result["minimum_colour1_escapes"],
          result["minimum_colour1_escape_orbits"]["orbits"],
          result["minimum_colour1_escape_orbits"]["orbit_size_histogram"])
    print("second singleton histograms",
          result["second_escape_singleton_histograms"])
    print("second escape orbits",
          {colour: (registry["orbits"], registry["orbit_size_histogram"])
           for colour, registry in result["second_escape_orbits"].items()})
    print("full completions / singleton histogram",
          result["full_minimum_completions"],
          result["full_completion_singleton_histogram"])
    print("consequence: first local guard, then immediate source unit")
    print("sha256:", digest)


if __name__ == "__main__":
    main()
