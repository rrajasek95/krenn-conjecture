#!/usr/bin/env python3
"""Fail-closed small-file validation of the exhaustive triple boundary."""

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
    ledger = json.loads((HERE / "triple_group_ledger.json").read_text())
    run = json.loads((HERE / "results_triple_groups.json").read_text())
    audit = json.loads((HERE / "results_triple_boundary_audit.json").read_text())
    assert ledger["status"] == "PASS_ENUMERATION_ONLY_NO_IDEALS_RUN"
    assert ledger["raw_triple_count"] == 54740 and ledger["normalized_group_count"] == 3366
    assert run["status"] == "PASS_ALL_TRIPLE_GROUPS_UNIT"
    assert run["attempt_count"] == run["unit_count"] == 3366
    assert run["attempted_raw_chart_coverage"] == 54740
    assert run["nonunit_count"] == run["failure_count"] == 0
    assert run["max_lane_wall_seconds"] < run["per_lane_wall_cap_seconds"] == 2
    assert run["aggregate_wall_seconds"] < run["aggregate_wall_cap_seconds"] == 900
    assert audit["status"] == "PASS_EXACT_NO_FULL_PAIR01_POINT_WITH_AT_MOST_THREE_EXTRA_COORDINATES"
    assert audit["raw_normalization_hash_replays"] == 54740
    assert audit["canonical_q_unit_replays"] == 3366
    assert audit["exact_minimum_extra_coordinate_lower_bound"] == 4

    records = {tuple(item["triple"]): item["normalized_sha256"] for item in ledger["triple_records"]}
    zero = sorted({coordinate for triple in records for coordinate in triple})
    assert len(zero) == 70
    assert set(records) == set(itertools.combinations(zero, 3))
    grouped = {
        tuple(triple): group["normalized_sha256"]
        for group in ledger["groups"] for triple in group["members"]
    }
    assert grouped == records
    assert len({group["normalized_sha256"] for group in ledger["groups"]}) == 3366
    assert all(item["status"] == "UNIT_IDEAL" for item in run["attempts"])

    result = {
        "schema": "KRENN_X5_REP2_SPARSE_TRIPLE_BOUNDARY_VALIDATION_V1",
        "status": "PASS",
        "ledger_sha256": sha256(HERE / "triple_group_ledger.json"),
        "run_sha256": sha256(HERE / "results_triple_groups.json"),
        "audit_sha256": sha256(HERE / "results_triple_boundary_audit.json"),
        "raw_triple_set_checks": 54740,
        "normalized_group_checks": 3366,
        "exact_lower_bound": 4,
        "scope_hostiles": [
            "no guard/adjoint/incidence inference",
            "no >=4-coordinate coverage",
            "prior388 diagnostics excluded",
        ],
    }
    output = HERE / "results_validation.json"
    temporary = output.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, output)
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
