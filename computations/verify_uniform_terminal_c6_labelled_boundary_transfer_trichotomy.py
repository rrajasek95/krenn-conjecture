#!/usr/bin/env python3
"""Labelled boundary-transfer theorem and rowwise C6 counterguard.

This checker works in the literal occurrence module of a diagonal tight C6.
It keeps the output word, fine matching, operation, oriented cap window, and
the two separated shore states.  It verifies two sharply different facts:

* a rowwise ``different label => private or C4`` trichotomy is false, with a
  normalized pure row on the full-colour C6 as the smallest alternating-cycle
  counterguard; and
* at packet level the sharp three-pure-channel support has six literal private
  mixed rows.  Their only possible local repairs are the two oriented C4
  flips, and all 64 first repair packets retain a private mixed row.

No B/Eq, cap-presentation, or declared operation generator is used.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction
import hashlib
from itertools import combinations, product
import json


N = 6
VERTICES = tuple(range(N))
COLOURS = tuple(range(3))
SHORE = frozenset((0, 1, 2))


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def edge(left, right):
    return tuple(sorted((left, right)))


def perfect_matchings(vertices):
    vertices = tuple(sorted(vertices))
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1:]
        for tail in perfect_matchings(rest):
            yield tuple(sorted(((first, second),) + tail))


MATCHINGS = tuple(sorted(perfect_matchings(VERTICES)))
A_CHANNEL = tuple(sorted((edge(0, 1), edge(2, 3), edge(4, 5))))
B_CHANNEL = tuple(sorted((edge(0, 5), edge(1, 2), edge(3, 4))))
CYCLE_EDGES = frozenset(A_CHANNEL + B_CHANNEL)
CHANNELS = (A_CHANNEL, B_CHANNEL)


def occurrence_cells(matching, word):
    if any(word[left] != word[right] for left, right in matching):
        return None
    return frozenset((endpoints, word[endpoints[0]])
                     for endpoints in matching)


def occurrence_fibre(word, support):
    answer = []
    for matching in MATCHINGS:
        cells = occurrence_cells(matching, word)
        if cells is not None and cells <= support:
            answer.append((matching, cells))
    return tuple(answer)


def oriented_cut_edge(matching):
    crossing = tuple(endpoints for endpoints in matching
                     if (endpoints[0] in SHORE) !=
                     (endpoints[1] in SHORE))
    require(len(crossing) == 1, (matching, crossing))
    left, right = crossing[0]
    return (left, right) if left in SHORE else (right, left)


def boundary_label(word, matching):
    cap_window = oriented_cut_edge(matching)
    left_vertex, right_vertex = cap_window
    left_state = tuple(endpoints for endpoints in matching
                       if set(endpoints) <= SHORE)
    right_state = tuple(endpoints for endpoints in matching
                        if not (set(endpoints) & SHORE))
    require(len(left_state) == len(right_state) == 1,
            (matching, left_state, right_state))
    return {
        "word": "".join(map(str, word)),
        "fine_matching": "|".join(
            f"{left}{right}" for left, right in matching
        ),
        "operation": "tight_cut_restriction_reinsertion",
        "cap_window_L_to_R": f"{left_vertex}>{right_vertex}",
        "cap_colour": word[left_vertex],
        "left_near_state": f"{left_state[0][0]}{left_state[0][1]}",
        "right_near_state": f"{right_state[0][0]}{right_state[0][1]}",
    }


def full_colour_rowwise_counterguard():
    support = frozenset((endpoints, colour)
                        for endpoints in CYCLE_EDGES
                        for colour in COLOURS)
    word = (0,) * N
    fibre = occurrence_fibre(word, support)
    require(tuple(matching for matching, _cells in fibre) == CHANNELS,
            fibre)
    labels = tuple(boundary_label(word, matching)
                   for matching, _cells in fibre)
    require(labels[0] != labels[1], labels)
    require({label["cap_window_L_to_R"] for label in labels}
            == {"2>3", "0>5"}, labels)

    # Give one edge in each channel coefficient 1/2 and every other selected
    # cell coefficient 1.  The literal pure coefficient is exactly 1.
    weights = {(endpoints, colour): Fraction(1)
               for endpoints, colour in support}
    weights[(edge(0, 1), 0)] = Fraction(1, 2)
    weights[(edge(1, 2), 0)] = Fraction(1, 2)
    terms = tuple(
        product_value(weights[cell] for cell in cells)
        for _matching, cells in fibre
    )
    require(terms == (Fraction(1, 2), Fraction(1, 2))
            and sum(terms) == 1, terms)

    symmetric_difference = set(fibre[0][0]) ^ set(fibre[1][0])
    require(symmetric_difference == CYCLE_EDGES,
            symmetric_difference)
    require(len(symmetric_difference) == 6, symmetric_difference)

    common_cells = fibre[0][1] & fibre[1][1]
    require(not common_cells, common_cells)
    return {
        "normalized_word": "000000",
        "literal_term_weights": tuple(map(str, terms)),
        "fibre_rank": len(fibre),
        "labels": labels,
        "private_occurrence": False,
        "common_nonconstant_cell_factor": False,
        "symmetric_difference_cycle_length": 6,
        "oriented_complementary_C4": False,
        "scope": "one exact normalized source coefficient, not a full GHZ packet",
    }


def product_value(values):
    answer = Fraction(1)
    for value in values:
        answer *= value
    return answer


def canonical_support_and_debts():
    support = frozenset(
        ((endpoints, 0) for endpoints in A_CHANNEL)
    ) | frozenset(
        ((endpoints, colour)
         for endpoints in B_CHANNEL for colour in (1, 2))
    )
    pure_fibres = tuple(occurrence_fibre((colour,) * N, support)
                        for colour in COLOURS)
    require(tuple(len(fibre) for fibre in pure_fibres) == (1, 1, 1),
            pure_fibres)
    require(tuple(fibre[0][0] for fibre in pure_fibres)
            == (A_CHANNEL, B_CHANNEL, B_CHANNEL), pure_fibres)

    debts = []
    for assignment in product((1, 2), repeat=3):
        if len(set(assignment)) == 1:
            continue
        word = [None] * N
        for endpoints, colour in zip(B_CHANNEL, assignment, strict=True):
            for vertex in endpoints:
                word[vertex] = colour
        word = tuple(word)
        fibre = occurrence_fibre(word, support)
        require(len(fibre) == 1 and fibre[0][0] == B_CHANNEL,
                (word, fibre))
        debts.append(word)
    debts = tuple(sorted(debts))
    require(tuple("".join(map(str, word)) for word in debts) == (
        "111221", "122111", "122221",
        "211112", "211222", "222112",
    ), debts)
    return support, pure_fibres, debts


def complementary_c4_options(word, core_matching, support):
    counts = Counter(word)
    require(sorted(counts.values()) == [2, 4], (word, counts))
    minority_colour = next(colour for colour, count in counts.items()
                           if count == 2)
    majority_colour = next(colour for colour, count in counts.items()
                           if count == 4)
    minority_vertices = tuple(vertex for vertex, colour in enumerate(word)
                              if colour == minority_colour)
    cap_window = edge(*minority_vertices)
    require(cap_window in core_matching, (word, core_matching, cap_window))
    cap_orientation = cap_window

    compatible = tuple(
        matching for matching in MATCHINGS
        if occurrence_cells(matching, word) is not None
    )
    require(len(compatible) == 3 and core_matching in compatible,
            (word, compatible))
    alternatives = tuple(matching for matching in compatible
                         if matching != core_matching)
    records = []
    for side, matching in zip(("left", "right"), alternatives, strict=True):
        cells = occurrence_cells(matching, word)
        missing = cells - support
        symmetric_difference = set(matching) ^ set(core_matching)
        require(cap_window in set(matching) & set(core_matching),
                (word, matching, cap_window))
        require(len(symmetric_difference) == 4
                and all(cell[1] == majority_colour for cell in missing)
                and len(missing) == 2,
                (word, matching, missing, symmetric_difference))
        records.append({
            "operation": f"oriented_complementary_C4_{side}",
            "cap_window_order": f"{cap_orientation[0]}>{cap_orientation[1]}",
            "cap_colour": minority_colour,
            "majority_colour": majority_colour,
            "fine_matching": "|".join(
                f"{left}{right}" for left, right in matching
            ),
            "missing_cells": tuple(
                f"{endpoints[0]}{endpoints[1]};{colour}"
                for endpoints, colour in sorted(missing)
            ),
            "changed_edges": tuple(
                f"{left}{right}" for left, right in sorted(symmetric_difference)
            ),
            "missing_cell_set": missing,
        })
    return tuple(records)


def packet_level_trichotomy():
    support, pure_fibres, debts = canonical_support_and_debts()
    option_ledger = []
    options = []
    for word in debts:
        core_matching, _cells = occurrence_fibre(word, support)[0]
        records = complementary_c4_options(word, core_matching, support)
        options.append(tuple(record["missing_cell_set"] for record in records))
        option_ledger.append({
            "word": "".join(map(str, word)),
            "private_label": boundary_label(word, core_matching),
            "alternatives": tuple(
                {key: value for key, value in record.items()
                 if key != "missing_cell_set"}
                for record in records
            ),
        })

    residual_histogram = Counter()
    pure_histogram = Counter()
    best = None
    for choices in product((0, 1), repeat=len(debts)):
        additions = frozenset().union(*(
            options[index][choice] for index, choice in enumerate(choices)
        ))
        require(len(additions) == 12, (choices, additions))
        repaired = support | additions
        residual = tuple(
            word for word in product(COLOURS, repeat=N)
            if len(set(word)) > 1
            and len(occurrence_fibre(word, repaired)) == 1
        )
        pure_counts = tuple(len(occurrence_fibre((colour,) * N, repaired))
                            for colour in COLOURS)
        residual_histogram[len(residual)] += 1
        pure_histogram[pure_counts] += 1
        if best is None or len(residual) < best:
            best = len(residual)
    require(best == 6, best)
    require(residual_histogram == Counter({
        6: 3, 8: 6, 10: 6, 15: 8, 17: 12, 18: 1,
        19: 6, 23: 6, 24: 7, 28: 3, 30: 6,
    }), residual_histogram)
    require(pure_histogram == Counter({
        (1, 4, 4): 16,
        (1, 4, 6): 16,
        (1, 6, 4): 16,
        (1, 6, 6): 16,
    }), pure_histogram)

    return {
        "boundary_module_basis_fields": (
            "word", "fine_matching", "operation",
            "cap_window_L_to_R", "cap_colour",
            "left_near_state", "right_near_state",
        ),
        "pure_channel_fines": tuple(
            boundary_label((colour,) * N, fibre[0][0])
            for colour, fibre in enumerate(pure_fibres)
        ),
        "private_mixed_debts": tuple(option_ledger),
        "private_debt_count": len(debts),
        "C4_mates_per_debt": 2,
        "minimal_repair_packets": 64,
        "pure_occurrence_histogram": tuple(
            (key, value) for key, value in sorted(pure_histogram.items())
        ),
        "residual_private_histogram": tuple(sorted(residual_histogram.items())),
        "minimum_residual_private_rows": best,
    }


def separated_rank_one_factorization_criterion():
    # A labelled fold is extra data.  Once supplied, two separated channel
    # blocks with the same tail label factor through the one-dimensional tail
    # module.  Different fine/cap labels do not manufacture that fold.
    rows = ("xy", "xz", "yz")
    channels = ("internal", "through")
    matrix = tuple(tuple(f"u_{row}*E_{row}*T_{channel}"
                         for channel in channels)
                   for row in rows)
    quotiented = tuple(f"u_{row}*E_{row}*(T_internal+T_through)"
                       for row in rows)
    require(len(matrix) == 3 and all(len(row) == 2 for row in matrix), matrix)
    require(all("T_internal+T_through" in row for row in quotiented),
            quotiented)
    return {
        "separated_transfer_shape": matrix,
        "label_preserving_fold_required": True,
        "rank_one_tail_after_fold": quotiented,
        "automatic_from_distinct_labels": False,
    }


def build_ledger():
    return {
        "theorem": "terminal C6 labelled boundary-transfer trichotomy",
        "rank_one_criterion": separated_rank_one_factorization_criterion(),
        "rowwise_counterguard": full_colour_rowwise_counterguard(),
        "packet_level_theorem": packet_level_trichotomy(),
        "verdict": (
            "rowwise trichotomy false; packet-level pure-normalized C6 "
            "forces a private mixed detector or an oriented C4/outside exit"
        ),
        "scope": (
            "literal diagonal tight-C6 occurrence module; not a full-source "
            "terminal-ear classification and not an active clean cap theorem"
        ),
    }


EXPECTED_LEDGER_SHA256 = "b75dd428c950a94ce6d2ec4fc4cb22e4a63a48d0f14d9607b2f97ee7a4d5f5ce"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("structural", "full", "exhaustive"),
                        default="structural")
    parser.add_argument("--dump-ledger", action="store_true")
    arguments = parser.parse_args()
    ledger = build_ledger()
    encoded = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = hashlib.sha256(encoded.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256:
        require(digest == EXPECTED_LEDGER_SHA256,
                f"labelled C6 ledger changed: {digest}")
    if arguments.dump_ledger:
        print(json.dumps(ledger, indent=2, sort_keys=True))
    print("uniform terminal-C6 labelled boundary-transfer theorem: PASS")
    print("mode", arguments.mode)
    print("ledger_sha256", digest)
    print("rowwise trichotomy: FALSE (normalized alternating C6 counterguard)")
    print("packet theorem: private mixed detector or oriented C4/outside exit")


if __name__ == "__main__":
    main()
