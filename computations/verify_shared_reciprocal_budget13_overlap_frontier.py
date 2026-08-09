#!/usr/bin/env python3
"""Exact overlap census and first coefficient obstruction at budget thirteen.

Two reciprocal pairs ``pq`` and ``pr`` share ``p``.  Their deletion charts
have residual sets ``C union {r}`` and ``C union {q}``, with ``|C|=5``.
This checker couples the nine one-chart normal forms from the pinned budget
frontier, quotients the five common sites, simultaneous colour relabeling,
and exchange of the two charts, and freezes the complete 9 by 9 state table.

It then reconstructs the lexicographically first full support-shadow packet
at pure-matching multiplicity (2,2,2).  That 130-cell localized coefficient
stratum is empty over characteristic not two by an exact three-binomial odd
Laurent circuit.  No claim is made for its proper support subsets.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from itertools import permutations, product
import json
from pathlib import Path

import verify_shared_reciprocal_fullspan_budget_frontier as frontier


ROOT = Path(__file__).resolve().parents[1]
COLORS = (0, 1, 2)
COLOR_PERMUTATIONS = tuple(permutations(COLORS))
PINNED_FRONTIER_SHA256 = (
    "f555435b7f6ae19d4023ef1b98bc5753dbe2b475576c2b9c675f23f139a8cdcc"
)
EXPECTED_LEDGER_SHA256 = (
    "631187d58b99962e61bc1a5cb52d90e805e73ba085762b705bc631117450a505"
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def pin_dependency():
    path = ROOT / "computations/verify_shared_reciprocal_fullspan_budget_frontier.py"
    require(sha256(path.read_bytes()).hexdigest() == PINNED_FRONTIER_SHA256,
            "the budget-thirteen frontier dependency changed")


def permute_record(record, color_permutation):
    mask, transverse = record
    return frontier.permute_mask(mask, color_permutation), transverse


def unique_permutations(values):
    return set(permutations(values))


def raw_states(left_form, right_form):
    """Enumerate relative placements with distinguished exceptional sites."""

    states = set()
    for left_exception in set(left_form):
        left_common = list(left_form)
        left_common.remove(left_exception)
        for color_permutation in COLOR_PERMUTATIONS:
            right = tuple(
                permute_record(record, color_permutation)
                for record in right_form
            )
            for right_exception in set(right):
                right_common = list(right)
                right_common.remove(right_exception)
                for placed_right in unique_permutations(right_common):
                    states.add((
                        left_exception,
                        right_exception,
                        tuple(sorted(zip(left_common, placed_right))),
                    ))
    return states


def transform_state(state, color_permutation, exchange):
    left_exception, right_exception, common = state
    left_exception = permute_record(left_exception, color_permutation)
    right_exception = permute_record(right_exception, color_permutation)
    common = tuple(
        (permute_record(left, color_permutation),
         permute_record(right, color_permutation))
        for left, right in common
    )
    if exchange:
        left_exception, right_exception = right_exception, left_exception
        common = tuple((right, left) for left, right in common)
    return left_exception, right_exception, tuple(sorted(common))


def canonical_state(state):
    return min(
        transform_state(state, color_permutation, exchange)
        for color_permutation in COLOR_PERMUTATIONS
        for exchange in (False, True)
    )


EXPECTED_PAIR_COUNTS = (
    (578, 285, 522, 1368, 684, 1224, 2448, 684, 1224),
    (None, 70, 150, 372, 248, 336, 636, 188, 336),
    (None, None, 162, 684, 352, 624, 1224, 346, 624),
    (None, None, None, 1040, 960, 1764, 3528, 960, 1764),
    (None, None, None, None, 360, 908, 1764, 482, 908),
    (None, None, None, None, None, 938, 3384, 886, 1720),
    (None, None, None, None, None, None, 3540, 1764, 3384),
    (None, None, None, None, None, None, None, 283, 886),
    (None, None, None, None, None, None, None, None, 938),
)


def compatibility_census():
    _labelled, forms, _histogram, _labelled_histogram = (
        frontier.budget_thirteen_census()
    )
    require(len(forms) == 9, "the one-chart normal-form count changed")
    by_pair = {}
    all_states = set()
    for left in range(9):
        for right in range(left, 9):
            states = {
                canonical_state(state)
                for state in raw_states(forms[left], forms[right])
            }
            expected = EXPECTED_PAIR_COUNTS[left][right]
            require(len(states) == expected,
                    f"pair {(left, right)} state count changed: {len(states)}")
            by_pair[left, right] = states
            all_states.update(states)
    require(sum(map(len, by_pair.values())) == 47530,
            "the 9x9 upper-triangle state total changed")
    require(len(all_states) == 47530,
            "a relative state belongs to two different form pairs")
    return forms, by_pair, all_states


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(rest):
            yield ((first, second),) + tail


MATCHINGS = tuple(perfect_matchings(range(8)))
require(len(MATCHINGS) == 105, "the eight-site matching count changed")

# Sites are p,q,r,C0,...,C4 = 0,...,7.  A bit in a record mask means that
# the target axis is omitted.  The marked transverse plane may have nonzero
# entries in all three coordinate rows, so its support envelope is full.
FIRST_STATE = (
    (0, False),
    (0, False),
    (
        ((0, False), (0, False)),
        ((0, False), (1, False)),
        ((1, False), (6, False)),
        ((3, False), (4, False)),
        ((6, False), (3, True)),
    ),
)
FIRST_HEAD = (0, 1, 0, 0)  # (a,c,b,d): A_pq=E_{b,a}, A_pr=E_{d,c}


def endpoint_colors(record):
    mask, transverse = record
    if transverse:
        return set(COLORS)
    return {color for color in COLORS if not mask & (1 << color)}


def allowed_cell(state, head, left, right, left_color, right_color):
    left_exception, right_exception, common = state
    a, c, b, d = head
    left_records = [pair[0] for pair in common]
    right_records = [pair[1] for pair in common]
    if (left, right) == (0, 1):
        return (left_color, right_color) == (b, a)
    if (left, right) == (0, 2):
        return (left_color, right_color) == (d, c)
    if left == 0 or (left, right) == (1, 2):
        return True
    if left == 1:
        site = right - 3
        return (left_color in endpoint_colors(right_exception)
                and right_color in endpoint_colors(right_records[site]))
    if left == 2:
        site = right - 3
        return (left_color in endpoint_colors(left_exception)
                and right_color in endpoint_colors(left_records[site]))
    first, second = left - 3, right - 3
    return (
        left_color in endpoint_colors(left_records[first])
        and left_color in endpoint_colors(right_records[first])
        and right_color in endpoint_colors(left_records[second])
        and right_color in endpoint_colors(right_records[second])
    )


def first_support():
    support = frozenset(
        (left, right, left_color, right_color)
        for left in range(8)
        for right in range(left + 1, 8)
        for left_color in COLORS
        for right_color in COLORS
        if allowed_cell(FIRST_STATE, FIRST_HEAD, left, right,
                        left_color, right_color)
    )
    require(len(support) == 130,
            f"the first localized support changed: {len(support)}")
    return support


def supported_terms(word, support):
    terms = []
    for matching in MATCHINGS:
        monomial = tuple(sorted(
            (left, right, word[left], word[right])
            for left, right in matching
        ))
        if set(monomial) <= support:
            terms.append(monomial)
    return tuple(terms)


def support_shadow(support):
    histogram = Counter()
    term_table = {}
    for word in product(COLORS, repeat=8):
        terms = supported_terms(word, support)
        term_table[word] = terms
        histogram[len(terms)] += 1
        if len(set(word)) == 1:
            require(len(terms) == 2,
                    f"pure word {word} lost multiplicity two")
        else:
            require(len(terms) != 1,
                    f"mixed word {word} became a singleton")
    expected = {0: 2268, 2: 2835, 6: 648, 9: 810}
    require(histogram == expected,
            f"the first support-shadow histogram changed: {histogram}")
    return term_table, histogram


CIRCUIT = (
    ((0, 0, 0, 0, 1, 1, 1, 1), 1),
    ((0, 0, 0, 0, 1, 0, 2, 1), -1),
    ((0, 0, 0, 0, 0, 0, 1, 0), 1),
)


def exponent_difference(first, second):
    answer = Counter(first)
    answer.subtract(second)
    return Counter({cell: exponent for cell, exponent in answer.items()
                    if exponent})


def odd_laurent_circuit(term_table, support):
    total = Counter()
    visible = set()
    source_rows = []
    for word, multiplier in CIRCUIT:
        terms = term_table[word]
        require(len(terms) == 2,
                f"circuit word {word} stopped being binomial")
        difference = exponent_difference(terms[0], terms[1])
        for cell, exponent in difference.items():
            total[cell] += multiplier * exponent
            if not total[cell]:
                del total[cell]
        visible.update(terms[0])
        visible.update(terms[1])
        source_rows.append((word, multiplier, terms))
    require(not total, "the three Laurent exponents no longer cancel")
    require(sum(multiplier for _word, multiplier in CIRCUIT) % 2 == 1,
            "the Laurent circuit lost its odd character")
    require(visible <= support and len(visible) == 11,
            "the Laurent circuit uses a nonlocalized or changed cell set")
    return tuple(source_rows), frozenset(visible)


def main():
    pin_dependency()
    _forms, by_pair, all_states = compatibility_census()
    require(FIRST_STATE in by_pair[0, 6],
            "the first semantic state left form pair (0,6)")
    support = first_support()
    term_table, histogram = support_shadow(support)
    circuit, visible = odd_laurent_circuit(term_table, support)
    nonzero_generators = sum(bool(terms) for terms in term_table.values())
    mixed_binomials = sum(
        len(terms) == 2 and len(set(word)) > 1
        for word, terms in term_table.items()
    )
    require((nonzero_generators, mixed_binomials) == (4293, 2832),
            "the first coefficient-generator census changed")
    ledger = {
        "pinned_frontier_sha256": PINNED_FRONTIER_SHA256,
        "relative_states": len(all_states),
        "pair_counts": EXPECTED_PAIR_COUNTS,
        "first_form_pair": [0, 6],
        "first_state": FIRST_STATE,
        "first_head": FIRST_HEAD,
        "localized_cells": len(support),
        "support_sha256": sha256(json.dumps(
            sorted(support), separators=(",", ":")
        ).encode()).hexdigest(),
        "fibre_histogram": dict(sorted(histogram.items())),
        "nonzero_coefficient_generators": nonzero_generators,
        "mixed_binomials": mixed_binomials,
        "circuit_words_and_multipliers": CIRCUIT,
        "circuit_visible_cells": sorted(visible),
        "circuit_source_sha256": sha256(json.dumps(
            circuit, separators=(",", ":")
        ).encode()).hexdigest(),
        "scope": (
            "the 130-cell maximal localized support of the first semantic "
            "pair-(0,6) packet is empty over characteristic not two"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    require(digest == EXPECTED_LEDGER_SHA256,
            f"the overlap-frontier ledger changed: {digest}")
    print("shared reciprocal budget-13 overlap frontier: PASS")
    print("relative 9x9 states:", len(all_states))
    print("first semantic packet: pair (0,6), 130 localized cells")
    print("support shadow:", dict(sorted(histogram.items())))
    print("coefficient kill: three-binomial odd Laurent circuit on",
          len(visible), "cells")
    print("ledger_sha256=", digest, sep="")


if __name__ == "__main__":
    main()
