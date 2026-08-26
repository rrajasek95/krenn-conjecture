#!/usr/bin/env python3
"""Structural census of the frozen 884-row c<=6 residual; no closure/rank."""

from collections import Counter
from hashlib import sha256
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
UP = ROOT / "computations/unaudited-codex-orbit0-k16-coloured-necklace-referee-2026-08-23"
ROWS = UP / "c7_certified_reduction_residual.tsv"
C6_SOURCE = (ROOT / "computations/unaudited-codex-orbit0-k16-c6-schur-boundary-2026-08-23"
             / "audit_k16_c6_schur_boundary.py")
OUT = HERE / "results_c6_residual_structure.json"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    require(spec.loader is not None, path)
    spec.loader.exec_module(module)
    return module


def necklace(word):
    word = tuple(word)
    candidates = []
    for base in (word, tuple(reversed(word))):
        candidates.extend(base[index:] + base[:index]
                          for index in range(len(base)))
    return min(candidates)


def coloured_state(row, cells):
    adjacency = [[] for _ in range(24)]
    edges = []
    for cell in row:
        u, v, a, b = cells[cell]
        left, right = 3 * u + a, 3 * v + b
        edge = len(edges)
        edges.append((left, right))
        adjacency[left].append(edge)
        adjacency[right].append(edge)
    require(set(map(len, adjacency)) == {2}, "non-2-regular row")
    used = set()
    cycles = []
    for first_edge in range(len(edges)):
        if first_edge in used:
            continue
        start, _ = edges[first_edge]
        vertex, edge = start, first_edge
        word = []
        while edge not in used:
            used.add(edge)
            word.append(vertex % 3)
            left, right = edges[edge]
            vertex = right if vertex == left else left
            choices = [candidate for candidate in adjacency[vertex]
                       if candidate != edge]
            require(len(choices) == 1, (row.hex(), vertex, choices))
            edge = choices[0]
        cycles.append(necklace(word))
    require(sum(map(len, cycles)) == 24, row.hex())
    return tuple(sorted(cycles, key=lambda value: (len(value), value)))


def factor_gcd(rows):
    common = Counter(rows[0])
    for row in rows[1:]:
        common &= Counter(row)
    return bytes(sorted(common.elements()))


def main():
    C6 = load("c6_residual_structural_provider", C6_SOURCE)
    HQ, D24, F, H = C6.HQ, C6.D24, C6.F, C6.H
    records = []
    with ROWS.open() as stream:
        require(next(stream).strip() == "row\tcoefficient", "bad TSV header")
        for line in stream:
            row_hex, coefficient = line.rstrip().split("\t")
            records.append((bytes.fromhex(row_hex), int(coefficient)))
    require(len(records) == 884, len(records))
    coefficient_histogram = Counter(coefficient for _row, coefficient in records)
    rows = tuple(row for row, _ in records)
    require(len(set(rows)) == 884, "duplicate residual H representative")
    require(all(HQ.canonical_row(row) == row for row in rows),
            "noncanonical residual representative")

    profile = Counter()
    cycle_partitions = Counter()
    necklaces = Counter()
    content_types = Counter()
    stabilizers = Counter()
    orbit_sizes = Counter()
    invariant_factor_degrees = Counter()
    pivot_reasons = Counter()
    monochromatic_cycle_by_pivot_status = Counter()
    unpivotable = []
    by_profile = {}
    for row, coefficient in records:
        partition, _ids = C6.graph_data(row)
        state = coloured_state(row, D24.BASE.CELLS)
        require(tuple(map(len, state)) == partition,
                (row.hex(), partition, tuple(map(len, state))))
        degree = D24.row_k_degree(row)
        cycles = len(partition)
        profile[(degree, cycles)] += 1
        cycle_partitions[partition] += 1
        necklaces[state] += 1
        contents = tuple(sorted((word.count(0), word.count(1), word.count(2))
                                for word in state))
        content_types[contents] += 1
        images = {F.move_row(row, action) for action in H}
        orbit_sizes[len(images)] += 1
        stabilizers[len(H) // len(images)] += 1
        orbit_factor = factor_gcd(tuple(images))
        invariant_factor_degrees[(len(orbit_factor),
                                  sum(cell in D24.ANCHORS
                                      for cell in orbit_factor))] += 1
        pivot = C6.eligible_pivot(row)
        has_mono = any(sum(value > 0 for value in content) == 1
                       for content in contents)
        if pivot is None:
            reason = ("fewer_than_four_cycles" if cycles < 4
                      else "no_physical_pm_across_four_cycles")
            unpivotable.append((row, coefficient, degree, partition,
                                state, contents, reason))
            pivot_reasons[reason] += 1
            monochromatic_cycle_by_pivot_status[("unpivotable", has_mono)] += 1
        else:
            pivot_reasons["pivotable"] += 1
            monochromatic_cycle_by_pivot_status[("pivotable", has_mono)] += 1
        by_profile.setdefault((degree, cycles), []).append(row)

    packet_gcd = factor_gcd(rows)
    profile_gcds = {
        f"K{degree}c{cycles}": {
            "rows": len(group),
            "gcd_degree": len(factor_gcd(tuple(group))),
            "gcd_anchor_degree": sum(cell in D24.ANCHORS
                                     for cell in factor_gcd(tuple(group))),
            "gcd": factor_gcd(tuple(group)).hex(),
        }
        for (degree, cycles), group in sorted(by_profile.items())
    }

    unp_partition = Counter(item[3] for item in unpivotable)
    unp_content = Counter(item[5] for item in unpivotable)
    unp_necklace = Counter(item[4] for item in unpivotable)
    small_signature = Counter(
        (item[2], item[3], item[5]) for item in unpivotable)
    # A genuinely small universal support invariant is recorded only if one
    # coordinate is common to every unpivotable row.
    universal = {}
    if unpivotable:
        universal = {
            "K_degrees": sorted({item[2] for item in unpivotable}),
            "cycle_counts": sorted({len(item[3]) for item in unpivotable}),
            "has_monochromatic_cycle_values": sorted({
                any(sum(value > 0 for value in content) == 1
                    for content in item[5]) for item in unpivotable}),
            "all_cycles_mixed_values": sorted({
                all(sum(value > 0 for value in content) > 1
                    for content in item[5]) for item in unpivotable}),
        }

    result = {
        "status": "PASS exact 884-row structural census",
        "input_rows": len(records),
        "input_sha256": sha256(ROWS.read_bytes()).hexdigest(),
        "H_order": len(H),
        "H_orbits": len(records),
        "coefficient_histogram": dict(sorted(coefficient_histogram.items())),
        "signed_quotient_mass": sum(coefficient for _row, coefficient in records),
        "absolute_quotient_mass": sum(abs(coefficient)
                                      for _row, coefficient in records),
        "K_cycle_profile": {f"{k},{c}": n for (k, c), n in sorted(profile.items())},
        "cycle_partition_types": len(cycle_partitions),
        "cycle_partition_histogram": {
            "+".join(map(str, key)): value
            for key, value in sorted(cycle_partitions.items())},
        "coloured_necklace_types": len(necklaces),
        "cycle_content_types": len(content_types),
        "stabilizer_size_histogram": dict(sorted(stabilizers.items())),
        "H_orbit_size_histogram": dict(sorted(orbit_sizes.items())),
        "H_orbit_invariant_factor_degree_histogram": {
            f"degree{degree}_anchor{anchor}": count
            for (degree, anchor), count in sorted(invariant_factor_degrees.items())},
        "packet_common_factor": {
            "degree": len(packet_gcd),
            "anchor_degree": sum(cell in D24.ANCHORS for cell in packet_gcd),
            "cells": packet_gcd.hex(),
        },
        "profile_common_factors": profile_gcds,
        "cycle_Morse": {
            "reason_histogram": dict(sorted(pivot_reasons.items())),
            "pivotable": pivot_reasons["pivotable"],
            "unpivotable": len(unpivotable),
            "monochromatic_cycle_by_status": {
                f"{status},mono={str(mono).lower()}": count
                for (status, mono), count
                in sorted(monochromatic_cycle_by_pivot_status.items())},
        },
        "unpivotable_subset": {
            "cycle_partition_types": len(unp_partition),
            "cycle_partition_histogram": {
                "+".join(map(str, key)): value
                for key, value in sorted(unp_partition.items())},
            "cycle_content_types": len(unp_content),
            "cycle_content_histogram": {
                ";".join(",".join(map(str, part)) for part in key): value
                for key, value in sorted(unp_content.items())},
            "coloured_necklace_types": len(unp_necklace),
            "small_K_partition_content_signatures": len(small_signature),
            "universal_small_tests": universal,
            "first_rows": [
                {"row": row.hex(), "coefficient": coefficient,
                 "K_degree": degree, "cycle_partition": list(partition),
                 "reason": reason}
                for row, coefficient, degree, partition, _state, _contents, reason
                in unpivotable[:12]
            ],
        },
        "scope": "Frozen 884 H-coinvariant rows only; no incidence closure or rank.",
        "pinned_provider_sha256": sha256(C6_SOURCE.read_bytes()).hexdigest(),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["logical_sha256"] = sha256(logical.encode()).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "rows": len(records), "profiles": result["K_cycle_profile"],
        "necklace_types": len(necklaces), "stabilizers": dict(stabilizers),
        "pivot_reasons": dict(pivot_reasons),
        "unpivotable_small_signatures": len(small_signature),
        "logical_sha256": result["logical_sha256"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
