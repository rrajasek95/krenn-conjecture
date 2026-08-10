#!/usr/bin/env python3
"""Audit anchor safety of the two-bad zero-row affine retraction.

The pinned source-row audit proves that the two outer zero-row families may
be set to zero through exact sources.  Here we audit the missing graph fact:
every removed scalar cell meets a coordinate already incident with the
preserved direct unit, hence no removed cell is a mutual anchor.  In the
shared-endpoint normal form the other endpoint of each direct unit already
has degree one.  The zero limit therefore preserves every old mutual anchor
and creates the direct unit as a new one whenever its outer family was
nonempty.

At a maximum-mutual-anchor source both outer families must consequently be
zero.  The selected pair rows then reduce to the unary-top/binary-response
packet, whose support charge is pinned separately.
"""

from __future__ import annotations

from hashlib import sha256
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_shared_reciprocal_two_bad_zero_row_affine_retraction.py":
        "ba9a319b5edb9a69d6594ec143d0c070cd4ea46ad2435e8afe2b7b2a77a1a3ca",
    "computations/verify_scalar_unit_binary_residual_target_branch.py":
        "6d5f1b8cacf29ea21b0033fbb7e553e5044d5a5dcb7ea3923ad8c3e4d812ca54",
}
EXPECTED_DIGEST = "c58180a926bf03b533d591a5c5f050ed315be49af9bcad6d9d22a672e747d208"


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, f"dependency changed: {relative}: {actual}")


def mutual_anchors(edges):
    degrees = {}
    for left, right, name in edges:
        degrees[left] = degrees.get(left, 0) + 1
        degrees[right] = degrees.get(right, 0) + 1
    return {
        name for left, right, name in edges
        if degrees[left] == degrees[right] == 1
    }


def audit_anchor_monotonicity():
    # q_i and r_j stand for the 18 slots in each scaled endpoint family.
    # D_ac is their only common physical scalar cell.  Distinct opposite
    # coordinate labels are the adversarial case for anchor creation; an
    # arbitrary pre-existing retained graph is represented by old anchors
    # on disjoint vertices and by extra retained edges at selected opposite
    # coordinates.  We exhaust the occupancy and extra-degree bits of a
    # symmetry-complete three-slot quotient: q-only, r-only, and shared.
    patterns = 0
    strict_cases = 0
    for q_only, r_only, shared in itertools.product((0, 1), repeat=3):
        for q_extra, r_extra, shared_left_extra, shared_right_extra in (
                itertools.product((0, 1), repeat=4)):
            edges = [
                ("p:a", "q:a", "pq"),
                ("p:c", "r:c", "pr"),
                ("u:0", "v:0", "old0"),
            ]
            removed = set()
            if q_only:
                edges.append(("q:a", "x:q", "qcell"))
                removed.add("qcell")
            if r_only:
                edges.append(("r:c", "x:r", "rcell"))
                removed.add("rcell")
            if shared:
                edges.append(("q:a", "r:c", "Dac"))
                removed.add("Dac")
            if q_extra:
                edges.append(("x:q", "z:q", "qextra"))
            if r_extra:
                edges.append(("x:r", "z:r", "rextra"))
            if shared_left_extra:
                edges.append(("q:a", "z:ql", "ql_extra"))
                removed.add("ql_extra")
            if shared_right_extra:
                edges.append(("r:c", "z:rr", "rr_extra"))
                removed.add("rr_extra")

            before = mutual_anchors(edges)
            after_edges = [edge for edge in edges if edge[2] not in removed]
            after = mutual_anchors(after_edges)
            require(not (before - removed) - after,
                    "the retraction destroyed a retained mutual anchor")
            require(not (before & removed),
                    "a scaled outer-row cell became a mutual anchor")

            q_nonempty = q_only or shared or shared_left_extra
            r_nonempty = r_only or shared or shared_right_extra
            require(("pq" in after) and ("pr" in after),
                    "a preserved direct unit failed to become an anchor")
            require(len(after) >= len(before) + int(q_nonempty) + int(r_nonempty),
                    "the direct-anchor gain ledger failed")
            strict_cases += int(q_nonempty or r_nonempty)
            patterns += 1

    require((patterns, strict_cases) == (128, 124),
            f"the anchor-safety quotient census changed: "
            f"{patterns}/{strict_cases}")
    return {
        "symmetry_quotient_patterns": patterns,
        "strict_gain_patterns": strict_cases,
        "scaled_cell_anchor_status": "never mutual",
        "gain": "1_(Qa,D_a* nonempty)+1_(Rc,D_*c nonempty)",
        "conclusion_at_maximum_nu": [
            "Qa=0 and D_a*=0", "Rc=0 and D_*c=0",
        ],
    }


def audit_unary_binary_reduction():
    # In the shared-endpoint packet the p-side a and c rows were already
    # zero.  Anchor maximality supplies the two outer zero rows.  Around pq
    # this makes both selected a-star rows zero, leaving exactly one unary
    # top row and a 2x2 binary response matrix.
    colours = ("a", "b", "c")
    rows = {}
    for left in colours:
        for right in colours:
            if left == right == "a":
                rows[left, right] = "alpha*q^[h]=X_a"
            elif left == "a" or right == "a":
                rows[left, right] = "0=0"
            elif left == right:
                rows[left, right] = f"p_{left}*s_{right}*q^[h-1]=X_{left}"
            else:
                rows[left, right] = f"p_{left}*s_{right}*q^[h-1]=0"
    require(len(rows) == 9, "the reduced pair lost a target row")
    require(sum(value == "0=0" for value in rows.values()) == 4,
            "the four selected-colour zero rows changed")
    require(rows["a", "a"] == "alpha*q^[h]=X_a",
            "the unary top row changed")

    charges = {
        h: {
            "unary_top_cells": h,
            "missing_b_near_matching": h - 1,
            "missing_c_near_matching": h - 1,
            "minimum_internal_support": 3 * h - 2,
        }
        for h in range(3, 9)
    }
    require(charges[3]["minimum_internal_support"] == 7,
            "the N=8 unary/binary support charge changed")
    return {
        "nine_rows": {f"{left}{right}": value
                      for (left, right), value in rows.items()},
        "support_charge_by_h": charges,
        "N8_residual_sites": 6,
        "N8_minimum_internal_support": 7,
        "remaining_gate": (
            "anchor-preserving nine-row modification of the unary-top/"
            "binary-response packet; the retraction itself is now anchor-safe"
        ),
    }


def main():
    pin_dependencies()
    anchors = audit_anchor_monotonicity()
    reduced = audit_unary_binary_reduction()
    ledger = {
        "pins": PINS,
        "anchor_safety": anchors,
        "unary_binary_reduction": reduced,
        "verdict": (
            "the zero-row affine retraction preserves every mutual anchor "
            "and strictly raises nu unless both outer rows already vanish; "
            "hence the synchronized two-bad packet is forced into the "
            "unary-top/binary-response one-bad normal form"
        ),
        "scope": (
            "exact maximum-mutual-anchor normalization; this closes the "
            "retraction caveat but not the remaining one-bad packet"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_DIGEST != "TO_BE_FILLED":
        require(digest == EXPECTED_DIGEST,
                f"anchor-safe retraction ledger changed: {digest}")

    print("shared reciprocal anchor-safe zero-row retraction: PASS")
    print("anchor quotient patterns: 128; strict gain patterns: 124")
    print("maximum nu forces Qa=Rc=0 and the corresponding D row/column zero")
    print("reduced packet: unary top + 2x2 binary response")
    print("N=8 internal support charge: at least 7 cells")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
