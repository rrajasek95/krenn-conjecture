#!/usr/bin/env python3
"""Fail-closed static audit of the held cap-750k continuation."""

import hashlib
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
PARENT = REPO / "computations/unaudited-codex-n8-x5-d11-triangle-resume20-advanced-2026-08-25"


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    pins = {
        "parent_source": "855ef288b03f2c07f4c8988a738aeb3409e5909e208c6c0ef8966eb8c8923035",
        "parent_watchdog": "05917823ff4b8b152d12f16112473af6acd6b8174fa94db6a74e66f35ad01011",
        "parent_production_manifest": "a41b060659d86a3fbd908a8f2241b0bf6b52fe0f57bd7ce1f253482412fb0232",
        "source": "9b26ec7aff3e2117e31b2a593843466e2521adf7e17a4ff05bf0b6892fe8c53d",
        "binary": "53fb7ab0c2e565ca5376821b1b8db625c7709a1a354c22bd0f1074d9cd496a93",
        "watchdog": "27e51205a359cbb5d85a741c5ddfc190a6b705b9e0c00a6244dd6f4e89812864",
        "selected": "e3c300a7992e22ffb52e79f84ae4e87a64a4a9951fb2c0794461bf2077e4994f",
        "dual": "eeea4d8278a798ae829f28ac92a70bbdff9b3660144b618835091c470cbcbdea",
        "checkpoint_audit": "947b95df9bd37cf5bf31ab4ad6e03dc457507c6216c82943443246d558440aba",
    }
    paths = {
        "parent_source": PARENT / "src/main.rs", "parent_watchdog": PARENT / "watchdog20_600_resume.py",
        "parent_production_manifest": PARENT / "PRODUCTION_MANIFEST.sha256",
        "source": HERE / "src/main.rs", "binary": HERE / "x5_d11_triangle_resume24_cap750",
        "watchdog": HERE / "watchdog24_600_resume.py", "selected": HERE / "sealed_resume_input/selected.tsv",
        "dual": HERE / "sealed_resume_input/dual.tsv",
        "checkpoint_audit": HERE / "sealed_resume_input/checkpoint_audit.json",
    }
    assert {name: sha(path) for name, path in paths.items()} == pins
    parent_source = paths["parent_source"].read_text()
    expected_source = parent_source.replace("column_cap > 500_000", "column_cap > 750_000", 1)
    assert expected_source != parent_source and paths["source"].read_text() == expected_source
    parent_watchdog = paths["parent_watchdog"].read_text()
    expected_watchdog = parent_watchdog
    for old, new in (
        ("Fail-closed 20-GiB/600-second watchdog for one advanced D11 triangle resume.",
         "Fail-closed 24-GiB/600-second watchdog for one cap-750k D11 triangle resume."),
        ("args.rss_gib != 20", "args.rss_gib != 24"),
        ("sealed 20-GiB, <=600-second advanced D11 resume", "sealed 24-GiB, <=600-second cap-750k D11 resume"),
        ("KRENN_X5_D11_TRIANGLE_ADVANCED_RESUME_WATCHDOG_20G_600_V1",
         "KRENN_X5_D11_TRIANGLE_CAP750_RESUME_WATCHDOG_24G_600_V1"),
    ):
        assert expected_watchdog.count(old) == 1
        expected_watchdog = expected_watchdog.replace(old, new, 1)
    assert paths["watchdog"].read_text() == expected_watchdog
    checkpoint = json.loads(paths["checkpoint_audit"].read_text())
    assert checkpoint["status"] == "PASS_FAIL_CLOSED_COLUMN_CAP_CHECKPOINT_ADVANCED"
    assert checkpoint["selected_columns"] == checkpoint["selected_pairings_replayed"] == 307_885
    assert checkpoint["dual_support"] == 184_659 and checkpoint["pairing_failures"] == 0
    selftest = json.loads(subprocess.run([str(paths["binary"]), "--selftest"], check=True,
                                         text=True, capture_output=True).stdout)
    assert selftest["status"] == "PASS"
    prior_watch = json.loads((PARENT / "production_advanced_resume_p1073741827_triangle_endpoint_colour/watchdog.json").read_text())
    prior_result = json.loads((PARENT / "production_advanced_resume_p1073741827_triangle_endpoint_colour/result.json").read_text())
    assert prior_watch["peak_rss_kib"] == 7_099_376 and prior_result["selected_columns"] == 307_885
    linear_cap_rss_kib = prior_watch["peak_rss_kib"] * 750_000 / 307_885
    margin_rss_kib = linear_cap_rss_kib * 1.25
    assert margin_rss_kib < 24 * 1024 * 1024
    assert not (HERE / "CLEARANCE.json").exists()
    assert not (HERE / "production_cap750_resume_p1073741827_triangle_endpoint_colour").exists()
    held = subprocess.run(["python3", str(HERE / "run_cap750_resume.py")], cwd=REPO,
                          check=False, text=True, capture_output=True)
    assert held.returncode != 0 and "HOLD: r1538 audit/compaction and explicit clearance required" in held.stderr
    result = {
        "schema": "KRENN_X5_D11_TRIANGLE_CAP750_RESUME24_DESIGN_AUDIT_V1",
        "status": "PASS_HELD",
        "source_diff": {"sole_change": "column cap guard 500000 -> 750000", "math_changes": 0,
                        "provider_changes": 0, "wall_changes": 0, "checkpoint_changes": 0},
        "watchdog_diff": {"resource_only": True, "rss_gib": [20, 24],
                          "native_wall_seconds": 590, "wrapper_wall_seconds": 600},
        "checkpoint": {"selected_columns": 307_885, "dual_support": 184_659,
                       "pairings_replayed": 307_885, "failures": 0},
        "preflight": {"prior_peak_rss_kib": prior_watch["peak_rss_kib"],
                      "linear_rss_at_750k_kib": linear_cap_rss_kib,
                      "linear_plus_25pct_margin_kib": margin_rss_kib,
                      "rss_cap_kib": 24 * 1024 * 1024,
                      "known_prior_violations": 192_116,
                      "new_cap_remaining_from_seed": 442_115,
                      "verdict": "FEASIBLE_HELD; projection diagnostic only"},
        "pins": pins, "selftest": selftest,
        "clearance_present": False, "output_present": False,
        "arithmetic_launched": False, "degree_twelve_reads": False,
    }
    temporary = HERE / "results_design_audit.json.tmp"
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    temporary.replace(HERE / "results_design_audit.json")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
