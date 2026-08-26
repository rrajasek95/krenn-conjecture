#!/usr/bin/env python3
"""Independent referee for the single rep1 guard-minor modular diagnostic."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
RUN = ROOT / "computations/unaudited-codex-n8-x5-seven-block-rep1-guard-minor-diagnostic-2026-08-25"
SOURCE_DIR = ROOT / "computations/unaudited-codex-n8-x5-seven-block-rep1-guard-minor-quotient-2026-08-25"
SOURCE = SOURCE_DIR / "rep1_minor_i0_p00_x0_y0_d01_p32003.sing"
DESIGN_REF = ROOT / "computations/unaudited-codex-n8-x5-seven-block-rep1-guard-minor-quotient-referee-2026-08-25"
PINS = {
    RUN / "MANIFEST.sha256": "df0964395da2742bf1df6cd322dcdbe7e5d13113d0c8967b12176e5ed2a98351",
    RUN / "PRELAUNCH_MANIFEST.sha256": "1ac0c0c1c657ae3fdbb228c4af100e332b7dfd557e8dea5c1ece8707f766f61a",
    RUN / "run_one_lane.py": "72a80924d7c61fe9e60351ab17a3b76462b810eb607971ba09d8c475764755de",
    RUN / "clearance.json": "b118e4a476cddd8bdcdcc2d6fff8dc6b827a35f27844ecab1b3ff1d4a0001d6b",
    RUN / "result.json": "24edfc0c4680b57d0ec7ea0df62485ceb9f08062ff6153ed608839cdf988766c",
    SOURCE_DIR / "MANIFEST.sha256": "4f367478c0a91257022234f5115979423bc8e889dd81a74cc3c200e25e3f82c1",
    SOURCE: "edd174ccbc75a563fd67e0515b6dde2c54e5469b742629953080290fe7d1fb49",
    DESIGN_REF / "FINAL_MANIFEST.sha256": "16226d5f15d9f0d2d419095ec3842a7122ad77b40c1abe83bc9afe1b45b7800c",
    Path("/usr/local/bin/Singular"): "9436b32ff7565719240230de8a6fb1d27af5e65f0ca4c9c5b756a77e82409b88",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def replay_manifest(path: Path, base: Path):
    for line in path.read_text().splitlines():
        expected, relative = line.split("  ", 1)
        assert sha256(base / relative) == expected


def main():
    for path, expected in PINS.items():
        assert sha256(path) == expected, path
    replay_manifest(RUN / "MANIFEST.sha256", RUN)
    replay_manifest(RUN / "PRELAUNCH_MANIFEST.sha256", RUN)

    clearance = json.loads((RUN / "clearance.json").read_text())
    assert clearance == {
        "maximum_lane_count": 1,
        "no_exact_Q": True,
        "no_relaunch": True,
        "referee_manifest_sha256": PINS[DESIGN_REF / "FINAL_MANIFEST.sha256"],
        "status": "EXPLICIT_MANAGER_CLEARANCE",
    }

    source = SOURCE.read_text()
    ring = next(line for line in source.splitlines() if line.startswith("ring r="))
    assert ring.startswith("ring r=32003,")
    variables = ring.split(",(", 1)[1].split("),dp;", 1)[0].split(",")
    assert len(variables) == len(set(variables)) == 91
    equations = source.split("ideal I=", 1)[1].split(";\nprint(", 1)[0].split(",\n")
    assert len(equations) == len(set(equations)) == 6577
    assert 'ideal G=slimgb(I);' in source
    assert 'poly remainder=reduce(1,G);' in source
    assert 'if (remainder==0) { print("STATUS=UNIT_IDEAL"); }' in source

    result = json.loads((RUN / "result.json").read_text())
    assert result["schema"] == "KRENN_X5_REP1_GUARD_MINOR_ONE_LANE_DIAGNOSTIC_V1"
    assert result["status"] == "UNIT_IDEAL_MODULAR_DIAGNOSTIC"
    assert result["chart"] == "all-equal-y/i0/p00/x0/y0/d01"
    assert result["field"] == "F_32003"
    assert result["termination"] is None and result["returncode"] == 0 and result["stderr"] == ""
    assert result["native_wall_cap_seconds"] == 300 and result["wrapper_wall_cap_seconds"] == 310
    assert result["rss_cap_bytes"] == 8 * 1024**3
    assert result["wall_seconds"] == 13.57906291692052
    assert result["observed_peak_rss_bytes"] == 733069312
    stdout = result["stdout"]
    for line in ("INPUT_GENERATORS=6577", "GROEBNER_SIZE=1", "UNIT_REMAINDER=0", "STATUS=UNIT_IDEAL"):
        assert stdout.count(line) == 1
    assert result["pins"] == {str(path): digest for path, digest in PINS.items() if path in (
        SOURCE_DIR / "MANIFEST.sha256", SOURCE, DESIGN_REF / "FINAL_MANIFEST.sha256", Path("/usr/local/bin/Singular"))
    }
    assert result["diagnostic_only"] is True and result["mathematical_coverage"] is False
    assert result["second_lane_launched"] is False and result["exact_Q_launched"] is False
    names = {path.name for path in RUN.iterdir() if path.is_file()}
    assert names == {"MANIFEST.sha256", "PRELAUNCH_MANIFEST.sha256", "REPORT.md", "clearance.json", "result.json", "run_one_lane.py", "validate.py"}
    assert not any(name.endswith(".tmp") for name in names)

    audited = {
        "schema": "KRENN_X5_REP1_GUARD_MINOR_MODULAR_DIAGNOSTIC_REFEREE_V1",
        "status": "PASS_UNIT_IDEAL_MODULAR_DIAGNOSTIC_ONLY",
        "producer_manifest_sha256": PINS[RUN / "MANIFEST.sha256"],
        "result_sha256": PINS[RUN / "result.json"],
        "input": {"field": "F_32003", "variables": 91, "generators": 6577, "sha256": PINS[SOURCE]},
        "terminal": {
            "returncode": 0,
            "basis_size": 1,
            "remainder_of_one": 0,
            "wall_seconds": result["wall_seconds"],
            "peak_rss_bytes": result["observed_peak_rss_bytes"],
        },
        "exclusions": {"second_modular_lane": True, "exact_Q": True, "relaunch": True, "temporary_outputs": True},
        "scope": {"modular_chart_eliminated": True, "characteristic_zero_coverage": False, "rep1_closed": False, "ideal_runs_by_referee": 0, "D12_reads": False},
    }
    temporary = HERE / "results_referee.json.tmp"
    temporary.write_text(json.dumps(audited, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, HERE / "results_referee.json")
    print(json.dumps({"status": audited["status"], "Q": False, "relaunch": False}, sort_keys=True))


if __name__ == "__main__":
    main()
