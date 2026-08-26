#!/usr/bin/env python3
"""Independent fail-closed referee for the next-three pre-arithmetic failure."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
PROD = ROOT / "computations/unaudited-codex-n8-x5-rep1-next3-exact-q-batch-2026-08-25"
GROUP13_REF = ROOT / "computations/unaudited-codex-n8-x5-rep1-group13-exact-q-referee-2026-08-25"
OUT = HERE / "results_referee.json"
ADVICE = HERE / "DISTINCT_GROUP15_DIRECT_LIBPROC_ADVICE.json"

EXPECTED = {
    PROD / "MANIFEST.sha256": "e7d3e6bb528cf3614690aaf0b8f246975c87d9f6c8a681a8bc2f5c536037af32",
    PROD / "BATCH_FAILURE.json": "d6c039db2db4154be5b0ef4afaa78d81314666284e5b025ded604bac41aa85fb",
    PROD / "FAILURE_TRACE.txt": "84e7c2a10c41ffbd658f107e3e76e585b23d963db0b381ed65b9cea9b991d101",
    PROD / "LAUNCH_RECORD.json": "95e3b145c17e3afe065b921172428a60ac7b648f2fdb082168370d96f52df3b1",
    PROD / "run_next3.py": "348b43fcb372568a1ffda1a20bfcbe67dc4ae130d80b99f2fb7a947299966588",
    GROUP13_REF / "NEXT3_EXACT_Q_HELD_PLAN.json": "8549c4e52ef4f3e6e48997a14b7e0473d8c4fbdf3536be97d4278182f24d4224",
    GROUP13_REF / "FINAL_MANIFEST.sha256": "aa7e6ef6457d18b8020dc1ece2566b83155a4f6d44bb569242e56c345f60a16e",
}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replay_manifest(path):
    count = 0
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        digest, rel = line.split(None, 1)
        assert sha(path.parent / rel.strip()) == digest, (path, rel)
        count += 1
    return count


for path, digest in EXPECTED.items():
    assert sha(path) == digest, (path, sha(path), digest)
manifest_entries = replay_manifest(PROD / "MANIFEST.sha256")
failure = json.loads((PROD / "BATCH_FAILURE.json").read_text())
launch = json.loads((PROD / "LAUNCH_RECORD.json").read_text())
trace = (PROD / "FAILURE_TRACE.txt").read_text()
runner = (PROD / "run_next3.py").read_text()

assert failure["schema"] == "KRENN_X5_REP1_NEXT3_EXACT_Q_BATCH_FAILURE_V1"
assert failure["status"] == "STOPPED_FAIL_CLOSED_FRESH_PROCESS_CENSUS_EPERM_ZERO_COVERAGE"
assert failure["accepted_coverage"] == 0
assert failure["requested_groups"] == [15, 17, 25]
assert failure["launched_groups"] == failure["unit_groups"] == []
assert failure["failure"] == {
    "stage": "group15 fresh per-lane process/resource census",
    "operation": "/bin/ps -axo pid=,ppid=,rss=,etime=,command=",
    "exception": "PermissionError", "errno": 1, "message": "Operation not permitted",
    "runner_exit_code": 1, "singular_process_created": False,
    "group15_source_materialized": False, "group15_preflight_published": False,
    "batch_result_published": False,
}
assert failure["output_census"] == {
    "group15_directory_exists_empty": True, "group17_directory_absent": True,
    "group25_directory_absent": True, "singular_source_files": 0,
    "singular_result_files": 0, "watchdog_files": 0, "temporary_files": 0,
    "matching_heavy_processes_after_failure": 0,
}
assert failure["disposition"] == {
    "stop_rule_triggered": "process/census failure", "automatic_relaunch": False,
    "patched_relaunch": False, "further_groups_launched": False,
    "group_closure_claimed": False, "representative_1_closed": False,
    "next_action": "A new independently reviewed execution contract would be required; this cleared batch is terminal.",
}
assert launch["status"] == "CLEARED_PRELAUNCH"
assert launch["scope"] == "Sequential exact-Q groups 15,17,25 only; stop on first mismatch; no further groups or relaunch."
assert launch["stop_rule"].startswith("Stop immediately on first nonunit, timeout, RSS/process/census failure")

# Source-order proof: the only mutation before the failing census is mkdir.
mkdir_at = runner.index("lane_dir.mkdir()")
census_at = runner.index("census = fresh_census(group_id, lane_dir)", mkdir_at)
materialize_at = runner.index("program = minor.build_program", census_at)
singular_at = runner.index("process = subprocess.Popen", materialize_at)
assert mkdir_at < census_at < materialize_at < singular_at
assert '["/bin/ps", "-axo", "pid=,ppid=,rss=,etime=,command="]' in runner
assert "PermissionError" in trace and "Operation not permitted: '/bin/ps'" in trace

group15 = PROD / "group15"
assert group15.is_dir() and list(group15.iterdir()) == []
assert not (PROD / "group17").exists() and not (PROD / "group25").exists()
assert not (PROD / "BATCH_RESULT.json").exists()
assert not list(PROD.rglob("*.sing"))
assert not list(PROD.rglob("result.json"))
assert not list(PROD.rglob("watchdog.json"))
assert not list(PROD.rglob("*.log"))
assert not list(PROD.rglob("*.tmp"))

advice = json.loads(ADVICE.read_text())
assert advice["verdict"] == "LOGICALLY_PERMISSIBLE_ONLY_AS_WHOLELY_NEW_HELD_SINGLE_GROUP15_DESIGN"
assert advice["launch_authorized"] is False
assert advice["old_batch_disposition"] == "terminal; no patch, relaunch, or further group under manifest e7d3e6bb..."
assert advice["geometry_disposition"] == "not stopped: no arithmetic or geometric test occurred"
assert advice["required_contract"]["maximum_groups"] == [15]
assert advice["required_contract"]["process_census"] == "direct libproc only; no /bin/ps subprocess"
assert advice["required_contract"]["fresh_directory_no_attempt_reuse"] is True
assert advice["required_contract"]["automatic_relaunch"] is False

audit = {
    "schema": "KRENN_X5_REP1_NEXT3_ZERO_COVERAGE_FAILURE_REFEREE_V1",
    "status": "PASS_FAIL_CLOSED_ZERO_COVERAGE_OLD_PLAN_TERMINAL",
    "producer_manifest_sha256": EXPECTED[PROD / "MANIFEST.sha256"],
    "producer_failure_sha256": EXPECTED[PROD / "BATCH_FAILURE.json"],
    "manifest_entries_replayed": manifest_entries,
    "failure": "PermissionError EPERM from /bin/ps in the mandatory group15 fresh census",
    "accepted_coverage": 0,
    "group15_directory_empty": True,
    "group17_and_group25_absent": True,
    "source_result_log_watchdog_tmp_files": 0,
    "singular_process_created": False,
    "old_plan": {
        "terminal": True, "patch_forbidden": True, "relaunch_forbidden": True,
        "further_groups_forbidden": True,
    },
    "geometry": {
        "tested": False,
        "must_stop": False,
        "distinct_single_group15_contract_logically_permissible": True,
    },
    "distinct_group15_advice_sha256": sha(ADVICE),
}
OUT.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n")
print(json.dumps({"status": audit["status"], "result_sha256": sha(OUT)}, sort_keys=True))
