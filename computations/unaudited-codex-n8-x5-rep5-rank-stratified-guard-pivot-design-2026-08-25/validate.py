#!/usr/bin/env python3
import hashlib
from pathlib import Path
here = Path(__file__).resolve().parent
for line in (here / "MANIFEST.sha256").read_text().splitlines():
    expected, name = line.split(None, 1)
    target = Path(name.strip())
    if not target.is_absolute(): target = (here / target).resolve()
    assert hashlib.sha256(target.read_bytes()).hexdigest() == expected
print("PASS")
