#!/usr/bin/env python3
"""Exact-Q discovery sweep for joint cofactor-branch/Q-support orbits.

This is a Singular-backed discovery probe.  A UNIT result is exact for the
displayed ideal, but this script does not retain Nullstellensatz multipliers;
terminal promotion requires an independently replayable certificate.
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
ROOT = HERE.parents[1]
CORE_PATH = (ROOT / "computations" /
             "unaudited-codex-n8-dangerous-chart-bridge-2026-08-20" /
             "audit_diagonal_cofactor_branch_orbits.py")
EDGE_ORDER = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGE_ORDER)}
BRANCH_REPRESENTATIVES = (0, 1, 11)


def require(condition: bool, detail: str) -> None:
    if not condition:
        raise RuntimeError(detail)


def load_core():
    spec = importlib.util.spec_from_file_location("root_lowq_core", CORE_PATH)
    module = importlib.util.module_from_spec(spec)
    require(spec.loader is not None, "core loader missing")
    spec.loader.exec_module(module)
    return module


CORE = load_core()


def transform_branch(mask, permutation, flips):
    answer = 0
    for edge_index, (left, right) in enumerate(EDGE_ORDER):
        bit = ((mask >> edge_index) & 1) ^ flips[left] ^ flips[right]
        image = tuple(sorted((permutation[left], permutation[right])))
        answer |= bit << EDGE_INDEX[image]
    return answer


def bit_tuple(index):
    return tuple((index >> (3 - position)) & 1 for position in range(4))


def q_map(permutation, flips):
    answer = []
    for source in range(16):
        source_bits = bit_tuple(source)
        target_bits = [0] * 4
        for position in range(4):
            target_bits[permutation[position]] = source_bits[position] ^ flips[position]
        answer.append(sum(bit << (3 - position)
                          for position, bit in enumerate(target_bits)))
    return tuple(answer)


GROUP = tuple((permutation, flips, q_map(permutation, flips))
              for permutation in permutations(range(4))
              for flips in product((0, 1), repeat=4))


def transform_support(mask, mapping):
    answer = 0
    for source in range(16):
        if (mask >> source) & 1:
            answer |= 1 << mapping[source]
    return answer


def support_tuple(mask):
    return tuple(index for index in range(16) if (mask >> index) & 1)


def joint_representatives(size):
    records = []
    for branch in BRANCH_REPRESENTATIVES:
        stabilizer = tuple(element for element in GROUP
                           if transform_branch(branch, element[0], element[1]) == branch)
        unseen = {sum(1 << index for index in choice)
                  for choice in combinations(range(16), size)}
        representatives = []
        while unseen:
            representative = min(unseen)
            orbit = {transform_support(representative, element[2])
                     for element in stabilizer}
            unseen -= orbit
            representatives.append((representative, len(orbit)))
        records.extend({"branch_mask": branch,
                        "branch_stabilizer_order": len(stabilizer),
                        "support_mask": representative,
                        "support": list(support_tuple(representative)),
                        "support_orbit_size": orbit_size}
                       for representative, orbit_size in representatives)
    return records


def common_generators(branch):
    generators = [CORE.permanent_poly(edge) for edge in range(6)]
    generators.extend(CORE.triangle_poly(*triple) for triple in CORE.TRIPLES)
    for edge, (left, right) in enumerate(CORE.EDGES):
        entries = (((0, 1), (1, 0)) if (branch >> edge) & 1
                   else ((0, 0), (1, 1)))
        for x_value, y_value in entries:
            generators.append(CORE.cofactor_poly(2 * left + x_value,
                                                  2 * right + y_value))
    hafnian = CORE.matching_poly(tuple(range(8)))
    generators.append(CORE.normalize_poly(
        tuple((coefficient, monomial + (24,))
              for monomial, coefficient in hafnian.items()) + ((-1, ()),)
    ))
    require(len(generators) == 23, "common generator count changed")
    return tuple(CORE.poly_to_singular(poly) for poly in generators)


COMMON = {branch: common_generators(branch)
          for branch in BRANCH_REPRESENTATIVES}
Q_STRINGS = tuple(CORE.poly_to_singular(CORE.q_poly(index))
                  for index in range(16))


def singular_program(record):
    support = set(record["support"])
    zero_q = [Q_STRINGS[index] for index in range(16)
              if index not in support]
    variables = ",".join([f"x{index}" for index in range(24)] + ["u"])
    return (
        f"ring r=0,({variables}),dp;\n"
        'LIB "sing.lib";\n'
        "ideal I=" + ",".join(COMMON[record["branch_mask"]] + tuple(zero_q)) + ";\n"
        "ideal G=slimgb(I);\n"
        'print("MARK_DONE"); size(G); reduce(1,G);\n'
    )


def run_record(index, record, timeout):
    started = time.monotonic()
    try:
        completed = subprocess.run(
            ["Singular", "-q"], input=singular_program(record), text=True,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            timeout=timeout, check=False,
        )
    except subprocess.TimeoutExpired as error:
        return index, {**record, "status": "TIMEOUT",
                       "elapsed_seconds": time.monotonic() - started,
                       "output_tail": (error.stdout or "")[-500:]}
    lines = [line.strip() for line in completed.stdout.splitlines()
             if line.strip()]
    status = "ERROR"
    basis_size = None
    remainder = None
    if "MARK_DONE" in lines:
        position = lines.index("MARK_DONE")
        if position + 2 < len(lines):
            basis_size = lines[position + 1]
            remainder = lines[position + 2]
            status = "UNIT" if remainder == "0" else "NONUNIT"
    return index, {**record, "status": status,
                   "elapsed_seconds": time.monotonic() - started,
                   "basis_size": basis_size, "remainder_of_one": remainder,
                   "return_code": completed.returncode,
                   "output_tail": lines[-8:]}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--support-size", type=int, choices=(7, 8), required=True)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--timeout", type=float, default=2.0)
    args = parser.parse_args()
    records = joint_representatives(args.support_size)
    expected = {7: 2289, 8: 2606}[args.support_size]
    require(len(records) == expected, "joint orbit census changed")
    started = time.monotonic()
    completed_records = [None] * len(records)
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = [executor.submit(run_record, index, record, args.timeout)
                   for index, record in enumerate(records)]
        done = 0
        for future in as_completed(futures):
            index, result = future.result()
            completed_records[index] = result
            done += 1
            if done % 100 == 0 or result["status"] != "UNIT":
                counts = Counter(item["status"] for item in completed_records
                                 if item is not None)
                print("progress", done, "/", len(records), dict(counts), flush=True)
    require(all(record is not None for record in completed_records),
            "a worker result is missing")
    counts = Counter(record["status"] for record in completed_records)
    result = {
        "status": "UNAUDITED exact-Q joint branch/support discovery sweep",
        "support_size": args.support_size,
        "branch_representatives": list(BRANCH_REPRESENTATIVES),
        "record_count": len(records),
        "status_histogram": dict(sorted(counts.items())),
        "timeout_seconds_per_case": args.timeout,
        "workers": args.workers,
        "elapsed_seconds": time.monotonic() - started,
        "records": completed_records,
        "scope": (
            "Singular exact-Q discovery. UNIT is mathematically exact for a "
            "case, but replayable Nullstellensatz multipliers are not retained."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    out = HERE / f"results_diagonal_lowq_joint_support{args.support_size}.json"
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("DONE", dict(sorted(counts.items())), "elapsed", result["elapsed_seconds"])
    print("result sha256", result["result_sha256"])


if __name__ == "__main__":
    main()
