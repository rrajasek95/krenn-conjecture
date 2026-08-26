#!/usr/bin/env python3
"""Fail-closed small-file audit of the sealed D11 cross-branch diagnostic."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parents[1]
PRIME = 1_073_741_827
PINS = {
    "source_manifest": (ROOT / "computations/unaudited-codex-n8-x5-d11-triangle-resume20-advanced-2026-08-25/PRODUCTION_MANIFEST.sha256", "a41b060659d86a3fbd908a8f2241b0bf6b52fe0f57bd7ce1f253482412fb0232"),
    "source_dual": (ROOT / "computations/unaudited-codex-n8-x5-d11-triangle-resume20-advanced-2026-08-25/production_advanced_resume_p1073741827_triangle_endpoint_colour/dual.tsv", "eeea4d8278a798ae829f28ac92a70bbdff9b3660144b618835091c470cbcbdea"),
    "source_provider": (ROOT / "computations/unaudited-codex-n8-x5-four-blocker-d6-cegar-gate-2026-08-25/provider_triangle_endpoint_colour.ms", "06df5052a50099dc400d622323257fef9b3077a791f918c8f1c46d7bf7a5782c"),
    "third_provider": (ROOT / "computations/unaudited-codex-n8-x5-four-blocker-d6-cegar-gate-2026-08-25/provider_third_colour.ms", "b5ce054d529a5390c366254d08e43595cfa16e04854514f80db1b34f109d4ae8"),
    "cap_provider": (ROOT / "computations/unaudited-codex-n8-x5-four-blocker-d6-cegar-gate-2026-08-25/provider_cap_endpoint_colour.ms", "d040d1525989588bce3b912413aa6841869de63575bb3ebf976de817869e0b64"),
    "source": (PACKAGE / "src/main.rs", "dbed9910aa791c59e6077a3064dfd9777f92831eb3315a4772d7ded310267d97"),
    "binary": (PACKAGE / "x5_d11_transport_diagnostic", "3cb03b9276dfacf5b877428242c15048c27d14e5da73af158a78783db4ae5efa"),
    "watchdog": (PACKAGE / "watchdog4_120.py", "6c77af08481c20b045b0a8e7bfe8c8710d15b129862f0e6f8766c72636c02443"),
}
EXPECTED = {
    "third_colour": {
        "incident_columns_checked": 411275,
        "violation_columns": 208088,
        "violation_row_union": 21331925,
        "new_violation_rows": 21230547,
        "allowed_rows_support_union_violation_rows": 21415206,
    },
    "cap_endpoint_colour": {
        "incident_columns_checked": 411275,
        "violation_columns": 208088,
        "violation_row_union": 21332929,
        "new_violation_rows": 21231551,
        "allowed_rows_support_union_violation_rows": 21416210,
    },
}
RESULT_KEYS = {
    "schema", "status", "reason", "branch", "prime", "degree", "target",
    "coordinate_transport", "provider_variables", "provider_equations",
    "provider_terms_parsed", "transported_support",
    "target_coefficient_before_normalization", "normalization_factor",
    "target_coefficient_after_normalization", "incident_scan_exhaustive",
    "incident_columns_checked", "violation_columns", "violation_row_union",
    "new_violation_rows", "allowed_rows_support_union_violation_rows",
    "small_repair_column_cap", "small_repair_attempted", "repair_system_scope",
    "repair_consistent_over_p107", "repair_basis_rank", "repair_candidate_support",
    "repair_selected_replay_failures", "repair_dual_written", "global_dual_claim",
    "nonviolating_incident_columns_replayed_after_repair", "general_cegar_launched",
    "second_prime_launched", "degree_twelve_cache_read", "scan_seconds",
    "repair_solve_seconds", "elapsed_seconds", "native_wall_limit_seconds",
}


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def validate_result(value: dict, branch: str) -> None:
    assert set(value) == RESULT_KEYS
    assert value["schema"] == "KRENN_X5_D11_CROSS_BRANCH_TRANSPORT_DIAGNOSTIC_V1"
    assert value["status"] == "PASS_EXACT_TRANSPORT_DIAGNOSTIC_NOT_SMALL"
    assert value["reason"] == "VIOLATION_SYSTEM_EXCEEDS_FROZEN_100000_COLUMN_REPAIR_GATE"
    assert value["branch"] == branch and value["prime"] == PRIME
    assert value["degree"] == 11 and value["target"] == "t^11"
    assert value["coordinate_transport"] == "IDENTICAL_361_NAME_HEADER"
    assert value["provider_variables"] == 361 and value["provider_equations"] == 6571
    assert value["provider_terms_parsed"] == 690855
    assert value["transported_support"] == 184659
    assert value["target_coefficient_before_normalization"] == 1
    assert value["normalization_factor"] == 1
    assert value["target_coefficient_after_normalization"] == 1
    assert value["incident_scan_exhaustive"] is True
    for field, expected in EXPECTED[branch].items():
        assert value[field] == expected
    assert value["allowed_rows_support_union_violation_rows"] == value["transported_support"] + value["new_violation_rows"]
    assert value["violation_columns"] > value["small_repair_column_cap"] == 100000
    assert value["small_repair_attempted"] is False
    assert value["repair_system_scope"] == "ALL_AND_ONLY_VIOLATING_COLUMNS_INCIDENT_TO_TRANSPORTED_SUPPORT"
    assert value["repair_consistent_over_p107"] is None
    assert value["repair_basis_rank"] is None and value["repair_candidate_support"] is None
    assert value["repair_selected_replay_failures"] is None and value["repair_dual_written"] is False
    assert value["global_dual_claim"] is False
    assert value["nonviolating_incident_columns_replayed_after_repair"] is False
    assert value["general_cegar_launched"] is False
    assert value["second_prime_launched"] is False
    assert value["degree_twelve_cache_read"] is False
    assert 0 < value["scan_seconds"] < 110 and 0 < value["elapsed_seconds"] < 120
    assert value["repair_solve_seconds"] == 0 and value["native_wall_limit_seconds"] == 110


def main() -> None:
    for path, expected in PINS.values():
        assert sha(path) == expected
    providers = [PINS[name][0] for name in ("source_provider", "third_provider", "cap_provider")]
    headers = [path.open("rb").readline() for path in providers]
    assert headers[0] == headers[1] == headers[2]
    assert hashlib.sha256(headers[0]).hexdigest() == "9cbfbc5e67f636b7ebf80dbea1a3d036d583b859c47b14e8b02c74adee2c06df"
    assert len(headers[0].rstrip(b"\n").split(b",")) == 361

    dual_lines = PINS["source_dual"][0].read_text().splitlines()
    assert dual_lines[0] == f"KRENN_X5_BLOCKER_D11_MODULAR_DUAL_V1\t{PRIME}\t184659\t1"
    target = "361," * 10 + "361"
    target_lines = [line for line in dual_lines[1:] if line.startswith(f"ROW\t{target}\t")]
    assert target_lines == [f"ROW\t{target}\t1"]

    results = {}
    for branch in EXPECTED:
        result = json.loads((PACKAGE / branch / "result.json").read_text())
        validate_result(result, branch)
        watchdog = json.loads((PACKAGE / branch / "watchdog.json").read_text())
        assert watchdog["status"] == "PASS" and watchdog["breach"] is None and watchdog["returncode"] == 0
        assert watchdog["peak_rss_kib"] <= 4 * 1024 * 1024
        assert watchdog["elapsed_seconds"] < 120
        assert not (PACKAGE / branch / "repair_dual.tsv").exists()
        assert (PACKAGE / branch / "stdout.log").read_bytes() == b""
        assert (PACKAGE / branch / "stderr.log").read_bytes() == b""
        results[branch] = {
            **EXPECTED[branch],
            "result_sha256": sha(PACKAGE / branch / "result.json"),
            "watchdog_sha256": sha(PACKAGE / branch / "watchdog.json"),
            "peak_rss_kib": watchdog["peak_rss_kib"],
            "elapsed_seconds": watchdog["elapsed_seconds"],
        }

    hostile_tests = 0
    base = json.loads((PACKAGE / "third_colour/result.json").read_text())
    for field, bad in [
        ("normalization_factor", 2),
        ("incident_scan_exhaustive", False),
        ("small_repair_attempted", True),
        ("general_cegar_launched", True),
        ("degree_twelve_cache_read", True),
    ]:
        mutant = dict(base)
        mutant[field] = bad
        try:
            validate_result(mutant, "third_colour")
        except AssertionError:
            hostile_tests += 1
        else:
            raise AssertionError(f"hostile mutation accepted: {field}")
    mutant = dict(base)
    mutant["extra"] = 1
    try:
        validate_result(mutant, "third_colour")
    except AssertionError:
        hostile_tests += 1
    else:
        raise AssertionError("hostile extra field accepted")

    audit = {
        "schema": "KRENN_X5_D11_CROSS_BRANCH_TRANSPORT_AUDIT_V1",
        "status": "PASS",
        "source_checkpoint_manifest_sha256": PINS["source_manifest"][1],
        "coordinate_identity_exact": True,
        "source_dual_target_normalization": {"before": 1, "factor": 1, "after": 1},
        "branches": results,
        "small_support_repair_available": False,
        "repair_consistency_evaluated": False,
        "reason": "both exact violation systems exceed the frozen 100000-column gate and expand to more than 21.4 million allowed rows",
        "global_dual_claim": False,
        "general_cegar_launched": False,
        "second_prime_launched": False,
        "degree_twelve_cache_read": False,
        "hostile_tests_passed": hostile_tests,
    }
    output = PACKAGE / "results_audit.json"
    temporary = output.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, output)


if __name__ == "__main__":
    main()
