#!/usr/bin/env python3
"""Hostile semantic mutations for the cap/eviction result contract."""
import argparse,copy,json,subprocess,tempfile
from pathlib import Path
def main():
 p=argparse.ArgumentParser();p.add_argument("--audit",required=True);p.add_argument("--results",required=True);p.add_argument("--binary",required=True);p.add_argument("--checkpoint",required=True);p.add_argument("--output",required=True);a=p.parse_args();base=json.load(open(a.results));cases={}
 def run(r):
  with tempfile.TemporaryDirectory() as td:
   q=Path(td)/"r.json";q.write_text(json.dumps(r));return subprocess.run(["python3",a.audit,"--results",str(q),"--binary",a.binary,"--checkpoint",a.checkpoint],capture_output=True).returncode
 cases["positive_control"]=(run(base)==0)
 mutations={
  "missing_run":lambda r:r["runs"].pop(),
  "wrong_digest":lambda r:r["runs"][1].__setitem__("sorted_sha256","0"*64),
  "cap_overflow":lambda r:r["runs"][1].__setitem__("memo_entries",100001),
  "wrong_hit_count":lambda r:r["runs"][1].__setitem__("hits",1),
  "wrong_input_hash":lambda r:r.__setitem__("checkpoint_sha256","f"*64),
  "broad_authorization":lambda r:r["promotion_contract"].__setitem__("broad_run_authorized",True),
  "weakened_probe":lambda r:r["promotion_contract"].__setitem__("minimum_probe_hit_rate",0.0),
  "extra_top_field":lambda r:r.__setitem__("unsealed",True),
 }
 for name,mut in mutations.items():r=copy.deepcopy(base);mut(r);cases[name]=(run(r)!=0)
 out={"status":"PASS" if all(cases.values()) else "FAIL","cases":cases,"fail_closed":True};Path(a.output).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n");print(json.dumps(out));raise SystemExit(0 if out["status"]=="PASS" else 1)
if __name__=="__main__":main()
