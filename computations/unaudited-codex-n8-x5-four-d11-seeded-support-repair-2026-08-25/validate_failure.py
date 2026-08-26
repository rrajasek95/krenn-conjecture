#!/usr/bin/env python3
"""Strict validation of accepted direct D11 evidence and coloured failures."""
import hashlib
import json
import os
from pathlib import Path

if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent
SOURCE_SHA = "57127904ab633bb5e9c58af1e66fe41cfae169659a32220a4460c998c54ef66d"
BINARY_SHA = "faf03447eb47bfc5cdeeea8feba7a4027160504a6622161baea595f5becb24d5"

def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()

def load(path):
    return json.loads((HERE / path).read_text())

def atomic(path, value):
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, path)

def main():
    assert sha(HERE / "src/main.rs") == SOURCE_SHA
    assert sha(HERE / "x5_four_d11_seeded_repair") == BINARY_SHA
    seeds = load("results_seed_build.json")
    assert seeds["status"] == "PASS_FOUR_EXACT_D11_TRANSPORT_SEEDS"
    assert [r["exact_transport_pairing_failures"] for r in seeds["records"]] == [0, 76, 76, 70]
    direct = load("p1073741827_direct/result.json")
    direct_watch = load("p1073741827_direct/watchdog.json")
    direct_exact = load("exact_lift_direct/result.json")
    assert direct["status"] == "COMPLETE_MODULAR_DUAL_DIAGNOSTIC" and direct["selected_columns"] == 0
    assert direct_watch["status"] == "PASS_TERMINAL" and direct_watch["breach"] is None
    assert direct_exact["status"] == "PASS_DIRECT_CHARACTERISTIC_ZERO_D11_OBSTRUCTION"
    assert direct_exact["target_coefficient"] == 1 and direct_exact["pairing_failures"] == 0
    assert direct_exact["integer_dual_sha256"] == "d631677cef2be77de0f2f28e815bdb50ef93da484e0d2a548c6f8287f22f4c87"

    guard = load("failed_empty_checkpoint_guard_p1073741827_direct/watchdog.json")
    assert guard["status"] == "FAIL_CLOSED" and guard["result_exists"] is False
    general = load("p1073741827_triangle_endpoint_colour/watchdog.json")
    assert general["status"] == "FAIL_CLOSED" and general["breach"] == "RSS_CAP"
    assert general["result_exists"] is False and general["peak_rss_kib"] > 8 * 1024 * 1024
    restricted = load("support_probe_p1073741827_triangle_endpoint_colour/result.json")
    restricted_watch = load("support_probe_p1073741827_triangle_endpoint_colour/watchdog.json")
    assert restricted["status"] == "INCOMPLETE_SUPPORT_RESTRICTED_INCONSISTENT"
    assert restricted_watch["status"] == "FAIL_CLOSED" and restricted_watch["breach"] is None
    shift = load("shift_probe_p1073741827_triangle_endpoint_colour/result.json")
    shift_watch = load("shift_probe_p1073741827_triangle_endpoint_colour/watchdog.json")
    assert shift["status"] == "INCOMPLETE_SHIFT_SPAN_INCONSISTENT"
    assert shift_watch["status"] == "FAIL_CLOSED" and shift_watch["breach"] is None
    census = load("one_hop_census_failure.json")
    assert census["accepted_coverage"] == 0 and census["resource_contract_pass"] is False
    assert not (HERE / "results_first_prime.json").exists()
    assert not any(path.name.startswith("p1000000007") for path in HERE.iterdir())
    assert not (HERE / "p1073741827_third_colour").exists()
    assert not (HERE / "p1073741827_cap_endpoint_colour").exists()
    assert not any(path.name.startswith("d12") for path in HERE.iterdir())
    result = {
        "schema": "KRENN_X5_FOUR_D11_GATE_FINAL_AUDIT_V1",
        "status": "FAIL_CLOSED_COLOURED_D11_UNRESOLVED",
        "accepted_exact_branches": ["direct"],
        "unresolved_branches": ["triangle_endpoint_colour", "third_colour", "cap_endpoint_colour"],
        "direct_integer_dual_sha256": direct_exact["integer_dual_sha256"],
        "direct_literal_incident_columns_replayed": direct_exact["literal_incident_columns_replayed"],
        "triangle_general_cegar": {"status": "RSS_CAP_NO_RESULT", "elapsed_seconds": general["elapsed_seconds"], "peak_rss_kib": general["peak_rss_kib"], "accepted_coverage": 0},
        "triangle_support_restriction": {"status": restricted["status"], "allowed_rows": restricted["allowed_rows"], "incident_columns": restricted["incident_columns"], "coefficient_rank": restricted["basis_rank"], "accepted_coverage": 0},
        "triangle_shift_span": {"status": shift["status"], "candidate_shifts": shift["candidate_shifts"], "union_support": shift["union_support"], "nonzero_equation_columns": shift["nonzero_equation_columns"], "coefficient_rank": shift["coefficient_rank"], "accepted_coverage": 0},
        "second_prime_authorized": False,
        "reason_second_prime_not_run": "first-prime four-branch closure condition failed",
        "all_four_characteristic_zero_d11_obstructions": False,
        "source_sha256": SOURCE_SHA, "binary_sha256": BINARY_SHA,
        "degree_twelve_launched": False
    }
    atomic(HERE / "results_final_audit.json", result)
    print(json.dumps(result, sort_keys=True))

if __name__ == "__main__":
    main()
