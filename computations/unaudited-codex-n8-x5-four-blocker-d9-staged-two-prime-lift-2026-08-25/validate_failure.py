#!/usr/bin/env python3
"""Fail-closed audit of the capped D9 coloured phase and rejected overrun."""
import argparse
import json
import os
import sys
from pathlib import Path

if not __debug__:
    raise RuntimeError("fail closed: validator requires assertions enabled")

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import validate as common

REPO = HERE.parents[1]
SCHEDULE = json.loads((HERE / "SCHEDULE.json").read_text())
PRIME = SCHEDULE["primes"][0]


def load_selected(path, generators):
    lines = path.read_text().splitlines()
    assert lines[0] == "KRENN_X5_BLOCKER_D9_SELECTED_COLUMNS_V1"
    columns = []
    for line in lines[1:]:
        kind, generator, degree, multiplier = line.split("\t")
        generator, degree = int(generator), int(degree)
        multiplier = tuple(int(item) for item in multiplier.split(",") if item)
        assert kind == "COL" and 0 <= generator < len(generators)
        assert generators[generator][0] == degree
        assert degree + len(multiplier) == 9 and tuple(sorted(multiplier)) == multiplier
        columns.append((generator, multiplier))
    assert columns == sorted(set(columns))
    return tuple(columns)


def modular_pairing(vector, dual, prime):
    return sum(value * dual.get(row, 0) for row, value in vector.items()) % prime


def verify_incomplete(directory, generators, expected_branch, require_watchdog):
    result_path = directory / "result.json"
    result = json.loads(result_path.read_text())
    assert result["schema"] == "KRENN_X5_FOUR_BLOCKER_D9_CEGAR_RESULT_V1"
    assert result["branch"] == expected_branch and result["prime"] == PRIME
    assert result["degree"] == 9 and result["target"] == "t^9"
    assert result["status"] == "INCOMPLETE_WALL_CAP"
    assert result["incomplete_reason"] == "WALL_CAP"
    assert result["global_modular_dual"] is None
    assert result["exact_rational_unit_replay"] is False
    assert result["mathematical_verdict"] is None
    assert result["column_cap"] == 2_000_000 and result["wall_limit_seconds"] == 175
    assert result["elapsed_seconds"] < 180 and result["selected_columns"] < 2_000_000
    assert result["rounds"] and result["rounds"][-1]["columns_after"] == result["selected_columns"]
    previous = 0
    for index, round_record in enumerate(result["rounds"]):
        assert round_record["round"] == index
        assert round_record["columns_before"] == previous
        assert round_record["columns_after"] >= round_record["columns_before"]
        previous = round_record["columns_after"]

    columns = load_selected(directory / "selected.tsv", generators)
    dual = common.load_modular_dual(directory / "dual.tsv", PRIME)
    assert len(columns) == result["selected_columns"] and len(dual) == result["dual_support"]
    pairing_failures = sum(
        modular_pairing(common.materialize(generators, column), dual, PRIME) != 0
        for column in columns
    )
    assert pairing_failures == 0

    watchdog_record = None
    if require_watchdog:
        watchdog = json.loads((directory / "watchdog.json").read_text())
        # Historical wrapper v1 checked process/wall/RSS and atomic existence,
        # but incorrectly called a native INCOMPLETE result PASS.  This audit
        # explicitly supersedes that semantic status.
        assert watchdog["status"] == "PASS" and watchdog["breach"] is None
        assert watchdog["wall_limit_seconds"] == 180
        assert watchdog["peak_rss_kib"] <= 8 * 1024 * 1024
        assert watchdog["result_sha256"] == common.sha256(result_path)
        assert watchdog["source_sha256"] == SCHEDULE["engine"]["source_sha256"]
        assert watchdog["binary_sha256"] == SCHEDULE["engine"]["binary_sha256"]
        watchdog_record = {
            "historical_status": watchdog["status"],
            "superseded_semantic_status": "FAIL_CLOSED_NATIVE_INCOMPLETE",
            "elapsed_seconds": watchdog["elapsed_seconds"],
            "peak_rss_kib": watchdog["peak_rss_kib"],
            "sha256": common.sha256(directory / "watchdog.json"),
        }
    else:
        assert not (directory / "watchdog.json").exists()
        assert (directory / "stdout.log.tmp").exists()
        assert (directory / "stderr.log.tmp").exists()

    return {
        "branch": expected_branch,
        "status": result["status"],
        "selected_columns": result["selected_columns"],
        "dual_support": result["dual_support"],
        "rounds": len(result["rounds"]),
        "engine_elapsed_seconds": result["elapsed_seconds"],
        "selected_pairings_replayed": len(columns),
        "selected_pairing_failures": pairing_failures,
        "result_sha256": common.sha256(result_path),
        "selected_sha256": common.sha256(directory / "selected.tsv"),
        "dual_sha256": common.sha256(directory / "dual.tsv"),
        "watchdog": watchdog_record,
        "accepted_coverage": False,
    }


def hostile_tests(base):
    tests = []
    mutations = {
        "invent_complete": ("status", "COMPLETE_MODULAR_DUAL_DIAGNOSTIC"),
        "invent_global_dual": ("global_modular_dual", True),
        "invent_exact_replay": ("exact_rational_unit_replay", True),
        "wrong_degree": ("degree", 10),
        "wrong_prime": ("prime", SCHEDULE["primes"][1]),
    }
    for name, (field, value) in mutations.items():
        candidate = dict(base)
        candidate[field] = value
        try:
            assert candidate["status"] == "INCOMPLETE_WALL_CAP"
            assert candidate["global_modular_dual"] is None
            assert candidate["exact_rational_unit_replay"] is False
            assert candidate["degree"] == 9 and candidate["prime"] == PRIME
        except AssertionError:
            tests.append({"name": name, "status": "REJECTED"})
            continue
        raise AssertionError(f"hostile accepted: {name}")
    return tests


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args()
    assert common.sha256(HERE / SCHEDULE["engine"]["source"]) == SCHEDULE["engine"]["source_sha256"]
    assert common.sha256(HERE / SCHEDULE["engine"]["binary"]) == SCHEDULE["engine"]["binary_sha256"]
    root = SCHEDULE["provider_roots"][str(PRIME)]
    assert common.sha256(REPO / root["package"] / "MANIFEST.sha256") == root["manifest_sha256"]
    generators_by_branch = {}
    for branch in ("triangle_endpoint_colour", "cap_endpoint_colour"):
        provider_spec = root["providers"][branch]
        provider = REPO / root["package"] / provider_spec[0]
        assert common.sha256(provider) == provider_spec[1]
        _variables, generators_by_branch[branch] = common.load_provider(provider, PRIME)

    authoritative = verify_incomplete(
        HERE / "p1073741827_triangle_endpoint_colour",
        generators_by_branch["triangle_endpoint_colour"],
        "triangle_endpoint_colour",
        True,
    )
    rejected = verify_incomplete(
        HERE / "rejected_control_flow_v1" / "p1073741827_cap_endpoint_colour",
        generators_by_branch["cap_endpoint_colour"],
        "cap_endpoint_colour",
        False,
    )
    absent = [
        str(path.relative_to(HERE))
        for path in (
            HERE / "p1073741827_third_colour",
            HERE / "p1073741827_direct",
            *(HERE / f"p1000000007_{branch}" for branch in SCHEDULE["branches"]),
        )
        if not path.exists()
    ]
    assert len(absent) == 6
    assert not any((HERE / f"exact_lift_{branch}").exists() for branch in SCHEDULE["branches"])
    assert not (HERE / "results_characteristic_zero_lift.json").exists()

    base = json.loads((HERE / "p1073741827_triangle_endpoint_colour" / "result.json").read_text())
    result = {
        "schema": "KRENN_X5_D9_FAIL_CLOSED_AUDIT_V1",
        "status": "PASS_FAIL_CLOSED_DIAGNOSTIC_NO_D9_Q_COVERAGE",
        "authoritative_attempt": authoritative,
        "rejected_control_flow_attempt": rejected,
        "absent_unlaunched_directories": absent,
        "accepted_modular_branches": 0,
        "accepted_two_prime_branches": 0,
        "exact_q_certificates": 0,
        "degree_nine_mathematical_coverage": 0,
        "direct_launched": False,
        "exact_lift_launched": False,
        "degree_ten_launched": False,
        "conjecture_closed": False,
        "hostile_tests": hostile_tests(base) if args.selftest else [],
    }
    target = HERE / ("results_validation_selftest.json" if args.selftest else "results_d9_fail_closed_audit.json")
    temporary = target.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, target)
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
