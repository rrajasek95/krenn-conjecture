#!/usr/bin/env python3
"""Freeze the first physical injective/no-crossed-wedge lock packet.

On six residual sites a seven-cell colour-diagonal common quadratic carries
both diagonal response targets and both crossed zero responses exactly.  An
anchor-safe deletion of 15:11 has one and only one finite-difference lock:
the 12 response word 111211.  The 21 lock is identically zero, so common-q
matching provenance plus all four response rows does not force the
complementary crossed wedge of 016886b.

The same packet has q^[3]=0.  A pinned source-ideal theorem excludes every
colour-diagonal unary attachment with these concentrated spokes.  Hence a
full source extending the packet must use an off-diagonal internal cell;
the nonanchor theorem routes every such cell outside the selected anchor
union, leaving the decorated-anchor-edge case as the exact boundary.
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
    CYCLE_PATH:
        "f99c185403bf2e86b7352c555cd02d85bfed0df668b8a87b44a725c3db7edc71",
    "notes/uniform-diagonal-alternating-cycle-switch-boundary.md":
        "1e5b1a530d782ff03805b293ccfc3e6d76db6f046c8d8ffd4224ed3f9725f9e8",
    "computations/verify_uniform_five_lock_wedge_or_switch.py":
        "c2541a60db1f8e7a661bc698d2bd1f1a1f396a0f0bfde389ea89bea17fac175e",
    "notes/uniform-five-lock-wedge-or-switch.md":
        "0871d5151a0fdb46fee0c9b15797a864e579a85c360a2638d458583479426914",
    "computations/verify_n8_lemma_e_unary_top_diagonal_aggregate_identity.py":
        "d805a2d78ddf83239b2edca0598b8a88f90517296b375613030eb24defb1b2c2",
    "notes/n8-lemma-e-unary-top-diagonal-aggregate-identity.md":
        "d959fd085e6585d46000ace7a173d898e0a5f0306f03f2f476ad1890a0e24aa0",
    "computations/verify_uniform_one_bad_nonanchor_offdiagonal_good_pair.py":
        "64e85cd84112b5160efe4f43ce1208da3c49f5e58b3e4a4d6192e6a9c229c306",
    "notes/uniform-one-bad-nonanchor-offdiagonal-good-pair.md":
        "4516c5ff02f130e1ad25b4fde395c81557e58ba0c83f7f98969d95df17fd6409",
}
EXPECTED_LEDGER_SHA256 = (
    "b4888f92f99cc964e9603c7edf49a5351c3a15b5e580f7a39e79620ac7c5c6d9"
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")


def load_cycle():
    path = ROOT / CYCLE_PATH
    spec = spec_from_file_location("diagonal_cycle", path)
    require(spec is not None and spec.loader is not None,
            f"cannot load {CYCLE_PATH}")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def packet(cycle):
    return {
        cycle.cell(2, 4, 1, 1): Q(1),
        cycle.cell(3, 5, 1, 1): Q(1),
        cycle.cell(0, 5, 2, 2): Q(1),
        cycle.cell(1, 4, 2, 2): Q(1),
        cycle.cell(1, 5, 1, 1): Q(1),
        cycle.cell(1, 2, 1, 1): Q(1),
        cycle.cell(4, 5, 1, 1): Q(-1),
    }


def audit_physical_packet(cycle):
    sites = tuple(range(6))
    q = packet(cycle)
    p1 = ((0, 1, Q(1)),)
    s1 = ((1, 1, Q(1)),)
    p2 = ((2, 2, Q(1)),)
    s2 = ((3, 2, Q(1)),)
    stars = {"11": (p1, s1), "12": (p1, s2),
             "21": (p2, s1), "22": (p2, s2)}

    top = cycle.matchings(q, sites)
    require(top == Counter(), "the boundary unary top stopped being zero")
    responses = {
        label: cycle.response(q, p, s, sites)
        for label, (p, s) in stars.items()
    }
    x1 = (1,) * 6
    x2 = (2,) * 6
    require(responses == {
        "11": Counter({x1: Q(1)}),
        "12": Counter(),
        "21": Counter(),
        "22": Counter({x2: Q(1)}),
    }, f"the exact four-response packet changed: {responses}")

    # The 12 zero is one literal alternating C4:
    #   P1@0 | S2@3 | 15 | 24    (+1)
    #   P1@0 | S2@3 | 12 | 45    (-1).
    lock_word = (1, 1, 1, 2, 1, 1)
    direction = {cycle.cell(1, 5, 1, 1): Q(-1)}
    locks = {
        label: cycle.response_with_inserted_edge(
            q, p, s, direction, sites
        ) for label, (p, s) in stars.items()
    }
    unary_lock = cycle.inserted_edge_tensor(q, direction, sites)
    require(unary_lock == Counter(), "the switch acquired a unary lock")
    require(locks == {
        "11": Counter(),
        "12": Counter({lock_word: Q(-1)}),
        "21": Counter(),
        "22": Counter(),
    }, f"the one-sided crossed lock changed: {locks}")

    q_new = dict(q)
    del q_new[cycle.cell(1, 5, 1, 1)]
    require(cycle.subtract(cycle.matchings(q_new, sites), top) == unary_lock,
            "the unary finite difference stopped being exact")
    for label, (p, s) in stars.items():
        actual = cycle.subtract(
            cycle.response(q_new, p, s, sites), responses[label]
        )
        require(actual == locks[label],
                f"the {label} finite difference stopped being exact")

    old_anchors = cycle.mutual_anchors(q)
    new_anchors = cycle.mutual_anchors(q_new)
    deleted = cycle.cell(1, 5, 1, 1)
    require(deleted not in old_anchors,
            "the switch cell unexpectedly became a mutual anchor")
    require(old_anchors <= new_anchors,
            "the one-sided lock deletion destroyed an old mutual anchor")

    # On the nonzero coefficient torus the only response cancellation
    # character is (q15*q24)/(q12*q45)=-1.  This is the C4 character, so
    # the displayed point represents the whole nonzero weighted orbit.
    cancellation_character = (
        q[cycle.cell(1, 5, 1, 1)] * q[cycle.cell(2, 4, 1, 1)]
        / (q[cycle.cell(1, 2, 1, 1)]
           * q[cycle.cell(4, 5, 1, 1)])
    )
    require(cancellation_character == Q(-1),
            "the crossed C4 torus character changed")

    return {
        "sites": len(sites),
        "internal_cells": len(q),
        "all_internal_cells_diagonal": all(
            edge[2] == edge[3] for edge in q
        ),
        "unary_top": 0,
        "response_tensors": {"11": "X1", "12": 0,
                             "21": 0, "22": "X2"},
        "crossed_12_terms": [
            "+ P1@0 S2@3 15:11 24:11",
            "- P1@0 S2@3 12:11 45:11",
        ],
        "switch": "delete 15:11",
        "support_drop": 1,
        "old_mutual_anchors_preserved": True,
        "five_lock_support": {"unary": 0, "11": 0,
                              "12": ["111211:-1"],
                              "21": 0, "22": 0},
        "lock_map_rank": 1,
        "lock_map_kernel_dimension": 0,
        "complementary_crossed_wedge": False,
        "c4_torus_character": str(cancellation_character),
    }


def main():
    pin_dependencies()
    cycle = load_cycle()
    ledger = {
        "physical_common_provenance_guard": audit_physical_packet(cycle),
        "diagonal_attachment_theorem": (
            "the pinned aggregate identity excludes q^[3]=X0 with these "
            "concentrated spokes for every colour-diagonal internal q, "
            "including arbitrary cancellation and extra diagonal cells"
        ),
        "offdiagonal_routing": (
            "therefore a full packet extending the guard needs an "
            "off-diagonal internal cell; if its physical edge lies outside "
            "the three selected anchor matchings, the pinned reselection "
            "theorem gives a rank-(3,3) good active-minor pair"
        ),
        "verdict": (
            "common q plus all four exact response rows do not force "
            "opposite crossed-lock mating: an injective one-sided L12 lock "
            "is physical.  Unary exactness kills its whole diagonal chart, "
            "so the first unresolved escape is an off-diagonal decoration "
            "on the selected anchor union"
        ),
        "scope": (
            "the guard has unary top zero and is not a one-bad source or a "
            "Krenn counterexample; it proves the precise load-bearing role "
            "of the unary row and does not close decorated anchor edges"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256:
        require(digest == EXPECTED_LEDGER_SHA256,
                f"ledger digest changed: {digest}")
    print(payload)
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
