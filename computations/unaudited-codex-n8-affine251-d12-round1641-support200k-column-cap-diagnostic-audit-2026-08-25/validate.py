#!/usr/bin/env python3
import json
from pathlib import Path

d = json.loads((Path(__file__).parent / "results_independent_diagnostic_audit.json").read_text())
assert d["status"] == "PASS_ZERO_COVERAGE_COLUMN_CAP_UNCHANGED_R1640"
assert d["independent_large_rehash"] == {"checkpoint_equal": True, "vector_cache_equal": True}
assert d["result"]["rounds_completed"] == 1640 and d["result"]["round_records"] == []
assert d["guard_referee"]["support_guard_reached"] is False
assert d["guard_referee"]["new_columns_lower_bound"] == 180290
assert d["guard_referee"]["exact_next_columns_known"] is False
assert d["filesystem"]["temporary_files"] == 0
assert d["classification"]["accepted_r1641_coverage"] == 0
assert d["classification"]["may_resume"] is False
print("PASS independent r1641 COLUMN_CAP diagnostic audit")
