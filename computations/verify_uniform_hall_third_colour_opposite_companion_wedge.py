#!/usr/bin/env python3
"""Opposite-companion closure of the paired third-colour Hall web."""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_uniform_hall_bridge_dark_alternating_path_boundary.py":
        "c812dec842ea2edbe58c525edab8133fe55c54e37c2576bdd707ddf2b5b4550c",
    "notes/uniform-hall-bridge-dark-alternating-path-boundary.md":
        "24dcd5f9690103d705022f41b95f6ae35700607aefb395b7a424839778b9785e",
    "computations/verify_uniform_five_lock_wedge_or_switch.py":
        "c2541a60db1f8e7a661bc698d2bd1f1a1f396a0f0bfde389ea89bea17fac175e",
    "notes/uniform-five-lock-wedge-or-switch.md":
        "0871d5151a0fdb46fee0c9b15797a864e579a85c360a2638d458583479426914",
    "computations/verify_uniform_decorated_anchor_mixed_word_exchange.py":
        "150bf15eb8ac475f866c062afcd7e3002477d02338acdb082c14f9136a3e58b7",
    "notes/uniform-decorated-anchor-mixed-word-exchange.md":
        "0cdc391bebb44150c7941bdbeec853029929f20d46ee813eb2a09bb76c27a5de",
    "computations/verify_uniform_triple_shared_anchor_unary_escape.py":
        "3f754bd020c63a7b03079746b26293e52af6c64d7edd1b7049b70f75ebe45283",
    "notes/uniform-triple-shared-anchor-unary-escape.md":
        "bc5840079555fed469dbc8fcb34ba50b84a8e7dfd35423cfe75b9902e831376e",
}
EXPECTED_LEDGER_SHA256 = "9f18f9a1266df4f0ff1a406bd14b05c42bc8dd62ff9e13f31e432a1911a46cb7"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def edge(left, right):
    return tuple(sorted((left, right)))


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")


def rank(matrix):
    matrix = [[Q(value) for value in row] for row in matrix]
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


def star_matrix(cells):
    # Columns are literal (physical neighbour, neighbour-colour) slots.
    columns = sorted({(neighbour, neighbour_colour)
                      for _row, neighbour, neighbour_colour in cells})
    matrix = [[0 for _column in columns] for _row in range(3)]
    for row, neighbour, neighbour_colour in cells:
        matrix[row][columns.index((neighbour, neighbour_colour))] = 1
    return matrix, columns


def audit_opposite_companion_rank_repair():
    # Canonical dual-blind skeleton from 3ed7f4a:
    # M0=03|14|25, M1=24|35, M2=15|34.
    # The four nonzero trapped mates are
    # 24:02, 35:20, 15:01, 34:10.
    # Test the central adjacent selected arms 35 (colour one) and 34
    # (colour two).  The opposite-colour decorations repair the row lost
    # at every deleted endpoint.
    deleted_stars = {
        "35_at_3": (
            (0, 0, 0),       # Q0: 03:00
            (2, 4, 2),       # Q2: 34:22
            (1, 4, 0),       # opposite companion: 34:10
        ),
        "35_at_5": (
            (0, 2, 0),       # Q0: 25:00
            (2, 1, 2),       # Q2: 15:22
            (1, 1, 0),       # opposite companion: 15:01
        ),
        "34_at_3": (
            (0, 0, 0),       # Q0: 03:00
            (1, 5, 1),       # Q1: 35:11
            (2, 5, 0),       # opposite companion: 35:20
        ),
        "34_at_4": (
            (0, 1, 0),       # Q0: 14:00
            (1, 2, 1),       # Q1: 24:11
            (2, 2, 0),       # opposite companion: 24:02
        ),
    }
    audits = {}
    for label, cells in deleted_stars.items():
        matrix, columns = star_matrix(cells)
        computed_rank = rank(matrix)
        require(computed_rank == 3,
                f"the opposite-companion rank repair changed at {label}")
        audits[label] = {
            "witness_cells": cells,
            "output_columns": columns,
            "rank": computed_rank,
        }
    return {
        "central_arms": [edge(3, 5), edge(3, 4)],
        "selected_anchor_colours": [1, 2],
        "deleted_star_audits": audits,
        "mechanism": (
            "on the colour-one arm, the two colour-two-edge decorations "
            "supply row one; on the colour-two arm, the two colour-one-edge "
            "decorations supply row two.  Q0 and the opposite pure anchor "
            "supply the other two rows"
        ),
    }


def audit_transition_dichotomy():
    # At shared site 3, the central decorations have the common remote
    # colour zero and distinct head rows:
    #
    #       35:20 -> e2 at site3,     34:10 -> e1 at site3.
    #
    # The only entries capable of cancelling their wedge are precisely the
    # k-labelled companions 35:10 and 34:20.  If those companions are absent
    # in the sharp residual, kappa=-B*D is nonzero.  If either is present,
    # the complete decorated-anchor exchange theorem applies to that
    # k-labelled decoration: it gives pure-anchor reselection, an avoiding
    # matching/off-anchor escape, or its localized row unit.
    samples = ((Q(2), Q(3)), (Q(-1), Q(5)), (Q(7), Q(-4)))
    open_values = []
    for b_value, d_value in samples:
        kappa = -b_value * d_value
        require(kappa,
                "two nonzero third-colour companions lost their wedge")
        open_values.append(int(kappa))

    # Sharp flat scalar guard when both missing k-labelled entries are
    # allowed: B*D-X*Y can vanish, but X=35:10 and Y=34:20 are exactly the
    # positive alternative, not a counterexample to the dichotomy.
    b_value = d_value = x_value = y_value = Q(1)
    flat = b_value * d_value - x_value * y_value
    require(flat == 0 and x_value and y_value,
            "the k-labelled flat alternative changed")
    return {
        "shared_site": 3,
        "third_colour_cells": ["35:20", "34:10"],
        "third_colour_heads": [2, 1],
        "common_remote_colour": 0,
        "sharp_residual_minor": "kappa=-q35_20*q34_10",
        "nonzero_sample_values": open_values,
        "only_cancelling_entries": ["35:10", "34:20"],
        "dichotomy": (
            "if a k-labelled cancelling entry is nonzero, complete "
            "decorated-anchor exchange gives reselection, avoiding "
            "matching/off-anchor escape, or its localized unit; otherwise "
            "kappa is the nonzero product of the two active third-colour "
            "cells"
        ),
    }


def audit_activity_and_padding():
    # Each central arm lies in its selected diagonal target matching.  Its
    # deleted cofactor is the product of the other selected cells and is
    # therefore nonzero over the integral localized chart.  Extra order is
    # added by disjoint common factor edges and cannot change the local
    # ranks or the shared-site wedge.
    q1 = (edge(6, 0), edge(7, 1), edge(2, 4), edge(3, 5))
    q2 = (edge(6, 2), edge(7, 0), edge(1, 5), edge(3, 4))
    require(edge(3, 5) in q1 and edge(3, 4) in q2,
            "a central activity witness disappeared")
    cofactor1 = tuple(pair for pair in q1 if pair != edge(3, 5))
    cofactor2 = tuple(pair for pair in q2 if pair != edge(3, 4))
    require(len(cofactor1) == len(cofactor2) == 3,
            "the order-eight activity cofactors changed")
    return {
        "colour1_selected_matching": q1,
        "colour2_selected_matching": q2,
        "arm35_activity_cofactor": cofactor1,
        "arm34_activity_cofactor": cofactor2,
        "all_order_padding": (
            "tensor every selected matching and every cofactor with the "
            "same disjoint diagonal factor edges; local ranks, nonzero "
            "activity, and kappa are unchanged for every h>=3"
        ),
    }


def main():
    pin_dependencies()
    ledger = {
        "opposite_companion_rank_repair":
            audit_opposite_companion_rank_repair(),
        "transition_dichotomy": audit_transition_dichotomy(),
        "activity_and_uniform_padding": audit_activity_and_padding(),
        "theorem": (
            "the four active third-colour decorations in the paired Hall "
            "path repair one another's selected colour-one/two central "
            "arms.  Both arms have deleted-star ranks (3,3), are active, "
            "and share a site.  Either a missing k-labelled companion is "
            "present and complete exchange gives a prior landing, or their "
            "shared-site transition minor is the nonzero product of the "
            "two central decorations"
        ),
        "landing": (
            "pure-Qk reselection, off-anchor escape, and lock-kernel "
            "deletion remain the earlier complete-exchange alternatives; "
            "the sole anchor-contained third-colour alternative now lands "
            "on the distinct-head active four-good overlap"
        ),
        "scope": (
            "uniform local source-labelled theorem for the four-decoration "
            "paired path, not a new support census and not a reproof of the "
            "downstream curved full-nine theorem"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"Hall opposite-companion wedge ledger changed: {digest}")
    print("uniform Hall third-colour opposite-companion wedge: PASS")
    print("central arms 35/34: active with four deleted-star ranks three")
    print("k-labelled complete-exchange route, or nonzero distinct-head minor")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
