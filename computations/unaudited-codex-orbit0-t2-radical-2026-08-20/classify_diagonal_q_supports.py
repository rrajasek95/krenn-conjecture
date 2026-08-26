#!/usr/bin/env python3
"""Joint branch/Q-support orbit enumeration and modular Singular screen.

For a fixed cofactor-orientation representative, supports must be quotiented
by its stabilizer, not by the full B4 action.  The three representatives are
0, 1, and 11.  A live support S imposes Q_i=0 for i outside S, together with
the 22 branch equations and u*H-1.

The modular screen is discovery/triage.  A reported modular unit must still
be replayed over Q (or by an exact certificate) before it is theorem-bearing.
Timeouts include both genuinely nonunit ideals and merely hard unit ideals.
"""

from __future__ import annotations

import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from hashlib import sha256
from itertools import combinations, permutations, product
import importlib.util
import json
from pathlib import Path
import subprocess
import time


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
DEFINITIONS = (REPO / "computations" /
               "unaudited-codex-n8-dangerous-chart-bridge-2026-08-20" /
               "audit_diagonal_cofactor_branch_orbits.py")
EDGES = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}
BRANCHES = (0, 1, 11)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load_definitions():
    spec = importlib.util.spec_from_file_location("diagonal_defs", DEFINITIONS)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def transform_mask(mask, switches, permutation):
    answer = 0
    for edge_index, (i, j) in enumerate(EDGES):
        bit = ((mask >> edge_index) & 1) ^ switches[i] ^ switches[j]
        target = EDGE_INDEX[tuple(sorted((permutation[i], permutation[j])))]
        answer |= bit << target
    return answer


def transform_q_index(index, switches, permutation):
    bits = tuple((index >> (3 - site)) & 1 for site in range(4))
    transformed = [0] * 4
    for site in range(4):
        transformed[permutation[site]] = bits[site] ^ switches[site]
    return sum(transformed[site] << (3 - site) for site in range(4))


def group():
    return tuple((switches, permutation)
                 for switches in product((0, 1), repeat=4)
                 for permutation in permutations(range(4)))


def support_orbit_representatives(branch, size):
    stabilizer = tuple(element for element in group()
                       if transform_mask(branch, *element) == branch)
    unseen = {sum(1 << index for index in subset)
              for subset in combinations(range(16), size)}
    representatives = []
    while unseen:
        representative = min(unseen)
        orbit = set()
        for switches, permutation in stabilizer:
            transformed = 0
            for index in range(16):
                if representative >> index & 1:
                    transformed |= 1 << transform_q_index(
                        index, switches, permutation)
            orbit.add(transformed)
        require(representative == min(orbit), "noncanonical support orbit")
        unseen -= orbit
        representatives.append(representative)
    return stabilizer, tuple(representatives)


def branch_generators(defs, branch):
    generators = [defs.permanent_poly(edge) for edge in range(6)]
    generators.extend(defs.triangle_poly(*triple) for triple in defs.TRIPLES)
    for edge, (i, j) in enumerate(EDGES):
        entries = (((0, 1), (1, 0)) if branch >> edge & 1
                   else ((0, 0), (1, 1)))
        for x, y in entries:
            generators.append(defs.cofactor_poly(2 * i + x, 2 * j + y))
    require(len(generators) == 22, "branch generator count changed")
    return generators


def singular_program(defs, branch, support, characteristic):
    generators = branch_generators(defs, branch)
    generators.extend(defs.q_poly(index) for index in range(16)
                      if not (support >> index & 1))
    # On the six e_ij=1+per_ij and four t_ijk equations, the exact polarized
    # identity is H=sum_{s=0}^7 Q_s Q_{15-s}.  Use this much smaller literal
    # representative in the localization equation.  It is equivalent on the
    # base variety, not a truncated or one-sided replacement.
    q_strings = [defs.poly_to_singular(defs.q_poly(index))
                 for index in range(16)]
    localized_hafnian = "+".join(
        f"({q_strings[index]})*({q_strings[15 - index]})"
        for index in range(8))
    complementary_pairs = [index for index in range(8)
                           if (support >> index & 1)
                           and (support >> (15 - index) & 1)]
    variables = ",".join(["u", "v"] + [f"x{index}" for index in range(24)])
    if len(complementary_pairs) == 1:
        index = complementary_pairs[0]
        localization = (f",\n-1+u*({q_strings[index]}),"
                        f"\n-1+v*({q_strings[15 - index]})")
    else:
        localization = f",\n-1+u*({localized_hafnian})"
    return (
        f"ring r={characteristic},({variables}),dp;\n"
        "option(redSB);\n"
        "ideal J=" + ",\n".join(defs.poly_to_singular(poly)
                                  for poly in generators) +
        localization + ";\n"
        "ideal G=std(J);\n"
        'print("MARK_SIZE"); size(G);\n'
        'print("MARK_ONE"); reduce(1,G);\n'
    )


def run_case(defs, branch, support, characteristic, timeout):
    started = time.monotonic()
    try:
        completed = subprocess.run(
            ["Singular", "-q"],
            input=singular_program(defs, branch, support, characteristic),
            text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            timeout=timeout, check=False)
    except subprocess.TimeoutExpired:
        return {
            "branch": branch,
            "support_mask": support,
            "support_indices": [index for index in range(16)
                                if support >> index & 1],
            "status": "timeout",
            "complementary_live_pairs": sum(
                (support >> index & 1) and
                (support >> (15 - index) & 1) for index in range(8)),
            "elapsed_seconds": time.monotonic() - started,
        }
    lines = [line.strip() for line in completed.stdout.splitlines()
             if line.strip()]
    markers = {}
    for marker in ("MARK_SIZE", "MARK_ONE"):
        if marker in lines:
            position = lines.index(marker)
            markers[marker] = (lines[position + 1]
                               if position + 1 < len(lines) else None)
    one = markers.get("MARK_ONE")
    return {
        "branch": branch,
        "support_mask": support,
        "support_indices": [index for index in range(16)
                            if support >> index & 1],
        "status": ("unit" if one == "0" else
                   "nonunit" if one == "1" else "error"),
        "complementary_live_pairs": sum(
            (support >> index & 1) and
            (support >> (15 - index) & 1) for index in range(8)),
        "basis_size": (int(markers["MARK_SIZE"])
                       if markers.get("MARK_SIZE", "").isdigit() else None),
        "return_code": completed.returncode,
        "elapsed_seconds": time.monotonic() - started,
        "output_tail": lines[-8:],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--size", type=int, choices=(7, 8), required=True)
    parser.add_argument("--prime", type=int, default=7)
    parser.add_argument("--timeout", type=float, default=2.0)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--limit", type=int)
    args = parser.parse_args()
    defs = load_definitions()
    records = []
    orbit_counts = {}
    stabilizer_sizes = {}
    complementary_pair_histograms = {}
    cases = []
    for branch in BRANCHES:
        stabilizer, supports = support_orbit_representatives(branch, args.size)
        stabilizer_sizes[str(branch)] = len(stabilizer)
        orbit_counts[str(branch)] = len(supports)
        complementary_pair_histograms[str(branch)] = dict(sorted(Counter(
            sum((support >> index & 1) and
                (support >> (15 - index) & 1) for index in range(8))
            for support in supports).items()))
        cases.extend((branch, support) for support in supports)
    expected = ({"0": 337, "1": 1615, "11": 337} if args.size == 7
                else {"0": 386, "1": 1834, "11": 386})
    require(orbit_counts == expected, "joint branch/support orbit census changed")
    if args.limit is not None:
        cases = cases[:args.limit]
    print("setup size / cases / branch counts / stabilizers:",
          args.size, len(cases), orbit_counts, stabilizer_sizes, flush=True)
    started = time.monotonic()
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {executor.submit(run_case, defs, branch, support,
                                   args.prime, args.timeout): (branch, support)
                   for branch, support in cases}
        for count, future in enumerate(as_completed(futures), 1):
            records.append(future.result())
            if count % 100 == 0 or count == len(futures):
                histogram = Counter(record["status"] for record in records)
                print("progress", count, dict(histogram),
                      f"{time.monotonic() - started:.2f}s", flush=True)
    records.sort(key=lambda row: (row["branch"], row["support_mask"]))
    histogram = Counter(record["status"] for record in records)
    result = {
        "status": "UNAUDITED modular joint branch/Q-support screen",
        "definitions_path": str(DEFINITIONS.relative_to(REPO)),
        "definitions_sha256": sha256(DEFINITIONS.read_bytes()).hexdigest(),
        "support_size": args.size,
        "prime": args.prime,
        "timeout_seconds_per_case": args.timeout,
        "workers": args.workers,
        "branch_stabilizer_sizes": stabilizer_sizes,
        "joint_orbit_counts": orbit_counts,
        "joint_orbit_complementary_live_pair_histograms":
            complementary_pair_histograms,
        "cases_screened": len(cases),
        "result_histogram": dict(sorted(histogram.items())),
        "elapsed_seconds": time.monotonic() - started,
        "records": records,
        "scope": (
            "Modular unit results are a discovery screen until replayed over "
            "Q. A timeout can be nonunit or merely hard. Orbit counts use the "
            "stabilizer of each fixed cofactor branch."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    suffix = (f"_limit{args.limit}_timeout{args.timeout:g}"
              if args.limit is not None else "")
    out = HERE / (f"results_diagonal_q_support_k{args.size}_p{args.prime}"
                  f"{suffix}.json")
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("final", dict(histogram), "elapsed", result["elapsed_seconds"],
          "sha", result["result_sha256"], flush=True)


if __name__ == "__main__":
    main()
