#!/usr/bin/env python3
"""Coefficient-complete emptiness of the frozen sharp r=4 support chart.

The selected twenty-block packet is imported from the exact incidence
frontier.  Every selected witness arc fixes the factor at its head to its
target coordinate axis.  All other endpoint factors are deliberately
relaxed to arbitrary ternary vectors.  Thus the matching rows computed here
are an upper bound on the terms available in every source-faithful equality
stratum with these labelled arcs.

The pure 0 and pure 1 rows are empty even in this relaxation.  Hence the
literal GHZ coefficient ideal contains the integer unit -1.  Arbitrary
nonzero edge weights and arbitrary free endpoint entries cannot repair the
chart.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from hashlib import sha256
import importlib.util
from itertools import product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEPENDENCIES = {
    "computations/verify_n8_r4_matching_incidence_frontier.py":
        "0b75a605b4f393f795fca0cce90cc5785a1a1f0b2e86a393381142bbdfa59353",
    "notes/n8-r4-matching-incidence-frontier.md":
        "618c20989fdbf6d5219e5611af662f8fe12904c966438d0249eef663db9dd04b",
}
EXPECTED_LEDGER_SHA256 = (
    "19ab47c47af694f0d15c740b8f3c78d292117b9482cb14ae7bb8372c3438a03e"
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load_frontier():
    path = ROOT / "computations/verify_n8_r4_matching_incidence_frontier.py"
    spec = importlib.util.spec_from_file_location("r4_frontier", path)
    require(spec is not None and spec.loader is not None,
            "could not load the r=4 frontier dependency")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def pin_dependencies():
    for relative, expected in DEPENDENCIES.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, f"dependency drift: {relative}")


def endpoint_allowed_colours(frontier, selected):
    """Return the maximal endpoint supports allowed by the head labels."""

    allowed = {}
    all_colours = frozenset(frontier.COLORS)
    for left, right in selected:
        for site, other in ((left, right), (right, left)):
            incoming = (other, site)
            if incoming in frontier.ARCS:
                allowed[(site, other)] = frozenset({frontier.LABEL[incoming]})
            else:
                # This factor is free at the selected-witness level.  Giving
                # it all three coordinates is a relaxation of every common-
                # line and essential-line constraint, hence safe for an
                # emptiness certificate.
                allowed[(site, other)] = all_colours
    require(len(allowed) == 2 * len(selected),
            "endpoint-domain count changed")
    return allowed


def sparse_rows(frontier, selected, allowed):
    matchings = tuple(frontier.perfect_matchings(range(frontier.N), selected))
    require(len(matchings) == 24, "selected-support matching count changed")
    rows = defaultdict(list)
    for matching in matchings:
        local_options = []
        for left, right in matching:
            local_options.append(tuple(
                (left_colour, right_colour)
                for left_colour in allowed[(left, right)]
                for right_colour in allowed[(right, left)]
            ))
        for choices in product(*local_options):
            word = [None] * frontier.N
            for (left, right), (left_colour, right_colour) in zip(
                    matching, choices):
                word[left] = left_colour
                word[right] = right_colour
            rows[tuple(word)].append(matching)
    return matchings, rows


def realized_rows(frontier, selected, endpoint):
    rows = defaultdict(list)
    matchings = tuple(frontier.perfect_matchings(range(frontier.N), selected))
    for matching in matchings:
        local_options = []
        for left, right in matching:
            local_options.append(tuple(
                (left_colour, right_colour)
                for left_colour in frontier.COLORS
                for right_colour in frontier.COLORS
                if endpoint[(left, right)][left_colour]
                and endpoint[(right, left)][right_colour]
            ))
        for choices in product(*local_options):
            word = [None] * frontier.N
            for (left, right), (left_colour, right_colour) in zip(
                    matching, choices):
                word[left] = left_colour
                word[right] = right_colour
            rows[tuple(word)].append(matching)
    return rows


def audit():
    pin_dependencies()
    frontier = load_frontier()
    selected, _support, common, endpoint = frontier.build_endpoint_lines()
    frontier.audit_selected_witnesses(selected, common, endpoint)
    allowed = endpoint_allowed_colours(frontier, selected)
    matchings, maximal_rows = sparse_rows(frontier, selected, allowed)
    fixed_rows = realized_rows(frontier, selected, endpoint)

    pure_words = {colour: (colour,) * frontier.N
                  for colour in frontier.COLORS}
    maximal_pure_counts = {
        colour: len(maximal_rows.get(word, ()))
        for colour, word in pure_words.items()
    }
    fixed_pure_counts = {
        colour: len(fixed_rows.get(word, ()))
        for colour, word in pure_words.items()
    }
    require(maximal_pure_counts[0] == 0,
            "a pure-0 matching appeared in the head-axis relaxation")
    require(maximal_pure_counts[1] == 0,
            "a pure-1 matching appeared in the head-axis relaxation")
    require(maximal_pure_counts[2] > 0,
            "the surviving pure-2 row disappeared")
    require(all(fixed_pure_counts[colour] <= maximal_pure_counts[colour]
                for colour in frontier.COLORS),
            "the fixed line packet exceeded its endpoint relaxation")

    maximal_histogram = Counter(len(terms) for terms in maximal_rows.values())
    fixed_histogram = Counter(len(terms) for terms in fixed_rows.values())
    require(sum(maximal_histogram.values()) <= 3 ** frontier.N,
            "too many output words in the sparse system")

    # The GHZ coefficient equation in the pure-zero row is F_{0^8}-1=0.
    # Because that row has no source monomial at all, this generator is the
    # literal constant -1 over Z.  No localization or characteristic
    # assumption is used.
    unit_generator = -1
    require(unit_generator == -1 and maximal_pure_counts[0] == 0,
            "the integer unit certificate changed")

    ledger = {
        "sites": frontier.N,
        "selected_blocks": len(selected),
        "physical_matchings": len(matchings),
        "target_words": 3 ** frontier.N,
        "maximal_nonzero_rows": len(maximal_rows),
        "fixed_nonzero_rows": len(fixed_rows),
        "maximal_row_term_histogram": dict(sorted(maximal_histogram.items())),
        "fixed_row_term_histogram": dict(sorted(fixed_histogram.items())),
        "maximal_pure_counts": maximal_pure_counts,
        "fixed_pure_counts": fixed_pure_counts,
        "unit_equation": "F_00000000-1=-1",
        "base_ring": "Z[edge weights, free endpoint entries]",
        "verdict": "selected-20 labelled support chart is empty",
        "scope": (
            "fixed selected support and witness head labels from b369357; "
            "all unforced endpoint factors arbitrary; not all r=4 label or "
            "good-graph orbits"
        ),
    }
    encoded = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(encoded.encode("ascii")).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                "the selected-20 coefficient ledger changed")
    return ledger, digest


def main():
    ledger, digest = audit()
    print("N=8 r=4 selected-20 full-source chart: EMPTY")
    print("physical matchings:", ledger["physical_matchings"])
    print("maximal/fixed nonzero rows:",
          ledger["maximal_nonzero_rows"], ledger["fixed_nonzero_rows"])
    print("maximal pure counts:", ledger["maximal_pure_counts"])
    print("unit equation:", ledger["unit_equation"])
    print("sha256:", digest)


if __name__ == "__main__":
    main()
