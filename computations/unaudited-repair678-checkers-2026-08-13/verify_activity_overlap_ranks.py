#!/usr/bin/env python3
"""UNAUDITED REPAIR CANDIDATE (repair item 7): compute the overlap ranks.

Replaces the rank half of
``computations/verify_h3_physical_cartan_active_overlap_landing.py``.
That checker assigns

    rank_before = (2, 3)
    rank_after  = (3, 3)

as *literals* inside the branch and then asserts
``rank_after == (3,3) and rank_before in ((3,3),(2,3))`` -- two literals
compared to themselves.  No matrix is built and no rank is computed anywhere
in the file; negating the rank claim leaves its frozen digest byte-identical
(external audit 2026-08-13, CRITICAL defect 5).

THE MODEL, STATED EXPLICITLY.  The overlap cap is (P, u) for a target-full
internal site u.  Its endpoint quotient carries three *selected endpoint
heads*, one per colour: the unary pure-zero head e0 (carried by the direct
PS matching) and the two selected bright heads e1, e2 (carried by the two
selected bright matchings, matching1 in colour 1 and matching2 in colour 2).
Passing to the overlap cap at u deletes exactly those bright heads whose
S-arm is (S, u), i.e. head e_c is deleted iff u is the S-neighbour of the
colour-c selected bright matching.  Target-fullness of u is precisely the
statement that the inner u-star is rank three.  So, for each incidence
packet,

    outer(u)  = [e0] + [e1 if u != n1] + [e2 if u != n2]
    inner(u)  = [e0, e1, e2]
    arm(u)    = e1 if u == n1 else e2 if u == n2 else (no deleted arm)

    before    = (rank outer(u), rank inner(u))
    after     = (rank (outer(u) + arm(u)), rank (inner(u) + arm(u)))

This is exactly the linear model that
``verify_h3_post_ks_full_nine_overlap_visibility_reduction.audit_overlap_rank_
reduction`` and ``verify_h3_residual_q_order6_one_sided_overlap_landing_
target`` already build for the single canonical packet, and this checker
imports THEIR ``rank`` routine (exact Gaussian elimination over Q) rather
than reimplementing it.  The repair is that the ranks are now computed for
every one of the 461,700 incidence packets, including all 310,500 packets of
the selected-arm branch, instead of being typed in.

ORBIT ARGUMENT (verified, not assumed).  Let
``G = S6 x S2`` act on the packets: S6 relabels the six internal sites
(fixing P=6 and S=7) and S2 swaps the two selected bright colours, i.e. it
swaps (matching1, matching2) and simultaneously swaps the heads e1 <-> e2.
Both the branch classification and the rank data above are defined purely
from the G-equivariant incidence data (which of n1, n2 lie in the target-full
set, and whether n1 = n2), so they are constant on G-orbits.  This checker
computes the full orbit decomposition of the 461,700 packets by union-find
over the generators (0 1), (0 1 2 3 4 5), and the colour swap, and then
VERIFIES that branch and rank data are constant on every orbit.  Hence the
orbit representatives are a provably sufficient certificate -- but the
checker evaluates all 461,700 packets anyway and hashes the evaluation
stream, so the certificate is not merely representative.

Frozen ledger hashes: the per-orbit rank/branch table, the orbit-size
histogram, and a rolling content digest of the FULL 461,700-entry
(branch, before, after) evaluation stream in canonical packet order.

POSITIVE CONTROLS (run in the same process, must FAIL):
  1. fabricated bright inventory -- drop the direct-free condition, so the
     "bright" matchings include the ones using the direct PS pair;
  2. fabricated synchronization -- in the selected-arm branch, take the
     candidate site outside {n1, n2} instead of inside it, which is the
     precise geometric content of the target-full/bright synchronization
     theorem.  Then the overlap is already rank (3,3) before transport and
     the (2,3) -> (3,3) restoration claim is false.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
from itertools import combinations
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
P, S = 6, 7
INTERNAL = tuple(range(6))
ALL_SITES = tuple(range(8))
E0 = (Q(1), Q(0), Q(0))
E1 = (Q(0), Q(1), Q(0))
E2 = (Q(0), Q(0), Q(1))
HEAD = {0: E0, 1: E1, 2: E2}

PINS = {
    "computations/verify_h3_physical_cartan_active_overlap_landing.py":
        "8161ab2f2b1c8de0db01a358d0ed4aad5b48779d04355ef0fc16a186b92c8cbd",
    "computations/verify_h3_post_ks_full_nine_overlap_visibility_reduction.py":
        "3614315b855828d7b11b62d5d54f4642a7a5990f88ef662c2deca2224ad631dd",
    "computations/verify_h3_target_full_selected_anchor_overlap_synchronization.py":
        "2a985129813eb28ed102abc531ee3e83c03fb503f71c2aa721d1bd614d579f13",
    "computations/verify_h3_residual_q_order6_one_sided_overlap_landing_target.py":
        "8067fe309f363e21939a543fc37c005b54867391ca502e594762cb7d3617b9df",
}
EXPECTED_LEDGER_SHA256 = (
    "962f9d51f57acde38f22b959b0e32fface655f4f94a36167b4e57d5bdf2177e9"
)


class ControlDidNotFail(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def should_fail(label, thunk):
    try:
        thunk()
    except RuntimeError as failure:
        return {"control": label, "fired": True, "reason": str(failure)[:200]}
    raise ControlDidNotFail(("positive control did not fail", label))


def load(relative, name):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


# ---------------------------------------------------------------- geometry --

def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for position, second in enumerate(vertices[1:], start=1):
        remainder = vertices[1:position] + vertices[position + 1:]
        for tail in perfect_matchings(remainder):
            answer.append((tuple(sorted((first, second))),) + tail)
    return tuple(tuple(sorted(matching)) for matching in answer)


def neighbour(matching, site):
    for left, right in matching:
        if left == site:
            return right
        if right == site:
            return left
    raise RuntimeError(("site absent from matching", site, matching))


def internal_edges(matching):
    return tuple(edge for edge in matching
                 if edge[0] in INTERNAL and edge[1] in INTERNAL)


def bright_inventory(direct_free=True):
    direct = tuple(sorted((P, S)))
    return tuple(matching for matching in perfect_matchings(ALL_SITES)
                 if not direct_free or direct not in matching)


def full_sets():
    return tuple(frozenset(choice)
                 for size in range(2, len(INTERNAL) + 1)
                 for choice in combinations(INTERNAL, size))


# ------------------------------------------------------------------- ranks --

def make_rank(pinned_rank):
    cache = {}

    def ranked(columns):
        key = tuple(columns)
        if key not in cache:
            cache[key] = pinned_rank(list(key))
        return cache[key]

    return ranked, cache


def overlap_columns(site, neighbour1, neighbour2):
    """The three selected endpoint heads that survive at the overlap cap."""
    outer = [E0]
    if site != neighbour1:
        outer.append(E1)
    if site != neighbour2:
        outer.append(E2)
    inner = [E0, E1, E2]
    if site == neighbour1:
        arm = E1
    elif site == neighbour2:
        arm = E2
    else:
        arm = None
    return tuple(outer), tuple(inner), arm


# ------------------------------------------------------------------ census --

def census(ranked, bright, choose_outside_in_selected_branch=False):
    """Walk the complete selected-matching/target-full incidence inventory and
    COMPUTE the overlap ranks in every packet."""
    sets = full_sets()
    branches = Counter()
    rank_profiles = Counter()
    packet_stream = sha256()
    packets = 0
    per_orbit_key = {}
    occupied_arm = Counter()
    for index1, matching1 in enumerate(bright):
        neighbour1 = neighbour(matching1, S)
        tails1 = internal_edges(matching1)
        for index2, matching2 in enumerate(bright):
            neighbour2 = neighbour(matching2, S)
            for index3, target_full in enumerate(sets):
                selected_full = target_full & {neighbour1, neighbour2}
                if neighbour1 != neighbour2 and selected_full:
                    branch = "selected_target_full_arm_repairs_quotient"
                    if choose_outside_in_selected_branch:
                        outside = target_full - {neighbour1, neighbour2}
                        require(outside,
                                "fabricated synchronization has no outside "
                                "site in this packet")
                        site = min(outside)
                        selected_matching = matching1
                    elif neighbour1 in target_full:
                        site = neighbour1
                        selected_matching = matching1
                    else:
                        site = neighbour2
                        selected_matching = matching2
                    tails = internal_edges(selected_matching)
                    require(len(tails) == 2
                            and all(site not in edge for edge in tails),
                            "selected target-full arm lost its two cofactors")
                    tail = tails[0]
                else:
                    outside = target_full - {neighbour1, neighbour2}
                    require(outside,
                            "unresolved incidence packet lost an outside site")
                    site = min(outside)
                    tails = tuple(edge for edge in tails1 if site not in edge)
                    require(tails, "rank-three branch lost a selected cofactor")
                    tail = tails[0]
                    selected_matching = matching1
                    branch = ("shared_bright_neighbour_activity_not_forced"
                              if neighbour1 == neighbour2 else
                              "full_set_avoids_bright_neighbours_activity_"
                              "not_forced")

                # ---- the ranks, actually computed ----------------------
                outer, inner, arm = overlap_columns(site, neighbour1,
                                                    neighbour2)
                before = (ranked(outer), ranked(inner))
                if arm is None:
                    after = before
                else:
                    after = (ranked(outer + (arm,)), ranked(inner + (arm,)))

                arm_edge = tuple(sorted((S, site)))
                selected_edges = {tuple(sorted(edge))
                                  for edge in selected_matching}
                occupied_arm[arm_edge in selected_edges] += 1
                require(tail in selected_edges and site not in tail,
                        "physical face lost its selected tail candidate")

                branches[branch] += 1
                rank_profiles[(branch, before, after)] += 1
                packet_stream.update(
                    f"{index1}|{index2}|{index3}|{branch}|"
                    f"{before[0]},{before[1]}|{after[0]},{after[1]}\n".encode()
                )
                key = (branch, before, after)
                per_orbit_key[(index1, index2, index3)] = key
                packets += 1
    return {
        "packets": packets,
        "branches": branches,
        "rank_profiles": rank_profiles,
        "evaluation_stream_sha256": packet_stream.hexdigest(),
        "packet_keys": per_orbit_key,
        "occupied_arm": occupied_arm,
    }


# ------------------------------------------------------------------ orbits --

def orbit_decomposition(bright, packet_keys):
    """Union-find over the generators of G = S6 x S2 on the packet set, then
    verify that the computed branch/rank data is constant on every orbit."""
    sets = full_sets()
    set_index = {value: index for index, value in enumerate(sets)}
    bright_index = {matching: index for index, matching in enumerate(bright)}
    size1, size3 = len(bright), len(sets)

    def relabel_matching(matching, permutation):
        mapping = dict(zip(INTERNAL, permutation))
        mapping[P] = P
        mapping[S] = S
        return tuple(sorted(tuple(sorted((mapping[left], mapping[right])))
                            for left, right in matching))

    generators = []
    for permutation in ((1, 0, 2, 3, 4, 5), (1, 2, 3, 4, 5, 0)):
        matching_map = tuple(bright_index[relabel_matching(matching,
                                                           permutation)]
                             for matching in bright)
        set_map = tuple(set_index[frozenset(permutation[site]
                                            for site in value)]
                        for value in sets)
        generators.append(("internal_" + "".join(map(str, permutation)),
                           matching_map, set_map))

    parent = list(range(size1 * size1 * size3))

    def find(node):
        while parent[node] != node:
            parent[node] = parent[parent[node]]
            node = parent[node]
        return node

    def union(left, right):
        left, right = find(left), find(right)
        if left != right:
            parent[left] = right

    for index1 in range(size1):
        base1 = index1 * size1 * size3
        for index2 in range(size1):
            base = base1 + index2 * size3
            # colour swap: exchange the two selected bright matchings
            swapped = index2 * size1 * size3 + index1 * size3
            for index3 in range(size3):
                union(base + index3, swapped + index3)
            for _label, matching_map, set_map in generators:
                image = (matching_map[index1] * size1 * size3
                         + matching_map[index2] * size3)
                for index3 in range(size3):
                    union(base + index3, image + set_map[index3])

    orbits = {}
    for index1 in range(size1):
        for index2 in range(size1):
            for index3 in range(size3):
                node = index1 * size1 * size3 + index2 * size3 + index3
                root = find(node)
                key = packet_keys[(index1, index2, index3)]
                if root not in orbits:
                    orbits[root] = [key, 0, (index1, index2, index3)]
                require(orbits[root][0] == key,
                        ("branch/rank data is not constant on a G-orbit",
                         orbits[root][2], (index1, index2, index3),
                         orbits[root][0], key))
                orbits[root][1] += 1
    return orbits


# ------------------------------------------------------------------- audit --

def audit():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual))
    overlap = load(
        "computations/verify_h3_post_ks_full_nine_overlap_visibility_reduction.py",
        "activity_overlap_rank_engine",
    )
    ranked, cache = make_rank(overlap.rank)

    # Sanity-tie the imported rank routine to the one canonical packet the
    # committed one-sided landing target already checks.
    require(ranked((E0, E2)) == 2 and ranked((E0, E1, E2)) == 3
            and ranked((E0, E2, E1)) == 3,
            "the pinned overlap rank routine changed behaviour")

    bright = bright_inventory()
    sets = full_sets()
    require(len(bright) == 90 and len(sets) == 57,
            ("landing inventory changed", len(bright), len(sets)))

    result = census(ranked, bright)
    require(result["packets"] == 90 * 90 * 57 == 461_700,
            ("landing census changed", result["packets"]))
    require(dict(result["branches"]) == {
        "selected_target_full_arm_repairs_quotient": 310_500,
        "shared_bright_neighbour_activity_not_forced": 76_950,
        "full_set_avoids_bright_neighbours_activity_not_forced": 74_250,
    }, ("physical landing branches changed", dict(result["branches"])))
    require(result["occupied_arm"][True] and result["occupied_arm"][False],
            "the theorem stopped auditing both occupied and new directions")

    # THE REPAIRED CLAIM: the rank profiles are computed, not typed in.
    profiles = {}
    for (branch, before, after), count in result["rank_profiles"].items():
        profiles.setdefault(branch, {})[
            f"{list(before)}->{list(after)}"] = count
    require(profiles["selected_target_full_arm_repairs_quotient"]
            == {"[2, 3]->[3, 3]": 310_500},
            ("the selected-arm branch is no longer uniformly (2,3)->(3,3)",
             profiles["selected_target_full_arm_repairs_quotient"]))
    require(profiles["shared_bright_neighbour_activity_not_forced"]
            == {"[3, 3]->[3, 3]": 76_950},
            ("the shared-neighbour branch left rank (3,3)",
             profiles["shared_bright_neighbour_activity_not_forced"]))
    require(profiles["full_set_avoids_bright_neighbours_activity_not_forced"]
            == {"[3, 3]->[3, 3]": 74_250},
            ("the avoidance branch left rank (3,3)",
             profiles["full_set_avoids_bright_neighbours_activity_not_forced"]))

    orbits = orbit_decomposition(bright, result["packet_keys"])
    orbit_table = []
    for _root, (key, size, representative) in sorted(
            orbits.items(), key=lambda item: (item[1][0], item[1][2])):
        branch, before, after = key
        orbit_table.append({
            "representative_packet": list(representative),
            "orbit_size": size,
            "branch": branch,
            "rank_before": list(before),
            "rank_after": list(after),
        })
    require(sum(record["orbit_size"] for record in orbit_table) == 461_700,
            "orbit sizes stopped covering the census")
    orbit_histogram = Counter(record["orbit_size"] for record in orbit_table)

    return {
        "theorem": ("the physical Cartan overlap landing ranks, computed on "
                    "every incidence packet"),
        "bright_matchings": len(bright),
        "target_full_sets": len(sets),
        "audited_matching_packets": result["packets"],
        "branches": dict(sorted(result["branches"].items())),
        "computed_rank_profiles": {branch: dict(sorted(table.items()))
                                   for branch, table in sorted(profiles.items())},
        "selected_arm_packets_with_computed_2_3_to_3_3": 310_500,
        "distinct_rank_inputs_evaluated": len(cache),
        "rank_input_table": sorted(
            (repr([[str(entry) for entry in column] for column in key]), value)
            for key, value in cache.items()
        ),
        "orbit_group": "S6 (internal relabelling) x S2 (bright colour swap)",
        "orbit_count": len(orbit_table),
        "orbit_size_histogram": dict(sorted(orbit_histogram.items())),
        "orbits": orbit_table,
        "full_evaluation_stream_sha256": result["evaluation_stream_sha256"],
        "arm_current_support": {
            "occupied": result["occupied_arm"][True],
            "new_physical_direction": result["occupied_arm"][False],
        },
        "reading": (
            "310,500 packets are closed by an actually computed rank "
            "restoration (2,3) -> (3,3); the remaining 151,200 packets sit "
            "at (3,3) -> (3,3) before and after transport, so the residual "
            "activity question is untouched by this repair"
        ),
        "scope": (
            "the linear overlap model pinned by the post-KS visibility "
            "reduction: three selected endpoint heads, deletion of the head "
            "whose S-arm is the chosen candidate, target-full inner star of "
            "rank three.  It does not prove nonvanishing of the Cartan "
            "quadratic coefficient on an already rank-(3,3) overlap"
        ),
    }


def controls():
    overlap = load(
        "computations/verify_h3_post_ks_full_nine_overlap_visibility_reduction.py",
        "activity_overlap_rank_control_engine",
    )
    ranked, _cache = make_rank(overlap.rank)
    fired = []

    def fabricated_bright_inventory():
        bright = bright_inventory(direct_free=False)
        require(len(bright) == 90,
                "fabricated inventory changed size before the census")
        result = census(ranked, bright)
        require(dict(result["branches"]) == {
            "selected_target_full_arm_repairs_quotient": 310_500,
            "shared_bright_neighbour_activity_not_forced": 76_950,
            "full_set_avoids_bright_neighbours_activity_not_forced": 74_250,
        }, "fabricated non-direct-free inventory reproduced the branch census")

    def fabricated_synchronization():
        bright = bright_inventory()
        result = census(ranked, bright,
                        choose_outside_in_selected_branch=True)
        selected = {key: value for key, value
                    in result["rank_profiles"].items()
                    if key[0] == "selected_target_full_arm_repairs_quotient"}
        require(set(selected) == {
            ("selected_target_full_arm_repairs_quotient", (2, 3), (3, 3))
        }, ("fabricated synchronization still produced the (2,3)->(3,3) "
            "restoration", sorted(map(repr, selected))))

    fired.append(should_fail("fabricated bright inventory (direct PS pair "
                             "allowed)", fabricated_bright_inventory))
    fired.append(should_fail("fabricated target-full synchronization "
                             "(candidate taken outside {n1,n2})",
                             fabricated_synchronization))
    return fired


def main():
    control_records = controls()
    ledger = audit()
    ledger["positive_controls"] = [
        {"control": record["control"], "fired": record["fired"]}
        for record in control_records
    ]
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("activity overlap rank ledger changed", digest))
    print("repair678 activity overlap ranks: PASS")
    print("packets:", ledger["audited_matching_packets"])
    print("computed rank profiles:", ledger["computed_rank_profiles"])
    print("G-orbits:", ledger["orbit_count"],
          "sizes:", ledger["orbit_size_histogram"])
    print("full evaluation stream sha256:",
          ledger["full_evaluation_stream_sha256"])
    for record in control_records:
        print("positive control fired:", record["control"])
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
