#!/usr/bin/env python3
"""Enumerate every physical-pair support at the orbitwise arm floor."""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import importlib.util
from itertools import combinations, permutations
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
CORE_SPEC = importlib.util.spec_from_file_location(
    "codex_quotient_skeleton_core", HERE / "audit_quotient_skeleton.py")
core = importlib.util.module_from_spec(CORE_SPEC)
CORE_SPEC.loader.exec_module(core)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def selected_from_record(record):
    triple = tuple(tuple(tuple(edge) for edge in matching)
                   for matching in record["representative"])
    return tuple(sorted(set(edge for matching in triple for edge in matching)))


def floor_masks(record):
    selected = selected_from_record(record)
    initial = core.graph_mask(selected)
    missing = tuple(index for index in range(28)
                    if not initial & (1 << index))
    count = record["minimum_additional_physical_pairs"]
    survivors = []
    tested = 0
    for addition in combinations(missing, count):
        tested += 1
        mask = initial
        for index in addition:
            mask |= 1 << index
        if core.arm_property(mask, selected):
            survivors.append(mask)
    require(survivors, (record["orbit"], "floor lost all witnesses"))
    require(all(mask.bit_count() == record["minimum_total_physical_pairs"]
                for mask in survivors), (record["orbit"], "wrong floor size"))
    return survivors, tested


def edge_maps():
    answer = []
    for permutation in permutations(range(8)):
        answer.append(tuple(core.EDGE_INDEX[
            min(permutation[u], permutation[v]), max(permutation[u], permutation[v])
        ] for u, v in core.EDGES))
    return tuple(answer)


def transform(mask, mapping):
    output = 0
    while mask:
        bit = mask & -mask
        index = bit.bit_length() - 1
        output |= 1 << mapping[index]
        mask ^= bit
    return output


def graph_types(all_masks):
    """Classify only the encountered labelled graphs, orbit-by-orbit."""
    remaining = set(all_masks)
    maps = edge_maps()
    records = []
    while remaining:
        seed = min(remaining)
        orbit = {transform(seed, mapping) for mapping in maps}
        encountered = remaining.intersection(orbit)
        require(encountered, "graph orbit failed to meet its seed")
        remaining.difference_update(encountered)
        degree_sequence = tuple(sorted(core.degrees(seed), reverse=True))
        records.append({
            "canonical_mask": min(orbit),
            "full_labelled_orbit_size": len(orbit),
            "encountered_masks": len(encountered),
            "edges": seed.bit_count(),
            "degree_sequence": list(degree_sequence),
        })
    return records


def deletion_control(orbit_records, masks_by_orbit):
    fired = []
    for record in orbit_records:
        selected = selected_from_record(record)
        initial = core.graph_mask(selected)
        for mask in masks_by_orbit[record["orbit"]]:
            additions = mask & ~initial
            for index in range(28):
                if additions & (1 << index):
                    mutant = mask & ~(1 << index)
                    if not core.arm_property(mutant, selected):
                        fired.append({"orbit": record["orbit"],
                                      "deleted_edge": list(core.EDGES[index])})
                        break
            if fired and fired[-1]["orbit"] == record["orbit"]:
                break
    require(fired, "floor deletion mutation did not fire")
    return fired


def main():
    upstream_path = HERE / "results.json"
    upstream_sha = sha256(upstream_path.read_bytes()).hexdigest()
    upstream = json.loads(upstream_path.read_text())
    require(upstream["status"] == "PASS", "upstream quotient audit not passing")
    orbit_records = upstream["pure_matching_orbits"]["records"]
    require(len(orbit_records) == 31, "upstream orbit count")

    records = []
    masks_by_orbit = {}
    all_masks = set()
    for record in orbit_records:
        masks, tested = floor_masks(record)
        masks_by_orbit[record["orbit"]] = masks
        all_masks.update(masks)
        records.append({
            "orbit": record["orbit"],
            "selected_physical_pairs": record["selected_physical_pairs"],
            "minimum_total_physical_pairs": record["minimum_total_physical_pairs"],
            "augmentation_size": record["minimum_additional_physical_pairs"],
            "candidate_augmentations": tested,
            "surviving_floor_supports": len(masks),
            "floor_masks": masks,
        })

    types = graph_types(all_masks)
    mutations = deletion_control(orbit_records, masks_by_orbit)
    require(any(item["minimum_total_physical_pairs"] == 16
                and item["surviving_floor_supports"] > 0 for item in records),
            "unique 16-edge floor stratum vanished")

    result = {
        "schema": "codex.x4_quotient_floor_supports.v1",
        "status": "PASS",
        "scope": "all orbitwise minimum physical-pair augmentations satisfying the necessary arm condition",
        "upstream_results_sha256": upstream_sha,
        "summary": {
            "orbits": len(records),
            "distinct_encountered_labelled_masks": len(all_masks),
            "unlabelled_physical_graph_types": len(types),
            "floor_support_histogram": dict(sorted(Counter(
                record["minimum_total_physical_pairs"] for record in records
            ).items())),
            "survivor_count_by_floor": {
                floor: sum(record["surviving_floor_supports"] for record in records
                           if record["minimum_total_physical_pairs"] == floor)
                for floor in sorted(set(record["minimum_total_physical_pairs"]
                                        for record in records))
            },
        },
        "orbit_records": records,
        "physical_graph_types": types,
        "controls": {
            "necessary_edge_deletion_mutations": mutations,
        },
    }
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    output_path = HERE / "floor_supports.json"
    output_path.write_text(payload)
    print(json.dumps({
        "status": result["status"],
        "survivors": result["summary"]["survivor_count_by_floor"],
        "graph_types": len(types),
        "sha256": sha256(payload.encode()).hexdigest(),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
