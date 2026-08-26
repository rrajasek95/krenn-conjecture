#!/usr/bin/env python3
"""Seal the tiny quotient diagnostic without converting it into coverage."""

from __future__ import annotations

import copy
import hashlib
import json
import os
from pathlib import Path


if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def validate(result):
    assert result["schema"] == "KRENN_X5_REP1_INCIDENCE_PIVOT_TERMINAL_AUDIT_V1"
    assert result["status"] == "PASS_DESIGN_TINY_WALL_ZERO_COVERAGE"
    assert result["design_status"] == "PASS_EXACT_CONTRACTION_DESIGN"
    assert result["diagnostic"] == {"runs": 1, "unit_results": 0, "nonunit_results": 0, "exact_Q_runs": 0, "mathematical_coverage": False}
    assert result["scope"] == {"rep1_closed": False, "other_charts_run": False, "D12_reads": False}


def hostile(result, mutation):
    candidate = copy.deepcopy(result)
    mutation(candidate)
    try:
        validate(candidate)
    except (AssertionError, KeyError, TypeError):
        return True
    return False


def main():
    assert sha256(HERE / "DESIGN_MANIFEST.sha256") == "993aa587b2c092e6d422366e65b5ac3a2d4897443cddbbe574c8edb253d268d6"
    design = json.loads((HERE / "results_design_audit.json").read_text())
    assert design["status"] == "PASS_EXACT_CONTRACTION_DESIGN"
    run = json.loads((HERE / "results_tiny_diagnostic.json").read_text())
    assert run["schema"] == "KRENN_X5_REP1_INCIDENCE_PIVOT_TINY_DIAGNOSTIC_V1"
    assert run["status"] == "FAIL_CLOSED_RESOURCE_DIAGNOSTIC"
    assert run["termination"] == "WALL_CAP_15" and run["mathematical_coverage"] is False
    assert run["rss_cap_bytes"] == 4 * 1024**3 and run["observed_peak_rss_bytes"] < run["rss_cap_bytes"]
    assert run["input_sha256"] == "b54e527887fd9fe250d24f21d932f6f25a0ddb6d38e36c03328d2c1ca91d02e3"
    assert "INPUT_GENERATORS=6580" in run["stdout"]
    assert "STATUS=UNIT_IDEAL" not in run["stdout"] and "STATUS=NONUNIT_OR_UNRESOLVED" not in run["stdout"]
    assert not list(HERE.glob("*Q*.json"))
    result = {
        "schema": "KRENN_X5_REP1_INCIDENCE_PIVOT_TERMINAL_AUDIT_V1",
        "status": "PASS_DESIGN_TINY_WALL_ZERO_COVERAGE",
        "design_status": "PASS_EXACT_CONTRACTION_DESIGN",
        "design_manifest_sha256": sha256(HERE / "DESIGN_MANIFEST.sha256"),
        "diagnostic_result_sha256": sha256(HERE / "results_tiny_diagnostic.json"),
        "resource_evidence": {"wall_seconds": run["wall_seconds"], "peak_rss_bytes": run["observed_peak_rss_bytes"], "termination": run["termination"]},
        "diagnostic": {"runs": 1, "unit_results": 0, "nonunit_results": 0, "exact_Q_runs": 0, "mathematical_coverage": False},
        "scope": {"rep1_closed": False, "other_charts_run": False, "D12_reads": False},
    }
    validate(result)
    tests = {
        "coverage_overclaim": hostile(result, lambda item: item["diagnostic"].__setitem__("mathematical_coverage", True)),
        "unit_overclaim": hostile(result, lambda item: item["diagnostic"].__setitem__("unit_results", 1)),
        "closure_overclaim": hostile(result, lambda item: item["scope"].__setitem__("rep1_closed", True)),
        "Q_overclaim": hostile(result, lambda item: item["diagnostic"].__setitem__("exact_Q_runs", 1)),
        "D12_scope_mutation": hostile(result, lambda item: item["scope"].__setitem__("D12_reads", True)),
    }
    assert all(tests.values())
    result["hostile_tests"] = tests
    temporary = HERE / "results_terminal_audit.json.tmp"
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, HERE / "results_terminal_audit.json")
    print(json.dumps({"status": result["status"], "coverage": 0, "hostiles": len(tests)}, sort_keys=True))


if __name__ == "__main__":
    main()
