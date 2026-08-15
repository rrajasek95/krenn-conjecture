#!/usr/bin/env python3
"""Audit what low connectivity actually forces at the first rank-two tail.

The seed fibre is

    a01^00 a23^00 (a45^01 a67^22 + a46^02 a57^12)

in word 00000122.  We enumerate pure matching completions, require one
occurrence in each pure word and 3-vertex-connected aggregate support, and
ask whether the extra crossing cells must enter the seed word.  They do not:
the checker freezes the lexicographically first minimum completion for which
the seed fibre remains exactly the displayed two occurrences.

This is a deliberately sharp counterguard to a *support-only* recurrence.
It is not a full GHZ solution: its first mixed singleton is recorded.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_low_connectivity_channels.py":
        "c5b6be7eee29848ebb691df46b3c153b85f8e314fa9b189a7677e4748c5c2513",
    "notes/series-parallel-support-obstruction.md":
        "60122e27286598f5903bc53e7828ad1016fc3882830e6eca384d4275095da9f6",
    "computations/verify_n8_two_crossing_c4_three_colour_completion_guard.py":
        "d4db491cc32c73f1a0b247d4bbcf6a0365587707e5f5abe46de20c05d942a074",
    "notes/2026-08-15-n8-two-crossing-c4-three-colour-completion-guard.md":
        "767c406dd5aea4be35ac3a1fd4fb452fa7aeeceb6a49f00f58f222a37918ae84",
}

SITES = tuple(range(8))
LEFT = frozenset((0, 1, 2, 3))
RIGHT = frozenset((4, 5, 6, 7))
COLOURS = tuple(range(3))
SEED_WORD = (0, 0, 0, 0, 0, 1, 2, 2)

# Ordered endpoint colours are physical: no sorting of the last two entries.
SEED = frozenset({
    (0, 1, 0, 0),
    (2, 3, 0, 0),
    (4, 5, 0, 1),
    (6, 7, 2, 2),
    (4, 6, 0, 2),
    (5, 7, 1, 2),
})
SEED_FINES = (
    ((0, 1), (2, 3), (4, 5), (6, 7)),
    ((0, 1), (2, 3), (4, 6), (5, 7)),
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1:]
        for tail in perfect_matchings(rest):
            yield tuple(sorted(((first, second),) + tail))


MATCHINGS = tuple(sorted(perfect_matchings(SITES)))


def matching_name(matching):
    return "|".join(f"{left}{right}" for left, right in matching)


def word_name(word):
    return "".join(map(str, word))


def cell_name(cell):
    left, right, alpha, beta = cell
    return f"a{left}{right}^{alpha}{beta}"


def occurrence_cells(matching, word):
    return frozenset((left, right, word[left], word[right])
                     for left, right in matching)


def live_fines(support, word):
    return tuple(matching for matching in MATCHINGS
                 if occurrence_cells(matching, word) <= support)


def aggregate_edges(support):
    return frozenset((left, right) for left, right, _, _ in support)


def connected_after_deleting(edges, deleted):
    remaining = [site for site in SITES if site not in deleted]
    if not remaining:
        return True
    adjacency = {site: set() for site in remaining}
    for left, right in edges:
        if left in adjacency and right in adjacency:
            adjacency[left].add(right)
            adjacency[right].add(left)
    seen = {remaining[0]}
    stack = [remaining[0]]
    while stack:
        site = stack.pop()
        for other in adjacency[site] - seen:
            seen.add(other)
            stack.append(other)
    return len(seen) == len(remaining)


def three_vertex_connected(edges):
    return all(connected_after_deleting(edges, frozenset(deleted))
               for size in range(3)
               for deleted in combinations(SITES, size))


def crossing_count(matching):
    return sum((left in LEFT) != (right in LEFT)
               for left, right in matching)


def common_tail_count(matching):
    return sum(edge in {(0, 1), (2, 3)} for edge in matching)


def classify_matching_geometry():
    histogram = Counter((crossing_count(matching),
                         common_tail_count(matching))
                        for matching in MATCHINGS)
    require(histogram == {
        (0, 0): 6,
        (0, 2): 3,
        (2, 0): 48,
        (2, 1): 24,
        (4, 0): 24,
    }, histogram)
    require(all(crossing_count(matching) % 2 == 0
                for matching in MATCHINGS), histogram)
    live = frozenset(SEED_FINES)
    remaining = [matching for matching in MATCHINGS if matching not in live]
    local_third = [matching for matching in remaining
                   if common_tail_count(matching) == 2]
    tail_changing = [matching for matching in remaining
                     if common_tail_count(matching) < 2]
    separator_breaking = [matching for matching in tail_changing
                          if crossing_count(matching) > 0]
    require(tuple(local_third) == (
        ((0, 1), (2, 3), (4, 7), (5, 6)),), local_third)
    require(len(tail_changing) == 102, len(tail_changing))
    require(len(separator_breaking) == 96, len(separator_breaking))
    return {
        f"crossings={crossings},common_tail={common}": count
        for (crossings, common), count in sorted(histogram.items())
    } | {
        "rank_two_fibre_remaining_local_mates": len(local_third),
        "rank_two_fibre_remaining_tail_changing_mates": len(tail_changing),
        "rank_two_fibre_remaining_separator_crossing_mates":
            len(separator_breaking),
    }


def supported_occurrence_inventory(support):
    decorations = defaultdict(list)
    for left, right, alpha, beta in support:
        decorations[(left, right)].append((alpha, beta))
    counts = Counter()
    fines = defaultdict(list)
    for matching in MATCHINGS:
        choices = [decorations[edge] for edge in matching]
        if any(not choice for choice in choices):
            continue
        for endpoint_colours in product(*choices):
            word = [None] * len(SITES)
            for (left, right), (alpha, beta) in zip(
                    matching, endpoint_colours, strict=True):
                word[left] = alpha
                word[right] = beta
            word = tuple(word)
            counts[word] += 1
            fines[word].append(matching)
    return counts, fines


def pure_completion_guard():
    pure_choices = []
    for colour in COLOURS:
        rows = []
        word = (colour,) * len(SITES)
        for matching in MATCHINGS:
            cells = occurrence_cells(matching, word)
            rows.append((matching, cells, len(cells - SEED)))
        pure_choices.append(tuple(rows))

    pure_lower_bounds = tuple(min(row[2] for row in rows)
                              for rows in pure_choices)
    require(pure_lower_bounds == (2, 4, 3), pure_lower_bounds)

    minimum_added = None
    guards = []
    candidate_count = 0
    for row0 in pure_choices[0]:
        for row1 in pure_choices[1]:
            for row2 in pure_choices[2]:
                candidate_count += 1
                chosen = (row0, row1, row2)
                support = SEED | frozenset().union(
                    *(row[1] for row in chosen))
                added = len(support - SEED)
                if minimum_added is not None and added > minimum_added:
                    continue
                edges = aggregate_edges(support)
                if not three_vertex_connected(edges):
                    continue
                pure_counts = tuple(len(live_fines(
                    support, (colour,) * len(SITES)))
                    for colour in COLOURS)
                if pure_counts != (1, 1, 1):
                    continue
                seed_fines = live_fines(support, SEED_WORD)
                if seed_fines != SEED_FINES:
                    continue
                record = (tuple(row[0] for row in chosen), support)
                if minimum_added is None or added < minimum_added:
                    minimum_added = added
                    guards = [record]
                elif added == minimum_added:
                    guards.append(record)

    require(minimum_added is not None, "no guard")
    guards.sort(key=lambda item: tuple(map(matching_name, item[0])))
    pure_matchings, support = guards[0]
    counts, fines = supported_occurrence_inventory(support)
    mixed_singletons = tuple(sorted(
        word for word, count in counts.items()
        if len(set(word)) > 1 and count == 1))
    require(mixed_singletons, "counterguard accidentally satisfies support rows")
    first = mixed_singletons[0]

    crossing_cells = tuple(sorted(
        cell for cell in support - SEED
        if (cell[0] in LEFT) != (cell[1] in LEFT)))
    compatible_crossing_cells = tuple(
        cell for cell in crossing_cells
        if (cell[2], cell[3]) == (SEED_WORD[cell[0]],
                                  SEED_WORD[cell[1]]))
    require(crossing_cells, "3-connectivity supplied no crossing")
    require(not compatible_crossing_cells, compatible_crossing_cells)

    edge_degrees = Counter()
    for left, right in aggregate_edges(support):
        edge_degrees[left] += 1
        edge_degrees[right] += 1
    require(min(edge_degrees.values()) >= 3, edge_degrees)

    # The displayed Laurent point is exact on the protected rows: seed
    # monomials are +1 and -1; every chosen pure monomial is +1.
    values = {cell: 1 for cell in support}
    values[(5, 7, 1, 2)] = -1
    seed_values = []
    for matching in SEED_FINES:
        value = 1
        for cell in occurrence_cells(matching, SEED_WORD):
            value *= values[cell]
        seed_values.append(value)
    require(tuple(seed_values) == (1, -1), seed_values)
    pure_values = []
    for colour in COLOURS:
        live = live_fines(support, (colour,) * len(SITES))
        require(len(live) == 1, live)
        value = 1
        for cell in occurrence_cells(live[0], (colour,) * len(SITES)):
            value *= values[cell]
        pure_values.append(value)
    require(tuple(pure_values) == (1, 1, 1), pure_values)

    # Classify every possible source-labelled mate of the first singleton.
    # Keeping both protected tail edges is equivalent to staying in the
    # local C4 fibre.  Every other mate strictly lowers the number of those
    # tail edges, and its crossing count is even.
    first_fine = fines[first][0]
    mate_histogram = Counter()
    mate_records = []
    for matching in MATCHINGS:
        if matching == first_fine:
            continue
        cells = occurrence_cells(matching, first)
        additions = cells - support
        geometry = (crossing_count(matching),
                    common_tail_count(matching), len(additions))
        mate_histogram[geometry] += 1
        mate_records.append((len(additions), matching, additions, geometry))
    require(len(mate_records) == 104, len(mate_records))
    require(all(geometry[0] % 2 == 0
                for _, _, _, geometry in mate_records), mate_records)
    require(all((geometry[1] == 2) == (geometry[0] == 0 and
                                       {(0, 1), (2, 3)} <= set(matching))
                for _, matching, _, geometry in mate_records), mate_records)
    local_mates = [record for record in mate_records
                   if record[3][1] == 2]
    require(len(local_mates) == 2, local_mates)
    tail_changing_mates = [record for record in mate_records
                           if record[3][1] < 2]
    separator_crossing_mates = [record for record in tail_changing_mates
                                if record[3][0] > 0]
    require(len(tail_changing_mates) == 102, len(tail_changing_mates))
    require(len(separator_crossing_mates) == 96,
            len(separator_crossing_mates))
    minimum_mate_additions = min(record[0] for record in mate_records)
    minimum_mates = sorted(record for record in mate_records
                           if record[0] == minimum_mate_additions)

    def mate_record(record):
        additions, matching, cells, geometry = record
        return {
            "fine": matching_name(matching),
            "new_cells": tuple(map(cell_name, sorted(cells))),
            "crossing_edges": geometry[0],
            "retained_protected_tail_edges": geometry[1],
            "new_cell_count": additions,
        }

    return {
        "enumerated_pure_matching_triples": candidate_count,
        "new_cell_lower_bounds_by_pure_colour": pure_lower_bounds,
        "minimum_new_cells": minimum_added,
        "minimum_guard_count": len(guards),
        "canonical_pure_matchings": tuple(map(matching_name,
                                                pure_matchings)),
        "canonical_added_cells": tuple(map(cell_name,
                                             sorted(support - SEED))),
        "aggregate_edges": tuple(matching_name((edge,))
                                 for edge in sorted(aggregate_edges(support))),
        "aggregate_degrees": tuple(edge_degrees[site] for site in SITES),
        "aggregate_is_3_vertex_connected": True,
        "extra_crossing_cells": tuple(map(cell_name, crossing_cells)),
        "seed_word_compatible_extra_crossing_cells": tuple(
            map(cell_name, compatible_crossing_cells)),
        "seed_word": word_name(SEED_WORD),
        "seed_live_fines": tuple(map(matching_name,
                                       live_fines(support, SEED_WORD))),
        "seed_monomial_values": tuple(seed_values),
        "seed_row_value": sum(seed_values),
        "pure_row_values": tuple(pure_values),
        "supported_word_count": len(counts),
        "mixed_singleton_count": len(mixed_singletons),
        "first_mixed_singleton": {
            "word": word_name(first),
            "fine": matching_name(fines[first][0]),
            "cells": tuple(map(cell_name,
                               sorted(occurrence_cells(fines[first][0],
                                                       first)))),
        },
        "first_singleton_mate_geometry": {
            f"crossings={crossings},common_tail={common},new={new}": count
            for (crossings, common, new), count
            in sorted(mate_histogram.items())
        },
        "minimum_mate_new_cells": minimum_mate_additions,
        "minimum_mates": tuple(map(mate_record, minimum_mates)),
        "local_same_tail_mates": tuple(map(mate_record,
                                             sorted(local_mates))),
        "tail_changing_mate_count": len(tail_changing_mates),
        "separator_crossing_mate_count": len(separator_crossing_mates),
        "tail_potential_statement": (
            "for the protected tail C={01,23}, every mate either retains "
            "C and is one of the two local C4 fines, or changes the literal "
            "fine and strictly lowers |C intersection M| from 2 to at most "
            "1; the latter is a finite fixed-word recurrence, not a global "
            "support contraction"
        ),
        "verdict": (
            "pure normalization and 3-vertex-connected aggregate support "
            "do not force a crossing into the protected rank-two fibre; "
            "the canonical guard is killed instead by its first mixed "
            "singleton"
        ),
    }


def build_ledger():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        if expected != "TO_BE_FILLED":
            require(actual == expected,
                    ("pinned dependency changed", relative, actual, expected))
    return {
        "theorem": "rank-two-tail separator-breaking counterguard",
        "matching_geometry": classify_matching_geometry(),
        "full_pure_guard": pure_completion_guard(),
        "scope": (
            "exhaustive for all triples of eight-site pure perfect "
            "matchings added to the six-cell seed, with exactly one live "
            "occurrence in each pure word and 3-vertex-connected aggregate "
            "support; it does not impose all mixed GHZ rows"
        ),
    }


EXPECTED_LEDGER_SHA256 = "16601e3a9b4ecb8fadfd3ed46402bc5214a3b554bcb1e63c313485f162ef2750"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("structural", "full", "exhaustive"),
                        default="structural")
    parser.parse_args()
    ledger = build_ledger()
    digest = sha256(json.dumps(ledger, sort_keys=True,
                               separators=(",", ":")).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256, (digest,
                                                   EXPECTED_LEDGER_SHA256))
    print(json.dumps(ledger, indent=2, sort_keys=True))
    print("ledger_sha256", digest)


if __name__ == "__main__":
    main()
