#!/usr/bin/env python3
from __future__ import annotations

import ast
import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


pins = json.loads((HERE / "v2_pins.json").read_text())
for name, key in (
    ("future_dependencies.json", "future_dependencies_sha256"),
    ("dependency_verifier.py", "dependency_verifier_sha256"),
    ("run_groups126_161.py", "runner_sha256"),
    ("source_ledger.json", "source_ledger_sha256"),
    ("normalize_dependencies.py", "normalizer_sha256"),
):
    assert sha(HERE / name) == pins[key], (name, sha(HERE / name), pins[key])

future = json.loads((HERE / "future_dependencies.json").read_text())
first = future["dependencies"][0]
assert first["result_schema"] == "KRENN_X5_REP4_FIRST25_TERMINAL_COMPATIBILITY_ALIAS_V1"
assert first["result_status"] == "PASS_ALIAS_EXACT_GROUPS_1_25_UNIT"
assert first["groups_closed"] == list(range(1, 26))
assert future["dependencies"][1]["groups_closed"] == list(range(26, 76))
assert future["dependencies"][2]["groups_closed"] == list(range(76, 126))

normalized_path = HERE / "normalized_dependencies.json"
assert normalized_path.is_file()
normalized = json.loads(normalized_path.read_text())
assert normalized["status"] == "PASS_NORMALIZED_EXACT_CLOSED_UNION_0_125"
assert normalized["closed_union"] == list(range(126))
from dependency_verifier import verify_payload

replay = verify_payload(future, normalized, ROOT)
assert replay["status"] == "PASS_REPLAYED_ALL_SIX_DEPENDENCY_ARTIFACTS_EXACT_UNION_0_125"

ledger = json.loads((HERE / "source_ledger.json").read_text())
assert [lane["group_id"] for lane in ledger["lanes"]] == list(range(126, 162))
assert len(ledger["lanes"]) == 36
for lane in ledger["lanes"]:
    source = HERE / lane["source_path"]
    assert source.is_file() and sha(source) == lane["source_sha256"]
    assert source.stat().st_size == lane["source_bytes"]
    assert lane["variables"] == 91 and lane["generators"] == 6577

runner = (HERE / "run_groups126_161.py").read_text()
ast.parse(runner)
assert runner.count("subprocess.Popen(") == 1
assert runner.index("verify_payload(") < runner.index("exclusive(HERE/'BATCH_ATTEMPT.json'") < runner.index("subprocess.Popen(")
assert "SELECTED=tuple(range(126,162))" in runner
assert "NATIVE_WALL=240;WRAPPER_WALL=250;RSS_CAP=8*1024**3" in runner

manifest = HERE / "MANIFEST.sha256"
checked = 0
if manifest.exists():
    for line in manifest.read_text().splitlines():
        digest, name = line.split(None, 1)
        path = (HERE / name.strip()).resolve()
        assert re.fullmatch(r"[0-9a-f]{64}", digest)
        assert path.is_file() and sha(path) == digest
        checked += 1
print(json.dumps({"status": "PASS_REP4_FINAL36_V2_VALIDATED", "sources": 36, "manifest_lines": checked}, sort_keys=True))
