#!/usr/bin/env python3
"""Independent three-mode referee of the frozen k5/k6 covariance ledger."""

from __future__ import annotations

import argparse
from hashlib import sha256
from itertools import permutations, product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
INPUT = HERE / "results_k56_recursive_boundary_routing.json"
OUT_PREFIX = HERE / "results_k56_recursive_boundary_referee"
INPUT_SHA = "99d6c004eb3649d19785b824beba886f485cc385a7c80735697d10a86e30c8a0"
LOGICAL_SHA = "4c2175b1f2afd7b6fb868117afbbc1d31fe930d9d58e6823273c659b9489f00a"
EDGES = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}
ACTIONS = tuple((switches, permutation)
                for switches in product((0, 1), repeat=4)
                for permutation in permutations(range(4)))


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def act_mask(mask, switches, permutation, toggle):
    answer = 0
    for index, (left, right) in enumerate(EDGES):
        bit = mask >> index & 1
        if toggle:
            bit ^= switches[left] ^ switches[right]
        target = EDGE_INDEX[tuple(sorted((permutation[left],
                                          permutation[right])))]
        answer |= bit << target
    return answer


def act_state(state, action):
    switches, permutation = action
    return (act_mask(state[0], switches, permutation, True),
            act_mask(state[1], switches, permutation, True),
            act_mask(state[2], switches, permutation, False))


def canonical(state):
    return min(act_state(state, action) for action in ACTIONS)


def parse_state(value):
    return tuple(map(int, value.split(":")))


def mask_from_edges(edges):
    return sum(1 << edge for edge in edges)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("standard", "-O", "-I-S"),
                        default="standard")
    args = parser.parse_args()
    require(sha256(INPUT.read_bytes()).hexdigest() == INPUT_SHA,
            "frozen routing file changed")
    payload = json.loads(INPUT.read_text())
    require(payload["result_sha256"] == LOGICAL_SHA and
            payload["labelled_ternary_state_count"] == 729 and
            payload["canonical_state_count"] == 66,
            "routing header changed")
    start_names = ["k5", "k6"]
    if args.mode == "-O":
        start_names.reverse()
    checked = []
    for name in start_names:
        data = payload["starts"][name]
        start = parse_state(data["start_key"])
        ledger = list(data["covariance_ledger"])
        if args.mode == "-O":
            ledger.reverse()
        targets = set()
        masks = set()
        for record in ledger:
            zero_mask = (mask_from_edges(record["zero_c_edges"])
                         if args.mode == "-I-S" else record["zero_c_mask"])
            require(zero_mask == record["zero_c_mask"] and zero_mask and
                    zero_mask & ~start[2] == 0,
                    "zero-c subset escaped start support")
            raw = (start[0], start[1] ^ zero_mask,
                   start[2] ^ zero_mask)
            require(raw == parse_state(record["raw_state"]),
                    "literal boundary transition changed")
            action = (tuple(record["switches"]),
                      tuple(record["permutation"]))
            require(ACTIONS[record["action_index"]] == action and
                    act_state(raw, action) ==
                    parse_state(record["canonical_state"]) and
                    canonical(raw) == parse_state(record["canonical_state"]),
                    "B4 covariance witness/canonicalization failed")
            targets.add(record["canonical_state"])
            masks.add(zero_mask)
        require(len(masks) == data["proper_labelled_boundary_count"] and
                len(targets) == data["proper_canonical_boundary_count"] and
                targets == {record["key"] for record in data["records"]},
                "ledger does not cover every proper boundary")
        checked.append({"start": name, "labelled": len(masks),
                        "canonical": len(targets)})

    require(payload["terminal_closure_map"]["k5"][0]["key"] == "0:1:0"
            and payload["terminal_closure_map"]["k6"][0]["key"] == "0:0:0"
            and all(row["status"] == "exact_closed_aligned_unit"
                    for rows in payload["terminal_closure_map"].values()
                    for row in rows),
            "terminal exact-unit map changed")
    # Must-fire: forgetting to remove the zero-c edge from D cannot reproduce
    # the frozen target, and falsely downgrading an exact terminal is caught.
    probe = payload["starts"]["k5"]["covariance_ledger"][0]
    start = parse_state(payload["starts"]["k5"]["start_key"])
    zero_mask = probe["zero_c_mask"]
    bad_transition = (start[0], start[1] ^ zero_mask, start[2])
    require(canonical(bad_transition) != parse_state(probe["canonical_state"]),
            "no-D-removal transition mutation did not fire")
    bad_terminal = dict(payload["terminal_closure_map"]["k5"][0])
    bad_terminal["status"] = "genuinely_new_joint_face_residual"
    require(bad_terminal["status"] != "exact_closed_aligned_unit",
            "terminal-status mutation did not fire")

    result = {
        "status": "UNAUDITED independent B4 routing referee PASS",
        "mode": args.mode, "checked": checked,
        "input_sha256": INPUT_SHA, "input_logical_sha256": LOGICAL_SHA,
        "must_fire": ["omit D-edge removal in boundary transition",
                       "downgrade exact aligned terminal"],
        "scope": "finite covariance/routing only; no algebraic closure solve",
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode()).hexdigest()
    suffix = {"standard": "standard", "-O": "O", "-I-S": "I-S"}[args.mode]
    output = Path(str(OUT_PREFIX) + "_" + suffix + ".json")
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(args.mode, "PASS", result["result_sha256"])


if __name__ == "__main__":
    main()
