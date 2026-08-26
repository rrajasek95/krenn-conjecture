#!/usr/bin/env python3
import hashlib
from pathlib import Path
H=Path(__file__).resolve().parent;files=['REPORT.md','analyze_and_build.py','rep2_group016_guardpivot_k0_Q.sing','rep2_group016_guardpivot_k1_Q.sing','rep2_group016_guardpivot_k2_Q.sing','results_group16_design.json','results_validation.json','seal_manifest.py','validate.py'];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert all((H/f).is_file() for f in files) and not any(H.glob('*.tmp'))
(H/'MANIFEST.sha256').write_text(''.join(f'{sha(H/f)}  {f}\n' for f in files))
for line in (H/'MANIFEST.sha256').read_text().splitlines():d,f=line.split('  ',1);assert sha(H/f)==d
print(sha(H/'MANIFEST.sha256'))
