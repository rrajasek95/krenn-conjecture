#!/usr/bin/env python3
"""Compare the 28 -> 8 -> 24 boundary supports without expanding tails."""

from __future__ import annotations

from collections import Counter
from functools import lru_cache
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import time


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
C6_DIR = ROOT / "computations/unaudited-codex-orbit0-k16-c6-schur-boundary-2026-08-23"
C6_SCRIPT = C6_DIR / "audit_k16_c6_schur_boundary.py"
C6_RESULT = C6_DIR / "results_k16_c6_schur_boundary.json"
SCHUR = HERE / "results_c6_boundary_schur_lift.json"
C7_LIFT = HERE / "results_c7_pair_schur_lift.json"
OUT = HERE / "results_boundary_recurrence.json"
TIME_CAP = 115.0


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    require(spec.loader is not None, path)
    spec.loader.exec_module(module)
    return module


def packet_gcd(rows):
    common = Counter(rows[0])
    for row in rows[1:]:
        common &= Counter(row)
    return bytes(sorted(common.elements()))


def contained(left, right):
    return all(right.get(cell, 0) >= multiplicity
               for cell, multiplicity in left.items())


def main():
    started = time.monotonic()
    C6 = load("boundary_recurrence_c6", C6_SCRIPT)
    HQ, D24, F, H = C6.HQ, C6.D24, C6.F, C6.H
    first_data = json.loads(C6_RESULT.read_text())
    second_data = json.loads(SCHUR.read_text())
    third_data = json.loads(C7_LIFT.read_text())
    first = tuple(HQ.canonical_row(bytes.fromhex(record["row"]))
                  for record in first_data["blockers"])
    second = tuple(bytes.fromhex(record["row"])
                   for record in second_data["uncertified_high_rows"])
    third = tuple(bytes.fromhex(record["row"])
                  for record in third_data["frontier_rows"])
    require((len(first), len(second), len(third)) == (28, 8, 24),
            (len(first), len(second), len(third)))
    require(all(HQ.canonical_row(row) == row for row in first + second + third),
            "noncanonical boundary representative")

    groups = {"first28": first, "second8": second, "third24": third}

    def group_profile(rows):
        return {
            "support": len(rows),
            "K_degree_histogram": dict(sorted(Counter(
                D24.row_k_degree(row) for row in rows).items())),
            "cycle_partition_histogram": {
                "+".join(map(str, key)): value
                for key, value in sorted(Counter(
                    C6.graph_data(row)[0] for row in rows).items())
            },
            "packet_gcd_cells": packet_gcd(rows).hex(),
            "packet_gcd_degree": len(packet_gcd(rows)),
            "packet_gcd_anchor_degree": sum(
                cell in D24.ANCHORS for cell in packet_gcd(rows)),
        }

    profiles = {name: group_profile(rows) for name, rows in groups.items()}
    exact_intersections = {
        "third_vs_first": len(set(third) & set(first)),
        "third_vs_second": len(set(third) & set(second)),
        "second_vs_first": len(set(second) & set(first)),
    }

    @lru_cache(None)
    def moved_nonanchor_orbit(row):
        answer = set()
        for action in H:
            moved = F.move_row(row, action)
            answer.add(bytes(cell for cell in moved if cell not in D24.ANCHORS))
        return tuple(sorted(answer))

    @lru_cache(None)
    def moved_full_orbit(row):
        return tuple(sorted({F.move_row(row, action) for action in H}))

    def compare_to_prior(prior):
        exact_offanchor = 0
        nested_offanchor = 0
        maximum_full_overlap_histogram = Counter()
        maximum_nonanchor_overlap_histogram = Counter()
        for current in third:
            current_counter = Counter(current)
            current_nonanchor = Counter(cell for cell in current
                                        if cell not in D24.ANCHORS)
            exact_here = False
            nested_here = False
            best_full = 0
            best_nonanchor = 0
            for old in prior:
                old_k = D24.row_k_degree(old)
                current_k = D24.row_k_degree(current)
                for moved in moved_full_orbit(old):
                    best_full = max(best_full,
                                    sum((Counter(moved) & current_counter).values()))
                for moved_nonanchor in moved_nonanchor_orbit(old):
                    moved_counter = Counter(moved_nonanchor)
                    overlap = sum((moved_counter & current_nonanchor).values())
                    best_nonanchor = max(best_nonanchor, overlap)
                    if old_k == current_k and moved_counter == current_nonanchor:
                        exact_here = True
                    smaller, larger = ((moved_counter, current_nonanchor)
                                       if old_k <= current_k else
                                       (current_nonanchor, moved_counter))
                    if contained(smaller, larger):
                        nested_here = True
            exact_offanchor += exact_here
            nested_offanchor += nested_here
            maximum_full_overlap_histogram[best_full] += 1
            maximum_nonanchor_overlap_histogram[best_nonanchor] += 1
        return {
            "third_rows_with_equal_offanchor_skeleton": exact_offanchor,
            "third_rows_with_K_shift_nested_offanchor_skeleton": nested_offanchor,
            "max_full_monomial_overlap_histogram": dict(
                sorted(maximum_full_overlap_histogram.items())),
            "max_nonanchor_overlap_histogram": dict(
                sorted(maximum_nonanchor_overlap_histogram.items())),
        }

    transport_tests = {
        "against_first28": compare_to_prior(first),
        "against_second8": compare_to_prior(second),
    }

    incident_profiles = []
    aggregate_cycle_selection = Counter()
    eligible_count = 0
    total_incident = 0
    for row in third:
        partition, cycle_ids = C6.graph_data(row)
        incident = D24.incident_degree24_columns(row)
        histogram = Counter()
        for word, multiplier in incident:
            remaining = list(row)
            for cell in multiplier:
                remaining.remove(cell)
            require(len(remaining) == 4, (row.hex(), len(remaining)))
            selected_cycles = []
            for cell in remaining:
                u, v, a, b = D24.BASE.CELLS[cell]
                require(cycle_ids[3 * u + a] == cycle_ids[3 * v + b], cell)
                selected_cycles.append(cycle_ids[3 * u + a])
            histogram[len(set(selected_cycles))] += 1
        aggregate_cycle_selection.update(histogram)
        eligible = C6.eligible_pivot(row) is not None
        eligible_count += eligible
        total_incident += len(incident)
        incident_profiles.append({
            "row": row.hex(),
            "K_degree": D24.row_k_degree(row),
            "cycle_partition": list(partition),
            "incident_mixed_columns": len(incident),
            "selected_distinct_cycle_count_histogram": {
                str(key): value for key, value in sorted(histogram.items())
            },
            "has_certified_four_distinct_cycle_pivot": eligible,
        })
        require(time.monotonic() - started < TIME_CAP,
                ("time cap", len(incident_profiles)))

    genuinely_new = (
        exact_intersections["third_vs_first"] == 0
        and exact_intersections["third_vs_second"] == 0
        and transport_tests["against_first28"]
            ["third_rows_with_equal_offanchor_skeleton"] == 0
        and transport_tests["against_second8"]
            ["third_rows_with_equal_offanchor_skeleton"] == 0
    )
    result = {
        "schema": "orbit0-k16-boundary-recurrence-v1",
        "status": "GENUINELY_NEW_24_ROW_BOUNDARY_TYPES" if genuinely_new
                  else "PRIOR_BOUNDARY_TRANSPORT_DETECTED",
        "profiles": profiles,
        "exact_H_orbit_intersections": exact_intersections,
        "transport_and_deletion_tests": transport_tests,
        "third_boundary_incident_PM_profile": {
            "rows": len(third),
            "total_incident_mixed_columns_with_row_multiplicity": total_incident,
            "aggregate_selected_distinct_cycle_count_histogram": {
                str(key): value for key, value in
                sorted(aggregate_cycle_selection.items())
            },
            "rows_with_certified_four_distinct_cycle_pivot": eligible_count,
            "rows_without_certified_pivot": len(third) - eligible_count,
            "rows_detail": incident_profiles,
        },
        "theorem_scope": (
            "H-orbit equality, anchor-stripped skeleton equality, and one-sided "
            "nonanchor divisibility under every H transport. Skeleton nesting is "
            "reported only as combinatorial deletion data, not module membership. "
            "No source tails were expanded."
        ),
        "pinned": {
            "first_boundary_logical": first_data["logical_sha256"],
            "second_boundary_schur_logical": second_data["logical_sha256"],
            "third_boundary_lift_logical": third_data["logical_sha256"],
        },
        "elapsed_seconds": time.monotonic() - started,
    }
    logical = dict(result)
    logical.pop("elapsed_seconds")
    result["logical_sha256"] = sha256(json.dumps(
        logical, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "profiles": profiles,
        "exact_intersections": exact_intersections,
        "transport_tests": transport_tests,
        "incident_PM_summary": {
            "total": total_incident,
            "cycle_selection": dict(sorted(aggregate_cycle_selection.items())),
            "eligible_rows": eligible_count,
        },
        "logical_sha256": result["logical_sha256"],
        "elapsed_seconds": result["elapsed_seconds"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
