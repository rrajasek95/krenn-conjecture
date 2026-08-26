#!/usr/bin/env python3
import hashlib
from pathlib import Path

here = Path(__file__).resolve().parent
for line in (here / "FINAL_MANIFEST.sha256").read_text().splitlines():
    expected, name = line.split(None, 1)
    path = here / name.strip()
    assert hashlib.sha256(path.read_bytes()).hexdigest() == expected
print("PASS")
