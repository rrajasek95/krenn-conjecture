#!/usr/bin/env python3
"""Independent conditional exhaustion ledger for the X5 zero-tail packet.

This audit reconstructs the 1,638 source-label partition and independently
re-enumerates the complete 275,568-record Boolean survivor universe and its
310 B4 x S3 orbits.  It then validates the exact 0,7,25 Laurent closure and
exports a strict acceptance contract for the independently owned 0,30,45
closure.

Important scope: the 310 records are exact *minimal-support* strata.  Closing
both Q geometries exhausts those strata.  Promotion to the whole e=t=0,
H-live component additionally requires a degeneration/initial-ideal (or
larger-support exclusion) lemma, which is not present in the frozen inputs.
"""

from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ROUTING = (ROOT / "computations" /
    "unaudited-codex-x5-zero-tail-routing-2026-08-21" /
    "results_x5_zero_tail_routing.json")
EXTENSION_422 = (ROOT / "computations" /
    "unaudited-codex-x5-zero-tail-routing-2026-08-21" /
    "results_422_nonpairconstant_extension.json")
ASSEMBLY = HERE / "results_extended_diagonal_packet_support_shadow.json"
PACKET = HERE / "extended_diagonal_packet_1566.json"
CLOSURE_0725 = HERE / "results_q_geometry_0_7_25_laurent_closure.json"
PENDING_03045 = (ROOT / "computations" /
    "unaudited-codex-x5-zero-tail-class-03045-2026-08-21" /
    "results_class_03045_exact_branches.json")
OUT = HERE / "results_zero_tail_exhaustion_ledger.json"

PAIRING = ((0, 1), (2, 3), (4, 5), (6, 7))
SUPER_EDGES = tuple(combinations(range(4), 2))
EDGE_INDEX = {edge: index for index, edge in enumerate(SUPER_EDGES)}
COMPLEMENTARY_EDGE_PAIRS = (((0, 1), (2, 3)),
                            ((0, 2), (1, 3)),
                            ((0, 3), (1, 2)))
EXPECTED_0725_LOGICAL = \
    "dbaed76c449aa872227e0e8f67ed311fb3ebc87723f082197c229e4f5cb0271d"
EXPECTED_03045_LOGICAL = \
    "6bdee0c2a402e1d30dae17ef2f769e7bfac6685883cc48bb157962b310454327"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def file_sha(path):
    return sha256(path.read_bytes()).hexdigest()


def logical_sha(payload):
    return sha256(json.dumps(payload, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


def vertex_actions():
    actions = set()
    for block_permutation in permutations(range(4)):
        for flips in product((0, 1), repeat=4):
            actions.add(tuple(
                2*block_permutation[vertex//2]
                + ((vertex % 2) ^ flips[vertex//2])
                for vertex in range(8)))
    require(len(actions) == 384, "B4 order changed")
    return tuple(sorted(actions))


def act_word(label, vertex_action, colour_permutation):
    old = tuple(map(int, label))
    new = [None]*8
    for vertex, colour in enumerate(old):
        new[vertex_action[vertex]] = colour_permutation[colour]
    return "".join(map(str, new))


def word_orbit(label, actions):
    return frozenset(act_word(label, action, colour_permutation)
                     for action in actions
                     for colour_permutation in permutations(range(3)))


def profile(label):
    counts = sorted(Counter(label).values(), reverse=True)
    return "+".join(map(str, counts + [0]*(3-len(counts))))


def packet_ledger():
    routing = json.loads(ROUTING.read_text())
    extension = json.loads(EXTENSION_422.read_text())
    packet = json.loads(PACKET.read_text())
    actions = vertex_actions()
    orbit_rows = []
    all_labels = set()
    for row in routing["routing_table"]:
        computed = word_orbit(row["canonical_word"], actions)
        frozen = frozenset(row["literal_source_labels"])
        require(computed == frozen and len(computed) == row["literal_row_count"],
                ("source word orbit changed", row["canonical_word"]))
        require(not (all_labels & frozen),
                ("source word orbits overlap", row["canonical_word"]))
        all_labels |= frozen
        orbit_rows.append({
            "canonical_word": row["canonical_word"],
            "orbit": row["orbit"],
            "orbit_size": len(computed),
            "labels_sha256": row["labels_sha256"],
        })
    require(len(orbit_rows) == 10 and len(all_labels) == 1638,
            "ten-orbit/1638 source census changed")

    classification = {row["orbit"]: row["classification"]
                      for row in extension["orbit_records"]}
    omitted_orbits = {name for name, status in classification.items()
                      if status == "REDUNDANT_exact_e_multiple"}
    require(omitted_orbits == {
        "422_two_majority_loops_two_minor_cross_edges"},
        "omitted e-multiple orbit changed")
    omitted_labels = set(next(row["literal_source_labels"]
                              for row in routing["routing_table"]
                              if row["orbit"] in omitted_orbits))
    explicit_labels = {row["label"] for row in packet["explicit_rows"]}
    require(len(explicit_labels) == 1566 and len(omitted_labels) == 72 and
            not explicit_labels & omitted_labels and
            explicit_labels | omitted_labels == all_labels,
            "1566+72 disjoint source partition changed")
    require(Counter(profile(label) for label in explicit_labels) == {
        "6+2+0": 168, "4+4+0": 210, "4+2+2": 1188},
        "explicit profile census changed")

    # Every omitted majority four-set is exactly two anchor pairs, the
    # combinatorial antecedent of the frozen e*X*X quotient identity.
    for label in omitted_labels:
        word = tuple(map(int, label))
        majority = next(colour for colour in range(3)
                        if word.count(colour) == 4)
        sites = {site for site, colour in enumerate(word)
                 if colour == majority}
        anchor_pairs = [pair for pair in PAIRING if set(pair) <= sites]
        require(len(anchor_pairs) == 2 and
                sites == set(anchor_pairs[0] + anchor_pairs[1]),
                ("omitted row lost e-factor", label))
    return {
        "B4_order": len(actions),
        "colour_group_order": 6,
        "B4_times_S3_order": len(actions)*6,
        "source_orbits": orbit_rows,
        "source_orbit_count": len(orbit_rows),
        "all_nontrivial_zero_tail_rows": len(all_labels),
        "explicit_rows": len(explicit_labels),
        "exact_e_multiple_rows": len(omitted_labels),
        "partition_identity": "1638=1566+72",
        "explicit_profile_counts": {
            "6+2+0": 168, "4+4+0": 210, "4+2+2": 1188},
        "literal_orbit_replay": True,
        "omitted_anchor_union_test": True,
    }


def cut_mask(bits):
    return sum((((bits >> left) & 1) ^ ((bits >> right) & 1)) << index
               for index, (left, right) in enumerate(SUPER_EDGES))


CUT_MASKS = tuple(sorted({cut_mask(bits) for bits in range(16)}))


def compatible_422(q_cut, left_x, right_x):
    for first, second in COMPLEMENTARY_EDGE_PAIRS:
        i, j = EDGE_INDEX[first], EDGE_INDEX[second]
        if (((left_x >> i) & 1) == ((q_cut >> i) & 1) and
                ((right_x >> j) & 1) == ((q_cut >> j) & 1)):
            return False
        if (((left_x >> j) & 1) == ((q_cut >> j) & 1) and
                ((right_x >> i) & 1) == ((q_cut >> i) & 1)):
            return False
    return True


def enumerate_survivors():
    require(len(CUT_MASKS) == 8, "Q cut-mask census changed")
    allowed = {
        q_cut: tuple(sum(1 << right for right in range(64)
                         if compatible_422(q_cut, left, right))
                     for left in range(64))
        for q_cut in CUT_MASKS
    }
    survivors = set()
    completion_histogram = Counter()
    for q_cuts in permutations(CUT_MASKS, 3):
        count = 0
        for x0 in range(64):
            for x1 in range(64):
                if not compatible_422(q_cuts[2], x0, x1):
                    continue
                possible = allowed[q_cuts[0]][x1] & allowed[q_cuts[1]][x0]
                while possible:
                    low = possible & -possible
                    x2 = low.bit_length()-1
                    possible -= low
                    survivors.add((q_cuts, (x0, x1, x2)))
                    count += 1
        completion_histogram[count] += 1
    require(len(survivors) == 275568 and
            completion_histogram == {735: 288, 1331: 48},
            ("Boolean survivor enumeration changed", len(survivors),
             completion_histogram))
    return survivors, completion_histogram


def transform_mask(mask, permutation, flip_mask):
    answer = 0
    for index, (left, right) in enumerate(SUPER_EDGES):
        bit = ((mask >> index) & 1) ^ ((flip_mask >> left) & 1) ^ \
              ((flip_mask >> right) & 1)
        image = tuple(sorted((permutation[left], permutation[right])))
        answer |= bit << EDGE_INDEX[image]
    return answer


def act_state(state, permutation, flip_mask, colour_permutation):
    q_cuts, x_masks = state
    new_q, new_x = [None]*3, [None]*3
    for colour in range(3):
        image_colour = colour_permutation[colour]
        new_q[image_colour] = transform_mask(q_cuts[colour], permutation,
                                             flip_mask)
        new_x[image_colour] = transform_mask(x_masks[colour], permutation,
                                             flip_mask)
    return tuple(new_q), tuple(new_x)


STATE_ACTIONS = tuple((permutation, flip_mask, colour_permutation)
                      for permutation in permutations(range(4))
                      for flip_mask in range(16)
                      for colour_permutation in permutations(range(3)))


def state_orbit(state):
    return frozenset(act_state(state, *action) for action in STATE_ACTIONS)


def shadow_ledger():
    assembly = json.loads(ASSEMBLY.read_text())
    frozen = assembly["support_shadow"][
        "minimal_surviving_support_signature_antichain"]
    require(len(frozen) == 310, "frozen support orbit count changed")
    survivors, completion_histogram = enumerate_survivors()
    reconstructed = set()
    geometry_counts = Counter()
    orbit_size_histogram = Counter()
    for row in frozen:
        state = (
            tuple(row["q_pair_cut_masks_e01_e02_e03_e12_e13_e23"]),
            tuple(row["x_relation_masks_e01_e02_e03_e12_e13_e23"]),
        )
        orbit = state_orbit(state)
        require(state == min(orbit), ("noncanonical state", state))
        require(len(orbit) == row["orbit_size"],
                ("state orbit size changed", state, len(orbit),
                 row["orbit_size"]))
        require(not (reconstructed & orbit), ("state orbit overlap", state))
        reconstructed |= orbit
        geometry_counts[state[0]] += 1
        orbit_size_histogram[len(orbit)] += 1
    require(reconstructed == survivors,
            ("frozen orbit list does not exhaust reconstructed survivors",
             len(reconstructed), len(survivors),
             len(reconstructed-survivors), len(survivors-reconstructed)))
    require(geometry_counts == {(0, 7, 25): 224, (0, 30, 45): 86},
            ("Q geometry split changed", geometry_counts))
    return {
        "cut_masks": list(CUT_MASKS),
        "ordered_distinct_Q_cut_triples": 336,
        "labelled_survivors": len(survivors),
        "local_completion_histogram": {
            str(count): multiplicity for count, multiplicity
            in sorted(completion_histogram.items())},
        "B4_times_S3_support_orbits": len(frozen),
        "q_geometry_refinement_counts": {
            "0,7,25": geometry_counts[(0, 7, 25)],
            "0,30,45": geometry_counts[(0, 30, 45)],
        },
        "orbit_size_histogram": {
            str(size): count for size, count
            in sorted(orbit_size_histogram.items())},
        "orbit_union_equals_reconstructed_survivor_universe": True,
    }


def validate_0725():
    closure = json.loads(CLOSURE_0725.read_text())
    require(closure["logical_sha256"] == EXPECTED_0725_LOGICAL,
            "0,7,25 logical digest changed")
    require(closure["input_geometry"] == {
        "q_cut_masks": [0, 7, 25],
        "support_orbits": 224,
        "labelled_minimal_supports": 211680,
    }, "0,7,25 input geometry changed")
    tri = closure["triangle_support_filter"]
    require((tri["support_orbits_rejected_by_constant_minus_two_t_row"],
             tri["surviving_support_orbits"]) == (220, 4),
            "0,7,25 triangle partition changed")
    records = closure["Laurent_closure_records"]
    require(len(records) == 4 and all(not row["realizable"] for row in records),
            "0,7,25 Laurent closure count changed")
    root_branches = 0
    root_orbits = 0
    support_orbits = tri["support_orbits_rejected_by_constant_minus_two_t_row"]
    for row in records:
        require(row["three_colour_root_branches"] == 216 and
                row["H_values_on_every_root_branch"] == [4, 4, 4] and
                row["uniform_killer"]["nonzero_on_all_root_branches"],
                ("0,7,25 root/sign coverage changed",
                 row["x_relation_masks"]))
        histogram = row["root_branch_orbit_size_histogram"]
        require(sum(int(size)*count for size, count in histogram.items()) == 216,
                ("root/sign stabilizer quotient dropped a branch",
                 row["x_relation_masks"], histogram))
        root_branches += 216
        root_orbits += row["root_branch_orbits_under_support_stabilizer"]
        support_orbits += 1
    require(support_orbits == 224 and root_branches == 864 and
            root_orbits == 202,
            "0,7,25 total support/root coverage changed")
    return {
        "logical_sha256": closure["logical_sha256"],
        "support_orbits_closed": support_orbits,
        "triangle_unit_orbits": 220,
        "Laurent_support_orbits": len(records),
        "exact_root_branches_replayed": root_branches,
        "root_branch_stabilizer_orbits": root_orbits,
        "all_H_values": [4, 4, 4],
        "all_unrealizable": True,
    }


def validate_03045(path):
    data = json.loads(path.read_text())
    require(data["status"] ==
            "PASS exact class-0,30,45 Laurent branch inconsistency",
            "0,30,45 status contract failed")
    require(data["support_refinements"] == 86,
            "0,30,45 support-refinement contract failed")
    require(data["theorem"] ==
            "No minimal support refinement in the Q-geometry 0,30,45 is "
            "realizable by an H-live e=t=0 point satisfying the full "
            "1,638-row diagonal packet over Qbar.",
            "0,30,45 theorem/scope contract failed")
    proof = data["proof_structure"]
    require("84 support orbits" in proof and
            "remaining two" in proof and "216 combined branches" in proof,
            "0,30,45 support/sign coverage contract failed")
    digest = data["logical_sha256"]
    require(digest == EXPECTED_03045_LOGICAL,
            "0,30,45 terminal logical digest changed")
    return {
        "status": "absorbed_and_validated",
        "path": str(path.relative_to(ROOT)),
        "file_sha256": file_sha(path),
        "logical_sha256": digest,
        "support_orbits_closed": 86,
        "triangle_unit_orbits": 84,
        "Laurent_support_orbits": 2,
        "exact_root_branches_per_Laurent_orbit": 216,
        "all_unrealizable": True,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--check-results", action="store_true")
    parser.add_argument("--absorb-03045", type=Path)
    args = parser.parse_args()

    packet = packet_ledger()
    shadow = shadow_ledger()
    closure_0725 = validate_0725()
    closure_03045 = ({
        "status": "pending_independent_cycle_lane_digest",
        "expected_path": str(PENDING_03045.relative_to(ROOT)),
        "acceptance_contract": {
            "status": "PASS exact class-0,30,45 Laurent branch inconsistency",
            "support_refinements": 86,
            "triangle_unit_orbits": 84,
            "Laurent_support_orbits": 2,
            "exact_root_branches_per_Laurent_orbit": 216,
            "theorem_scope": "minimal support refinements only",
        },
    } if args.absorb_03045 is None else
        validate_03045(args.absorb_03045.resolve()))
    minimal_complete = closure_03045["status"] == "absorbed_and_validated"

    result = {
        "status": ("PASS exact minimal-support zero-tail exhaustion ledger"
                   if minimal_complete else
                   "PASS conditional zero-tail exhaustion ledger; 0,30,45 pending"),
        "packet_exhaustion": packet,
        "support_shadow_exhaustion": shadow,
        "exact_geometry_closures": {
            "0,7,25": closure_0725,
            "0,30,45": closure_03045,
        },
        "conditional_theorem": {
            "minimal_support_statement": (
                "Once a result satisfying the frozen 0,30,45 acceptance "
                "contract is absorbed, all 310 B4 x S3 minimal-support "
                "orbits of the full 1,638-row e=t=0, H-live diagonal packet "
                "are unrealizable over Qbar."),
            "minimal_support_complete": minimal_complete,
            "whole_e0_component_statement": (
                "Closure of 0,30,45 suffices for the entire e=0 component "
                "only conditional on an additional theorem that every "
                "H-live e=t=0 point either lies on an exact minimal-support "
                "stratum or specializes/degenerates to one while preserving "
                "the full source packet and H-localization."),
            "whole_e0_component_complete": False,
            "missing_bridge": (
                "support-minimal degeneration/initial-ideal lemma, or an "
                "independent exact exclusion of all larger-support strata"),
        },
        "scope_audit": {
            "assembly_scope": "inclusion-minimal Boolean support shadow",
            "coefficient_closure_scope": "exact minimal Laurent support strata",
            "forbidden_inference": (
                "An exact obstruction on a smaller support is not monotone "
                "under adjoining live entries or Q coordinates; coefficient "
                "cancellations can change."),
            "full_e0_promotion_present_in_inputs": False,
        },
        "hostile_mutation_guards": {
            "replace_1638_by_1637": True,
            "replace_1566_plus_72_by_1565_plus_73": True,
            "drop_one_of_ten_source_orbits": True,
            "replace_310_by_309": True,
            "replace_224_plus_86_by_225_plus_85": True,
            "replace_275568_survivors_by_275567": True,
            "mutate_local_completion_histogram": True,
            "mutate_any_B4_times_S3_word_or_state_orbit_size": True,
            "change_0725_logical_digest": True,
            "replace_220_plus_4_by_219_plus_5": True,
            "drop_one_of_864_0725_root_branches": True,
            "drop_one_of_202_0725_root_stabilizer_orbits": True,
            "absorb_03045_without_exact_theorem_scope_match": True,
            "promote_minimal_support_closure_to_whole_e0_without_bridge": True,
        },
        "source_hashes": {
            str(path.relative_to(ROOT)): file_sha(path)
            for path in (ROUTING, EXTENSION_422, ASSEMBLY, PACKET,
                         CLOSURE_0725)
        },
    }
    result["logical_sha256"] = logical_sha(result)
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.write_results:
        OUT.write_text(text)
    if args.check_results:
        require(OUT.read_text() == text, "frozen ledger replay mismatch")
    print(json.dumps({
        "status": result["status"],
        "packet_rows": packet["all_nontrivial_zero_tail_rows"],
        "support_orbits": shadow["B4_times_S3_support_orbits"],
        "geometry_split": shadow["q_geometry_refinement_counts"],
        "closure_0725": closure_0725["support_orbits_closed"],
        "closure_03045": closure_03045["status"],
        "whole_e0_component_complete": False,
        "logical_sha256": result["logical_sha256"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
