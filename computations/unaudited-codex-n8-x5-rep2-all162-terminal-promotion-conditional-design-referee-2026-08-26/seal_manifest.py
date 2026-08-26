#!/usr/bin/env python3
import hashlib
from pathlib import Path
H=Path(__file__).resolve().parent
files=["REPORT.md","referee.py","results_referee.json","seal_manifest.py"]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert all((H/f).is_file() for f in files) and not any(H.glob("*.tmp"))
(H/"FINAL_MANIFEST.sha256").write_text("".join(f"{sha(H/f)}  {f}\n" for f in files))
for line in (H/"FINAL_MANIFEST.sha256").read_text().splitlines():
 d,f=line.split("  ",1); assert sha(H/f)==d
print(sha(H/"FINAL_MANIFEST.sha256"))
