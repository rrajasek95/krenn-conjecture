#!/usr/bin/env python3
"""Fail-closed independent audit of the r1627 3.75m -> 4.0m cap gate."""
from hashlib import sha256
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BASE = ROOT / "computations/unaudited-codex-n8-affine251-d12-round1601-direct-cap3500-gate-audit-2026-08-25/audit_direct_cap_gate.py"
raw = BASE.read_bytes()
assert sha256(raw).hexdigest() == "e7834ea164feadb73fa45a7c6120837b1b82c50e78e8a8a4f7cb88d27f9338cb"
s = raw.decode()
replacements = {
    "r1601 3.25m -> 3.5m": "r1627 3.75m -> 4.0m",
    '"PASS_EXACT_FULLY_TELEMETERED_ROUND1600_CAP3250_CHAIN"':
        '"PASS_EXACT_ROUND1626_CAP3750_CHAIN"',
    'input_audit["final"]["round"] == 1600':
        'input_audit["final"]["round"] == 1626',
    '"PASS_SIX_DESCENDANT_EDGES_AND_ALL_COLUMNS"':
        '"PASS_ALL_DESCENDANT_EDGES_AND_ALL_COLUMNS"',
    '"KRENN_AFFINE251_D12_ROUND1601_DIRECT_CAP3500_AUDIT_V1"':
        '"KRENN_AFFINE251_D12_ROUND1627_DIRECT_CAP4000_AUDIT_V1"',
    '"PASS_EXACT_DIRECT_CAP3250_TO_CAP3500_EQUIVALENCE"':
        '"PASS_EXACT_DIRECT_CAP3750_TO_CAP4000_EQUIVALENCE"',
    'results_round1601_direct_cap3500_audit.json.tmp':
        'results_round1627_direct_cap4000_audit.json.tmp',
    'results_round1601_direct_cap3500_audit.json':
        'results_round1627_direct_cap4000_audit.json',
    '"continued_beyond_round1601"': '"continued_beyond_round1626"',
}
for old, new in replacements.items():
    assert s.count(old) >= 1, (old, s.count(old))
    s = s.replace(old, new)
exec(compile(s, str(HERE / "run_audit.py"), "exec"),
     {"__file__": str(HERE / "run_audit.py"), "__name__": "__main__"})
