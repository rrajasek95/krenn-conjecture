#!/usr/bin/env python3
"""Synchronize an h=3 target-full site with the selected bright anchors.

For an eight-site source let P=6,S=7 and let the unary pure-zero matching
use PS.  Each selected bright matching avoids PS and therefore gives one
bright neighbour of S and two internal bright cofactor edges.  The corrected
h=3 incidence theorem supplies at least two target-full residual sites.

Either one target-full site is outside the two selected bright neighbours;
then all three selected endpoint heads survive in the overlap (S,u).  Or the
two target-full sites are exactly the two distinct bright neighbours.  In
that case choosing the colour-one neighbour deletes precisely the selected
colour-one arm, so that arm is the missing quotient direction, and its
matching contains two nonzero internal colour-one cofactor edges disjoint
from it.  This is exactly the site/colour type of the primitive order-six
face 07:11 wedge 24:11 after relabelling.

The theorem is a rank/label synchronization.  It does not physically
totalize the order-six chain or prove activity of an unoccupied arm in the
already-rank-three branch.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
P, S = 6, 7
INTERNAL = tuple(range(6))
ALL_SITES = tuple(range(8))
PINS = {
    "computations/verify_h3_post_ks_full_nine_overlap_visibility_reduction.py":
        "3a18ddb3cf717d41dd3d8033d128382093d33561c98ab164bec9876b74fb8eb8",
    "computations/verify_h3_residual_q_order6_missing_face_probe.py":
        "5f0e6ad385547aed67f1d954da57c71929d336552bb98d07c68d271889b982ab",
}
EXPECTED_LEDGER_SHA256 = "9f659658be255adff96c424c557fbe32742af49b65e727b61c1de18fcc24d908"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for position, second in enumerate(vertices[1:], start=1):
        remainder = vertices[1:position] + vertices[position + 1:]
        for tail in matchings(remainder):
            answer.append(((first, second),) + tail)
    return tuple(answer)


def neighbour(matching, site):
    for left, right in matching:
        if left == site:
            return right
        if right == site:
            return left
    raise RuntimeError(("site absent from matching", site, matching))


def internal_edges(matching):
    return tuple(tuple(sorted(edge)) for edge in matching
                 if edge[0] in INTERNAL and edge[1] in INTERNAL)


def audit():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual))

    direct = tuple(sorted((P, S)))
    bright = tuple(matching for matching in matchings(ALL_SITES)
                   if direct not in {tuple(sorted(edge)) for edge in matching})
    require(len(bright) == 90, "the direct-free K8 matching count changed")
    full_sets = tuple(frozenset(choice)
                      for size in range(2, len(INTERNAL) + 1)
                      for choice in combinations(INTERNAL, size))
    require(len(full_sets) == 57, "the target-full subset count changed")

    branches = Counter()
    audits = 0
    for matching1 in bright:
        neighbour1 = neighbour(matching1, S)
        tails1 = internal_edges(matching1)
        require(neighbour1 in INTERNAL and len(tails1) == 2,
                "a bright matching lost its S arm or two internal tails")
        for matching2 in bright:
            neighbour2 = neighbour(matching2, S)
            require(neighbour2 in INTERNAL,
                    "a bright matching acquired the forbidden PS edge")
            for target_full in full_sets:
                outside = target_full - {neighbour1, neighbour2}
                if outside:
                    site = min(outside)
                    surviving_colours = {
                        0,  # the selected pure-zero PS arm
                        1 if neighbour1 != site else None,
                        2 if neighbour2 != site else None,
                    } - {None}
                    require(surviving_colours == {0, 1, 2},
                            "an outside target-full overlap lost selected rank 3")
                    disjoint_tails = tuple(edge for edge in tails1
                                           if site not in edge)
                    require(disjoint_tails,
                            "the rank-three overlap lost a disjoint pure tail")
                    branches["selected_overlap_already_rank_3"] += 1
                else:
                    require(neighbour1 != neighbour2
                            and target_full == {neighbour1, neighbour2},
                            "the trapped two-site alternative changed")
                    site = neighbour1
                    surviving_colours = {0, 2}
                    require(neighbour2 != site
                            and surviving_colours == {0, 2},
                            "the trapped overlap lost its e0/e2 plane")
                    arm = tuple(sorted((S, site)))
                    require(arm in {tuple(sorted(edge)) for edge in matching1},
                            "the missing colour-one arm is not selected")
                    require(len(tails1) == 2
                            and all(site not in edge for edge in tails1),
                            "the selected missing arm lost its pure cofactors")
                    branches["selected_missing_arm_is_visible_colour_1"] += 1
                audits += 1

    require(sum(branches.values()) == audits == 90 * 90 * 57,
            "the selected-anchor synchronization census changed")
    require(set(branches) == {
        "selected_overlap_already_rank_3",
        "selected_missing_arm_is_visible_colour_1",
    }, "an unexpected synchronization branch appeared")
    return {
        "direct_free_bright_matchings_per_colour": len(bright),
        "target_full_subsets_of_six_sites": len(full_sets),
        "audited_pairs_and_full_sets": audits,
        "branch_counts": dict(sorted(branches.items())),
        "rank_three_branch": (
            "a target-full site outside the two selected bright neighbours "
            "gives an overlap whose selected S-star already has heads 0,1,2"
        ),
        "visible_arm_branch": (
            "otherwise the two full sites are the two distinct bright "
            "neighbours; choosing the colour-one neighbour leaves span(e0,e2) "
            "and the deleted selected S-u:11 arm is the missing quotient axis"
        ),
        "cofactor_tail": (
            "the selected colour-one matching has two internal pure-11 edges "
            "disjoint from its S-u arm; either can be the primitive tail"
        ),
        "canonical_relabelling": (
            "internal-site relabelling sends the chosen site to 0 and one "
            "chosen tail to 24; the typed face is 07:11 wedge 24:11"
        ),
    }


def main():
    ledger = {
        "theorem": "h3 target-full selected-anchor overlap synchronization",
        "audit": audit(),
        "conditional_consequence": (
            "once a source-faithful order-six totalization supplies its "
            "primitive endpoint/cofactor carrier, selected-anchor incidence "
            "creates no additional site/colour rank branch: the overlap is "
            "already rank (3,3), or the primitive arm is the selected missing "
            "bright quotient direction"
        ),
        "scope": (
            "exact matching/rank/label theorem for an eight-site h=3 source. "
            "It does not construct the physical relative totalization, prove "
            "an unoccupied endpoint arm active, or perform downstream descent"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"selected-anchor synchronization ledger changed: {digest}")
    print("h3 target-full selected-anchor overlap synchronization: PASS")
    print(f"audits={ledger['audit']['audited_pairs_and_full_sets']}")
    print(f"branches={ledger['audit']['branch_counts']}")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
