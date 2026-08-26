#!/usr/bin/env python3
"""Materialize the sealed group15 Q source; never launch a process."""
import hashlib
import importlib.util
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
MINOR = ROOT / "computations/unaudited-codex-n8-x5-seven-block-rep1-guard-minor-quotient-2026-08-25"
PLAN = ROOT / "computations/unaudited-codex-n8-x5-rep1-group15-direct-libproc-held-plan-2026-08-25/HELD_GROUP15_PLAN.json"
REFEREE = ROOT / "computations/unaudited-codex-n8-x5-rep1-group15-direct-libproc-held-plan-referee-2026-08-25/FINAL_MANIFEST.sha256"
SOURCE = HERE / "rep1_group15_Q.sing"
EXPECTED = {
    MINOR / "MANIFEST.sha256": "4f367478c0a91257022234f5115979423bc8e889dd81a74cc3c200e25e3f82c1",
    MINOR / "generate_minor_quotient.py": "63a4a58344c4bfdce0406d243f881216ca53eaa71264926a28364a823f560ac8",
    PLAN: "e778f68f78c087a2d63f4491e0d67d9920302dc55cd2d39e80abc380f66c6ce4",
    REFEREE: "b1714d0a1d689ebae04017bf6ccb5120861996160cc4a37892542e3592e36761",
}
SOURCE_SHA = "1611c16c73323e7a85ee730ba055f9f2092873841698e8fcc4f5799571ccab04"
SOURCE_BYTES = 1841468


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


for path, expected in EXPECTED.items():
    assert sha(path) == expected, (path, sha(path), expected)
if len(sys.argv) == 2 and sys.argv[1] == "--verify":
    assert SOURCE.is_file() and SOURCE.stat().st_size == SOURCE_BYTES and sha(SOURCE) == SOURCE_SHA
    print(f"PASS {SOURCE_SHA} {SOURCE_BYTES}")
    raise SystemExit(0)
assert sys.argv == [sys.argv[0]], "usage: materialize_source.py [--verify]"
assert not SOURCE.exists(), f"refusing to overwrite {SOURCE}"
spec = importlib.util.spec_from_file_location("sealed_minor", MINOR / "generate_minor_quotient.py")
assert spec and spec.loader
minor = importlib.util.module_from_spec(spec)
spec.loader.exec_module(minor)
base = minor.load_base()
chart = {"coordinate": 0, "outside": (0, 0), "x_pivot": 1, "q_kind": "z", "q_pivot": 1, "minor_pair": (0, 2)}
program = minor.build_program(base, chart, "0")
encoded = program.encode()
assert len(encoded) == SOURCE_BYTES and hashlib.sha256(encoded).hexdigest() == SOURCE_SHA
temporary = SOURCE.with_suffix(".sing.tmp")
with temporary.open("wb") as stream:
    stream.write(encoded)
    stream.flush()
    os.fsync(stream.fileno())
os.replace(temporary, SOURCE)
assert sha(SOURCE) == SOURCE_SHA and not temporary.exists()
print(f"MATERIALIZED_NOT_RUN {SOURCE_SHA} {SOURCE_BYTES}")
