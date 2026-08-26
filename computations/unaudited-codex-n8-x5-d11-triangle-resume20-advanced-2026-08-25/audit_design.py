#!/usr/bin/env python3
"""Static fail-closed audit of the held advanced D11 resume."""

import hashlib
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
PARENT = REPO / "computations/unaudited-codex-n8-x5-d11-triangle-resume16-design-2026-08-25"


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    pins = {
        "parent_source": "936ad21fa4aa8ed0ffe78dc090d9e85ddeefa33713be75c1daa1bcd5f7aca142",
        "parent_watchdog": "5a83fe143da9e4c7f646874f97944a4858b21362e5bbf91da98e3794fd0a3fd4",
        "parent_production_manifest": "2e1c3a4027a89eac8da2dc90dfa6e95d878cf6098ae08944a7b5f811cda65f41",
        "source": "855ef288b03f2c07f4c8988a738aeb3409e5909e208c6c0ef8966eb8c8923035",
        "binary": "9abae41a47cc0b5e0a1c93bbdc9bc13c3497d2f7cd1326dcf69c3831ae121d6a",
        "watchdog": "05917823ff4b8b152d12f16112473af6acd6b8174fa94db6a74e66f35ad01011",
        "selected": "9c70caaf26b71345b03565dbdf2edba8c52f06eca4ad74d6e7b888fa8a49cca5",
        "dual": "06ded311e326a66105d69ae7be2eb56c7ba9720ab19718f7cd173c09efb2ce02",
        "checkpoint_audit": "5f5152302fb3f0e48fde944eb8aba7904479e73337ad46d4d1f18c6daa4077fd",
    }
    paths = {
        "parent_source": PARENT / "src/main.rs",
        "parent_watchdog": PARENT / "watchdog16_360_resume.py",
        "parent_production_manifest": PARENT / "PRODUCTION_MANIFEST.sha256",
        "source": HERE / "src/main.rs", "binary": HERE / "x5_d11_triangle_resume20",
        "watchdog": HERE / "watchdog20_600_resume.py",
        "selected": HERE / "sealed_resume_input/selected.tsv",
        "dual": HERE / "sealed_resume_input/dual.tsv",
        "checkpoint_audit": HERE / "sealed_resume_input/checkpoint_audit.json",
    }
    assert {name: sha(path) for name, path in paths.items()} == pins
    parent_source = paths["parent_source"].read_text()
    assert paths["source"].read_text() == parent_source.replace("wall_seconds > 350", "wall_seconds > 590", 1)
    parent_watchdog = paths["parent_watchdog"].read_text()
    expected = parent_watchdog
    changes = (
        ("Fail-closed 16-GiB/360-second watchdog for one D11 triangle resume.",
         "Fail-closed 20-GiB/600-second watchdog for one advanced D11 triangle resume."),
        ("args.rss_gib != 16 or not 1 <= args.wall_seconds <= 360",
         "args.rss_gib != 20 or not 1 <= args.wall_seconds <= 600"),
        ("sealed 16-GiB, <=360-second D11 resume", "sealed 20-GiB, <=600-second advanced D11 resume"),
        ("KRENN_X5_D11_TRIANGLE_RESUME_WATCHDOG_16G_360_V1",
         "KRENN_X5_D11_TRIANGLE_ADVANCED_RESUME_WATCHDOG_20G_600_V1"),
    )
    for old, new in changes:
        assert expected.count(old) == 1
        expected = expected.replace(old, new, 1)
    assert paths["watchdog"].read_text() == expected
    checkpoint = json.loads(paths["checkpoint_audit"].read_text())
    assert checkpoint["status"] == "PASS_FAIL_CLOSED_CHECKPOINT_ADVANCED"
    assert checkpoint["selected_columns"] == checkpoint["selected_pairings_replayed"] == 230_091
    assert checkpoint["dual_support"] == 80_922 and checkpoint["pairing_failures"] == 0
    selftest = json.loads(subprocess.run([str(paths["binary"]), "--selftest"], check=True,
                                         text=True, capture_output=True).stdout)
    assert selftest["status"] == "PASS"
    prior = json.loads((PARENT / "production_resume_p1073741827_triangle_endpoint_colour/watchdog.json").read_text())
    assert prior["elapsed_seconds"] == 360.177739 and prior["peak_rss_kib"] == 15_308_688
    projection = prior["elapsed_seconds"] * (20 * 1024 * 1024) / prior["peak_rss_kib"]
    assert 493 < projection < 494
    result = {
        "schema": "KRENN_X5_D11_TRIANGLE_ADVANCED_RESUME20_DESIGN_AUDIT_V1",
        "status": "PASS_READY_TO_SEAL",
        "source_diff": {"sole_change": "wall guard 350 -> 590", "math_changes": 0,
                        "provider_changes": 0, "checkpoint_changes": 0},
        "watchdog_diff": {"resource_only": True, "rss_gib": [16, 20],
                          "wrapper_wall_seconds": [360, 600]},
        "checkpoint": {"selected_columns": 230_091, "dual_support": 80_922,
                       "pairings_replayed": 230_091, "failures": 0},
        "preflight": {"prior_elapsed_seconds": prior["elapsed_seconds"],
                      "prior_peak_rss_kib": prior["peak_rss_kib"],
                      "linear_20g_projection_seconds": projection,
                      "native_wall_headroom_seconds": 590 - projection,
                      "verdict": "ACCEPT_BOUNDED; useful persistence plausible but nonlinear"},
        "geometry": {"native_wall_seconds": 590, "wrapper_wall_seconds": 600,
                     "rss_gib": 20, "column_cap": 500_000},
        "pins": pins, "selftest": selftest,
        "arithmetic_launched": False, "degree_twelve_reads": False,
    }
    temporary = HERE / "results_design_audit.json.tmp"
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    temporary.replace(HERE / "results_design_audit.json")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
