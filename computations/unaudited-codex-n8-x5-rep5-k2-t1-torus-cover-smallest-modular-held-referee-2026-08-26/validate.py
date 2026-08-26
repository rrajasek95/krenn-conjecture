#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
H=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
r=json.loads((H/'results_referee.json').read_text())
assert r['status']=='PASS_APPROVED_HELD_ZERO_RUN'
assert r['held_manifest_sha256']=='21df0017be41a8ec9e4035b0902649cf9c8ed97d43c65c88a93d1db7f8bf6d72'
assert r['selected_Q_sha256']=='13c204f73bb82e263267ec977c19a10dba045541921375c2e7568ba48d5baba0'
assert r['modular_source_sha256']=='c36bd3b77052487b43751b03f48849c76091ec121a04abc3305cb56ec6494a8b'
assert (r['variables'],r['generators'],r['attempts'],r['solver_runs'])==(73,6561,0,0)
assert r['mathematical_coverage'] is r['exact_Q_authorized'] is r['other_chart_authorized'] is r['automatic_relaunch_authorized'] is False
for line in (H/'MANIFEST.sha256').read_text().splitlines():
 d,n=line.split(None,1);p=H/n.strip();assert p.is_file() and sha(p)==d
print('PASS_APPROVED_HELD_ZERO_RUN')
