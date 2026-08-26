#!/usr/bin/env python3
"""Regenerate conditional rep2 groups76..125 Q sources; never solve."""
from __future__ import annotations
import hashlib,importlib.util,json,os
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
BASE=ROOT/'computations/unaudited-codex-n8-x5-rep2-first25-exact-q-held-2026-08-25'
DESIGN=ROOT/'computations/unaudited-codex-n8-x5-rep2-corrected-guard-minor-contraction-design-2026-08-25'
PRIOR=ROOT/'computations/unaudited-codex-n8-x5-rep2-groups26-75-exact-q-conditional-held-2026-08-26'
PINS={BASE/'MANIFEST.sha256':'d694841e71b7982f50449b033ae21fb5798bd0ae765f75a9d655909a8c61022c',BASE/'canonical_census.json':'5ee661f3fdfd0e35e75d92d6efe7700b83011049e1d74a712ba8918681f86c8a',DESIGN/'MANIFEST.sha256':'ab18ee8446de2a163f1e6c14dfc60d2cd4c6465f5464206e10ecb35c2d2facf2',DESIGN/'generate_design.py':'ca23dbcb4179753393b7b0b3cd81d5c73d2c1bd26da559b00ca5136524aa83dc',PRIOR/'MANIFEST.sha256':'07c356ff169a8586add38bb8cb808977570a1ad83f001fb4918c5da163ef0f38'}
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def atomic(path,text):tmp=path.with_suffix(path.suffix+'.tmp');tmp.write_text(text);os.replace(tmp,path)
for path,want in PINS.items():assert sha(path)==want,(path,sha(path),want)
future=json.loads((HERE/'future_dependencies.json').read_text());assert future['status']=='UNSATISFIED_BOTH_NULL_HASH_PAIRS' and future['satisfied'] is False and len(future['dependencies'])==2
assert all(not d['satisfied'] and d['manifest_sha256'] is d['result_sha256'] is None for d in future['dependencies'])
census=json.loads((BASE/'canonical_census.json').read_text());assert census['status']=='PASS_REGENERATED_AUTHORITATIVE_972_TO_162_CENSUS' and [x['group_id'] for x in census['groups']]==list(range(162))
spec=importlib.util.spec_from_file_location('sealed_rep2_design',DESIGN/'generate_design.py');assert spec and spec.loader
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);engine=module.load_engine();module.configure_engine(engine)
ep='''ideal G=slimgb(I);\nprint("GROEBNER_SIZE="+string(size(G)));\npoly remainder=reduce(1,G);\nprint("UNIT_REMAINDER="+string(remainder));\nif (remainder==0) { print("STATUS=UNIT_IDEAL"); } else { print("STATUS=NONUNIT_OR_UNRESOLVED"); }\nquit;\n'''
lanes=[]
for ordinal,gid in enumerate(range(76,126),1):
 record=census['groups'][gid];q=module.build_program(engine,tuple(record['canonical_chart']));assert q.endswith('quit;\n') and q.count('quit;')==1;q=q[:-len('quit;\n')]+ep;data=q.encode();digest=hashlib.sha256(data).hexdigest();assert digest==record['exact_Q_source_sha256'] and len(data)==record['exact_Q_source_bytes']
 path=HERE/'sources'/f'rep2_group{gid:03d}_Q.sing';atomic(path,q);assert sha(path)==digest
 lanes.append({'ordinal':ordinal,'group_id':gid,'canonical_chart':record['canonical_chart'],'family':record['family'],'source_path':str(path.relative_to(HERE)),'source_sha256':digest,'source_bytes':len(data),'variables':91,'generators':6577})
ledger={'schema':'KRENN_X5_REP2_GROUPS76_125_EXACT_Q_SOURCE_LEDGER_V1','status':'PASS_REGENERATED_50_SOURCES_ZERO_SOLVES_CONDITIONAL','selection':{'required_closed_union':list(range(76)),'rule':'exact canonical group IDs 76..125 in strict ascending order','selected_group_ids':list(range(76,126))},'future_dependencies':{'path':'future_dependencies.json','sha256':sha(HERE/'future_dependencies.json'),'satisfied':False,'both_hash_pairs_null':True},'authoritative_census':{'path':str((BASE/'canonical_census.json').relative_to(ROOT)),'sha256':PINS[BASE/'canonical_census.json']},'lanes':lanes,'pins':{str(path.relative_to(ROOT)):digest for path,digest in PINS.items()},'scope':{'source_files_materialized':50,'solver_launches':0,'results_materialized':0,'clearances_materialized':0,'groups_newly_closed':0,'mathematical_coverage_added':False,'rep2_closed':False}}
atomic(HERE/'source_ledger.json',json.dumps(ledger,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':ledger['status'],'selected':[76,125],'ledger_sha256':sha(HERE/'source_ledger.json'),'bytes':sum(x['source_bytes'] for x in lanes),'solver_runs':0},sort_keys=True))
