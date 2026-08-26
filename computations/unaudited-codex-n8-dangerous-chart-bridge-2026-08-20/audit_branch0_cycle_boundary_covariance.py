#!/usr/bin/env python3
"""Exact covariance/scope audit for the branch-0 k4-cycle boundary.

On the offdiagonal parametrization

  c_e=-(1+a_e*d_e)/b_e,

the defect chart localizes a_e,d_e,b_e on S={1,2,3,4}.  Therefore c_e=0
is exactly a_e*d_e=-1, and the live selected term on that edge can be
switched from b_e*c_e to a_e*d_e.  This audit enumerates all 15 nonempty
zero subsets and their induced (branch,term,remaining-full-support) charts.

Only the all-four-zero stratum is a fully aligned six-block chart.  Proper
subsets leave at least one genuinely full block and hence require a
lower-defect recursive theorem; the 50 aligned charts alone do not close
them.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import importlib.util
from itertools import combinations, permutations, product
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
OUT = HERE / "results_branch0_cycle_boundary_covariance.json"
ALIGNED_SOURCE = (HERE.parent
                  / "unaudited-codex-orbit0-t2-radical-2026-08-20"
                  / "audit_joint_aligned_zero_chart_census.py")
COMPONENT_RESULT = HERE / "results_branch0_cycle_czero_component.json"
EDGES = tuple(combinations(range(4), 2))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}
DEFECT_SUPPORT = frozenset((1, 2, 3, 4))
INITIAL_TERM_MASK = 63


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


ALIGNED = load("n8_cycle_boundary_aligned", ALIGNED_SOURCE)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def edge_mask(edges):
    return sum(1 << edge for edge in edges)


def permute_edge_mask(mask, permutation):
    answer = 0
    for edge_index, (left, right) in enumerate(EDGES):
        if not mask & (1 << edge_index):
            continue
        image = tuple(sorted((permutation[left], permutation[right])))
        answer |= 1 << EDGE_INDEX[image]
    return answer


def canonical_triple(branch, term, remaining):
    images = []
    for switches in product((0, 1), repeat=4):
        for permutation in permutations(range(4)):
            images.append((
                ALIGNED.act_mask(branch, switches, permutation),
                ALIGNED.act_mask(term, switches, permutation),
                permute_edge_mask(remaining, permutation),
            ))
    return min(images), len(set(images))


def cycle_adjacency_type(zero_edges):
    if len(zero_edges) != 2:
        return str(len(zero_edges))
    left, right = (EDGES[edge] for edge in zero_edges)
    return "adjacent_pair" if set(left) & set(right) else "opposite_pair"


def main():
    require(COMPONENT_RESULT.exists(), "the exact all-four-zero result is missing")
    component = json.loads(COMPONENT_RESULT.read_text())
    require(component["result_sha256"]
            == "5dcb5dc3ad09933773076efd5b25c3a069e6f239c523a2c2a97218d16f8c7b48",
            "the exact all-four-zero component digest changed")

    records = []
    for size in range(1, 5):
        for zero_edges in combinations(sorted(DEFECT_SUPPORT), size):
            zero_mask = edge_mask(zero_edges)
            remaining_mask = edge_mask(DEFECT_SUPPORT) ^ zero_mask
            term_mask = INITIAL_TERM_MASK ^ zero_mask
            canonical, orbit_size = canonical_triple(0, term_mask,
                                                       remaining_mask)
            records.append({
                "zero_edges": list(zero_edges),
                "zero_mask": zero_mask,
                "zero_type": cycle_adjacency_type(zero_edges),
                "selected_term_mask": term_mask,
                "remaining_full_support": [edge for edge in DEFECT_SUPPORT
                                           if remaining_mask & (1 << edge)],
                "remaining_full_mask": remaining_mask,
                "canonical_branch_term_remaining": list(canonical),
                "joint_orbit_size": orbit_size,
                "fully_aligned": remaining_mask == 0,
            })
    require(len(records) == 15, "boundary Boolean lattice count changed")
    require(Counter(len(row["zero_edges"]) for row in records)
            == {1: 4, 2: 6, 3: 4, 4: 1},
            "boundary size histogram changed")
    require(Counter(row["zero_type"] for row in records if
                    len(row["zero_edges"]) == 2)
            == {"adjacent_pair": 4, "opposite_pair": 2},
            "two-edge boundary types changed")

    aligned = [row for row in records if row["fully_aligned"]]
    require(len(aligned) == 1 and aligned[0]["selected_term_mask"] == 33,
            "the fully aligned boundary mask changed")
    require(aligned[0]["canonical_branch_term_remaining"] == [0, 12, 0],
            "the fully aligned canonical chart changed")
    require(all(not row["fully_aligned"] for row in records[:-1]),
            "a proper boundary subset was mislabeled fully aligned")

    # Hostile regression: forgetting to switch one dead offdiagonal term
    # would retain bit 1 although b_e*c_e=0, so it is not a live chart.
    for row in records:
        for edge in row["zero_edges"]:
            require(not row["selected_term_mask"] & (1 << edge),
                    "a dead offdiagonal term remained selected")

    result = {
        "status": "UNAUDITED exact k4-cycle boundary covariance audit",
        "branch_mask": 0,
        "initial_term_mask": INITIAL_TERM_MASK,
        "defect_support": sorted(DEFECT_SUPPORT),
        "offdiagonal_formula": "b_e*c_e=-(1+a_e*d_e)",
        "localized_factors": ["b_e", "a_e*d_e for e in S"],
        "boundary_records": records,
        "histograms": {
            "zero_count": {str(key): value for key, value in sorted(
                Counter(len(row["zero_edges"]) for row in records).items())},
            "two_edge_type": dict(Counter(
                row["zero_type"] for row in records
                if len(row["zero_edges"]) == 2)),
        },
        "all_four_zero": {
            "branch_term": [0, 33],
            "canonical_aligned_pair": [0, 12],
            "exact_component_result_sha256": component["result_sha256"],
            "pure_hafnian": component["pure_hafnian"],
        },
        "scope": (
            "Cprod=0 is a union of 15 exact strata. Only Z=S is fully "
            "aligned and already belongs to the closed 50-chart family. "
            "Every proper Z recursively leaves |S\\Z| full blocks in the "
            "listed joint branch/term chart; those lower-defect charts need "
            "their own unit/pairwise closure before an interior saturation "
            "can close the whole k4 chart."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("branch-0 k4-cycle boundary covariance: PASS")
    print("records / aligned:", len(records), len(aligned))
    print("zero hist:", result["histograms"])
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
