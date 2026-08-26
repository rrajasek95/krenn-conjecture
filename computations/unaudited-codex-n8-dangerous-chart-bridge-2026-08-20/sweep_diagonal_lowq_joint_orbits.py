#!/usr/bin/env python3
"""Exact-Q sweep of joint (cofactor branch, Q support) B4 orbits.

For support size k, quotient the k-subsets of the sixteen Q coordinates only
by the stabilizer of the fixed cofactor-orientation branch.  For k=7 the
counts are 337, 1615, 337 for branch representatives 0,1,11.  Each case asks
whether the branch equations, the nine complementary Q zeros, and u*H-1
generate the unit ideal over Q.  A unit result excludes the full joint orbit.

The script writes deterministic chunks so hard/nonunit cases can be isolated
without losing completed exact computations.
"""

from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
import importlib.util
from itertools import combinations, permutations, product
import json
from pathlib import Path
import time


HERE = Path(__file__).resolve().parent
PROBE_PATH = HERE / "probe_diagonal_q_units.py"
SPEC = importlib.util.spec_from_file_location("q_unit_probe", PROBE_PATH)
probe = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(probe)

EDGES = tuple(combinations(range(4), 2))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def group_actions():
    answer = []
    for permutation in permutations(range(4)):
        for flips in product((0, 1), repeat=4):
            edge_action = []
            for i, j in EDGES:
                left, right = sorted((permutation[i], permutation[j]))
                edge_action.append((EDGE_INDEX[(left, right)],
                                    flips[i] ^ flips[j]))
            q_action = []
            for word in range(16):
                source = tuple((word >> (3 - site)) & 1 for site in range(4))
                target = [0] * 4
                for site in range(4):
                    target[permutation[site]] = source[site] ^ flips[site]
                q_action.append(sum(target[site] << (3 - site)
                                    for site in range(4)))
            answer.append((tuple(edge_action), tuple(q_action)))
    require(len(answer) == 384, "B4 action size changed")
    return tuple(answer)


GROUP = group_actions()


def transform_branch(mask, action):
    answer = 0
    for source, (target, flip) in enumerate(action):
        answer |= (((mask >> source) & 1) ^ flip) << target
    return answer


def transform_support(mask, action):
    answer = 0
    for source, target in enumerate(action):
        if mask >> source & 1:
            answer |= 1 << target
    return answer


def support_orbit_representatives(branch, support_size):
    stabilizer = tuple(q_action for edge_action, q_action in GROUP
                       if transform_branch(branch, edge_action) == branch)
    unseen = {sum(1 << coordinate for coordinate in subset)
              for subset in combinations(range(16), support_size)}
    records = []
    while unseen:
        seed = min(unseen)
        orbit = {transform_support(seed, action) for action in stabilizer}
        unseen -= orbit
        records.append((min(orbit), len(orbit)))
    records.sort()
    return len(stabilizer), tuple(records)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--branch", type=int, choices=(0, 1, 11), required=True)
    parser.add_argument("--support-size", type=int, default=7)
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--limit", type=int, default=100)
    parser.add_argument("--timeout", type=int, default=10)
    args = parser.parse_args()

    stabilizer_size, representatives = support_orbit_representatives(
        args.branch, args.support_size)
    expected = {(0, 7): 337, (1, 7): 1615, (11, 7): 337,
                (0, 8): 386, (1, 8): 1834, (11, 8): 386}
    if (args.branch, args.support_size) in expected:
        require(len(representatives) == expected[(args.branch,
                                                  args.support_size)],
                "joint-orbit count changed")
    stop = min(len(representatives), args.start + args.limit)
    selected = representatives[args.start:stop]
    print("branch/support/stabilizer/orbits/chunk:", args.branch,
          args.support_size, stabilizer_size, len(representatives),
          args.start, stop, flush=True)
    records = []
    started = time.monotonic()
    for offset, (support_mask, orbit_size) in enumerate(selected):
        zero_indices = tuple(index for index in range(16)
                             if not (support_mask >> index & 1))
        status, elapsed, detail = probe.run(
            args.branch, zero_indices, 0, "slimgb", args.timeout)
        record = {
            "orbit_index": args.start + offset,
            "support_mask": support_mask,
            "support_indices": [index for index in range(16)
                                if support_mask >> index & 1],
            "zero_indices": list(zero_indices),
            "orbit_size_under_branch_stabilizer": orbit_size,
            "status": status,
            "elapsed_seconds": elapsed,
            "detail": detail,
        }
        records.append(record)
        if offset % 25 == 0 or status != "UNIT":
            print("case", args.start + offset, status,
                  f"{elapsed:.3f}s", record["support_indices"], flush=True)
    result = {
        "status": "UNAUDITED exact-Q diagonal low-Q joint-orbit chunk",
        "branch_mask": args.branch,
        "support_size": args.support_size,
        "B4_size": len(GROUP),
        "branch_stabilizer_size": stabilizer_size,
        "joint_orbit_count_for_fixed_branch": len(representatives),
        "chunk_start": args.start,
        "chunk_stop": stop,
        "timeout_seconds_per_case": args.timeout,
        "status_histogram": dict(sorted(Counter(record["status"]
                                                  for record in records).items())),
        "total_elapsed_seconds": time.monotonic() - started,
        "records": records,
        "scope": (
            "UNIT is an exact characteristic-zero Singular slimgb result for "
            "the displayed Rabinowitsch ideal. TIMEOUT/NONUNIT is nonterminal."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    output = HERE / (f"results_lowq_sweep_b{args.branch}_k{args.support_size}_"
                     f"{args.start}_{stop}.json")
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("histogram/elapsed:", result["status_histogram"],
          f"{result['total_elapsed_seconds']:.3f}s")
    print("result/path:", result["result_sha256"], output)


if __name__ == "__main__":
    main()
