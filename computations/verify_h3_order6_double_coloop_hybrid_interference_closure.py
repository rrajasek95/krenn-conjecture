#!/usr/bin/env python3
"""Route the last Cartan packets by the shared-arm hybrid interference row.

The selected-activity census leaves 270 packets.  In every one, the two
bright pure matchings share the physical S-arm e=S--n (and also the P-arm).
Replace the pure-1 cell on e by the already selected pure-2 cell and retain
the three pure-1 cells on the first bright matching.  This is a nonzero term
in a mixed zero row.

The complete-row factorization gives the exact alternative already proved
by the target-coloop hybrid theorem.  An avoiding mate either uses the
forbidden mixed direct PS cell or has a new off-diagonal S-arm outside all
three pure anchors.  If there is no avoiding mate, the pure-1 target row
forces a pure matching omitting e, so the selected-arm theorem applies after
reselection.  Thus the 270 packets are not a new interference branch.
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
    "computations/verify_h3_order6_primitive_selected_matching_activity.py":
        "aa0c3ec3f3a96f7fe9e8bb98117f4aec21501c0b77dda2ff5245eef19e9a34f2",
    "notes/h3-order6-primitive-selected-matching-activity.md":
        "a3db89edb5395e222566ae916197e8bed9dc5d4b22720304369aa7fbe10af184",
    "computations/verify_h3_axis_target_coloop_hybrid_anchor_escape.py":
        "e16f10abeb8d3ae8a40f2f6f57be9297d0bb49d7997214fe07861ef8dab6a307",
    "computations/verify_uniform_one_bad_nonanchor_offdiagonal_good_pair.py":
        "64e85cd84112b5160efe4f43ce1208da3c49f5e58b3e4a4d6192e6a9c229c306",
}
EXPECTED_LEDGER_SHA256 = (
    "ec06a9462201d11a1ea1aa68e0e2bde55109e9b3419592b294a84b86d0623b93"
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


def audit():
    for relative, expected in PINS.items():
        if expected == "TO_BE_PINNED":
            continue
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, ("pinned dependency changed", relative, actual))

    activity = load(
        "computations/verify_h3_order6_primitive_selected_matching_activity.py",
        "double_coloop_activity",
    )
    landing = load(
        "computations/verify_h3_physical_cartan_active_overlap_landing.py",
        "double_coloop_landing",
    )
    bright = tuple(
        normalize(matching)
        for matching in landing.matchings(tuple(range(8)))
        if (P, S) not in normalize(matching)
    )

    residuals = []
    shapes = Counter()
    for matching1 in bright:
        n1 = landing.neighbour(matching1, S)
        p1 = landing.neighbour(matching1, P)
        for matching2 in bright:
            n2 = landing.neighbour(matching2, S)
            p2 = landing.neighbour(matching2, P)
            if n1 != n2 or p1 != p2:
                continue
            # The selected-activity residual has the unique target-full set
            # {n,p}.  Its matching count is therefore one per ordered pair.
            common = {tuple(sorted((S, n1))), tuple(sorted((P, p1)))}
            tail1 = set(matching1) - common
            tail2 = set(matching2) - common
            require(len(tail1) == len(tail2) == 2,
                    "shared-arm tail inventory changed")
            shape = "same_two_edge_tail" if tail1 == tail2 else "one_C4_tail_switch"
            if shape != "same_two_edge_tail":
                require(len(tail1 ^ tail2) == 4,
                        "unequal double-coloop tails stopped being one C4")
            shapes[shape] += 1
            residuals.append((matching1, matching2, n1, p1, shape))

    require(len(residuals) == 270 and shapes == {
        "same_two_edge_tail": 90,
        "one_C4_tail_switch": 180,
    }, ("double-coloop residual census changed", len(residuals), shapes))

    # The hybrid word has colour 2 at S,n and colour 1 elsewhere.  Relative
    # to its selected matching term, the other 104 physical matchings split
    # universally as 14 retaining e, 15 using direct PS, and 75 omitting e
    # without PS.  The last class has a new off-diagonal S-arm.
    route_counts = Counter()
    all_matchings = tuple(normalize(matching)
                          for matching in landing.matchings(tuple(range(8))))
    examples = []
    for matching1, matching2, neighbour_s, neighbour_p, shape in residuals:
        e = tuple(sorted((S, neighbour_s)))
        require(e in matching1 and e in matching2,
                "hybrid edge stopped being common to both bright anchors")
        pure_anchors = set(matching1) | set(matching2) | {(P, S)}
        local = Counter()
        for mate in all_matchings:
            if mate == matching1:
                local["selected_seed"] += 1
            elif e in mate:
                local["retains_e_pure1_reselection"] += 1
            elif (P, S) in mate:
                local["mixed_direct_PS_forbidden"] += 1
            else:
                local["new_offdiagonal_S_arm"] += 1
                new_s = tuple(edge for edge in mate if S in edge)
                require(len(new_s) == 1 and new_s[0] not in pure_anchors,
                        ("avoiding mate failed to expose an external S arm",
                         matching1, matching2, mate))
        require(local == {
            "selected_seed": 1,
            "retains_e_pure1_reselection": 14,
            "mixed_direct_PS_forbidden": 15,
            "new_offdiagonal_S_arm": 75,
        }, ("hybrid mate partition changed", local))
        route_counts.update(local)
        if len(examples) < 2:
            examples.append({
                "shape": shape,
                "matching1": [list(edge) for edge in matching1],
                "matching2": [list(edge) for edge in matching2],
                "hybrid_edge": list(e),
                "mate_partition": dict(sorted(local.items())),
            })

    require(route_counts == {
        "selected_seed": 270,
        "retains_e_pure1_reselection": 3780,
        "mixed_direct_PS_forbidden": 4050,
        "new_offdiagonal_S_arm": 20250,
    }, ("aggregate hybrid routing changed", route_counts))

    return {
        "theorem": "double-coloop hybrid interference closure",
        "residual_packets": len(residuals),
        "residual_shapes": dict(sorted(shapes.items())),
        "per_packet_mate_partition": {
            "selected_seed": 1,
            "retains_e_pure1_reselection": 14,
            "mixed_direct_PS_forbidden": 15,
            "new_offdiagonal_S_arm": 75,
        },
        "aggregate_mate_routes": dict(sorted(route_counts.items())),
        "examples": examples,
        "identity": (
            "use the pure-2 cell on the common S arm and the three pure-1 "
            "cells on matching1.  The mixed coefficient is zero.  Avoiding "
            "mates expose an external off-diagonal S arm; if none exists, "
            "the pure-1 target coefficient forces a pure matching omitting "
            "the common S arm"
        ),
        "consequence": (
            "the 270 packets either re-enter selected-arm Cartan landing "
            "after pure-target reselection or enter the nonanchor rank-(3,3) "
            "active-minor route.  No double-coloop-specific activity case "
            "remains"
        ),
        "scope": (
            "this removes the last selected Cartan incidence packet as an "
            "independent branch.  The generic good-active-minor to clean/"
            "curved promotion and global uniform entry remain separate"
        ),
    }


def main():
    ledger = audit()
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("double-coloop hybrid ledger changed", digest))
    print("h3 order-six double-coloop hybrid interference: PASS")
    print("residual shapes:", ledger["residual_shapes"])
    print("per-packet mate routes:", ledger["per_packet_mate_partition"])
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
