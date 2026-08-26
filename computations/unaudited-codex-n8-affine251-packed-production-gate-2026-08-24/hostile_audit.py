#!/usr/bin/env python3
"""Require the equivalence audit to reject scope/result mutations."""
import argparse,copy,json,subprocess,tempfile
from pathlib import Path
def main():
 p=argparse.ArgumentParser();p.add_argument("--audit",required=True);p.add_argument("--d10",required=True);p.add_argument("--d11",required=True);p.add_argument("--output",required=True);p.add_argument("audit_args",nargs=argparse.REMAINDER);a=p.parse_args();base10=json.load(open(a.d10));base11=json.load(open(a.d11));cases={}
 def run(r10,r11,swap=False):
  with tempfile.TemporaryDirectory() as td:
   x=Path(td)/"d10.json";y=Path(td)/"d11.json";x.write_text(json.dumps(r10));y.write_text(json.dumps(r11));tail=a.audit_args[1:] if a.audit_args and a.audit_args[0]=="--" else a.audit_args;args=["python3",a.audit]+tail
   args[args.index(a.d10)]=str(x);args[args.index(a.d11)]=str(y)
   if swap:
    i=args.index("--d11-closure");j=args.index("--d11-interrupted");args[i+1],args[j+1]=args[j+1],args[i+1]
   return subprocess.run(args,capture_output=True).returncode
 cases["positive_control"]=(run(base10,base11)==0)
 mutations={
  "d10_wrong_count":("d10",lambda r:r.__setitem__("row_orbits",1)),
  "d10_nonterminal":("d10",lambda r:r.__setitem__("status","INCOMPLETE_RESOURCE_GATE")),
  "d11_false_terminal":("d11",lambda r:r.__setitem__("status","COMPLETE_NONMEMBER_MOD_PRIME")),
  "d11_linear_accepted":("d11",lambda r:r.__setitem__("rank",194006)),
  "d11_wrong_count":("d11",lambda r:r.__setitem__("column_orbits",1)),
  "d11_wall_overrun":("d11",lambda r:r.__setitem__("elapsed_seconds",300.0)),
  "d11_rss_overrun":("d11",lambda r:r.__setitem__("peak_rss_kib",8*1024*1024)),
  "d11_false_complete":("d11",lambda r:r.__setitem__("closure_complete",False)),
 }
 for name,(which,mut) in mutations.items():
  x=copy.deepcopy(base10);y=copy.deepcopy(base11);mut(x if which=="d10" else y);cases[name]=(run(x,y)!=0)
 cases["partial_complete_swap"]=(run(base10,base11,True)!=0)
 out={"status":"PASS" if all(cases.values()) else "FAIL","cases":cases,"fail_closed":True};Path(a.output).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n");print(json.dumps(out));raise SystemExit(0 if out["status"]=="PASS" else 1)
if __name__=="__main__":main()
