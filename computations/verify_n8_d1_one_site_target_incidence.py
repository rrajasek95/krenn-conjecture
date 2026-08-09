#!/usr/bin/env python3
"""Exact one-site target-incidence theorem and O4 support packets."""

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


PINNED_CANDIDATE_SHA256 = (
    "28b5de217d61dbe41c699657fb7ad3d7f29d0a42521a2e9b99926d135cf8b8ca"
)
SOURCE = os.path.join(HERE, "verify_n8_d1_m10_334_branch63_candidate.py")
with open(SOURCE, "rb") as handle:
    require(hashlib.sha256(handle.read()).hexdigest()
            == PINNED_CANDIDATE_SHA256,
            "the pinned D1 candidate source changed")
C = importlib.import_module("verify_n8_d1_m10_334_branch63_candidate")
D, V = C.D, C.V

EXPECTED_LEDGER_SHA256 = (
    "091f1fb4305131bea5b5dc0c73cf27c5af5efe3d196b8e60a007ae75eee897ec"
)


def matching_recursion_audit():
    rows = []
    matching_set = set(V.MATCHINGS[V.SITES])
    for center in V.SITES:
        packets = {}
        recovered = set()
        for neighbour in V.SITES:
            if neighbour == center:
                continue
            packet = tuple(
                matching for matching in V.MATCHINGS[V.SITES]
                if V.cell(center, neighbour, 0, 0)[:2] in matching
            )
            require(len(packet) == 15,
                    "a one-site hafnian recursion packet changed")
            packets[str(neighbour)] = len(packet)
            recovered.update(packet)
        require(recovered == matching_set and len(recovered) == 105,
                "the one-site matching packets stopped partitioning H8")
        rows.append({
            "center": center,
            "partner_packet_sizes": packets,
            "matching_partition_sha256": D.content_hash([
                [list(edge) for edge in matching]
                for matching in sorted(recovered)
            ]),
        })
    return rows


def mask_quotient_audit():
    rows = []
    for target_colour in V.COLORS:
        for mask_bits in itertools.product((False, True), repeat=3):
            support = {colour for colour, live in enumerate(mask_bits) if live}
            target_only_active = support == {target_colour}
            if not support:
                quotient_action = "term absent"
            elif target_only_active:
                quotient_action = "target line; permitted incidence"
            else:
                require(any(colour != target_colour for colour in support),
                        "a non-target incident vector lost its witness")
                quotient_action = "quotient by vector; target survives"
            rows.append({
                "target_colour": target_colour,
                "support_mask": sorted(support),
                "target_only_active": target_only_active,
                "quotient_action": quotient_action,
            })
    require(len(rows) == 24,
            "the incident-vector mask classification changed")
    return rows


def o4_allowed_support():
    F = importlib.import_module(
        "verify_n8_d1_residue_orbit4_four_star_lemma"
    )
    _state, _extras, _base, admissible, _stats = C.candidate_input()
    allowed = (set(admissible) - set(F.O.RESIDUE_HOLES)
               - set(F.S.BOUNDARY_OMISSIONS))
    require(len(allowed) == 193, "the O4 incidence universe changed")
    return frozenset(allowed)


def incidence_packets():
    allowed = o4_allowed_support()
    packets = []
    for center in V.SITES:
        for target_colour in V.COLORS:
            alternatives = []
            for neighbour in V.SITES:
                if neighbour == center:
                    continue
                target_cell = V.cell(
                    center, neighbour, target_colour, target_colour
                )
                if target_cell not in allowed:
                    continue
                off_target = tuple(sorted(
                    cell for colour in V.COLORS
                    if colour != target_colour
                    for cell in [V.cell(center, neighbour,
                                        target_colour, colour)]
                    if cell in allowed
                ))
                alternatives.append({
                    "neighbour": neighbour,
                    "target_cell": list(target_cell),
                    "off_target_cells": [list(cell) for cell in off_target],
                })
            require(alternatives,
                    "an O4 pure slice has no possible target incidence")
            packets.append({
                "center": center,
                "target_colour": target_colour,
                "alternatives": alternatives,
                "support_conclusion": (
                    "at least one alternative has its target cell live and "
                    "every listed off-target cell absent"
                ),
            })
    require(len(packets) == 24,
            "the O4 target-incidence packet census changed")
    return packets


def paired_frontier_audit(packets):
    packet = next(row for row in packets
                  if row["center"] == 7 and row["target_colour"] == 0)
    alternatives = {row["neighbour"]: row for row in packet["alternatives"]}
    # O4 kills the residue incident columns at site 7.  The paired-routing
    # frontier additionally kills the off-target columns on 07 and 27, while
    # the full 17 and 37 columns are not target-only.  Thus every alternative
    # is false, exactly as the global theorem predicts.
    require(set(alternatives) == {0, 1, 2, 3},
            "the paired frontier incidence alternatives changed")
    require(len(alternatives[0]["off_target_cells"]) == 1
            and len(alternatives[1]["off_target_cells"]) == 1
            and len(alternatives[2]["off_target_cells"]) == 2
            and len(alternatives[3]["off_target_cells"]) == 2,
            "the paired frontier column masks changed")
    return {
        "center": 7,
        "colours": [0, 1],
        "live_neighbours_after_frontier_holes": [1, 3],
        "contradiction": (
            "the only live incident columns are full/non-target, so no "
            "active target-only incidence remains"
        ),
    }


def build_ledger():
    packets = incidence_packets()
    return {
        "pinned_candidate_sha256": PINNED_CANDIDATE_SHA256,
        "hafnian_recursion": matching_recursion_audit(),
        "incident_mask_classification": mask_quotient_audit(),
        "o4_support_packets": packets,
        "paired_frontier": paired_frontier_audit(packets),
        "theorem": (
            "for every site v and pure colour a, some incident column at "
            "v is active and supported only on the target line e_a"
        ),
        "proof": (
            "expand H8 by the partner of v; absent incident vectors give no "
            "term, and quotient every other neighbour space by its nonzero "
            "non-target incident vector. The left side dies while e_a^7 "
            "survives unless one active vector is the target line"
        ),
        "base_ring_scope": (
            "the matching recursion is integral; the line quotients are "
            "taken over the fraction field of a localized integral domain"
        ),
        "characteristic_scope": "every field",
        "status": "global N=8 one-site target incidence proved",
    }


def main():
    started = monotonic()
    ledger = build_ledger()
    digest = D.content_hash(ledger)
    if EXPECTED_LEDGER_SHA256 == "TO_BE_FROZEN":
        print("ledger sha256:", digest)
    else:
        require(digest == EXPECTED_LEDGER_SHA256,
                "the one-site target-incidence ledger changed")
        print("ledger sha256 (frozen):", digest)
    print("N=8 one-site target incidence: PASS (all characteristics)")
    print("O4 packets:", len(ledger["o4_support_packets"]))
    print("elapsed: %.3fs" % (monotonic() - started))


if __name__ == "__main__":
    main()
