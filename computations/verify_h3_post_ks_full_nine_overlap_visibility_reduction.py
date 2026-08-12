#!/usr/bin/env python3
"""Reduce post-KS double darkness to one-sided full-nine overlap tests.

On an eight-site cap the uniform full-nine incidence theorem forces at least
two internal sites whose aggregate q-star contains all three target axes.
Such a site remains aggregate rank three when it is promoted to an endpoint
of either overlapping cap.  Consequently a transported active carrier on an
overlap needs to repair only the *other* endpoint: one nonzero deficient-
quotient coordinate gives a rank-(3,3) active cap.

This does not construct the source-faithful overlap transport.  It isolates
its exact output and shows that restoring both deficient quotients on the
original post-KS cap is stronger than the global clean-pair proof requires.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_uniform_full_nine_target_incidence_invariant.py":
        "67eccb70f90dc1c89b6eb33cf06b6c38e61224258e4d131b709cb4c3979e9a59",
    "notes/uniform-full-nine-target-incidence-invariant.md":
        "25c73e8e8ecacdbb8156ed27a093d62e107e219fcd3451c3a45ab381649f679e",
    "computations/verify_h3_post_ks_same_head_rank_support_counterguard.py":
        "21ebd9d48fed3bc91af820bc84b37bd5133971e519d60fb1d0727de4a4acec3e",
    "notes/h3-post-ks-same-head-rank-support-counterguard.md":
        "4aa713664175bd2f5c91eeaebf07bd7c58b357dfe9a6d276c31ddb77c6eb57c6",
    "computations/verify_h3_residual_q_ks_constructive_landing_boundary.py":
        "bc11c8fe61ec8c21a1850326de037a328ab7f7404bcf3902655f6541e496bc9f",
    "notes/h3-residual-q-ks-constructive-landing-boundary.md":
        "225f79e54f121c375771510b4a9a07c3b666e0ffc36b4b9ebfd589c9c475756b",
}
EXPECTED_LEDGER_SHA256 = "efcf8f7ee13b735f1db707abdd6c6089d9e1fb2b6f78b46a432ef538f639c157"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")


def rank(columns):
    if not columns:
        return 0
    height = len(columns[0])
    matrix = [[Q(columns[column][row]) for column in range(len(columns))]
              for row in range(height)]
    pivot_row = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(pivot_row, height)
                      if matrix[row][column]), None)
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        value = matrix[pivot_row][column]
        matrix[pivot_row] = [entry / value for entry in matrix[pivot_row]]
        for row in range(height):
            if row == pivot_row or not matrix[row][column]:
                continue
            value = matrix[row][column]
            matrix[row] = [left - value * right for left, right in
                           zip(matrix[row], matrix[pivot_row], strict=True)]
        pivot_row += 1
    return pivot_row


def audit_eight_site_incidence():
    """Enumerate the exact set-theoretic consequences at boundary size 8."""
    sites = frozenset(range(8))
    # |D_i|>=6, so enumerate their complements of size at most two.
    complements = [frozenset(choice)
                   for size in range(3)
                   for choice in combinations(sites, size)]
    survivors = 0
    minimum_full = 8
    full_histogram = {}
    for missing0 in complements:
        for missing1 in complements:
            for missing2 in complements:
                # D0 union D1 union D2=U iff no site is missed by all three.
                if missing0 & missing1 & missing2:
                    continue
                survivors += 1
                full = sites - (missing0 | missing1 | missing2)
                minimum_full = min(minimum_full, len(full))
                full_histogram[len(full)] = full_histogram.get(len(full), 0) + 1
                n1 = sum(sum(site not in missing for missing in
                             (missing0, missing1, missing2)) == 1
                         for site in sites)
                require(len(full) >= n1 + 2,
                        "the h=3 full-nine incidence inequality changed")
    require(survivors == 46585 and minimum_full == 2,
            "the exact eight-site incidence ledger changed")
    return {
        "boundary_sites": 8,
        "incidence_patterns": survivors,
        "minimum_target_full_sites": minimum_full,
        "target_full_site_histogram": sorted(full_histogram.items()),
        "uniform_reason": (
            "each |D_i|>=6, the three D_i cover U, and "
            "n_3>=n_1+2"
        ),
    }


def audit_overlap_rank_reduction():
    """A target-full intermediate changes a two-sided test to one-sided."""
    e0 = (Q(1), Q(0), Q(0))
    e1 = (Q(0), Q(1), Q(0))
    e2 = (Q(0), Q(0), Q(1))

    # In an overlap cap (P,u), target-fullness of u in the original cap
    # supplies an injective aggregate u-star.  The P-star may still be rank 2.
    outer_deficient = (e0, e1)
    full_intermediate = (e0, e1, e2)
    dark = e0
    visible = e2

    before = (rank(outer_deficient), rank(full_intermediate))
    after_dark = (rank(outer_deficient + (dark,)),
                  rank(full_intermediate + (dark,)))
    after_visible = (rank(outer_deficient + (visible,)),
                     rank(full_intermediate + (visible,)))
    require(before == (2, 3)
            and after_dark == (2, 3)
            and after_visible == (3, 3),
            "the one-sided overlap quotient test changed")

    # Two target-full sites give two independent opportunities.  No claim is
    # made that their transported columns are automatically visible.
    opportunity_profiles = {
        "both_dark": [after_dark, after_dark],
        "first_visible": [after_visible, after_dark],
        "second_visible": [after_dark, after_visible],
    }
    require(all(any(profile == (3, 3) for profile in profiles)
                for name, profiles in opportunity_profiles.items()
                if name != "both_dark"),
            "a visible overlap stopped producing a good cap")
    return {
        "original_post_KS_bad_profile": [2, 2, 3, 3],
        "overlap_profile_before_transport": list(before),
        "dark_transport_profile": list(after_dark),
        "visible_transport_profile": list(after_visible),
        "minimum_overlap_opportunities": 2,
        "one_sided_criterion": (
            "for an overlapping cap (P,u) with u target-full, an active "
            "transport is rank-(3,3) iff its P-star image is nonzero in "
            "the one-dimensional deficient quotient"
        ),
        "global_consequence": (
            "the clean-pair proof may descend on the overlapping cap; it "
            "need not restore both deficient quotients of the original cap"
        ),
    }


def main():
    pin_dependencies()
    ledger = {
        "pins": PINS,
        "eight_site_full_nine_incidence": audit_eight_site_incidence(),
        "overlap_rank_reduction": audit_overlap_rank_reduction(),
        "conditional_transport_theorem": (
            "if the source-faithful full-nine overlap carries the selected "
            "active/common-q class from a bad cap (P,S) to (P,u) or (S,u) "
            "for one target-full internal site u, and the transported outer "
            "endpoint column is nonzero in its deficient quotient, then the "
            "overlap cap is active and rank-(3,3) at both endpoints"
        ),
        "exact_remaining_branch": (
            "for at least two target-full internal sites, every legitimate "
            "overlap transport is absent, source-dependent, or quotient-"
            "dark at the non-full endpoint.  This is the one-sided endpoint-"
            "dark/maximal-shore overlap gate, not the former requirement of "
            "one arm simultaneously repairing two quotients"
        ),
        "separate_support_branch": (
            "a complete same-row dependence touching the carrier still gives "
            "the exact anchor-safe support deletion pinned upstream"
        ),
        "scope": (
            "exact incidence and linear-rank reduction.  Aggregate target-"
            "fullness does not construct a blockwise active overlap column, "
            "and no source-faithful transport is asserted"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"post-KS overlap visibility ledger changed: {digest}")
    print("h3 post-KS full-nine overlap visibility reduction: PASS")
    print("eight-site cap: at least two target-full internal sites")
    print("overlap through a full site: rank restoration is one-sided")
    print("remaining input: source-faithful visible overlap or endpoint-dark shore")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
