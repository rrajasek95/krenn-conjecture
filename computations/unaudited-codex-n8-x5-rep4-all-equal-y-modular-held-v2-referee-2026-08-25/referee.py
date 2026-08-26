#!/usr/bin/env python3
"""Read-only referee for the wholly fresh rep4 hardened-v2 held lane."""
import hashlib, json, re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
HELD = ROOT / "computations/unaudited-codex-n8-x5-rep4-all-equal-y-modular-held-v2-2026-08-25"
DESIGN = ROOT / "computations/unaudited-codex-n8-x5-rep4-guard-minor-contraction-design-2026-08-25"
FAIL = ROOT / "computations/unaudited-codex-n8-x5-rep4-all-equal-y-modular-terminal-second-referee-2026-08-25"
SEM = ROOT / "computations/unaudited-codex-n8-x5-rep5-all-equal-y-modular-held-v2-referee-2026-08-25"

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

pins = {
    HELD / "MANIFEST.sha256": "27fe22cd124f15d85373db13cbbbed9ca0bb55e23b326247ba695689681012d0",
    HELD / "rep4_all_equal_y_i0_p00_x0_y0_d01_p32003.sing": "9471d6bbfb0af012c313cafa97e12f5b3cea380e6cefb0c8f355cb53def80524",
    HELD / "run_one_lane.py": "975cb4baa7ca06fb1471fdd883a75ba2e27d61983a5ff5669676a0835242f2f0",
    HELD / "held_pilot.json": "74f6b85bdc97927e51341d48264aa383e5444a3577241f8bbf5362a46d1eb97b",
    DESIGN / "rep4_guard_minor_tiny_y_Q.sing": "d46cdf77b9edafbc17a92ec851badba2db63640ec7324e024a83e29da04e121b",
    FAIL / "FINAL_MANIFEST.sha256": "b965154ba8acdd16c39dd074bc983a4d0e20ae13e24ff528ea1f16697ed0a074",
    FAIL / "results_referee.json": "9b43ae57ea42a4f281b2d3d758ee72817e38170a744171966486595f2591e89c",
    SEM / "FINAL_MANIFEST.sha256": "de9477718cef401aace156f2614b31cf576d761dd5d2b53a4f6c994f5d375771",
    SEM / "results_referee.json": "59089b5781ed0ef9a117f465e855f4da116ad60b52396ca08e620f1354e4ed4a",
}
for path, expected in pins.items():
    assert sha(path) == expected, (path, sha(path), expected)

def replay_manifest(path, base):
    count = 0
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        expected, raw = line.split(None, 1)
        target = Path(raw.strip())
        if not target.is_absolute():
            target = ROOT / target if raw.strip().startswith("computations/") else base / target
        assert target.is_file() and sha(target) == expected, target
        count += 1
    return count

held_entries = replay_manifest(HELD / "MANIFEST.sha256", HELD)
rejection_entries = replay_manifest(FAIL / "FINAL_MANIFEST.sha256", FAIL)
semantics_entries = replay_manifest(SEM / "FINAL_MANIFEST.sha256", SEM)

source = (HELD / "rep4_all_equal_y_i0_p00_x0_y0_d01_p32003.sing").read_text()
q_source = (DESIGN / "rep4_guard_minor_tiny_y_Q.sing").read_text()
epilogue = "\n".join([
    "ideal G=slimgb(I);",
    'print("GROEBNER_SIZE="+string(size(G)));',
    "poly remainder=reduce(1,G);",
    'print("UNIT_REMAINDER="+string(remainder));',
    'if (remainder==0) { print("STATUS=UNIT_IDEAL"); } else { print("STATUS=NONUNIT_OR_UNRESOLVED"); }',
    "quit;",
])
expected_source = q_source.replace("ring r=0,", "ring r=32003,", 1).replace("quit;", epilogue, 1)
assert q_source.count("ring r=0,") == q_source.count("quit;") == 1 and "slimgb" not in q_source
assert source == expected_source
ring_line = next(line for line in source.splitlines() if line.startswith("ring r="))
variables = len(ring_line.split(",(", 1)[1].rsplit("),dp;", 1)[0].split(","))
ideal_body = source.split("ideal I=", 1)[1].split(';\nprint("INPUT_VARIABLES=', 1)[0]
depth = 0
generators = 1
for char in ideal_body:
    if char == "(": depth += 1
    elif char == ")": depth -= 1
    elif char == "," and depth == 0: generators += 1
assert depth == 0 and (variables, generators) == (91, 6577)

held = json.loads((HELD / "held_pilot.json").read_text())
failure = json.loads((FAIL / "results_referee.json").read_text())
semantics = json.loads((SEM / "results_referee.json").read_text())
assert held["status"] == "HELD_FRESH_ZERO_RUN_PENDING_INDEPENDENT_AUDIT"
assert held["source"]["freshly_derived_from_Q"] is True and held["source"]["old_local_source_reused"] is False
assert held["supersession"]["old_clearance_result_attempt_reused"] is False
assert held["supersession"]["old_lane_remains_consumed"] is True
assert failure["status"] == "PASS_ZERO_PROOF_COVERAGE_EXACT_TRANSCRIPT_RESOURCE_OBSERVER_FAILED"
assert failure["accepted_mathematical_coverage"] is False
assert semantics["status"] == "PASS_APPROVED_HELD_ALL_SIX_DEFECTS_FIXED_ZERO_RUNS"
assert len(semantics["defects_fixed"]) == 6

runner = (HELD / "run_one_lane.py").read_text()
compile(runner, str(HELD / "run_one_lane.py"), "exec")
required_runner_tokens = (
    "proc_listallpids", "proc_pidpath", "proc_listpgrppids",
    "return [buffer[index] for index in range(count)",
    "rusage observation failure for live group member",
    "fresh_process_census()", 'f"{WRAPPER_WALL}s"',
    "MAX_CLEARANCE_LIFETIME_SECONDS = 600", "issued <= now < expires",
    'clearance["no_overlap_confirmed"] is True',
    'exclusive_json(HERE / "ATTEMPT.json"',
    'assert not (HERE / stale).exists()', 'assert not any(HERE.glob("*.tmp"))',
    '"automatic_relaunch": False', '"rep2_equivalence_used": False',
)
for token in required_runner_tokens:
    assert token in runner, token
assert "returned // ctypes.sizeof" not in runner
assert runner.index('exclusive_json(HERE / "ATTEMPT.json"') < runner.index("subprocess.Popen(")
assert re.search(r"NATIVE_WALL = 180\nWRAPPER_WALL = 195\nRSS_CAP = 8 \* 1024\*\*3", runner)

acceptance_schema = json.loads((HELD / "independent_referee_acceptance.schema.json").read_text())
clearance_schema = json.loads((HELD / "launch_clearance.schema.json").read_text())
for schema in (acceptance_schema, clearance_schema):
    assert schema["additionalProperties"] is False
    assert set(schema["required"]) == set(schema["properties"])
assert clearance_schema["properties"]["nonce"]["pattern"] == "^[0-9a-f]{32}$"
assert clearance_schema["properties"]["expected_census_match_count"]["const"] == 0
assert clearance_schema["properties"]["no_overlap_confirmed"]["const"] is True
assert clearance_schema["properties"]["manager_clearance_confirmed"]["const"] is True
assert clearance_schema["properties"]["resource_clearance_confirmed"]["const"] is True

for absent in (
    "independent_referee_acceptance.json", "launch_clearance.json", "ATTEMPT.json",
    "result.json", "result.json.tmp", "stdout.log", "stderr.log", "watchdog.json",
):
    assert not (HELD / absent).exists(), absent
assert not any(HELD.glob("*.tmp"))

print(json.dumps({
    "status": "PASS_APPROVED_HELD_FRESH_REP4_V2_ZERO_RUNS",
    "source_sha256": sha(HELD / "rep4_all_equal_y_i0_p00_x0_y0_d01_p32003.sing"),
    "runner_sha256": sha(HELD / "run_one_lane.py"),
    "variables": variables, "generators": generators,
    "held_manifest_entries": held_entries,
    "rejection_manifest_entries": rejection_entries,
    "accepted_semantics_manifest_entries": semantics_entries,
    "solver_runs": 0, "mathematical_coverage": False,
}, sort_keys=True))
