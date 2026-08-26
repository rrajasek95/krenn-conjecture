#!/usr/bin/env python3
import hashlib
import json
import os
from pathlib import Path

here = Path(__file__).resolve().parent
root = here.parents[1]
run = root / "computations/unaudited-codex-n8-x5-rep2-group16-Dt1-global-unit-gauge-exact-q-run-2026-08-26"
manifest = run / "TERMINAL_MANIFEST.sha256"
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
assert sha(manifest) == "d3d7fc425252358e1383a6d13af318d3a007e0e8510f9b6f3a63b775b26970c8"
count = 0
for line in manifest.read_text().splitlines():
    digest, name = line.split(None, 1)
    target = run / name.strip()
    assert target.is_file() and sha(target) == digest
    count += 1
assert count == 11
assert sha(run / "result.json") == "61ecab8e1361d263d3122ea0638298f75b712b2e9b1375a246baeaffcd3b338d"
r = json.loads((run / "result.json").read_text())
assert r["status"] == "UNIT_IDEAL_EXACT_Q" and r["mathematical_coverage"] is True
assert r["variables"] == 61 and r["generators"] == 6568
assert r["returncode"] == 0 and r["termination"] is None
assert r["source_sha256"] == "686ceb9529ba9487fe093845c770c237371c8866a54be5aeba6629f7ba640537"
assert r["runner_sha256"] == "fe4cda541cfdc4fa8017815cfbbed52e6c36323adbb5978deec18a86ba0af66d"
assert r["wall_seconds"] < r["native_wall_cap_seconds"] == 480
assert r["peak_group_rss_bytes"] < r["rss_cap_bytes"] == 8589934592
assert all(token in r["stdout"] for token in ("INPUT_VARIABLES=61", "INPUT_GENERATORS=6568", "GROEBNER_SIZE=1", "UNIT_REMAINDER=0", "STATUS=UNIT_IDEAL"))
assert r["other_chart_launched"] is r["automatic_relaunch"] is False
attempt = json.loads((run / "ATTEMPT.json").read_text())
assert attempt["status"] == "ATTEMPT_CONSUMED" and attempt["automatic_relaunch"] is False
output = {
    "schema": "KRENN_X5_REP2_GROUP16_DT1_GLOBAL_UNIT_GAUGE_EXACT_Q_TERMINAL_REFEREE_V1",
    "status": "PASS_UNIT_IDEAL_EXACT_Q_DT1_SUBCHART_ONLY",
    "producer_result_sha256": sha(run / "result.json"),
    "producer_terminal_manifest_sha256": sha(manifest),
    "manifest_entries": count,
    "variables": 61,
    "generators": 6568,
    "wall_seconds": r["wall_seconds"],
    "peak_group_rss_bytes": r["peak_group_rss_bytes"],
    "unit_remainder": 0,
    "groebner_basis_size": 1,
    "resource_clear": True,
    "chart_closed": True,
    "group16_closed": False,
    "rep2_closed": False,
    "automatic_relaunch": False,
}
tmp = here / "results_referee.json.tmp"
tmp.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
os.replace(tmp, here / "results_referee.json")
print(json.dumps({"status": output["status"], "resource_clear": True}, sort_keys=True))
