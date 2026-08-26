#!/usr/bin/env python3
"""Materialize the exact-Q closed-t source by sole strong-transcript substitution."""
from __future__ import annotations

import hashlib
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BASE = ROOT / "computations/unaudited-codex-n8-x5-rep2-group16-67-timeout-reduction-design-2026-08-26/rep2_group016_67_Vt0_Vt1_Vt2_Q.sing"
OUT = HERE / "rep2_group016_62_Vt0_Vt1_Vt2_Q_strong.sing"
BASE_SHA = "43beb317cb0bc59b24f1d4c5613ef6baccd7ec064651e004c1f8eb4657d538fc"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


assert sha(BASE) == BASE_SHA
old = b'print("INPUT_GENERATORS="+string(size(I)));\nquit;\n'
strong = (
    b'print("INPUT_GENERATORS="+string(size(I)));\n'
    b"ideal G=slimgb(I);\n"
    b'print("GROEBNER_SIZE="+string(size(G)));\n'
    b"poly remainder=reduce(1,G);\n"
    b'print("UNIT_REMAINDER="+string(remainder));\n'
    b'if (remainder==0) { print("STATUS=UNIT_IDEAL"); } else { print("STATUS=NONUNIT_OR_UNRESOLVED"); }\n'
    b"quit;\n"
)
data = BASE.read_bytes()
assert data.count(old) == 1
runtime = data.replace(old, strong, 1)
temporary = OUT.with_suffix(OUT.suffix + ".tmp")
temporary.write_bytes(runtime)
os.replace(temporary, OUT)
assert OUT.read_bytes().replace(strong, old, 1) == data
print(sha(OUT))
