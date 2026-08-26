#!/usr/bin/env python3
"""Create v2 normalized dependencies, then replay them through the launch verifier."""
from __future__ import annotations
import hashlib,importlib.util,json,os
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];PROD=ROOT/'computations/unaudited-codex-n8-x5-rep2-groups76-125-exact-q-conditional-held-2026-08-26';ADAPTER=PROD/'normalize_dependencies.py';ADAPTER_SHA='887762ea499c3dbf8b566987fe1ba234f518e72ba9733f6b96accd4435dee1fb'
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def main():
 assert sha(ADAPTER)==ADAPTER_SHA;contract=json.loads((PROD/'future_dependencies.json').read_text());spec=importlib.util.spec_from_file_location('sealed_v1_adapter',ADAPTER);assert spec and spec.loader;m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);results=[];mhs=[];rhs=[]
 for dep in contract['dependencies']:
  manifest=ROOT/dep['manifest_path'];result=ROOT/dep['result_path'];assert manifest.is_file() and result.is_file(),'HELD: both future terminal pairs must exist';results.append(json.loads(result.read_text()));mhs.append(sha(manifest));rhs.append(sha(result))
 normalized=m.validate_payload(contract,results[0],results[1],mhs,rhs);from dependency_verifier import verify_payload;replay=verify_payload(contract,normalized,ROOT);normalized['v2_replay_status']=replay['status'];tmp=HERE/'normalized_dependencies.json.tmp';tmp.write_text(json.dumps(normalized,indent=2,sort_keys=True)+'\n');os.replace(tmp,HERE/'normalized_dependencies.json');print(json.dumps({'status':replay['status'],'closed_union':[0,75]},sort_keys=True))
if __name__=='__main__':main()
