#!/usr/bin/env python3
"""Exact B4 routing census for every proper k5/k6 c=0 boundary.

This is combinatorics only.  It independently reconstructs the 729 labelled
ternary states and the simultaneous B4 action, verifies the frozen 66-orbit
interface, and classifies all nonempty zero-c subsets of the branch0 k5 and
k6 starts.  No polynomial solve is run.
"""

from __future__ import annotations

from collections import Counter, defaultdict, deque
from hashlib import sha256
from itertools import permutations, product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
FACE_DIR = (HERE.parent /
            "unaudited-codex-branch0-offdiag-support-strata-2026-08-21")
FROZEN_GRAPH = FACE_DIR / "results_recursive_joint_face_interface.json"
FROZEN_BUILDER = FACE_DIR / "build_recursive_joint_face_interface.py"
EASY = (HERE.parent / "unaudited-codex-root-integration-2026-08-20" /
        "results_branch0_both_live_easy_strata.json")
ALIGNED = (HERE.parent / "unaudited-codex-orbit0-t2-radical-2026-08-20" /
           "results_joint_aligned_zero_chart_census.json")
CYCLE_EXACT = FACE_DIR / "results_recursive_face_exact_units.json"
TP_P26 = HERE.parent / "unaudited-codex-tp-p26-boundary-char0-2026-08-21"
OUT = HERE / "results_k56_recursive_boundary_routing.json"
EDGES = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}
ACTIONS = tuple((switches, permutation)
                for switches in product((0, 1), repeat=4)
                for permutation in permutations(range(4)))
STARTS = {"k5": (0, 63, 31), "k6": (0, 63, 63)}
SUPPORT_NAMES = {15: "triangle_plus_pendant", 30: "four_cycle",
                 31: "K4_minus_one_edge", 63: "K4"}


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def file_sha(path):
    return sha256(path.read_bytes()).hexdigest()


def state_key(state):
    return ":".join(map(str, state))


def edge_list(mask):
    return [edge for edge in range(6) if mask >> edge & 1]


def act_mask(mask, switches, permutation, toggle):
    answer = 0
    for index, (left, right) in enumerate(EDGES):
        bit = (mask >> index) & 1
        if toggle:
            bit ^= switches[left] ^ switches[right]
        target = EDGE_INDEX[tuple(sorted((permutation[left],
                                          permutation[right])))]
        answer |= bit << target
    return answer


def act_state(state, action):
    branch, term, full = state
    switches, permutation = action
    return (act_mask(branch, switches, permutation, True),
            act_mask(term, switches, permutation, True),
            act_mask(full, switches, permutation, False))


def canonical_with_witness(state):
    candidates = [(act_state(state, action), index, action)
                  for index, action in enumerate(ACTIONS)]
    transformed, index, action = min(candidates,
                                     key=lambda item: (item[0], item[1]))
    require(act_state(state, action) == transformed,
            "covariance witness failed")
    return transformed, index, action


def canonical(state):
    return canonical_with_witness(state)[0]


def all_initial_states():
    answer = []
    # Per edge: offdiagonal-only, both-live, diagonal-only.
    for types in product(range(3), repeat=6):
        term = sum((kind != 2) << edge
                   for edge, kind in enumerate(types))
        full = sum((kind == 1) << edge
                   for edge, kind in enumerate(types))
        answer.append((0, term, full))
    require(len(answer) == 729 and len(set(answer)) == 729,
            "labelled ternary state census changed")
    return tuple(answer)


def transitions(state):
    branch, term, full = state
    return tuple(sorted({canonical((branch, term ^ (1 << edge),
                                    full ^ (1 << edge)))
                         for edge in edge_list(full)}))


def reachable(start, transition_map):
    seen = {start}
    queue = deque([start])
    while queue:
        current = queue.popleft()
        for target in transition_map[current]:
            if target not in seen:
                seen.add(target)
                queue.append(target)
    return seen


def every_nonempty_subset(mask):
    subset = mask
    while subset:
        yield subset
        subset = (subset - 1) & mask


def classify(key, aligned_units, easy_keys, cycle_keys):
    state = tuple(map(int, key.split(":")))
    branch, term, full = state
    if full == 0 and (branch, term) in aligned_units:
        return {
            "status": "exact_closed_aligned_unit",
            "reference": "50-orbit aligned exact-Q unit census",
            "reference_key": f"{branch}:{term}",
        }
    if state in easy_keys:
        return {
            "status": "exact_closed_easy_support_stratum",
            "reference": "branch0 exact k<=3 broad stratum",
            "reference_key": key,
        }
    if state in cycle_keys:
        return {
            "status": "exact_pairwise_closed_cycle_boundary",
            "reference": "four exact/pairwise cycle boundary types",
            "reference_key": key,
        }
    return {
        "status": "genuinely_new_joint_face_residual",
        "reference": None,
        "reference_key": None,
    }


def main():
    HERE.mkdir(parents=True, exist_ok=True)
    require(len(ACTIONS) == 384, "B4 action count changed")
    labelled = all_initial_states()
    representatives = sorted({canonical(state) for state in labelled},
                             key=lambda state: (state[2].bit_count(), state))
    require(len(representatives) == 66 and
            Counter(state[2].bit_count() for state in representatives) ==
            {0: 11, 1: 14, 2: 18, 3: 14, 4: 6, 5: 2, 6: 1},
            "independent 66-orbit census changed")
    transition_map = {state: transitions(state) for state in representatives}

    frozen = json.loads(FROZEN_GRAPH.read_text())
    frozen_records = {record["key"]: record for record in frozen["records"]}
    require(frozen["labelled_state_count"] == 729 and
            frozen["joint_orbit_count"] == 66 and
            frozen["result_sha256"] ==
            "a3a6fbc330aa06791417a3c06e1779de7c15b070ca734b657f4ed0c9b1311ac7",
            "frozen recursive graph header changed")
    require(set(frozen_records) == {state_key(state) for state in representatives},
            "frozen/rebuilt canonical key sets differ")
    for state in representatives:
        record = frozen_records[state_key(state)]
        require(record["orbit_size"] ==
                len({act_state(state, action) for action in ACTIONS}) and
                record["boundary_targets"] ==
                [state_key(target) for target in transition_map[state]],
                f"frozen covariance/transition mismatch at {state}")

    aligned = json.loads(ALIGNED.read_text())
    aligned_units = set()
    aligned_unit_records = {}
    for record in aligned["records"]:
        if record["statuses"]["0"] == "UNIT":
            key = (record["branch_mask"], record["permanent_term_mask"])
            aligned_units.add(key)
            aligned_unit_records[key] = {
                "joint_orbit_size": record["joint_orbit_size"],
                "exact_multiplier_ledger_sha256":
                    record["exact_lift"]["multiplier_ledger_sha256"],
            }
    require((0, 0) in aligned_units and (0, 1) in aligned_units,
            "required aligned terminal units changed")

    easy_payload = json.loads(EASY.read_text())
    require(easy_payload["result_sha256"] ==
            "71896910025164afcb24015d655cb252bd9e911cdaa744555a16b6f438553bea",
            "easy-strata exact ledger changed")
    easy_supports = (1, 3, 12, 7, 11, 13)
    easy_keys = {canonical((0, 63, support)) for support in easy_supports}
    cycle_keys = {(0, 31, 13), (0, 15, 3),
                  (0, 30, 12), (0, 13, 1)}
    cycle_payload = json.loads(CYCLE_EXACT.read_text())
    require(cycle_payload["result_sha256"] ==
            "1adc0b76fcce32afb9f0f400c2247a8753e278b60cd11360f96e18a188001141",
            "exact recursive cycle-face ledger changed")
    require((TP_P26 / "REPORT.md").is_file(),
            "TP P26 exact boundary report missing")

    starts = {}
    global_proper_keys = set()
    for name, raw_start in STARTS.items():
        start = canonical(raw_start)
        require(start == raw_start, f"{name} start canonicalization changed")
        grouped = defaultdict(list)
        covariance = []
        for zero_mask in sorted(every_nonempty_subset(start[2])):
            # A zero c numerator makes the opposite/diagonal term survive:
            # toggle T on exactly those edges and remove them from D.
            raw = (start[0], start[1] ^ zero_mask,
                   start[2] ^ zero_mask)
            target, action_index, action = canonical_with_witness(raw)
            require(target[2].bit_count() ==
                    start[2].bit_count() - zero_mask.bit_count(),
                    "boundary codimension changed under covariance")
            grouped[target].append(zero_mask)
            switches, permutation = action
            covariance.append({
                "zero_c_mask": zero_mask,
                "zero_c_edges": edge_list(zero_mask),
                "raw_state": state_key(raw),
                "canonical_state": state_key(target),
                "action_index": action_index,
                "switches": list(switches),
                "permutation": list(permutation),
            })
        reached = reachable(start, transition_map)
        proper = reached - {start}
        require(set(grouped) == proper and
                sum(map(len, grouped.values())) == 2 ** start[2].bit_count()-1,
                f"{name} subset/reachability cover changed")
        records = []
        for state in sorted(grouped, key=lambda item:
                            (-item[2].bit_count(), item)):
            key = state_key(state)
            classification = classify(key, aligned_units, easy_keys,
                                      cycle_keys)
            records.append({
                "key": key,
                "branch_mask": state[0],
                "selected_term_mask": state[1],
                "both_live_edge_mask": state[2],
                "both_live_degree": state[2].bit_count(),
                "support_shape": SUPPORT_NAMES.get(state[2]),
                "orbit_size": frozen_records[key]["orbit_size"],
                "boundary_targets": frozen_records[key]["boundary_targets"],
                "labelled_zero_subset_count": len(grouped[state]),
                "labelled_zero_masks": sorted(grouped[state]),
                **classification,
            })
        status_histogram = Counter(record["status"] for record in records)
        starts[name] = {
            "start_key": state_key(start),
            "proper_labelled_boundary_count": 2 ** start[2].bit_count() - 1,
            "proper_canonical_boundary_count": len(records),
            "degree_histogram": dict(sorted(Counter(
                record["both_live_degree"] for record in records).items(),
                reverse=True)),
            "status_histogram": dict(sorted(status_histogram.items())),
            "records": records,
            "covariance_ledger": covariance,
            "first_boundary_targets": [state_key(target)
                                       for target in transition_map[start]],
        }
        global_proper_keys |= {record["key"] for record in records}

    require(set(starts["k5"]["first_boundary_targets"]) ==
            {"0:31:15", "0:31:30"},
            "k5 first-face split changed")
    require(starts["k6"]["first_boundary_targets"] == ["0:31:31"],
            "k6 first-face split changed")
    require(not ({record["key"] for record in starts["k5"]["records"]} &
                 {record["key"] for record in starts["k6"]["records"]}),
            "k5/k6 proper canonical families unexpectedly overlap")
    # The first-face antichain is the minimal broad-face attack: proving a
    # first face without localizing its remaining c factors covers every one
    # of its descendants.
    minimal_boundary_residuals = {
        "k5": [
            {"key": "0:31:15", "support_shape": "triangle_plus_pendant",
             "codimension": 1, "labelled_multiplicity": 4},
            {"key": "0:31:30", "support_shape": "four_cycle",
             "codimension": 1, "labelled_multiplicity": 1},
        ],
        "k6": [
            {"key": "0:31:31", "support_shape": "K4_minus_one_edge",
             "codimension": 1, "labelled_multiplicity": 6},
        ],
        "k6_boundary_second_split": [
            {"key": "0:15:15", "support_shape": "triangle_plus_pendant",
             "codimension": 2, "labelled_multiplicity": 12},
            {"key": "0:30:30", "support_shape": "four_cycle",
             "codimension": 2, "labelled_multiplicity": 3},
        ],
    }
    for rows in minimal_boundary_residuals.values():
        for row in rows:
            require(any(record["key"] == row["key"] and
                        record["labelled_zero_subset_count"] ==
                        row["labelled_multiplicity"]
                        for start in starts.values()
                        for record in start["records"]),
                    f"minimal residual multiplicity changed: {row}")

    terminals = {
        name: [record for record in data["records"]
               if record["both_live_degree"] == 0]
        for name, data in starts.items()
    }
    require([record["key"] for record in terminals["k5"]] == ["0:1:0"]
            and [record["key"] for record in terminals["k6"]] == ["0:0:0"]
            and all(record["status"] == "exact_closed_aligned_unit"
                    for records in terminals.values() for record in records),
            "aligned terminal closure map changed")

    result = {
        "status": "UNAUDITED exact B4 covariance/routing census only",
        "edge_order": ["".join(map(str, edge)) for edge in EDGES],
        "group": "B4=C2^4 semidirect S4 (384 listed actions)",
        "labelled_ternary_state_count": len(labelled),
        "canonical_state_count": len(representatives),
        "transition": "(B,T,D)->(B,T xor Z,D minus Z)",
        "starts": starts,
        "proper_canonical_union_count": len(global_proper_keys),
        "minimal_boundary_residuals": minimal_boundary_residuals,
        "remaining_full_interiors": ["0:63:31", "0:63:63"],
        "terminal_closure_map": terminals,
        "known_exact_class_keys": {
            "easy_k_le_3_branch0_all_offdiagonal":
                sorted(state_key(state) for state in easy_keys),
            "cycle_proper_boundary_pairwise":
                sorted(state_key(state) for state in cycle_keys),
            "aligned_units_used": ["0:0", "0:1"],
        },
        "partial_results_not_counted_as_state_closure": {
            "triangle_pendant_P26_zero":
                "Exact only on determinant boundary; P26!=0 remains separate",
        },
        "source_hashes": {
            "frozen_729_graph": file_sha(FROZEN_GRAPH),
            "frozen_graph_builder": file_sha(FROZEN_BUILDER),
            "easy_strata": file_sha(EASY),
            "aligned_census": file_sha(ALIGNED),
            "cycle_exact_faces": file_sha(CYCLE_EXACT),
            "tp_p26_report": file_sha(TP_P26 / "REPORT.md"),
        },
        "scope_guard": (
            "No polynomial membership or emptiness is computed here. "
            "A new residual label means only that its canonical (B,T,D) key "
            "is not B4-equivalent to a frozen exact-closed k<=4 key.  A "
            "broad proof for a first-face residual without localizing its "
            "remaining c numerators covers its whole descendant subgraph."),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode()).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("k5/k6 recursive boundary routing: PASS")
    for name, data in starts.items():
        print(name, "labelled/canonical/status", data[
            "proper_labelled_boundary_count"],
            data["proper_canonical_boundary_count"],
            data["status_histogram"])
    print("minimal", minimal_boundary_residuals)
    print("result", result["result_sha256"])


if __name__ == "__main__":
    main()
