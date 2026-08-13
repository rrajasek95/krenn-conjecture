#!/usr/bin/env python3
"""Reduce failed common tails of squarefree N=8 circuits to star/triangle."""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_frame_circuit_matching_lift_trichotomy.py":
        "e0bdd386a63b17b67038ef8e8d0faf15ff041a1e8cb9f6f138e6a781233d44f1",
    "notes/frame-circuit-matching-lift-trichotomy.md":
        "b19ee3b4fb462df20c6b035bfae79bcd5518293814f6b9bc311b8a483481dab1",
    "notes/uniform-multisite-endpoint-affine-hall-concentration-boundary.md":
        "241b46d9ecede656aa59f2be6d74bc288fbada2aa4843103a950441066763df2",
    "notes/oo-one-anchor-permanent-null-frontier.md":
        "47b229a098f7bca3cc56c3427d91628420532228f28a196b54bd91ac3c38f5b2",
}
EXPECTED_LEDGER_SHA256 = (
    "89e59d2a2a173c911cb7ac88b24f76a9d5f92a46035687f0d83793c4b0d6ee2f"
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def matching_number(vertices, edges):
    edges = tuple(edges)
    best = 0
    for size in range(1, len(vertices) // 2 + 1):
        for selected in combinations(edges, size):
            endpoints = [vertex for edge in selected for vertex in edge]
            if len(set(endpoints)) == 2 * size:
                best = size
    return best


def classify_intersecting(vertices, edges):
    edges = set(edges)
    if not edges:
        return "empty"
    common = set(vertices)
    for edge in edges:
        common.intersection_update(edge)
    if common:
        return "star"
    used = set(vertex for edge in edges for vertex in edge)
    require(len(used) == 3, "pairwise-intersecting nonstar is not triangular")
    require(edges.issubset(set(combinations(sorted(used), 2))),
            "triangle containment failed")
    return "triangle"


def audit_four_site_graphs():
    vertices = tuple(range(4))
    complete = tuple(combinations(vertices, 2))
    counts = Counter()
    examples = {}
    for mask in range(1 << len(complete)):
        edges = tuple(complete[index] for index in range(len(complete))
                      if mask & (1 << index))
        nu = matching_number(vertices, edges)
        if nu == 2:
            counts["tail_exists"] += 1
            continue
        require(nu <= 1, "four-site no-tail graph has unexpected matching number")
        kind = classify_intersecting(vertices, edges)
        counts[kind] += 1
        examples.setdefault(kind, edges)
        require(all(set(left) & set(right)
                    for left, right in combinations(edges, 2)),
                "no-tail graph is not pairwise intersecting")
    require(sum(counts.values()) == 64, "four-site graph census incomplete")
    require(counts["tail_exists"] and counts["star"] and counts["triangle"],
            "four-site census missed a branch")
    return counts, examples


def main():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, ("pinned dependency changed", relative, actual))

    counts, examples = audit_four_site_graphs()
    # A squarefree frame circuit has at least four physical sites.  At N=8
    # its even complement therefore has cardinality 0, 2, or 4.
    complement_sizes = (0, 2, 4)
    ledger = {
        "pins": PINS,
        "squarefree_n8_complement_sizes": list(complement_sizes),
        "four_site_physical_support_graphs": dict(sorted(counts.items())),
        "canonical_no_tail_examples": {
            kind: [list(edge) for edge in edges]
            for kind, edges in sorted(examples.items())
        },
        "two_site_branch": (
            "a supported decorated edge is exactly a common tail; otherwise "
            "the two-site cofactor support is empty"
        ),
        "four_site_branch": (
            "no common tail iff matching number is at most one; every "
            "nonempty support is pairwise intersecting and lies in a star or "
            "triangle"
        ),
        "scope": (
            "this identifies the N=8 tail barrier but does not prove that "
            "every star/triangle barrier has an anchor-preserving landing or "
            "that the resulting active carrier is transversely rank-good"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("N8 frame-circuit tail ledger changed", digest))
    print("N=8 frame-circuit tail Hall reduction: PASS")
    print("four-site graph census:", dict(sorted(counts.items())))
    print("complement sizes:", complement_sizes)
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
