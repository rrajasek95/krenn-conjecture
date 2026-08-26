#!/usr/bin/env python3
import hashlib
from pathlib import Path

here = Path(__file__).resolve().parent
for line in (here / "FINAL_MANIFEST.sha256").read_text().splitlines():
    digest, name = line.split(None, 1)
    assert hashlib.sha256((here / name.strip()).read_bytes()).hexdigest() == digest
print("PASS")
