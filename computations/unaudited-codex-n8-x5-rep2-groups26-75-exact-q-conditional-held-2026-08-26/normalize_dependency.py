#!/usr/bin/env python3
"""Fail-closed adapter from a future first25 terminal referee to closed union0..25."""
from __future__ import annotations
import hashlib,json,os,re
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];FUTURE_SHA='df9ec9aba49241c0d17853c9081917e48b134e16b51f382fee85f4f5f550651c'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def validate_payload(contract,result,manifest_sha,result_sha):
 assert contract['status']=='UNSATISFIED_NULL_HASH_PAIR' and contract['satisfied'] is False and contract['manifest_sha256'] is contract['result_sha256'] is None
 required=contract['required'];assert result['schema']==required['result_schema'] and result['status']==required['result_status'];assert result['groups_closed']==required['groups_closed']==list(range(1,26));closed=[0]+result['groups_closed'];assert closed==required['closed_union']==list(range(26)) and len(closed)==len(set(closed))==26;assert re.fullmatch(r'[0-9a-f]{64}',manifest_sha) and re.fullmatch(r'[0-9a-f]{64}',result_sha)
 return {'schema':'KRENN_X5_REP2_FIRST25_NORMALIZED_DEPENDENCY_V1','status':'PASS_NORMALIZED_EXACT_CLOSED_UNION_0_25','dependency_manifest_path':required['manifest_path'],'dependency_result_path':required['result_path'],'dependency_manifest_sha256':manifest_sha,'dependency_result_sha256':result_sha,'dependency_result_schema':required['result_schema'],'dependency_result_status':required['result_status'],'groups_closed_by_future':list(range(1,26)),'baseline_closed_group':0,'closed_union':list(range(26)),'duplicates':[],'missing':[],'extra':[]}
def main():
 assert sha(HERE/'future_dependency.json')==FUTURE_SHA;contract=json.loads((HERE/'future_dependency.json').read_text());manifest=ROOT/contract['required']['manifest_path'];result_path=ROOT/contract['required']['result_path'];assert manifest.is_file() and result_path.is_file(),'HELD: future independent terminal files absent';mh,rh=sha(manifest),sha(result_path)
 # Independently replay the terminal manifest and require the result hash is a listed member.
 listed={}
 for line in manifest.read_text().splitlines():
  digest,name=line.split(None,1);path=(manifest.parent/name.strip()).resolve();assert path.is_file() and sha(path)==digest,name;listed[path]=digest
 assert result_path.resolve() in listed and listed[result_path.resolve()]==rh
 normalized=validate_payload(contract,json.loads(result_path.read_text()),mh,rh);tmp=HERE/'normalized_dependency.json.tmp';tmp.write_text(json.dumps(normalized,indent=2,sort_keys=True)+'\n');os.replace(tmp,HERE/'normalized_dependency.json');print(json.dumps({'status':normalized['status'],'manifest_sha256':mh,'result_sha256':rh},sort_keys=True))
if __name__=='__main__':main()
