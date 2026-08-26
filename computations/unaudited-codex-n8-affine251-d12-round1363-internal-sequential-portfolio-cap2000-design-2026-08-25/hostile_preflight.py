#!/usr/bin/env python3
"""Small static hostiles proving the future-input launch interlock and frozen geometry."""
import ast
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
schedule = json.loads((HERE / "SCHEDULE.json").read_text())
assert schedule["status"] == "PREPARED_HELD_FOR_ROUND1362_FINAL_REPLAY_CLEAR"
assert not (HERE / "FUTURE_INPUT_PINS.json").exists()
texts = {}
for name in ("freeze_future_input.py", "run_gate.py", "validate.py"):
    texts[name] = (HERE / name).read_text()
    ast.parse(texts[name], filename=name)
assert 'AUDIT_RESULT_REL = "WAIT_FOR_ROUND1362_AUDIT_RESULT"' in texts["freeze_future_input.py"]
assert 'assert pins_path.exists(), "launch interlock: round1362 FINAL_REPLAY_CLEAR pins absent"' in texts["run_gate.py"]
assert 'command("portfolio", "auto", "best", 1750000, 520, 1)' in texts["run_gate.py"]
assert 'command("cap2000_candidate", "rare", "cold", 2000000, 120, 256)' in texts["run_gate.py"]
assert 'winner == ("cold", "rare")' in texts["validate.py"]
parent = (HERE.parents[1] / schedule["engine"]["production_parent_source"]).read_text()
audit_source = (HERE.parents[1] / schedule["engine"]["source"]).read_text()
removed_guard = '''    if config.elimination != "hierarchical"
        || config.strategy != "cold"
        || config.pivot != "rare"
        || config.workers != 16
        || config.incremental
    {
        fail("v4 rare-order index requires fixed cold/rare/16 hierarchical nonincremental mode");
    }
'''
assert parent.count(removed_guard) == 1 and audit_source == parent.replace(removed_guard, "", 1)
assert 'fail("hierarchical elimination requires explicit --workers 16 --pivot rare --strategy cold --incremental no")' in audit_source
sha256 = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
assert sha256(HERE.parents[1] / schedule["engine"]["source"]) == schedule["engine"]["source_sha256"]
assert sha256(HERE.parents[1] / schedule["engine"]["binary"]) == schedule["engine"]["binary_sha256"]
value = {
    "schema": "KRENN_AFFINE251_D12_ROUND1363_PRELAUNCH_HOSTILES_V1",
    "status": "PASS_PREPARED_HELD_FAIL_CLOSED",
    "future_input_pins_absent": True,
    "unresolved_placeholders_block_before_any_read": True,
    "runner_blocks_before_any_clone": True,
    "scripts_parse": True,
    "portfolio_geometry_frozen": True,
    "cap2000_is_cold_rare_conditional": True,
    "audit_source_exact_single_guard_deletion": True,
    "parser_hierarchical_guard_retained": True,
    "large_reads_or_clones": False,
    "solves": False
}
(HERE / "hostile_preflight_results.json").write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
print(json.dumps(value, sort_keys=True))
