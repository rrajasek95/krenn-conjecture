#!/usr/bin/env python3
"""Close the double-coloop rank fork with the conjugate hybrid row.

The one-sided hybrid theorem sends each of the last 270 Cartan packets to
pure-target reselection or to one nonanchor off-diagonal S arm.  Use it in
both bright-colour orientations.  If neither pure cofactor vanishes, the
two crossed zero rows give nonempty 21- and 12-debt sets on the same strict
Hall star.  Different debt sites give the pinned distinct-head wedge; one
common site gives the pinned co-located unary-wedge closure.

The finite audit below checks the complete physical incidence behind that
composition.  It does not enumerate supports: exactness of the two complete
crossed rows supplies one supported literal mate in each nonzero aggregate.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
P, S = 6, 7
PINS = {
    "computations/verify_h3_order6_double_coloop_hybrid_interference_closure.py":
        "a04ba81cc751a262c20fa78f3fd0e2719ab1bda6ac5aad7ce63bfd87ef41c3f9",
    "notes/h3-order6-double-coloop-hybrid-interference-closure.md":
        "b33c4077ad47dbc8d6497283fadc2bd4a418926e5e18e12356bda5f7fa183a2b",
    "computations/verify_h3_physical_cartan_active_overlap_landing.py":
        "8161ab2f2b1c8de0db01a358d0ed4aad5b48779d04355ef0fc16a186b92c8cbd",
    "computations/verify_uniform_multisite_hall_star_source_reduction.py":
        "65ccab6e5830efd9f0dfa084c0d98391e89bad083fa7a41743b2fec7dde15bd5",
    "notes/uniform-multisite-hall-star-source-reduction.md":
        "a0efe068a25423f16d0e24f8d943fd09c4c6911d1dbcdd231d45e66ae37868e0",
    "computations/verify_uniform_multisite_hall_star_colocated_unary_wedge_closure.py":
        "195c57ea9d315f685246e38f00a9b14a3fdf62de084ad84313d1fa953a9a9c29",
    "notes/uniform-multisite-hall-star-colocated-unary-wedge-closure.md":
        "921aff0192d667ff569061c4bb33f03f64587eb8a915972fa9783a0578b32f1d",
}
EXPECTED_LEDGER_SHA256 = (
    "7ecdc14a0466a42bea73ce69b41308b51b00ca856c09d12ca206fe9ae7532f9e"
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load(relative, name):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def normalize(matching):
    return tuple(sorted(tuple(sorted(edge)) for edge in matching))


def partner(matching, site):
    for left, right in matching:
        if left == site:
            return right
        if right == site:
            return left
    raise RuntimeError(("site absent from matching", site, matching))


def audit():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual))

    landing = load(
        "computations/verify_h3_physical_cartan_active_overlap_landing.py",
        "double_coloop_conjugate_landing",
    )
    all_matchings = tuple(normalize(matching)
                          for matching in landing.matchings(tuple(range(8))))
    bright = tuple(matching for matching in all_matchings
                   if (P, S) not in matching)

    residuals = []
    shapes = Counter()
    for matching1 in bright:
        n1, p1 = partner(matching1, S), partner(matching1, P)
        for matching2 in bright:
            n2, p2 = partner(matching2, S), partner(matching2, P)
            if (n1, p1) != (n2, p2):
                continue
            common = {tuple(sorted((S, n1))), tuple(sorted((P, p1)))}
            tail1, tail2 = set(matching1) - common, set(matching2) - common
            require(len(tail1) == len(tail2) == 2,
                    "double-coloop tail inventory changed")
            shape = ("same_two_edge_tail" if tail1 == tail2
                     else "one_C4_tail_switch")
            if tail1 != tail2:
                require(len(tail1 ^ tail2) == 4,
                        "unequal tails stopped being one C4")
            shapes[shape] += 1
            residuals.append((matching1, matching2, n1, p1))
    require(len(residuals) == 270 and shapes == {
        "same_two_edge_tail": 90,
        "one_C4_tail_switch": 180,
    }, ("double-coloop residual census changed", len(residuals), shapes))

    pair_routes = Counter()
    mate_inventory = Counter()
    examples = []
    for matching1, matching2, centre, p_neighbour in residuals:
        common_arm = tuple(sorted((S, centre)))
        require(common_arm in matching1 and common_arm in matching2,
                "bright matchings lost their common Hall-centre arm")
        require(partner(matching1, P) == partner(matching2, P) == p_neighbour,
                "double-coloop P arm changed")

        anchors = set(matching1) | set(matching2) | {(P, S)}
        avoiding = tuple(mate for mate in all_matchings
                         if common_arm not in mate and (P, S) not in mate)
        require(len(avoiding) == 75,
                ("avoiding mate inventory changed", len(avoiding)))
        by_site = Counter(partner(mate, S) for mate in avoiding)
        expected_sites = set(range(6)) - {centre}
        require(set(by_site) == expected_sites
                and set(by_site.values()) == {15},
                ("Hall-star debt distribution changed", centre, by_site))

        for mate in avoiding:
            arm = tuple(sorted((S, partner(mate, S))))
            require(arm not in anchors,
                    ("hybrid mate stopped being off-anchor", mate, anchors))
        mate_inventory.update(by_site.values())

        # The two conjugate rows have the same 75 physical avoiding
        # matchings.  The first decorates the new S arm by 21 and the second
        # by 12.  Exactness chooses at least one supported literal mate from
        # each nonzero avoiding aggregate, so audit every possible choice.
        local = Counter()
        for mate21 in avoiding:
            site21 = partner(mate21, S)
            for mate12 in avoiding:
                site12 = partner(mate12, S)
                if site21 == site12:
                    local["colocated_reciprocal_Hall_lock"] += 1
                else:
                    local["distinct_site_transverse_wedge"] += 1
        require(local == {
            "colocated_reciprocal_Hall_lock": 1125,
            "distinct_site_transverse_wedge": 4500,
        }, ("conjugate mate-pair split changed", local))
        pair_routes.update(local)
        if not examples:
            examples.append({
                "bright_1": [list(edge) for edge in matching1],
                "bright_2": [list(edge) for edge in matching2],
                "Hall_centre": centre,
                "debt_sites": sorted(by_site),
                "mates_per_debt_site": dict(sorted(by_site.items())),
                "ordered_pair_routes": dict(sorted(local.items())),
            })

    require(pair_routes == {
        "colocated_reciprocal_Hall_lock": 303750,
        "distinct_site_transverse_wedge": 1215000,
    }, ("aggregate conjugate Hall split changed", pair_routes))
    require(mate_inventory == {15: 1350},
            ("per-site avoiding-mate multiplicities changed", mate_inventory))

    return {
        "theorem": "conjugate hybrid interference closes double-coloop rank",
        "residual_packets": len(residuals),
        "residual_shapes": dict(sorted(shapes.items())),
        "hybrid_rows": {
            "21": (
                "S--centre:22 times the other three pure-1 cells; if its "
                "complete pure-1 cofactor is nonzero, an avoiding mate "
                "carries a nonzero external S-arm cell 21"
            ),
            "12": (
                "S--centre:11 times the other three pure-2 cells; if its "
                "complete pure-2 cofactor is nonzero, an avoiding mate "
                "carries a nonzero external S-arm cell 12"
            ),
        },
        "zero_cofactor_branch": (
            "if either complete pure cofactor vanishes, its pure target row "
            "forces reselection away from the common arm and the selected-"
            "arm Cartan theorem lands the packet"
        ),
        "nonzero_cofactor_branch": {
            "avoiding_matchings_per_orientation": 75,
            "external_debt_sites": 5,
            "matchings_per_site": 15,
            "ordered_literal_mate_pairs_per_packet": 5625,
            "route_counts_per_packet": {
                "distinct_site_transverse_wedge": 4500,
                "colocated_reciprocal_Hall_lock": 1125,
            },
            "route_counts_all_packets": dict(sorted(pair_routes.items())),
        },
        "composition": (
            "the common S arm is the effective side of one strict Hall "
            "star.  Different 21/12 sites invoke the Hall-star distinct-"
            "head wedge.  A common site invokes the co-located unary-wedge "
            "closure because the normalized direct block is scalar E00"
        ),
        "consequence": (
            "the 270 packets no longer enter the generic same-head active-"
            "minor rank fork: each reselects to the selected Cartan arm or "
            "reaches a certified distinct-head active four-good overlap"
        ),
        "scope": (
            "this closes the double-coloop transverse-rank problem.  It does "
            "not by itself prove the global curved-OO source reduction, the "
            "arbitrary-packet entry theorem, or inactive Yw-to-W comparison"
        ),
        "example": examples[0],
    }


def main():
    ledger = audit()
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("conjugate Hall ledger changed", digest))
    print("h3 double-coloop conjugate Hall interference: PASS")
    print("packets=", ledger["residual_packets"])
    print("per-packet routes=",
          ledger["nonzero_cofactor_branch"]["route_counts_per_packet"])
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
