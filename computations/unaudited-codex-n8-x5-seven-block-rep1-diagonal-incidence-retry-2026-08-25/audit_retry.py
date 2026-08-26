#!/usr/bin/env python3
"""Audit the rep1 resource-only retry as zero mathematical coverage."""

from __future__ import annotations

import copy
import hashlib
import json
import os
from pathlib import Path


if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PARENT = ROOT / "computations/unaudited-codex-n8-x5-seven-block-rep1-diagonal-incidence-gate-2026-08-25"


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def validate(result):
    assert result["schema"] == "KRENN_X5_REP1_DIAGONAL_INCIDENCE_RETRY_AUDIT_V1"
    assert result["status"] == "FAIL_CLOSED_NATIVE180_ZERO_COVERAGE"
    assert result["coverage"] == {"modular_units": 0, "exact_Q_units": 0, "representative_1_closed": False}
    assert result["launch_census"] == {"modular_lanes": 1, "exact_Q_lanes": 0, "later_charts": 0}
    assert result["algebra_changed"] is False


def hostile(result, mutation):
    candidate = copy.deepcopy(result)
    mutation(candidate)
    try:
        validate(candidate)
    except (AssertionError, KeyError, TypeError):
        return True
    return False


def main():
    assert sha256(PARENT / "MANIFEST.sha256") == "36e39752896a052d8bfe75af29c39c4d8c09c090afb8a9692e818a63c9a811bf"
    assert sha256(PARENT / "results_modular_p00.json") == "119d02ac5ea337303f34b9b4285821305169e7d9420cf976521c0b645ef936b3"
    assert sha256(HERE / "DESIGN_MANIFEST.sha256") == "d5a4a1f4650b73ed390b9c6110034a269c97b652dff1c3ba9603a5b68f4494e2"
    run = json.loads((HERE / "results_p00_p32003.json").read_text())
    assert run["schema"] == "KRENN_X5_REP1_DIAGONAL_INCIDENCE_RETRY_LANE_V1"
    assert run["status"] == "FAIL_CLOSED_RESOURCE_GATE" and run["mathematical_coverage"] is False
    assert run["termination"] == "NATIVE_WALL_CAP_180"
    assert run["native_wall_cap_seconds"] == 180 and run["wrapper_wall_cap_seconds"] == 190
    assert run["rss_cap_bytes"] == 8 * 1024**3 and run["observed_peak_rss_bytes"] < run["rss_cap_bytes"]
    assert run["input_sha256"] == "7ce1d68dad3bb3f27b0cb7ee481be541017fa76aab29d2499f40403e87693dba"
    assert run["sealed_60s_failure_manifest_sha256"] == "36e39752896a052d8bfe75af29c39c4d8c09c090afb8a9692e818a63c9a811bf"
    assert "INPUT_GENERATORS=6586" in run["stdout"]
    assert "STATUS=UNIT_IDEAL" not in run["stdout"] and "STATUS=NONUNIT_OR_UNRESOLVED" not in run["stdout"]
    assert not (HERE / "results_p00_Q.json").exists()
    for chart in ("p01", "p10", "p11", "p12"):
        assert not (HERE / f"results_{chart}_p32003.json").exists()
        assert not (HERE / f"results_{chart}_Q.json").exists()

    result = {
        "schema": "KRENN_X5_REP1_DIAGONAL_INCIDENCE_RETRY_AUDIT_V1",
        "status": "FAIL_CLOSED_NATIVE180_ZERO_COVERAGE",
        "run_result": "results_p00_p32003.json",
        "run_result_sha256": sha256(HERE / "results_p00_p32003.json"),
        "resource_evidence": {
            "wall_seconds": run["wall_seconds"],
            "peak_rss_bytes": run["observed_peak_rss_bytes"],
            "termination": run["termination"],
        },
        "coverage": {"modular_units": 0, "exact_Q_units": 0, "representative_1_closed": False},
        "launch_census": {"modular_lanes": 1, "exact_Q_lanes": 0, "later_charts": 0},
        "algebra_changed": False,
        "scope": "representative 1 p00 incidence retry only; rep1 remains open",
    }
    validate(result)
    tests = {
        "modular_overclaim": hostile(result, lambda item: item["coverage"].__setitem__("modular_units", 1)),
        "Q_overclaim": hostile(result, lambda item: item["launch_census"].__setitem__("exact_Q_lanes", 1)),
        "closure_overclaim": hostile(result, lambda item: item["coverage"].__setitem__("representative_1_closed", True)),
        "algebra_mutation": hostile(result, lambda item: item.__setitem__("algebra_changed", True)),
    }
    assert all(tests.values())
    result["hostile_tests"] = tests
    temporary = HERE / "results_retry_audit.json.tmp"
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, HERE / "results_retry_audit.json")
    print(json.dumps({"status": result["status"], "coverage": 0, "hostiles": len(tests)}, sort_keys=True))


if __name__ == "__main__":
    main()
