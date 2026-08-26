#!/usr/bin/env python3
"""Bounded exact FIFO cap/eviction gate for the natural-minimum orbit memo."""
import argparse, hashlib, json, statistics, subprocess
from pathlib import Path

def sha(path):
 h=hashlib.sha256()
 with open(path,"rb") as f:
  for b in iter(lambda:f.read(8<<20),b""):h.update(b)
 return h.hexdigest()
def run(cmd):
 p=subprocess.run(cmd,capture_output=True,text=True)
 if p.returncode:raise RuntimeError({"cmd":cmd,"stderr":p.stderr})
 return json.loads(p.stdout)
def repeated(cmd,reps=3):
 xs=[run(cmd) for _ in range(reps)];assert len({(x["output_count"],x["sorted_sha256"]) for x in xs})==1
 r=dict(xs[0]);r["seconds"]=statistics.median(x["seconds"] for x in xs);r["timing_repetitions_seconds"]=[x["seconds"] for x in xs];r["peak_rss_kib"]=max(x["peak_rss_kib"] for x in xs);r["repetitions"]=reps;return r
def main():
 p=argparse.ArgumentParser();p.add_argument("--binary",required=True);p.add_argument("--checkpoint",required=True);p.add_argument("--output",required=True);a=p.parse_args();b=str(Path(a.binary).resolve());c=str(Path(a.checkpoint).resolve());runs=[]
 for pattern,n in (("correlated",100_000),("adversarial",2_000)):
  baseline=repeated([b,"canoncap",c,"exact_cache",pattern,str(n),"400000"]);runs.append(baseline)
  for cap in (100_000,250_000,400_000):
   x=repeated([b,"canoncap",c,"orbit_memo_cap",pattern,str(n),str(cap)])
   if (x["output_count"],x["sorted_sha256"])!=(baseline["output_count"],baseline["sorted_sha256"]):raise RuntimeError("capped natural-minimum mismatch")
   x["throughput_ratio_vs_exact_cache"]=baseline["seconds"]/x["seconds"];x["rss_ratio_vs_exact_cache"]=x["peak_rss_kib"]/baseline["peak_rss_kib"];runs.append(x)
 result={"status":"PASS","scope":"bounded_capped_orbit_memo_gate_only","checkpoint_sha256":sha(c),"binary_sha256":sha(b),"runs":runs,"promotion_contract":{"cap_entries":400_000,"probe_candidates":10_000,"minimum_probe_hit_rate":0.90,"minimum_probe_speedup":2.0,"fallback":"exact_cache","adversarial_fallback_required":True,"broad_run_authorized":False}}
 Path(a.output).write_text(json.dumps(result,indent=2,sort_keys=True)+"\n");print(json.dumps({"status":"PASS","output":a.output,"runs":len(runs)}))
if __name__=="__main__":main()

