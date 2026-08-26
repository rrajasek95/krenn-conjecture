#!/usr/bin/env python3
"""Read-only independent referee for the rep4 modular held package."""
from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PRODUCER = ROOT / "computations/unaudited-codex-n8-x5-rep4-all-equal-y-modular-held-2026-08-25"
DESIGN = ROOT / "computations/unaudited-codex-n8-x5-rep4-guard-minor-contraction-design-2026-08-25"
PRIOR = ROOT / "computations/unaudited-codex-n8-x5-rep4-guard-minor-contraction-referee-2026-08-25"
Q_SOURCE = DESIGN / "rep4_guard_minor_tiny_y_Q.sing"
SOURCE = PRODUCER / "rep4_all_equal_y_i0_p00_x0_y0_d01_p32003.sing"
RUNNER = PRODUCER / "run_one_lane.py"

PINS = {
    PRODUCER / "MANIFEST.sha256": "2fcbd08ee016c979d30540e83f0d01d1c9efcfcc625884d0957b423fdcf7c4a2",
    PRODUCER / "held_pilot.json": "7d8c497e3cbc76d1ef72285b3efade9346b2df1f3b03a3340ec97ca3d1dc992c",
    SOURCE: "9471d6bbfb0af012c313cafa97e12f5b3cea380e6cefb0c8f355cb53def80524",
    RUNNER: "1a0bee89d2f15cfaa82ad25110dc005952deb0bbbf696530e8e435a328065e7f",
    Q_SOURCE: "d46cdf77b9edafbc17a92ec851badba2db63640ec7324e024a83e29da04e121b",
    PRIOR / "FINAL_MANIFEST.sha256": "185b51b8107d5dcf12e7194a7d806157e0df6a2b6d047cf4adc6c8ac400fa4ae",
    PRIOR / "ONE_CHART_MODULAR_HELD_PLAN.json": "ee484b5a58d63cef6ed60c81760a790b06be363426678f50031f9891fb149203",
    PRIOR / "results_referee.json": "279565e76618b8fa8c4eb08f513f8109a018d23ed1e9fe11acb0489dd82bb863",
}


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def replay(path: Path, base: Path) -> int:
    count = 0
    for line in path.read_text().splitlines():
        if not line.strip(): continue
        digest, raw = line.split(None, 1)
        target = Path(raw.strip())
        if not target.is_absolute():
            target = (ROOT / target) if raw.strip().startswith("computations/") else (base / target)
        assert target.is_file() and sha(target) == digest, target
        count += 1
    return count


def top_level_count(body: str) -> int:
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


for path, expected in PINS.items():
    assert sha(path) == expected, (path, sha(path), expected)
producer_entries = replay(PRODUCER / "MANIFEST.sha256", PRODUCER)
prior_entries = replay(PRIOR / "FINAL_MANIFEST.sha256", PRIOR)

q_program = Q_SOURCE.read_text()
assert q_program.count("ring r=0,") == 1 and "ring r=32003," not in q_program
assert q_program.count("quit;") == 1 and "slimgb" not in q_program and "reduce(1" not in q_program
epilogue = "\n".join([
    "ideal G=slimgb(I);", 'print("GROEBNER_SIZE="+string(size(G)));',
    "poly remainder=reduce(1,G);", 'print("UNIT_REMAINDER="+string(remainder));',
    'if (remainder==0) { print("STATUS=UNIT_IDEAL"); } else { print("STATUS=NONUNIT_OR_UNRESOLVED"); }',
    "quit;",
])
derived = q_program.replace("ring r=0,", "ring r=32003,", 1).replace("quit;", epilogue, 1)
assert SOURCE.read_text() == derived and SOURCE.stat().st_size == 1764288
source = SOURCE.read_text()
ring_start = source.index("ring r=32003,(") + len("ring r=32003,(")
ring_end = source.index("),dp;", ring_start)
variables = [item.strip() for item in source[ring_start:ring_end].split(",")]
assert len(variables) == len(set(variables)) == 91
ideal_start = source.index("ideal I=") + len("ideal I=")
ideal_end = source.index(';\nprint("INPUT_VARIABLES=', ideal_start)
assert top_level_count(source[ideal_start:ideal_end]) == 6577
for token in ("ideal G=slimgb(I);", "poly remainder=reduce(1,G);", "STATUS=UNIT_IDEAL", "STATUS=NONUNIT_OR_UNRESOLVED", "quit;"):
    assert source.count(token) == 1

runner = RUNNER.read_text()
ast.parse(runner)
for token in (
    'ctypes.CDLL("/usr/lib/libproc.dylib")', "proc_listpgrppids",
    "process_group_rss_bytes(process.pid)", "start_new_session=True", "os.killpg",
    "NATIVE_WALL = 180", "WRAPPER_WALL = 195", "RSS_CAP = 8 * 1024**3",
    'acceptance_path = HERE / "independent_referee_acceptance.json"',
    'clearance_path = HERE / "launch_clearance.json"',
    'atomic_json(HERE / "result.json", result)', '"cross_representative_equivalence_used": False',
):
    assert token in runner, token
assert runner.count("subprocess.Popen(") == 1
assert runner.index("held_manifest_sha, acceptance_sha, clearance_sha") < runner.index("process = subprocess.Popen")

clearance = json.loads((PRODUCER / "launch_clearance.schema.json").read_text())
assert clearance["additionalProperties"] is False
assert set(clearance["required"]) == set(clearance["properties"])
assert clearance["properties"]["independent_referee_acceptance_sha256"] == {"const": PINS[PRIOR / "ONE_CHART_MODULAR_HELD_PLAN.json"]}
assert clearance["properties"]["independent_referee_final_manifest_sha256"] == {"const": PINS[PRIOR / "FINAL_MANIFEST.sha256"]}
assert clearance["properties"]["runner_sha256"] == {"const": PINS[RUNNER]}
assert clearance["properties"]["native_wall_seconds"] == {"const": 180}
assert clearance["properties"]["wrapper_wall_seconds"] == {"const": 195}
assert clearance["properties"]["rss_cap_bytes"] == {"const": 8589934592}
refusal = json.loads((PRODUCER / "refusal_contract.json").read_text())
assert refusal["status"] == "ARMED_ZERO_LAUNCH" and refusal["result_present_at_seal"] is False
assert refusal["forbidden"] == {
    "automatic_relaunch": True, "cross_representative_equivalence": True,
    "exact_Q": True, "second_lane": True,
}
held = json.loads((PRODUCER / "held_pilot.json").read_text())
assert held["scope"]["ideal_runs"] == 0 and held["scope"]["launched"] is False
assert held["scope"]["exact_Q_authorized"] is held["scope"]["second_lane_authorized"] is False
assert held["scope"]["automatic_relaunch_authorized"] is False
assert held["scope"]["cross_representative_equivalence_used"] is False
for name in ("independent_referee_acceptance.json", "launch_clearance.json", "result.json", "result.json.tmp"):
    assert not (PRODUCER / name).exists()
assert not list(PRODUCER.glob("*.tmp")) and not list(PRODUCER.glob("attempt*"))

print(json.dumps({
    "status": "PASS_APPROVED_HELD_ZERO_RUNS_REQUIRES_FRESH_MANAGER_CLEARANCE",
    "source_sha256": sha(SOURCE), "runner_sha256": sha(RUNNER),
    "variables": len(variables), "generators": 6577,
    "producer_manifest_entries": producer_entries, "prior_manifest_entries": prior_entries,
    "solver_runs": 0,
}, sort_keys=True))
