#!/usr/bin/env python3
"""Append only the strong exact-Q transcript epilogue to the pinned Q design."""
from __future__ import annotations
import hashlib,json
from pathlib import Path
H=Path(__file__).resolve().parent
BASE=H/'rep5_k2_t1_torus_smallest_Q_base.sing'; OUT=H/'rep5_k2_t1_torus_smallest_Q.sing'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(BASE)=='13c204f73bb82e263267ec977c19a10dba045541921375c2e7568ba48d5baba0'
base=BASE.read_bytes(); old=b'print("INPUT_GENERATORS="+string(size(I)));\nquit;\n'
strong=b'''print("INPUT_GENERATORS="+string(size(I)));
ideal G=slimgb(I);
print("GROEBNER_SIZE="+string(size(G)));
poly remainder=reduce(1,G);
print("UNIT_REMAINDER="+string(remainder));
if (remainder==0) { print("STATUS=UNIT_IDEAL"); } else { print("STATUS=NONUNIT_OR_UNRESOLVED"); }
quit;
'''
assert base.count(old)==1
out=base.replace(old,strong,1);OUT.write_bytes(out)
assert out.replace(strong,old,1)==base
variables=out.split(b'ring r=0,(',1)[1].split(b'),dp;',1)[0].split(b',')
body=out.split(b'ideal I=',1)[1].split(b';\n',1)[0];depth=0;generators=1
for c in body:
 if c==40:depth+=1
 elif c==41:depth-=1
 elif c==44 and depth==0:generators+=1
assert len(variables)==73 and generators==6561 and depth==0
result={'schema':'KRENN_X5_REP5_TORUS_SMALLEST_EXACT_Q_SOURCE_DERIVATION_V1','status':'PASS_SOLE_STRONG_TRANSCRIPT_APPEND','base_Q_sha256':sha(BASE),'runtime_Q_sha256':sha(OUT),'variables':73,'generators':6561,'field':'Q','body_identity':True,'solver_runs':0}
(H/'source_derivation.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print(json.dumps(result,sort_keys=True))
