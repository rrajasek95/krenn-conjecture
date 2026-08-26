#!/usr/bin/env python3
"""Static seal for the held group15 runner. Never invokes launch mode."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
PLAN = ROOT / "computations/unaudited-codex-n8-x5-rep1-group15-direct-libproc-held-plan-2026-08-25/HELD_GROUP15_PLAN.json"
REFEREE = ROOT / "computations/unaudited-codex-n8-x5-rep1-group15-direct-libproc-held-plan-referee-2026-08-25/FINAL_MANIFEST.sha256"
SOURCE = HERE / "rep1_group15_Q.sing"
RUNNER = HERE / "run_group15_direct_libproc.py"
CORE = HERE / "HELD_RUNNER_MANIFEST.sha256"
SCHEMA = HERE / "FRESH_CLEARANCE.schema.json"
OUT = HERE / "results_held.json"
EXPECTED = {
    PLAN: "e778f68f78c087a2d63f4491e0d67d9920302dc55cd2d39e80abc380f66c6ce4",
    REFEREE: "b1714d0a1d689ebae04017bf6ccb5120861996160cc4a37892542e3592e36761",
    SOURCE: "1611c16c73323e7a85ee730ba055f9f2092873841698e8fcc4f5799571ccab04",
    RUNNER: "c539f6f47e824a536271a3e4700a5d2b86408c39c0850602e37db14bbad748d4",
    SCHEMA: "dee7cc8a9810af83b6ec212109a2fd5e1ceefac6a3a502b19859701d142bc5fa",
}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replay(path):
    count = 0
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        digest, rel = line.split(None, 1)
        assert sha(ROOT / rel.strip()) == digest, rel
        count += 1
    return count


def top_level_count(body):
    depth = 0
    count = 1 if body.strip() else 0
    for char in body:
        if char == "(": depth += 1
        elif char == ")":
            depth -= 1
            assert depth >= 0
        elif char == "," and depth == 0: count += 1
    assert depth == 0
    return count


for path, digest in EXPECTED.items():
    assert sha(path) == digest, (path, sha(path), digest)
core_entries = replay(CORE)
source = SOURCE.read_text()
assert SOURCE.stat().st_size == 1841468
ring_start = source.index("ring r=0,(") + len("ring r=0,(")
ring_end = source.index("),dp;", ring_start)
variables = [value.strip() for value in source[ring_start:ring_end].split(",")]
assert len(variables) == len(set(variables)) == 91
ideal_start = source.index("ideal I=(") + len("ideal I=")
ideal_end = source.index(";\nprint(\"INPUT_GENERATORS=", ideal_start)
assert top_level_count(source[ideal_start:ideal_end]) == 6577
for token in ("ideal G=slimgb(I);", "poly remainder=reduce(1,G);", "STATUS=UNIT_IDEAL", "STATUS=NONUNIT_OR_UNRESOLVED"):
    assert source.count(token) == 1

runner = RUNNER.read_text()
assert "/bin/ps" not in runner and "subprocess.run" not in runner and "os.system" not in runner
for token in ("proc_listpids", "proc_pidpath", "PROC_PIDTASKINFO", "subprocess.Popen", "start_new_session=True"):
    assert token in runner
assert runner.count("process = subprocess.Popen") == 1
assert 'NATIVE_WALL = 240' in runner and 'WRAPPER_WALL = 250' in runner
assert 'RSS_LIMIT_KIB = 8 * 1024 * 1024' in runner
assert 'ATTEMPT.mkdir()' in runner
assert runner.index("census = fresh_process_census()") < runner.index("atomic_bytes(attempt_source, SOURCE.read_bytes())") < runner.index("process = subprocess.Popen")
assert runner.count('automatic_relaunch": False') >= 2
assert runner.count('second_lane": False') >= 2
schema = json.loads(SCHEMA.read_text())
assert schema["$id"] == "KRENN_X5_REP1_GROUP15_FRESH_CLEARANCE_V1"
assert schema["additionalProperties"] is False
assert schema["properties"]["group_id"]["const"] == 15
assert schema["properties"]["plan_sha256"]["const"] == EXPECTED[PLAN]
assert schema["properties"]["independent_manifest_sha256"]["const"] == EXPECTED[REFEREE]
assert not (HERE / "FRESH_CLEARANCE.json").exists()
assert not (HERE / "attempt_group15").exists()
assert not list(HERE.glob("*.tmp"))

result = {
    "schema": "KRENN_X5_REP1_GROUP15_HELD_RUNNER_SEAL_V1",
    "status": "PASS_MATERIALIZED_SEALED_NOT_LAUNCHED",
    "plan_sha256": EXPECTED[PLAN],
    "independent_manifest_sha256": EXPECTED[REFEREE],
    "held_runner_manifest_sha256": sha(CORE),
    "held_runner_manifest_entries": core_entries,
    "source_sha256": EXPECTED[SOURCE],
    "source_bytes": SOURCE.stat().st_size,
    "variables": len(variables),
    "generators": 6577,
    "runner_sha256": EXPECTED[RUNNER],
    "no_external_process_listing": True,
    "direct_libproc_census_and_process_group_rss": True,
    "limits": {"lanes": 1, "native_wall_seconds": 240, "wrapper_wall_seconds": 250, "rss_limit_bytes": 8589934592},
    "atomic_refuse_overwrite_stop_no_relaunch": True,
    "fresh_clearance_schema_sha256": EXPECTED[SCHEMA],
    "fresh_clearance_present": False,
    "attempt_directory_present": False,
    "process_launched": False,
}
OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(json.dumps({"status": result["status"], "result_sha256": sha(OUT), "held_runner_manifest_sha256": sha(CORE)}, sort_keys=True))
