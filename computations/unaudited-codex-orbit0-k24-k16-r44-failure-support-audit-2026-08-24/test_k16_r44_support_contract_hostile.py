#!/usr/bin/env python3
"""Hostile candidate-ledger mutations for the support-aware contract."""

import copy
import csv
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("support_audit", HERE / "audit_k16_r44_failure_and_support.py")
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)

with audit.PINS["support_candidates"][0].open(newline="") as stream:
    reader = csv.DictReader(stream, delimiter="\t")
    GOOD = list(reader)


def reject(name, mutation):
    rows = copy.deepcopy(GOOD)
    mutation(rows)
    try:
        audit.validate_candidates(rows)
    except (RuntimeError, KeyError, TypeError, ValueError):
        return name
    raise RuntimeError("hostile candidate ledger accepted: " + name)


mutations = [
    ("duplicate_slot", lambda rows: rows[1].__setitem__("candidate_slot", "0")),
    ("duplicate_record", lambda rows: rows[1].__setitem__("record_index", rows[0]["record_index"])),
    ("wrong_support_bin", lambda rows: rows[0].__setitem__("support_bin", "36")),
    ("wrong_source_row", lambda rows: rows[0].__setitem__("source_row", "00" * 24)),
    ("wrong_coefficient", lambda rows: rows[0].__setitem__("coefficient", "1")),
    ("zero_terminal_q", lambda rows: rows[0].__setitem__("terminal_q", "0")),
    ("wrong_unit", lambda rows: rows[0].__setitem__("unit_scaled_U", "1")),
    ("wrong_contribution", lambda rows: rows[0].__setitem__("nonzero_contribution_scaled_U", "0")),
    ("wrong_final_degree", lambda rows: rows[0].__setitem__("final_degree", "3")),
    ("non_natural_order", lambda rows: rows.__setitem__(slice(0, 2), [rows[1], rows[0]])),
]

rejected = [reject(name, mutation) for name, mutation in mutations]
print(json.dumps({
    "status": "PASS_HOSTILE_K16_R44_SUPPORT_AWARE_CANDIDATE_CONTRACT",
    "rejected": rejected,
    "count": len(rejected),
}, sort_keys=True))
