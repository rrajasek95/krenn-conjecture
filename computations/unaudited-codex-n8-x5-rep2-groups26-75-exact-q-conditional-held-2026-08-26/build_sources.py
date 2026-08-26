#!/usr/bin/env python3
"""Regenerate conditional rep2 groups26..75 sources from the authoritative census; no solve."""
from __future__ import annotations
import hashlib,importlib.util,json,os
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];BASE=ROOT/'computations/unaudited-codex-n8-x5-rep2-first25-exact-q-held-2026-08-25';DESIGN=ROOT/'computations/unaudited-codex-n8-x5-rep2-corrected-guard-minor-contraction-design-2026-08-25'
PINS={BASE/'MANIFEST.sha256':'d694841e71b7982f50449b033ae21fb5798bd0ae765f75a9d655909a8c61022c',BASE/'canonical_census.json':'5ee661f3fdfd0e35e75d92d6efe7700b83011049e1d74a712ba8918681f86c8a',BASE/'source_ledger.json':'20737fd8197335f98214222bc5caa4c3d8c1ba2b2fcc283065d865befcf6389e',DESIGN/'MANIFEST.sha256':'ab18ee8446de2a163f1e6c14dfc60d2cd4c6465f5464206e10ecb35c2d2facf2',DESIGN/'generate_design.py':'ca23dbcb4179753393b7b0b3cd81d5c73d2c1bd26da559b00ca5136524aa83dc'}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def atomic(p,text):t=p.with_suffix(p.suffix+'.tmp');t.write_text(text);os.replace(t,p)
def module():
 s=importlib.util.spec_from_file_location('sealed_rep2_design',DESIGN/'generate_design.py');assert s and s.loader;m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
for p,h in PINS.items():assert sha(p)==h,(p,sha(p),h)
census=json.loads((BASE/'canonical_census.json').read_text());assert census['status']=='PASS_REGENERATED_AUTHORITATIVE_972_TO_162_CENSUS' and census['closed_group_identification']['group_id']==0 and [x['group_id'] for x in census['groups']]==list(range(162))
future=json.loads((HERE/'future_dependency.json').read_text());assert future['status']=='UNSATISFIED_NULL_HASH_PAIR' and future['satisfied'] is False and future['manifest_sha256'] is future['result_sha256'] is None
m=module();engine=m.load_engine();m.configure_engine(engine);ep='''ideal G=slimgb(I);
print("GROEBNER_SIZE="+string(size(G)));
poly remainder=reduce(1,G);
print("UNIT_REMAINDER="+string(remainder));
if (remainder==0) { print("STATUS=UNIT_IDEAL"); } else { print("STATUS=NONUNIT_OR_UNRESOLVED"); }
quit;
''';lanes=[]
for ordinal,gid in enumerate(range(26,76),1):
 record=census['groups'][gid];q=m.build_program(engine,tuple(record['canonical_chart']));assert q.endswith('quit;\n');q=q[:-len('quit;\n')]+ep;digest=hashlib.sha256(q.encode()).hexdigest();assert digest==record['exact_Q_source_sha256'] and len(q.encode())==record['exact_Q_source_bytes'];path=HERE/'sources'/f'rep2_group{gid:03d}_Q.sing';atomic(path,q);assert sha(path)==digest;lanes.append({'ordinal':ordinal,'group_id':gid,'canonical_chart':record['canonical_chart'],'family':record['family'],'source_path':str(path.relative_to(HERE)),'source_sha256':digest,'source_bytes':path.stat().st_size,'variables':91,'generators':6577})
ledger={'schema':'KRENN_X5_REP2_GROUPS26_75_EXACT_Q_SOURCE_LEDGER_V1','status':'PASS_REGENERATED_50_SOURCES_ZERO_SOLVES_CONDITIONAL','selection':{'required_closed_union':list(range(26)),'rule':'exact canonical group IDs 26..75 in strict ascending order','selected_group_ids':list(range(26,76))},'future_dependency':{'path':'future_dependency.json','sha256':sha(HERE/'future_dependency.json'),'satisfied':False,'hash_pair_null':True},'authoritative_census':{'path':str((BASE/'canonical_census.json').relative_to(ROOT)),'sha256':PINS[BASE/'canonical_census.json']},'lanes':lanes,'pins':{str(p.relative_to(ROOT)):h for p,h in PINS.items()},'scope':{'source_files_materialized':50,'solver_launches':0,'results_materialized':0,'clearances_materialized':0,'groups_newly_closed':0,'mathematical_coverage_added':False,'rep2_closed':False}};atomic(HERE/'source_ledger.json',json.dumps(ledger,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':ledger['status'],'selected':[26,75],'ledger_sha256':sha(HERE/'source_ledger.json'),'bytes':sum(x['source_bytes'] for x in lanes),'solver_runs':0},sort_keys=True))
