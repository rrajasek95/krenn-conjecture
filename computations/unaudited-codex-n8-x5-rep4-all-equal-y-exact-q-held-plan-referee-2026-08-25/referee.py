#!/usr/bin/env python3
"""Independent held-plan referee for the rep4 same-chart exact-Q lane."""
import ast, hashlib, json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
HELD = ROOT / "computations/unaudited-codex-n8-x5-rep4-all-equal-y-exact-q-held-plan-2026-08-25"
DES = ROOT / "computations/unaudited-codex-n8-x5-rep4-guard-minor-contraction-design-2026-08-25"
SREF = ROOT / "computations/unaudited-codex-n8-x5-rep4-guard-minor-contraction-referee-2026-08-25"
REJECT = ROOT / "computations/unaudited-codex-n8-x5-rep4-all-equal-y-modular-terminal-second-referee-2026-08-25"
MOD = ROOT / "computations/unaudited-codex-n8-x5-rep4-all-equal-y-modular-v2-terminal-referee-2026-08-25"
EPI = ROOT / "computations/unaudited-codex-n8-x5-anchor-no-rectangle-base81-p32003-held-pilot-2026-08-25/SOLVER_EPILOGUE.sing"

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()

pins = {
    HELD / "MANIFEST.sha256": "7b93ce7bee8ac3d8bad0384490ee511a819e9c4b1d800b776dc8016897a30d20",
    HELD / "HELD_EXACT_Q_PLAN.json": "ed0a6b95a9cf6e228e22eb588c41de9f6b8140560e4eed853489375526dd31a0",
    HELD / "rep4_all_equal_y_exact_Q.sing": "c90c69b11ca931677bc1de138bdfc8c1eb7618d5aee20744764e4a4b1b511019",
    HELD / "run_exact_q.py": "1892065935daf8ad47530fee138f48ed4a5d6a772320018f6e9d94cfddab894a",
    DES / "rep4_guard_minor_tiny_y_Q.sing": "d46cdf77b9edafbc17a92ec851badba2db63640ec7324e024a83e29da04e121b",
    SREF / "FINAL_MANIFEST.sha256": "185b51b8107d5dcf12e7194a7d806157e0df6a2b6d047cf4adc6c8ac400fa4ae",
    REJECT / "FINAL_MANIFEST.sha256": "b965154ba8acdd16c39dd074bc983a4d0e20ae13e24ff528ea1f16697ed0a074",
    MOD / "FINAL_MANIFEST.sha256": "fb2a0ab3d036269b34476bf0a8c0f9d6871f7dd312c25efe2691fa1dbbea3cf0",
    MOD / "results_referee.json": "981b6dd37a26f2ebb3b1645aafbe89a0f5837273cbb20fe578cf57b2b860e9ce",
    EPI: "4e89c111ad7d0f708bce7296a0d209507dede12b4a2ccfce78be184ccc790500",
}
for path, expected in pins.items(): assert sha(path) == expected, (path, sha(path), expected)

def replay(path, base):
    count = 0
    for line in path.read_text().splitlines():
        if not line.strip(): continue
        expected, raw = line.split(None, 1); target = Path(raw.strip())
        if not target.is_absolute(): target = ROOT / target if raw.strip().startswith("computations/") else base / target
        assert target.is_file() and sha(target) == expected, target
        count += 1
    return count

manifest_entries = replay(HELD / "MANIFEST.sha256", HELD)
canonical = (DES / "rep4_guard_minor_tiny_y_Q.sing").read_text()
epilogue = EPI.read_text()
assert canonical.count("ring r=0,") == canonical.count("quit;\n") == 1 and "slimgb(I)" not in canonical
expected_source = canonical.replace("quit;\n", epilogue, 1)
source_path = HELD / "rep4_all_equal_y_exact_Q.sing"
source = source_path.read_text()
assert source == expected_source and sha(source_path) == pins[source_path]
assert source.count("ring r=0,") == 1 and "ring r=32003," not in source
assert source.count("ideal G=slimgb(I);") == source.count("poly remainder=reduce(1,G);") == 1
ring_line = next(line for line in source.splitlines() if line.startswith("ring r="))
variables = ring_line.split(",(", 1)[1].rsplit("),dp;", 1)[0].split(",")
body = source.split("ideal I=", 1)[1].split(';\nprint("INPUT_VARIABLES=', 1)[0]
depth = 0; generators = 1
for char in body:
    if char == "(": depth += 1
    elif char == ")": depth -= 1; assert depth >= 0
    elif char == "," and depth == 0: generators += 1
assert depth == 0 and len(variables) == len(set(variables)) == 91 and generators == 6577

plan = json.loads((HELD / "HELD_EXACT_Q_PLAN.json").read_text())
held_result = json.loads((HELD / "results_held.json").read_text())
modular = json.loads((MOD / "results_referee.json").read_text())
assert plan["status"] == "HELD_ZERO_RUNS_REQUIRES_INDEPENDENT_PLAN_AUDIT_AND_MANAGER_RESOURCE_CLEARANCE"
assert plan["source"]["canonical_Q_sha256"] == pins[DES / "rep4_guard_minor_tiny_y_Q.sing"]
assert plan["source"]["execution_Q_sha256"] == pins[source_path]
assert (plan["source"]["variables"], plan["source"]["generators"]) == (91, 6577)
assert plan["lane"] == {"field": "Q", "maximum_lanes": 1, "native_wall_seconds": 480, "wrapper_wall_seconds": 510, "rss_cap_bytes": 8589934592, "fresh_libproc_census": True, "process_group_rss": True, "atomic_outputs": True, "refuse_overwrite": True}
assert plan["terminal_rule"] == "stop and seal after any outcome"
assert plan["automatic_relaunch"] is plan["second_lane"] is plan["modular_relaunch"] is False
assert plan["solver_launches"] == 0 and plan["clearance_present"] is plan["attempt_present"] is False
assert held_result["status"] == "READY_HELD_ZERO_RUNS_PENDING_INDEPENDENT_PLAN_AUDIT" and held_result["execution"]["solver_runs"] == 0
assert all(held_result["hostile_tests"].values())
assert modular["status"] == "PASS_ONE_MODULAR_UNIT_DIAGNOSTIC_ONLY"

runner_path = HELD / "run_exact_q.py"; runner = runner_path.read_text(); ast.parse(runner)
tokens = (
    "proc_listallpids", "proc_pidpath", "proc_listpgrppids", "proc_pid_rusage",
    "return [buffer[index] for index in range(count)",
    "rusage observation failure for live group member", "fresh_process_census()",
    "NATIVE_WALL = 480", "WRAPPER_WALL = 510", "RSS_CAP = 8 * 1024**3",
    'f"{WRAPPER_WALL}s"', "start_new_session=True", "MAX_CLEARANCE_LIFETIME_SECONDS = 600",
    "issued <= now < expires", 'clearance["no_overlap_confirmed"] is True',
    'exclusive_json(HERE / "ATTEMPT.json"', 'atomic_json(HERE / "result.json"',
    '"second_lane_launched": False', '"automatic_relaunch": False',
)
for token in tokens: assert token in runner, token
assert "returned // ctypes.sizeof" not in runner
assert runner.index('exclusive_json(HERE / "ATTEMPT.json"') < runner.index("subprocess.Popen(")
assert runner.count("subprocess.Popen(") == 1
# Narrow non-load-bearing caveat: the source hash proves 91/6577 and remainder
# zero proves the unit ideal, but terminal audit must enforce every advertised line.
assert '"STATUS=UNIT_IDEAL" in stdout and "UNIT_REMAINDER=0" in stdout' in runner
assert '"GROEBNER_SIZE=1" in stdout' not in runner

clearance_schema = json.loads((HELD / "launch_clearance.schema.json").read_text())
assert clearance_schema["additionalProperties"] is False and set(clearance_schema["required"]) == set(clearance_schema["properties"])
acceptance = json.loads((HERE / "independent_referee_acceptance.json").read_text())
expected_acceptance = {
    "schema": "KRENN_X5_REP4_ALL_EQUAL_Y_EXACT_Q_INDEPENDENT_ACCEPTANCE_V1",
    "status": "PASS_APPROVE_ONE_HARDENED_EXACT_Q_SAME_CHART_ONLY",
    "held_manifest_sha256": pins[HELD / "MANIFEST.sha256"],
    "source_sha256": pins[source_path], "runner_sha256": pins[runner_path],
    "source_referee_manifest_sha256": pins[SREF / "FINAL_MANIFEST.sha256"],
    "rejection_manifest_sha256": pins[REJECT / "FINAL_MANIFEST.sha256"],
    "singular_sha256": "9436b32ff7565719240230de8a6fb1d27af5e65f0ca4c9c5b756a77e82409b88",
    "gtimeout_sha256": "1e26c50fa8c439fe1f4e6c6edd106e95030e16582c1c8c32e73d8a889cdf5b95",
    "variables": 91, "generators": 6577, "maximum_lane_count": 1,
    "exact_Q_authorized": True, "second_lane_authorized": False, "automatic_relaunch_authorized": False,
}
assert acceptance == expected_acceptance
for absent in ("independent_referee_acceptance.json", "launch_clearance.json", "ATTEMPT.json", "result.json", "result.json.tmp", "stdout.log", "stderr.log", "watchdog.json"):
    assert not (HELD / absent).exists(), absent
assert not any(HELD.glob("*.tmp"))

print(json.dumps({
    "status": "PASS_APPROVED_HELD_REP4_EXACT_Q_ZERO_RUNS_WITH_TERMINAL_TRANSCRIPT_REFEREE_REQUIRED",
    "source_sha256": sha(source_path), "runner_sha256": sha(runner_path),
    "variables": 91, "generators": 6577, "manifest_entries": manifest_entries,
    "acceptance_sha256": sha(HERE / "independent_referee_acceptance.json"),
    "scope": {"solver_runs": 0, "mathematical_coverage": False, "second_lane": False, "relaunch": False},
}, sort_keys=True))
