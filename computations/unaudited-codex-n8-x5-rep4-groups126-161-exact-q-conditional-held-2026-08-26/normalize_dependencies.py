#!/usr/bin/env python3
"""Create normalized three-stage dependencies and immediately replay all six files."""
import json,os
from pathlib import Path
from dependency_verifier import sha,validate_payload,verify_payload,CONTRACT_SHA
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
def main():
 contract_path=HERE/'future_dependencies.json';assert sha(contract_path)==CONTRACT_SHA;contract=json.loads(contract_path.read_text());results=[];mhs=[];rhs=[]
 for dep in contract['dependencies']:
  manifest=ROOT/dep['manifest_path'];result=ROOT/dep['result_path'];assert manifest.is_file() and result.is_file(),'HELD: all three future terminal pairs must exist';results.append(json.loads(result.read_text()));mhs.append(sha(manifest));rhs.append(sha(result))
 normalized=validate_payload(contract,results,mhs,rhs);replay=verify_payload(contract,normalized,ROOT);normalized['launch_replay_status']=replay['status'];tmp=HERE/'normalized_dependencies.json.tmp';tmp.write_text(json.dumps(normalized,indent=2,sort_keys=True)+'\n');os.replace(tmp,HERE/'normalized_dependencies.json');print(json.dumps({'status':replay['status'],'closed_union':[0,125]},sort_keys=True))
if __name__=='__main__':main()
