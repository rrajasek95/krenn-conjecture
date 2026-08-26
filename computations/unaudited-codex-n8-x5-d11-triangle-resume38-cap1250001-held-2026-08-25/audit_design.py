#!/usr/bin/env python3
"""Fail-closed static audit of held cap-1,250,001 continuation."""

import hashlib
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
PARENT = REPO / "computations/unaudited-codex-n8-x5-d11-triangle-resume38-cap1250-held-2026-08-25"


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    pins = {
        "parent_source": "c9d296f4bef3cc8e706d948d3f72e37003eccdbf59e3288a1be2bd4b2b1d0182",
        "parent_watchdog": "854042e448cca17a6a1154934bb229dec794f72f8f528c265b7d2de0ebb107a3",
        "parent_production_manifest": "97b468162f7c5c58ecfc3c35f124d5c052738bc63cd8d6a2eaa2a995e7553825",
        "source": "1f6fdab1da6b0821f7188efac30c7b4d5597b18414b52947eb50278b6894390d",
        "binary": "f49fc3aa5b4bc93d06ada200d4c32eb30b2c2a5b67475431390f3aedbb610c82",
        "watchdog": "854042e448cca17a6a1154934bb229dec794f72f8f528c265b7d2de0ebb107a3",
        "runner": "c90d3ff3fd9a8862c4bc4283b32c0fc0e1adf02b61b3327b0f970bb6131b2d6c",
        "selected": "81b4c5b8f929b26a8a7dc839a3638c8be9bd7973df843c131e4fc0b1056313c8",
        "dual": "c2c0d95e2063e1437e05b42169879d018031a6b5625955bd548cbca4880ca284",
        "checkpoint_audit": "68170d3b81f3e71e40ad2d00f6c034172deb88723f6764a4df7aa8838dee5669",
    }
    paths = {
        "parent_source": PARENT / "src/main.rs",
        "parent_watchdog": PARENT / "watchdog38_600_resume.py",
        "parent_production_manifest": PARENT / "PRODUCTION_MANIFEST.sha256",
        "source": HERE / "src/main.rs",
        "binary": HERE / "x5_d11_triangle_resume38_cap1250001",
        "watchdog": HERE / "watchdog38_600_resume.py",
        "runner": HERE / "run_cap1250001_resume.py",
        "selected": HERE / "sealed_resume_input/selected.tsv",
        "dual": HERE / "sealed_resume_input/dual.tsv",
        "checkpoint_audit": HERE / "sealed_resume_input/checkpoint_audit.json",
    }
    assert {name: sha(path) for name, path in paths.items()} == pins

    parent_source = paths["parent_source"].read_text()
    expected_source = parent_source.replace("column_cap > 1_250_000", "column_cap > 1_250_001", 1)
    assert expected_source != parent_source and paths["source"].read_text() == expected_source
    parent_watchdog = paths["parent_watchdog"].read_text()
    assert paths["watchdog"].read_text() == parent_watchdog
    runner = paths["runner"].read_text()
    for literal in ('"--column-cap", "1250001"', '"--wall-seconds", "590"',
                    '"--rss-gib", "38"', '"--wall-seconds", "600"'):
        assert runner.count(literal) == 1
    assert '"--column-cap", "1250000"' not in runner

    contract = json.loads((HERE / "LAUNCH_CONTRACT.json").read_text())
    assert contract["status"] == "HOLD_PENDING_EXPLICIT_CLEARANCE"
    assert contract["parent_production_manifest_sha256"] == pins["parent_production_manifest"]
    assert contract["runner_sha256"] == pins["runner"]
    assert contract["column_cap"] == 1_250_001 and contract["rss_gib"] == 38
    assert contract["native_wall_seconds"] == 590 and contract["wrapper_wall_seconds"] == 600
    assert contract["checkpoint_first_snapshot"] and contract["checkpoint_write_order"] == "dual_then_selected"

    checkpoint = json.loads(paths["checkpoint_audit"].read_text())
    assert checkpoint["status"] == "PASS_FAIL_CLOSED_COLUMN_CAP_CHECKPOINT_CAP1250_NO_PROGRESS"
    assert checkpoint["selected_columns"] == checkpoint["selected_pairings_replayed"] == 913_636
    assert checkpoint["dual_support"] == 924_170 and checkpoint["pairing_failures"] == 0
    selftest = json.loads(subprocess.run([str(paths["binary"]), "--selftest"], check=True,
                                         text=True, capture_output=True).stdout)
    assert selftest["status"] == "PASS"

    prior_watch = json.loads((PARENT / "production_cap1250_resume_p1073741827_triangle_endpoint_colour/watchdog.json").read_text())
    prior_result = json.loads((PARENT / "production_cap1250_resume_p1073741827_triangle_endpoint_colour/result.json").read_text())
    assert prior_watch["peak_rss_kib"] == 21_473_088
    assert prior_result["selected_columns"] == 913_636 and prior_result["dual_support"] == 924_170
    assert prior_result["rounds"][-1]["new_violations"] == 336_365
    linear_cap_rss_kib = prior_watch["peak_rss_kib"] * 1_250_001 / 913_636
    margin_rss_kib = linear_cap_rss_kib * 1.25
    assert margin_rss_kib < 38 * 1024 * 1024

    assert not (HERE / "CLEARANCE.json").exists()
    assert not (HERE / "production_cap1250001_resume_p1073741827_triangle_endpoint_colour").exists()
    held = subprocess.run(["python3", str(HERE / "run_cap1250001_resume.py")], cwd=REPO,
                          check=False, text=True, capture_output=True)
    assert held.returncode != 0 and "HOLD:" in held.stderr
    result = {
        "schema": "KRENN_X5_D11_TRIANGLE_CAP1250001_RESUME38_DESIGN_AUDIT_V1",
        "status": "PASS_HELD",
        "source_diff": {"sole_change": "column cap guard 1250000 -> 1250001",
                        "math_changes": 0, "provider_changes": 0, "wall_changes": 0,
                        "checkpoint_changes": 0},
        "watchdog_diff": {"resource_only": False, "rss_gib": [38, 38], "byte_identical": True,
                          "native_wall_seconds": 590, "wrapper_wall_seconds": 600},
        "checkpoint": {"selected_columns": 913_636, "dual_support": 924_170,
                       "pairings_replayed": 913_636, "failures": 0},
        "preflight": {"prior_peak_rss_kib": prior_watch["peak_rss_kib"],
                      "linear_rss_at_1250001_kib": linear_cap_rss_kib,
                      "linear_plus_25pct_margin_kib": margin_rss_kib,
                      "rss_cap_kib": 38 * 1024 * 1024,
                      "known_prior_violations": 336_365,
                      "new_cap_remaining_from_seed": 336_365,
                      "verdict": "FEASIBLE_HELD; projection diagnostic only"},
        "pins": pins,
        "selftest": selftest,
        "clearance_present": False,
        "output_present": False,
        "arithmetic_launched": False,
        "degree_twelve_reads": False,
    }
    temporary = HERE / "results_design_audit.json.tmp"
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    temporary.replace(HERE / "results_design_audit.json")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
