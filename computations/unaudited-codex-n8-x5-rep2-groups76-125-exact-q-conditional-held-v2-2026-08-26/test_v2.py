#!/usr/bin/env python3
"""Original dependency hostiles plus the stale/fabricated normalized hostile."""
import copy,hashlib,importlib.util,json,os
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];PROD=ROOT/'computations/unaudited-codex-n8-x5-rep2-groups76-125-exact-q-conditional-held-2026-08-26'
spec=importlib.util.spec_from_file_location('adapter',PROD/'normalize_dependencies.py');assert spec and spec.loader;adapter=importlib.util.module_from_spec(spec);spec.loader.exec_module(adapter);contract=json.loads((PROD/'future_dependencies.json').read_text());first={'schema':contract['dependencies'][0]['result_schema'],'status':contract['dependencies'][0]['result_status'],'groups_closed':list(range(1,26))};middle={'schema':contract['dependencies'][1]['result_schema'],'status':contract['dependencies'][1]['result_status'],'groups_closed':list(range(26,76))};tests={}
def reject(name,cm=None,fm=None,mm=None,mhs=None,rhs=None):
 c,f,m=copy.deepcopy(contract),copy.deepcopy(first),copy.deepcopy(middle)
 if cm:cm(c)
 if fm:fm(f)
 if mm:mm(m)
 try:adapter.validate_payload(c,f,m,mhs or ['a'*64,'b'*64],rhs or ['c'*64,'d'*64])
 except (AssertionError,KeyError,TypeError):tests[name]=True
 else:tests[name]=False
reject('null_treated_satisfied',lambda c:c.__setitem__('satisfied',True));reject('future_hash_injected',lambda c:c['dependencies'][0].__setitem__('manifest_sha256','0'*64));reject('first_wrong_schema',fm=lambda x:x.__setitem__('schema','wrong'));reject('first_wrong_status',fm=lambda x:x.__setitem__('status','wrong'));reject('first_missing',fm=lambda x:x['groups_closed'].pop());reject('first_duplicate',fm=lambda x:x['groups_closed'].__setitem__(24,24));reject('first_reordered',fm=lambda x:x['groups_closed'].reverse());reject('middle_wrong_schema',mm=lambda x:x.__setitem__('schema','wrong'));reject('middle_wrong_status',mm=lambda x:x.__setitem__('status','wrong'));reject('middle_missing',mm=lambda x:x['groups_closed'].pop());reject('middle_duplicate',mm=lambda x:x['groups_closed'].__setitem__(49,74));reject('middle_reordered',mm=lambda x:x['groups_closed'].reverse());reject('cross_overlap',mm=lambda x:x['groups_closed'].__setitem__(0,25));reject('union_extra',lambda c:c['required_closed_union'].append(76));reject('bad_manifest_hash',mhs=['a'*63,'b'*64]);reject('bad_result_hash',rhs=['c'*64,'z'*64])
assert len(tests)==16 and all(tests.values())
fabricated=adapter.validate_payload(contract,first,middle,['a'*64,'b'*64],['c'*64,'d'*64]);from dependency_verifier import verify_payload
try:verify_payload(contract,fabricated,ROOT)
except (AssertionError,FileNotFoundError):tests['fabricated_or_stale_normalized_with_absent_artifacts']=True
else:tests['fabricated_or_stale_normalized_with_absent_artifacts']=False
assert len(tests)==17 and all(tests.values());result={'schema':'KRENN_X5_REP2_GROUPS76_125_V2_HOSTILES_V1','status':'PASS_17_HOSTILES_INCLUDING_STALE_NORMALIZED_PROVENANCE','tests':tests,'producer_adapter_sha256':hashlib.sha256((PROD/'normalize_dependencies.py').read_bytes()).hexdigest(),'v2_verifier_sha256':hashlib.sha256((HERE/'dependency_verifier.py').read_bytes()).hexdigest(),'solver_runs':0};tmp=HERE/'results_hostile_tests_v2.json.tmp';tmp.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');os.replace(tmp,HERE/'results_hostile_tests_v2.json');print(json.dumps({'status':result['status'],'tests':17,'solver_runs':0},sort_keys=True))
