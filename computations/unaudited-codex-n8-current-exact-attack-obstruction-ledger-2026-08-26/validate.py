#!/usr/bin/env python3
"""Replay the sealed metadata ledger without invoking any algebra solver."""

import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_ledger import HERE, hostile_tests, make_ledger, validate_ledger


def require(condition, detail):
    if not condition:
        raise ValueError(detail)


def digest(data):
    return hashlib.sha256((json.dumps(data, sort_keys=True, separators=(",", ":")) + "\n").encode()).hexdigest()


def main():
    recorded = json.loads((HERE / "results_attack_obstruction_ledger.json").read_text())
    expected = make_ledger()
    validate_ledger(recorded)
    require(recorded == expected, "recorded ledger differs from builder")
    hostiles = hostile_tests(recorded)
    recorded_hostiles = json.loads((HERE / "results_hostiles.json").read_text())
    require(recorded_hostiles["status"] == "PASS", "hostile status")
    require(recorded_hostiles["cases"] == hostiles, "hostile ledger mismatch")
    print(json.dumps({
        "status": "PASS_EXACT_METADATA_LEDGER_REPLAY",
        "ledger_sha256": hashlib.sha256((HERE / "results_attack_obstruction_ledger.json").read_bytes()).hexdigest(),
        "logical_sha256": digest(recorded),
        "nodes": len(recorded["logical_nodes"]),
        "pins": len(recorded["evidence_pins"]),
        "hostiles": len(hostiles),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
