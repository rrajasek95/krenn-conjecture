#!/usr/bin/env python3
"""Twelve hostile dependency/selection tests; no future files or solves."""
import copy,hashlib,importlib.util,json,os
from pathlib import Path
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('adapter',HERE/'normalize_dependency.py');assert spec and spec.loader;m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
contract=json.loads((HERE/'future_dependency.json').read_text());good={'schema':contract['required']['result_schema'],'status':contract['required']['result_status'],'groups_closed':list(range(1,26))};tests={}
def reject(name,cm=None,rm=None,mh='a'*64,rh='b'*64):
 c,r=copy.deepcopy(contract),copy.deepcopy(good)
 if cm:cm(c)
 if rm:rm(r)
 try:m.validate_payload(c,r,mh,rh)
 except (AssertionError,KeyError,TypeError):tests[name]=True
 else:tests[name]=False
reject('null_treated_satisfied',lambda c:c.__setitem__('satisfied',True));reject('future_hash_injected',lambda c:c.__setitem__('manifest_sha256','0'*64));reject('wrong_schema',rm=lambda r:r.__setitem__('schema','wrong'));reject('wrong_status',rm=lambda r:r.__setitem__('status','wrong'));reject('missing_group',rm=lambda r:r['groups_closed'].pop());reject('duplicate_group',rm=lambda r:r['groups_closed'].__setitem__(24,24));reject('extra_group',rm=lambda r:r['groups_closed'].append(26));reject('reordered_groups',rm=lambda r:r['groups_closed'].reverse());reject('baseline_zero_removed',lambda c:c['required']['closed_union'].pop(0));reject('closed_union_extra',lambda c:c['required']['closed_union'].append(26));reject('bad_manifest_hash',mh='a'*63);reject('bad_result_hash',rh='z'*64)
assert len(tests)==12 and all(tests.values());ledger=json.loads((HERE/'source_ledger.json').read_text());assert ledger['selection']['selected_group_ids']==list(range(26,76));result={'schema':'KRENN_X5_REP2_GROUPS26_75_DEPENDENCY_HOSTILES_V1','status':'PASS_12_HOSTILES_FUTURE_ABSENT','tests':tests,'future_dependency_sha256':hashlib.sha256((HERE/'future_dependency.json').read_bytes()).hexdigest(),'selected_group_ids':list(range(26,76)),'normalized_dependency_present':False,'solver_runs':0};tmp=HERE/'results_hostile_tests.json.tmp';tmp.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');os.replace(tmp,HERE/'results_hostile_tests.json');print(json.dumps({'status':result['status'],'tests':12},sort_keys=True))
