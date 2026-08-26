#!/usr/bin/env python3
"""Fail-closed future rep4 first25 adapter to exact closed union0..25."""
from __future__ import annotations
import hashlib,json,os,re
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def validate_payload(c,r,mh,rh):
 assert c['status']=='UNSATISFIED_NULL_HASH_PAIR' and c['satisfied'] is False and c['manifest_sha256'] is c['result_sha256'] is None;q=c['required'];assert r['schema']==q['result_schema'] and r['status']==q['result_status'] and r['groups_closed']==q['groups_closed']==list(range(1,26));closed=[0]+r['groups_closed'];assert closed==q['closed_union']==list(range(26)) and len(closed)==len(set(closed))==26 and re.fullmatch(r'[0-9a-f]{64}',mh) and re.fullmatch(r'[0-9a-f]{64}',rh)
 return {'schema':'KRENN_X5_REP4_FIRST25_NORMALIZED_DEPENDENCY_V1','status':'PASS_NORMALIZED_EXACT_CLOSED_UNION_0_25','dependency_manifest_path':q['manifest_path'],'dependency_result_path':q['result_path'],'dependency_manifest_sha256':mh,'dependency_result_sha256':rh,'dependency_result_schema':q['result_schema'],'dependency_result_status':q['result_status'],'groups_closed_by_future':list(range(1,26)),'baseline_closed_group':0,'closed_union':list(range(26)),'duplicates':[],'missing':[],'extra':[]}
def main():
 c=json.loads((HERE/'future_dependency.json').read_text());manifest=ROOT/c['required']['manifest_path'];rp=ROOT/c['required']['result_path'];assert manifest.is_file() and rp.is_file(),'HELD: future independent terminal files absent';mh,rh=sha(manifest),sha(rp);listed={}
 for line in manifest.read_text().splitlines():digest,name=line.split(None,1);path=(manifest.parent/name.strip()).resolve();assert path.is_file() and sha(path)==digest,name;listed[path]=digest
 assert rp.resolve() in listed and listed[rp.resolve()]==rh;n=validate_payload(c,json.loads(rp.read_text()),mh,rh);t=HERE/'normalized_dependency.json.tmp';t.write_text(json.dumps(n,indent=2,sort_keys=True)+'\n');os.replace(t,HERE/'normalized_dependency.json');print(json.dumps({'status':n['status'],'manifest_sha256':mh,'result_sha256':rh},sort_keys=True))
if __name__=='__main__':main()
