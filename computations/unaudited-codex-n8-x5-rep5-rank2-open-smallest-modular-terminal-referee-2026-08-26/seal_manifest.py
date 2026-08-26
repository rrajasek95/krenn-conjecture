#!/usr/bin/env python3
import hashlib
from pathlib import Path

here = Path(__file__).resolve().parent
names = ["referee.py", "results_referee.json", "REPORT.md", "validate.py"]
lines = []
for name in names:
    data = (here / name).read_bytes()
    lines.append(f"{hashlib.sha256(data).hexdigest()}  {name}\n")
(here / "FINAL_MANIFEST.sha256").write_text("".join(lines))
print(hashlib.sha256((here / "FINAL_MANIFEST.sha256").read_bytes()).hexdigest())
