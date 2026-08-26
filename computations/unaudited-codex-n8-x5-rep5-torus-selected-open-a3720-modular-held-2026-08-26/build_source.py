#!/usr/bin/env python3
"""Derive the sole held p32003 source from the sealed q=a37_20=1 Q chart."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

H = Path(__file__).resolve().parent
ROOT = H.parents[1]
REDUCTION = ROOT / "computations/unaudited-codex-n8-x5-rep5-torus-selected-further-reduction-design-2026-08-26"
Q = REDUCTION / "sources/stage0_a37_201_Q_design.sing"
OUT = H / "rep5_torus_selected_open_a37_201_p32003.sing"

PINS = {
    "selected73_held_manifest": (ROOT / "computations/unaudited-codex-n8-x5-rep5-k2-t1-torus-cover-smallest-modular-held-2026-08-26/MANIFEST.sha256", "21df0017be41a8ec9e4035b0902649cf9c8ed97d43c65c88a93d1db7f8bf6d72"),
    "selected73_referee_manifest": (ROOT / "computations/unaudited-codex-n8-x5-rep5-k2-t1-torus-cover-smallest-modular-held-referee-2026-08-26/MANIFEST.sha256", "16a32d07221def48a9e8388ca1e8b716cd71dfb44c2dc0cbea0bb22ab91203ab"),
    "torus_design_manifest": (ROOT / "computations/unaudited-codex-n8-x5-rep5-k2-t1-open84-torus-cover-design-2026-08-26/MANIFEST.sha256", "2b220f91ffa21c28506f5112a3a3e7fe791c7e3c783c1e7a319186628743659e"),
    "torus_referee_manifest": (ROOT / "computations/unaudited-codex-n8-x5-rep5-k2-t1-open84-torus-cover-referee-2026-08-26/MANIFEST.sha256", "20f24c8de6e7edb0818c30c11df4716e983fd5f8bf5778ee36d6d3bccf27d0ff"),
    "further_reduction_manifest": (REDUCTION / "MANIFEST.sha256", "a1be34a89dae7597ab06efe6eaba6e0e4fc12256949f667ac8124ee93c35690e"),
    "further_reduction_referee_manifest": (ROOT / "computations/unaudited-codex-n8-x5-rep5-torus-selected-further-reduction-design-referee-2026-08-26/FINAL_MANIFEST.sha256", "d87fe6724f8d1f4bf628eb01986339c86705e55adf9b471cfeed140e725b123e"),
    "prior_timeout_referee_manifest": (ROOT / "computations/unaudited-codex-n8-x5-rep5-rank2-open-smallest-modular-terminal-referee-2026-08-26/FINAL_MANIFEST.sha256", "0cb2ba3080ddda143ac01e4fd9f8714876c070ee86e7e574415c22cae4cac4ff"),
}
Q_SHA = "1e49c2b4127f1a185f50dbacbc63a51b97c210cb5dd9bd16a97f914c897fac1f"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def atomic_bytes(path: Path, value: bytes) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_bytes(value)
    os.replace(temporary, path)


def atomic_json(path: Path, value: object) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, path)


for _, (path, expected) in PINS.items():
    assert path.is_file() and sha(path) == expected
assert sha(Q) == Q_SHA
q = Q.read_bytes()
assert q.count(b"ring r=0,(") == 1 and q.endswith(b"quit;\n")
assert b'a37_20' not in q.split(b"ring r=0,(", 1)[1].split(b"),dp;", 1)[0]
assert b'print("INPUT_VARIABLES="+string(nvars(r)));' in q
assert b'print("INPUT_GENERATORS="+string(size(I)));' in q
strong = b'''ideal G=slimgb(I);
print("GROEBNER_SIZE="+string(size(G)));
poly remainder=reduce(1,G);
print("UNIT_REMAINDER="+string(remainder));
if (remainder==0) { print("STATUS=UNIT_IDEAL"); } else { print("STATUS=NONUNIT_OR_UNRESOLVED"); }
quit;
'''
modular = q.replace(b"ring r=0,(", b"ring r=32003,(", 1)[:-len(b"quit;\n")] + strong
assert modular.replace(b"ring r=32003,(", b"ring r=0,(", 1)[:-len(strong)] + b"quit;\n" == q
assert modular.count(b"ring r=32003,(") == 1
atomic_bytes(OUT, modular)
record = {
    "schema": "KRENN_X5_REP5_TORUS_SELECTED_OPEN_A3720_MODULAR_SOURCE_V1",
    "status": "PASS_SOLE_Q_TO_P_RING_PLUS_STRONG_EPILOGUE_ZERO_RUN",
    "input": {"path": str(Q.relative_to(ROOT)), "sha256": Q_SHA, "field": "Q", "variables": 72, "generators": 6561, "chart": "D(a37_20), normalized a37_20=1"},
    "output": {"path": OUT.name, "sha256": sha(OUT), "field": "F_32003", "variables": 72, "generators": 6561, "bytes": OUT.stat().st_size},
    "transformation": {"ring_replacements": 1, "strong_epilogue_appended": True, "inverse_byte_replay": True, "Q_body_otherwise_byte_identical": True},
    "pins": {name + "_sha256": expected for name, (_, expected) in PINS.items()},
    "scope": {"solver_runs": 0, "attempts": 0, "launch_authorized": False, "exact_Q_authorized": False, "closed_branch_authorized": False, "automatic_relaunch_authorized": False},
}
atomic_json(H / "source_derivation.json", record)
print(json.dumps({"status": record["status"], "source_sha256": sha(OUT), "shape": [72, 6561], "solver_runs": 0}, sort_keys=True))
