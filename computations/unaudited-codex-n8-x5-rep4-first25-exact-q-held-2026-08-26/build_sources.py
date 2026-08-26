#!/usr/bin/env python3
"""Regenerate authoritative rep4 census and first strict exact-Q batch; never solve."""
from __future__ import annotations
import hashlib,importlib.util,json,os
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
DESIGN=ROOT/'computations/unaudited-codex-n8-x5-rep4-guard-minor-contraction-design-2026-08-25';DESIGN_REF=ROOT/'computations/unaudited-codex-n8-x5-rep4-guard-minor-contraction-referee-2026-08-25';CLOSED=ROOT/'computations/unaudited-codex-n8-x5-rep4-all-equal-y-exact-q-held-plan-2026-08-25';FIRST_REF=ROOT/'computations/unaudited-codex-n8-x5-rep4-all-equal-y-exact-q-terminal-referee-2026-08-25';SECOND_REF=ROOT/'computations/unaudited-codex-n8-x5-rep4-all-equal-y-exact-q-terminal-second-referee-2026-08-25'
PINS={DESIGN/'MANIFEST.sha256':'7f47c0567580aba565925b95860bace46ebaf5703aace4ec8aa100f48ec33e02',DESIGN/'generate_design.py':'b83218b25635efe8c46ff2faf9e2028921408d884be7fb2e4d8541ccdf9c847a',DESIGN/'chart_orbit_ledger.json':'dac85725f217b45cbaae7b9b434640309cc5ed6e0b40e846534c8a26409bd4d8',DESIGN/'results_rep4_contraction_design.json':'7e96874cca1afaaa377aa3001d8e00b73ed4fe9322381ec269c4a46b9144bf0c',DESIGN_REF/'FINAL_MANIFEST.sha256':'185b51b8107d5dcf12e7194a7d806157e0df6a2b6d047cf4adc6c8ac400fa4ae',DESIGN_REF/'results_referee.json':'279565e76618b8fa8c4eb08f513f8109a018d23ed1e9fe11acb0489dd82bb863',CLOSED/'TERMINAL_MANIFEST.sha256':'ff3178d7b546d4afadeeb8659001685d7d5bd3bb78c73b06b33ed539184e6d5d',CLOSED/'rep4_all_equal_y_exact_Q.sing':'c90c69b11ca931677bc1de138bdfc8c1eb7618d5aee20744764e4a4b1b511019',FIRST_REF/'FINAL_MANIFEST.sha256':'a8280c98344eb62f6df89ffec125e6cdba33a7dae63f47061c71114f7aabe805',FIRST_REF/'results_referee.json':'ccc22fe2ec3d5db1d3ed3d175e5196819efa3e412cf632ef8c862ae70f3b72d3',SECOND_REF/'FINAL_MANIFEST.sha256':'b2a543e59df1edf32df414f44938b418e35ea4ed258354642aff3d2b45e522b4',SECOND_REF/'results_second_referee.json':'4e38098b41a4b4fb16eb443e56f4b6ca6de6edbd390eec9df464b0147e1c21f1'}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def atomic(p,text):t=p.with_suffix(p.suffix+'.tmp');t.write_text(text);os.replace(t,p)
def load():
 spec=importlib.util.spec_from_file_location('sealed_rep4_design',DESIGN/'generate_design.py');assert spec and spec.loader;m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
for p,h in PINS.items():assert sha(p)==h,(p,sha(p),h)
design=json.loads((DESIGN/'results_rep4_contraction_design.json').read_text());dref=json.loads((DESIGN_REF/'results_referee.json').read_text());first=json.loads((FIRST_REF/'results_referee.json').read_text());second=json.loads((SECOND_REF/'results_second_referee.json').read_text())
assert design['status']=='PASS_STRICT_SMALLER_EXACT_DESIGN_NO_IDEAL_RUN' and design['chart_census']=={'raw':972,'S3_orbits':162,'orbit_size':6,'y_orbits':81,'z_orbits':81}
assert dref['status']=='PASS_STRICT_SMALLER_EXACT_DESIGN_NO_RUN_NO_CLOSURE' and dref['producer_manifest_sha256']==PINS[DESIGN/'MANIFEST.sha256']
assert first['status']=='PASS_EXACT_Q_UNIT_IDEAL_REP4_ALL_EQUAL_Y_SAME_CHART' and first['source_sha256']==PINS[CLOSED/'rep4_all_equal_y_exact_Q.sing']
assert second['status']=='PASS_EXACT_Q_STRONG_UNIT_IDEAL_ONE_REP4_CHART_ONLY' and second['source_sha256']==first['source_sha256']
m=load();raw,groups=m.orbit_ledger();ordered=sorted(groups.items());sealed=json.loads((DESIGN/'chart_orbit_ledger.json').read_text());assert len(raw)==972 and len(ordered)==162 and sealed['raw']==972
assert [list(rep) for rep,_ in ordered]==[x['representative'] for x in sealed['groups']]
assert [[list(v) for v in sorted(ms)] for _,ms in ordered]==[x['members'] for x in sealed['groups']]
epilogue='''ideal G=slimgb(I);
print("GROEBNER_SIZE="+string(size(G)));
poly remainder=reduce(1,G);
print("UNIT_REMAINDER="+string(remainder));
if (remainder==0) { print("STATUS=UNIT_IDEAL"); } else { print("STATUS=NONUNIT_OR_UNRESOLVED"); }
quit;
'''
census=[]
for gid,(rep,members) in enumerate(ordered):
 q=m.build_program(rep);assert q.endswith('quit;\n') and q.count('quit;')==1;q=q[:-len('quit;\n')]+epilogue
 census.append({'group_id':gid,'canonical_chart':list(rep),'family':rep[4],'raw_members':[list(x) for x in sorted(members)],'raw_member_count':len(members),'exact_Q_source_sha256':hashlib.sha256(q.encode()).hexdigest(),'exact_Q_source_bytes':len(q.encode())})
matches=[x for x in census if x['exact_Q_source_sha256']==second['source_sha256']];assert len(matches)==1 and matches[0]['group_id']==0 and matches[0]['canonical_chart']==[0,0,0,0,'y',0,0,1]
selected=[x for x in census if x['group_id']!=0][:25];assert [x['group_id'] for x in selected]==list(range(1,26));lanes=[]
for ordinal,x in enumerate(selected,1):
 q=m.build_program(tuple(x['canonical_chart']));q=q[:-len('quit;\n')]+epilogue;path=HERE/'sources'/f'rep4_group{x["group_id"]:03d}_Q.sing';atomic(path,q);assert sha(path)==x['exact_Q_source_sha256'] and path.stat().st_size==x['exact_Q_source_bytes'];assert q.count('ring r=0,')==q.count('ideal G=slimgb(I);')==q.count('poly remainder=reduce(1,G);')==q.count('quit;')==1
 lanes.append({'ordinal':ordinal,'group_id':x['group_id'],'canonical_chart':x['canonical_chart'],'family':x['family'],'source_path':str(path.relative_to(HERE)),'source_sha256':sha(path),'source_bytes':path.stat().st_size,'variables':91,'generators':6577})
census_result={'schema':'KRENN_X5_REP4_CANONICAL_162_CENSUS_V1','status':'PASS_REGENERATED_AUTHORITATIVE_972_TO_162_CENSUS','counts':{'raw':972,'canonical_groups':162,'members_each':6,'y_groups':81,'z_groups':81},'closed_group_identification':{'group_id':0,'method':'unique exact-Q source SHA match to independently sealed all-equal-y chart','chart':matches[0]['canonical_chart'],'source_sha256':matches[0]['exact_Q_source_sha256'],'terminal_manifest_sha256':PINS[CLOSED/'TERMINAL_MANIFEST.sha256'],'first_referee_manifest_sha256':PINS[FIRST_REF/'FINAL_MANIFEST.sha256'],'second_referee_manifest_sha256':PINS[SECOND_REF/'FINAL_MANIFEST.sha256']},'groups':census};atomic(HERE/'canonical_census.json',json.dumps(census_result,indent=2,sort_keys=True)+'\n')
ledger={'schema':'KRENN_X5_REP4_FIRST25_EXACT_Q_SOURCE_LEDGER_V1','status':'PASS_REGENERATED_SOURCES_ZERO_SOLVES','selection':{'excluded_proven_group_ids':[0],'rule':'25 lowest canonical group IDs after excluding exactly the sealed all-equal-y group','selected_group_ids':list(range(1,26))},'closed_dependency':census_result['closed_group_identification'],'lanes':lanes,'canonical_census':{'path':'canonical_census.json','sha256':sha(HERE/'canonical_census.json')},'pins':{str(p.relative_to(ROOT)):h for p,h in PINS.items()},'scope':{'source_files_materialized':25,'solver_launches':0,'results_materialized':0,'clearances_materialized':0,'mathematical_coverage_added':False,'rep4_closed':False}};atomic(HERE/'source_ledger.json',json.dumps(ledger,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':ledger['status'],'closed_group':0,'selected':list(range(1,26)),'census_sha256':sha(HERE/'canonical_census.json'),'ledger_sha256':sha(HERE/'source_ledger.json'),'bytes':sum(x['source_bytes'] for x in lanes)},sort_keys=True))
