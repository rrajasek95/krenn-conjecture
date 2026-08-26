#!/usr/bin/env python3
"""Exact modular screen of joint cofactor-branch/Q-support orbits.

There are three B4 orbits of six cofactor-orientation bits, represented by
edge masks 0, 11 and 1.  Once a branch representative is fixed, Q supports
must be quotiented only by its stabilizer (not by all of B4).  For every
joint representative this script tests

    six permanent rows + four triangle rows + twelve selected cofactors
    + Q_s=0 off the allowed support + u*H-1.

Singular arithmetic over a prime field is exact.  A UNIT result is therefore
a sound characteristic-zero exclusion.  NONUNIT and TIMEOUT are only
survivors for later exact-Q replay.
"""

from __future__ import annotations

import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from hashlib import sha256
import importlib.util
from itertools import combinations, permutations, product
import json
from pathlib import Path
import subprocess
import time


HERE = Path(__file__).resolve().parent
CORE_PATH = HERE / "audit_polarized_superpair_core_identity.py"
PROBE_PATH = HERE / "probe_cofactor_orientation_classes.py"
EDGES = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}
BRANCH_REPRESENTATIVES = (0, 11, 1)


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


CORE = load_module("n8_joint_screen_core", CORE_PATH)
PROBE = load_module("n8_joint_screen_probe", PROBE_PATH)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def act_index(value, permutation, flips):
    old = tuple((value >> (3 - site)) & 1 for site in range(4))
    new = [0] * 4
    for old_site in range(4):
        new[permutation[old_site]] = old[old_site]
    return sum((new[site] ^ flips[site]) << (3 - site)
               for site in range(4))


def act_support_mask(mask, permutation, flips):
    return sum(1 << act_index(value, permutation, flips)
               for value in range(16) if mask & (1 << value))


def act_branch_mask(mask, permutation, flips):
    old = tuple((mask >> edge_index) & 1 for edge_index in range(6))
    new = [0] * 6
    for edge_index, (left, right) in enumerate(EDGES):
        new_left, new_right = permutation[left], permutation[right]
        new_edge = tuple(sorted((new_left, new_right)))
        new[EDGE_INDEX[new_edge]] = (
            old[edge_index] ^ flips[new_left] ^ flips[new_right]
        )
    return sum(value << edge_index for edge_index, value in enumerate(new))


ACTIONS = tuple((permutation, flips)
                for permutation in permutations(range(4))
                for flips in product((0, 1), repeat=4))


def support_masks(size):
    return (sum(1 << value for value in support)
            for support in combinations(range(16), size))


def joint_representatives(branch, size):
    stabilizer = tuple(action for action in ACTIONS
                       if act_branch_mask(branch, *action) == branch)
    seen = set()
    representatives = []
    for mask in support_masks(size):
        if mask in seen:
            continue
        orbit = {act_support_mask(mask, *action) for action in stabilizer}
        representative = min(orbit)
        seen.update(orbit)
        representatives.append(representative)
    return stabilizer, tuple(sorted(representatives))


def branch_bits(branch):
    return tuple((branch >> edge_index) & 1 for edge_index in range(6))


def support_values(mask):
    return tuple(value for value in range(16) if mask & (1 << value))


def q_poly(value):
    bits = tuple((value >> (3 - site)) & 1 for site in range(4))
    return CORE.q_orientation(bits)


def singular_command(branch, support_mask, prime):
    equations, hafnian = PROBE.equations(branch_bits(branch))
    equations.extend(q_poly(value) for value in range(16)
                     if not support_mask & (1 << value))
    variables = ",".join([f"x{index}" for index in range(24)] + ["u"])
    ideal = ",".join(PROBE.singular(poly) for poly in equations)
    return (
        f"ring R={prime},({variables}),dp; "
        f"ideal I={ideal},u*({PROBE.singular(hafnian)})-1; "
        "ideal G=slimgb(I); poly z=reduce(1,G); "
        "if(z==0){print(\"UNIT\");}else{print(\"NONUNIT\");}; quit;"
    )


def screen_one(task):
    branch, size, support_mask, prime, timeout = task
    start = time.monotonic()
    try:
        completed = subprocess.run(
            ["Singular", "-q", "-c",
             singular_command(branch, support_mask, prime)],
            text=True, capture_output=True, timeout=timeout, check=False,
        )
        elapsed = time.monotonic() - start
        tokens = completed.stdout.split()
        if completed.returncode != 0:
            status = "ERROR"
        elif "UNIT" in tokens:
            status = "UNIT"
        elif "NONUNIT" in tokens:
            status = "NONUNIT"
        else:
            status = "ERROR"
        return {
            "branch_mask": branch,
            "support_size": size,
            "support_mask": support_mask,
            "support": list(support_values(support_mask)),
            "prime": prime,
            "status": status,
            "elapsed_seconds": round(elapsed, 6),
            "stdout_tail": completed.stdout[-500:],
            "stderr_tail": completed.stderr[-500:],
        }
    except subprocess.TimeoutExpired:
        return {
            "branch_mask": branch,
            "support_size": size,
            "support_mask": support_mask,
            "support": list(support_values(support_mask)),
            "prime": prime,
            "status": "TIMEOUT",
            "elapsed_seconds": round(time.monotonic() - start, 6),
        }


def census():
    rows = []
    expected = {0: {7: 337, 8: 386},
                11: {7: 337, 8: 386},
                1: {7: 1615, 8: 1834}}
    expected_stabilizer = {0: 48, 11: 48, 1: 8}
    for branch in BRANCH_REPRESENTATIVES:
        row = {"branch_mask": branch, "sizes": {}}
        for size in (7, 8):
            stabilizer, representatives = joint_representatives(branch, size)
            require(len(stabilizer) == expected_stabilizer[branch],
                    "branch stabilizer count changed")
            require(len(representatives) == expected[branch][size],
                    "joint orbit count changed")
            row["stabilizer_size"] = len(stabilizer)
            row["sizes"][str(size)] = {
                "representative_count": len(representatives),
                "representative_masks": list(representatives),
            }
        rows.append(row)
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--screen", action="store_true")
    parser.add_argument("--prime", type=int, default=1009)
    parser.add_argument("--timeout", type=float, default=3.0)
    parser.add_argument("--workers", type=int, default=3)
    parser.add_argument("--branches", type=int, nargs="*",
                        default=list(BRANCH_REPRESENTATIVES))
    parser.add_argument("--sizes", type=int, nargs="*", default=[7, 8])
    parser.add_argument("--limit", type=int)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    rows = census()
    summary = {
        "status": "UNAUDITED exact joint orbit census",
        "action_count": len(ACTIONS),
        "branches": rows,
        "total_size7_representatives": 2289,
        "total_size8_representatives": 2606,
    }
    logical = json.dumps(summary, sort_keys=True, separators=(",", ":"))
    summary["census_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    print("joint census: PASS; size7 / size8 = 2289 / 2606")
    print("census sha256:", summary["census_sha256"])
    if not args.screen:
        return

    tasks = []
    by_branch = {row["branch_mask"]: row for row in rows}
    for branch in args.branches:
        require(branch in BRANCH_REPRESENTATIVES, "unknown branch")
        for size in args.sizes:
            require(size in (7, 8), "only support sizes seven/eight are frozen")
            masks = by_branch[branch]["sizes"][str(size)][
                "representative_masks"]
            tasks.extend((branch, size, mask, args.prime, args.timeout)
                         for mask in masks)
    if args.limit is not None:
        tasks = tasks[:args.limit]
    output = args.output or (
        HERE / f"results_lowq_joint_screen_p{args.prime}.jsonl"
    )
    status_counts = Counter()
    completed_count = 0
    with output.open("w") as stream:
        header = dict(summary)
        header.update({
            "record_type": "header",
            "prime": args.prime,
            "timeout_seconds": args.timeout,
            "workers": args.workers,
            "task_count": len(tasks),
        })
        stream.write(json.dumps(header, sort_keys=True) + "\n")
        with ThreadPoolExecutor(max_workers=args.workers) as executor:
            futures = {executor.submit(screen_one, task): task
                       for task in tasks}
            for future in as_completed(futures):
                record = future.result()
                stream.write(json.dumps(record, sort_keys=True) + "\n")
                stream.flush()
                completed_count += 1
                status_counts[record["status"]] += 1
                if completed_count % 100 == 0:
                    print("completed", completed_count, "of", len(tasks),
                          dict(status_counts), flush=True)
    print("screen complete:", dict(status_counts), "output", output)


if __name__ == "__main__":
    main()
