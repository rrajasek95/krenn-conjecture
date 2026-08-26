#!/usr/bin/env python3
"""Mutate accepted semantic fields and require the independent audit to reject."""
import argparse, copy, json, subprocess, tempfile
from pathlib import Path

def main():
    p=argparse.ArgumentParser();p.add_argument("--audit",required=True);p.add_argument("--results",required=True);p.add_argument("--hostiles",required=True);p.add_argument("--binary",required=True);p.add_argument("--checkpoint",required=True);p.add_argument("--output",required=True);a=p.parse_args()
    base=json.load(open(a.results));cases={}
    def run(value):
      with tempfile.TemporaryDirectory() as td:
        q=Path(td)/"r.json";q.write_text(json.dumps(value));
        return subprocess.run(["python3",a.audit,"--results",str(q),"--hostiles",a.hostiles,"--binary",a.binary,"--checkpoint",a.checkpoint],capture_output=True).returncode
    cases["positive_control"]=(run(base)==0)
    mutations={
      "missing_run":lambda r:r["dedup_runs"].pop(),
      "wrong_digest":lambda r:r["dedup_runs"][1].__setitem__("sorted_sha256","0"*64),
      "wrong_count":lambda r:r["dedup_runs"][0].__setitem__("output_count",1),
      "wrong_input_hash":lambda r:r["checkpoint"].__setitem__("sha256","0"*64),
      "broad_authorization":lambda r:r["promotion_rule"].__setitem__("broad_run_authorized",True),
      "wrong_canonical_digest":lambda r:r["canonicalization"]["runs"][1].__setitem__("sorted_sha256","f"*64),
      "extra_top_field":lambda r:r.__setitem__("unsealed",True),
    }
    for name,mutation in mutations.items():
      r=copy.deepcopy(base);mutation(r);cases[name]=(run(r)!=0)
    result={"status":"PASS" if all(cases.values()) else "FAIL","cases":cases,"fail_closed":True};Path(a.output).write_text(json.dumps(result,indent=2,sort_keys=True)+"\n");print(json.dumps(result));raise SystemExit(0 if result["status"]=="PASS" else 1)
if __name__=="__main__":main()
