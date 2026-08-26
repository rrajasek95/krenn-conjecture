#!/usr/bin/env python3
import hashlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
files = sorted(path for path in HERE.iterdir() if path.is_file() and path.name != "MANIFEST.sha256")
lines = []
for path in files:
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    lines.append(f"{digest}  {path.name}\n")
(HERE / "MANIFEST.sha256").write_text("".join(lines))
print(hashlib.sha256((HERE / "MANIFEST.sha256").read_bytes()).hexdigest())
