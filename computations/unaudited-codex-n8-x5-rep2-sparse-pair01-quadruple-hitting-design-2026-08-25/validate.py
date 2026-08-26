#!/usr/bin/env python3
"""Fail-closed validator for the scoped fixed-base hitting theorem."""

from __future__ import annotations

import hashlib
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
    ledger = json.loads((HERE / "hitting_support_ledger.json").read_text())
    audit = json.loads((HERE / "results_hitting_audit.json").read_text())
    assert ledger["status"] == "PASS_DESIGN_ONLY_NO_Q_IDEALS_RUN"
    assert ledger["hitting_support_counts"] == {"0": 0, "1": 0, "2": 0, "3": 0, "4": 0}
    assert ledger["minimal_size4_hitting_support_count"] == ledger["normalized_group_count"] == 0
    assert ledger["minimum_fixed_base_hitting_size"] == 7
    assert ledger["minimum_fixed_base_hitting_support_count"] == 6
    assert ledger["inclusion_minimal_hitting_support_count"] == 259
    assert ledger["launch_gate"]["no_q_ideals_run"] is True
    assert audit["status"] == "PASS_SCOPED_FIXED_BASE_MINIMUM_SEVEN_NO_SIZE4_SUPPORT"
    assert audit["minimum_coordinate_deletion_hostiles"] == 42
    assert audit["scope"]["not_a_global_quadruple_filter"] is True
    assert audit["scope"]["not_necessary_for"] == "arbitrary points of the base17+S chart where the 17 base coordinates may move"
    result = {
        "schema": "KRENN_X5_REP2_FIXED_BASE_HITTING_VALIDATION_V1",
        "status": "PASS",
        "ledger_sha256": sha256(HERE / "hitting_support_ledger.json"),
        "audit_sha256": sha256(HERE / "results_hitting_audit.json"),
        "size4_supports": 0,
        "fixed_base_minimum": 7,
        "fixed_base_minimum_supports": 6,
        "scope_hostiles": 3,
    }
    output = HERE / "results_validation.json"
    temporary = output.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, output)
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
