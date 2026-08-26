#!/usr/bin/env python3
"""Regenerate conditional rep4 groups26..75 from authoritative census; no solve."""
from __future__ import annotations
import hashlib,importlib.util,json,os
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];BASE=ROOT/'computations/unaudited-codex-n8-x5-rep4-first25-exact-q-held-2026-08-26';DESIGN=ROOT/'computations/unaudited-codex-n8-x5-rep4-guard-minor-contraction-design-2026-08-25'
PINS={BASE/'MANIFEST.sha256':'d6c098fb885ad9faac566b6f01a9e94f01aa6a8b4a61562ec4fa14f66b44a029',BASE/'canonical_census.json':'12773aacfd9fa702ce4202a5da64c356d0451be8b904ebcf9848bcbf99913261',BASE/'source_ledger.json':'59cbe8e6464be1774bbf9310cacae4ef4c9cf076f6185926716881b376718587',DESIGN/'MANIFEST.sha256':'7f47c0567580aba565925b95860bace46ebaf5703aace4ec8aa100f48ec33e02',DESIGN/'generate_design.py':'b83218b25635efe8c46ff2faf9e2028921408d884be7fb2e4d8541ccdf9c847a'}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def atomic(p,text):t=p.with_suffix(p.suffix+'.tmp');t.write_text(text);os.replace(t,p)
def module():s=importlib.util.spec_from_file_location('sealed_rep4_design',DESIGN/'generate_design.py');assert s and s.loader;m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
for p,h in PINS.items():assert sha(p)==h,(p,sha(p),h)
census=json.loads((BASE/'canonical_census.json').read_text());future=json.loads((HERE/'future_dependency.json').read_text());assert census['status']=='PASS_REGENERATED_AUTHORITATIVE_972_TO_162_CENSUS' and census['closed_group_identification']['group_id']==0 and [x['group_id'] for x in census['groups']]==list(range(162));assert future['status']=='UNSATISFIED_NULL_HASH_PAIR' and future['satisfied'] is False and future['manifest_sha256'] is future['result_sha256'] is None
m=module();ep='''ideal G=slimgb(I);
print("GROEBNER_SIZE="+string(size(G)));
poly remainder=reduce(1,G);
print("UNIT_REMAINDER="+string(remainder));
if (remainder==0) { print("STATUS=UNIT_IDEAL"); } else { print("STATUS=NONUNIT_OR_UNRESOLVED"); }
quit;
''';lanes=[]
for ordinal,gid in enumerate(range(26,76),1):
 record=census['groups'][gid];q=m.build_program(tuple(record['canonical_chart']));assert q.endswith('quit;\n');q=q[:-len('quit;\n')]+ep;digest=hashlib.sha256(q.encode()).hexdigest();assert digest==record['exact_Q_source_sha256'] and len(q.encode())==record['exact_Q_source_bytes'];path=HERE/'sources'/f'rep4_group{gid:03d}_Q.sing';atomic(path,q);assert sha(path)==digest;lanes.append({'ordinal':ordinal,'group_id':gid,'canonical_chart':record['canonical_chart'],'family':record['family'],'source_path':str(path.relative_to(HERE)),'source_sha256':digest,'source_bytes':path.stat().st_size,'variables':91,'generators':6577})
ledger={'schema':'KRENN_X5_REP4_GROUPS26_75_EXACT_Q_SOURCE_LEDGER_V1','status':'PASS_REGENERATED_50_SOURCES_ZERO_SOLVES_CONDITIONAL','selection':{'required_closed_union':list(range(26)),'rule':'exact canonical group IDs 26..75 in strict ascending order','selected_group_ids':list(range(26,76))},'future_dependency':{'path':'future_dependency.json','sha256':sha(HERE/'future_dependency.json'),'satisfied':False,'hash_pair_null':True},'authoritative_census':{'path':str((BASE/'canonical_census.json').relative_to(ROOT)),'sha256':PINS[BASE/'canonical_census.json']},'lanes':lanes,'pins':{str(p.relative_to(ROOT)):h for p,h in PINS.items()},'scope':{'source_files_materialized':50,'solver_launches':0,'results_materialized':0,'clearances_materialized':0,'groups_newly_closed':0,'mathematical_coverage_added':False,'rep4_closed':False}};atomic(HERE/'source_ledger.json',json.dumps(ledger,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':ledger['status'],'selected':[26,75],'ledger_sha256':sha(HERE/'source_ledger.json'),'bytes':sum(x['source_bytes'] for x in lanes),'solver_runs':0},sort_keys=True))
