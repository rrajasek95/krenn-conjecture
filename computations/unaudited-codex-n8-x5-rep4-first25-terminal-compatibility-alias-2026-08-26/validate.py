#!/usr/bin/env python3
import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


result = json.loads((HERE / "compatibility_result.json").read_text())
assert result["status"] == "PASS_ALIAS_EXACT_GROUPS_1_25_UNIT"
assert result["groups_closed"] == list(range(1, 26))
assert result["closed_union"] == list(range(26))
assert result["mathematical_claim_changed"] is False
manifest = HERE / "FINAL_MANIFEST.sha256"
checked = 0
if manifest.exists():
    for line in manifest.read_text().splitlines():
        digest, name = line.split(None, 1)
        path = (HERE / name.strip()).resolve()
        assert re.fullmatch(r"[0-9a-f]{64}", digest)
        assert path.is_file() and sha(path) == digest
        checked += 1
print(json.dumps({"status": "PASS_FIRST25_ALIAS_VALIDATED", "manifest_lines": checked}, sort_keys=True))
