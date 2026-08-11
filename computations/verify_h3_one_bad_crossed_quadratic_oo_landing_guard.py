#!/usr/bin/env python3
"""Exact OO-landing audit for the crossed h=3 quadratic mate.

The crossed pair repairs the two displayed 2 by 2 response minors, and the
complete one-bad rows force both old direct arms to be active and nonflat.
It does not repair the selected a-row of the bad pq arm.  Consequently the
four deleted endpoint-star ranks are (2,2,3,3), not (3,3,3,3), and the
crossed pair cannot be fed directly to the curved doubly-good OO theorem.
"""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
import importlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_one_bad_common_q_cap_extraction_boundary.py":
        "02517a037d7dfc273d2eee63dd85e8228d88cd4824397b7ac478c013624afe5e",
    "computations/verify_h3_one_bad_second_principal_parts_companion_closure.py":
        "3612f9d7c03a3e265792543cd602f27ebf64830390f95b5bddb8d953d238c3f5",
    "computations/verify_h3_one_bad_companion_quadratic_mate_partition.py":
        "b8047fd1e610052fc47fcc0a5e11dd99d582f3ae638ad18825af46d036bc52cb",
    "computations/verify_shared_reciprocal_two_bad_anchor_safe_retraction.py":
        "a280b40657f2ab02c9c9f6ecf50dd3326db12bcc20614cbbd12bddffac8a1b62",
    "computations/verify_uniform_one_bad_clean_cap_dependency_audit.py":
        "4d7712c7514df9e852e502a30fab14a8a85969af1c57827774e62297c1aad397",
    "computations/verify_shared_reciprocal_flat_bicase_unit.py":
        "ea7ca9b3de2bc2e7d71d45cfba35fb62d77309819d9b6a910307b91061dd7a18",
    "computations/verify_oo_doubly_good_two_anchor_counterguard.py":
        "b9d986f4e1725082c1101e73729018a6d66296aef628879de50b03508f804699",
}
EXPECTED_LEDGER_SHA256 = (
    "5c68a7da95b6060d9b8bc15dca35cc592c86f23c321f65fa5804e62a0acb5d4e"
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, f"dependency changed: {relative}: {actual}")


def determinant2(matrix):
    return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]


def main():
    pin_dependencies()
    base = importlib.import_module(
        "verify_h3_one_bad_common_q_cap_extraction_boundary")
    closure = importlib.import_module(
        "verify_h3_one_bad_second_principal_parts_companion_closure")
    oo = importlib.import_module(
        "verify_oo_doubly_good_two_anchor_counterguard")

    # Endpoint colours are (a,c,t)=(0,1,2).  The exact one-bad nine-row
    # normal form has P_a=Q_a=0 on pq.  The crossed quadratic mate adds only
    # P_c and R_c, so it cannot change either zero a-row.
    p_selected = ((1, 0), (0, 1))  # P_t@1 and P_c@2
    r_selected = ((0, 1), (1, 0))  # R_a@2 and R_c@1
    selected_minors = (determinant2(p_selected), determinant2(r_selected))
    require(selected_minors == (1, -1),
            f"the crossed selected minors changed: {selected_minors}")

    # The two new physical edges are disjoint.  They are response-star
    # entries, not a new pair of rank-one arms sharing an endpoint.
    crossed_edges = (frozenset((1, 7)), frozenset((2, 5)))
    require(crossed_edges[0].isdisjoint(crossed_edges[1]),
            "the crossed response cells unexpectedly became shared arms")

    # Use t=-1: C=Q1=-1 and the two crossed cells have coefficient +1, so
    # the literal companion word C + (R_c@1)(P_c@2) is exactly cancelled.
    source = dict(closure.build_eight_site_source(base, Fraction(-1)))
    source[base.cell(1, 7, 1, 1)] = Fraction(1)  # R_c@1
    source[base.cell(2, 5, 0, 1)] = Fraction(1)  # P_c@2
    p, q, r = 5, 6, 7
    arms = ((p, q), (p, r))

    direct_ranks = tuple(
        oo.rational_rank(oo.direct_matrix(source, *arm)) for arm in arms
    )
    star_ranks = tuple(
        oo.star_rank(source, endpoint, deleted)
        for endpoint, deleted in ((p, q), (q, p), (p, r), (r, p))
    )
    require(direct_ranks == (1, 1),
            f"the two direct-arm ranks changed: {direct_ranks}")
    require(star_ranks == (2, 2, 3, 3),
            f"the crossed deleted-star ranks changed: {star_ranks}")

    # The exact rank defect is the selected a-row at each endpoint of pq.
    # It is zero away from the deleted neighbour.  This is the rank <=2
    # statement in the complete one-bad normal form, not a numerical
    # accident of the displayed coefficients.
    def endpoint_row(endpoint, deleted, colour):
        residual = tuple(v for v in range(8)
                         if v not in (endpoint, deleted))
        return tuple(
            oo.entry(source, endpoint, v, colour, other_colour)
            for v in residual for other_colour in range(3)
        )

    zero_rows = (
        endpoint_row(p, q, 0),
        endpoint_row(q, p, 0),
    )
    require(all(not any(row) for row in zero_rows),
            "the one-bad selected a-row was repaired")

    # Both direct arms are support-active.  In the exact row language this
    # is forced by R_a*q^[2]=X_a and Q_c*q^[2]=X_c.  Here we independently
    # enumerate their literal residual perfect matchings.
    cofactor_counts = tuple(
        len(oo.supported_cofactor_matchings(source, arm)) for arm in arms
    )
    require(all(count > 0 for count in cofactor_counts),
            f"a crossed direct arm became inactive: {cofactor_counts}")

    # Shared factors e_a,e_c are independent.  The uniform exact flat-bicase
    # theorem says flatness would force both outer restricted stars to zero.
    # Q_c and R_a are nonzero because their complete diagonal rows have
    # nonzero pure targets, so the crossed one-bad packet is on the nonflat
    # side.  Check the literal witnesses as a source-label calibration.
    q_outer = tuple(
        base.cell(u, q, colour, endpoint_colour)
        for u in range(5) for colour in range(3)
        for endpoint_colour in range(3)
        if source.get(base.cell(u, q, colour, endpoint_colour))
    )
    r_outer = tuple(
        base.cell(u, r, colour, endpoint_colour)
        for u in range(5) for colour in range(3)
        for endpoint_colour in range(3)
        if source.get(base.cell(u, r, colour, endpoint_colour))
    )
    require(q_outer and r_outer,
            "an outer restricted star vanished in the crossed packet")

    # Complete source-label audit.  This finite calibration expands all
    # 3^8 full-output rows.  It is deliberately not claimed to be a GHZ
    # source: it cancels the selected companion and has all three pure
    # anchors, but ten other mixed rows remain.  Those are exactly the
    # additional source obligations which any actual completion must meet.
    tensor, _supported = oo.matching_tensor(source)
    pure = {word: coefficient for word, coefficient in tensor.items()
            if len(set(word)) == 1}
    expected_pure = {(colour,) * 8: Fraction(1) for colour in range(3)}
    require(pure == expected_pure, f"the pure rows changed: {pure}")
    companion = tuple(map(int, "21000121"))
    require(not tensor.get(companion),
            "the crossed pair stopped cancelling the companion")
    mixed = tuple(sorted(
        ("".join(map(str, word)), str(coefficient))
        for word, coefficient in tensor.items() if len(set(word)) > 1
    ))
    require(len(mixed) == 10,
            f"the full-row residual count changed: {len(mixed)}")

    # The theorem-level implication is therefore one-sided: the complete
    # rows imply activity and exactness excludes flatness, but the one-bad
    # zero row forbids OO goodness on pq.  A valid curved landing must first
    # leave this normal form by a source-valid modification or reselect a
    # genuinely shared second pair whose four deleted stars are injective.
    ledger = {
        "dependencies": PINS,
        "crossed_pair": {
            "cells": ["R_c@1:1", "P_c@2:0"],
            "physical_edges": [[1, 7], [2, 5]],
            "edges_disjoint": True,
            "selected_endpoint_minors": list(selected_minors),
        },
        "oo_audit": {
            "direct_arms": [[p, q], [p, r]],
            "direct_ranks": list(direct_ranks),
            "deleted_endpoint_star_ranks": list(star_ranks),
            "bad_arm_zero_rows": ["P_a", "Q_a"],
            "cofactor_matching_counts": list(cofactor_counts),
            "activity": True,
            "transition": "nonflat_by_independent_shared_factors_and_nonzero_outer_stars",
            "curved_doubly_good_hypothesis": False,
        },
        "full_source_label_calibration": {
            "rows_checked": 3 ** 8,
            "pure_rows": 3,
            "companion_word": "21000121",
            "companion_residual": 0,
            "other_mixed_residuals": list(mixed),
        },
        "minimal_missing_hypothesis": (
            "a source-valid modification or reselection producing one shared "
            "pair with both missing a-rows restored, hence all four deleted "
            "endpoint-star ranks equal to three; the two crossed response "
            "cells are disjoint and cannot themselves be that shared pair"
        ),
        "verdict": (
            "the crossed mate makes the selected 2x2 minors unimodular and "
            "the complete one-bad rows give activity/nonflatness, but the "
            "original pq arm remains rank-two at both deleted endpoints, so "
            "the curved doubly-good OO theorem is not automatically available"
        ),
        "scope": (
            "universal rank obstruction inside the exact one-bad normal form, "
            "plus a complete 6561-row audit of the smallest literal crossed "
            "calibration; the calibration has ten mixed residuals and is not "
            "a GHZ source or counterexample"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"the crossed OO landing ledger changed: {digest}")

    print("h=3 crossed quadratic OO-landing guard: PASS")
    print(f"selected minors={selected_minors}; direct ranks={direct_ranks}")
    print(f"deleted-star ranks={star_ranks}; cofactor counts={cofactor_counts}")
    print("activity/nonflatness survive; curved doubly-good landing does not")
    print("full calibration: companion=0, pure rows=3, mixed residual rows=10")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
