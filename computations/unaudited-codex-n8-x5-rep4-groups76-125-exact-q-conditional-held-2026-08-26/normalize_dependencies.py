#!/usr/bin/env python3
"""Fail-closed adapter from future rep4 groups1..25 and26..75 terminal seals."""
from __future__ import annotations
import hashlib,json,os,re
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];FUTURE_SHA='02e042533a68fb7a9a08d230caa7de915c3176e4d7e54b8f68a9704da7e6916e'
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def validate_payload(contract,first,middle,manifest_hashes,result_hashes):
 assert contract['status']=='UNSATISFIED_BOTH_NULL_HASH_PAIRS' and contract['satisfied'] is False and contract['baseline_closed_group']==0
 deps=contract['dependencies'];assert len(deps)==2 and [d['name'] for d in deps]==['groups1_25','groups26_75']
 assert all(d['satisfied'] is False and d['manifest_sha256'] is d['result_sha256'] is None for d in deps)
 for dep,result,mh,rh in zip(deps,[first,middle],manifest_hashes,result_hashes):
  assert result['schema']==dep['result_schema'] and result['status']==dep['result_status'] and result['groups_closed']==dep['groups_closed']
  assert re.fullmatch(r'[0-9a-f]{64}',mh) and re.fullmatch(r'[0-9a-f]{64}',rh)
 closed=[0]+first['groups_closed']+middle['groups_closed'];assert closed==contract['required_closed_union']==list(range(76)) and len(closed)==len(set(closed))==76
 return {'schema':'KRENN_X5_REP4_GROUPS76_125_NORMALIZED_DEPENDENCIES_V1','status':'PASS_NORMALIZED_EXACT_CLOSED_UNION_0_75','dependency_manifest_paths':[d['manifest_path'] for d in deps],'dependency_result_paths':[d['result_path'] for d in deps],'dependency_manifest_sha256':manifest_hashes,'dependency_result_sha256':result_hashes,'dependency_result_schemas':[d['result_schema'] for d in deps],'dependency_result_statuses':[d['result_status'] for d in deps],'groups_closed_by_first':list(range(1,26)),'groups_closed_by_middle':list(range(26,76)),'baseline_closed_group':0,'closed_union':list(range(76)),'duplicates':[],'missing':[],'extra':[]}
def main():
 assert sha(HERE/'future_dependencies.json')==FUTURE_SHA;contract=json.loads((HERE/'future_dependencies.json').read_text());results=[];mhs=[];rhs=[]
 for dep in contract['dependencies']:
  manifest=ROOT/dep['manifest_path'];result_path=ROOT/dep['result_path'];assert manifest.is_file() and result_path.is_file(),'HELD: both future independent terminal pairs must exist'
  listed={}
  for line in manifest.read_text().splitlines():
   digest,name=line.split(None,1);path=(manifest.parent/name.strip()).resolve();assert path.is_file() and sha(path)==digest,name;listed[path]=digest
  rh=sha(result_path);assert result_path.resolve() in listed and listed[result_path.resolve()]==rh
  results.append(json.loads(result_path.read_text()));mhs.append(sha(manifest));rhs.append(rh)
 normalized=validate_payload(contract,results[0],results[1],mhs,rhs);tmp=HERE/'normalized_dependencies.json.tmp';tmp.write_text(json.dumps(normalized,indent=2,sort_keys=True)+'\n');os.replace(tmp,HERE/'normalized_dependencies.json');print(json.dumps({'status':normalized['status'],'manifest_sha256':mhs,'result_sha256':rhs},sort_keys=True))
if __name__=='__main__':main()
