#!/usr/bin/env python3
import copy,hashlib,importlib.util,json,os
from pathlib import Path
HERE=Path(__file__).resolve().parent;s=importlib.util.spec_from_file_location('adapter',HERE/'normalize_dependency.py');assert s and s.loader;m=importlib.util.module_from_spec(s);s.loader.exec_module(m);c=json.loads((HERE/'future_dependency.json').read_text());good={'schema':c['required']['result_schema'],'status':c['required']['result_status'],'groups_closed':list(range(1,26))};tests={}
def reject(name,cm=None,rm=None,mh='a'*64,rh='b'*64):
 cc,rr=copy.deepcopy(c),copy.deepcopy(good)
 if cm:cm(cc)
 if rm:rm(rr)
 try:m.validate_payload(cc,rr,mh,rh)
 except (AssertionError,KeyError,TypeError):tests[name]=True
 else:tests[name]=False
reject('null_treated_satisfied',lambda x:x.__setitem__('satisfied',True));reject('future_hash_injected',lambda x:x.__setitem__('manifest_sha256','0'*64));reject('wrong_schema',rm=lambda x:x.__setitem__('schema','wrong'));reject('wrong_status',rm=lambda x:x.__setitem__('status','wrong'));reject('missing_group',rm=lambda x:x['groups_closed'].pop());reject('duplicate_group',rm=lambda x:x['groups_closed'].__setitem__(24,24));reject('extra_group',rm=lambda x:x['groups_closed'].append(26));reject('reordered_groups',rm=lambda x:x['groups_closed'].reverse());reject('baseline_removed',lambda x:x['required']['closed_union'].pop(0));reject('union_extra',lambda x:x['required']['closed_union'].append(26));reject('bad_manifest_hash',mh='a'*63);reject('bad_result_hash',rh='z'*64);assert len(tests)==12 and all(tests.values());r={'schema':'KRENN_X5_REP4_GROUPS26_75_DEPENDENCY_HOSTILES_V1','status':'PASS_12_HOSTILES_FUTURE_ABSENT','tests':tests,'future_dependency_sha256':hashlib.sha256((HERE/'future_dependency.json').read_bytes()).hexdigest(),'selected_group_ids':list(range(26,76)),'normalized_dependency_present':False,'solver_runs':0};t=HERE/'results_hostile_tests.json.tmp';t.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n');os.replace(t,HERE/'results_hostile_tests.json');print(json.dumps({'status':r['status'],'tests':12},sort_keys=True))
