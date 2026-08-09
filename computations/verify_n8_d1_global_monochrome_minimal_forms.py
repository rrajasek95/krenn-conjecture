#!/usr/bin/env python3
"""All-size completeness of the N=8 D1 monochrome 3/4 anchors."""

from __future__ import annotations

import hashlib
import importlib
import itertools
import os
import sys
from time import monotonic

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


PINNED_M10_FRONTIER_SHA256 = (
    "40500a706dd0ba82a25df26cea95ff8231245c367f4350b9c2d9363ff1ffb64a"
)
SOURCE = os.path.join(HERE, "audit_n8_d1_m10_support_frontier.py")
with open(SOURCE, "rb") as handle:
    require(hashlib.sha256(handle.read()).hexdigest()
            == PINNED_M10_FRONTIER_SHA256,
            "the committed normal-form source changed")
A = importlib.import_module("audit_n8_d1_m10_support_frontier")
V, N, D = A.V, A.N, A.D

EXPECTED_LEDGER_SHA256 = (
    "c3b4f739b0ceb180dd3b4869dc1df72f86ee4af8a4c153b87e1060cb9e454102"
)


def colour_audit(colour, off_sigma):
    monochrome = sorted(entry for entry in off_sigma
                        if entry[2:] == (colour, colour))
    require(len(monochrome) == 22,
            "a colour no longer has 22 off-Sigma cells")
    full_traces = {
        frozenset(V.cell(u, v, colour, colour) for u, v in matching
                  if V.cell(u, v, colour, colour) in off_sigma)
        for matching in V.MATCHINGS[V.SITES]
    }
    residue_matchings = {
        frozenset(V.cell(u, v, colour, colour) for u, v in matching)
        for matching in V.MATCHINGS[V.RESIDUE]
    }
    require(len(full_traces) == 99 and len(residue_matchings) == 3,
            "the trace census changed")

    valid, minimal = {}, {}
    for size in range(2, 9):
        supports = set()
        for chosen in itertools.combinations(monochrome, size):
            support = frozenset(chosen)
            if not any(trace <= support for trace in full_traces):
                continue
            if sum(matching <= support
                   for matching in residue_matchings) == 1:
                continue
            supports.add(support)
        valid[size] = supports
        minimal[size] = {
            support for support in supports
            if not any(smaller <= support
                       for earlier in range(2, size)
                       for smaller in minimal[earlier])
        }
    require({size: len(rows) for size, rows in valid.items()} == {
        2: 0, 3: 72, 4: 1179, 5: 8382, 6: 34657,
        7: 95272, 8: 189990,
    }, "the one-colour support census through size eight changed")
    require({size: len(rows) for size, rows in minimal.items()} == {
        2: 0, 3: 72, 4: 27, 5: 0, 6: 0, 7: 0, 8: 0,
    }, "a new minimal form appeared through size eight")
    known = minimal[3] | minimal[4]
    require(minimal[3] == {state[0] for state in N.triple_states(colour)}
            and minimal[4] == {
                state[0] for state in N.special_four_supports(colour)[0]
            }, "the constructive 3/4 forms are incomplete")

    zero_checks, pair_checks = 0, 0
    for trace in full_traces:
        residue_count = sum(matching <= trace
                            for matching in residue_matchings)
        require(residue_count in (0, 1),
                "a full trace contains two residue matchings")
        if residue_count == 0:
            require(len(trace) <= 4 and any(row <= trace for row in known),
                    "a zero-residue trace escaped the known forms")
            zero_checks += 1
        for first, second in itertools.combinations(residue_matchings, 2):
            bounded = trace | first | second
            require(len(bounded) <= 8
                    and sum(row <= bounded for row in residue_matchings) >= 2
                    and any(row <= bounded for row in known),
                    "a bounded two-residue reduction escaped the known forms")
            pair_checks += 1
    require((zero_checks, pair_checks) == (96, 297),
            "the all-size reduction census changed")
    return {
        "off_monochrome_cells": len(monochrome),
        "distinct_full_traces": len(full_traces),
        "residue_perfect_matchings": len(residue_matchings),
        "valid_by_size_through_eight": {
            size: len(rows) for size, rows in sorted(valid.items())
        },
        "minimal_by_size_through_eight": {
            size: len(rows) for size, rows in sorted(minimal.items())
        },
        "zero_residue_trace_checks": zero_checks,
        "two_residue_pair_checks": pair_checks,
        "global_conclusion": ("every valid support contains one of the 72 "
                              "triples or 27 special fours"),
    }


def audit():
    started = monotonic()
    _admissible, _sigma, off_sigma, _kinds = V.reconstruct_support_domains()
    colours = {
        "b": colour_audit(0, off_sigma),
        "c": colour_audit(1, off_sigma),
    }
    ledger = {
        "pinned_m10_frontier_sha256": PINNED_M10_FRONTIER_SHA256,
        "colours": colours,
        "minimal_anchor_counts_per_colour": {"triple": 72, "special_four": 27},
        "proof": ("choose a contained full trace T; with zero residue "
                  "matchings T is a valid <=4 subset, while with at least "
                  "two choose two contained residue matchings and obtain a "
                  "valid subset of size <=8"),
        "status": "the 3/4 monochrome anchor forms are complete at all sizes",
    }
    digest = D.content_hash(ledger)
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                "the global monochrome-anchor ledger changed")
    return ledger, digest, monotonic() - started


def main():
    ledger, digest, seconds = audit()
    print("n8 D1 global monochrome minimal forms: PASS (exact)")
    print("minimal anchors per colour: 72 triples; 27 special fours")
    print("bounded reduction size: 8")
    print("scope: all monochrome support cardinalities")
    print("ledger sha256:", digest)
    print("total: %.1f s" % seconds)


if __name__ == "__main__":
    main()
