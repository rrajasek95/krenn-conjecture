#!/usr/bin/env python3
"""Independent fail-closed audit of the exact cap/eviction gate."""
import argparse,hashlib,json
from pathlib import Path
CHECKPOINT="d9f3a71525b2a5070d9e911b12f313a0d20e0d1763c3e3adfaa1294cb638f241"
def sha(p):
 h=hashlib.sha256()
 with open(p,"rb") as f:
  for b in iter(lambda:f.read(8<<20),b""):h.update(b)
 return h.hexdigest()
def ck(x,m):
 if not x:raise ValueError(m)
def main():
 p=argparse.ArgumentParser();p.add_argument("--results",required=True);p.add_argument("--binary",required=True);p.add_argument("--checkpoint",required=True);p.add_argument("--output");a=p.parse_args();r=json.load(open(a.results))
 ck(set(r)=={"status","scope","checkpoint_sha256","binary_sha256","runs","promotion_contract"},"schema mismatch");ck(r["status"]=="PASS" and r["scope"]=="bounded_capped_orbit_memo_gate_only","scope mismatch");ck(r["checkpoint_sha256"]==CHECKPOINT==sha(a.checkpoint),"checkpoint pin mismatch");ck(r["binary_sha256"]==sha(a.binary),"binary pin mismatch");ck(len(r["runs"])==8,"run count mismatch")
 for pattern,n in (("correlated",100_000),("adversarial",2_000)):
  q=[x for x in r["runs"] if x["pattern"]==pattern];ck(len(q)==4,"pattern cardinality mismatch");base=next(x for x in q if x["backend"]=="exact_cache")
  for cap in (100_000,250_000,400_000):
   x=next(y for y in q if y["backend"]=="orbit_memo_cap" and y["cap_entries"]==cap);ck(x["output_count"]==base["output_count"]==n and x["sorted_sha256"]==base["sorted_sha256"],"exact equality mismatch");ck(x["hits"]+x["misses"]==n and x["memo_entries"]<=cap and x["actions"]==1440,"cap/count mismatch");ck(x["repetitions"]==3 and len(x["timing_repetitions_seconds"])==3,"repetition mismatch")
 c=r["promotion_contract"];ck(c=={"adversarial_fallback_required":True,"broad_run_authorized":False,"cap_entries":400000,"fallback":"exact_cache","minimum_probe_hit_rate":.9,"minimum_probe_speedup":2.0,"probe_candidates":10000},"promotion contract mismatch")
 corr=next(x for x in r["runs"] if x["pattern"]=="correlated" and x["backend"]=="orbit_memo_cap" and x["cap_entries"]==400000);adv=next(x for x in r["runs"] if x["pattern"]=="adversarial" and x["backend"]=="orbit_memo_cap" and x["cap_entries"]==400000)
 ck(corr["hit_rate"]>=.9 and corr["throughput_ratio_vs_exact_cache"]>2,"correlated promotion gate failed");ck(adv["hit_rate"]<.1 and adv["throughput_ratio_vs_exact_cache"]<1,"adversarial fallback gate failed")
 out={"status":"PASS","exact_pairs":6,"promotion":"cap400k_only_after_probe","correlated_speedup":corr["throughput_ratio_vs_exact_cache"],"adversarial_slowdown":1/adv["throughput_ratio_vs_exact_cache"],"broad_run_authorized":False};
 if a.output:Path(a.output).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
 print(json.dumps(out,sort_keys=True))
if __name__=="__main__":main()
