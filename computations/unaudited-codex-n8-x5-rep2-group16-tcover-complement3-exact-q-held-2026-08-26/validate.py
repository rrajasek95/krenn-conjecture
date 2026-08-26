#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


ledger = json.loads((HERE / "source_ledger.json").read_text())
assert ledger["status"] == "PASS_MATERIALIZED_THREE_COMPLEMENTARY_CHARTS_ZERO_RUNS"
assert ledger["partition"] == ["D(t1)", "V(t1) intersect D(t2)", "V(t1,t2) intersect D(t0)", "V(t0,t1,t2)"]
assert [lane["variables"] for lane in ledger["lanes"]] == [63, 64, 64]
assert all(lane["generators"] == 6569 for lane in ledger["lanes"])
for lane in ledger["lanes"]:
    source = HERE / lane["source_path"]
    assert source.is_file() and sha(source) == lane["source_sha256"]
    text = source.read_text()
    assert text.count("ideal G=slimgb(I);") == 1
    assert text.count("STATUS=UNIT_IDEAL") == 1
assert not any(HERE.glob("*ATTEMPT*")) and not (HERE / "results").exists()
print(json.dumps({"status": "PASS_TCOVER_COMPLEMENT3_HELD_VALIDATION", "solver_runs": 0}, sort_keys=True))
