#!/usr/bin/env python3
"""Fail-closed static audit of the held cap-1.25m continuation."""

import hashlib
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
PARENT = REPO / "computations/unaudited-codex-n8-x5-d11-triangle-resume32-cap1m-held-2026-08-25"


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    pins = {
        "parent_source": "9d206429d53ce8a2c08b974d56c158860092aa799446429a05933b5e74322840",
        "parent_watchdog": "07a950ab271418f19e888ea2aa068d8ee2f0de007b18a0cbc0bb33fa7b8e55e9",
        "parent_production_manifest": "07410690da03aa6b1509081db9051ca0d1858daf77c502d0b4c2f307658310d8",
        "source": "c9d296f4bef3cc8e706d948d3f72e37003eccdbf59e3288a1be2bd4b2b1d0182",
        "binary": "7e87a4d4f2bca06478178f98e90d62c9eb207a5873ade804249da9bef42e1602",
        "watchdog": "854042e448cca17a6a1154934bb229dec794f72f8f528c265b7d2de0ebb107a3",
        "runner": "dfde71889371f1f1a3957a252730e64a3346a8fb159dd8f31eb5b998576732de",
        "selected": "81b4c5b8f929b26a8a7dc839a3638c8be9bd7973df843c131e4fc0b1056313c8",
        "dual": "c2c0d95e2063e1437e05b42169879d018031a6b5625955bd548cbca4880ca284",
        "checkpoint_audit": "db6d963a6971ad25d9d3b71502807f1f079539607ca4ada9f6c82f354c52a1dc",
    }
    paths = {
        "parent_source": PARENT / "src/main.rs",
        "parent_watchdog": PARENT / "watchdog32_600_resume.py",
        "parent_production_manifest": PARENT / "PRODUCTION_MANIFEST.sha256",
        "source": HERE / "src/main.rs",
        "binary": HERE / "x5_d11_triangle_resume38_cap1250",
        "watchdog": HERE / "watchdog38_600_resume.py",
        "runner": HERE / "run_cap1250_resume.py",
        "selected": HERE / "sealed_resume_input/selected.tsv",
        "dual": HERE / "sealed_resume_input/dual.tsv",
        "checkpoint_audit": HERE / "sealed_resume_input/checkpoint_audit.json",
    }
    assert {name: sha(path) for name, path in paths.items()} == pins

    parent_source = paths["parent_source"].read_text()
    expected_source = parent_source.replace("column_cap > 1_000_000", "column_cap > 1_250_000", 1)
    assert expected_source != parent_source and paths["source"].read_text() == expected_source
    parent_watchdog = paths["parent_watchdog"].read_text()
    expected_watchdog = parent_watchdog
    for old, new in (
        ("Fail-closed 32-GiB/600-second watchdog for one cap-1m D11 triangle resume.",
         "Fail-closed 38-GiB/600-second watchdog for one cap-1.25m D11 triangle resume."),
        ("args.rss_gib != 32", "args.rss_gib != 38"),
        ("sealed 32-GiB, <=600-second cap-1m D11 resume",
         "sealed 38-GiB, <=600-second cap-1.25m D11 resume"),
        ("KRENN_X5_D11_TRIANGLE_CAP1M_RESUME_WATCHDOG_32G_600_V1",
         "KRENN_X5_D11_TRIANGLE_CAP1250_RESUME_WATCHDOG_38G_600_V1"),
    ):
        assert expected_watchdog.count(old) == 1
        expected_watchdog = expected_watchdog.replace(old, new, 1)
    assert paths["watchdog"].read_text() == expected_watchdog
    runner = paths["runner"].read_text()
    for literal in ('"--column-cap", "1250000"', '"--wall-seconds", "590"',
                    '"--rss-gib", "38"', '"--wall-seconds", "600"'):
        assert runner.count(literal) == 1
    assert '"--column-cap", "1000000"' not in runner

    contract = json.loads((HERE / "LAUNCH_CONTRACT.json").read_text())
    assert contract["status"] == "HOLD_PENDING_EXPLICIT_CLEARANCE"
    assert contract["parent_production_manifest_sha256"] == pins["parent_production_manifest"]
    assert contract["runner_sha256"] == pins["runner"]
    assert contract["column_cap"] == 1_250_000 and contract["rss_gib"] == 38
    assert contract["native_wall_seconds"] == 590 and contract["wrapper_wall_seconds"] == 600
    assert contract["checkpoint_first_snapshot"] and contract["checkpoint_write_order"] == "dual_then_selected"

    checkpoint = json.loads(paths["checkpoint_audit"].read_text())
    assert checkpoint["status"] == "PASS_FAIL_CLOSED_COLUMN_CAP_CHECKPOINT_CAP1M"
    assert checkpoint["selected_columns"] == checkpoint["selected_pairings_replayed"] == 913_636
    assert checkpoint["dual_support"] == 924_170 and checkpoint["pairing_failures"] == 0
    selftest = json.loads(subprocess.run([str(paths["binary"]), "--selftest"], check=True,
                                         text=True, capture_output=True).stdout)
    assert selftest["status"] == "PASS"

    prior_watch = json.loads((PARENT / "production_cap1m_resume_p1073741827_triangle_endpoint_colour/watchdog.json").read_text())
    prior_result = json.loads((PARENT / "production_cap1m_resume_p1073741827_triangle_endpoint_colour/result.json").read_text())
    assert prior_watch["peak_rss_kib"] == 20_707_504
    assert prior_result["selected_columns"] == 913_636 and prior_result["dual_support"] == 924_170
    assert prior_result["rounds"][-1]["new_violations"] == 86_365
    linear_cap_rss_kib = prior_watch["peak_rss_kib"] * 1_250_000 / 913_636
    margin_rss_kib = linear_cap_rss_kib * 1.25
    assert margin_rss_kib < 38 * 1024 * 1024

    assert not (HERE / "CLEARANCE.json").exists()
    assert not (HERE / "production_cap1250_resume_p1073741827_triangle_endpoint_colour").exists()
    held = subprocess.run(["python3", str(HERE / "run_cap1250_resume.py")], cwd=REPO,
                          check=False, text=True, capture_output=True)
    assert held.returncode != 0 and "HOLD:" in held.stderr
    result = {
        "schema": "KRENN_X5_D11_TRIANGLE_CAP1250_RESUME38_DESIGN_AUDIT_V1",
        "status": "PASS_HELD",
        "source_diff": {"sole_change": "column cap guard 1000000 -> 1250000",
                        "math_changes": 0, "provider_changes": 0, "wall_changes": 0,
                        "checkpoint_changes": 0},
        "watchdog_diff": {"resource_only": True, "rss_gib": [32, 38],
                          "native_wall_seconds": 590, "wrapper_wall_seconds": 600},
        "checkpoint": {"selected_columns": 913_636, "dual_support": 924_170,
                       "pairings_replayed": 913_636, "failures": 0},
        "preflight": {"prior_peak_rss_kib": prior_watch["peak_rss_kib"],
                      "linear_rss_at_1250k_kib": linear_cap_rss_kib,
                      "linear_plus_25pct_margin_kib": margin_rss_kib,
                      "rss_cap_kib": 38 * 1024 * 1024,
                      "known_prior_violations": 86_365,
                      "new_cap_remaining_from_seed": 336_364,
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
