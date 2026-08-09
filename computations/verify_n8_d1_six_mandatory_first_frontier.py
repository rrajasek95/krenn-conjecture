#!/usr/bin/env python3
"""Freeze the first semantic D1 frontier from only six mandatory cells."""

from __future__ import annotations

import hashlib
import importlib
import itertools
import os
import sys
from collections import Counter
from fractions import Fraction
from time import monotonic

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


PINNED_CANDIDATE_SHA256 = (
    "28b5de217d61dbe41c699657fb7ad3d7f29d0a42521a2e9b99926d135cf8b8ca"
)
PINNED_PURE_LIFT_SHA256 = (
    "993f1f578e53cee526f4a8a0050266c683cd67a5494663a7e5c0713d6d81a0ac"
)
PINNED_TRIPOD_SHA256 = (
    "11c8f8ac09ea7d37e330d9a6482b27d53c6d67f2cefd2addd1d869edf631971f"
)
for filename, expected in (
    ("verify_n8_d1_m10_334_branch63_candidate.py", PINNED_CANDIDATE_SHA256),
    ("verify_n8_d1_escape85_pure_fibre_factorization.py",
     PINNED_PURE_LIFT_SHA256),
    ("verify_n8_d1_tripod_two_kernel_obstruction.py",
     PINNED_TRIPOD_SHA256),
):
    with open(os.path.join(HERE, filename), "rb") as handle:
        require(hashlib.sha256(handle.read()).hexdigest() == expected,
                "a pinned D1 frontier dependency changed: %s" % filename)

C = importlib.import_module("verify_n8_d1_m10_334_branch63_candidate")
D, V = C.D, C.V
T = importlib.import_module("verify_n8_d1_tripod_two_kernel_obstruction")

EXPECTED_LEDGER_SHA256 = (
    "1ca524ac641f7f2a3d4783eb3459a0878f37f5031f2e8bd7d2c390cc84dea4c0"
)

MANDATORY = frozenset({
    (0, 1, 0, 0), (0, 2, 0, 1), (0, 2, 2, 2),
    (1, 3, 0, 1), (1, 3, 2, 2), (2, 3, 1, 1),
})

# First deterministic semantic escape after restarting the exploratory CEGAR
# from MANDATORY rather than the 77-cell branch-63 support.  This payload is
# the proof input; the checker never trusts the CEGAR run or its clauses.
SUPPORT = frozenset({
    (0, 1, 0, 0), (0, 1, 0, 1), (0, 1, 1, 0), (0, 1, 1, 1),
    (0, 2, 0, 0), (0, 2, 0, 1), (0, 2, 1, 0), (0, 2, 1, 1),
    (0, 2, 2, 2), (0, 3, 0, 1),
    (0, 4, 0, 0), (0, 4, 0, 1), (0, 4, 1, 0),
    (0, 5, 0, 1), (0, 5, 1, 1), (0, 5, 1, 2),
    (0, 6, 0, 0), (0, 6, 0, 2), (0, 6, 1, 0), (0, 6, 1, 2),
    (0, 7, 0, 2), (0, 7, 1, 2),
    (1, 2, 0, 0), (1, 2, 0, 1), (1, 2, 1, 0),
    (1, 3, 0, 1), (1, 3, 1, 1), (1, 3, 2, 2),
    (1, 4, 0, 0), (1, 4, 0, 2), (1, 4, 1, 0), (1, 4, 1, 2),
    (1, 5, 0, 0), (1, 5, 0, 1), (1, 5, 1, 0), (1, 5, 1, 1),
    (1, 5, 1, 2),
    (1, 6, 0, 1), (1, 6, 0, 2), (1, 6, 1, 0), (1, 6, 1, 1),
    (1, 6, 1, 2),
    (1, 7, 0, 0), (1, 7, 0, 2), (1, 7, 1, 0), (1, 7, 1, 2),
    (2, 3, 0, 1), (2, 3, 1, 1),
    (2, 4, 0, 0), (2, 4, 0, 1), (2, 4, 1, 0), (2, 4, 1, 1),
    (2, 4, 1, 2),
    (2, 5, 0, 0), (2, 5, 0, 1), (2, 5, 0, 2), (2, 5, 1, 0),
    (2, 5, 1, 2),
    (2, 6, 0, 1), (2, 6, 0, 2), (2, 6, 1, 1), (2, 6, 1, 2),
    (2, 7, 0, 0), (2, 7, 0, 2), (2, 7, 1, 0), (2, 7, 1, 2),
    (3, 4, 1, 2),
    (3, 5, 0, 1), (3, 5, 1, 0), (3, 5, 1, 1), (3, 5, 1, 2),
    (3, 6, 0, 2), (3, 6, 1, 0), (3, 6, 1, 1), (3, 6, 1, 2),
    (3, 7, 0, 0), (3, 7, 0, 2), (3, 7, 1, 0), (3, 7, 1, 1),
    (3, 7, 1, 2),
    (4, 5, 0, 1), (4, 5, 0, 2), (4, 5, 2, 0), (4, 5, 2, 1),
    (4, 5, 2, 2),
    (4, 6, 0, 0), (4, 6, 0, 2), (4, 6, 2, 0), (4, 6, 2, 1),
    (4, 6, 2, 2),
    (4, 7, 0, 2), (4, 7, 2, 0), (4, 7, 2, 2),
    (5, 6, 0, 0), (5, 6, 0, 2), (5, 6, 1, 0), (5, 6, 1, 1),
    (5, 6, 1, 2), (5, 6, 2, 1), (5, 6, 2, 2),
    (5, 7, 0, 2), (5, 7, 1, 0), (5, 7, 2, 0), (5, 7, 2, 2),
    (6, 7, 0, 0), (6, 7, 0, 2), (6, 7, 1, 2), (6, 7, 2, 0),
    (6, 7, 2, 2),
})


def polynomial_key(poly):
    return tuple(sorted((monomial, str(coefficient))
                        for monomial, coefficient in poly.items()))


def build_blocks(admissible):
    require(len(SUPPORT) == 109 and MANDATORY <= SUPPORT <= admissible,
            "the frozen six-mandatory frontier support changed")
    blocks = D.sym_zero_blocks(V.SITES)
    for cell in sorted(SUPPORT):
        D.sym_put(blocks, *cell,
                  D.p_var("x_%d%d_%d%d" % cell))
    return blocks


def coefficient_audit(admissible):
    blocks = build_blocks(admissible)
    shadow = C.support_shadow_audit(SUPPORT)
    records = C.coefficient_generators(SUPPORT)
    histogram = Counter(len(record["terms"]) for record in records)
    family_histogram = Counter()
    plus_binomials = 0
    all_binomials = 0
    for record in records:
        for family in record["families"]:
            family_histogram[family] += 1
        if len(record["terms"]) == 2:
            all_binomials += 1
            plus_binomials += {
                Fraction(coefficient) for _monomial, coefficient
                in record["terms"]
            } == {Fraction(1)}
    require(len(records) == 1889 and all_binomials == 376
            and plus_binomials == 375
            and not any(len(record["terms"]) == 1 for record in records),
            "the frozen frontier generator census changed")
    return blocks, records, {
        "fibres_checked": shadow["fibres_checked"],
        "live_matching_histogram": shadow["live_matching_histogram"],
        "generators": len(records),
        "term_count_histogram": {
            str(key): value for key, value in sorted(histogram.items())
        },
        "family_histogram": dict(sorted(family_histogram.items())),
        "all_binomials": all_binomials,
        "plus_binomials": plus_binomials,
        "generator_sha256": D.content_hash(records),
    }


def projection_rank_range(first, second):
    first, second = frozenset(first), frozenset(second)
    if not first and not second:
        return [0], "whole_K"
    if not first:
        return [1], "row0_kernel"
    if not second:
        return [1], "row1_kernel"
    if first != second:
        return [2], "injective_by_distinct_zero_patterns"
    if len(first) == 1:
        return [1], "coincident_single_coordinate"
    return [1, 2], "coincident_support_rank_undecided"


def tripod_projection_audit():
    result = {}
    for center in V.RESIDUE:
        projections = []
        forced_kernel_lines = []
        for neighbour in V.RESIDUE:
            if neighbour == center:
                continue
            rows = []
            for source_colour in (0, 1):
                rows.append(tuple(target_colour
                                  for target_colour in V.COLORS
                                  if V.cell(center, neighbour, source_colour,
                                            target_colour) in SUPPORT))
            ranks, incidence = projection_rank_range(*rows)
            if incidence in ("row0_kernel", "row1_kernel"):
                forced_kernel_lines.append(incidence)
            projections.append({
                "neighbour": neighbour,
                "row_supports": [list(row) for row in rows],
                "rank_range": ranks,
                "kernel_incidence": incidence,
            })
        result[str(center)] = {
            "projections": projections,
            "forced_coordinate_kernel_lines": forced_kernel_lines,
            "incidence_type": (
                "none_forced" if not forced_kernel_lines else
                "all_same" if len(set(forced_kernel_lines)) == 1 else
                "two_coordinate_points"
            ),
        }
    return result


def product(*polys):
    out = D.p_const(1)
    for poly in polys:
        out = D.p_mul(out, poly)
    return out


def pure_lift_pairing_audit(blocks):
    residue_word = {site: 2 for site in V.RESIDUE}
    residue = D.sym_matching_sum(blocks, V.RESIDUE, residue_word)
    pairings = (
        ((0, 1), (2, 3)),
        ((0, 2), (1, 3)),
        ((0, 3), (1, 2)),
    )
    result = []
    for first, second in pairings:
        exact_words = []
        localized_factors = 0
        for boundary_colours in itertools.product(V.COLORS, repeat=4):
            if boundary_colours == (2, 2, 2, 2):
                continue
            word = dict(enumerate(boundary_colours))
            word.update(residue_word)
            factor = product(
                D.sym_cell(blocks, first[0], first[1],
                           word[first[0]], word[first[1]]),
                D.sym_cell(blocks, second[0], second[1],
                           word[second[0]], word[second[1]]),
            )
            localized_factors += bool(factor)
            full = D.sym_matching_sum(blocks, V.SITES, word)
            if factor and full == product(factor, residue):
                exact_words.append(list(boundary_colours))
        result.append({
            "pairing": [list(first), list(second)],
            "localized_factor_words": localized_factors,
            "exact_mixed_lifts": exact_words,
        })
    return result


def audit():
    started = monotonic()
    _state, _extras, _base, admissible, _stats = C.candidate_input()
    blocks, records, coefficient = coefficient_audit(admissible)
    pairings = pure_lift_pairing_audit(blocks)
    projections = tripod_projection_audit()
    tripod_ledger, tripod_digest = T.audit()
    injective_centers = [
        int(center) for center, record in projections.items()
        if all(projection["rank_range"] == [2]
               for projection in record["projections"])
    ]
    require(injective_centers == [5, 6]
            and tripod_ledger["characteristic_scope"] == "every field",
            "the checked tripod closure left the first frontier")
    ledger = {
        "pinned_candidate_sha256": PINNED_CANDIDATE_SHA256,
        "pinned_pure_lift_sha256": PINNED_PURE_LIFT_SHA256,
        "pinned_tripod_sha256": PINNED_TRIPOD_SHA256,
        "tripod_ledger_sha256": tripod_digest,
        "mandatory_cells": [list(cell) for cell in sorted(MANDATORY)],
        "support_cells": [list(cell) for cell in sorted(SUPPORT)],
        "support_size": len(SUPPORT),
        "residue_support_size": sum(cell[0] in V.RESIDUE
                                    and cell[1] in V.RESIDUE
                                    for cell in SUPPORT),
        "coefficient_frontier": coefficient,
        "tripod_projection_support_ranks": projections,
        "injective_tripod_centers": injective_centers,
        "pure_lift_pairing_census": pairings,
        "scope": (
            "This freezes the smallest first semantic support found by an "
            "exploratory six-mandatory CEGAR. Its complete support shadow and "
            "all coefficient generators are independently reconstructed. "
            "The exploratory CEGAR clauses are not trusted. The independently "
            "checked injective two-kernel tripod theorem applies at residue "
            "vertices 5 and 6 and closes the coefficient ideal."
        ),
        "status": (
            "exact semantic support frontier, empty over every field by the "
            "injective two-kernel tripod obstruction"
        ),
    }
    digest = D.content_hash(ledger)
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                "the six-mandatory first-frontier ledger changed")
    return ledger, digest, monotonic() - started


def main():
    ledger, digest, seconds = audit()
    print("n8 D1 six-mandatory first frontier: PASS (exact input)")
    print("support/generators:", ledger["support_size"], "/",
          ledger["coefficient_frontier"]["generators"])
    print("residue cells:", ledger["residue_support_size"])
    print("pure-lift counts:",
          [len(row["exact_mixed_lifts"])
           for row in ledger["pure_lift_pairing_census"]])
    print("ledger sha256:", digest)
    print("total: %.1f s" % seconds)


if __name__ == "__main__":
    main()
