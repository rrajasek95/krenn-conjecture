#!/usr/bin/env python3
"""Freeze the only permitted differences for the widened portfolio retry."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
failure = json.loads((HERE / "portfolio_failed120/watchdog.json").read_text())
audit = json.loads((HERE / "FAILURE_AUDIT.json").read_text())
assert audit["status"] == "PASS_FAIL_CLOSED_NO_STATE_ACCEPTED"
assert failure["breach"] == "WALL_CAP" and failure["returncode"] == -15
assert failure["abort_final_output_absent"] and failure["result_sha256"] is None
assert failure["quarantined_abort_paths"] == []
assert not (HERE / "portfolio_failed120/result.json").exists()
command = failure["command"]


def argument(items, flag):
    assert items.count(flag) == 1
    return items[items.index(flag) + 1]


required = {
    "--workers": "16", "--pivot": "auto", "--strategy": "best",
    "--elimination": "tree", "--incremental": "no",
    "--portfolio-period": "1", "--portfolio-parallel": "yes",
    "--support-cap": "100000", "--column-cap": "1250000",
    "--round-cap": "1262", "--rss-gib": "36", "--wall-seconds": "110",
}
for flag, value in required.items():
    assert argument(command, flag) == value

source = (HERE / "run_retry_after_wallcap.py").read_text()
assert 'watched("portfolio_retry155", native("portfolio_retry155", "auto", "best", 1250000, 145), 155)' in source
assert 'watched("selected_control", native(' in source
assert 'native("cap1500_candidate", "rare", "cold", 1500000)' in source
assert 'assert not (HERE / "selected_control").exists()' in source

value = {
    "schema": "KRENN_AFFINE251_D12_ROUND1262_PORTFOLIO_RETRY_ACCEPTANCE_V1",
    "status": "PASS_RETRY_FROZEN_NOT_LAUNCHED",
    "preserved_failure": {
        "watchdog_sha256": audit["watchdog_sha256"],
        "result_absent": True,
        "input_clones_unchanged": True,
        "no_fixed_or_cap_run": True,
    },
    "retry_native_command_changes": {
        "output_directory": "portfolio_failed120 -> portfolio_retry155",
        "wall_seconds": "110 -> 145",
        "all_mathematical_and_strategy_arguments_identical": True,
    },
    "retry_wrapper_change": {"wall_seconds": "120 -> 155", "rss_gib": 36},
    "fixed_and_cap_geometry": {"native_wall_seconds": 110, "watchdog_wall_seconds": 120,
                               "rss_gib": 36},
    "production_mutated": False,
}
(HERE / "RETRY_ACCEPTANCE.json").write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
print(json.dumps(value, sort_keys=True))
