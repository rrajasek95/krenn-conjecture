#!/usr/bin/env python3
"""Independent small-file audit of the held D9 resumable recovery design."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import statistics
import subprocess
import sys

if not __debug__:
    raise RuntimeError("fail closed: validator requires assertions enabled")

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
SCHEDULE = json.loads((HERE / "SCHEDULE.json").read_text())


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(8 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def selected_count(path):
    with path.open() as stream:
        assert stream.readline().rstrip("\n") == "KRENN_X5_BLOCKER_D9_SELECTED_COLUMNS_V1"
        previous = None
        count = 0
        for line in stream:
            kind, generator, degree, multiplier = line.rstrip("\n").split("\t")
            key = (int(generator), tuple(map(int, multiplier.split(","))))
            assert kind == "COL" and int(degree) in (2, 3, 4)
            assert key[1] == tuple(sorted(key[1])) and len(key[1]) + int(degree) == 9
            assert previous is None or previous < key
            previous = key
            count += 1
    return count


def dual_support(path):
    with path.open() as stream:
        header = stream.readline().rstrip("\n").split("\t")
        assert header[0] == "KRENN_X5_BLOCKER_D9_MODULAR_DUAL_V1"
        assert int(header[1]) == 1073741827 and header[3] == "1"
        expected = int(header[2])
        rows = [line.rstrip("\n").split("\t") for line in stream]
    assert len(rows) == expected
    assert all(row[0] == "ROW" and 0 < int(row[2]) < 1073741827 for row in rows)
    assert [row[1] for row in rows] == sorted({row[1] for row in rows}, key=lambda text: tuple(map(int, text.split(","))))
    return expected


def run_json(command):
    completed = subprocess.run(command, cwd=HERE, text=True, capture_output=True, check=True)
    assert completed.stderr == ""
    return json.loads(completed.stdout)


def hostile_tests():
    tests = []
    base = {
        "source_hash": SCHEDULE["engine"]["source_sha256"],
        "selected_hash": SCHEDULE["inputs"]["resume_selected_sha256"],
        "branch": "triangle_endpoint_colour",
        "prime": 1073741827,
        "resume_columns": 15273,
        "engine_status": "INCOMPLETE_WALL_CAP",
        "semantic_class": "RESTART_CHECKPOINT_ONLY",
        "column_cap": 2000000,
    }
    mutations = {
        "wrong_source_hash": ("source_hash", "0" * 64),
        "wrong_selected_hash": ("selected_hash", "0" * 64),
        "wrong_branch": ("branch", "direct"),
        "wrong_prime": ("prime", 1000000007),
        "wrong_resume_count": ("resume_columns", 15272),
        "incomplete_invented_terminal": ("semantic_class", "TERMINAL_MODULAR_DUAL"),
        "wrong_column_cap": ("column_cap", 2000001),
        "unknown_status": ("engine_status", "PASS"),
    }
    for name, (field, value) in mutations.items():
        candidate = dict(base)
        candidate[field] = value
        try:
            assert candidate["source_hash"] == SCHEDULE["engine"]["source_sha256"]
            assert candidate["selected_hash"] == SCHEDULE["inputs"]["resume_selected_sha256"]
            assert candidate["branch"] == "triangle_endpoint_colour"
            assert candidate["prime"] == 1073741827
            assert candidate["resume_columns"] == 15273
            assert candidate["column_cap"] == 2000000
            assert candidate["engine_status"] in {
                "COMPLETE_MODULAR_DUAL_DIAGNOSTIC",
                "MODULAR_MEMBER_REQUIRES_EXACT_RATIONAL_REPLAY",
                "INCOMPLETE_WALL_CAP",
            }
            if candidate["engine_status"] == "INCOMPLETE_WALL_CAP":
                assert candidate["semantic_class"] == "RESTART_CHECKPOINT_ONLY"
        except AssertionError:
            tests.append({"name": name, "status": "REJECTED"})
            continue
        raise AssertionError(f"hostile accepted: {name}")
    return tests


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args()
    assert SCHEDULE["status"] == "FROZEN_HELD_NO_PRODUCTION_LAUNCH"
    inputs, engine = SCHEDULE["inputs"], SCHEDULE["engine"]
    paths = {
        "source": HERE / engine["source"],
        "binary": HERE / engine["binary"],
        "runner": HERE / SCHEDULE["runner"]["path"],
        "watchdog": HERE / SCHEDULE["watchdog"]["path"],
        "provider": REPO / inputs["provider"],
        "selected": REPO / inputs["resume_selected"],
        "dual": REPO / inputs["resume_dual"],
        "parent_manifest": REPO / inputs["parent_manifest"],
    }
    expected = {
        "source": engine["source_sha256"],
        "binary": engine["binary_sha256"],
        "runner": SCHEDULE["runner"]["sha256"],
        "watchdog": SCHEDULE["watchdog"]["sha256"],
        "provider": inputs["provider_sha256"],
        "selected": inputs["resume_selected_sha256"],
        "dual": inputs["resume_dual_sha256"],
        "parent_manifest": inputs["parent_manifest_sha256"],
    }
    observed = {name: sha256(path) for name, path in paths.items()}
    assert observed == expected
    assert selected_count(paths["selected"]) == inputs["resume_selected_columns"] == 15273
    assert dual_support(paths["dual"]) == inputs["resume_dual_support"] == 178

    engine_selftest = run_json([str(paths["binary"]), "--selftest"])
    runner_selftest = run_json([sys.executable, str(paths["runner"]), "--selftest"])
    assert engine_selftest["status"] == "PASS" and engine_selftest["tests"] == 5
    assert runner_selftest["status"] == "PASS" and runner_selftest["cases"] == 6
    assert runner_selftest["multi_branch_advancement"] is False

    parent_result = json.loads((paths["selected"].parent / "result.json").read_text())
    rounds = parent_result["rounds"]
    assert parent_result["status"] == "INCOMPLETE_WALL_CAP"
    assert parent_result["selected_columns"] == 15273 and len(rounds) == 434
    solve_sum = sum(record["solve_seconds"] for record in rounds)
    incidence_sum = sum(record["incidence_seconds"] for record in rounds)
    tail25 = rounds[-25:]
    exact_profile = {
        "elapsed_seconds": parent_result["elapsed_seconds"],
        "rounds": len(rounds),
        "selected_columns": parent_result["selected_columns"],
        "dual_support": parent_result["dual_support"],
        "solve_seconds_sum": round(solve_sum, 6),
        "solve_fraction_percent": round(100 * solve_sum / parent_result["elapsed_seconds"], 6),
        "incidence_seconds_sum": round(incidence_sum, 6),
        "last_solve_seconds": rounds[-1]["solve_seconds"],
        "last_25_new_columns": rounds[-1]["columns_after"] - tail25[0]["columns_before"],
        "last_25_violation_min": min(record["new_violations"] for record in tail25),
        "last_25_violation_median": statistics.median(record["new_violations"] for record in tail25),
        "last_25_violation_max": max(record["new_violations"] for record in tail25),
    }
    assert exact_profile == {
        "elapsed_seconds": 175.758071,
        "rounds": 434,
        "selected_columns": 15273,
        "dual_support": 178,
        "solve_seconds_sum": 174.739622,
        "solve_fraction_percent": 99.420539,
        "incidence_seconds_sum": 0.764937,
        "last_solve_seconds": 0.814643,
        "last_25_new_columns": 3028,
        "last_25_violation_min": 84,
        "last_25_violation_median": 118,
        "last_25_violation_max": 162,
    }
    previous = []
    for degree, relative in (
        (6, "computations/unaudited-codex-n8-x5-four-blocker-d6-cegar-gate-2026-08-25/branch_triangle_endpoint_colour/result.json"),
        (7, "computations/unaudited-codex-n8-x5-four-blocker-d7-two-prime-lift-2026-08-25/p1073741827_triangle_endpoint_colour/result.json"),
        (8, "computations/unaudited-codex-n8-x5-four-blocker-d8-two-prime-lift-2026-08-25/p1073741827_triangle_endpoint_colour/result.json"),
    ):
        record = json.loads((REPO / relative).read_text())
        assert record["degree"] == degree and record["status"] == "COMPLETE_MODULAR_DUAL_DIAGNOSTIC"
        previous.append({
            "degree": degree,
            "rounds": len(record["rounds"]),
            "selected_columns": record["selected_columns"],
            "dual_support": record["dual_support"],
            "elapsed_seconds": record["elapsed_seconds"],
        })
    assert [(r["rounds"], r["selected_columns"], r["dual_support"]) for r in previous] == [
        (210, 439, 14), (217, 1943, 23), (225, 4309, 52)
    ]

    result = {
        "schema": "KRENN_X5_D9_RESUMABLE_SINGLE_BRANCH_DESIGN_AUDIT_V1",
        "status": "PASS_FROZEN_HELD_NO_PRODUCTION_LAUNCH",
        "pins": observed,
        "engine_selftest": engine_selftest,
        "runner_selftest": runner_selftest,
        "previous_complete_degrees": previous,
        "partial_d9_profile": exact_profile,
        "dominant_cost": "full selected-system dual rebuild each CEGAR round",
        "optimization": "freeze checkpoint-frequency pivot order, rebuild once, then incrementally insert only new equations",
        "closure_estimate": {
            "kind": "low-confidence diagnostic, not a bound",
            "selected_columns_scenario": "20000--35000",
            "total_rounds_scenario": "500--700",
            "legacy_total_wall_seconds_scenario": "240--600",
            "evidence_based_lower_bound_seconds": 175.758071,
            "finite_upper_bound_established": False,
            "reason_for_uncertainty": "the last 25 rounds added 3028 columns and every round still exposed 84--162 violations",
        },
        "held_gate": {
            "single_branch": "triangle_endpoint_colour",
            "single_prime": 1073741827,
            "native_wall_seconds": 175,
            "wrapper_wall_seconds": 180,
            "rss_gib": 8,
            "launch_clearance_required": True,
        },
        "production_launched": False,
        "d12_cache_access": False,
        "degree_ten_launched": False,
        "hostile_tests": hostile_tests() if args.selftest else [],
    }
    target = HERE / ("results_validation_selftest.json" if args.selftest else "results_design_audit.json")
    temporary = target.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, target)
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
