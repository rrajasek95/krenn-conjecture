#!/usr/bin/env python3
"""Fail-closed static audit for the held 16-GiB D11 triangle resume."""

import hashlib
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
PARENT = REPO / "computations/unaudited-codex-n8-x5-d11-triangle-general-cegar-recovery-design-2026-08-25"
PROVIDER = REPO / "computations/unaudited-codex-n8-x5-four-blocker-d6-cegar-gate-2026-08-25/provider_triangle_endpoint_colour.ms"
OUTPUT = HERE / "production_resume_p1073741827_triangle_endpoint_colour"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def atomic_json(path: Path, value: object) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    temporary.replace(path)


def main() -> None:
    if not __debug__:
        raise RuntimeError("fail closed: assertions required")

    paths = {
        "parent_source": PARENT / "src/main.rs",
        "parent_watchdog": PARENT / "watchdog12_600_recovery.py",
        "parent_production_manifest": PARENT / "PRODUCTION_MANIFEST.sha256",
        "parent_watchdog_result": PARENT / "production_p1073741827_triangle_endpoint_colour/watchdog.json",
        "source": HERE / "src/main.rs",
        "binary": HERE / "x5_d11_triangle_resume16",
        "watchdog": HERE / "watchdog16_360_resume.py",
        "provider": PROVIDER,
        "selected": HERE / "sealed_resume_input/selected.tsv",
        "dual": HERE / "sealed_resume_input/dual.tsv",
        "checkpoint_audit": HERE / "sealed_resume_input/checkpoint_audit.json",
    }
    pins = {
        "parent_source": "521e8f503f900c15b9b0668f60095fae120b6f47e44666076179fbc2058d9120",
        "parent_watchdog": "4418ffadb5cc45ec4bdec1427850810d66438d7d09679520eab7d5fba142291e",
        "parent_production_manifest": "071d61b42769fe335ec9c84bbc779a30c7761537b7e70cfdb2928b5fb21ac9b3",
        "parent_watchdog_result": "9d45b22c2c8795abc0c6553989fec7080982abf16e79c88a0e8d40b18420fc47",
        "source": "936ad21fa4aa8ed0ffe78dc090d9e85ddeefa33713be75c1daa1bcd5f7aca142",
        "binary": "2c342802e955a437bb9c6f7fa686a6d1912dad9fe045bec1bf79232b77a97755",
        "watchdog": "5a83fe143da9e4c7f646874f97944a4858b21362e5bbf91da98e3794fd0a3fd4",
        "provider": "06df5052a50099dc400d622323257fef9b3077a791f918c8f1c46d7bf7a5782c",
        "selected": "1f70a3220d6091e0877fd00d86c6ff9f06f25789e03cc854556e6d7ae34fb2a7",
        "dual": "a91f2be59901b4f29c09f64845e700fb40d7f15181bcd7ac8df89022d4e39d93",
        "checkpoint_audit": "37208d8103869d80513f2e3d67b557fbdf71f532e98f3cdada3221cbdc919c06",
    }
    observed = {name: sha256(path) for name, path in paths.items()}
    assert observed == pins

    parent_source = paths["parent_source"].read_text()
    child_source = paths["source"].read_text()
    assert parent_source.count("wall_seconds > 590") == 1
    expected_source = parent_source.replace("wall_seconds > 590", "wall_seconds > 350", 1)
    unsafe_final_order = (
        "    write_selected(&config.selected, &provider, &selected);\n"
        "    write_dual(&config.dual, config.prime, candidate.as_ref());\n"
        "    write_result("
    )
    safe_final_order = (
        "    write_dual(&config.dual, config.prime, candidate.as_ref());\n"
        "    write_selected(&config.selected, &provider, &selected);\n"
        "    write_result("
    )
    assert expected_source.count(unsafe_final_order) == 1
    expected_source = expected_source.replace(unsafe_final_order, safe_final_order, 1)
    assert child_source == expected_source

    parent_watchdog = paths["parent_watchdog"].read_text()
    expected_watchdog = parent_watchdog
    substitutions = (
        ("Fail-closed 12-GiB/600-second watchdog for one D11 triangle recovery.",
         "Fail-closed 16-GiB/360-second watchdog for one D11 triangle resume."),
        ("args.rss_gib != 12 or not 1 <= args.wall_seconds <= 600",
         "args.rss_gib != 16 or not 1 <= args.wall_seconds <= 360"),
        ("sealed 12-GiB, <=600-second D11 recovery", "sealed 16-GiB, <=360-second D11 resume"),
        ("KRENN_X5_D11_TRIANGLE_RECOVERY_WATCHDOG_12G_600_V1",
         "KRENN_X5_D11_TRIANGLE_RESUME_WATCHDOG_16G_360_V1"),
    )
    for old, new in substitutions:
        assert expected_watchdog.count(old) == 1
        expected_watchdog = expected_watchdog.replace(old, new, 1)
    assert paths["watchdog"].read_text() == expected_watchdog

    checkpoint = json.loads(paths["checkpoint_audit"].read_text())
    assert checkpoint["status"] == "PASS_RESTART_PAIR"
    assert checkpoint["degree"] == 11 and checkpoint["prime"] == 1_073_741_827
    assert checkpoint["provider_sha256"] == pins["provider"]
    assert checkpoint["selected_columns"] == checkpoint["selected_pairings_replayed"] == 94_526
    assert checkpoint["dual_support"] == 13_116
    assert checkpoint["target_coefficient"] == 1 and checkpoint["pairing_failures"] == 0
    assert not checkpoint["global_incident_scan_performed"]
    assert checkpoint["mathematical_verdict"] is None
    assert not checkpoint["second_prime_launched"] and not checkpoint["degree_twelve_launched"]

    contract = json.loads((HERE / "LAUNCH_CONTRACT.json").read_text())
    assert contract["status"] == "HOLD_PENDING_EXCLUSIVE_SLOT_CLEARANCE"
    assert contract["branch"] == "triangle_endpoint_colour" and contract["prime"] == 1_073_741_827
    assert contract["native_wall_seconds"] == 350 and contract["wrapper_wall_seconds"] == 360
    assert contract["rss_gib"] == 16 and contract["column_cap"] == 500_000
    assert contract["checkpoint_interval_seconds"] == 30 and contract["checkpoint_first_snapshot"]
    assert contract["checkpoint_write_order"] == "dual_then_selected"
    assert not contract["second_prime"] and not contract["degree_twelve"]
    assert not (HERE / "CLEARANCE.json").exists() and not OUTPUT.exists()

    selftest = subprocess.run([str(paths["binary"]), "--selftest"], cwd=REPO,
                              check=True, text=True, capture_output=True)
    selftest_result = json.loads(selftest.stdout)
    assert selftest_result["status"] == "PASS" and selftest_result["tests"] == 5

    held = subprocess.run(["python3", str(HERE / "run_resume.py")], cwd=REPO,
                          check=False, text=True, capture_output=True)
    assert held.returncode != 0 and "HOLD: missing explicit exclusive-slot CLEARANCE.json" in held.stderr
    assert not (HERE / "CLEARANCE.json").exists() and not OUTPUT.exists()

    parent_telemetry = json.loads(paths["parent_watchdog_result"].read_text())
    assert parent_telemetry["breach"] == "RSS_CAP" and not parent_telemetry["result_exists"]
    assert parent_telemetry["restart_pair_available"]
    assert parent_telemetry["restart_selected_sha256"] == pins["selected"]
    assert parent_telemetry["restart_dual_sha256"] == pins["dual"]
    elapsed = parent_telemetry["elapsed_seconds"]
    peak = parent_telemetry["peak_rss_kib"]
    projected_16g = elapsed * (16 / 12)
    assert abs(projected_16g - 340.894632) < 0.000001

    result = {
        "schema": "KRENN_X5_D11_TRIANGLE_RESUME16_DESIGN_AUDIT_V1",
        "status": "READY_HELD",
        "launch_verdict": "READY_ONLY_AFTER_EXCLUSIVE_CLEARANCE",
        "arithmetic_launched": False,
        "degree_twelve_cache_reads": False,
        "source_diff": {
            "changes": ["native wall guard 590 -> 350", "final checkpoint write order selected/dual -> dual/selected"],
            "math_changes": 0,
            "provider_changes": 0,
            "checkpoint_safety_changes": 1,
        },
        "watchdog_diff": {
            "resource_only": True,
            "rss_gib": [12, 16],
            "wrapper_wall_seconds": [600, 360],
            "schema_and_diagnostic_text_changes": 2,
        },
        "resume_checkpoint": {
            "selected_columns": 94_526,
            "dual_support": 13_116,
            "target_coefficient": 1,
            "selected_pairings_replayed": 94_526,
            "pairing_failures": 0,
            "checkpoint_first_snapshot_bytes": paths["selected"].stat().st_size + paths["dual"].stat().st_size,
        },
        "geometry": {
            "native_wall_seconds": 350,
            "wrapper_wall_seconds": 360,
            "rss_gib": 16,
            "column_cap": 500_000,
            "checkpoint_interval_seconds": 30,
        },
        "measured_parent": {
            "elapsed_seconds": elapsed,
            "peak_rss_kib": peak,
            "checkpoint_selected_columns": 94_526,
            "result_exists": False,
        },
        "projection": {
            "linear_time_to_16g_seconds": round(projected_16g, 6),
            "native_wall_headroom_after_linear_16g_projection_seconds": round(350 - projected_16g, 6),
            "interpretation": "diagnostic only; resume rebuild and pivot geometry can be nonlinear",
            "useful_progress": "plausible but not guaranteed; a new checkpoint requires rebuild plus one completed CEGAR round",
            "terminality_expected": False,
        },
        "compression": {
            "verdict": "PROMISING_SEPARATE_GATE_NOT_READY_FOR_THIS_RESUME",
            "exact_semantics_possible": True,
            "candidate_changes": [
                "ranked u32 row interning preserving frozen (frequency,Mono) order",
                "sorted compact sparse rows with exact modular merge/subtract",
                "u128 selected-column encoding with literal natural-order comparator",
                "provider rematerialization instead of retaining every selected vector",
            ],
            "promotion_gate": "1k then 5k sealed columns; identical candidate/support SHA and all pairings; require >=2x memory or material throughput win",
        },
        "pins": pins,
        "selftest": selftest_result,
        "clearance_present": False,
        "production_output_present": False,
    }
    atomic_json(HERE / "results_design_audit.json", result)
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
