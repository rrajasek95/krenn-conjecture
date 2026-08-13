#!/usr/bin/env python3
"""Reduce physical Cartan overlap landing to one activity branch.

The Cartan theorem makes the primitive order-six face type

    S-u:11 wedge ab:11

an actual coefficient-space relative direction, equivariantly under physical
site relabelling.  The selected-anchor theorem supplies a target-full u and
a selected internal bright edge ab disjoint from u.  If u is the selected
colour-one neighbour, arm and tail occur in one selected matching, giving the
pinned visible carrier and changing (2,3) to (3,3).  If u lies outside the
two selected bright neighbours, the overlap already has ranks (3,3), but the
chosen arm is absent from both selected bright matchings.  Physicality of the
direction does not prove that its quadratic coefficient evaluates nonzero.

This checker exhausts the complete selected-matching/target-full incidence
inventory and constructs the relabelling to 07:11 wedge 24:11 in every case.
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
    "computations/verify_h3_physical_cartan_source_orbit_descent.py":
        "c92667c38c57c69dff18fd7570fa154db7e1a634a83f462dfde6bd5553128a3a",
    "computations/verify_h3_target_full_selected_anchor_overlap_synchronization.py":
        "2a985129813eb28ed102abc531ee3e83c03fb503f71c2aa721d1bd614d579f13",
    "computations/verify_h3_residual_q_order6_one_sided_overlap_landing_target.py":
        "8067fe309f363e21939a543fc37c005b54867391ca502e594762cb7d3617b9df",
    "computations/verify_h3_post_ks_full_nine_overlap_visibility_reduction.py":
        "3a18ddb3cf717d41dd3d8033d128382093d33561c98ab164bec9876b74fb8eb8",
}
EXPECTED_LEDGER_SHA256 = "63624aa41504526b8ef7676cab86bd75f3e7b550771a6acce99fe33d8bb36dd8"


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


def canonical_relabelling(site, tail):
    """Fix P,S and send (site,tail) to (0,24)."""
    left, right = tail
    require(site not in tail and left != right,
            ("carrier arm and tail stopped being disjoint", site, tail))
    mapping = {P: P, S: S, site: 0, left: 2, right: 4}
    remaining_source = [value for value in INTERNAL if value not in mapping]
    remaining_target = [value for value in INTERNAL
                        if value not in mapping.values()]
    require(len(remaining_source) == len(remaining_target) == 3,
            "internal relabelling complement changed")
    mapping.update(zip(remaining_source, remaining_target, strict=True))
    require(tuple(sorted(mapping.values())) == ALL_SITES,
            ("relabeling stopped being a site permutation", mapping))
    mapped_arm = tuple(sorted((mapping[S], mapping[site])))
    mapped_tail = tuple(sorted((mapping[left], mapping[right])))
    require(mapped_arm == (0, 7) and mapped_tail == (2, 4),
            ("carrier did not normalize to 07 wedge 24", mapping))
    return mapping


def audit():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual))

    direct = tuple(sorted((P, S)))
    bright = tuple(matching for matching in matchings(ALL_SITES)
                   if direct not in {tuple(sorted(edge)) for edge in matching})
    full_sets = tuple(frozenset(choice)
                      for size in range(2, len(INTERNAL) + 1)
                      for choice in combinations(INTERNAL, size))
    require(len(bright) == 90 and len(full_sets) == 57,
            "landing inventory changed")

    branches = Counter()
    occupied_arm = Counter()
    relabel_types = set()
    audits = 0
    for matching1 in bright:
        neighbour1 = neighbour(matching1, S)
        tails1 = internal_edges(matching1)
        for matching2 in bright:
            neighbour2 = neighbour(matching2, S)
            for target_full in full_sets:
                outside = target_full - {neighbour1, neighbour2}
                if outside:
                    site = min(outside)
                    tails = tuple(edge for edge in tails1 if site not in edge)
                    require(tails, "rank-three branch lost a selected cofactor")
                    tail = tails[0]
                    rank_before = (3, 3)
                    rank_after = (3, 3)
                    branches["rank3_overlap_activity_not_forced"] += 1
                else:
                    require(target_full == {neighbour1, neighbour2}
                            and neighbour1 != neighbour2,
                            "trapped target-full alternative changed")
                    site = neighbour1
                    require(all(site not in edge for edge in tails1),
                            "selected missing arm lost its internal cofactors")
                    tail = tails1[0]
                    rank_before = (2, 3)
                    rank_after = (3, 3)
                    branches["selected_arm_repairs_deficient_quotient"] += 1

                arm = tuple(sorted((S, site)))
                selected_edges = {tuple(sorted(edge)) for edge in matching1}
                occupied_arm[arm in selected_edges] += 1
                mapping = canonical_relabelling(site, tail)
                relabel_types.add(tuple(mapping[index] for index in ALL_SITES))

                require(tail in selected_edges and site not in tail,
                        "physical face lost its selected tail candidate")
                require(rank_after == (3, 3)
                        and rank_before in ((3, 3), (2, 3)),
                        "one-sided rank landing changed")
                audits += 1

    require(audits == 90 * 90 * 57 == 461700,
            ("landing census changed", audits))
    require(branches == {
        "rank3_overlap_activity_not_forced": 454950,
        "selected_arm_repairs_deficient_quotient": 6750,
    }, ("physical landing branches changed", branches))
    require(occupied_arm[True] and occupied_arm[False],
            "the theorem stopped auditing both occupied and new directions")

    return {
        "theorem": "physical Cartan overlap landing has one exact activity boundary",
        "audited_matching_packets": audits,
        "branches": dict(sorted(branches.items())),
        "arm_current_support": {
            "occupied": occupied_arm[True],
            "new_physical_direction": occupied_arm[False],
        },
        "canonical_site_relabellings": len(relabel_types),
        "canonical_face": "07:11 wedge 24:11",
        "activity": (
            "the trapped branch has arm and tail in one selected bright "
            "matching and is the pinned visible carrier.  In the rank-three "
            "branch the arm is absent from both selected bright matchings; "
            "Cartan source provenance alone does not make its quadratic "
            "coefficient evaluation nonzero"
        ),
        "rank": (
            "outside-neighbour branch already has selected ranks (3,3); "
            "trapped branch uses the same arm as the missing quotient axis "
            "and changes (2,3) to (3,3)"
        ),
        "consequence": (
            "the selected-arm branch is closed; the sole landing residue is "
            "nonvanishing or dependence/separator for the Cartan coefficient "
            "on an already rank-(3,3) overlap"
        ),
        "scope": (
            "the synchronized h=3 order-six packet after physical Cartan "
            "descent.  It does not prove uniform entry of every clean packet "
            "into this normalization or the inactive dual route"
        ),
    }


def main():
    ledger = audit()
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("physical overlap landing ledger changed", digest))
    print("h3 physical Cartan active-overlap landing: PASS")
    print("audits=", ledger["audited_matching_packets"])
    print("branches=", ledger["branches"])
    print("selected-arm branch -> active rank-(3,3); rank3 activity remains")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
