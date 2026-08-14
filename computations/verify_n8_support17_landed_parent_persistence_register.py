#!/usr/bin/env python3
"""Structural persistence register for the 133 landed support-16 parents.

Every support-17 graph of minimum degree at least three has a high-high edge;
deleting it preserves minimum degree and gives support 16.  The 148 cap-dark
parents are handled by the matching-debt recurrence.  This checker classifies
all one-edge augmentations of the remaining 133 directed parent orbits by
literal complete-private persistence and crossed-binary response faces, then
quotients the genuine failure strata by directed graph isomorphism.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
from itertools import permutations
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
EXPECTED_SHA256 = "005230a4aed405107975d9eda404ef2949be10f36fd191a5468cf6eb707b0e45"
N = 8


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load_local(module_name, filename):
    spec = spec_from_file_location(module_name, HERE / filename)
    require(spec is not None and spec.loader is not None,
            ("failed to load dependency", filename))
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


PROTOTYPE = load_local(
    "n8_support16_prototype_for_landed_parent_persistence",
    "verify_n8_support16_two_cap_prototype_orbit_extension.py",
)
ORBIT = PROTOTYPE.ORBIT


def high_high_deletion_lemma():
    """Return the exact excess-degree contradiction for support 17."""
    feasible_independent_high_sizes = []
    ledger = []
    for high_size in range(1, N + 1):
        excess_capacity = 4 * high_size
        high_degree_sum = 3 * high_size + 10
        low_degree_capacity = 3 * (N - high_size)
        excess_possible = excess_capacity >= 10
        shore_possible = high_degree_sum <= low_degree_capacity
        if excess_possible and shore_possible:
            feasible_independent_high_sizes.append(high_size)
        ledger.append({
            "high_vertex_count": high_size,
            "excess_capacity": excess_capacity,
            "high_degree_sum": high_degree_sum,
            "low_degree_capacity": low_degree_capacity,
            "can_hold_total_excess_10": excess_possible,
            "can_be_independent": shore_possible,
        })
    require(not feasible_independent_high_sizes,
            ("independent high-degree support17 class survived",
             feasible_independent_high_sizes))
    return {
        "support_size": 17,
        "degree_sum": 34,
        "minimum_degree": 3,
        "total_excess_over_cubic": 10,
        "size_ledger": tuple(ledger),
        "conclusion": (
            "the degree>=4 vertex set contains an edge; deleting that edge "
            "leaves 16 edges and minimum degree at least 3"
        ),
    }


def canonical_directed_key(edges, incidence):
    endpoint, target_edge = incidence
    other = target_edge[0] if target_edge[1] == endpoint else target_edge[1]
    remaining = tuple(
        vertex for vertex in range(N) if vertex not in (endpoint, other)
    )
    best = None
    for images in permutations(range(2, N)):
        mapping = {endpoint: 0, other: 1}
        mapping.update(dict(zip(remaining, images)))
        key = tuple(sorted(
            tuple(sorted((mapping[left], mapping[right])))
            for left, right in edges
        ))
        if best is None or key < best:
            best = key
    require(best is not None, ("failed directed canonicalization", edges,
                               incidence))
    return best


def parent_route(item):
    if item["route"] == "forced-distinct-two-cap":
        return "original-two-cap"
    if item["private_face_count"]:
        return "complete-private-cap"
    if len(item["prototype_faces"]) >= 2:
        return "collision-normalization"
    return None


def audit_persistence_register():
    terminal_records = ORBIT.terminal_two_rrx_records()
    ORBIT.terminal_two_rrx_records = lambda: terminal_records
    audit = PROTOTYPE.audit_all_orbits()
    parents = tuple(
        item for item in audit["graph_ledgers"]
        if parent_route(item) is not None
    )
    require(len(parents) == 133,
            ("landed parent-orbit count changed", len(parents)))
    all_edges = {
        (left, right)
        for left in range(N) for right in range(left + 1, N)
    }
    structural = Counter()
    weighted_structural = Counter()
    hardest = Counter()
    failure_keys = {
        "complete-private-cap": Counter(),
        "original-two-cap": Counter(),
        "collision-normalization": Counter(),
    }
    ledgers = []

    for item in parents:
        route = parent_route(item)
        edges = tuple(
            terminal_records[item["graph_index"]]["representative_edges"]
        )
        for new_edge in sorted(all_edges - set(edges)):
            augmented = tuple(sorted(edges + (new_edge,)))
            adjacency = ORBIT.adjacency_from_edges(augmented)
            shapes = []
            private_caps = []
            binary_caps = []
            for cap_edge in augmented:
                if item["incidence"][0] not in cap_edge:
                    continue
                through, residue = PROTOTYPE.cap_shape(
                    adjacency, augmented, item["incidence"], cap_edge
                )
                if not through:
                    continue
                shapes.append((cap_edge, len(through), len(residue)))
                if not residue:
                    private_caps.append(cap_edge)
                if len(residue) == 2:
                    PROTOTYPE.audit_prototype_crossed_shape(cap_edge, residue)
                    binary_caps.append(cap_edge)

            signature = (route, bool(private_caps), len(binary_caps))
            structural[signature] += 1
            weighted_structural[signature] += item["orbit_size"]
            if route == "complete-private-cap":
                failure = not private_caps
                hard = failure and not binary_caps
            elif route == "original-two-cap":
                # A new private face is an unconditional landing.  Two binary
                # faces are the exact rank-deformation candidate; zero or one
                # is the structural failure stratum.
                failure = not private_caps and len(binary_caps) < 2
                hard = failure
            else:
                # The collision route used a missing pure row, not a cap, so
                # every augmentation needs a new row/cap audit.
                failure = True
                hard = not private_caps and not binary_caps

            if hard:
                hardest[route] += 1
            if failure:
                key = canonical_directed_key(augmented, item["incidence"])
                failure_keys[route][key] += 1
            ledgers.append({
                "parent_route": route,
                "graph_index": item["graph_index"],
                "parent_orbit_size": item["orbit_size"],
                "incidence": item["incidence"],
                "new_edge": new_edge,
                "response_shapes": tuple(shapes),
                "private_caps": tuple(private_caps),
                "binary_caps": tuple(binary_caps),
                "requires_deformation_or_row_audit": failure,
                "hard_no_private_or_sufficient_binary": hard,
            })

    require(len(ledgers) == 133 * 12,
            ("landed-parent augmentation count changed", len(ledgers)))
    require(structural == Counter({
        ("complete-private-cap", True, 0): 611,
        ("complete-private-cap", True, 1): 246,
        ("complete-private-cap", True, 2): 48,
        ("complete-private-cap", False, 0): 207,
        ("complete-private-cap", False, 1): 85,
        ("complete-private-cap", False, 2): 85,
        ("complete-private-cap", False, 3): 38,
        ("original-two-cap", True, 0): 5,
        ("original-two-cap", True, 1): 12,
        ("original-two-cap", True, 2): 7,
        ("original-two-cap", False, 0): 35,
        ("original-two-cap", False, 1): 66,
        ("original-two-cap", False, 2): 104,
        ("original-two-cap", False, 3): 35,
        ("collision-normalization", False, 0): 1,
        ("collision-normalization", False, 1): 8,
        ("collision-normalization", False, 2): 3,
    }), ("landed-parent structural split changed", structural))
    require(hardest == Counter({
        "complete-private-cap": 207,
        "original-two-cap": 101,
        "collision-normalization": 1,
    }), ("hardest persistence strata changed", hardest))

    return {
        "parent_orbit_count": len(parents),
        "augmentation_count": len(ledgers),
        "structural_histogram": tuple(sorted(structural.items())),
        "weighted_structural_histogram": tuple(
            sorted(weighted_structural.items())
        ),
        "hard_no_private_or_sufficient_binary": tuple(
            sorted(hardest.items())
        ),
        "failure_directed_isomorphism_types": tuple(
            (
                route,
                len(counter),
                tuple(sorted(Counter(counter.values()).items())),
            )
            for route, counter in sorted(failure_keys.items())
        ),
        "augmentations": tuple(ledgers),
        "scope": (
            "structural persistence only: binary candidates still require "
            "colour/rank compatibility, and all recorded failures require "
            "cap deformation or normalized source-row analysis"
        ),
    }


def canonical(value):
    if isinstance(value, dict):
        return {
            str(key): canonical(item)
            for key, item in sorted(value.items(), key=lambda pair: str(pair[0]))
        }
    if isinstance(value, (list, tuple)):
        return [canonical(item) for item in value]
    return value


def main():
    ledger = canonical({
        "high_high_deletion": high_high_deletion_lemma(),
        "landed_parent_persistence": audit_persistence_register(),
    })
    digest = sha256(
        json.dumps(ledger, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    if EXPECTED_SHA256 == "TO_BE_PINNED":
        print("LEDGER", digest)
    else:
        require(digest == EXPECTED_SHA256,
                ("landed-parent persistence ledger changed", digest))
    persistence = ledger["landed_parent_persistence"]
    print("N=8 support-17 landed-parent persistence register: PASS")
    print("  landed support-16 parent orbits:",
          persistence["parent_orbit_count"])
    print("  representative one-edge augmentations:",
          persistence["augmentation_count"])
    print("  hardest structural strata:",
          persistence["hard_no_private_or_sufficient_binary"])
    print("  directed failure types:",
          persistence["failure_directed_isomorphism_types"])


if __name__ == "__main__":
    main()
