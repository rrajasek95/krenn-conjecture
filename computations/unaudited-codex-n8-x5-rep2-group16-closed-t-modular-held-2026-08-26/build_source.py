#!/usr/bin/env python3
"""Derive the sole held p32003 closed-t source from the sealed exact-Q chart."""
import hashlib,json,os
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[1]
Q=ROOT/'computations/unaudited-codex-n8-x5-rep2-group16-67-timeout-reduction-design-2026-08-26/rep2_group016_67_Vt0_Vt1_Vt2_Q.sing';OUT=H/'rep2_group016_62_Vt0_Vt1_Vt2_p32003.sing'
QSHA='43beb317cb0bc59b24f1d4c5613ef6baccd7ec064651e004c1f8eb4657d538fc';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(Q)==QSHA;q=Q.read_bytes();assert q.count(b'ring r=0,(')==1 and q.endswith(b'quit;\n')
strong=b'''ideal G=slimgb(I);\nprint("GROEBNER_SIZE="+string(size(G)));\npoly remainder=reduce(1,G);\nprint("UNIT_REMAINDER="+string(remainder));\nif (remainder==0) { print("STATUS=UNIT_IDEAL"); } else { print("STATUS=NONUNIT_OR_UNRESOLVED"); }\nquit;\n'''
p=q.replace(b'ring r=0,(',b'ring r=32003,(',1)[:-len(b'quit;\n')]+strong;assert p.replace(b'ring r=32003,(',b'ring r=0,(',1)[:-len(strong)]+b'quit;\n'==q
t=OUT.with_suffix('.sing.tmp');t.write_bytes(p);os.replace(t,OUT)
body=p.split(b'ideal I=',1)[1].split(b';\nprint',1)[0];depth=0;gens=1
for c in body:depth+=c==40;depth-=c==41;gens+=c==44 and depth==0
variables=p.split(b'ring r=32003,(',1)[1].split(b'),dp;',1)[0].split(b',');assert depth==0 and len(variables)==62 and gens==6568
d={'schema':'KRENN_X5_REP2_GROUP16_CLOSED_T_MODULAR_SOURCE_V1','status':'PASS_SOLE_RING_PLUS_STRONG_EPILOGUE_ZERO_RUN','exact_Q':{'path':str(Q.relative_to(ROOT)),'sha256':QSHA,'bytes':len(q),'variables':62,'generators':6568},'modular':{'path':OUT.name,'sha256':sha(OUT),'bytes':len(p),'field':'F_32003','variables':62,'generators':6568},'transformation':{'ring_replacements':1,'strong_epilogue_appended':True,'inverse_byte_replay':True,'other_Q_body_bytes_identical':True},'chart':{'conditions':['A67=0','A12=0','D(b0)','t0=0','t1=0','t2=0'],'global_cover_member_count':60,'single_chart_closes_group16':False},'scope':{'solver_runs':0,'attempts':0,'launch_authorized':False,'exact_Q_authorized':False,'other_chart_authorized':False,'automatic_relaunch_authorized':False}}
j=H/'source_derivation.json.tmp';j.write_text(json.dumps(d,indent=2,sort_keys=True)+'\n');os.replace(j,H/'source_derivation.json');print(json.dumps({'status':d['status'],'source_sha256':sha(OUT),'shape':[62,6568],'solver_runs':0},sort_keys=True))
