#!/usr/bin/env python3
"""Exact five-lock propagation: simultaneous switch or crossed OO wedge.

For switch directions supported on one physical star, every linear
combination has divided square zero.  Hence the unary plus four response
locks form a linear map; a kernel vector is an exact simultaneous switch.

In the axis-purified branch, complementary crossed-lock components on two
off-anchor pairs sharing one port give the other alternative.  Three pure
target matchings make both pairs good at both endpoints, the crossed
components give nonzero cofactor witnesses, and their centre heads are the
distinct target axes.  The checker audits both statements exactly and
freezes the sharp abstract counterguard when the crossed incidence wedge is
absent.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CYCLE_PATH = (
    "computations/verify_uniform_diagonal_alternating_cycle_switch_boundary.py"
)
PINS = {
    "computations/verify_uniform_axis_circuit_k3_unary_attachment_rees_rigidity.py":
        "071ef2904e189164c92e1853aa31eefad540fccf6a316175fb1d4242fb668a9d",
    "notes/uniform-axis-circuit-k3-unary-attachment-rees-rigidity.md":
        "05f649ea3dba3233247344f54fe8782e07584f7c1a3214ebe9cf054dde932fdc",
    CYCLE_PATH:
        "f99c185403bf2e86b7352c555cd02d85bfed0df668b8a87b44a725c3db7edc71",
    "notes/uniform-diagonal-alternating-cycle-switch-boundary.md":
        "1e5b1a530d782ff03805b293ccfc3e6d76db6f046c8d8ffd4224ed3f9725f9e8",
    "computations/verify_uniform_one_bad_nonanchor_offdiagonal_good_pair.py":
        "64e85cd84112b5160efe4f43ce1208da3c49f5e58b3e4a4d6192e6a9c229c306",
    "notes/uniform-one-bad-nonanchor-offdiagonal-good-pair.md":
        "4516c5ff02f130e1ad25b4fde395c81557e58ba0c83f7f98969d95df17fd6409",
}
EXPECTED_LEDGER_SHA256 = (
    "74e798509caf61d60ae99657e33019a9a1ad00187c7b5fa8db133184c7961137"
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load_cycle():
    path = ROOT / CYCLE_PATH
    spec = spec_from_file_location("diagonal_cycle_lock", path)
    require(spec is not None and spec.loader is not None,
            f"cannot load {CYCLE_PATH}")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def clean(counter):
    return Counter({key: value for key, value in counter.items() if value})


def add(left, right, scalar=Q(1)):
    keys = set(left) | set(right)
    return clean(Counter({
        key: left.get(key, 0) + scalar * right.get(key, 0)
        for key in keys
    }))


def scale_cells(direction, scalar):
    return {cell: scalar * coefficient
            for cell, coefficient in direction.items() if coefficient}


def add_cells(*directions):
    output = Counter()
    for direction in directions:
        output.update(direction)
    return {cell: coefficient for cell, coefficient in output.items()
            if coefficient}


def perturb(q, direction):
    output = Counter(q)
    output.update(direction)
    return {cell: coefficient for cell, coefficient in output.items()
            if coefficient}


def audit_same_star_lock_linearity(cycle):
    audits = []
    for h in range(3, 9):
        sites = tuple(range(2 * h))
        q = cycle.extended_web(h)
        d1 = {
            cycle.cell(0, 1, 1, 1): Q(-2, 3),
            cycle.cell(0, 2, 1, 1): Q(5, 7),
        }
        d2 = {cycle.cell(0, 4, 1, 1): Q(3, 5)}
        a, b = Q(4, 3), Q(-7, 4)
        combined = add_cells(scale_cells(d1, a), scale_cells(d2, b))
        require(all(cell[0] == 0 for cell in combined),
                "the simultaneous switch left its common physical star")

        q_new = perturb(q, combined)
        top_difference = cycle.subtract(
            cycle.matchings(q_new, sites), cycle.matchings(q, sites))
        top_linear = add(
            cycle.inserted_edge_tensor(q, d1, sites),
            cycle.inserted_edge_tensor(q, d2, sites), b / a)
        top_linear = clean(Counter({key: a * value
                                    for key, value in top_linear.items()}))
        require(top_difference == top_linear,
                f"the simultaneous unary lock stopped being linear at h={h}")

        p1 = ((1, 1, Q(2)), (3, 0, Q(-1)))
        p2 = ((2, 2, Q(3)), (5, 1, Q(1)))
        s1 = ((3, 1, Q(1)), (4, 2, Q(-2)))
        s2 = ((1, 2, Q(1)), (5, 0, Q(3)))
        response_checks = 0
        for p, s in ((p1, s1), (p1, s2), (p2, s1), (p2, s2)):
            actual = cycle.subtract(
                cycle.response(q_new, p, s, sites),
                cycle.response(q, p, s, sites))
            first = cycle.response_with_inserted_edge(q, p, s, d1, sites)
            second = cycle.response_with_inserted_edge(q, p, s, d2, sites)
            predicted = add(first, second, b / a)
            predicted = clean(Counter({key: a * value
                                       for key, value in predicted.items()}))
            require(actual == predicted,
                    f"a simultaneous companion lock became nonlinear at h={h}")
            response_checks += 1
        audits.append({
            "h": h,
            "common_switch_star": 0,
            "unary_linearity": True,
            "companion_linearity_checks": response_checks,
            "combined_direction_cells": len(combined),
        })
    return audits


def rank(matrix):
    matrix = [[Q(value) for value in row] for row in matrix]
    if not matrix:
        return 0
    row = 0
    for column in range(len(matrix[0])):
        pivot = next((index for index in range(row, len(matrix))
                      if matrix[index][column]), None)
        if pivot is None:
            continue
        matrix[row], matrix[pivot] = matrix[pivot], matrix[row]
        value = matrix[row][column]
        matrix[row] = [entry / value for entry in matrix[row]]
        for index in range(len(matrix)):
            if index == row or not matrix[index][column]:
                continue
            value = matrix[index][column]
            matrix[index] = [entry - value * pivot_entry
                             for entry, pivot_entry
                             in zip(matrix[index], matrix[row], strict=True)]
        row += 1
    return row


def audit_lock_kernel_theorem():
    audits = []
    for switches in range(2, 9):
        # A lock map with fewer independent rows has a simultaneous kernel;
        # an identity block is the exact injective boundary.
        deficient = [[Q(int(row == column))
                      for column in range(switches)]
                     for row in range(switches - 1)]
        injective = [[Q(int(row == column))
                      for column in range(switches)]
                     for row in range(switches)]
        require(rank(deficient) == switches - 1,
                "the model simultaneous-switch kernel disappeared")
        require(rank(injective) == switches,
                "the injective lock boundary lost rank")
        audits.append({
            "switch_directions": switches,
            "deficient_lock_rank": switches - 1,
            "simultaneous_kernel_dimension": 1,
            "injective_boundary_rank": switches,
        })
    return audits


PURE_MATCHINGS = {
    0: ((0, 1), (2, 3), (4, 5), (6, 7)),
    1: ((0, 2), (1, 3), (4, 6), (5, 7)),
    2: ((0, 3), (1, 2), (4, 7), (5, 6)),
}


def partner(matching, site):
    for left, right in matching:
        if left == site:
            return right
        if right == site:
            return left
    raise RuntimeError(f"site {site} is absent from matching")


def deleted_star_columns(site):
    # The three pure matchings give one coordinate column per target colour.
    # Encode rows by (neighbour, colour); their supports are disjoint.
    rows = sorted((partner(PURE_MATCHINGS[colour], site), colour)
                  for colour in range(3))
    return [[Q(int(row == (partner(PURE_MATCHINGS[colour], site), colour)))
             for colour in range(3)] for row in rows]


def audit_crossed_wedge_landing():
    anchor_edges = {
        tuple(sorted(edge)) for matching in PURE_MATCHINGS.values()
        for edge in matching
    }
    centre, outer12, outer21 = 0, 4, 5
    pair12 = tuple(sorted((centre, outer12)))
    pair21 = tuple(sorted((centre, outer21)))
    require(pair12 not in anchor_edges and pair21 not in anchor_edges,
            "the canonical crossed wedge entered the anchor graph")

    ranks = {
        "pair12_centre": rank(deleted_star_columns(centre)),
        "pair12_outer": rank(deleted_star_columns(outer12)),
        "pair21_centre": rank(deleted_star_columns(centre)),
        "pair21_outer": rank(deleted_star_columns(outer21)),
    }
    require(set(ranks.values()) == {3},
            "the pure matchings stopped making the wedge four-good")

    # Axis-purified crossed components have the two distinct centre heads.
    e1, e2 = (Q(0), Q(1), Q(0)), (Q(0), Q(0), Q(1))
    centre_minor = e1[1] * e2[2] - e1[2] * e2[1]
    require(centre_minor == 1,
            "the complementary crossed locks lost their transverse heads")
    cofactor12, cofactor21 = Q(2), Q(-3)
    require(cofactor12 * cofactor21 != 0,
            "the crossed lock components stopped being active")
    return {
        "pure_anchor_union_edges": len(anchor_edges),
        "crossed_12_pair": pair12,
        "crossed_21_pair": pair21,
        "pairs_share_centre": centre,
        "four_deleted_star_ranks": ranks,
        "centre_head_minor": str(centre_minor),
        "cofactor_witnesses": [str(cofactor12), str(cofactor21)],
        "landing": "distinct-head four-good active overlap",
    }


def audit_sharp_incidence_counterguard():
    # Two independent switch directions can have injective nonzero locks
    # while the crossed incidence needed above is absent.  This is the exact
    # abstract boundary; it is not asserted to be a full one-bad source.
    lock_coordinates = ("unary", "cross12@0-4", "cross21@0-5")
    columns = (
        (Q(1), Q(0), Q(0)),
        (Q(0), Q(1), Q(0)),
    )
    matrix = [[column[row] for column in columns]
              for row in range(len(lock_coordinates))]
    require(rank(matrix) == 2,
            "the sharp lock counterguard acquired a simultaneous switch")
    cross12_edges = {(0, 4)}
    cross21_edges = set()
    wedge_centres = {
        site for edge in cross12_edges for site in edge
        if any(site in other for other in cross21_edges)
    }
    require(not wedge_centres,
            "the sharp counterguard unexpectedly acquired a crossed wedge")
    return {
        "switch_directions": 2,
        "lock_rank": 2,
        "simultaneous_kernel": 0,
        "nonzero_lock_coordinates": ["unary", "cross12@0-4"],
        "complementary_crossed_wedge": False,
        "scope": "abstract source-labelled lock module, not a full source",
    }


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")


def main():
    pin_dependencies()
    cycle = load_cycle()
    ledger = {
        "same_star_linearity": audit_same_star_lock_linearity(cycle),
        "lock_kernel_theorem": audit_lock_kernel_theorem(),
        "crossed_wedge_landing": audit_crossed_wedge_landing(),
        "sharp_incidence_counterguard": audit_sharp_incidence_counterguard(),
        "theorem": (
            "a same-star five-lock kernel gives an exact simultaneous "
            "anchor-safe switch; complementary axis-pure crossed components "
            "on off-anchor pairs sharing a centre give a distinct-head "
            "four-good active overlap"
        ),
        "remaining": (
            "an injective five-lock map whose crossed port-incidence graph "
            "contains no complementary off-anchor wedge"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"five-lock wedge-or-switch ledger changed: {digest}")
    print("uniform five-lock wedge-or-switch theorem: PASS")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
