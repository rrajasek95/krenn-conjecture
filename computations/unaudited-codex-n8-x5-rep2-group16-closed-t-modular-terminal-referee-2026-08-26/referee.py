#!/usr/bin/env python3
"""Independent terminal replay of rep2 group16 closed-t modular pilot."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
RUN = ROOT / "computations/unaudited-codex-n8-x5-rep2-group16-closed-t-modular-held-2026-08-26"
HELD_REF = ROOT / "computations/unaudited-codex-n8-x5-rep2-group16-closed-t-modular-held-referee-2026-08-26"

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def replay(manifest):
    count = 0
    for line in manifest.read_text().splitlines():
        digest, name = line.split(None, 1)
        path = Path(name.strip())
        path = path if path.is_absolute() else (manifest.parent / path).resolve()
        assert path.is_file() and sha(path) == digest, (path, digest)
        count += 1
    return count

assert sha(RUN / "MANIFEST.sha256") == "eefb9e1045f63f945fa62cc83119f171128575eb29d5a1d41b1aabf2e6a374c2"
assert sha(RUN / "TERMINAL_MANIFEST.sha256") == "31d3c4290de2214fed4846909e0a1309a3adf103ea9415bea35a391e0a87999b"
assert replay(RUN / "MANIFEST.sha256") == 19
assert replay(RUN / "TERMINAL_MANIFEST.sha256") == 4
assert sha(HELD_REF / "results_referee.json") == "4dd60da1340a3fbd86ec03cc691c3917fc451a4b196a22b907350a739cb01361"
assert sha(HELD_REF / "MANIFEST.sha256") == "d8f36615a10cc254a91fa6c555ebc764736747e1b69d33d66cc96ff222f32ef0"
replay(HELD_REF / "MANIFEST.sha256")
assert sha(RUN / "rep2_group016_62_Vt0_Vt1_Vt2_p32003.sing") == "d7e57a3d43fb1280381660be2fea9c966eb086bd2aced3189b0f599030f5822b"
assert sha(RUN / "run_one_lane.py") == "a617b032eae5ecdb3cf41660f43fb900891e86240a97ffe4f25417d56a2de624"

attempt = json.loads((RUN / "ATTEMPT.json").read_text())
assert attempt["status"] == "ATTEMPT_CONSUMED" and attempt["relaunch_forbidden_even_if_no_result"]
assert attempt["prelaunch_census"]["match_count"] == 0
assert attempt["prelaunch_census"]["unobservable_pids"] == 0
result = json.loads((RUN / "result.json").read_text())
assert result["status"] == "UNIT_IDEAL_MODULAR_DIAGNOSTIC"
assert result["diagnostic_only"] and not result["mathematical_coverage"] and result["attempt_consumed"]
assert result["field"] == "F_32003"
assert result["chart"] == "V(A67,A12,t0,t1,t2) intersect D(b0)"
assert result["variables"] == 62 and result["generators"] == 6568
assert result["termination"] is None and result["returncode"] == 0 and result["stderr"] == ""
assert result["wall_seconds"] < 240 and result["peak_group_rss_bytes"] < 8 * 1024**3
assert result["stdout"].splitlines()[-6:] == [
    "INPUT_VARIABLES=62", "INPUT_GENERATORS=6568", "GROEBNER_SIZE=1",
    "UNIT_REMAINDER=0", "STATUS=UNIT_IDEAL", "Auf Wiedersehen.",
]
assert not result["exact_Q_launched"] and not result["other_chart_launched"]
assert not result["prior_timeout_reused"] and not result["automatic_relaunch"]
assert not list(RUN.rglob("*.tmp")) and len(list(RUN.glob("result.json"))) == 1

out = {
    "schema": "KRENN_X5_REP2_GROUP16_CLOSED_T_MODULAR_TERMINAL_REFEREE_V1",
    "status": "PASS_UNIT_IDEAL_MODULAR_DIAGNOSTIC_CHART_ONLY",
    "field": "F_32003",
    "chart": result["chart"],
    "variables": 62,
    "generators": 6568,
    "groebner_basis_size": 1,
    "unit_remainder": 0,
    "wall_seconds": result["wall_seconds"],
    "peak_rss_bytes": result["peak_group_rss_bytes"],
    "result_sha256": sha(RUN / "result.json"),
    "terminal_manifest_sha256": sha(RUN / "TERMINAL_MANIFEST.sha256"),
    "held_referee_result_sha256": sha(HELD_REF / "results_referee.json"),
    "held_referee_manifest_sha256": sha(HELD_REF / "MANIFEST.sha256"),
    "modular_chart_diagnostic_pass": True,
    "mathematical_coverage_promoted": False,
    "group16_closed": False,
    "exact_Q_launched": False,
    "other_chart_launched": False,
    "automatic_relaunch": False,
    "attempt_consumed": True,
    "resource_clear": True,
    "rep2_closed_union": list(range(16)),
    "rep2_closed_count": 16,
    "rep2_closed": False,
    "conjecture_closed": False,
}
(HERE / "results_referee.json").write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
print(json.dumps({"status": out["status"], "audit_sha256": sha(HERE / "results_referee.json")}, sort_keys=True))
