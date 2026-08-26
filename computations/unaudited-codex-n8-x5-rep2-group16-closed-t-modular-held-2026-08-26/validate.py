#!/usr/bin/env python3
"""Validate held closed-t package without solving."""
import ast,hashlib,json
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[1];Q=ROOT/'computations/unaudited-codex-n8-x5-rep2-group16-67-timeout-reduction-design-2026-08-26/rep2_group016_67_Vt0_Vt1_Vt2_Q.sing';P=H/'rep2_group016_62_Vt0_Vt1_Vt2_p32003.sing';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(Q)=='43beb317cb0bc59b24f1d4c5613ef6baccd7ec064651e004c1f8eb4657d538fc' and sha(P)=='d7e57a3d43fb1280381660be2fea9c966eb086bd2aced3189b0f599030f5822b'
strong=b'''ideal G=slimgb(I);\nprint("GROEBNER_SIZE="+string(size(G)));\npoly remainder=reduce(1,G);\nprint("UNIT_REMAINDER="+string(remainder));\nif (remainder==0) { print("STATUS=UNIT_IDEAL"); } else { print("STATUS=NONUNIT_OR_UNRESOLVED"); }\nquit;\n''';assert P.read_bytes().replace(b'ring r=32003,(',b'ring r=0,(',1)[:-len(strong)]+b'quit;\n'==Q.read_bytes()
d=json.loads((H/'source_derivation.json').read_text());held=json.loads((H/'held_pilot.json').read_text());assert d['status']=='PASS_SOLE_RING_PLUS_STRONG_EPILOGUE_ZERO_RUN' and d['modular']['variables']==62 and d['modular']['generators']==6568 and d['transformation']['inverse_byte_replay']
assert held['status']=='HELD_ZERO_RUN_PENDING_INDEPENDENT_AUDIT_AND_FRESH_CLEARANCE' and held['execution']=={'maximum_lane_count':1,'native_wall_seconds':240,'wrapper_wall_seconds':255,'rss_cap_bytes':8589934592,'direct_libproc_group_rss':True,'fresh_libproc_process_census':True,'atomic_result':True,'exclusive_attempt_marker':True,'strict_stop_after_any_outcome':True}
pins=held['pins'];assert pins['timeout_referee_manifest_sha256']=='ef85c2ee938da004226540d76e609feb9fae4261808f6ac755e9bfd8b268c73c' and pins['reduction_design_manifest_sha256']=='3d4d6fbc89f5adcc45032c37b1b038780761f479313575c59e4e8bd760da75fd' and pins['reduction_referee_manifest_sha256']=='e41de381875869a6ac206454b57e091b7ed1093f76aad4a9b71ed30929d3b3cd' and pins['torus_producer_manifest_sha256']=='1492e69373819fda0c50afc4f1366e2d6da90e857c26f73c03c0212ffd879282' and pins['guard_pivot_manifest_sha256']=='6a781149041e8808d58a53af77059253fe0a0d4295052bfe34756a0f994a0aee' and pins['combined_cover_manifest_sha256']=='1a2dcba289d5f31e39be48c4f98ff44a6b0c6891841fd345df52f06abfd5525a'
assert held['authorization']=={'independent_acceptance_present':False,'fresh_clearance_present':False,'exact_Q_authorized':False,'other_chart_authorized':False,'automatic_relaunch_authorized':False} and held['scope']['solver_runs']==held['scope']['attempts']==held['scope']['results']==0 and held['scope']['prior_timeout_reused'] is False
assert not (H/'independent_referee_acceptance.json').exists() and not (H/'launch_clearance.json').exists()
for name in ('ATTEMPT.json','result.json','stdout.log','stderr.log','watchdog.json','RUN_EXCLUSIVE.lock'):assert not (H/name).exists()
assert not list(H.glob('*.tmp')) and not list(H.rglob('__pycache__'));runner=(H/'run_one_lane.py').read_text();ast.parse(runner)
for literal in ('NATIVE=240','WRAPPER=255','RSS_CAP=8*1024**3','census()','grss(process.pid)',"exclusive(H/'ATTEMPT.json'",'\'exact_Q_launched\':False','\'other_chart_launched\':False','\'automatic_relaunch\':False'):assert literal in runner
for name in ('independent_referee_acceptance.schema.json','launch_clearance.schema.json'):
 s=json.loads((H/name).read_text());assert s['additionalProperties'] is False and set(s['required'])==set(s['properties'])
if (H/'MANIFEST.sha256').exists():
 for line in (H/'MANIFEST.sha256').read_text().splitlines():d,name=line.split(None,1);p=(H/name.strip()).resolve();assert p.is_file() and sha(p)==d
print(json.dumps({'status':'PASS_CLOSED_T_MODULAR_HELD_ZERO_RUN','source':sha(P),'shape':[62,6568],'attempts':0,'solver_runs':0},sort_keys=True))
