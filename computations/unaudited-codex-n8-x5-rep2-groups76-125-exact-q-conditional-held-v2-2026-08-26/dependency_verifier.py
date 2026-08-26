#!/usr/bin/env python3
"""Exact reusable replay of both future terminal dependency pairs."""
from __future__ import annotations
import hashlib,json,re
from pathlib import Path
CONTRACT_SHA='5173f8f03b8eb7feff428573cb6a0b2813ef1e6cb1d4c4696543c30585e522e4'
def sha(path:Path)->str:return hashlib.sha256(path.read_bytes()).hexdigest()
def verify_payload(contract:dict,normalized:dict,root:Path)->dict:
 assert contract['schema']=='KRENN_X5_REP2_GROUPS76_125_FUTURE_DEPENDENCIES_V1' and contract['status']=='UNSATISFIED_BOTH_NULL_HASH_PAIRS' and contract['satisfied'] is False and contract['baseline_closed_group']==0 and contract['required_closed_union']==list(range(76))
 deps=contract['dependencies'];assert [d['name'] for d in deps]==['groups1_25','groups26_75'] and [d['groups_closed'] for d in deps]==[list(range(1,26)),list(range(26,76))]
 assert all(d['satisfied'] is False and d['manifest_sha256'] is d['result_sha256'] is None for d in deps)
 assert normalized['schema']=='KRENN_X5_REP2_GROUPS76_125_NORMALIZED_DEPENDENCIES_V1' and normalized['status']=='PASS_NORMALIZED_EXACT_CLOSED_UNION_0_75'
 assert normalized['dependency_manifest_paths']==[d['manifest_path'] for d in deps] and normalized['dependency_result_paths']==[d['result_path'] for d in deps]
 assert normalized['dependency_result_schemas']==[d['result_schema'] for d in deps] and normalized['dependency_result_statuses']==[d['result_status'] for d in deps]
 assert normalized['groups_closed_by_first']==list(range(1,26)) and normalized['groups_closed_by_middle']==list(range(26,76)) and normalized['baseline_closed_group']==0 and normalized['closed_union']==list(range(76)) and normalized['duplicates']==normalized['missing']==normalized['extra']==[]
 mhs=normalized['dependency_manifest_sha256'];rhs=normalized['dependency_result_sha256'];assert len(mhs)==len(rhs)==2 and all(re.fullmatch(r'[0-9a-f]{64}',x) for x in mhs+rhs)
 manifest_entries=[];results=[]
 for index,(dep,mh,rh) in enumerate(zip(deps,mhs,rhs)):
  manifest=root/dep['manifest_path'];result_path=root/dep['result_path'];assert manifest.is_file() and result_path.is_file(),('dependency artifact absent',index)
  assert sha(manifest)==mh and sha(result_path)==rh,('dependency top-level hash mismatch',index)
  listed={}
  for line in manifest.read_text().splitlines():
   digest,name=line.split(None,1);path=(manifest.parent/name.strip()).resolve();assert re.fullmatch(r'[0-9a-f]{64}',digest) and path.is_file() and sha(path)==digest,(index,name);listed[path]=digest
  assert result_path.resolve() in listed and listed[result_path.resolve()]==rh,('result omitted/mismatched in manifest',index)
  result=json.loads(result_path.read_text());assert result['schema']==dep['result_schema'] and result['status']==dep['result_status'] and result['groups_closed']==dep['groups_closed'],('terminal result mismatch',index)
  results.append(result);manifest_entries.append(len(listed))
 closed=[0]+results[0]['groups_closed']+results[1]['groups_closed'];assert closed==list(range(76)) and len(closed)==len(set(closed))==76
 return {'status':'PASS_REPLAYED_ALL_FOUR_DEPENDENCY_ARTIFACTS_EXACT_UNION_0_75','dependency_pairs':2,'manifest_entries':manifest_entries,'manifest_sha256':mhs,'result_sha256':rhs,'closed_union':closed}
def verify_files(contract_path:Path,normalized_path:Path,root:Path)->dict:
 assert sha(contract_path)==CONTRACT_SHA
 return verify_payload(json.loads(contract_path.read_text()),json.loads(normalized_path.read_text()),root)
