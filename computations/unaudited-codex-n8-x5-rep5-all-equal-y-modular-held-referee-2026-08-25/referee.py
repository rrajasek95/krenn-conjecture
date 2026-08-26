#!/usr/bin/env python3
"""Read-only independent referee for the rep5 held modular package."""
from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
PRODUCER = ROOT / "computations/unaudited-codex-n8-x5-rep5-all-equal-y-modular-held-2026-08-25"
DESIGN = ROOT / "computations/unaudited-codex-n8-x5-rep5-guard-minor-contraction-design-2026-08-25"
PRIOR_REFEREE = ROOT / "computations/unaudited-codex-n8-x5-rep5-guard-minor-contraction-referee-2026-08-25"
SOURCE = PRODUCER / "rep5_all_equal_y_i0_p00_x0_y0_d01_p32003.sing"
ORIGINAL = DESIGN / "rep5_guard_minor_tiny_y_p32003.sing"
RUNNER = PRODUCER / "run_one_lane.py"
CLEARANCE = PRODUCER / "launch_clearance.schema.json"
REFUSAL = PRODUCER / "refusal_contract.json"

PINS = {
    PRODUCER / "MANIFEST.sha256": "dcacfb67e77a36a3eeab2caff442b22695cf62ebce49f231c8151a52439985bc",
    PRODUCER / "held_pilot.json": "3d55d3a7bf144df75fdec5f2331a0b748f330cf507bddd78874b4ba392248b90",
    SOURCE: "33716adb0c1e2e9064e8c68e8cd60df305fe88781153c195853dba8131838c97",
    RUNNER: "be9ead0b5229459ba00adc5e61b5aad91e0c306f3c71c82c0b8ac84a880b824c",
    ORIGINAL: "33716adb0c1e2e9064e8c68e8cd60df305fe88781153c195853dba8131838c97",
    PRIOR_REFEREE / "FINAL_MANIFEST.sha256": "ad86daeae93aaa154ef9ade124c719c8e683c3ae1b95130f948a2d90c0fc495a",
    PRIOR_REFEREE / "HELD_MODULAR_PILOT.json": "0df5f63b08cb3f601a5d77d22f07293e557f6dae6b7e727849916d943e5b70c7",
    PRIOR_REFEREE / "results_independent_referee.json": "451159d198b0188ee2780c7468797b6a438d04e041212e36a0cc2b1469b73292",
}


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def replay_manifest(path: Path, base: Path) -> int:
    count = 0
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        digest, raw = line.split(None, 1)
        target = Path(raw.strip())
        if not target.is_absolute():
            target = base / target
        assert target.is_file() and sha(target) == digest, target
        count += 1
    return count


def top_level_count(body: str) -> int:
    depth = 0
    count = 1 if body.strip() else 0
    for char in body:
        if char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            assert depth >= 0
        elif char == "," and depth == 0:
            count += 1
    assert depth == 0
    return count


for path, expected in PINS.items():
    assert sha(path) == expected, (path, sha(path), expected)
producer_manifest_entries = replay_manifest(PRODUCER / "MANIFEST.sha256", PRODUCER)
prior_manifest_entries = replay_manifest(PRIOR_REFEREE / "FINAL_MANIFEST.sha256", PRIOR_REFEREE)
assert SOURCE.read_bytes() == ORIGINAL.read_bytes()
assert SOURCE.stat().st_size == 1950700

source = SOURCE.read_text()
assert source.count("ring r=32003,(") == 1 and "ring r=0," not in source
ring_start = source.index("ring r=32003,(") + len("ring r=32003,(")
ring_end = source.index("),dp;", ring_start)
variables = [item.strip() for item in source[ring_start:ring_end].split(",")]
assert len(variables) == len(set(variables)) == 91
ideal_start = source.index("ideal I=") + len("ideal I=")
ideal_end = source.index(';\nprint("INPUT_VARIABLES=', ideal_start)
assert top_level_count(source[ideal_start:ideal_end]) == 6577
epilogue = (
    'print("INPUT_VARIABLES="+string(nvars(r)));\n'
    'print("INPUT_GENERATORS="+string(size(I)));\n'
    'ideal G=slimgb(I);\n'
    'print("GROEBNER_SIZE="+string(size(G)));\n'
    'poly remainder=reduce(1,G);\n'
    'print("UNIT_REMAINDER="+string(remainder));\n'
    'if (remainder==0) { print("STATUS=UNIT_IDEAL"); } else { print("STATUS=NONUNIT_OR_UNRESOLVED"); }\n'
    'quit;\n'
)
assert source.endswith(epilogue)
for token in ("ideal G=slimgb(I);", "poly remainder=reduce(1,G);", "STATUS=UNIT_IDEAL", "STATUS=NONUNIT_OR_UNRESOLVED", "quit;"):
    assert source.count(token) == 1, token

held = json.loads((PRODUCER / "held_pilot.json").read_text())
prior = json.loads((PRIOR_REFEREE / "results_independent_referee.json").read_text())
assert held["lane"] == {
    "chart": "all-equal-y/i0/p00/x0/y0/d01", "field": "F_32003",
    "generators": 6577, "maximum_lane_count": 1,
    "representative": "rep5", "variables": 91,
}
assert held["rep5_derivation"]["exact_source_byte_match"] is True
assert held["rep5_derivation"]["rep2_source_or_equivalence_used"] is False
assert prior["status"] == "PASS_INDEPENDENT_EXACT_DESIGN_NO_IDEAL_RUN"
assert prior["counts"]["new_variables"] == 91 and prior["counts"]["new_generators"] == 6577

runner = RUNNER.read_text()
ast.parse(runner)
assert runner.count("subprocess.Popen(") == 1
assert 'ctypes.CDLL("/usr/lib/libproc.dylib")' in runner
assert "NATIVE_WALL = 180" in runner and "WRAPPER_WALL = 195" in runner
assert "RSS_CAP = 8 * 1024**3" in runner
assert 'atomic_json(HERE / "result.json", result)' in runner and "os.replace(temporary, path)" in runner
assert '"exact_Q_launched": False' in runner and '"second_lane_launched": False' in runner
assert '"automatic_relaunch": False' in runner and '"rep2_equivalence_used": False' in runner

# These are deliberate negative assertions.  They identify why launch approval
# cannot be granted even though the held source and zero-run state are valid.
assert "proc_listpids" not in runner and "proc_pidpath" not in runner
assert "os.getpgid" not in runner
assert "return record.resident_size if" in runner and "else 0" in runner
assert "GTIMEOUT" in runner and "subprocess.Popen(\n    [str(SINGULAR), str(SOURCE)]" in runner
assert 'assert not (HERE / "result.json").exists()' in runner
assert 'assert not (HERE / "result.json.tmp").exists()' not in runner

clearance = json.loads(CLEARANCE.read_text())
assert clearance["additionalProperties"] is False
assert clearance["properties"]["native_wall_seconds"] == {"const": 180}
assert clearance["properties"]["wrapper_wall_seconds"] == {"const": 195}
assert clearance["properties"]["rss_cap_bytes"] == {"const": 8589934592}
assert clearance["properties"]["runner_sha256"] == {"const": PINS[RUNNER]}
for missing in ("nonce", "issued_unix_seconds", "expires_unix_seconds", "no_overlap_confirmed"):
    assert missing not in clearance["properties"]
refusal = json.loads(REFUSAL.read_text())
assert refusal["status"] == "ARMED_ZERO_LAUNCH"
assert refusal["result_present_at_seal"] is False

for forbidden in (
    "result.json", "result.json.tmp", "independent_referee_acceptance.json",
    "launch_clearance.json", "stdout.log", "stderr.log", "watchdog.json",
):
    assert not (PRODUCER / forbidden).exists(), forbidden
assert not list(PRODUCER.glob("*.tmp"))
assert not list(PRODUCER.glob("attempt*"))

print(json.dumps({
    "status": "REJECT_LAUNCH_APPROVAL_HELD_SOURCE_ZERO_RUNS_PASS",
    "producer_manifest_entries": producer_manifest_entries,
    "prior_referee_manifest_entries": prior_manifest_entries,
    "source_sha256": sha(SOURCE),
    "runner_sha256": sha(RUNNER),
    "variables": len(variables),
    "generators": 6577,
    "solver_runs": 0,
    "blocking_defects": 6,
}, sort_keys=True))
