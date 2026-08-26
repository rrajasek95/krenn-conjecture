#!/usr/bin/env python3
import argparse,copy,json,subprocess,tempfile
from pathlib import Path
def main():
 p=argparse.ArgumentParser();p.add_argument("--validator",required=True);p.add_argument("--raw",required=True);p.add_argument("--audit",required=True);p.add_argument("--output",required=True);a=p.parse_args();r=json.load(open(a.raw));u=json.load(open(a.audit));cases={}
 def run(x,y):
  with tempfile.TemporaryDirectory() as td:
   p=Path(td);rp=p/"r.json";up=p/"u.json";rp.write_text(json.dumps(x));up.write_text(json.dumps(y));return subprocess.run(["python3",a.validator,"--raw",str(rp),"--audit",str(up)],capture_output=True).returncode
 cases["positive_control"]=(run(r,u)==0)
 muts={"false_promotion":("audit",lambda x:x.__setitem__("promotion",True)),"wrong_frontier":("raw",lambda x:x["outcomes"][0].__setitem__("frontier",1268)),"hidden_violation":("audit",lambda x:x.__setitem__("repair_violations",1)),"missing_equation":("audit",lambda x:x.__setitem__("equations_replayed",315300)),"continued":("raw",lambda x:x.__setitem__("continued_beyond_round731",True)),"candidate_mismatch":("audit",lambda x:x.__setitem__("candidate_variants_equal",False)),"rss_overrun":("raw",lambda x:x.__setitem__("peak_rss_kib",8*1024*1024)),"false_verdict":("audit",lambda x:x.__setitem__("verdict","PROMOTE"))}
 for name,(which,mut) in muts.items():x=copy.deepcopy(r);y=copy.deepcopy(u);mut(x if which=="raw" else y);cases[name]=(run(x,y)!=0)
 out={"status":"PASS" if all(cases.values()) else "FAIL","cases":cases,"fail_closed":True};Path(a.output).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n");print(json.dumps(out));raise SystemExit(0 if out["status"]=="PASS" else 1)
if __name__=="__main__":main()
