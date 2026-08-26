#!/usr/bin/env python3
"""Exact normalization and launch-time replay for all three dependency pairs."""
from __future__ import annotations
import hashlib,json,re
from pathlib import Path
CONTRACT_SHA='3b61f3d0f19eb2d31fa590f07559c14d64b776a1f744cfe747b2f06de0160a39'
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def validate_payload(contract,results,manifest_hashes,result_hashes):
 assert contract['schema']=='KRENN_X5_REP4_GROUPS126_161_FUTURE_DEPENDENCIES_V1' and contract['status']=='UNSATISFIED_THREE_NULL_HASH_PAIRS' and contract['satisfied'] is False and contract['baseline_closed_group']==0 and contract['required_closed_union']==list(range(126))
 deps=contract['dependencies'];assert len(deps)==len(results)==len(manifest_hashes)==len(result_hashes)==3 and [d['name'] for d in deps]==['groups1_25','groups26_75','groups76_125']
 assert [d['groups_closed'] for d in deps]==[list(range(1,26)),list(range(26,76)),list(range(76,126))] and all(d['satisfied'] is False and d['manifest_sha256'] is d['result_sha256'] is None for d in deps)
 for dep,result,mh,rh in zip(deps,results,manifest_hashes,result_hashes):
  assert result['schema']==dep['result_schema'] and result['status']==dep['result_status'] and result['groups_closed']==dep['groups_closed'] and re.fullmatch(r'[0-9a-f]{64}',mh) and re.fullmatch(r'[0-9a-f]{64}',rh)
 closed=[0]+sum((r['groups_closed'] for r in results),[]);assert closed==list(range(126)) and len(closed)==len(set(closed))==126
 return {'schema':'KRENN_X5_REP4_GROUPS126_161_NORMALIZED_DEPENDENCIES_V1','status':'PASS_NORMALIZED_EXACT_CLOSED_UNION_0_125','dependency_manifest_paths':[d['manifest_path'] for d in deps],'dependency_result_paths':[d['result_path'] for d in deps],'dependency_manifest_sha256':manifest_hashes,'dependency_result_sha256':result_hashes,'dependency_result_schemas':[d['result_schema'] for d in deps],'dependency_result_statuses':[d['result_status'] for d in deps],'groups_closed_by_first':list(range(1,26)),'groups_closed_by_middle':list(range(26,76)),'groups_closed_by_third':list(range(76,126)),'baseline_closed_group':0,'closed_union':closed,'duplicates':[],'missing':[],'extra':[]}
def verify_payload(contract,normalized,root):
 assert normalized['schema']=='KRENN_X5_REP4_GROUPS126_161_NORMALIZED_DEPENDENCIES_V1' and normalized['status']=='PASS_NORMALIZED_EXACT_CLOSED_UNION_0_125' and normalized['closed_union']==list(range(126)) and normalized['groups_closed_by_first']==list(range(1,26)) and normalized['groups_closed_by_middle']==list(range(26,76)) and normalized['groups_closed_by_third']==list(range(76,126)) and normalized['duplicates']==normalized['missing']==normalized['extra']==[]
 deps=contract['dependencies'];assert normalized['dependency_manifest_paths']==[d['manifest_path'] for d in deps] and normalized['dependency_result_paths']==[d['result_path'] for d in deps] and normalized['dependency_result_schemas']==[d['result_schema'] for d in deps] and normalized['dependency_result_statuses']==[d['result_status'] for d in deps]
 mhs=normalized['dependency_manifest_sha256'];rhs=normalized['dependency_result_sha256'];assert len(mhs)==len(rhs)==3 and all(re.fullmatch(r'[0-9a-f]{64}',x) for x in mhs+rhs);results=[];entry_counts=[]
 for index,(dep,mh,rh) in enumerate(zip(deps,mhs,rhs)):
  manifest=root/dep['manifest_path'];result_path=root/dep['result_path'];assert manifest.is_file() and result_path.is_file(),('dependency artifact absent',index);assert sha(manifest)==mh and sha(result_path)==rh,('top-level hash mismatch',index);listed={}
  for line in manifest.read_text().splitlines():digest,name=line.split(None,1);path=(manifest.parent/name.strip()).resolve();assert re.fullmatch(r'[0-9a-f]{64}',digest) and path.is_file() and sha(path)==digest,(index,name);listed[path]=digest
  assert result_path.resolve() in listed and listed[result_path.resolve()]==rh,('result omitted/mismatched in manifest',index);result=json.loads(result_path.read_text());assert result['schema']==dep['result_schema'] and result['status']==dep['result_status'] and result['groups_closed']==dep['groups_closed'],('terminal result mismatch',index);results.append(result);entry_counts.append(len(listed))
 replayed=validate_payload(contract,results,mhs,rhs);assert replayed['closed_union']==normalized['closed_union']
 return {'status':'PASS_REPLAYED_ALL_SIX_DEPENDENCY_ARTIFACTS_EXACT_UNION_0_125','dependency_pairs':3,'manifest_entries':entry_counts,'closed_union':list(range(126))}
def verify_files(contract_path,normalized_path,root):assert sha(contract_path)==CONTRACT_SHA;return verify_payload(json.loads(contract_path.read_text()),json.loads(normalized_path.read_text()),root)
