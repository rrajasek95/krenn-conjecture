#!/usr/bin/env python3
"""Read-only referee for the rep5 guard-pivot k0 modular held package."""
import ast, hashlib, json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
HELD = ROOT / "computations/unaudited-codex-n8-x5-rep5-guard-pivot-k0-modular-held-2026-08-25"
DES = ROOT / "computations/unaudited-codex-n8-x5-rep5-post-timeout-guard-pivot-quotient-design-2026-08-25"
REF = ROOT / "computations/unaudited-codex-n8-x5-rep5-post-timeout-guard-pivot-quotient-design-referee-2026-08-25"

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()

pins = {
    HELD / "MANIFEST.sha256": "e5d31332126ecbe9ca2af75d8c8a1af9a4cc9bc1ef2518b266356496e60bfff1",
    HELD / "rep5_p00_guardpivot_k0_p32003.sing": "dc04c72252144d1a8ff798f49aa1130b1742fff342f21eaf02146b889e3370c1",
    HELD / "run_one_lane.py": "fdaaea4fead4ec7d47f0a513fa6b8c74a04e4821d1abb4751d32806f9cabc965",
    HELD / "held_pilot.json": "ae076bb94c7b20c7cb745114070d6b0185ecf857f0d77b1f8171227ac5686bbe",
    HELD / "refusal_contract.json": "2ef436cec0e81265c4d80d6e2b4150951e3ae4dfa7771bb95ccc7d665b585419",
    DES / "MANIFEST.sha256": "00ac8c2a1bea2b958644b0e6b1851d26535c83cc715d92b28335157b219da3f9",
    DES / "rep5_p00_guardpivot_k0_Q.sing": "d4204428cab5f3b5dd4ac321dd1ae04ce9b79c8f1197b8e1e863c6c186cc74f1",
    REF / "FINAL_MANIFEST.sha256": "af4bee0ca8db5391aac9f59cb1e52051d32e66fdb2974a126468b054ca3f5a4b",
    REF / "HELD_DIAGNOSTIC_PLAN.json": "acf0923735e96633389f8df6a74a0a35c3700fd9fd77ee28e1deffd1d8bac796",
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

manifest_counts = {"held": replay(HELD / "MANIFEST.sha256", HELD), "design": replay(DES / "MANIFEST.sha256", DES), "referee": replay(REF / "FINAL_MANIFEST.sha256", REF)}
q_source = (DES / "rep5_p00_guardpivot_k0_Q.sing").read_bytes()
mod_source_path = HELD / "rep5_p00_guardpivot_k0_p32003.sing"
mod_source = mod_source_path.read_bytes()
assert q_source.count(b"ring r=0,") == 1 and b"ring r=32003," not in q_source
assert mod_source == q_source.replace(b"ring r=0,", b"ring r=32003,")
assert sha(mod_source_path) == pins[mod_source_path]
text = mod_source.decode()
assert text.count("ring r=32003,(") == text.count("ideal G=slimgb(I);") == text.count("poly remainder=reduce(1,G);") == text.count("quit;") == 1
ring_line = next(line for line in text.splitlines() if line.startswith("ring r="))
variables = ring_line.split(",(", 1)[1].rsplit("),dp;", 1)[0].split(",")
body = text.split("ideal I=", 1)[1].split(';\nprint("INPUT_VARIABLES=', 1)[0]
depth = 0; generators = 1
for char in body:
    if char == "(": depth += 1
    elif char == ")": depth -= 1; assert depth >= 0
    elif char == "," and depth == 0: generators += 1
assert depth == 0 and len(variables) == len(set(variables)) == 88 and generators == 6574

held = json.loads((HELD / "held_pilot.json").read_text())
refusal = json.loads((HELD / "refusal_contract.json").read_text())
plan = json.loads((REF / "HELD_DIAGNOSTIC_PLAN.json").read_text())
assert held["status"] == "HELD_ZERO_RUN_PENDING_INDEPENDENT_ACCEPTANCE_AND_FRESH_CLEARANCE"
assert held["pins"]["design_referee_manifest_sha256"] == pins[REF / "FINAL_MANIFEST.sha256"]
assert held["pins"]["held_plan_sha256"] == pins[REF / "HELD_DIAGNOSTIC_PLAN.json"]
assert held["source"]["derivation"] == "replace sole literal ring r=0, by ring r=32003,; no other byte change"
assert held["lane"] == {"chart": "p00/guard-pivot/k0", "field": 32003, "generators": 6574, "maximum_lane_count": 1, "representative": "rep5", "variables": 88}
assert held["limits"] == {"maximum_clearance_lifetime_seconds": 600, "native_wall_seconds": 240, "rss_cap_bytes": 8589934592, "wrapper_wall_seconds": 250}
assert held["scope"] == {"attempt_marker_created": False, "automatic_relaunch_authorized": False, "exact_Q_authorized": False, "launched": False, "mathematical_coverage": False, "modular_lanes_authorized": 0, "other_k_authorized": False, "solver_runs": 0}
assert refusal["status"] == "ARMED_HELD_ZERO_RUN_SINGLE_USE"
assert refusal["forbidden"] == {"exact_Q": True, "other_k": True, "parallel": True, "relaunch": True}
assert plan["status"] == "HELD_DESIGN_ONLY_ZERO_RUN" and plan["first_and_only_chart"] == "pivot_k=0"
assert plan["prospective_source_sha256"] == pins[mod_source_path]

runner_path = HELD / "run_one_lane.py"; runner = runner_path.read_text(); ast.parse(runner)
tokens = (
    "proc_listallpids", "proc_pidpath", "proc_listpgrppids", "proc_pid_rusage",
    "return [buffer[index] for index in range(count)", "fresh_process_census()",
    "rusage observation failure for live group member", "process_group_rss_bytes",
    "NATIVE_WALL = 240", "WRAPPER_WALL = 250", "RSS_CAP = 8 * 1024**3",
    'f"{WRAPPER_WALL}s"', "MAX_CLEARANCE_LIFETIME_SECONDS = 600",
    "issued <= now < expires", 'clearance["no_overlap_confirmed"] is True',
    'clearance["other_k_authorized"] is False', 'clearance["exact_Q_authorized"] is False',
    'exclusive_json(HERE / "ATTEMPT.json"', 'atomic_json(HERE / "result.json"',
    '"exact_Q_launched": False', '"other_k_launched": False', '"automatic_relaunch": False',
)
for token in tokens: assert token in runner, token
assert "returned // ctypes.sizeof" not in runner and "second_lane" not in runner and "ALL_EQUAL_Y" not in runner
assert runner.index('exclusive_json(HERE / "ATTEMPT.json"') < runner.index("subprocess.Popen(")
assert runner.count("subprocess.Popen(") == 1

for schema_name in ("independent_referee_acceptance.schema.json", "launch_clearance.schema.json"):
    schema = json.loads((HELD / schema_name).read_text())
    assert schema["additionalProperties"] is False and set(schema["required"]) == set(schema["properties"])
acceptance = json.loads((HERE / "independent_referee_acceptance.json").read_text())
schema = json.loads((HELD / "independent_referee_acceptance.schema.json").read_text())
assert set(acceptance) == set(schema["required"])
for key, value in acceptance.items():
    if "const" in schema["properties"][key]: assert value == schema["properties"][key]["const"]
for absent in ("independent_referee_acceptance.json", "launch_clearance.json", "ATTEMPT.json", "result.json", "result.json.tmp", "stdout.log", "stderr.log", "watchdog.json"):
    assert not (HELD / absent).exists(), absent
assert not any(HELD.glob("*.tmp"))

print(json.dumps({
    "status": "PASS_APPROVED_HELD_REP5_GUARD_PIVOT_K0_MODULAR_ZERO_RUNS",
    "source_Q_sha256": sha(DES / "rep5_p00_guardpivot_k0_Q.sing"), "source_modular_sha256": sha(mod_source_path),
    "runner_sha256": sha(runner_path), "variables": 88, "generators": 6574,
    "acceptance_sha256": sha(HERE / "independent_referee_acceptance.json"), "manifest_counts": manifest_counts,
    "scope": {"solver_runs": 0, "mathematical_coverage": False, "exact_Q": False, "other_k": False, "relaunch": False},
}, sort_keys=True))
