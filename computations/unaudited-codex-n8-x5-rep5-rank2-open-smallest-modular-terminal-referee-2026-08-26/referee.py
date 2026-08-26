#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
RUN = ROOT / "computations/unaudited-codex-n8-x5-rep5-rank2-open-smallest-modular-held-2026-08-26"
REF = ROOT / "computations/unaudited-codex-n8-x5-rep5-rank2-open-smallest-modular-held-referee-2026-08-26"
COND = ROOT / "computations/unaudited-codex-n8-x5-rep5-rank2-open-same-stratum-exact-q-conditional-held-referee-2026-08-26"

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def replay(path, base):
    for line in path.read_text().splitlines():
        digest, name = line.split(None, 1)
        target = Path(name.strip())
        target = target if target.is_absolute() else (base / target).resolve()
        assert sha(target) == digest, (target, sha(target), digest)

assert sha(RUN / "MANIFEST.sha256") == "687dd47c10265ad82421cd06e015db4a88982710dbdba370ac0fee82f5f5596b"
assert sha(RUN / "TERMINAL_MANIFEST.sha256") == "aa18079a9f35fa858b52343a8f727282ccc8462ab5f801644c188a535533d851"
replay(RUN / "MANIFEST.sha256", RUN)
replay(RUN / "TERMINAL_MANIFEST.sha256", RUN)
assert sha(REF / "results_referee.json") == "9012ce33390a930126a64328d7f4b71dee118a27f1dafbd82e358158f7724697"
assert sha(REF / "independent_referee_acceptance.json") == "0aa77af998bab5c43aef0a791909c5a1198d0499f418cad76a476bdd860876cf"
assert sha(REF / "FINAL_MANIFEST.sha256") == "78ec2054761b8e6a6eeb3dc338f82338d02b48d25436a46b5cbcc37755d18a49"
replay(REF / "FINAL_MANIFEST.sha256", REF)
historical = json.loads((REF / "HELD_APPROVAL.json").read_text())
assert historical["referee_result_sha256"] == "9d0c26a6157d67728ddf600ed31b835082f80be934c1e44ddcde1082abe65e34"
conditional = json.loads((COND / "results_referee.json").read_text())
assert conditional["provenance"]["modular_referee_v1_historical_manifest_sha256"] == "1c33eea1ba807ef5502a1f3047844faaec05afe355858a3b041a0dd1584479f7"
assert conditional["provenance"]["modular_referee_v1_replayable_on_disk"] is False
assert conditional["provenance"]["modular_referee_v2_manifest_sha256"] == sha(REF / "FINAL_MANIFEST.sha256")
assert sha(RUN / "rep5_rank2_k2_t1_p32003.sing") == "fd182135d5da6eda87e284a4f38f147fbf13bef14016c1ee300bb9bde6713c5a"
assert sha(RUN / "run_one_lane.py") == "e459c779d54b93e58166b639ed29e0aa4e79b69b1366e65dc05b948381473ec7"
attempt = json.loads((RUN / "ATTEMPT.json").read_text())
assert attempt["status"] == "ATTEMPT_CONSUMED" and attempt["relaunch_forbidden_even_if_no_result"]
assert attempt["prelaunch_census"]["match_count"] == 0
assert attempt["prelaunch_census"]["unobservable_pids"] == 0
result = json.loads((RUN / "result.json").read_text())
assert result["status"] == "FAIL_CLOSED_RESOURCE_GATE"
assert result["termination"] == "NATIVE_WALL_CAP_300"
assert result["diagnostic_only"] and not result["mathematical_coverage"] and result["attempt_consumed"]
assert result["field"] == "F_32003" and result["pivot_k"] == 2 and result["t_open"] == 1
assert result["variables"] == 84 and result["generators"] == 6562
assert 300 <= result["wall_seconds"] < 315
assert result["peak_group_rss_bytes"] < 8589934592
assert result["stderr"] == ""
assert "INPUT_VARIABLES=84" in result["stdout"] and "INPUT_GENERATORS=6562" in result["stdout"]
assert "GROEBNER_SIZE=" not in result["stdout"]
assert "UNIT_REMAINDER=" not in result["stdout"] and "STATUS=" not in result["stdout"]
assert not result["exact_Q_launched"] and not result["other_stratum_launched"]
assert not result["prior_consumed_k0_reused"] and not result["automatic_relaunch"]
assert not list(RUN.rglob("*.tmp")) and len(list(RUN.glob("result.json"))) == 1

out = {
    "schema": "KRENN_X5_REP5_RANK2_OPEN_SMALLEST_MODULAR_TERMINAL_REFEREE_V1",
    "status": "PASS_FAIL_CLOSED_NATIVE_WALL_ZERO_COVERAGE",
    "field": "F_32003",
    "pivot_k": 2,
    "t_open": 1,
    "variables": 84,
    "generators": 6562,
    "termination": result["termination"],
    "wall_seconds": result["wall_seconds"],
    "peak_rss_bytes": result["peak_group_rss_bytes"],
    "result_sha256": sha(RUN / "result.json"),
    "terminal_manifest_sha256": sha(RUN / "TERMINAL_MANIFEST.sha256"),
    "held_referee_v1_result_sha256": historical["referee_result_sha256"],
    "held_referee_v1_manifest_sha256": conditional["provenance"]["modular_referee_v1_historical_manifest_sha256"],
    "held_referee_v1_replayable_on_disk": False,
    "held_referee_v2_result_sha256": sha(REF / "results_referee.json"),
    "held_referee_v2_approval_sha256": sha(REF / "independent_referee_acceptance.json"),
    "held_referee_v2_manifest_sha256": sha(REF / "FINAL_MANIFEST.sha256"),
    "mathematical_coverage": False,
    "exact_Q_launched": False,
    "other_stratum_launched": False,
    "automatic_relaunch": False,
    "attempt_consumed": True,
    "rep5_chart_closed": False,
    "seven_block_family_closed": False,
    "conjecture_closed": False,
    "post_terminal_process_census_match_count": 0,
    "resource_clear": True,
}
(HERE / "results_referee.json").write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
print(json.dumps({"status": out["status"], "audit_sha256": sha(HERE / "results_referee.json")}, sort_keys=True))
