#!/usr/bin/env python3
"""Independent static referee for the remaining-four rank-one held schedule."""
from __future__ import annotations

import copy
import hashlib
import json
import os
import re
from pathlib import Path

if not __debug__:
    raise RuntimeError("assertions required")

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
COMP = ROOT / "computations"
PLAN_DIR = COMP / "unaudited-codex-n8-x5-rectangle-rank1-remaining4-exact-q-held-plan-2026-08-25"
DESIGN = COMP / "unaudited-codex-n8-x5-unmapped16-rectangle-rank12-incidence-ideal-design-2026-08-25"
DESIGN_REF = COMP / "unaudited-codex-n8-x5-unmapped16-rectangle-rank12-incidence-ideal-referee-2026-08-25"
ORBIT0 = COMP / "unaudited-codex-n8-x5-rectangle-rank1-orbit0-exact-q-run-2026-08-25"


def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        while part := stream.read(1 << 20):
            h.update(part)
    return h.hexdigest()


PINS = {
    PLAN_DIR / "HELD_PLAN.json": "e85c4db6414a47d9fb76e4310ab4bd114fc787cda2d766e032a77f9312b08575",
    PLAN_DIR / "FINAL_MANIFEST.sha256": "2fce75e1cd35178e03a42ae02aa60ac981529d229d28e0ab77d0eb51c1b7870f",
    DESIGN / "MANIFEST.sha256": "743f3e526b21890509e32077ed5bf0c38b1240d25d475e71e2e78520445c85cf",
    DESIGN / "results_rank12_incidence_design.json": "96b13ad342acd0fb02c37015b86303c9d6d7d880abe0e2a4e21f5e9e1aea5a28",
    DESIGN_REF / "FINAL_MANIFEST.sha256": "e3e7974ae201f5915e7eeec95f7b01e3db37f0ddfe69619d00a4c1a84a92838f",
    DESIGN_REF / "results_referee.json": "74394ce3858867c5221743483f7b765f49c9980c9e010e9d64262b56d09c03b4",
    ORBIT0 / "AUDIT_RESULT.json": "4da4bf9c09cf10480eb8b79aa4d24a29a5c6d75749ae9d652e1b9eb9b1377b07",
    ORBIT0 / "FINAL_MANIFEST.sha256": "b129fdc2775a1fadb5659409ed9f953351cb47d591cef4fc50f5a09276bfbc07",
}


def source_census(text):
    ring = re.search(r"^ring r=([^,]+),\(([^\n]+)\),dp;$", text, re.MULTILINE)
    assert ring
    variables = ring.group(2).split(",")
    assert len(variables) == len(set(variables)) == 76
    body = text.split("ideal I=", 1)[1].split(";", 1)[0]
    assert body.count(",\n") + 1 == 6571
    return ring.group(1), len(variables), 6571


def derive(source, epilogue):
    assert source.count("quit;") == 1
    assert source.count("slimgb(I)") == 0
    head, tail = source.rsplit("quit;", 1)
    assert not tail.strip()
    exact = head + "\n".join(epilogue) + "\nquit;" + tail
    # The producer contract replaces immediately after INPUT_GENERATORS;
    # the independent construction above is equivalent byte-for-byte.
    return exact


def validate_plan(plan):
    assert plan["schema"] == "KRENN_X5_RECTANGLE_RANK1_REMAINING4_EXACT_Q_HELD_PLAN_V1"
    assert plan["status"] == "HELD_NOT_RUN_REQUIRES_INDEPENDENT_APPROVAL_AND_MANAGER_CLEARANCE"
    assert plan["launch_authorized"] is False
    assert plan["solver_launches"] == 0 and plan["rank2_launches_authorized"] == 0
    assert plan["execution_sources_materialized"] is False
    assert plan["runner_present"] is False and plan["fresh_clearance_present"] is False
    assert [lane["ordinal"] for lane in plan["lanes"]] == [1, 2, 3, 4]
    assert [lane["orbit"] for lane in plan["lanes"]] == [1, 2, 3, 4]
    assert all(lane["rank"] == 1 and lane["diagonal"] == 0 and lane["raw_orbit_size"] == 6 for lane in plan["lanes"])
    common = plan["common_lane_contract"]
    assert common == {
        "field": "Q", "variables": 76, "generators": 6571,
        "execution_source_bytes": 519397, "native_wall_seconds": 480,
        "wrapper_wall_seconds": 510, "rss_cap_bytes": 8589934592,
        "fresh_libproc_census_before_each_lane": True,
        "fresh_atomic_attempt_directory": True, "refuse_overwrite": True,
        "process_group_rss_observer": True, "observer_failure_terminal": True,
    }
    execution = plan["execution"]
    assert execution == {
        "sequential": True, "maximum_lanes": 4, "parallel_lanes": 1,
        "stop_on_first_nonunit": True, "stop_on_first_resource_failure": True,
        "stop_on_first_process_failure": True, "automatic_relaunch": False,
        "skip_or_reorder": False,
    }
    acceptance = plan["acceptance_per_lane"]
    assert acceptance == {"returncode": 0, "breach": None, "INPUT_VARIABLES": 76,
                           "INPUT_GENERATORS": 6571, "GROEBNER_SIZE": 1,
                           "UNIT_REMAINDER": 0, "STATUS": "UNIT_IDEAL"}


def hostile(base, mutation):
    value = copy.deepcopy(base)
    mutation(value)
    try:
        validate_plan(value)
    except (AssertionError, KeyError, TypeError):
        return True
    return False


def atomic_json(path, value):
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    os.replace(tmp, path)


def main():
    for path, expected in PINS.items():
        assert sha(path) == expected, (path, sha(path), expected)
    plan = json.loads((PLAN_DIR / "HELD_PLAN.json").read_text())
    validate_plan(plan)
    assert plan["dependencies"] == {
        "rank12_design_manifest_sha256": PINS[DESIGN / "MANIFEST.sha256"],
        "rank12_design_result_sha256": PINS[DESIGN / "results_rank12_incidence_design.json"],
        "rank12_referee_manifest_sha256": PINS[DESIGN_REF / "FINAL_MANIFEST.sha256"],
        "rank12_referee_result_sha256": PINS[DESIGN_REF / "results_referee.json"],
        "accepted_orbit0_audit_sha256": PINS[ORBIT0 / "AUDIT_RESULT.json"],
        "accepted_orbit0_manifest_sha256": PINS[ORBIT0 / "FINAL_MANIFEST.sha256"],
    }
    design = json.loads((DESIGN / "results_rank12_incidence_design.json").read_text())
    design_ref = json.loads((DESIGN_REF / "results_referee.json").read_text())
    orbit0 = json.loads((ORBIT0 / "AUDIT_RESULT.json").read_text())
    assert design_ref["status"] == "PASS_EXACT_FINITE_DESIGN_NO_SOLVE_NO_CLOSURE"
    assert design_ref["solver_launches"] == 0 and design_ref["records_closed"] == 0
    assert design_ref["orbit_census"]["rank1_orbits"] == 5
    assert design_ref["orbit_census"]["rank1_sizes"] == [3, 6, 6, 6, 6]
    assert orbit0["status"] == "PASS_UNIT_IDEAL_EXACT_Q_RANK1_ORBIT0_ONLY"
    assert orbit0["field"] == "Q" and orbit0["chart"] == {"rank": 1, "orbit": 0, "diagonal": 0, "I": [0], "J": [0]}
    assert orbit0["second_lane"] is False and orbit0["automatic_relaunch"] is False
    entries = {entry["orbit_index"]: entry for entry in design["canonical_inputs"] if entry["rank"] == 1}
    assert sorted(entries) == [0, 1, 2, 3, 4]
    rebuilt = []
    epilogue = plan["source_derivation"]["epilogue"]
    assert epilogue == [
        "ideal G=slimgb(I);",
        'print("GROEBNER_SIZE="+string(size(G)));',
        "poly remainder=reduce(1,G);",
        'print("UNIT_REMAINDER="+string(remainder));',
        'if (remainder==0) { print("STATUS=UNIT_IDEAL"); } else { print("STATUS=NONUNIT_OR_UNRESOLVED"); }',
    ]
    for lane in plan["lanes"]:
        entry = entries[lane["orbit"]]
        assert entry["rank"] == lane["rank"] == 1
        assert entry["diagonal"] == lane["diagonal"] == 0
        assert entry["row_chart"] == lane["I"] and entry["column_chart"] == lane["J"]
        assert entry["raw_orbit_size"] == lane["raw_orbit_size"] == 6
        source_path = DESIGN / entry["path"]
        assert sha(source_path) == entry["sha256"] == lane["design_source_sha256"]
        source = source_path.read_text()
        field, variables, generators = source_census(source)
        assert field == "0" and variables == 76 and generators == 6571
        execution = derive(source, epilogue)
        encoded = execution.encode()
        assert len(encoded) == plan["common_lane_contract"]["execution_source_bytes"] == 519397
        execution_sha = hashlib.sha256(encoded).hexdigest()
        assert execution_sha == lane["execution_source_sha256"]
        rebuilt.append({"ordinal": lane["ordinal"], "orbit": lane["orbit"],
                        "I": lane["I"], "J": lane["J"],
                        "design_source_sha256": sha(source_path),
                        "execution_source_sha256": execution_sha,
                        "execution_source_bytes": len(encoded),
                        "variables": variables, "generators": generators, "field": "Q"})
    existing = sorted(path.name for path in PLAN_DIR.iterdir())
    assert existing == ["FINAL_MANIFEST.sha256", "HELD_PLAN.json", "REPORT.md", "validate_plan.py"]
    tests = {
        "reorder": hostile(plan, lambda x: x["lanes"].reverse()),
        "skip": hostile(plan, lambda x: x["lanes"].pop()),
        "parallel": hostile(plan, lambda x: x["execution"].__setitem__("parallel_lanes", 2)),
        "relaunch": hostile(plan, lambda x: x["execution"].__setitem__("automatic_relaunch", True)),
        "rank2": hostile(plan, lambda x: x.__setitem__("rank2_launches_authorized", 1)),
        "premature_clearance": hostile(plan, lambda x: x.__setitem__("launch_authorized", True)),
        "wall_weakening": hostile(plan, lambda x: x["common_lane_contract"].__setitem__("wrapper_wall_seconds", 511)),
        "observer_weakening": hostile(plan, lambda x: x["common_lane_contract"].__setitem__("observer_failure_terminal", False)),
    }
    assert all(tests.values())
    result = {
        "schema": "KRENN_X5_RECTANGLE_RANK1_REMAINING4_EXACT_Q_HELD_PLAN_REFEREE_V1",
        "status": "PASS_APPROVED_HELD_ZERO_RUNS",
        "producer": {"plan_sha256": PINS[PLAN_DIR / "HELD_PLAN.json"],
                     "manifest_sha256": PINS[PLAN_DIR / "FINAL_MANIFEST.sha256"]},
        "dependencies": plan["dependencies"],
        "lanes": rebuilt,
        "schedule": {"exact_orbit_order": [1, 2, 3, 4], "sequential": True,
                     "maximum_lanes": 4, "parallel_lanes": 1,
                     "stop_first_nonunit_timeout_resource_process_or_mismatch": True,
                     "skip_or_reorder": False, "automatic_relaunch": False,
                     "rank2_authorized": False},
        "resource_contract": {"native_wall_seconds": 480, "wrapper_wall_seconds": 510,
                              "rss_cap_bytes": 8589934592,
                              "fresh_libproc_census_before_each_lane": True,
                              "atomic_distinct_attempt_per_lane": True,
                              "observer_failure_terminal": True},
        "held_state": {"solver_runs": 0, "execution_sources_materialized": False,
                       "runner_present": False, "fresh_clearance_present": False,
                       "launch_authorized": False,
                       "requires_new_manager_clearance": True},
        "scope_if_executed_and_all_pass": "With sealed orbit0, closes exactly the five rank-one canonical orbits and their two amplitude-inactive A12 lifts; rank two remains open.",
        "hostile_tests": tests,
        "pins": {str(path.relative_to(ROOT)): expected for path, expected in PINS.items()},
    }
    atomic_json(HERE / "results_referee.json", result)
    print(json.dumps({"status": result["status"], "orbits": [1, 2, 3, 4],
                      "execution_source_hashes": [lane["execution_source_sha256"] for lane in rebuilt],
                      "solver_runs": 0}, sort_keys=True))


if __name__ == "__main__":
    main()
