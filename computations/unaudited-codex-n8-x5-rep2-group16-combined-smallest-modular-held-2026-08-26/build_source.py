#!/usr/bin/env python3
"""Derive the sole held p32003 source from the sealed exact-Q pilot; never solve."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

H = Path(__file__).resolve().parent
ROOT = H.parents[1]
REF = ROOT / "computations/unaudited-codex-n8-x5-rep2-group16-torus-gauge-referee-comparison-2026-08-26"
Q_SOURCE = REF / "rep2_group016_torus_A67zero_A12zero_guardpivot_k0_Q.sing"
OUT = H / "rep2_group016_torus_zerozero_guardpivot_k0_p32003.sing"
Q_SHA = "2403105f5c6bf4860525220d0d2d036099b79ace67297c864767ae71b9e97339"
P_SHA = "66bdb9277c9bff605e0d8a808ca65beb5967afaaf8ae494193286a60338355c6"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def atomic_bytes(path: Path, data: bytes) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_bytes(data)
    os.replace(temporary, path)


def atomic_json(path: Path, value: object) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, path)


assert sha(Q_SOURCE) == Q_SHA
source = Q_SOURCE.read_bytes()
old = b"ring r=0,("
new = b"ring r=32003,("
assert source.count(old) == 1 and source.count(new) == 0
modular = source.replace(old, new, 1)
assert modular.replace(new, old, 1) == source
assert modular.count(new) == 1 and modular.count(old) == 0
assert b"ideal G=slimgb(I);" in modular
assert b"poly remainder=reduce(1,G);" in modular
assert b"STATUS=UNIT_IDEAL" in modular and b"STATUS=NONUNIT_OR_UNRESOLVED" in modular
atomic_bytes(OUT, modular)
assert sha(OUT) == P_SHA
variables = modular.split(b"ring r=32003,(", 1)[1].split(b"),dp;", 1)[0].split(b",")
body = modular.split(b"ideal I=", 1)[1].split(b";\nprint", 1)[0]
depth = 0
generators = 1
for byte in body:
    depth += byte == ord("(")
    depth -= byte == ord(")")
    generators += byte == ord(",") and depth == 0
assert depth == 0 and len(variables) == 67 and generators == 6574
derivation = {
    "schema": "KRENN_X5_REP2_GROUP16_COMBINED_SMALLEST_MODULAR_SOURCE_DERIVATION_V1",
    "status": "PASS_SOLE_Q_TO_P32003_RING_SUBSTITUTION_ZERO_RUN",
    "exact_Q": {"path": str(Q_SOURCE.relative_to(ROOT)), "sha256": Q_SHA, "bytes": len(source), "field": "Q", "variables": 67, "generators": 6574},
    "modular": {"path": OUT.name, "sha256": P_SHA, "bytes": len(modular), "field": "F_32003", "variables": 67, "generators": 6574},
    "transformation": {"occurrences_replaced": 1, "old_literal": "ring r=0,( ".rstrip(), "new_literal": "ring r=32003,( ".rstrip(), "inverse_byte_replay": True, "non_ring_bytes_identical": True, "strong_solver_epilogue_preserved": True},
    "chart": {"torus_stratum": "A67=A12=0", "guard_pivot_open": "D(b0)", "logical_scope": "V(A67,A12) intersect D(b0)", "sufficient_for_group16": False},
    "scope": {"solver_runs": 0, "ideal_runs": 0, "launch_authorized": False, "exact_Q_authorized": False, "other_chart_authorized": False, "automatic_relaunch_authorized": False},
}
atomic_json(H / "source_derivation.json", derivation)
print(json.dumps({"status": derivation["status"], "source_sha256": P_SHA, "variables": 67, "generators": 6574, "solver_runs": 0}, sort_keys=True))
