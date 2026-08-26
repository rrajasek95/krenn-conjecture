#!/usr/bin/env python3
"""Independent terminal replay of rep2 group16 combined-smallest modular pilot."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
RUN = ROOT / "computations/unaudited-codex-n8-x5-rep2-group16-combined-smallest-modular-held-2026-08-26"
HELD_REF = ROOT / "computations/unaudited-codex-n8-x5-rep2-group16-combined-smallest-modular-held-referee-2026-08-26"

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

assert sha(RUN / "MANIFEST.sha256") == "6842f4f8c70570772d2b3602682b103af4953c2cec67b88510f2df72aeef8fa8"
assert sha(RUN / "TERMINAL_MANIFEST.sha256") == "c4b56c5ead3d38247890652d333a5be0904e52eee90be9954bacee7c0cd03fda"
assert replay(RUN / "MANIFEST.sha256") == 17
assert replay(RUN / "TERMINAL_MANIFEST.sha256") == 4
assert sha(HELD_REF / "results_referee.json") == "bcf47edd2433933354dfb9d72b37cca0904a0736dff9dac6445e0d2ea6ffe2e5"
assert sha(HELD_REF / "independent_referee_acceptance.json") == "0b35d8bedab32c06dd4da9dac5cc27710f8d7d2153abe1a8fb0f1b231994ce54"
assert sha(HELD_REF / "FINAL_MANIFEST.sha256") == "5fdfd65e2321c840af97849acd97cb462b4613ed619209fb4f8365e155774fb7"
replay(HELD_REF / "FINAL_MANIFEST.sha256")
assert sha(RUN / "rep2_group016_torus_zerozero_guardpivot_k0_p32003.sing") == "66bdb9277c9bff605e0d8a808ca65beb5967afaaf8ae494193286a60338355c6"
assert sha(RUN / "run_one_lane.py") == "cec7089a43ddb82dc5f9654b5338a0dcc21f30fe2ace5640b8421dd7ef6ce656"

attempt = json.loads((RUN / "ATTEMPT.json").read_text())
assert attempt["status"] == "ATTEMPT_CONSUMED" and attempt["relaunch_forbidden_even_if_no_result"]
assert attempt["prelaunch_census"]["match_count"] == 0
assert attempt["prelaunch_census"]["unobservable_pids"] == 0
result = json.loads((RUN / "result.json").read_text())
assert result["status"] == "FAIL_CLOSED_RESOURCE_GATE"
assert result["termination"] == "NATIVE_WALL_CAP_240"
assert result["diagnostic_only"] and not result["mathematical_coverage"] and result["attempt_consumed"]
assert result["field"] == "F_32003" and result["torus_stratum"] == "A67=A12=0"
assert result["guard_pivot_k"] == 0 and result["variables"] == 67 and result["generators"] == 6574
assert 240 <= result["wall_seconds"] < 255
assert result["peak_group_rss_bytes"] < 8 * 1024**3
assert result["stderr"] == ""
assert "INPUT_VARIABLES=67" in result["stdout"] and "INPUT_GENERATORS=6574" in result["stdout"]
assert "GROEBNER_SIZE=" not in result["stdout"]
assert "UNIT_REMAINDER=" not in result["stdout"] and "STATUS=" not in result["stdout"]
assert not result["exact_Q_launched"] and not result["other_chart_launched"]
assert not result["prior_timeout_reused"] and not result["automatic_relaunch"]
assert not list(RUN.rglob("*.tmp")) and len(list(RUN.glob("result.json"))) == 1

out = {
    "schema": "KRENN_X5_REP2_GROUP16_COMBINED_SMALLEST_MODULAR_TERMINAL_REFEREE_V1",
    "status": "PASS_FAIL_CLOSED_NATIVE_WALL_ZERO_COVERAGE",
    "field": "F_32003",
    "logical_chart": "V(A67,A12) intersect D(b0)",
    "torus_stratum": "A67=A12=0",
    "guard_pivot_k": 0,
    "variables": 67,
    "generators": 6574,
    "termination": result["termination"],
    "wall_seconds": result["wall_seconds"],
    "peak_rss_bytes": result["peak_group_rss_bytes"],
    "result_sha256": sha(RUN / "result.json"),
    "terminal_manifest_sha256": sha(RUN / "TERMINAL_MANIFEST.sha256"),
    "held_referee_result_sha256": sha(HELD_REF / "results_referee.json"),
    "held_referee_acceptance_sha256": sha(HELD_REF / "independent_referee_acceptance.json"),
    "held_referee_manifest_sha256": sha(HELD_REF / "FINAL_MANIFEST.sha256"),
    "mathematical_coverage": False,
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
