#!/usr/bin/env python3
import hashlib
from pathlib import Path

here = Path(__file__).resolve().parent
names = ["referee.py", "results_referee.json", "REPORT.md", "validate.py"]
(here / "FINAL_MANIFEST.sha256").write_text("".join(
    f"{hashlib.sha256((here / name).read_bytes()).hexdigest()}  {name}\n" for name in names
))
print(hashlib.sha256((here / "FINAL_MANIFEST.sha256").read_bytes()).hexdigest())
