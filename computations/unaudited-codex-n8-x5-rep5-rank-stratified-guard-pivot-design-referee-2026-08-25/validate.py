#!/usr/bin/env python3
import hashlib
from pathlib import Path
p=Path(__file__).resolve().parent
for line in (p/'FINAL_MANIFEST.sha256').read_text().splitlines():
 d,n=line.split(None,1);assert hashlib.sha256((p/n.strip()).read_bytes()).hexdigest()==d
print('PASS')
