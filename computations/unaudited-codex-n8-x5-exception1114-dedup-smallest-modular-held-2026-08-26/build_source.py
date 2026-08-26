#!/usr/bin/env python3
"""Derive the sole held p32003 diagnostic from the sealed 58/6533 Q source."""

import hashlib
import json
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PARENT = ROOT / "computations/unaudited-codex-n8-x5-exception1114-rank1-symbolic-reduction-design-2026-08-26"
Q = PARENT / "rep1114_rank1_z1_fulltorus_dedup_Q.sing"
OUT = HERE / "rep1114_rank1_z1_fulltorus_dedup_p32003.sing"
PINS = {
    "rank1_refinement_manifest": (
        ROOT / "computations/unaudited-codex-n8-x5-exception1114-rank1-refinement-design-2026-08-26/MANIFEST.sha256",
        "aea0841b7b1b6fe0773cfb5087a930329c4da5d94951ad23d559de6d61cddb46",
    ),
    "symbolic_reduction_manifest": (PARENT / "MANIFEST.sha256", "785ec6cb6a5d790ece4fa3aed3801b48c3c51423e4378cd761ad8b50cd2d22b9"),
}
Q_SHA = "ed6a47ec38fca48e6b7396e36c61e3eca8004089bd2964476e1dcdd45b69de1f"
PRIME = 32003


def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            h.update(chunk)
    return h.hexdigest()


def atomic_bytes(path, value):
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_bytes(value)
    os.replace(temporary, path)


def atomic_json(path, value):
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, path)


for label, (path, expected) in PINS.items():
    if not path.is_file() or sha(path) != expected:
        raise RuntimeError((label, path))
if sha(Q) != Q_SHA:
    raise RuntimeError("Q source pin mismatch")
q = Q.read_bytes()
if q.count(b"ring r=0,(") != 1 or not q.endswith(b"quit;\n"):
    raise RuntimeError("unexpected Q source framing")
if q.count(b'print("INPUT_VARIABLES="+string(nvars(r)));') != 1 or q.count(b'print("INPUT_GENERATORS="+string(size(I)));') != 1:
    raise RuntimeError("missing shape transcript")
strong = b'''option(redSB);
ideal G=slimgb(I);
print("GROEBNER_SIZE="+string(size(G)));
poly unit_remainder=reduce(1,G);
print("UNIT_REMAINDER="+string(unit_remainder));
if (unit_remainder==0) { print("STATUS=UNIT_IDEAL"); } else { print("STATUS=NONUNIT_OR_UNRESOLVED"); }
quit;
'''
modular = q.replace(b"ring r=0,(", f"ring r={PRIME},(".encode(), 1)[:-len(b"quit;\n")] + strong
inverse = modular.replace(f"ring r={PRIME},(".encode(), b"ring r=0,(", 1)[:-len(strong)] + b"quit;\n"
if inverse != q:
    raise RuntimeError("inverse byte replay failed")
if modular.count(f"ring r={PRIME},(".encode()) != 1 or modular.count(b"ideal G=slimgb(I);") != 1:
    raise RuntimeError("modular source framing")
atomic_bytes(OUT, modular)
record = {
    "schema": "KRENN_X5_EXCEPTION1114_DEDUP_P32003_SOURCE_V1",
    "status": "PASS_SOLE_Q_TO_P_RING_PLUS_STRONG_TRANSCRIPT_ZERO_RUN",
    "input": {"path": str(Q.relative_to(ROOT)), "sha256": Q_SHA, "field": "Q", "variables": 58, "generators": 6533},
    "output": {"path": OUT.name, "sha256": sha(OUT), "field": "F_32003", "variables": 58, "generators": 6533, "bytes": OUT.stat().st_size},
    "prime": {"value": PRIME, "selection": "p32003 is the established safe diagnostic prime; source coefficients reduce literally and no denominator is zero"},
    "transformation": {
        "ring_replacements": 1,
        "strong_transcript": ["option(redSB)", "slimgb(I)", "GROEBNER_SIZE", "reduce(1,G)", "UNIT_REMAINDER", "STATUS"],
        "inverse_byte_replay": True,
        "Q_body_otherwise_byte_identical": True,
    },
    "pins": {label + "_sha256": expected for label, (_, expected) in PINS.items()},
    "scope": {"solver_runs": 0, "attempts": 0, "launch_authorized": False, "exact_Q_authorized": False, "automatic_relaunch_authorized": False},
}
atomic_json(HERE / "source_derivation.json", record)
print(json.dumps({"status": record["status"], "source_sha256": sha(OUT), "shape": [58, 6533]}, sort_keys=True))
