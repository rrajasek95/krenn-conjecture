#!/usr/bin/env python3
"""Read-only static replay of the held base81 p32003 pilot package."""
from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
CANONICAL = ROOT / "computations/unaudited-codex-n8-x5-anchor-no-rectangle-design-2026-08-25/canonical_reduced_full_x5_Q.sing"
PLAN = ROOT / "computations/unaudited-codex-n8-x5-anchor-no-rectangle-design-referee-2026-08-25/HELD_PILOT_PLAN.json"
DESIGN_RESULT = ROOT / "computations/unaudited-codex-n8-x5-anchor-no-rectangle-design-referee-2026-08-25/results_referee.json"
DESIGN_MANIFEST = ROOT / "computations/unaudited-codex-n8-x5-anchor-no-rectangle-design-referee-2026-08-25/MANIFEST.sha256"
SOURCE = HERE / "base81_p32003.sing"
EPILOGUE = HERE / "SOLVER_EPILOGUE.sing"
RUNNER = HERE / "run_pilot.py"
SCHEMA = HERE / "FRESH_CLEARANCE.schema.json"
REFUSAL_SCHEMA = HERE / "REFUSAL_SCHEMA.json"
RECORD = HERE / "HELD_LAUNCH_RECORD.json"
RESULT = HERE / "results_held.json"
MANIFEST = HERE / "MANIFEST.sha256"

EXPECTED = {
    CANONICAL: "25b25aac93a336c36c0299c5d6ee9b2a984b5ca0e644170ef235af92f01124f3",
    PLAN: "8c4c30693c21f01ded35272bfb154a1e312e085481a09c8a16c395d32a380d84",
    DESIGN_RESULT: "13c5f2b7ba1e3568a44cdad98924c65485f23e6eb0b9389e953ded594fe67c3c",
    DESIGN_MANIFEST: "e31c069a86041cd95d2d8e844a811032a2593ece33ad18a7a8ec12c58fff6074",
    SOURCE: "80495d946b3e3078a7538b4762e9151b612533cc2b1445269a1e24f30d3e5dc7",
    EPILOGUE: "4e89c111ad7d0f708bce7296a0d209507dede12b4a2ccfce78be184ccc790500",
    RUNNER: "90b276285e87741b18f990eb94c4694379601fc1e6a65a4c6f186a2a6726ad8a",
    SCHEMA: "824733740e0abbbb79ae0c493e8ec48eb9625f039b8011d7b8569216af1857ee",
    REFUSAL_SCHEMA: "ce2dce467d878b2d4da9430d689e1aea291ba646c99011beae7bb5b72687ed26",
}


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


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


def replay_manifest() -> int:
    count = 0
    for line in MANIFEST.read_text().splitlines():
        if not line.strip():
            continue
        digest, relative = line.split(None, 1)
        path = HERE / relative.strip()
        assert path.is_file() and sha(path) == digest, relative
        count += 1
    return count


for path, expected in EXPECTED.items():
    assert sha(path) == expected, (path, sha(path), expected)
assert SOURCE.stat().st_size == 420125
canonical = CANONICAL.read_text()
assert canonical.count("ring r=0,") == 1 and canonical.endswith("quit;\n")
derived = canonical.replace("ring r=0,", "ring r=32003,", 1)[:-len("quit;\n")] + EPILOGUE.read_text()
assert SOURCE.read_text() == derived
source = SOURCE.read_text()
ring_start = source.index("ring r=32003,(") + len("ring r=32003,(")
ring_end = source.index("),dp;", ring_start)
variables = [item.strip() for item in source[ring_start:ring_end].split(",")]
assert len(variables) == len(set(variables)) == 81
ideal_start = source.index("ideal I=") + len("ideal I=")
ideal_end = source.index(';\nprint("INPUT_VARIABLES=', ideal_start)
assert top_level_count(source[ideal_start:ideal_end]) == 6561
for token in ("ideal G=slimgb(I);", "poly remainder=reduce(1,G);", "STATUS=UNIT_IDEAL", "STATUS=NONUNIT_OR_UNRESOLVED"):
    assert source.count(token) == 1

ast.parse(RUNNER.read_text())
runner = RUNNER.read_text()
assert "/bin/ps" not in runner and "subprocess.run" not in runner and "os.system" not in runner
for token in ("proc_listpids", "proc_pidpath", "PROC_PIDTASKINFO", "subprocess.Popen", "start_new_session=True"):
    assert token in runner
assert runner.count("process = subprocess.Popen") == 1
assert "NATIVE_WALL = 180" in runner and "WRAPPER_WALL = 190" in runner
assert "RSS_LIMIT_KIB = 8 * 1024 * 1024" in runner
assert runner.index("census = fresh_process_census()") < runner.index("ATTEMPT.mkdir()") < runner.index("process = subprocess.Popen")
assert runner.count('"automatic_relaunch": False') >= 2
assert runner.count('"second_lane": False') >= 2

schema = json.loads(SCHEMA.read_text())
assert schema["$id"] == "KRENN_X5_ANCHOR_BASE81_P32003_FRESH_CLEARANCE_V1"
assert schema["additionalProperties"] is False
assert schema["properties"]["held_plan_sha256"]["const"] == EXPECTED[PLAN]
refusal = json.loads(REFUSAL_SCHEMA.read_text())
assert refusal["$id"] == "KRENN_X5_ANCHOR_BASE81_P32003_REFUSAL_V1"
assert refusal["additionalProperties"] is False
assert len(refusal["properties"]["reason"]["enum"]) == 8
record = json.loads(RECORD.read_text())
result = json.loads(RESULT.read_text())
assert record["status"] == "READY_HELD_ZERO_RUNS_REQUIRES_INDEPENDENT_AUDIT_AND_MANAGER_CLEARANCE"
assert record["runner"]["sha256"] == EXPECTED[RUNNER]
assert record["source"]["sha256"] == EXPECTED[SOURCE]
assert result["status"] == "PASS_READY_HELD_ZERO_RUNS" and result["solver_runs"] == 0
assert not (HERE / "FRESH_CLEARANCE.json").exists()
assert not (HERE / "attempt_p32003").exists()
assert not (HERE / "refusal.json").exists()
assert not list(HERE.glob("*.tmp"))
assert not list(HERE.glob("stdout*")) and not list(HERE.glob("stderr*")) and not list(HERE.glob("watchdog*"))
manifest_entries = replay_manifest()
print(json.dumps({
    "status": "PASS_READY_HELD_ZERO_RUNS",
    "manifest_entries": manifest_entries,
    "source_sha256": sha(SOURCE),
    "runner_sha256": sha(RUNNER),
    "result_sha256": sha(RESULT),
}, sort_keys=True))
