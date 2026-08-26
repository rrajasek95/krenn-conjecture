#!/usr/bin/env python3
import hashlib, json
from pathlib import Path
HERE=Path(__file__).resolve().parent;sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
r=json.loads((HERE/'results_compatibility.json').read_text());q=json.loads((HERE/'results_referee.json').read_text());d=json.loads((HERE/'normalized_dependencies.json').read_text());a=json.loads((HERE/'independent_referee_acceptance.json').read_text());h=json.loads((HERE/'results_hostile_tests.json').read_text())
assert r['status']=='PASS_HELD_LAUNCH_READY_COMPATIBLE_V1_ZERO_RUNS_NO_CLEARANCE' and q['status']=='PASS_INDEPENDENT_HELD_LAUNCH_READY_COMPATIBLE_V1_ZERO_RUNS_NO_CLEARANCE'
assert d['schema']=='KRENN_X5_REP4_GROUPS76_125_NORMALIZED_DEPENDENCIES_V1' and d['closed_union']==list(range(76));assert a['normalized_dependencies_sha256']==sha(HERE/'normalized_dependencies.json');assert len(h['tests'])==15 and all(h['tests'].values())
assert r['scope']['solver_runs']==r['scope']['attempts']==0 and r['scope']['launch_clearance_materialized'] is False
n=0
if (HERE/'FINAL_MANIFEST.sha256').exists():
 for line in (HERE/'FINAL_MANIFEST.sha256').read_text().splitlines():
  digest,name=line.split(None,1);path=(HERE/name.strip()).resolve();assert path.is_file() and sha(path)==digest;n+=1
print(json.dumps({'status':'PASS_COMPATIBILITY_V3_VALIDATED_ZERO_RUN','manifest_lines_checked':n},sort_keys=True))
