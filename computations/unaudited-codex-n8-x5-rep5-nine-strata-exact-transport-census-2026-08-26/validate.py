#!/usr/bin/env python3
"""Independent structural validation; no CAS."""
import copy,hashlib,json,subprocess,sys
from pathlib import Path
H=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
subprocess.run([sys.executable,str(H/'analyze_transport.py')],cwd=H,check=True,capture_output=True,text=True)
r=json.loads((H/'results_transport_partition.json').read_text())
assert r['status']=='PASS_EXACT_PARTITION_NINE_SINGLETONS_NO_CROSS_STRATUM_TRANSPORT'
names=list(r['pins']['source_sha256'])
assert len(names)==9 and sorted(r['exact_transport_classes'])==sorted([[name] for name in names])
assert r['required_representative_count']==9 and r['required_open84_representatives']==6 and r['required_complement86_representatives']==3
assert len(r['pair_ledger'])==81 and sum(x['color_permutations_tested'] for x in r['pair_ledger'])==270
positives=[x for x in r['pair_ledger'] if x['full_generator_mapping_verified']]
assert len(positives)==9 and all(x['source']==x['target'] and x['exact_occurrence_multiset_matches']==['012'] for x in positives)
assert all(x['first_exact_mismatch_witness'] is not None for x in r['pair_ledger'] if x['same_ring_and_generator_counts'] and not x['full_generator_mapping_verified'])
assert r['allowed_action']['site_permutations_enumerated']==40320 and r['allowed_action']['source_label_preserving_site_automorphisms']==[list(range(8))]
assert r['selected_k2_t1_transport']['covers']==['rep5_p00_guardpivot_k2_rank2_t1_Q.sing'] and len(r['selected_k2_t1_transport']['does_not_cover'])==8
assert r['scope']=={'design_only':True,'singular_runs':0,'ideal_runs':0,'mathematical_coverage':False,'rep5_closed':False}
def valid(x):
 assert x['required_representative_count']==len(x['exact_transport_classes'])==9
 assert all(len(c)==1 for c in x['exact_transport_classes'])
 assert sorted(v for c in x['exact_transport_classes'] for v in c)==sorted(names)
 assert x['selected_k2_t1_transport']['covers']==['rep5_p00_guardpivot_k2_rank2_t1_Q.sing']
 assert x['branch_invariant']['cross_branch_transport'] is False
 assert x['allowed_action']['source_label_preserving_site_automorphisms']==[list(range(8))]
 assert x['scope']['singular_runs']==x['scope']['ideal_runs']==0 and x['scope']['rep5_closed'] is False
mutations=[]
x=copy.deepcopy(r);x['required_representative_count']=8;mutations.append(x)
x=copy.deepcopy(r);x['exact_transport_classes'][0]+=x['exact_transport_classes'].pop();mutations.append(x)
x=copy.deepcopy(r);x['exact_transport_classes'].pop();mutations.append(x)
x=copy.deepcopy(r);x['selected_k2_t1_transport']['covers'].append(names[0]);mutations.append(x)
x=copy.deepcopy(r);x['branch_invariant']['cross_branch_transport']=True;mutations.append(x)
x=copy.deepcopy(r);x['allowed_action']['source_label_preserving_site_automorphisms'].append([1,0,2,3,4,5,6,7]);mutations.append(x)
x=copy.deepcopy(r);x['scope']['rep5_closed']=True;mutations.append(x)
rejected=0
for x in mutations:
 try:valid(x)
 except AssertionError:rejected+=1
assert rejected==len(mutations)==7
out={'schema':'KRENN_X5_REP5_NINE_STRATA_TRANSPORT_VALIDATION_V1','status':'PASS_EXACT_SINGLETON_PARTITION','pair_records':81,'permutation_candidates_same_shape':270,'positive_full_generator_maps':9,'hostiles':7,'solver_runs':0,'result_sha256':sha(H/'results_transport_partition.json')}
(H/'results_validation.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps(out,sort_keys=True))
