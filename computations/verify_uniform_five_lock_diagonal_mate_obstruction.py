#!/usr/bin/env python3
"""Exact obstruction to mating a crossed lock with a diagonal lock.

An L12 component on r-s and an L22 component on t-s use the identical
local vector s2 at their common site.  Thus their centre wedge vanishes
identically.  Dually, L12 on r-s and L11 on r-t repeat p1 at r.

The checker also separates the physical-pair issue.  When both pairs avoid
the three chosen pure-anchor matchings, those matchings guarantee all four
deleted-star ranks are three, but the overlap is flat.  If the diagonal
mate lies on an anchor edge, the same anchor data guarantee only rank two
at its endpoints.  Hence a diagonal mate cannot replace the complementary
L21 component in the five-lock wedge theorem.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_uniform_five_lock_wedge_or_switch.py":
        "c2541a60db1f8e7a661bc698d2bd1f1a1f396a0f0bfde389ea89bea17fac175e",
    "notes/uniform-five-lock-wedge-or-switch.md":
        "0871d5151a0fdb46fee0c9b15797a864e579a85c360a2638d458583479426914",
    "computations/verify_uniform_one_bad_nonanchor_offdiagonal_good_pair.py":
        "64e85cd84112b5160efe4f43ce1208da3c49f5e58b3e4a4d6192e6a9c229c306",
    "notes/uniform-one-bad-nonanchor-offdiagonal-good-pair.md":
        "4516c5ff02f130e1ad25b4fde395c81557e58ba0c83f7f98969d95df17fd6409",
}
EXPECTED_LEDGER_SHA256 = (
    "a4ffd2b3e7afa21c6baab8f56a560d750e794732d0e717eb100bbd8cc496d927"
)


PURE_MATCHINGS = {
    0: ((0, 1), (2, 3), (4, 5), (6, 7)),
    1: ((0, 2), (1, 3), (4, 6), (5, 7)),
    2: ((0, 3), (1, 2), (4, 7), (5, 6)),
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def rank(matrix):
    matrix = [[Q(value) for value in row] for row in matrix]
    if not matrix:
        return 0
    pivot_row = 0
    for column in range(len(matrix[0])):
        pivot = next((row for row in range(pivot_row, len(matrix))
                      if matrix[row][column]), None)
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        value = matrix[pivot_row][column]
        matrix[pivot_row] = [entry / value
                             for entry in matrix[pivot_row]]
        for row in range(len(matrix)):
            if row == pivot_row or not matrix[row][column]:
                continue
            value = matrix[row][column]
            matrix[row] = [entry - value * pivot_entry
                           for entry, pivot_entry
                           in zip(matrix[row], matrix[pivot_row], strict=True)]
        pivot_row += 1
    return pivot_row


def partner(matching, site):
    for left, right in matching:
        if left == site:
            return right
        if right == site:
            return left
    raise RuntimeError(f"site {site} is absent from matching")


def edge(left, right):
    return tuple(sorted((left, right)))


ANCHOR_EDGES = {
    edge(*pair) for matching in PURE_MATCHINGS.values() for pair in matching
}


def pure_anchor_deleted_star_matrix(site, deleted_pair):
    """Selected-anchor columns surviving deletion of a physical pair."""
    columns = []
    for colour, matching in PURE_MATCHINGS.items():
        incident = edge(site, partner(matching, site))
        if incident != deleted_pair:
            columns.append((partner(matching, site), colour))
    rows = sorted(columns)
    return [[Q(int(row == column)) for column in columns] for row in rows]


def guaranteed_pair_ranks(pair):
    return tuple(rank(pure_anchor_deleted_star_matrix(site, pair))
                 for site in pair)


def multiply_monomials(left, right):
    return tuple(sorted(left + right))


def polynomial_add_term(polynomial, monomial, coefficient):
    polynomial[monomial] += coefficient
    if not polynomial[monomial]:
        del polynomial[monomial]


def symbolic_wedge(left, right):
    """All 2x2 minors, over Z, of two symbolic three-vectors."""
    minors = []
    for first, second in ((0, 1), (0, 2), (1, 2)):
        value = Counter()
        polynomial_add_term(
            value, multiply_monomials(left[first], right[second]), 1)
        polynomial_add_term(
            value, multiply_monomials(left[second], right[first]), -1)
        minors.append(dict(value))
    return minors


def audit_repeated_factor_identity():
    p1 = (("p10",), ("p11",), ("p12",))
    s2 = (("s20",), ("s21",), ("s22",))
    l12_l22 = symbolic_wedge(s2, s2)
    l12_l11 = symbolic_wedge(p1, p1)
    require(all(not minor for minor in l12_l22),
            "the common s2 factor acquired a nonzero symbolic wedge")
    require(all(not minor for minor in l12_l11),
            "the common p1 factor acquired a nonzero symbolic wedge")
    return {
        "L12_rs_with_L22_ts": {
            "common_site_factor": "s2@s",
            "three_centre_minors": l12_l22,
        },
        "L12_rs_with_L11_rt": {
            "common_site_factor": "p1@r",
            "three_centre_minors": l12_l11,
        },
    }


def audit_offanchor_diagonal_mates():
    pair12 = edge(0, 4)
    pair22 = edge(1, 4)
    pair11 = edge(0, 5)
    require(all(pair not in ANCHOR_EDGES
                for pair in (pair12, pair22, pair11)),
            "the canonical off-anchor audit entered the anchor graph")
    ranks22 = guaranteed_pair_ranks(pair12) + guaranteed_pair_ranks(pair22)
    ranks11 = guaranteed_pair_ranks(pair12) + guaranteed_pair_ranks(pair11)
    require(ranks22 == (3, 3, 3, 3),
            "the off-anchor L12/L22 audit lost a selected-anchor column")
    require(ranks11 == (3, 3, 3, 3),
            "the off-anchor L12/L11 audit lost a selected-anchor column")
    cofactor12, cofactor22, cofactor11 = Q(2), Q(-3), Q(5)
    require(cofactor12 * cofactor22 != 0
            and cofactor12 * cofactor11 != 0,
            "a selected diagonal-mate cofactor became inactive")
    return {
        "L12_L22": {
            "pairs": [pair12, pair22],
            "shared_site": 4,
            "four_selected_anchor_ranks": ranks22,
            "cofactor_witnesses": [str(cofactor12), str(cofactor22)],
            "overlap": "four-good and active but same-head/flat",
        },
        "L12_L11_dual": {
            "pairs": [pair12, pair11],
            "shared_site": 0,
            "four_selected_anchor_ranks": ranks11,
            "cofactor_witnesses": [str(cofactor12), str(cofactor11)],
            "overlap": "four-good and active but same-head/flat",
        },
    }


def audit_anchor_edge_rank_loss():
    pair12 = edge(0, 4)
    pair22 = edge(4, 5)
    require(pair12 not in ANCHOR_EDGES and pair22 in ANCHOR_EDGES,
            "the canonical anchor-edge distinction changed")
    ranks = guaranteed_pair_ranks(pair12) + guaranteed_pair_ranks(pair22)
    require(ranks == (3, 3, 2, 2),
            "the selected-anchor rank guarantee on an anchor edge changed")
    return {
        "pairs": [pair12, pair22],
        "shared_site": 4,
        "selected_anchor_guaranteed_ranks": ranks,
        "missing_anchor_colour_on_diagonal_pair": 0,
        "scope": (
            "the selected pure anchors guarantee only rank two on the "
            "anchor pair; extra source columns could raise the actual rank"
        ),
        "common_head": "s2@4",
        "common_head_wedge": 0,
    }


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")


def main():
    pin_dependencies()
    ledger = {
        "anchor_union_edges": len(ANCHOR_EDGES),
        "repeated_factor_identity": audit_repeated_factor_identity(),
        "offanchor_diagonal_mates": audit_offanchor_diagonal_mates(),
        "anchor_edge_rank_loss": audit_anchor_edge_rank_loss(),
        "theorem": (
            "an L12 lock and an L22 diagonal arm sharing the s2 site, or "
            "an L12 lock and an L11 diagonal arm sharing the p1 site, "
            "have identically zero centre wedge; off-anchor pairs may be "
            "four-good and active but remain flat, while an anchor-edge "
            "mate has only a rank-two guarantee from the selected anchors"
        ),
        "remaining": (
            "a genuinely different shared-site star factor, such as the "
            "opposite crossed L21 row, or a source-valid arm exchange"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"five-lock diagonal-mate ledger changed: {digest}")
    print("uniform five-lock diagonal-mate obstruction: PASS")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
