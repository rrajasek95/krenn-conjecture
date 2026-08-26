#!/usr/bin/env python3
"""Fail-closed validation for the metadata-only rep1 held resource plan."""

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
ANTECEDENT = ROOT / "computations/unaudited-codex-n8-x5-seven-block-rep1-incidence-pivot-quotient-2026-08-25"


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def validate(plan):
    assert plan["schema"] == "KRENN_X5_REP1_CONTRACTED_HELD180_RESOURCE_PLAN_V1"
    assert plan["status"] == "HELD_NO_LAUNCH"
    assert plan["antecedent"]["manifest_sha256"] == "87bf2d17fcd4c5b8d52ba74c3cca8ecf5a19be2878df1fc2a86c70e05e7773cc"
    assert plan["exact_input"]["sha256"] == "b54e527887fd9fe250d24f21d932f6f25a0ddb6d38e36c03328d2c1ca91d02e3"
    assert plan["exact_input"]["variables"] == 94 and plan["exact_input"]["generators"] == 6580
    assert plan["sole_resource_change"] == {"native_wall_seconds": {"from": 15, "to": 180}, "wrapper_wall_seconds": 190, "rss_cap_bytes": {"from": 4294967296, "to": 8589934592}}
    assert plan["progression"] == {"maximum_modular_lanes": 1, "exact_Q_lanes_allowed": 0, "other_chart_lanes_allowed": 0, "automatic_relaunch_allowed": False}
    assert plan["clearance_gate"] == {"D12_final_lane_terminal_required": True, "fresh_explicit_root_clearance_required": True, "current_clearance_present": False, "runner_refuses_launch_while_held": True}
    assert plan["scope"] == {"algebra_changes": False, "input_regeneration": False, "D12_reads": False, "rep1_closed": False}


def hostile(plan, mutation):
    candidate = copy.deepcopy(plan)
    mutation(candidate)
    try:
        validate(candidate)
    except (AssertionError, KeyError, TypeError):
        return True
    return False


def main():
    plan = json.loads((HERE / "held_plan.json").read_text())
    validate(plan)
    assert sha256(ANTECEDENT / "MANIFEST.sha256") == plan["antecedent"]["manifest_sha256"]
    assert sha256(ANTECEDENT / "DESIGN_MANIFEST.sha256") == plan["antecedent"]["design_manifest_sha256"]
    assert sha256(ANTECEDENT / "results_tiny_diagnostic.json") == plan["antecedent"]["diagnostic_result_sha256"]
    assert sha256(ANTECEDENT / "results_terminal_audit.json") == plan["antecedent"]["terminal_audit_sha256"]
    source = ROOT / plan["exact_input"]["path"]
    assert sha256(source) == plan["exact_input"]["sha256"]
    diagnostic = json.loads((ANTECEDENT / "results_tiny_diagnostic.json").read_text())
    assert diagnostic["termination"] == "WALL_CAP_15" and diagnostic["mathematical_coverage"] is False
    assert diagnostic["input_sha256"] == plan["exact_input"]["sha256"]
    tests = {
        "clearance_injection": hostile(plan, lambda item: item["clearance_gate"].__setitem__("current_clearance_present", True)),
        "Q_injection": hostile(plan, lambda item: item["progression"].__setitem__("exact_Q_lanes_allowed", 1)),
        "chart_injection": hostile(plan, lambda item: item["progression"].__setitem__("other_chart_lanes_allowed", 1)),
        "input_mutation": hostile(plan, lambda item: item["exact_input"].__setitem__("sha256", "0" * 64)),
        "algebra_overclaim": hostile(plan, lambda item: item["scope"].__setitem__("algebra_changes", True)),
        "D12_scope_mutation": hostile(plan, lambda item: item["scope"].__setitem__("D12_reads", True)),
        "closure_overclaim": hostile(plan, lambda item: item["scope"].__setitem__("rep1_closed", True)),
    }
    assert all(tests.values())
    result = {
        "schema": "KRENN_X5_REP1_CONTRACTED_HELD180_PLAN_AUDIT_V1",
        "status": "PASS_HELD_PLAN_NO_LAUNCH",
        "plan_sha256": sha256(HERE / "held_plan.json"),
        "antecedent_manifest_sha256": plan["antecedent"]["manifest_sha256"],
        "exact_input_sha256": plan["exact_input"]["sha256"],
        "hostile_tests": tests,
        "launches": 0,
        "D12_reads": False
    }
    temporary = HERE / "results_plan_audit.json.tmp"
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, HERE / "results_plan_audit.json")
    print(json.dumps({"status": result["status"], "launches": 0, "hostiles": len(tests)}, sort_keys=True))


if __name__ == "__main__":
    main()
