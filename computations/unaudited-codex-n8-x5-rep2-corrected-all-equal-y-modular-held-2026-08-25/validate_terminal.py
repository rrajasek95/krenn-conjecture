#!/usr/bin/env python3
"""Validate the terminal single-lane result without rerunning Singular."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
REFEREE = ROOT / "computations/unaudited-codex-n8-x5-rep2-corrected-contraction-modular-held-referee-2026-08-25"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


assert sha256(HERE / "MANIFEST.sha256") == "174d817976688a75ef1826b6a5fb24f9b259cf7324a4022682abdf3e8f7bc214"
assert sha256(REFEREE / "FINAL_MANIFEST.sha256") == "986f819fcb4bcaa17bebaa60047624b16187f755d94897397acc372db6328692"
assert sha256(REFEREE / "INDEPENDENT_ACCEPTANCE_PAYLOAD.json") == "1f355debecd2b1ea02f1789f2da2df3a8e8f6972e6b6ad56b678ea3f00068322"
assert (HERE / "independent_referee_acceptance.json").read_bytes() == (REFEREE / "INDEPENDENT_ACCEPTANCE_PAYLOAD.json").read_bytes()
assert sha256(HERE / "launch_clearance.json") == "0e818be11aef41995a5735cb8311cfb6f7e9bd8741f6bba0143f0869fd9339ac"

result = json.loads((HERE / "result.json").read_text())
assert result["schema"] == "KRENN_X5_REP2_ALL_EQUAL_Y_ONE_LANE_RESULT_V1"
assert result["status"] == "UNIT_IDEAL_MODULAR_DIAGNOSTIC"
assert result["chart"] == "all-equal-y/i0/p00/x0/y0/d01"
assert result["field"] == "F_32003"
assert result["returncode"] == 0 and result["termination"] is None
assert result["stderr"] == ""
assert result["native_wall_cap_seconds"] == 180 and result["wrapper_wall_cap_seconds"] == 195
assert 0 < result["wall_seconds"] < 180
assert 0 < result["observed_peak_rss_bytes"] < result["rss_cap_bytes"] == 8589934592
assert result["held_manifest_sha256"] == "174d817976688a75ef1826b6a5fb24f9b259cf7324a4022682abdf3e8f7bc214"
assert result["independent_referee_acceptance_sha256"] == "1f355debecd2b1ea02f1789f2da2df3a8e8f6972e6b6ad56b678ea3f00068322"
assert result["launch_clearance_sha256"] == "0e818be11aef41995a5735cb8311cfb6f7e9bd8741f6bba0143f0869fd9339ac"
assert result["source_sha256"] == sha256(HERE / "rep2_all_equal_y_i0_p00_x0_y0_d01_p32003.sing") == "95147044a1703357db2045f393bea44759a854cf5d178b9329b150460ca9abe1"
assert result["runner_sha256"] == sha256(HERE / "run_one_lane.py") == "845bf7928d88b0c1109bc157fbca104423adc76408d1f98b9d470a93df0a180a"
assert result["singular_sha256"] == sha256(Path("/usr/local/bin/Singular")) == "9436b32ff7565719240230de8a6fb1d27af5e65f0ca4c9c5b756a77e82409b88"
for line in (
    "INPUT_VARIABLES=91",
    "INPUT_GENERATORS=6577",
    "GROEBNER_SIZE=1",
    "UNIT_REMAINDER=0",
    "STATUS=UNIT_IDEAL",
):
    assert result["stdout"].count(line) == 1, line
assert result["diagnostic_only"] is True and result["mathematical_coverage"] is False
assert result["second_lane_launched"] is False
assert result["exact_Q_launched"] is False
assert result["automatic_relaunch"] is False
assert not any(HERE.glob("*.tmp"))

print(json.dumps({
    "status": "PASS_TERMINAL_ONE_MODULAR_UNIT_DIAGNOSTIC",
    "result_sha256": sha256(HERE / "result.json"),
    "wall_seconds": result["wall_seconds"],
    "peak_rss_bytes": result["observed_peak_rss_bytes"],
    "mathematical_coverage": False,
}, sort_keys=True))
