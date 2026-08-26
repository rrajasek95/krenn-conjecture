#!/usr/bin/env python3
"""Fail-closed static audit of the held cap-1m continuation."""

import hashlib
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
PARENT = REPO / "computations/unaudited-codex-n8-x5-d11-triangle-resume24-cap750-held-2026-08-25"


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    pins = {
        "parent_source": "9b26ec7aff3e2117e31b2a593843466e2521adf7e17a4ff05bf0b6892fe8c53d",
        "parent_watchdog": "27e51205a359cbb5d85a741c5ddfc190a6b705b9e0c00a6244dd6f4e89812864",
        "parent_production_manifest": "7d5176a70b409a21b362725d7ae8f710640d5688604d2b10e04d5e3f611d8198",
        "source": "9d206429d53ce8a2c08b974d56c158860092aa799446429a05933b5e74322840",
        "binary": "6d5b237c92d7fa8f4023929a0fa15f3954090b0827d1974145cf5fe66012a8db",
        "watchdog": "07a950ab271418f19e888ea2aa068d8ee2f0de007b18a0cbc0bb33fa7b8e55e9",
        "runner": "a96170d9da00964c90e50eafe3dade361a80f7fed7520b26a853e214e212ef65",
        "selected": "e19fbb6b57ae672a130c38c03783845e39dceaea795ff371ec07973f6d8e82d5",
        "dual": "c56be60d563a1494a572a7bd6c89f9b03e928fc7ae22414644c9109767566fe3",
        "checkpoint_audit": "5e4918cc80a4a936b18a5add3f0d109af6d21af664cf67e65130ffe5ede3e6ab",
    }
    paths = {
        "parent_source": PARENT / "src/main.rs",
        "parent_watchdog": PARENT / "watchdog24_600_resume.py",
        "parent_production_manifest": PARENT / "PRODUCTION_MANIFEST.sha256",
        "source": HERE / "src/main.rs",
        "binary": HERE / "x5_d11_triangle_resume32_cap1m",
        "watchdog": HERE / "watchdog32_600_resume.py",
        "runner": HERE / "run_cap1m_resume.py",
        "selected": HERE / "sealed_resume_input/selected.tsv",
        "dual": HERE / "sealed_resume_input/dual.tsv",
        "checkpoint_audit": HERE / "sealed_resume_input/checkpoint_audit.json",
    }
    assert {name: sha(path) for name, path in paths.items()} == pins

    parent_source = paths["parent_source"].read_text()
    expected_source = parent_source.replace("column_cap > 750_000", "column_cap > 1_000_000", 1)
    assert expected_source != parent_source and paths["source"].read_text() == expected_source
    parent_watchdog = paths["parent_watchdog"].read_text()
    expected_watchdog = parent_watchdog
    for old, new in (
        ("Fail-closed 24-GiB/600-second watchdog for one cap-750k D11 triangle resume.",
         "Fail-closed 32-GiB/600-second watchdog for one cap-1m D11 triangle resume."),
        ("args.rss_gib != 24", "args.rss_gib != 32"),
        ("sealed 24-GiB, <=600-second cap-750k D11 resume",
         "sealed 32-GiB, <=600-second cap-1m D11 resume"),
        ("KRENN_X5_D11_TRIANGLE_CAP750_RESUME_WATCHDOG_24G_600_V1",
         "KRENN_X5_D11_TRIANGLE_CAP1M_RESUME_WATCHDOG_32G_600_V1"),
    ):
        assert expected_watchdog.count(old) == 1
        expected_watchdog = expected_watchdog.replace(old, new, 1)
    assert paths["watchdog"].read_text() == expected_watchdog
    runner = paths["runner"].read_text()
    for literal in ('"--column-cap", "1000000"', '"--wall-seconds", "590"',
                    '"--rss-gib", "32"', '"--wall-seconds", "600"'):
        assert runner.count(literal) == 1
    assert '"--column-cap", "750000"' not in runner

    contract = json.loads((HERE / "LAUNCH_CONTRACT.json").read_text())
    assert contract["status"] == "HOLD_PENDING_EXPLICIT_CLEARANCE"
    assert contract["parent_production_manifest_sha256"] == pins["parent_production_manifest"]
    assert contract["runner_sha256"] == pins["runner"]
    assert contract["column_cap"] == 1_000_000 and contract["rss_gib"] == 32
    assert contract["native_wall_seconds"] == 590 and contract["wrapper_wall_seconds"] == 600
    assert contract["checkpoint_first_snapshot"] and contract["checkpoint_write_order"] == "dual_then_selected"

    checkpoint = json.loads(paths["checkpoint_audit"].read_text())
    assert checkpoint["status"] == "PASS_FAIL_CLOSED_COLUMN_CAP_CHECKPOINT_CAP750"
    assert checkpoint["selected_columns"] == checkpoint["selected_pairings_replayed"] == 515_869
    assert checkpoint["dual_support"] == 427_712 and checkpoint["pairing_failures"] == 0
    selftest = json.loads(subprocess.run([str(paths["binary"]), "--selftest"], check=True,
                                         text=True, capture_output=True).stdout)
    assert selftest["status"] == "PASS"

    prior_watch = json.loads((PARENT / "production_cap750_resume_p1073741827_triangle_endpoint_colour/watchdog.json").read_text())
    prior_result = json.loads((PARENT / "production_cap750_resume_p1073741827_triangle_endpoint_colour/result.json").read_text())
    assert prior_watch["peak_rss_kib"] == 12_067_360
    assert prior_result["selected_columns"] == 515_869 and prior_result["dual_support"] == 427_712
    assert prior_result["rounds"][-1]["new_violations"] == 234_132
    linear_cap_rss_kib = prior_watch["peak_rss_kib"] * 1_000_000 / 515_869
    margin_rss_kib = linear_cap_rss_kib * 1.25
    assert margin_rss_kib < 32 * 1024 * 1024

    assert not (HERE / "CLEARANCE.json").exists()
    assert not (HERE / "production_cap1m_resume_p1073741827_triangle_endpoint_colour").exists()
    held = subprocess.run(["python3", str(HERE / "run_cap1m_resume.py")], cwd=REPO,
                          check=False, text=True, capture_output=True)
    assert held.returncode != 0 and "HOLD:" in held.stderr
    result = {
        "schema": "KRENN_X5_D11_TRIANGLE_CAP1M_RESUME32_DESIGN_AUDIT_V1",
        "status": "PASS_HELD",
        "source_diff": {"sole_change": "column cap guard 750000 -> 1000000",
                        "math_changes": 0, "provider_changes": 0, "wall_changes": 0,
                        "checkpoint_changes": 0},
        "watchdog_diff": {"resource_only": True, "rss_gib": [24, 32],
                          "native_wall_seconds": 590, "wrapper_wall_seconds": 600},
        "checkpoint": {"selected_columns": 515_869, "dual_support": 427_712,
                       "pairings_replayed": 515_869, "failures": 0},
        "preflight": {"prior_peak_rss_kib": prior_watch["peak_rss_kib"],
                      "linear_rss_at_1m_kib": linear_cap_rss_kib,
                      "linear_plus_25pct_margin_kib": margin_rss_kib,
                      "rss_cap_kib": 32 * 1024 * 1024,
                      "known_prior_violations": 234_132,
                      "new_cap_remaining_from_seed": 484_131,
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
