#!/usr/bin/env python3
"""Validate held smallest-chart package without invoking Singular."""
import ast,hashlib,json
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[1]
Q=ROOT/'computations/unaudited-codex-n8-x5-rep5-k2-t1-open84-torus-cover-design-2026-08-26/sources/rep5_k2_t1_gauge_yn11_yn21_t01_t20_Q_design.sing';P=H/'rep5_k2_t1_gauge_yn11_yn21_t01_t20_p32003.sing'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(Q)=='13c204f73bb82e263267ec977c19a10dba045541921375c2e7568ba48d5baba0' and sha(P)=='c36bd3b77052487b43751b03f48849c76091ec121a04abc3305cb56ec6494a8b'
q,p=Q.read_bytes(),P.read_bytes();strong=b'''ideal G=slimgb(I);\nprint("GROEBNER_SIZE="+string(size(G)));\npoly remainder=reduce(1,G);\nprint("UNIT_REMAINDER="+string(remainder));\nif (remainder==0) { print("STATUS=UNIT_IDEAL"); } else { print("STATUS=NONUNIT_OR_UNRESOLVED"); }\nquit;\n'''
assert p.replace(b'ring r=32003,(',b'ring r=0,(',1)[:-len(strong)]+b'quit;\n'==q
d=json.loads((H/'source_derivation.json').read_text());ledger=json.loads((H/'selection_ledger.json').read_text());held=json.loads((H/'held_pilot.json').read_text())
assert d['status']=='PASS_DETERMINISTIC_SMALLEST_SOLE_RING_PLUS_EPILOGUE_ZERO_RUN' and d['candidate_count']==16 and d['all_candidates_tied_on_bytes_and_terms']
assert d['selection_rule']==['source_bytes','expanded_syntax_term_count','lexicographic_sha256'] and d['selected']['sha256']==sha(Q)
assert len(ledger['candidates'])==16 and ledger['selected_sha256']==sha(Q)
assert all(x['bytes']==4416511 and x['expanded_syntax_term_count']==5322351 for x in ledger['candidates'])
assert [x['sha256'] for x in ledger['candidates']]==sorted(x['sha256'] for x in ledger['candidates'])
assert held['status']=='HELD_ZERO_RUN_PENDING_INDEPENDENT_AUDIT_AND_FRESH_CLEARANCE'
assert held['execution']=={'maximum_lane_count':1,'native_wall_seconds':240,'wrapper_wall_seconds':255,'rss_cap_bytes':8589934592,'direct_libproc_group_rss':True,'fresh_libproc_process_census':True,'atomic_result':True,'exclusive_attempt_marker':True,'strict_stop_after_any_outcome':True}
assert held['pins']['torus_producer_manifest_sha256']=='2b220f91ffa21c28506f5112a3a3e7fe791c7e3c783c1e7a319186628743659e' and held['pins']['torus_referee_manifest_sha256']=='20f24c8de6e7edb0818c30c11df4716e983fd5f8bf5778ee36d6d3bccf27d0ff' and held['pins']['prior_timeout_referee_manifest_sha256']=='0cb2ba3080ddda143ac01e4fd9f8714876c070ee86e7e574415c22cae4cac4ff'
assert held['authorization']=={'independent_acceptance_present':False,'fresh_clearance_present':False,'exact_Q_authorized':False,'other_chart_authorized':False,'automatic_relaunch_authorized':False}
assert held['scope']['solver_runs']==held['scope']['attempts']==held['scope']['results']==0 and held['scope']['prior_timeout_reused'] is False
assert not (H/'independent_referee_acceptance.json').exists() and not (H/'launch_clearance.json').exists()
for name in ('ATTEMPT.json','result.json','stdout.log','stderr.log','watchdog.json','RUN_EXCLUSIVE.lock'):assert not (H/name).exists()
assert not list(H.glob('*.tmp')) and not list(H.rglob('__pycache__'))
runner=(H/'run_one_lane.py').read_text();ast.parse(runner)
for literal in ('NATIVE=240','WRAPPER=255','RSS_CAP=8*1024**3','census()','grouprss(process.pid)','exclusive(H/\'ATTEMPT.json\'','\'exact_Q_launched\':False','\'other_chart_launched\':False','\'automatic_relaunch\':False'):assert literal in runner,literal
for name in ('independent_referee_acceptance.schema.json','launch_clearance.schema.json'):
 s=json.loads((H/name).read_text());assert s['additionalProperties'] is False and set(s['required'])==set(s['properties'])
if (H/'MANIFEST.sha256').exists():
 for line in (H/'MANIFEST.sha256').read_text().splitlines():
  digest,name=line.split(None,1);path=(H/name.strip()).resolve();assert path.is_file() and sha(path)==digest
print(json.dumps({'status':'PASS_REP5_SMALLEST_TORUS_MODULAR_HELD_ZERO_RUN','selected_Q':sha(Q),'source':sha(P),'shape':[73,6561],'attempts':0,'solver_runs':0},sort_keys=True))
