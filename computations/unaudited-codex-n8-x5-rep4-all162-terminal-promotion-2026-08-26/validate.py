#!/usr/bin/env python3
import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


result = json.loads((HERE / "results_promotion.json").read_text())
assert result["status"] == "PASS_REP4_ALL_162_CANONICAL_972_RAW_CHARTS"
assert result["canonical_groups_closed"] == list(range(162))
assert result["canonical_group_count"] == 162 and result["raw_charts_closed"] == 972
assert result["rep4_closed"] is True and result["full_conjecture_closed"] is False
manifest = HERE / "FINAL_MANIFEST.sha256"
count = 0
if manifest.exists():
    for line in manifest.read_text().splitlines():
        digest, name = line.split(None, 1)
        path = (HERE / name.strip()).resolve()
        assert re.fullmatch(r"[0-9a-f]{64}", digest)
        assert path.is_file() and sha(path) == digest
        count += 1
print(json.dumps({"status": "PASS_REP4_ALL162_PROMOTION_VALIDATED", "manifest_lines": count}, sort_keys=True))
