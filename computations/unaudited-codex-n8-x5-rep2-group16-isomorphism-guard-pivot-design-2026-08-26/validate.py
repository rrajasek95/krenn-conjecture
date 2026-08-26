#!/usr/bin/env python3
import copy,hashlib,json,re,subprocess,sys
from pathlib import Path
H=Path(__file__).resolve().parent;sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
subprocess.run([sys.executable,str(H/'analyze_and_build.py')],cwd=H,check=True,capture_output=True,text=True)
r=json.loads((H/'results_group16_design.json').read_text());assert r['status']=='PASS_NO_PREFIX_TRANSPORT_STRICT_88_6574_THREE_CHART_QUOTIENT_ZERO_SOLVES'
assert r['group16']['chart']==[0,0,0,1,'z',2,0,1] and r['group16']['termination']=='NATIVE_WALL_CAP_240' and r['group16']['mathematical_coverage'] is False
ledger=r['transport']['ledger'];assert [x['target_group_id'] for x in ledger]==list(range(17));assert all(x['color_permutations_tested']==6 for x in ledger)
assert ledger[16]['exact_occurrence_multiset_matches']==['012'] and all(not x['exact_occurrence_multiset_matches'] for x in ledger[:16]) and all(x['mismatch_witness'] for x in ledger[:16])
assert r['transport']['site_permutations_enumerated']==40320 and r['transport']['source_label_preserving_site_automorphisms']==[list(range(8))]
q=r['quotient'];assert (q['chart_count'],q['variables_each'],q['generators_each'],q['removed_variables_each'],q['removed_guards_each'],q['new_variables'])==(3,88,6574,3,3,0)
assert [x['pivot_k'] for x in q['inputs']]==[0,1,2]
for record in q['inputs']:
 p=H/record['path'];assert sha(p)==record['sha256'];text=p.read_text();ring=next(line for line in text.splitlines() if line.startswith('ring r='));variables=ring.split(',(',1)[1].rsplit('),dp;',1)[0].split(',');assert len(variables)==len(set(variables))==88
 assert all(f'a17_{i}{record["pivot_k"]}' not in text for i in range(3))
 for token in ('INPUT_VARIABLES','INPUT_GENERATORS','ideal G=slimgb(I)','UNIT_REMAINDER','STATUS=UNIT_IDEAL','STATUS=NONUNIT_OR_UNRESOLVED'):assert token in text
assert r['scope']=={'singular_runs':0,'ideal_runs':0,'mathematical_coverage':False,'group16_closed':False,'rep2_closed':False}
def valid(x):
 assert x['transport']['closed_prefix_transportable_to_group16']==[] and x['transport']['group16_covers']==[16]
 assert x['quotient']['chart_count']==3 and x['quotient']['variables_each']==88 and x['quotient']['generators_each']==6574
 assert x['quotient']['proof']['chart_union'].startswith('D(b0) union D(b1) union D(b2)')
 assert x['scope']['singular_runs']==x['scope']['ideal_runs']==0 and x['scope']['group16_closed'] is False
mutations=[]
x=copy.deepcopy(r);x['transport']['closed_prefix_transportable_to_group16']=[15];mutations.append(x)
x=copy.deepcopy(r);x['transport']['group16_covers']=[15,16];mutations.append(x)
x=copy.deepcopy(r);x['quotient']['chart_count']=2;mutations.append(x)
x=copy.deepcopy(r);x['quotient']['variables_each']=91;mutations.append(x)
x=copy.deepcopy(r);x['quotient']['generators_each']=6577;mutations.append(x)
x=copy.deepcopy(r);x['quotient']['proof']['chart_union']='one chart';mutations.append(x)
x=copy.deepcopy(r);x['scope']['group16_closed']=True;mutations.append(x)
rejected=0
for x in mutations:
 try:valid(x)
 except AssertionError:rejected+=1
assert rejected==len(mutations)==7
out={'schema':'KRENN_X5_REP2_GROUP16_DESIGN_VALIDATION_V1','status':'PASS_EXACT_NO_TRANSPORT_AND_THREE_CHART_QUOTIENT','source_comparisons':17,'color_candidates':102,'hostiles':7,'solver_runs':0,'result_sha256':sha(H/'results_group16_design.json'),'input_sha256':[x['sha256'] for x in q['inputs']]}
(H/'results_validation.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,sort_keys=True))
