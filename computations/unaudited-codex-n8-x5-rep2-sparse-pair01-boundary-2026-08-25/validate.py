#!/usr/bin/env python3
"""Fail-closed small-file validation of the sealed double-boundary audit."""

from __future__ import annotations

import hashlib
import itertools
import json
import os
from pathlib import Path


HERE = Path(__file__).resolve().parent


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    audit = json.loads((HERE / "results_double_boundary_audit.json").read_text())
    assert audit["status"] == "PASS_EXACT_NO_FULL_PAIR01_POINT_WITH_AT_MOST_TWO_EXTRA_COORDINATES"
    assert audit["coordinate_counts"] == {"amplitude": 87, "base_live": 17, "zero": 70}
    assert audit["base"] == {"charts": 1, "unit": 1, "nonunit": 0}
    assert audit["single"] == {"raw_charts": 70, "normalized_groups": 28, "unit_groups": 28, "nonunit": 0}
    assert audit["double"] == {"raw_charts": 2415, "normalized_groups": 381, "unit_groups": 381, "nonunit": 0}
    assert audit["exact_minimum_extra_coordinate_lower_bound"] == 3
    assert audit["regenerated_normalization_checks"] == 2485
    assert audit["independent_singular_unit_replays"] == 410

    single = json.loads((HERE / "single_relaxation_ledger.json").read_text())
    double = json.loads((HERE / "double_relaxation_ledger.json").read_text())
    single_run = json.loads((HERE / "results_single_relaxations.json").read_text())
    double_run = json.loads((HERE / "results_double_search.json").read_text())
    zero = sorted(item["extra"] for item in single["records"])
    assert len(zero) == 70 and len(set(zero)) == 70
    assert {tuple(item["pair"]) for item in double["pair_records"]} == set(itertools.combinations(zero, 2))
    assert sum(len(group["members"]) for group in single["normalized_polynomial_groups"]) == 70
    assert sum(len(group["members"]) for group in double["groups"]) == 2415
    assert all(group["status"] == "UNIT_IDEAL" for group in single_run["groups"])
    assert all(group["status"] == "UNIT_IDEAL" for group in double_run["attempts"])
    assert not single_run["nonunit_coordinates"] and double_run["winner"] is None
    assert audit["parent_core_point_scope"]["full_pair01"] is False
    assert audit["parent_core_point_scope"]["rank1_guard_A06v"] is False
    assert audit["parent_core_point_scope"]["cap45_inactivity_incidence"] is False

    result = {
        "schema": "KRENN_X5_REP2_SPARSE_PAIR01_DOUBLE_BOUNDARY_VALIDATION_V1",
        "status": "PASS",
        "audit_sha256": sha256(HERE / "results_double_boundary_audit.json"),
        "raw_chart_set_checks": 1 + 70 + 2415,
        "normalized_group_status_checks": 1 + 28 + 381,
        "hostile_scope_checks": 3,
        "exact_lower_bound": 3,
    }
    output = HERE / "results_validation.json"
    temporary = output.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, output)
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
