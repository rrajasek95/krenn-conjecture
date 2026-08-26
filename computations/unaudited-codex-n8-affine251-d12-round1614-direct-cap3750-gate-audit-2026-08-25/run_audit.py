#!/usr/bin/env python3
"""Run the pinned r1601 cap-audit parser with exact r1614 substitutions."""
from hashlib import sha256
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BASE = ROOT / "computations/unaudited-codex-n8-affine251-d12-round1601-direct-cap3500-gate-audit-2026-08-25/audit_direct_cap_gate.py"
raw = BASE.read_bytes()
assert sha256(raw).hexdigest() == "e7834ea164feadb73fa45a7c6120837b1b82c50e78e8a8a4f7cb88d27f9338cb"
s = raw.decode()
replacements = {
    "r1601 3.25m -> 3.5m": "r1614 3.5m -> 3.75m",
    '"PASS_EXACT_FULLY_TELEMETERED_ROUND1600_CAP3250_CHAIN"':
        '"PASS_EXACT_ROUND1613_CAP3500_CHAIN_WITH_AUDITED_COOPERATIVE_OVERSHOOT"',
    'input_audit["final"]["round"] == 1600':
        'input_audit["final"]["round"] == 1613',
    '"PASS_SIX_DESCENDANT_EDGES_AND_ALL_COLUMNS"':
        '"PASS_ALL_DESCENDANT_EDGES_AND_ALL_COLUMNS"',
    '"KRENN_AFFINE251_D12_ROUND1601_DIRECT_CAP3500_AUDIT_V1"':
        '"KRENN_AFFINE251_D12_ROUND1614_DIRECT_CAP3750_AUDIT_V1"',
    '"PASS_EXACT_DIRECT_CAP3250_TO_CAP3500_EQUIVALENCE"':
        '"PASS_EXACT_DIRECT_CAP3500_TO_CAP3750_EQUIVALENCE"',
    'results_round1601_direct_cap3500_audit.json.tmp':
        'results_round1614_direct_cap3750_audit.json.tmp',
    'results_round1601_direct_cap3500_audit.json':
        'results_round1614_direct_cap3750_audit.json',
}
for old, new in replacements.items():
    assert s.count(old) >= 1, (old, s.count(old))
    s = s.replace(old, new)
exec(compile(s, str(HERE / "run_audit.py"), "exec"),
     {"__file__": str(HERE / "run_audit.py"), "__name__": "__main__"})
