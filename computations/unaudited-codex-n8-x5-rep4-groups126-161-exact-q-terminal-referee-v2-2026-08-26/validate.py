#!/usr/bin/env python3
import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


result = json.loads((HERE / "results_referee.json").read_text())
assert result["status"] == "PASS_ALL_36_EXACT_Q_UNIT_IDEALS"
assert result["groups_closed"] == list(range(126, 162))
assert result["closed_union_after_batch"] == list(range(162))
manifest = HERE / "FINAL_MANIFEST.sha256"
count = 0
if manifest.exists():
    for line in manifest.read_text().splitlines():
        digest, name = line.split(None, 1)
        path = (HERE / name.strip()).resolve()
        assert re.fullmatch(r"[0-9a-f]{64}", digest)
        assert path.is_file() and sha(path) == digest
        count += 1
print(json.dumps({"status": "PASS_REP4_FINAL36_TERMINAL_REFEREE_VALIDATED", "manifest_lines": count}, sort_keys=True))
