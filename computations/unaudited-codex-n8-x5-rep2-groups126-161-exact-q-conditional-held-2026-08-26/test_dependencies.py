#!/usr/bin/env python3
"""Twenty-one dependency hostiles including fabricated/stale normalized provenance."""
import copy,hashlib,json,os
from pathlib import Path
from dependency_verifier import validate_payload,verify_payload
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];contract=json.loads((HERE/'future_dependencies.json').read_text());good=[{'schema':d['result_schema'],'status':d['result_status'],'groups_closed':list(d['groups_closed'])} for d in contract['dependencies']];tests={}
def reject(name,cm=None,rm=None,mhs=None,rhs=None):
 c,r=copy.deepcopy(contract),copy.deepcopy(good)
 if cm:cm(c)
 if rm:rm(r)
 try:validate_payload(c,r,mhs or ['a'*64,'b'*64,'c'*64],rhs or ['d'*64,'e'*64,'f'*64])
 except (AssertionError,KeyError,TypeError):tests[name]=True
 else:tests[name]=False
reject('null_treated_satisfied',lambda c:c.__setitem__('satisfied',True));reject('future_hash_injected',lambda c:c['dependencies'][0].__setitem__('manifest_sha256','0'*64));reject('dependency_order_swapped',lambda c:c['dependencies'].reverse());reject('first_wrong_schema',rm=lambda r:r[0].__setitem__('schema','wrong'));reject('first_missing',rm=lambda r:r[0]['groups_closed'].pop());reject('first_duplicate',rm=lambda r:r[0]['groups_closed'].__setitem__(24,24));reject('middle_wrong_status',rm=lambda r:r[1].__setitem__('status','wrong'));reject('middle_missing',rm=lambda r:r[1]['groups_closed'].pop());reject('middle_duplicate',rm=lambda r:r[1]['groups_closed'].__setitem__(49,74));reject('middle_reordered',rm=lambda r:r[1]['groups_closed'].reverse());reject('third_wrong_schema',rm=lambda r:r[2].__setitem__('schema','wrong'));reject('third_wrong_status',rm=lambda r:r[2].__setitem__('status','wrong'));reject('third_missing',rm=lambda r:r[2]['groups_closed'].pop());reject('third_duplicate',rm=lambda r:r[2]['groups_closed'].__setitem__(49,124));reject('third_reordered',rm=lambda r:r[2]['groups_closed'].reverse());reject('cross_first_middle_overlap',rm=lambda r:r[1]['groups_closed'].__setitem__(0,25));reject('cross_middle_third_overlap',rm=lambda r:r[2]['groups_closed'].__setitem__(0,75));reject('union_extra',lambda c:c['required_closed_union'].append(126));reject('bad_manifest_hash',mhs=['a'*63,'b'*64,'c'*64]);reject('bad_result_hash',rhs=['d'*64,'e'*64,'z'*64]);assert len(tests)==20 and all(tests.values())
fabricated=validate_payload(contract,good,['a'*64,'b'*64,'c'*64],['d'*64,'e'*64,'f'*64])
try:verify_payload(contract,fabricated,ROOT)
except (AssertionError,FileNotFoundError):tests['fabricated_or_stale_normalized_all_six_artifacts_absent']=True
else:tests['fabricated_or_stale_normalized_all_six_artifacts_absent']=False
assert len(tests)==21 and all(tests.values());result={'schema':'KRENN_X5_REP2_GROUPS126_161_DEPENDENCY_HOSTILES_V1','status':'PASS_21_HOSTILES_ALL_THREE_FUTURES_ABSENT','tests':tests,'future_dependencies_sha256':hashlib.sha256((HERE/'future_dependencies.json').read_bytes()).hexdigest(),'selected_group_ids':list(range(126,162)),'normalized_dependencies_present':False,'solver_runs':0};tmp=HERE/'results_hostile_tests.json.tmp';tmp.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');os.replace(tmp,HERE/'results_hostile_tests.json');print(json.dumps({'status':result['status'],'tests':21,'solver_runs':0},sort_keys=True))
