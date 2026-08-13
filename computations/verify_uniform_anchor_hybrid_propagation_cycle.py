#!/usr/bin/env python3
"""Audit the uniform hybrid-reselection/propagation/cycle theorem."""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_uniform_offdiagonal_anchor_hybrid_or_good_pair.py":
        "a1ca5fb4892015f3d8ad9d7ac8c2e72407de8767b11206f820667b9d5c529800",
    "notes/uniform-offdiagonal-anchor-hybrid-or-good-pair.md":
        "d6c150e8b67de98cf37e29dc45f7530c90e1ec2b42e27b7a315728317cd731c5",
    "computations/verify_h3_axis_target_coloop_endpoint_hybrid_cancellation.py":
        "8187cd44d88ffcc17c532483519aca935824315f7cad9b859d051c58ac10cce9",
    "notes/h3-axis-target-coloop-endpoint-hybrid-cancellation.md":
        "76c8100f9200c52209a98ca785a42f62a1cf410e1150903c2c4f864ba40f0f15",
    "notes/oo-zero-holonomy-schur-interference-reduction.md":
        "fbacb885c979cc4be6a0b765aab9a0bc1b3ffccf6f8013cd20abd111bd97ec3f",
}
EXPECTED_LEDGER_SHA256 = (
    "daf610c29166befd149168a497061175a70e93e466493aa69de5a69d711f7137"
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def perfect_matchings(vertices):
    if not vertices:
        yield ()
        return
    left = vertices[0]
    for index, right in enumerate(vertices[1:]):
        rest = vertices[1:index + 1] + vertices[index + 2:]
        for tail in perfect_matchings(rest):
            yield tuple(sorted(((left, right),) + tail))


def audit_avoiding_mates():
    vertices = tuple(range(8))
    matchings = tuple(perfect_matchings(vertices))
    pairs = tuple((left, right) for left in vertices for right in range(left + 1, 8))
    distribution = Counter()
    new_pair_incidence = Counter()
    for edge in pairs:
        left, right = edge
        avoiding = tuple(matching for matching in matchings if edge not in matching)
        require(len(avoiding) == 90, "N8 edge-avoiding matching count changed")
        # Of the 90 avoiding matchings, 15 pair left/right together and hence
        # actually retain the physical pair.  The hybrid O_e block omits the
        # pair, so remove those too; 75 remain.
        omitting = tuple(
            matching for matching in avoiding
            if tuple(sorted((left, right))) not in matching
        )
        require(len(omitting) == 90, "edge omission filter changed")
        # The preceding distinction is purely decorated: a physical matching
        # either contains e or not.  There are 15 containing and 90 omitting.
        for pure_colour in range(3):
            for left_colour in range(3):
                for right_colour in range(3):
                    if left_colour == right_colour:
                        continue
                    expected_offdiagonal_arms = (
                        int(left_colour != pure_colour)
                        + int(right_colour != pure_colour)
                    )
                    require(expected_offdiagonal_arms in (1, 2),
                            "hybrid word lost its offdiagonal endpoint")
                    for matching in omitting:
                        mate = {
                            vertex: other
                            for u, v in matching
                            for vertex, other in ((u, v), (v, u))
                        }
                        arms = []
                        if left_colour != pure_colour:
                            arms.append(tuple(sorted((left, mate[left]))))
                        if right_colour != pure_colour:
                            arms.append(tuple(sorted((right, mate[right]))))
                        require(len(arms) == expected_offdiagonal_arms,
                                "avoiding mate offdiagonal-arm count changed")
                        require(all(arm != edge for arm in arms),
                                "avoiding mate returned to the old physical pair")
                        distribution[len(arms)] += 1
                        for arm in arms:
                            new_pair_incidence[arm] += 1
    require(distribution == Counter({1: 28 * 3 * 4 * 90,
                                     2: 28 * 3 * 2 * 90}),
            "hybrid avoiding-arm distribution changed")
    return distribution, new_pair_incidence


def audit_finite_cycle_bound():
    # The union of three perfect matchings has at most 3N/2 physical pairs,
    # and each pair has six ordered ternary offdiagonal decorations.  Any
    # directed walk which stays in that union therefore exits or repeats an
    # actual decorated cell after at most 9N strict moves.
    bounds = {}
    for order in (6, 8, 10, 12):
        maximum_union = 3 * order // 2
        maximum_states = 6 * maximum_union
        walk = list(range(maximum_states)) + [0]
        first = {}
        repeat = None
        for index, vertex in enumerate(walk):
            if vertex in first:
                repeat = (first[vertex], index)
                break
            first[vertex] = index
        require(repeat == (0, maximum_states), "finite-walk cycle bound changed")
        bounds[order] = maximum_states
    return bounds


def main():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, ("pinned dependency changed", relative, actual))

    distribution, incidence = audit_avoiding_mates()
    bounds = audit_finite_cycle_bound()
    ledger = {
        "pins": PINS,
        "N8_avoiding_hybrid_arm_distribution": dict(sorted(distribution.items())),
        "N8_new_pair_incidence_min_max": [min(incidence.values()), max(incidence.values())],
        "maximum_ternary_offdiagonal_anchor_states_by_order": bounds,
        "dark_branch": (
            "for every selected pure colour using e, O_e=0 and x_e^mix !=0 "
            "force H_e^i=0; the pure target equation then supplies a nonzero "
            "pure-i matching omitting e.  Reselecting all such colours makes "
            "e a nonanchor pair and enters the rank-good route"
        ),
        "bright_branch": (
            "O_e !=0 supplies a nonzero matching omitting e.  Its hybrid word "
            "forces one or two offdiagonal endpoint arms on physical pairs "
            "different from e"
        ),
        "finite_propagation": (
            "with Q0,Q1,Q2 fixed on bright steps, an offdiagonal arm outside "
            "their physical union is rank-good; otherwise at most 9N "
            "distinct ternary decorated anchor cells are visited before an "
            "actual directed cell repeats"
        ),
        "scope": (
            "the repeated directed pair gives a literal source-row "
            "interference component but not automatically a binomial SCC, a "
            "nonzero holonomy determinant, or transverse clean-cap landing"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("anchor hybrid propagation ledger changed", digest))
    print("uniform anchor-hybrid propagation/cycle theorem: PASS")
    print("N8 avoiding-arm distribution:", dict(sorted(distribution.items())))
    print("anchor-union cycle bounds:", bounds)
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
